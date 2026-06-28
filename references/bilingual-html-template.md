# 英中对照 HTML 模板与解析器模式

Markdown→精美 HTML→PDF 的完整管道。核心难点不是 Playwright 参数，而是**解析双语 Markdown 并正确配对英文与中文**。

**一键脚本**：`scripts/bilingual-to-pdf.py` 是此管道的生产级实现，读 Markdown → 生成 HTML → 渲染 PDF，一条命令完成。详见 SKILL.md「输出 PDF 封装（一键脚本）」节。

以下内容是脚本内部的解析器逻辑与 CSS 设计参考，供需要自定义或调试时查阅。

## 双语 Markdown 的两种格式

### 格式 A：英文+中文，全部 blockquote（推荐，阅览器显示一致）

```markdown
> The night here isn't very dark, it's much brighter than full moon nights on Earth.

> 这里的夜并不很暗，比地球上满月之夜还要亮得多。
```

**优点**：在纯文本阅读器（VS Code、终端）中也能清晰区分英中。
**缺点**：解析器需要 CJK 字符检测来区分英文行和中文行。

### 格式 B：英文 blockquote，中文无标记（skill 原定标准格式）

```markdown
> The night here isn't very dark, it's much brighter than full moon nights on Earth.

这里的夜并不很暗，比地球上满月之夜还要亮得多。
```

**优点**：解析简单，无歧义。
**缺点**：纯文本阅读器中中文与英文混排，不易区分。

> **建议**：翻译时用格式 B（标准格式），导出 HTML/PDF 时无差别。如果用户同时需要纯文本查看，用格式 A。

## 解析器模式（Python）

核心逻辑：逐行遍历，遇到 `>` 行时，收集连续英文行 → 遇到有 CJK 字符的 `>` 行则作为中文译文 → 配对输出。

**生产代码见**：`scripts/bilingual-to-pdf.py` 中的 `parse_bilingual()` 函数，支持格式 B（标准）下三种变体：
- 纯英文 `>` 行 + 紧接中文段落 → pair
- 翻译说明 `> **...**` 行 → notes 块
- 标题 `##` → heading
- `---` 分隔线 → sep

### 格式 A 解析（全部 blockquote，备用）

```python
def has_cjk(s):
    return any('\u4e00' <= c <= '\u9fff' or '\u3400' <= c <= '\u4dbf' or '\uf900' <= c <= '\ufaff' for c in s)

entries = []  # [{'en': [lines], 'cn': str}, ...]
i = 0
while i < len(lines):
    raw = lines[i].rstrip('\r')
    if not raw.strip():
        i += 1; continue
    if raw.strip() == '---':
        entries.append({'type': 'sep'}); i += 1; continue
    if raw.startswith('## '):
        entries.append({'type': 'heading', 'text': raw[3:].strip()}); i += 1; continue

    if raw.lstrip().startswith('> '):
        content = raw[raw.index('> ')+2:].strip()
        if has_cjk(content):
            # Standalone Chinese line (e.g. translation notes in blockquote)
            entries.append({'type': 'cn_standalone', 'text': content})
            i += 1
        else:
            en_paras = [content]
            i += 1
            cn_text = ''
            while i < len(lines):
                nxt = lines[i].rstrip('\r')
                if nxt.lstrip().startswith('> '):
                    t = nxt[nxt.index('> ')+2:].strip()
                    if t and has_cjk(t):
                        cn_text = t; i += 1; break
                    elif t:
                        en_paras.append(t); i += 1
                    else:
                        i += 1; continue  # empty > line
                elif not nxt.strip():
                    i += 1; continue
                else:
                    break
            entries.append({'type': 'pair', 'en': en_paras, 'cn': cn_text})
        continue

    entries.append({'type': 'text', 'text': raw.strip()})
    i += 1
```

### 格式 B 解析（英文 blockquote，中文无标记）

更简单：遇到 `>` 行收集连续英文，然后跳过空行取下一个非空、非 `>` 行作为中文。

```python
if raw.lstrip().startswith('> '):
    en_paras = [raw[raw.index('> ')+2:].strip()]
    i += 1
    while i < len(lines):
        nxt = lines[i].rstrip('\r')
        if nxt.lstrip().startswith('> '):
            t = nxt[nxt.index('> ')+2:].strip()
            if t: en_paras.append(t); i += 1
            else: i += 1; continue
        else:
            break
    # Skip blanks
    while i < len(lines) and not lines[i].strip():
        i += 1
    cn_text = ''
    if i < len(lines):
        nxt = lines[i].rstrip('\r')
        if nxt.strip() and not nxt.lstrip().startswith('> '):
            cn_text = nxt.strip()
            i += 1
    entries.append({'type': 'pair', 'en': en_paras, 'cn': cn_text})
```

## CEU Academic Navy CSS 模板

### 文学/小说类（长篇叙事，Spectral+Noto Serif SC）

完整 CSS 见 `scripts/bilingual-to-pdf.py` 中的 `CEU_NAVY_CSS` 常量。核心变量如下：

```css
:root {
  --supply:#143a6b; --demand:#1f86a8; --equi:#a87f2e;
  --text-primary:#11243f; --text-secondary:#5a6c86;
  --text-tertiary:#8a99ad; --border:#d9e1ee; --border-light:#e8edf6;
}

body {
  background: radial-gradient(120% 60% at 50% -10%, #f5f8fd, transparent 55%),
              linear-gradient(180deg, #eef2f9, #e7eef7);
  font-family: 'Public Sans','Noto Sans SC',system-ui,sans-serif;
  font-size: 14.5px; line-height: 1.75;
}
.page { max-width: 740px; margin: 0 auto; padding: 2.5rem 2rem; }

/* 封面 */
.cover { text-align: center; padding: 3rem 0 2rem; border-bottom: 2px solid var(--border-light); }
.cover h1 { font-family: 'Spectral','Noto Serif SC',serif; font-size: clamp(24px,3vw,32px); font-weight: 600; color: var(--supply); }

/* 章节标题 */
.ch-header { margin: 2.2rem 0 1.2rem; padding: 1.2rem 0; text-align: center;
  border-top: 1px solid var(--border-light); border-bottom: 1px solid var(--border-light); }
.ch-header .en { font-family: 'Spectral', serif; font-size: 20px; font-weight: 500; color: var(--supply); }
.ch-header .cn { font-family: 'Noto Serif SC', serif; font-size: 16px; color: var(--text-primary); }

/* 双语条目 */
.pair { margin: 1rem 0; }
.pair blockquote {
  font-family: 'Spectral','Noto Serif SC',serif;
  font-size: 13px; line-height: 1.6; color: var(--text-secondary);
  border-left: 3px solid var(--demand);
  padding: 0.2rem 0 0.2rem 1rem;
  margin: 0 0 0.3rem 0;
}
.pair .cn {
  font-family: 'Public Sans','Noto Sans SC',system-ui,sans-serif;
  font-size: 14.5px; line-height: 1.8; color: var(--text-primary);
  padding-left: 1rem; text-indent: 2em;
}

/* 标注块（翻译说明等） */
.notes { padding: 1rem 1.5rem; background: #f0f4f8; border-radius: 6px;
  font-family: 'Noto Sans SC', sans-serif; font-size: 11px; line-height: 1.7; color: var(--text-secondary); }

/* 打印 */
@media print {
  body { background: white !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .page { padding: 0.6in 0.5in; }
  .pair { break-inside: avoid; page-break-inside: avoid; }
}
```

### 戏剧/对白类（分段人物名+对话，Spectral+Noto Serif TC）

与小说类的差异：
- 封面文本变更为剧名
- 新增 `act-header` 类（幕标题，含英文名+中文名+人物列表）
- 双语条目内可含舞台指示（斜体+淡色）
- 字体用 TC（繁体）而非 SC（简体），因萨德这类欧洲经典常用繁体中文出版

```css
/* 幕标题（新增） */
.act-header { margin: 2.5rem 0 1.2rem; padding: 1.5rem 0; text-align: center;
  border-top: 1px solid var(--border-light); border-bottom: 1px solid var(--border-light); }
.act-header .en { font-family: 'Spectral',serif; font-size: 22px; font-weight: 500; color: var(--supply); letter-spacing: 0.12em; }
.act-header .en-chars { font-size: 13px; color: var(--text-secondary); font-style: italic; }
.act-header .cn { font-family: 'Noto Serif TC',serif; font-size: 17px; color: var(--text-primary); }

/* 舞台指示 */
.sd { font-family: 'Spectral','Noto Serif TC',serif; font-size: 13px; font-style: italic;
  color: var(--text-tertiary); padding-left: 1rem; }

/* 说话人高亮 */
.pair .cn .sp { font-weight: 600; color: var(--micro); }
```

## 验证：配对计数

HTML 生成后必须验证英中配对数正确，避免解析器漏配对：

```python
import re
html = open('output.html', encoding='utf-8').read()
pairs = len(re.findall(r'<div class="pair">', html))
# 检查每个 pair 内是否都有 .cn
pair_blocks = re.findall(r'<div class="pair">(.*?)</div>', html, re.DOTALL)
cn_in_pairs = sum(1 for pb in pair_blocks if '<div class="cn">' in pb)
bq_only = sum(1 for pb in pair_blocks if '<div class="cn">' not in pb)
print(f'Total pairs: {pairs} | With CN: {cn_in_pairs} | CN missing: {bq_only}')
# bq_only 必须为 0
```

## 整条管道调用方式

```python
# 1. 读取 Markdown
# 2. 调用解析器 → entries list
# 3. 选择 CSS 模板（文学 vs 戏剧）
# 4. 渲染 HTML
# 5. 验证配对计数
# 6. 浏览器预览（browser_navigate + browser_vision）
# 7. Playwright 转 PDF（不传 scale/margin，由 CSS @page 控制）
```

**全都已封装为一条命令**：`python3 "$SKILL_DIR/scripts/bilingual-to-pdf.py" "路径/文件.md" --title "标题" --author "作者"`。
