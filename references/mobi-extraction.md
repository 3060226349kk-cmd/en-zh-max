# 电子书文本提取（Windows）

根据文件格式分流提取，**只对 Pandoc 支持的格式用 Pandoc**。

> ⚠ **前置条件**：原始文件必须已移入项目的 `source/` 子目录（见 SKILL.md 阶段 -1 步骤 2）。以下所有命令假设输入文件已在 `source/` 内，提取产物也写入 `source/`。

## 提取优先级（按格式分流）

```
.epub
  └── 见 references/epub-extraction.md（Python zipfile 优先，Pandoc/Calibre 备选）

.docx / .html / .md 等 Pandoc 支持的格式
  └── Pandoc 🥇（C:\pandoc-3.9\pandoc.exe -t markdown --wrap=none -o source/出力.md source/入力ファイル）

.mobi
  └── Python mobi 模块（Pandoc 不支持 mobi 输入）

.azw3
  └── Calibre ebook-convert 🥇
      └── D:\Calibre\Calibre Portable\Calibre\ebook-convert.exe（已安装）
```

## 🥇 方案一：Pandoc（.docx / .html / .md）

**路径：`C:\pandoc-3.9\pandoc.exe`**

```bash
"C:\pandoc-3.9\pandoc.exe" "source/输入文件.docx" -t markdown --wrap=none -o "source/输出文件.md"
```

- `-t markdown --wrap=none` 输出 Markdown，保留标题层级（`#`/`##`/`###`）与目录结构
- 硬文本（法律/合同等）如需纯文本，可换 `-t plain`
- 支持输入：`.docx`, `.html`, `.markdown`, `.latex`, `.rst`, `.org` 等 50+ 格式
- **不支持**输入：`.mobi`, `.azw3`（也不作为 .epub 首选，见 epub-extraction.md）

## 🥇 方案二：Calibre ebook-convert（.azw3 / .mobi fallback）

**路径：`D:\Calibre\Calibre Portable\Calibre\ebook-convert.exe`**（已在用户机器上安装）

```bash
"D:\Calibre\Calibre Portable\Calibre\ebook-convert.exe" "source/输入文件.azw3" "source/输出文件.txt"
```

- 支持输入：`.azw3`, `.mobi`, `.prc`, `.epub`, `.docx`, `.pdf` 等大量格式
- 输出为 `.txt` 即纯文本
- 也可输出 `.html` 保留格式：`... source/输出文件.html`

## 🥈 方案三：Python `mobi` 模块（.mobi 专有 fallback）

当 Pandoc 和 Calibre 都不适用时，用于 `.mobi` 格式。

```python
import mobi, shutil, re, os

# source_dir 已在 SKILL.md 阶段 -1 步骤 1 中定义
mobi_path = os.path.join(source_dir, '原书名.mobi')
temp_dir, extracted_path = mobi.extract(mobi_path)

with open(extracted_path, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# 陷阱：不能直接用 re.sub(r'<[^>]+>', '', content) 去标签——
# 这会丢失所有段落结构，全文压成一行，不可逆。
# 必须先将 <p>/<div>/<br> 替换为换行，再去标签：
content = re.sub(r'</?p[^>]*>', '\n\n', content)
content = re.sub(r'</?div[^>]*>', '\n\n', content)
content = re.sub(r'<br\s*/?>', '\n', content)
content = re.sub(r'<mbp:[^>]+>', '', content)

# ★ 标题映射：去标签前将 <h1>~<h4> 转为 Markdown（保留目录结构）
content = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', content, flags=re.DOTALL)
content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', content, flags=re.DOTALL)
content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', content, flags=re.DOTALL)
content = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1', content, flags=re.DOTALL)

# 去 HTML 标签
clean = re.sub(r'<[^>]+>', '', content)
clean = clean.replace('&nbsp;', ' ').replace('&amp;', '&')
clean = clean.replace('&lt;', '<').replace('&gt;', '>')
clean = clean.replace('&quot;', '"').replace('&#39;', "'").replace('&#8217;', "'")
clean = clean.replace('&#8230;', '…').replace('&#8212;', '—').replace('&#8211;', '–')
clean = re.sub(r' +', ' ', clean)
clean = re.sub(r'\n{3,}', '\n\n', clean)
clean = clean.strip()

# 产物写入 source/（.md 保留目录结构）
output_path = os.path.join(source_dir, '原书名_提取.md')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(clean)

shutil.rmtree(temp_dir, ignore_errors=True)
```

## ⚠ 切记：保留提取后的 .md 文件

**不要删除提取后的 `.md` 文件。** 翻译过程中需要反复引用原文核对段落边界和术语位置。
**避险方法**：「先 query，后 action」——每次遇到新格式，先跑 `--list-input-formats` 确认支持，不要凭印象。

### 不支持格式硬跑 = 浪费时间

如果 Pandoc 不支持的格式（如 `.mobi`），直接硬跑会：
- 报 `Unknown reader: mobi` 错误
- 或输出空文件
不要尝试用 `-f mobi` 硬绕——Pandoc 没有对应的 reader，硬跑的结局只有报错。

## 注意

- `mobi.extract()` 返回的路径在 `temp_dir` 中，必须用 `shutil.rmtree` 清理
- 提取的 HTML 含大量 `<span>` / `<font>` 标签，必须用正则去除
- 分幕切割时注意 `DIALOGUE THE SEVENTH AND LAST` 的特殊命名
- 保存两份文本：原始 HTML 提取（保留格式标记）+ 去标签后的 Markdown（便于阅读）
