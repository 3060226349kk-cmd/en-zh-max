# 翻译 PDF 生成（Playwright HTML→PDF）

中英对照翻译完成后，封装为精美 PDF 的推荐路径。

## 推荐路径：一键脚本

```bash
python3 "$SKILL_DIR/scripts/bilingual-to-pdf.py" \
  "《书名》/《书名》 翻译(中英对照).md" --title "书名" --author "作者"
```

脚本自动完成：解析双语 Markdown → 生成 CEU Navy HTML → Playwright 渲染 A4 PDF。

## 为什么不选其他方案

| 方案 | Windows 可行性 | 问题 |
|---|---|---|
| WeasyPrint | ❌ 不适用 | 依赖 GTK/libgobject（Windows 无预装） |
| `fpdf2` / `reportlab` | ✅ 可用 | 纯程序化排印，无 CSS，排版成本高 |
| **Playwright HTML→PDF** | **✅ 推荐** | 浏览器渲染 = 精确 CSS 支持，CEU Academic Navy 设计可直接应用 |

## 排版陷阱（大量实测经验）

以下陷阱按出现频率排列，生成 PDF 前必须逐项检查 CSS：

### ① 双重边距冲突（最常见）

**问题**：CSS `@page` 设置了 `margin`，Playwright `page.pdf()` 又传了 `margin` 参数 → 两者可能冲突，导致实际渲染与浏览器预览不一致。

**修复**：CSS `@page` 中设置边距，Playwright 的 `page.pdf()` **不传** `margin` 参数，让 CSS 全权控制。

```css
@page { size: A4; margin: 30mm 25mm 30mm 25mm; }
```

```python
# Playwright 不传 margin 参数
page.pdf(path=pdf_path, format="A4", print_background=True)
```

### ② scale=0.9 导致文字错位

**问题**：`scale=0.9` 缩小整个页面内容，导致文字在 A4 边界附近出现错位、溢出的视觉问题。

**修复**：**不要传 `scale` 参数**。边距应通过 CSS `@page` 和内部 padding 控制，而非缩放。

### ③ blockquote 右侧 padding 为零

**问题**：blockquote 的 CSS 如果只设 `padding-left` 不设 `padding-right`，灰色背景右侧会顶到容器边缘，文字看起来「死在边框上」。

**修复**：blockquote 的左右 padding 必须对称：

```css
blockquote {
    padding: 8px 20px;          /* 左右对称 */
    margin: 0.8em 24px;         /* 与容器边缘拉开距离 */
}
```

而不是：`padding: 4px 0 4px 16px;`（右 padding=0 ❌）

### ④ 容器 padding 过小

**问题**：`.container` 的水平 padding 太小（如 `padding: 30px 10px;`），导致文字几乎紧贴内容区边缘。

**修复**：用 `@page` 边距控制物理页边距，容器内不做额外约束 → 移除 container 的 padding/max-width：

```css
.container { max-width: 100%; margin: 0; padding: 0; }
```

### ⑤ 中文段落 text-indent 与其他 margin 不协调

中文段落标准用 `text-indent: 2em` 首行缩进，与 blockquote 的 `text-indent: 0` 形成明确区分。行距建议 `1.8-1.9` 适合双语排版。

## 视觉验证：生成 PDF 前先在浏览器预览

PDF 的视觉问题（文字贴边、溢页、背景延伸）在浏览器中就能发现。

```bash
# 1. 在 Hermes 浏览器中打开 HTML 文件
browser_navigate(url="file:///C:/path/to/translation.html")

# 2. 用视觉模型截屏检查布局
browser_vision(question="检查页面布局：1) blockquote灰色背景是否贴着左右边缘？2) 文字离页面左右边缘多远？3) 页面底部是否有文字紧贴下边缘？")
```

## Playwright PDF 生成代码（备用）

```python
from playwright.sync_api import sync_playwright

html_path = r"C:\path\to\translation.html"
pdf_path = r"C:\path\to\output.pdf"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    file_url = "file:///" + html_path.replace("\\", "/")
    page.goto(file_url, wait_until="networkidle")
    page.pdf(path=pdf_path, format="A4", print_background=True)
    browser.close()
```

> `print_background=True` 必须在 `page.pdf()` 里设置。

## 千万注意

- `file:///` URL 必须用正斜杠（`/`），Windows 反斜杠需替换
- **不要**同时使用 `@page` CSS 边距 + `page.pdf(margin=...)` 双重设置（见陷阱①）
- **不要**使用 `scale` 参数（见陷阱②）
