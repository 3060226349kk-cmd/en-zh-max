#!/usr/bin/env python3
"""长任务交接：量本会话上下文、写 HANDOFF.md（es-zh-max / en-zh-max / jp-zh-max 共用，三份保持一致）。

用法：
    python3 handoff.py meter [--done N] [--limit TOKENS]
    python3 handoff.py write 项目目录 --next "下一步" [--notes 文件|-] [--relay] [--no-copy]

meter  读本会话当前的上下文 token 数，达到阈值（默认 150000）报「→ 交接」，否则报「→ 继续」。
       只有 Claude Code 读得到用量；读不到时按 --done（本会话已做完的单元数）判断，满 2 个就交接。
write  覆盖写 项目目录/HANDOFF.md：续接顺序、下一步、translation-plan.md 的进度、--notes 给的事项
       （- 表示从标准输入读）。打印续接命令并复制到剪贴板；--no-copy 不复制，--relay 让续接命令带上「自动接力」。
退出码：0 = 正常；2 = 用法错误或读不到用量又没给 --done。
"""

import datetime
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

LIMIT = 150_000
UNITS_PER_SESSION = 2
TAIL = 1 << 20
USAGE_KEYS = ('input_tokens', 'cache_read_input_tokens', 'cache_creation_input_tokens', 'output_tokens')
TEMP_PATH = re.compile(r'/private/(?:tmp|var)/\S*|/var/folders/\S*|/tmp/\S*|\S*scratchpad\S*')
SKILL_DIR = Path(__file__).resolve().parent.parent


def take(args, name, has_value=True):
    if name not in args:
        return None if has_value else False
    k = args.index(name)
    if not has_value:
        del args[k]
        return True
    if k + 1 >= len(args):
        raise SystemExit('%s 后面缺少值' % name)
    value = args[k + 1]
    del args[k:k + 2]
    return value


def wan(n):
    return ('%.1f' % (n / 10000)).rstrip('0').rstrip('.') + ' 万'


def context_of(raw):
    if b'"usage"' not in raw:
        return 0
    try:
        entry = json.loads(raw)
    except ValueError:
        return 0
    if entry.get('type') != 'assistant' or entry.get('isSidechain'):
        return 0
    usage = (entry.get('message') or {}).get('usage') or {}
    return sum(usage.get(k) or 0 for k in USAGE_KEYS)


def session_context():
    """返回 (上下文 token 数, 读不到的原因)。取本会话记录里最后一条有用量的回复。"""
    sid = os.environ.get('CLAUDE_CODE_SESSION_ID')
    if not sid:
        return None, '不是 Claude Code 会话'
    root = Path(os.environ.get('CLAUDE_CONFIG_DIR') or Path.home() / '.claude') / 'projects'
    logs = sorted(root.glob('*/%s.jsonl' % sid), key=lambda p: p.stat().st_mtime)
    if not logs:
        return None, '找不到本会话记录'
    with open(logs[-1], 'rb') as f:
        size = f.seek(0, 2)
        span = TAIL
        while True:
            start = max(0, size - span)
            f.seek(start)
            lines = f.read().split(b'\n')
            if start:
                lines = lines[1:]
            for raw in reversed(lines):
                n = context_of(raw)
                if n:
                    return n, None
            if not start:
                return None, '本会话记录里还没有用量'
            span *= 4


def meter(args):
    done = take(args, '--done')
    limit = int(take(args, '--limit') or LIMIT)
    if args:
        print(__doc__)
        return 2
    n, why = session_context()
    if n:
        print('上下文 %s token，阈值 %s → %s' % (wan(n), wan(limit), '交接' if n >= limit else '继续'))
        return 0
    if done is None:
        print('读不到上下文用量（%s）。加 --done <本会话已做完的单元数> 再跑。' % why)
        return 2
    done = int(done)
    print('读不到上下文用量（%s）；本会话已做完 %d 个单元，每 %d 个交接 → %s'
          % (why, done, UNITS_PER_SESSION, '交接' if done >= UNITS_PER_SESSION else '继续'))
    return 0


def skill_name():
    md = SKILL_DIR / 'SKILL.md'
    if md.is_file():
        m = re.search(r'^name:\s*(\S+)', md.read_text(encoding='utf-8'), re.M)
        if m:
            return m.group(1)
    return SKILL_DIR.name


def progress(plan):
    done, todo, last = 0, 0, ''
    for ln in plan.read_text(encoding='utf-8').splitlines():
        m = re.match(r'\s*[-*+]\s+\[([ xX])\]\s*(.*)', ln)
        if not m:
            continue
        if m.group(1) == ' ':
            todo += 1
        else:
            done += 1
            last = m.group(2).strip()
    return done, todo, last


def to_clipboard(text):
    env = dict(os.environ, LANG='en_US.UTF-8', LC_ALL='en_US.UTF-8')
    for cmd in (['pbcopy'], ['wl-copy'], ['xclip', '-selection', 'clipboard']):
        if shutil.which(cmd[0]):
            try:
                subprocess.run(cmd, input=text.encode('utf-8'), env=env, check=True, timeout=5)
                return True
            except (OSError, subprocess.SubprocessError):
                return False
    return False


def write(args):
    nxt = take(args, '--next')
    notes_from = take(args, '--notes')
    relay = take(args, '--relay', False)
    copy = not take(args, '--no-copy', False)
    if len(args) != 1 or not nxt:
        print(__doc__)
        return 2
    proj = Path(args[0]).expanduser().resolve()
    if not proj.is_dir():
        print('项目目录不存在：%s' % proj)
        return 2
    if notes_from == '-':
        notes = sys.stdin.read().strip()
    elif notes_from:
        notes = Path(notes_from).read_text(encoding='utf-8').strip()
    else:
        notes = ''

    skill = skill_name()
    guide = 'references/handoff.md' if (SKILL_DIR / 'references' / 'handoff.md').is_file() else 'handoff.md'
    sid = os.environ.get('CLAUDE_CODE_SESSION_ID', '')
    stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    plan = proj / 'translation-plan.md'
    if plan.is_file():
        done, todo, last = progress(plan)
        state = 'translation-plan.md 已勾选 %d 项' % done
        state += '，未勾选 %d 项' % todo if todo else ''
        state += '；最后勾选的是「%s」。' % last if last else '。'
    else:
        state = '没有 translation-plan.md，进度只看本文件。'
    tools = sorted(p.name for p in (proj / 'tools').glob('*') if p.is_file()) if (proj / 'tools').is_dir() else []

    out = [
        '# 交接：%s' % proj.name,
        '',
        '写于 %s，技能 %s%s。新会话按「续接」读完，从「下一步」接着做。'
        % (stamp, skill, '，上一会话 ' + sid[:8] if sid else ''),
        '',
        '## 续接',
        '1. 本文件。',
        '2. `translation-plan.md`：进度以勾选为准，比本文件新时从勾选处接着做；开头记着定性结论、用户的长期指令和工具用法。',
        '3. `TERMS_GLOSSARY.md`：译名、语域标记、体例。',
        '4. %s 的 SKILL.md 里中档要读的参考文件，以及交接细则 `%s`。' % (skill, guide),
        '',
        '已定稿的章节、合订本、整本原文都不要回读；要查旧译法，就 grep 术语表或上一章。',
        '',
        '## 下一步',
        nxt.strip(),
        '',
        '## 进度',
        state,
    ]
    if tools:
        out.append('项目脚本：%s（在 tools/ 下）。' % '、'.join(tools))
    out += ['', '## 本会话留下的事项', notes or '无。', '']
    text = '\n'.join(out)
    target = proj / 'HANDOFF.md'
    target.write_text(text, encoding='utf-8')

    tail = '，自动接力' if relay else ''
    if os.environ.get('CLAUDECODE') == '1':
        prompt = '/%s 续译 %s%s' % (skill, proj, tail)
    else:
        prompt = '用 %s 技能续译 %s%s（先读其中的 HANDOFF.md）' % (skill, proj, tail)
    print('已写 %s（%d 字）' % (target, len(text)))
    temp = sorted(set(TEMP_PATH.findall(text + (plan.read_text(encoding='utf-8') if plan.is_file() else ''))))
    if temp:
        print('注意：交接或进度文件里提到了临时目录，新会话可能找不到：%s。项目脚本请移到 %s/tools/。'
              % ('、'.join(temp[:3]), proj))
    copied = copy and to_clipboard(prompt)
    print('续接命令%s：' % ('（已复制到剪贴板）' if copied else ''))
    print(prompt)
    return 0


def main(argv):
    args = argv[1:]
    if args and args[0] == 'meter':
        return meter(args[1:])
    if args and args[0] == 'write':
        return write(args[1:])
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv))
