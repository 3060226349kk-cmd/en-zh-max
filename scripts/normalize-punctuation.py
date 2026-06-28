#!/usr/bin/env python3
"""
标点归一化脚本 — 中文译文标点规范化 + 自检残留半角标点。

用法：
    python3 normalize-punctuation.py "<名称> 翻译(中英对照).md"

规则：逗号类与圆括号只在紧邻中文时才转全角；
      blockquote 行（> 开头）和 Markdown 链接内标点保持半角不动。
退出码：0 = 无残留，1 = 有残留（残留数已打印）。
"""

import re
import sys

CJK_EXTRA = set('""\'\'·—…《》〈〉「」『』【】、。，！？；：（）')


def is_cjk(c):
    if not c:
        return False
    o = ord(c)
    return (0x3400 <= o <= 0x9FFF) or (0x3000 <= o <= 0x303F) or (0xFF00 <= o <= 0xFFEF) or (c in CJK_EXTRA)


SMAP = {',': '，', ';': '；', ':': '：', '?': '？', '!': '！', '(': '（', ')': '）'}
OPEN2 = '"\u201c\u300c'
CLOSE2 = '"\u201d\u300d'
OPEN1 = "'\u2018\u300e"
CLOSE1 = "'\u2019\u300f"
LINK = re.compile(r'\[[^\]]*\]\([^)]*\)')


def fix(line):
    store = []
    line = LINK.sub(lambda m: store.append(m.group(0)) or '\x00%d\x00' % (len(store) - 1), line)
    out = []
    sop = True  # 歧义直双引号靠交替定开闭
    for c in line:
        if c == '"':
            out.append('\u201c' if sop else '\u201d')
            sop = not sop
        elif c in OPEN2:
            out.append('\u201c')
        elif c in CLOSE2:
            out.append('\u201d')
        elif c in OPEN1:
            out.append('\u2018')
        elif c in CLOSE1:
            out.append('\u2019')
        else:
            out.append(c)
    ch = out
    n = len(ch)
    for i, c in enumerate(ch):
        if c in SMAP and (is_cjk(ch[i - 1] if i else '') or is_cjk(ch[i + 1] if i + 1 < n else '')):
            ch[i] = SMAP[c]
    line = ''.join(ch)
    return re.sub('\x00(\\d+)\\x00', lambda m: store[int(m.group(1))], line)


def skip(ln):
    s = ln.strip()
    return s == '' or ln.lstrip().startswith('>') or s == '---'


def main():
    src = sys.argv[1]
    lines = open(src, encoding='utf-8').read().split('\n')
    res = [ln if skip(ln) else fix(ln) for ln in lines]
    open(src, 'w', encoding='utf-8').write('\n'.join(res))

    # 自检残留
    def residual(ln):
        t = LINK.sub('', ln)
        return sum(
            1 for m in re.finditer(r'[,;:?!()]', t)
            if is_cjk(t[m.start() - 1] if m.start() else '') or is_cjk(
                t[m.start() + 1] if m.start() + 1 < len(t) else ''
            )
        )

    bad = sum(residual(ln) for ln in res if not skip(ln))
    print('残留:', bad)
    sys.exit(0 if bad == 0 else 1)


if __name__ == '__main__':
    main()
