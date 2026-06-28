> ⚠ **此文件已降级为参考。** 自动并行模式（阶段 A–D）已废弃。
> 当前 max 技能使用混合模式管线（阶段 -2 → B1 → B2 → B3），见 `en-zh-max/SKILL.md` 或 `jp-zh-max/SKILL.md`。
> 本文档的子代理输出清理规则和合并脚本骨架仍适用于 B3 合并阶段，保留供参考。

# 子代理并行翻译模式

适用于**超长文本**（单篇 5,000+ 词）的翻译任务，按天然边界（章节、幕次）切割为独立子任务，派发子代理并行翻译。

## 何时使用

- 源文本 5,000–30,000+ 词，一次翻译会超上下文
- 文本有明显可独立的分段边界（书的章节、对话的幕次）
- 各段之间的术语和风格保持统一是关键风险点

## 前置准备

1. 提取全书纯文本 → 按对话/章节边界切割为 N 个独立文件
2. 编写统一的**术语映射表**（如 `prick→鸡巴 / cunt→屄 / libertine→浪荡子`）
3. 编写统一的**翻译原则**（语域、风格、标点规则）

## 委托代码

```python
delegate_task(tasks=[
    {
        "goal": "翻译第1部分（约10,000词）",
        "context": "术语表 + 风格指南 + 源文件路径",
        "toolsets": ["file", "terminal"]
    },
    {
        "goal": "翻译第2部分...",
        # ...
    },
])
```

## 连续文本的分割策略（无章节/标题时的操作）

当源文本是**连续叙事散文**（无章节标题、无幕次分界、无对话角色切换标记——如萨德《朱丽叶特》Part One）时，不能依赖"天然边界"。此时按**词数目标+段落边界**手动分割。

### 步骤

1. **提取全文**：用 zipfile 从 EPUB 提取所有 XHTML，合并同一章的多个文件（如 `part01.html` + `part01a.html` 可能同属一章）

2. **解析段落边界**：用 `</p>`→`\n\n` 保留段落结构，而非压缩全为单行。
   ```python
   text = re.sub(r'</p>', '\n\n', raw_text)
   lines = text.split('\n')
   ```

3. **寻找分割点**：遍历所有段落边界（空行位置），累计词数，找到最接近目标词数的边界：
   ```python
   para_boundaries = []
   cumulative = 0
   for i, line in enumerate(lines):
       if line.strip(): cumulative += len(line.split())
       if line.strip() == '' and cumulative > 0:
           para_boundaries.append((i, cumulative))
   # 找最接近 10K/20K/30K... 的边界
   for t in targets:
       closest = min(para_boundaries, key=lambda x: abs(x[1] - t))
   ```

4. **验证分割质量**：对每个分割点，检查前一段末尾和后一段开头是否语义连贯（不截断对话或论辩链）。若有截断，向相邻边界微调 ±1-2 段。

5. **产出独立源文件**：每个切片写入独立 `.txt`，文件名含 chunk 编号和词数以供参考。

6. **编写翻译指南**：为所有切片编写统一的术语映射表 + 翻译原则文件，每个子代理的 `context` 中均引用此文件。

### 注意

- 目标词数：单个子代理任务以 **10K–18K 词**为宜（基于 Sade 类文本的实测，子代理不会超上下文）
- 需为 5 段以上时，分批派发（每次 max_concurrent_children=3，等第一批返回后再发第二批）
- 分割后每个切片的内容混合度（性/哲学/叙事比例）可能不均，在 `context` 中说明当前切片的主要文本类型

## 关键风险

| 风险 | 缓解 |
|---|---|
| 术语不统一 | 在 `context` 字段提供完整术语映射表 |
| 风格不一致 | 提供前几幕已完成的中英对照样本段落 |
| 省略语域 | 明确说「不回避性词汇，直译」 |
| 子代理自行删文件 | 要求子代理将结果**返回**而非写文件；该写文件的路径必须明确给出 |
| **输出路径散落到主文件夹** | 在 `context` 中传递正确的项目目录路径（如 `Downloads/《书名》/`），不要传给子代理 Downloads 根目录。子代理保存文件时用 `os.makedirs(project_dir, exist_ok=True)` 确保目录存在 |

## 翻译成果集成步骤（子代理返回后的合并流程）

子代理各自返回独立翻译文件后，手动合并为一个连贯文档。以下是经实测的集成流程。

### 1. 清理子代理输出格式

子代理的翻译文件可能含有与主文件不兼容的格式标记，需统一清理：

| 不兼容项 | 清理方式 |
|---|---|
| 子代理自己加的 `#` 标题行（如 `# 朱丽叶特 第一部 第二段（共五段）`） | 删除除 Chunk 1 主标题外的所有 `# ` / `## ` / `### ` 行 |
| 子代理加的英文/双语副标题（如 `## Juliette, Part One — Chunk 2 (of 5)`） | 删除 |
| 中文文本加粗 `**中文译文**` | 移除 `**` |
| 多余的分隔线和脚注 `*本部分完。*` / `*第一段翻译完（共五段）*` | 移除 |
| 大量 `---` 分隔线（某个子代理可能在每段前都加 `---`，导致 150+ 条） | 全删，只在 chunk 之间插入一条 `---` |
| 子代理的文件头/尾注释 | 移除 |

**实测发现的常见子代理标记模式**（来自萨德《朱丽叶特》Part One 的 5 段并行翻译）：
- 每段开头插入 `# 朱丽叶特 第一部 第二段（共五段）` 类标题
- 末尾加 `*第X段翻译完（共五段）*` 脚注
- 某个子代理可能在每段前都加 `---`（导致 150+ 条分隔线）
- 中英对照格式不一致：有的段英文 blockquote 前有额外空行，有的没有

**推荐的合并脚本骨架**：

```python
import os, re

bilingual_dir = r'./bilingual'
output_dir = r'.'

# 读取所有 chunk
chunks = []
for i in range(1, N+1):  # N = chunk 总数
    fpath = os.path.join(bilingual_dir, f'Part1_chunk{i}_bilingual.md')
    with open(fpath, 'r', encoding='utf-8') as f:
        chunks.append(f.read())

merged_lines = []
for idx, chunk in enumerate(chunks):
    lines = chunk.split('\n')
    cleaned = []
    for line in lines:
        stripped = line.strip()
        # 删子代理加的标题行（保留 Chunk 1 的首次 # 标题）
        if stripped.startswith('# ') and idx > 0: continue
        if stripped.startswith('## ') or stripped.startswith('### '): continue
        # 删"完"标记
        if '完' in stripped and ('翻译' in stripped or '本段' in stripped or '本部分' in stripped): continue
        # 删所有 ---（合并时统一加）
        if stripped == '---': continue
        cleaned.append(line)
    chunk_text = '\n'.join(cleaned).strip()
    if idx == 0:
        merged_lines.append(chunk_text)
    else:
        merged_lines.extend(['', '---', '', chunk_text])

merged = '\n'.join(merged_lines)
merged = re.sub(r'\n{4,}', '\n\n\n', merged)

output_path = os.path.join(output_dir, '《书名》 翻译(中英对照).md')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(merged)
print(f'Merged: {output_path}')
```

### 2. 确认插入位置

在原文档中找到前一章节的结束处，确认插入点。常见锚点：章节分隔线 `---`、章节标题。

### 3. 更新对话标题格式

如果子代理输出了章节标题（如 `DIALOGUE THE FIFTH`），需确保与主文件格式一致——严格按 blockquote 格式：

```markdown
> DIALOGUE THE FIFTH
> DOLMANCE
> LE CHEVALIER
...

第五幕
多尔芒塞
骑士
...

---
```

### 4. 运行标点归一化

集成后务必重新跑 `scripts/normalize-punctuation.py`，因为子代理的标点可能未统一。

### 5. 验证完整性

集成后验证所有章节均存在且顺序正确：

```python
for phrase in ["DIALOGUE THE FIRST", ..., "DIALOGUE THE SEVENTH AND LAST"]:
    assert phrase in content, f"{phrase} missing!"
```

### 6. 哲学内容 vs 对话内容的委托差异

当子代理要翻译的内容性质不同时，术语表和翻译原则也应当不同：

- **性/色情场景**：性词汇直译表（鸡巴/屄/屁眼/操） + 口语化处理
- **哲学论述/小册子**：概念术语表示（Nature/大自然、virtue/美德、crime/罪行、republic/共和政体）+ 逻辑精确优先、18世纪论辩修辞
- **混合型**：两种诉求都在 `context` 中说明，给出两条术语表的交集和冲突处理规则

对于混合场景，委托的 `goal` 字段应当明确当前片段的主要文本类型。

## 本项目的实操经验（萨德《Philosophy in the Bedroom》第五幕）

- 第五幕 32,652 词，分为 3 段（Part1: 10,664 词性教育 → Part2: 18,580 词哲学小册子 → Part3: 3,408 词收尾）
- 每个子代理的 `context` 都包含完整术语表
- **关键**：Part 2 是纯哲学小册子内容（Frenchmen, Yet Another Effort），术语侧重不同——用概念术语表（Nature/美德/自由/共和政体）而非性器官表，同时保留 18 世纪论辩修辞
- 子代理返回后，手动合并 → 清理格式不兼容 → 跑标点归一化 → 生成 HTML → 封装 PDF
- 输出格式清理：子代理 Part 1 和 Part 3 用了 `**中文加粗**`，Part 2 则没有。集成前需统一移除加粗。

### 7. 整书级校验链（★ 合并后强制执行）

合并 + 标点归一化完成后，翻译**尚未完成**。必须执行以下三步校验链，与主技能阶段 7 完全对齐：

**步骤 1：`scribe:prose-reviewer`**
审查全书中译文的 AI 写作腔、翻译腔残留、禁用短语、语感漂移、结构单调。

**步骤 2：`verification-before-completion`**
全交付物完整性检查：MD 是否齐全、标点残留是否为 0、英中配对是否完整、humanizer 是否尚未执行。

**步骤 3：`humanizer`（★ 最终质量关卡·绝对不可跳过）**
整书级四维验证（Fidelity / Naturalness / Grammar / AI Patterns）+ 强制对抗自审 + 原位修复。此为并行翻译的最后一道质量关卡——子代理级质检无法发现跨 chunk 的语感漂移和术语不一致，只有 humanizer 的全局视角能覆盖。

> ⚠ 三项全部通过后，才可进入阶段 8（HTML/EPUB/MOBI 派生）。跳过任一项 = 翻译未完成。humanizer 的最终裁量权覆盖 prose-reviewer 的建议——冲突时以 humanizer 为准。
