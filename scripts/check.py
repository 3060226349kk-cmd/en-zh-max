#!/usr/bin/env python3
"""译文机检：标点残留 + 翻译腔信号（es-zh-max / en-zh-max / jp-zh-max 共用，三份保持一致）。

用法：
    python3 check.py zh 文件.md [--fix] [--pairs 对照表.md ...]   # 检查中文译文
    python3 check.py es 文件.md [--fix] [--pairs 对照表.md ...]   # 检查西语译文（中译西）

只检查译文行：跳过 > 开头的原文行、代码块、HTML 注释、空行和 --- 分隔线。
--fix    只做安全的标点机械替换；翻译腔信号只报告、不改。
--pairs  读取 Markdown 表格里首列表头为「源词」的行（源词 | 误译 | 正译），
         原文段含源词、紧随的译文段含误译时报出（同形词、假朋友）。
--keep-quotes  中文译文保留直角引号「」『』（轻小说、漫画台词按原作风格时用）。
退出码：0 = 无标点残留；1 = 仍有标点残留（翻译腔信号不影响退出码）。
"""

import re
import sys
from pathlib import Path

CJK_PUNCT = set('“”‘’·—…《》〈〉「」『』【】、。，！？；：（）～')
PROTECT = re.compile(r'\[[^\]]*\]\([^)]*\)|`[^`]*`|https?://\S+')
MAX_EXAMPLES = 5


def is_han(c):
    o = ord(c) if c else 0
    return 0x3400 <= o <= 0x9FFF or 0xF900 <= o <= 0xFAFF


def is_cjk(c):
    if not c:
        return False
    o = ord(c)
    return (is_han(c) or 0x3000 <= o <= 0x303F or 0x3040 <= o <= 0x30FF
            or 0xFF00 <= o <= 0xFFEF or c in CJK_PUNCT)


def read_text(path):
    raw = Path(path).read_bytes()
    for enc in ('utf-8-sig', 'gb18030'):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode('latin-1')


def line_kinds(lines):
    """逐行标注：'src' 原文行，'tr' 译文行，None 其他。"""
    kinds, in_code, in_comment = [], False, False
    for ln in lines:
        s = ln.strip()
        if s.startswith('```'):
            in_code = not in_code
            kinds.append(None)
        elif in_code:
            kinds.append(None)
        elif in_comment:
            in_comment = '-->' not in s
            kinds.append(None)
        elif s.startswith('<!--'):
            in_comment = '-->' not in s
            kinds.append(None)
        elif ln.lstrip().startswith('>'):
            kinds.append('src')
        elif not s or s == '---':
            kinds.append(None)
        else:
            kinds.append('tr')
    return kinds


def protect(line):
    store = []

    def keep(m):
        store.append(m.group(0))
        return '\x00%d\x00' % (len(store) - 1)

    return PROTECT.sub(keep, line), store


def restore(line, store):
    return re.sub('\x00(\\d+)\x00', lambda m: store[int(m.group(1))], line)


# ---------- 中文译文 ----------
ZH_MAP = {',': '，', ';': '；', ':': '：', '?': '？', '!': '！', '(': '（', ')': '）'}
ZH_QUOTES = {'「': '“', '」': '”', '『': '‘', '』': '’', '«': '“', '»': '”', '‹': '‘', '›': '’'}
OPTS = {'keep_quotes': False}


def zh_fix(line):
    line, store = protect(line)
    keep = '「」『』' if OPTS['keep_quotes'] else ''
    line = ''.join(c if c in keep else ZH_QUOTES.get(c, c) for c in line)
    line = line.replace('・', '·').replace('〜', '～')
    line = re.sub(r'(?<=[㐀-鿿])\.{3}|\.{3}(?=[㐀-鿿])', '……', line)
    out, open_quote = [], True
    for c in line:
        if c == '"':
            out.append('“' if open_quote else '”')
            open_quote = not open_quote
        else:
            out.append(c)
    ch, n = out, len(out)
    for i, c in enumerate(ch):
        prev = ch[i - 1] if i else ''
        nxt = ch[i + 1] if i + 1 < n else ''
        if c in ZH_MAP and (is_cjk(prev) or is_cjk(nxt)):
            ch[i] = ZH_MAP[c]
        elif c in '¿¡' and is_cjk(nxt):
            ch[i] = ''
        elif c == '.' and is_han(prev) and (not nxt or nxt in ' \t' or is_cjk(nxt)):
            ch[i] = '。'
    line = re.sub(r'([，。！？；：、）】」』”’])[ \t]+(?=[㐀-鿿“‘（《])', r'\1', ''.join(ch))
    return restore(line, store)


def zh_residual(line):
    t, _ = protect(line)
    hits = []
    for m in re.finditer(r'[,;:?!()¿¡]', t):
        i = m.start()
        prev = t[i - 1] if i else ''
        nxt = t[i + 1] if i + 1 < len(t) else ''
        if is_cjk(prev) or is_cjk(nxt):
            hits.append(m.group(0))
    hits += [c for c in t if c in ('«»‹›・〜' if OPTS['keep_quotes'] else '«»‹›「」『』・〜')]
    if re.search(r'[㐀-鿿]', t):
        hits += re.findall(r'"', t)
        if re.match(r'\s*—(?!—)', t):
            hits.append('行首对话破折号—')
    return hits


ZH_SIGNALS = [
    ('「的」链（三个「的」挤在一处）', re.compile(r'的[^，。！？；：、]{0,8}的[^，。！？；：、]{0,8}的')),
    ('「被」字句', re.compile(r'被')),
    ('万能动词（进行／作出／给予／加以／开展）', re.compile(r'进行|作出|做出|给予|加以|开展')),
    ('介词腔（通过／对于／关于／作为／随着）', re.compile(r'通过|对于|关于|作为|随着')),
    ('「当……时」', re.compile(r'当[^，。！？；]{1,15}时')),
    ('「在……方面」', re.compile(r'在[^，。！？；]{1,12}方面')),
    ('「一个／一种／一位……」', re.compile(r'一(?:个|种|位|名|项)')),
    ('「将会／可能会」', re.compile(r'将会|可能会')),
]


def zh_extra(line, ctx):
    found = []
    for sent in re.split(r'[。！？；]', line):
        if len(re.findall(r'(?<![其吉])[他她它](?:们)?', sent)) >= 3:
            found.append(('代词密集（一句里三个以上他／她／它）', sent.strip()[:40]))
        for clause in re.split(r'[，。！？；：]', sent):
            if len(re.findall(r'[㐀-鿿]', re.sub(r'、', '', clause))) > 40:
                found.append(('超长分句（逗号之间超过 40 个汉字）', clause.strip()[:40]))
            parts = clause.split('、')
            if ctx.get('jp_source') and any(
                    len(re.findall(r'[㐀-鿿]', p)) > 15 and not p.rstrip().endswith(('的', '地', '得'))
                    for p in parts[:-1]):
                found.append(('顿号隔开的长片段（日语读点「、」残留？应为逗号）', clause.strip()[:40]))
    return found


# ---------- 西语译文 ----------
ES_MAP = {'，': ',', '。': '.', '；': ';', '：': ':', '？': '?', '！': '!', '（': '(', '）': ')', '、': ','}


def es_fix(line):
    line, store = protect(line)
    line = re.sub(r'《([^》]*)》', r'*\1*', line)
    line = line.replace('「', '«').replace('」', '»').replace('『', '“').replace('』', '”')
    line = line.replace('……', '…').replace('——', '—')
    out = []
    for i, c in enumerate(line):
        if c in ES_MAP:
            out.append(ES_MAP[c])
            nxt = line[i + 1] if i + 1 < len(line) else ''
            if c != '（' and nxt and (nxt.isalnum() or nxt in '¿¡«“('):
                out.append(' ')
        else:
            out.append(c)
    line = ''.join(out)
    line = re.sub(r'[ \t]+([,.;:?!)»”])', r'\1', line)
    line = re.sub(r'([¿¡(«“])[ \t]+', r'\1', line)
    line = re.sub(r'([,;:])(?=[A-Za-zÁÉÍÓÚÜÑáéíóúüñ¿¡«])', r'\1 ', line)
    line = re.sub(r'([.?!])(?=[A-ZÁÉÍÓÚÜÑ¿¡«])', r'\1 ', line)
    line = re.sub(r'(?<=\S)[ \t]{2,}(?=\S)', ' ', line)
    return restore(line, store)


def es_residual(line):
    t, _ = protect(line)
    hits = [c for c in t if c in ES_MAP or c in '《》「」『』']
    hits += re.findall(r'……|——', t)
    hits += re.findall(r'[ \t][,.;:?!](?!\d)', t)
    return hits


ES_SIGNALS = [
    ('relativamente（「较」字硬译？）', re.compile(r'\brelativamente\b', re.I)),
    ('en el aspecto de（「……方面」硬译？）', re.compile(r'\ben (?:el|los) aspectos? de\b', re.I)),
    ('a la gente（「令人、给人」硬译？）', re.compile(r'\ba la gente\b', re.I)),
    ('realizar / efectuar / llevar a cabo（万能动词）', re.compile(r'\b(?:realiz\w+|efectu\w+|llev\w+ a cabo)\b', re.I)),
    ('hacer que（「使」硬译？）', re.compile(r'\bh(?:ace|izo|ará|acer|ecía|ago)\w* que\b', re.I)),
    ('身体部位或随身物品前用物主形容词（该用与格或自复代词？）', re.compile(
        r'\b(?:lav|cort|pus|pon|quit|sec|limpi|rasc|pein|toc|enjug)\w*\s+(?:su|sus|mi|mis|tu|tus)\s+'
        r'(?:manos?|cara|pelo|cabello|cabeza|pies?|ojos|dientes|uñas|gafas|lentes|sombrero|abrigo|'
        r'zapatos|brazos?|piernas?|espalda|boca|labios|lágrimas|sudor)\b', re.I)),
]


def es_extra(line, ctx):
    found = []
    t, _ = protect(line)
    for sent in re.split(r'(?<=[.?!])\s+', t):
        if sent.count('¿') != sent.count('?') or sent.count('¡') != sent.count('!'):
            found.append(('¿? ¡! 不配对', sent.strip()[:60]))
        if len(re.findall(r'[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+', sent)) > 60:
            found.append(('超长句（超过 60 个词）', sent.strip()[:60]))
    if re.search(r'[㐀-鿿]', t):
        found.append(('残留汉字（漏译？）', t.strip()[:60]))
    words = [w.lower() for w in re.findall(r'[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]{8,}', t)]
    for w in sorted(set(words)):
        if words.count(w) >= 3:
            found.append(('长词重复（同一句段三次以上）', w))
    return found


# ---------- 同形词、假朋友 ----------
SRC_HEADERS = {'源词', '日文', '西语', '原文'}
BAD_HEADERS = {'误译', '错误直搬', '中文字面理解', '易误译'}
GOOD_HEADERS = {'正译', '正确翻译', '应译', '正确译法'}


def _terms(cell):
    cell = re.sub(r'（[^）]*）|\([^)]*\)', '', cell)
    return [t.strip() for t in re.split(r'[／/、]', cell) if t.strip() and t.strip() not in ('无', '（无）')]


def load_pairs(paths):
    """读表头含「源词／日文…」「误译／错误直搬…」「正译／正确翻译…」三列的 Markdown 表格。"""
    pairs = []
    for p in paths:
        cols = None
        for ln in read_text(p).splitlines():
            if not ln.lstrip().startswith('|'):
                cols = None
                continue
            cells = [c.strip() for c in ln.strip().strip('|').split('|')]
            if cols is None:
                idx = [next((i for i, c in enumerate(cells) if c in hs), None)
                       for hs in (SRC_HEADERS, BAD_HEADERS, GOOD_HEADERS)]
                cols = idx if None not in idx else None
            elif not set(cells[0]) <= set('-: ') and len(cells) > max(cols):
                srcs, bads, good = (cells[i] for i in cols)
                good_terms = _terms(good)
                bad_terms = [b for b in _terms(bads) if b not in good_terms]
                if _terms(srcs) and bad_terms:
                    pairs.append((_terms(srcs), bad_terms, good))
    return pairs


def check_pairs(lines, kinds, pairs):
    hits, src_text, last = [], '', None
    for i, ln in enumerate(lines):
        if kinds[i] == 'src':
            if last == 'tr':
                src_text = ''
            src_text += ' ' + ln.lstrip()[1:]
            last = 'src'
        elif kinds[i] == 'tr':
            last = 'tr'
            if not src_text:
                continue
            low = src_text.lower()
            for srcs, bads, good in pairs:
                s = next((x for x in srcs if x.lower() in low), None)
                b = next((x for x in bads if x in ln), None)
                if s and b:
                    hits.append((i + 1, '%s → 译成了「%s」（应为：%s）' % (s, b, good)))
    return hits


def report(title, examples, per_k=None):
    density = '（每千字 %.1f）' % per_k if per_k is not None else ''
    print('  · %s：%d 处%s' % (title, len(examples), density))
    for ln, snippet in examples[:MAX_EXAMPLES]:
        print('      第 %d 行：%s' % (ln, snippet))


def fix_text(mode, text):
    """对整份文本做标点修正（供 normalize-punctuation*.py 兼容入口调用）。"""
    lines = text.split('\n')
    kinds = line_kinds(lines)
    fixer = zh_fix if mode == 'zh' else es_fix
    return '\n'.join(fixer(ln) if kinds[i] == 'tr' else ln for i, ln in enumerate(lines))


def count_residual(mode, text):
    lines = text.split('\n')
    kinds = line_kinds(lines)
    residual = zh_residual if mode == 'zh' else es_residual
    return sum(len(residual(ln)) for i, ln in enumerate(lines) if kinds[i] == 'tr')


def main(argv):
    args = argv[1:]
    pair_files = []
    while '--pairs' in args:
        k = args.index('--pairs')
        pair_files.append(args[k + 1])
        del args[k:k + 2]
    do_fix = '--fix' in args
    OPTS['keep_quotes'] = '--keep-quotes' in args
    args = [a for a in args if a not in ('--fix', '--keep-quotes')]
    if len(args) != 2 or args[0] not in ('zh', 'es'):
        print(__doc__)
        return 2
    mode, path = args
    text = read_text(path)
    if do_fix:
        text = fix_text(mode, text)
        Path(path).write_text(text, encoding='utf-8')
    lines = text.split('\n')
    kinds = line_kinds(lines)
    residual = zh_residual if mode == 'zh' else es_residual
    signals, extra = (ZH_SIGNALS, zh_extra) if mode == 'zh' else (ES_SIGNALS, es_extra)

    ctx = {'jp_source': any(kinds[i] == 'src' and re.search(r'[぀-ヿ]', ln)
                            for i, ln in enumerate(lines))}
    units = sum(len(re.findall(r'[㐀-鿿]' if mode == 'zh' else r'[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+', ln))
                for i, ln in enumerate(lines) if kinds[i] == 'tr') or 1
    left, sig_hits, extra_hits = 0, {}, {}
    for i, ln in enumerate(lines):
        if kinds[i] != 'tr':
            continue
        r = residual(ln)
        if r:
            left += len(r)
            extra_hits.setdefault('标点残留', []).append((i + 1, ' '.join(r)))
        for title, rx in signals:
            for m in rx.finditer(ln):
                sig_hits.setdefault(title, []).append((i + 1, m.group(0)))
        for title, snippet in extra(ln, ctx):
            extra_hits.setdefault(title, []).append((i + 1, snippet))
    if pair_files:
        ph = check_pairs(lines, kinds, load_pairs(pair_files))
        if ph:
            sig_hits['同形词、假朋友（对照原文确认词义）'] = ph

    lang = '中文' if mode == 'zh' else '西语'
    print('【%s译文机检】%s%s' % (lang, path, '（已执行 --fix）' if do_fix else ''))
    print('标点残留：%d' % left)
    for title, ex in extra_hits.items():
        report(title, ex)
    if sig_hits:
        print('翻译腔信号（只是提示，逐处判断是否要改）：')
        for title, ex in sig_hits.items():
            report(title, ex, len(ex) * 1000 / units)
    else:
        print('翻译腔信号：无')
    return 0 if left == 0 else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
