#!/usr/bin/env python3
"""交付前清理：删版本标记和 text-profile 注释、清 AI 流程残留与旧流程诊断记录、补译者署名。

en-zh-max / jp-zh-max 共用，两份保持一致。署名里的项目地址按脚本所在技能目录自动填写。
用法: python3 strip-version-markers.py <对照文件.md>
"""
import re
import sys
from pathlib import Path

TRANSLATOR_LINE = '**译者：Lilipuut + Claude**'
PROJECT_URLS = {
    'en-zh-max': 'https://github.com/3060226349kk-cmd/en-zh-max',
    'jp-zh-max': 'https://github.com/3060226349kk-cmd/ja-zh-max',
}

# ── 流程残留（整行删除，原文 blockquote 行不动） ──
AGENT_RESIDUE_PATTERNS = [
    # 文件路径泄漏：Windows 与 macOS/Linux
    r'C:\\Users\\.*?(?:\\bilingual\\|\\chunk|\\Downloads)',
    r'C:\\\\.*?\\\\bilingual\\\\',
    r'(?:/Users/[^/\s]+|/home/[^/\s]+|~)/\S*(?:Downloads|scratchpad|bilingual|chunk|\.claude|\.agents)',
    r'/private/(?:tmp|var)/\S+',
    r'/var/folders/\S+',
    # chunk 编号与来源标记
    r'以上为\s*\S*chunk[_\d]*\.txt\s*的完整',
    r'以上が\s*\S*chunk[_\d]*\.txt\s*の完全',
    r'源文件路径[：:].*',
    r'源ファイルパス[：:].*',
    r'源文件[：:]\s*<code>.*</code>',
    r'源ファイル[：:]\s*<code>.*</code>',
    r'译文已整合至[：:].*',
    r'翻訳済み統合先[：:].*',
    # 完成声明
    r'翻译完成[。.]\s*以下是最终输出摘要',
    r'翻訳完了[。.]\s*以下は最終出力サマリー',
    r'翻译已完成[，,]\s*文件已更新',
    r'翻訳が完了しました[，,]\s*ファイルが更新されました',
    r'翻译已就绪',
    r'翻译已处理',
    # Agent 自我描述
    r'现在我已掌握完整文本[。.]\s*开始翻译[。.]\s*这是一篇',
    r'現在、全文を把握しました[。.]\s*翻訳を開始します[。.]\s*これは',
    r'译文完整[。.]\s*所有英文段以blockquote标注',
    r'翻訳完了[。.]\s*全ての英文をblockquoteで',
    r'严格遵循术语表[。.]',
    r'用語テーブルに厳密に従う[。.]',
    # 结构化元数据标题
    r'^(?:翻訳カバー内容|翻译覆盖内容)\s*$',
    r'^(?:フォーマット|格式)[：:]\s*(?:段落レベル|段落级)',
    r'^(?:用語準拠|术语遵循)[：:]',
]

AGENT_RESIDUE_BLOCKS = [
    r'(?:^|\n)#+\s*(?:翻訳完了サマリー|翻译完成总结)\s*\n.*?(?=\n#+\s|\Z)',
]

# ── 旧流程（v3）诊断记录，英、日两套 ──
ULTRA_DIAG_INLINE = [
    r'<!--\s*(?:前景化[：:]|反释义[：:]|西化(?:六维)?评估[：:]|准确性六维(?:校验)?等级[：:]'
    r'|修辞类型[：:]|三阶段[：:]|多译案[：:]|回译诊断[：:]|ultra[：:]).*?-->',
    r'^\s*(?:前景化标注|反释义判断|西化(?:六维)?评分|六维等级'
    r'|修辞类型标注|三阶段评级|多译案候选|回译诊断差异|修辞处理决策)[：:]\s*.*$',
]

ULTRA_DIAG_BLOCKS = [
    r'(?:^|\n)#+\s*(?:前景化标注列表|文学反释义判断记录|西化六维评估的逐项评分|准确性六维校验的严重等级标记'
    r'|多译案候选列表|回译诊断差异记录|修辞类型标注汇总|三阶段评级记录|修辞意识发展评定)\s*\n.*?(?=\n\n|\n#|\Z)',
]


def _is_blockquote(line):
    return line.lstrip().startswith('>')


def _project_line():
    skill = Path(__file__).resolve().parent.parent.name
    url = PROJECT_URLS.get(skill)
    return f'> 源于 [{skill}]({url}) 翻译技能产出，欢迎使用和改进。' if url else None


def strip_and_attrib(filepath):
    text = Path(filepath).read_text(encoding='utf-8')
    original = text

    # 1. text-profile 注释块
    text = re.sub(r'<!-- text-profile.*?-->\s*', '', text, flags=re.DOTALL)

    # 2. 版本标记：[v1] [v2·S] [v3·Q✓] [v2·W·语域] 等，原文行也一并清掉
    version_re = re.compile(r'[ \t]*\[v[123](?:·[^\]]+)?\]')
    text, stripped = version_re.subn('', text)

    # 3. 译者署名（插在第一个 H1 上方）与项目地址
    project = _project_line()
    if not re.search(r'^\*\*译者：', text, re.MULTILINE):
        block = TRANSLATOR_LINE + ('\n' + project if project else '') + '\n\n---\n\n'
        text = re.sub(r'^(#\s+.+)$', lambda m: block + m.group(1), text, count=1, flags=re.MULTILINE)
        print('[完成] 译者署名已添加')
    elif project and project not in text:
        text = re.sub(r'^(\*\*译者：.*\*\*)$', lambda m: m.group(1) + '\n' + project, text, count=1,
                      flags=re.MULTILINE)
        print('[完成] 项目地址已补上')
    else:
        print('[跳过] 译者署名已存在')

    # 4. 流程残留
    for pat in AGENT_RESIDUE_BLOCKS:
        text = re.sub(pat, '', text, flags=re.DOTALL)
    kept, residue_removed = [], 0
    for ln in text.split('\n'):
        if not _is_blockquote(ln) and any(re.search(p, ln) for p in AGENT_RESIDUE_PATTERNS):
            residue_removed += 1
        else:
            kept.append(ln)
    text = re.sub(r'\n{3,}', '\n\n', '\n'.join(kept))

    # 5. 旧流程诊断记录
    diag_removed = 0
    for pat in ULTRA_DIAG_BLOCKS:
        text, n = re.subn(pat, '', text, flags=re.DOTALL)
        diag_removed += n
    for pat in ULTRA_DIAG_INLINE:
        text, n = re.subn(pat, '', text, flags=re.DOTALL | re.MULTILINE)
        diag_removed += n
    text = re.sub(r'\n{3,}', '\n\n', text)

    Path(filepath).write_text(text, encoding='utf-8')
    print(f'[完成] 版本标记清除: {stripped} 处')
    print(f'[完成] AI 流程残留清除: {residue_removed} 行')
    print(f'[完成] 旧流程诊断记录清除: {diag_removed} 块')
    print(f'[状态] 内容变更: {"是" if text != original else "否"}')
    return stripped


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python3 strip-version-markers.py <对照文件.md>')
        sys.exit(1)
    strip_and_attrib(sys.argv[1])
