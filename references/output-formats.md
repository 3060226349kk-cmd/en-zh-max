# 交付物脚本参考

仅在翻译落盘后执行。聊天小段翻译不需要。

## 全中文版派生

从英中对照 MD **用脚本机械派生**（删掉 `> ` 行），不要重打中文。

### Windows (git-bash)

```bash
python3 -c "
import re
src = r'<名称> 翻译(中英对照).md'
dst = r'<名称> 翻译(全中文).md'
lines = open(src, encoding='utf-8').read().split('\n')
kept = [ln for ln in lines if not ln.lstrip().startswith('>')]
open(dst, 'w', encoding='utf-8').write(re.sub(r'\n{3,}', '\n\n', '\n'.join(kept)).strip() + '\n')
"
```

### Linux/macOS

```bash
python3 - "<名称> 翻译(中英对照).md" "<名称> 翻译(全中文).md" <<'PY'
import sys, re
src, dst = sys.argv[1], sys.argv[2]
lines = open(src, encoding='utf-8').read().split('\n')
kept = [ln for ln in lines if not ln.lstrip().startswith('>')]
open(dst,'w',encoding='utf-8').write(re.sub(r'\n{3,}','\n\n','\n'.join(kept)).strip()+'\n')
PY
```

### 双语同入 blockquote 的变体

若选择**双语都在 blockquote 内**的排版（`> English...` + `> 中文...`），改用识别中文字符的脚本：

```bash
python3 -c "
import re
src = r'<名称> 翻译(中英对照).md'
dst = r'<名称> 翻译(全中文).md'
def has_cjk(s): return bool(re.search(r'[一-鿿㐀-䶿豈-﫿]', s))
lines = open(src, encoding='utf-8').read().split('\n')
out = []
for ln in lines:
    s = ln.lstrip()
    if s.startswith('>') and has_cjk(s):
        out.append(s[1:].strip())
    elif not s.startswith('>'):
        out.append(ln)
open(dst, 'w', encoding='utf-8').write('\n'.join(out).strip() + '\n')
"
```

> ⚠ 顺序要求：**先跑阶段 6 的标点归一，再派生全中文版**——派生脚本原样继承标点，不会再纠正。

## 输出 EPUB（纯中文单语）

翻译完成后（纯中文内容），用 ebooklib 生成：

```bash
python3 -c "
import os
from ebooklib import epub

book = epub.EpubBook()
book.set_identifier('your-book-id')
book.set_title('《书名》')
book.set_language('zh-CN')

md_path = r'《书名》 翻译(全中文).md'
with open(md_path, encoding='utf-8') as f:
    content = f.read()

chapters = content.split('## ')
for i, ch in enumerate(chapters):
    if not ch.strip(): continue
    lines = ch.strip().split('\n')
    title = lines[0].strip()
    body = '\n'.join(lines[1:]).strip()
    if not title: continue
    c = epub.EpubHtml(title=title, file_name=f'chap_{i}.xhtml', lang='zh-CN')
    c.content = f'<h2>{title}</h2><p>' + '</p><p>'.join(body.split('\n\n')) + '</p>'
    book.add_item(c)
    book.toc.append(c)
    book.spine.append(c)

style = 'body { font-family: serif; line-height: 1.8; padding: 1em; }'
nav_css = epub.EpubItem(uid='style', file_name='style.css', media_type='text/css', content=style.encode('utf-8'))
book.add_item(nav_css)
for item in book.items:
    if isinstance(item, epub.EpubHtml):
        item.add_item(nav_css)

epub_path = r'《书名》 译文.epub'
epub.write_epub(epub_path, book, {})
print(f'EPUB => {epub_path}')
"
```

## 输出 MOBI 电子书

用 Kindle Previewer 3 内置的 kindlegen 从 EPUB 转换：

```bash
KINDLEGEN="/path/to/kindlegen.exe"  # 替换为你的 kindlegen 实际路径（e.g. Kindle Previewer 3 安装目录）
"$KINDLEGEN" "<名称>.epub"
```

- 输入推荐用 EPUB（ebooklib 生成），kindlegen 自动输出同目录 MOBI
- 警告（如无封面）不影响生成，退出码 1 = 有警告但成功

## 输出 PDF 封装（按需）

PDF **默认不生成**，仅在用户明确要求时执行：

```bash
python3 "$SKILL_DIR/scripts/bilingual-to-pdf.py" "<名称> 翻译(中英对照).md" --title "书名" --author "作者"
```

脚本功能：解析 blockquote 格式 → Warm Paper HTML → Playwright 渲染 A4 PDF。

> **设计系统选择：** 翻译/小说类 → 默认暖纸；试卷/学习类 → `--theme navy`。

依赖（只需安装一次）：
```bash
pip install playwright && python3 -m playwright install chromium
```

详见 `references/playwright-pdf-generation.md` 和 `references/bilingual-html-template.md`。
