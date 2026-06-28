#!/usr/bin/env python3
"""剥夺版本标记 + 删除 AI 处理标记 + 增加译者署名 + 剥离子代理流程残留 + 清理 ultra 诊断记录。

en-zh / jp-zh 翻译管线 — 阶段 8 强制前置门禁。
用法: python3 strip-version-markers.py <对照文件.md>
"""
import re
import sys


# ── 子代理流程残留模式 ──
AGENT_RESIDUE_PATTERNS = [
    # 文件路径泄漏
    r'C:\\Users\\.*?(?:\\bilingual\\|\\chunk|\\Downloads)',
    r'C:\\\\.*?\\\\bilingual\\\\',
    # chunk 编号与来源标记
    r'以上为\s*\S*chunk[_\d]*\.txt\s*的完整',
    r'源文件路径[：:].*',
    r'源文件[：:]\s*<code>.*</code>',
    r'译文已整合至[：:].*',
    # 子代理完成声明
    r'翻译完成[。.]\s*以下是最终输出摘要',
    r'翻译已完成[，,]\s*文件已更新',
    r'翻译已就绪',
    r'翻译已处理',
    # Agent 自我描述
    r'现在我已掌握完整文本[。.]\s*开始翻译[。.]\s*这是一篇',
    r'译文完整[。.]\s*所有英文段以blockquote标注',
    r'严格遵循术语表[。.]',
    # 结构化元数据标题
    r'^翻译覆盖内容\s*$',
    r'^格式[：:]\s*段落级英中对照',
    r'^术语遵循[：:]',
]

AGENT_RESIDUE_BLOCKS = [
    # 翻译完成总结 section（HTML/MD 混合格式）
    r'(?:^|\n)#+\s*翻译完成总结\s*\n.*?(?=\n#+\s|\Z)',
]

# ── ultra 诊断记录模式（en-zh-max stage 8A §5） ──
ULTRA_DIAG_INLINE = [
    # HTML 注释型诊断
    r'<!--\s*(?:前景化[：:]|反释义[：:]|西化(?:六维)?评估[：:]|准确性六维(?:校验)?等级[：:]|ultra[：:]).*?-->',
    # 内联诊断标记行（整行删除）
    r'^\s*(?:前景化标注|反释义判断|西化(?:六维)?评分|六维等级)[：:]\s*.*$',
]

ULTRA_DIAG_BLOCKS = [
    # markdown 诊断段落标题 + 内容（直到空行或下一标题）
    r'(?:^|\n)#+\s*(?:前景化标注列表|文学反释义判断记录|西化六维评估的逐项评分|准确性六维校验的严重等级标记)\s*\n.*?(?=\n\n|\n#|\Z)',
]

# 检查是否为 blockquote 行（不动）
def _is_blockquote(line):
    return line.lstrip().startswith('>')


def strip_and_attrib(filepath, translator_line="**译者：Lilipuut + Claude**"):
    with open(filepath, encoding='utf-8') as f:
        text = f.read()

    original = text

    # ── 1. 删除 <!-- text-profile ... --> 注释块（可能跨行） ──
    text = re.sub(r'<!-- text-profile.*?-->\s*', '', text, flags=re.DOTALL)

    # ── 2. 剥夺版本标记 ──
    # 匹配: [v1] [v2·S] [v2·W] [v2·A] [v2·∅] [v3] [v3·Q✓]
    # 及 max 扩展版记: [v2·W·语域] [v2·S·多译案] 等
    version_re = re.compile(r'\s*\[v[123](?:·[^\]]+)?\]')

    lines = text.split('\n')
    stripped = 0
    cleaned = []
    for ln in lines:
        if _is_blockquote(ln):
            cleaned.append(ln)
        else:
            new_ln, n = version_re.subn('', ln)
            cleaned.append(new_ln)
            stripped += n
    text = '\n'.join(cleaned)

    # ── 3. 增加译者署名（插在第一个 H1 上方） ──
    has_attrib = bool(re.search(r'^\*\*译者：', text, re.MULTILINE))
    if has_attrib:
        print('[跳过] 译者署名已存在')
    else:
        attribution = f'{translator_line}\n\n---\n\n'
        text = re.sub(
            r'^(#\s+.+)$',
            lambda m: f'{attribution}{m.group(1)}',
            text,
            count=1,
            flags=re.MULTILINE
        )
        print('[完成] 译者署名已添加')

    # ── 4. 剥离子代理流程残留 ──
    # 4a. 移除整块元数据 section
    for block_pat in AGENT_RESIDUE_BLOCKS:
        text = re.sub(block_pat, '', text, flags=re.DOTALL)

    # 4b. 逐行删除残留模式（跳过 blockquote）
    lines = text.split('\n')
    residue_removed = 0
    cleaned2 = []
    for ln in lines:
        is_residue = False
        if not _is_blockquote(ln):
            for pat in AGENT_RESIDUE_PATTERNS:
                if re.search(pat, ln):
                    is_residue = True
                    break
        if is_residue:
            residue_removed += 1
        else:
            cleaned2.append(ln)
    text = '\n'.join(cleaned2)

    # 4c. 清除因删除残留行产生的连续空行（>=3 → 2）
    text = re.sub(r'\n{3,}', '\n\n', text)

    # ── 5. 清理 ultra 诊断记录（en-zh-max stage 8A §5） ──
    hyper_diag_removed = 0
    # 5a. 移除整块 ultra 诊断 section
    for block_pat in ULTRA_DIAG_BLOCKS:
        matches = list(re.finditer(block_pat, text, flags=re.DOTALL))
        hyper_diag_removed += len(matches)
        text = re.sub(block_pat, '', text, flags=re.DOTALL)
    # 5b. 逐行/逐注释删除内联 ultra 诊断
    for pat in ULTRA_DIAG_INLINE:
        matches = list(re.finditer(pat, text, flags=re.DOTALL | re.MULTILINE))
        hyper_diag_removed += len(matches)
        text = re.sub(pat, '', text, flags=re.DOTALL | re.MULTILINE)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # ── 写回 ──
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

    changed = (text != original)
    print(f'[完成] 版本标记清除: {stripped} 处')
    print('[完成] text-profile 注释块已移除')
    print(f'[完成] AI 流程残留清除: {residue_removed} 行')
    print(f'[完成] ultra 诊断记录清除: {hyper_diag_removed} 块')
    print(f'[状态] 内容变更: {"是" if changed else "否（仅元数据操作）"}')

    return stripped


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python3 strip-version-markers.py <对照文件.md>')
        sys.exit(1)
    strip_and_attrib(sys.argv[1])
