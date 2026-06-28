# EPUB 文本提取

适用于 `.epub` 格式电子书的纯文本提取。EPUB 本质是一个 ZIP 包（含 XHTML + CSS + 图片）。

> ⚠ **前置条件**：原始 `.epub` 文件必须已移入项目的 `source/` 子目录（见 SKILL.md 阶段 -1 步骤 2）。以下所有示例假设文件已在 `source/` 内，提取产物也写入 `source/`。

## 方法一：Python zipfile（推荐，最可靠）

提取所有 XHTML，用正则去掉 HTML 标签，取纯文本。适合大文件、复杂排版。

```python
import zipfile, re, html, os

# project_dir 已在 SKILL.md 阶段 -1 步骤 1 中定义
source_dir = os.path.join(project_dir, 'source')
epub_path = os.path.join(source_dir, '原书名.epub')

z = zipfile.ZipFile(epub_path)

def extract_text(xhtml_bytes):
    text = xhtml_bytes.decode('utf-8')
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    # 清除排版噪声
    text = re.sub(r'FInal_ebook_Lunar_Trilogy_11272020', '', text)  # 按需调整
    text = re.sub(r'\s*\n\s*', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# 列出内容
for name in z.namelist():
    print(name)

# 遍历所有 XHTML 文件，产物写入 source/
for name in z.namelist():
    if name.endswith('.xhtml'):
        txt = extract_text(z.read(name))
        fname = os.path.basename(name).replace('.xhtml', '.txt')
        with open(os.path.join(source_dir, fname), 'w', encoding='utf-8') as f:
            f.write(txt)
```

## 方法二：Pandoc

适合简单 EPUB（无复杂内嵌字体/排版）：

```bash
# Pandoc 在 C:\pandoc-3.9 的场合
# 输入输出均指向 source/ 子目录
/c/pandoc-3.9/pandoc.exe "source/书.epub" -t plain -o "source/书.txt"
```

## 方法三：Calibre ebook-convert

Calibre 的 `ebook-convert` 工具支持最广泛的格式：

```bash
# 获取路径
where ebook-convert
# 或指定路径；输入输出均指向 source/ 子目录
"D:\Calibre\Calibre Portable\Calibre\ebook-convert.exe" "source/书.epub" "source/书.txt"
```

## 常见问题

| 问题 | 解决 |
|------|------|
| XHTML 中章节标题无 `<h1>`/`<h2>` 包裹 | 检查 `<p class="...">` 的 CharOverride 类名，章节标题通常用特殊样式类 |
| 提取后文件头有书名/ID 噪声行 | 用 `re.sub()` 清洗 |
| 大 EPUB 内嵌字体使体积大 | Pandoc 可能内存不足，Python zipfile 无此问题 |
| Windows 路径问题 | Python 里用 `r'C:\路径'` 原始字符串，git-bash 里用 `/c/路径` |
