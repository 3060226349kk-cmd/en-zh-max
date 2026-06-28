#!/usr/bin/env python3
"""
bilingual-to-pdf.py — 双语对照 Markdown → HTML + PDF

默认主题：暖纸质感（Warm Paper），适用于翻译/小说。
海军蓝主题（Navy）用于试卷/学习类：--theme navy

用法：
    python3 bilingual-to-pdf.py "<名称> 翻译(中英对照).md" [--title "书名"] [--author "作者"] [--theme navy]

输出：与输入文件同目录下生成同名 .html 和 .pdf 文件。

依赖：pip install playwright && python3 -m playwright install chromium

解析格式 B：英文 blockquote（> 开头）+ 中文无标记正文
"""

import re
import os
import sys
import argparse

# ── CSS 主题 ─────────────────────────────────────────────────────

WARM_PAPER_CSS = r"""
:root {
  --bg: #faf8f5;
  --bg-page: #f5f0e8;
  --text: #1a1a1a;
  --text-light: #5a5a5a;
  --text-tertiary: #888;
  --accent: #8b3a3a;
  --accent-light: #c49b9b;
  --border: #d4c9b5;
  --quote-bg: #f3efe8;
  --shadow: rgba(0,0,0,0.06);
  --font-serif: 'Spectral','Noto Serif SC','Source Han Serif SC','STSong','SimSun',Georgia,serif;
  --font-sans: 'Public Sans','Noto Sans SC','PingFang SC','Microsoft YaHei',system-ui,sans-serif;
}

@page { size: A4; margin: 25mm 22mm 25mm 22mm; }

body {
  background: var(--bg-page);
  font-family: var(--font-sans);
  font-size: 15px; line-height: 1.9; color: var(--text);
  margin: 0; padding: 0;
  -webkit-font-smoothing: antialiased;
}

.page { max-width: 780px; margin: 0 auto; background: var(--bg); padding: 1.5rem 1rem; box-shadow: 0 0 30px var(--shadow); }

.cover { text-align: center; padding: 2.5rem 0 1.5rem; border-bottom: 1px solid var(--border); margin-bottom: 2rem; }
.cover h1 { font-family: var(--font-serif); font-size: clamp(24px,3.2vw,34px); font-weight: 600; color: var(--text); margin: 0.3rem 0; letter-spacing: 0.05em; }
.cover .sub { font-family: var(--font-serif); font-size: 15px; color: var(--text-light); }

.pair { margin: 0.9rem 0; page-break-inside: avoid; break-inside: avoid; }
.pair blockquote {
  font-family: var(--font-serif);
  font-size: 13.5px; line-height: 1.65; color: var(--text-light);
  border-left: 3px solid var(--accent-light);
  padding: 0.15rem 0 0.15rem 1rem; margin: 0 0 0.15rem 0;
}
.pair blockquote p { margin: 0.2rem 0; }
.pair .cn {
  font-family: var(--font-sans);
  font-size: 15px; line-height: 1.9; color: var(--text);
  padding-left: 1rem; text-indent: 2em;
}

.notes {
  padding: 0.8rem 1.5rem; margin: 1rem 0;
  background: var(--quote-bg);
  border-left: 3px solid var(--accent);
  border-radius: 0 6px 6px 0;
  font-size: 11px; line-height: 1.7; color: var(--text-light);
}
.notes p { margin: 0.3rem 0; }

.sep { text-align: center; color: var(--border); font-size: 18px; margin: 1.2rem 0; letter-spacing: 1em; }

@media print {
  body { background: white !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .page { box-shadow: none; padding: 0; background: white !important; }
  .pair blockquote { border-left-color: var(--accent-light) !important; }
}
"""

CEU_NAVY_CSS = r"""
:root {
  --supply:#143a6b; --demand:#1f86a8; --equi:#a87f2e;
  --text-primary:#11243f; --text-secondary:#5a6c86;
  --text-tertiary:#8a99ad; --border:#d9e1ee; --border-light:#e8edf6;
}

@page { size: A4; margin: 25mm 22mm 25mm 22mm; }

body {
  background: radial-gradient(120% 60% at 50% -10%, #f5f8fd, transparent 55%),
              linear-gradient(180deg, #eef2f9, #e7eef7);
  font-family: 'Public Sans','Noto Sans SC','Noto Sans TC',system-ui,sans-serif;
  font-size: 14.5px; line-height: 1.85; color: var(--text-primary);
  margin: 0; padding: 0;
  -webkit-font-smoothing: antialiased;
}

.page { max-width: 780px; margin: 0 auto; padding: 1.5rem 1rem; }

.cover { text-align: center; padding: 2.5rem 0 1.5rem; border-bottom: 2px solid var(--border-light); margin-bottom: 2rem; }
.cover h1 { font-family: 'Spectral','Noto Serif SC','Noto Serif TC',serif; font-size: clamp(24px,3.2vw,34px); font-weight: 600; color: var(--supply); margin: 0.3rem 0; letter-spacing: 0.05em; }
.cover .sub { font-family: 'Spectral',serif; font-size: 15px; color: var(--text-secondary); font-style: italic; }

.pair { margin: 0.9rem 0; page-break-inside: avoid; break-inside: avoid; }
.pair blockquote { font-family: 'Spectral','Noto Serif SC','Noto Serif TC',serif; font-size: 13px; line-height: 1.6; color: var(--text-secondary); border-left: 3px solid var(--demand); padding: 0.15rem 0 0.15rem 1rem; margin: 0 0 0.15rem 0; }
.pair blockquote p { margin: 0.2rem 0; }
.pair .cn { font-family: 'Public Sans','Noto Sans SC','Noto Sans TC',system-ui,sans-serif; font-size: 14.5px; line-height: 1.85; color: var(--text-primary); padding-left: 1rem; text-indent: 2em; }

.notes { padding: 0.8rem 1.5rem; margin: 1rem 0; background: rgba(20,58,107,0.04); border-left: 3px solid var(--supply); border-radius: 0 6px 6px 0; font-family: 'Noto Sans SC',sans-serif; font-size: 11px; line-height: 1.7; color: var(--text-secondary); }
.notes p { margin: 0.3rem 0; }
.sep { text-align: center; color: var(--border); font-size: 18px; margin: 1.2rem 0; letter-spacing: 1em; }

@media print { body { background: white !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; } .page { padding: 0; } .notes { background: #f7f9fc !important; } .pair blockquote { border-left-color: var(--demand) !important; } }
"""

THEMES = {
    'warm': {'css': WARM_PAPER_CSS, 'fonts_url': 'https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Public+Sans:wght@300;400;500;600&family=Noto+Sans+SC:wght@300;400;500;700&family=Noto+Serif+SC:wght@400;500;600;700&display=swap'},
    'navy': {'css': CEU_NAVY_CSS, 'fonts_url': 'https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Public+Sans:wght@300;400;500;600&family=Noto+Sans+SC:wght@300;400;500;700&family=Noto+Serif+SC:wght@400;500;600;700&display=swap'},
}


# ── PARSER ────────────────────────────────────────────────────────

def has_cjk(s):
    return any('\u4e00' <= c <= '\u9fff' or '\u3400' <= c <= '\u4dbf' or '\uf900' <= c <= '\ufaff' for c in s)


def parse_bilingual(lines):
    """解析格式 B：英文 blockquote + 中文无标记"""
    entries = []
    i = 0
    while i < len(lines):
        raw = lines[i].rstrip('\r\n')
        if not raw.strip():
            i += 1
            continue
        if raw.strip() == '---':
            entries.append({'type': 'sep'})
            i += 1
            continue
        if raw.startswith('## '):
            entries.append({'type': 'heading', 'text': raw[3:].strip()})
            i += 1
            continue

        # 翻译说明 block > **...**
        if raw.startswith('> **'):
            note_lines = [raw[2:].strip()]
            i += 1
            while i < len(lines):
                ln = lines[i].rstrip('\r\n')
                if ln.lstrip().startswith('> '):
                    note_lines.append(ln[ln.index('> ')+2:].strip())
                    i += 1
                else:
                    break
            entries.append({'type': 'notes', 'text': '<br>'.join(note_lines)})
            continue

        if raw.lstrip().startswith('> '):
            en_paras = []
            while i < len(lines):
                ln = lines[i].rstrip('\r\n')
                if ln.lstrip().startswith('> '):
                    content = ln[ln.index('> ')+2:].strip()
                    if content:
                        en_paras.append(content)
                    i += 1
                elif ln.strip() == '':
                    i += 1
                    continue
                else:
                    break
            # 跳过空行找中文
            while i < len(lines) and not lines[i].strip():
                i += 1
            cn_text = ''
            if i < len(lines):
                nxt = lines[i].rstrip('\r\n')
                if nxt.strip() and not nxt.lstrip().startswith('> '):
                    cn_text = nxt.strip()
                    i += 1
            entries.append({'type': 'pair', 'en': en_paras, 'cn': cn_text})
            continue

        # 普通文字
        if raw.startswith('#'):
            entries.append({'type': 'text', 'text': raw})
        else:
            entries.append({'type': 'text', 'text': raw})
        i += 1

    return entries


# ── HTML 生成 ─────────────────────────────────────────────────────

def build_html(entries, title="", author="", theme='warm'):
    t = THEMES.get(theme, THEMES['warm'])
    lines_html = [
        '<!DOCTYPE html>',
        '<html lang="zh-CN">',
        '<head>',
        '<meta charset="utf-8">',
        f'<title>{title or "双语对照"}</title>',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        f'<link href="{t["fonts_url"]}" rel="stylesheet">',
        f'<style>\n{t["css"]}\n</style>',
        '</head>',
        '<body>',
        '<div class="page">',
    ]

    # 封面
    lines_html.append('<div class="cover">')
    if title:
        lines_html.append(f'  <h1>{title}</h1>')
    if author:
        lines_html.append(f'  <div class="sub">{author}</div>')
    lines_html.append('</div>')

    for e in entries:
        if e['type'] == 'pair':
            en_html = ''.join(f'<p>{p}</p>' for p in e['en'])
            cn_html = e['cn']
            block = f'<div class="pair"><blockquote>{en_html}</blockquote>'
            if cn_html:
                block += f'<div class="cn">{cn_html}</div>'
            block += '</div>'
            lines_html.append(block)
        elif e['type'] == 'heading':
            lines_html.append(
                f'<h2 style="font-family:Spectral,serif;color:var(--supply);'
                f'text-align:center;margin:1.5rem 0 0.5rem;">{e["text"]}</h2>')
        elif e['type'] == 'notes':
            lines_html.append(f'<div class="notes"><p>{e["text"]}</p></div>')
        elif e['type'] == 'sep':
            lines_html.append('<div class="sep">· · ·</div>')
        elif e['type'] == 'text':
            t = e['text']
            if t.startswith('#'):
                level = len(t) - len(t.lstrip('#'))
                text = t.strip('#').strip()
                tag = f'h{min(level + 1, 4)}'
                lines_html.append(
                    f'<{tag} style="text-align:center;color:var(--supply);'
                    f'margin:1.2rem 0 0.5rem;">{text}</{tag}>')
            else:
                lines_html.append(
                    f'<p style="text-align:center;color:var(--text-secondary);'
                    f'font-size:13px;">{t}</p>')

    lines_html.append('</div></body></html>')
    return '\n'.join(lines_html)


# ── PDF 生成 ──────────────────────────────────────────────────────

def generate_pdf(html_path, pdf_path, timeout=30000):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        file_url = "file:///" + html_path.replace("\\", "/")
        page.goto(file_url, wait_until="networkidle", timeout=timeout)
        page.pdf(path=pdf_path, format="A4", print_background=True)
        browser.close()


# ── MAIN ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="双语对照 Markdown → HTML + PDF")
    parser.add_argument("input", help="双语对照 Markdown 文件路径")
    parser.add_argument("--title", default="", help="书籍/文档标题")
    parser.add_argument("--author", default="", help="作者名")
    parser.add_argument("--theme", default="warm", choices=['warm', 'navy'],
                        help="主题：warm=暖纸(默认，适用于翻译/小说)，navy=海军蓝(适用于试卷/学习)")
    parser.add_argument("--timeout", type=int, default=30000,
                        help="Playwright 页面加载超时(ms)，默认 30000")
    args = parser.parse_args()

    src = args.input
    if not os.path.isfile(src):
        print(f"错误：找不到文件 {src}", file=sys.stderr)
        sys.exit(1)

    base = os.path.splitext(src)[0]
    out_html = base + ".html"
    out_pdf = base + ".pdf"

    with open(src, encoding='utf-8') as f:
        md_lines = f.readlines()

    entries = parse_bilingual(md_lines)

    # 验证：所有 pair 必须含中文
    pairs = [e for e in entries if e['type'] == 'pair']
    cn_missing = sum(1 for e in pairs if not e['cn'])
    if cn_missing:
        print(f"警告：{cn_missing} 组英中配对缺少中文译文（将被跳过）",
              file=sys.stderr)
        for e in pairs:
            if not e['cn']:
                print(f"  -> 缺少译文：{e['en'][0][:60]}...", file=sys.stderr)

    print(f"条目：{len(entries)} | 英中配对：{len(pairs)} | 缺中文：{cn_missing} | 主题：{args.theme}")

    html = build_html(entries, title=args.title, author=args.author, theme=args.theme)
    with open(out_html, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"HTML => {out_html}")

    print("正在生成 PDF（Playwright）...")
    generate_pdf(out_html, out_pdf, timeout=args.timeout)
    print(f"PDF  => {out_pdf}")
    print("完成！")


if __name__ == '__main__':
    main()
