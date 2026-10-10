---
name: en-zh-max
description: >-
  Use when the user wants 英译中 / 英译汉 / English to Chinese / translate English into Chinese, or to
  polish translationese out of a Chinese draft translated from English. Also when producing 英中对照
  bilingual output, or translating full-length English books. Not for Chinese-to-English, other source
  languages, pure Chinese writing polish, or single-word lookups.
license: MIT
version: 4.1.0
tags: [translation, english-to-chinese, english-chinese, chinese-translation, 英译汉, 英译中, 翻译, 润色, 中英对照, localization, book2skill, ye-zinan, translation-pipeline]
allowed-tools: Read Write Edit Bash
---

# en-zh-max · 英译汉翻译润色

把英文译成地道中文，产出英中对照译文。方法论来自叶子南《高级英汉翻译理论与实践》（第 4 版，清华大学出版社，2020）。

**统领原则是读者中心**：每个翻译决策，最后都追溯到「这个中文读者是谁，在什么语境下读」。
- 英译汉最致命的错误，是把英语的形合结构、名词化的抽象主语、长定语从句原样搬进汉语。
- 好译文以读者为中心，按文本类型调节归化尺度，发挥汉语意合的长处，兼顾音韵节奏。

五条原则贯穿全程：
1. 翻译前先分析文本（第十五章）。
2. 以译入语为依归（第一章）。
3. 灵活变通是核心能力（第十一章）。
4. 保护汉语的纯洁性（第九章）。
5. 文学翻译忌释义（第十四章）。

**英译汉的三处根本差异**：
1. **形合与意合**：英语靠连接词、关系代词、介词把逻辑关系显化，汉语靠语序和语境。because、although、which、that 不要逐个对成「因为」「虽然」「它／其」「的」。
2. **名词化抽象主语**：The confidence that…、The realization of… 这类主语要改成具体的人或物，或者把名词还原成动词。
3. **长定语从句**：英语定语可以向右无限扩展，汉语定语前置，容量有限。长的拆成流水短句，或改成状语。

## 1. 先定工作量
| 档 | 场景 | 读什么 | 产出 |
|---|---|---|---|
| 小 | 聊天里几句、一段 | 只读本文件 | 在回复里给对照，不落盘 |
| 中 | 一篇文章、一份文档 | 加读 `references/methods.md`（15 法速查）和 `references/translationese-symptoms.md` | `<名称> 翻译(中英对照).md`，跑机检 |
| 大 | 整本书、长篇系列，或一个会话译不完的长文（约 2 万词以上） | 中档全部，另读 `references/project-init.md`、`references/output-formats.md`、`references/handoff.md` | 逐章对照 md、全书合订、EPUB/MOBI；PDF 按需 |

**大档分会话做**，细则见 `references/handoff.md`：
- 逐章串行，不并行。每做完一章，跑 `python3 "$SKILL_DIR/scripts/handoff.py" meter --done <本会话已做完的章数>`（`$SKILL_DIR` 指本技能所在目录）。报「→ 交接」就落盘、写 HANDOFF.md、停下，请用户开新窗口续译。
- 用户说「续译 <目录>」，或项目目录里有 HANDOFF.md：按细则第 3 节续接，不从头读起。
- 用户说「自动接力」：主会话只调度，每章派一个新的子代理，仍然一章接一章。除此之外不派子代理。

## 2. 流程
### 第 0 步：定性
回答四个问题：
- 这是硬文本还是软文本？
- 属纽马克哪一类（表达、信息、呼唤）？
- 自由度大致几分（1–10）？
- 语域如何（正式、中性、口语、混合）？如果原文有粗话或性描写，再定语域脏度（1–5）。

详见 `references/methods.md` 第 1–3 法和 `references/text-analysis-and-qa.md` 小节 A。中档把结论用一句话告诉用户；大档写进 `translation-plan.md` 的开头。**不再往译文文件头写 text-profile 注释。**

**三档策略**：
- **偏硬（1–3）**：政治、法律、经贸、科技、合同、说明书。紧贴原文逻辑，选词精准，准确比流畅重要；术语用固定译法。为了精确付出一点「西化」，是合理的代价。
- **偏中（4–6）**：教科书、新闻、一般论述。两头平衡，默认用交际翻译。
- **偏软（7–9）**：文学、散文、评论、演讲、广告、宣传。大胆发挥意合与汉语之美，可以调结构、换形象，流畅和效果优先。

**语域脏度**：
| 档 | 含义 |
|---|---|
| 1 | 零脏字：纯技术、学术、公务 |
| 2 | 可俗不脏：口语、俗语，偶有轻微贬称 |
| 3 | 粗鄙自由：性和暴力场景直译，不回避 |
| 4 | 脏字对等：脏字按原文语域还原，性直白内容大胆译 |
| 5 | 猎奇极限：中文脏度不低于原文 |

- 判定方法：读原文前 500 到 1000 词再定档；拿不准时宁高勿低。
- 脏度和软硬是两回事，各自独立判定。
- **学术、评论类著作里的脏字，先问用户要保留到什么程度**，不要自己定档。例如卡特的 *The Sadeian Woman*，用户要求最低脏度，一律用「做爱、性交、阴茎」。

### 第 1 步：理解，脱离语言外壳
读懂原文后，在脑中形成图像或概念，再用中文重构，不要在字面上挪移（第 4 法）。
- 名词叠加、A of B 这类压缩结构，用解包袱法（第 6 法）。
- 简单句直译不通时，怀疑是套语，做替换测试（第 7 法）。
- 软文本再查关联意义和结构意义（第 5 法）。

### 第 2 步：初译
- **大档开译前必读 `TERMS_GLOSSARY.md`**。表中带 🟡🔴⚪ 语域标记的词，本章出现时一律按标记和角色口吻选词，不许退回中性词。
- **以意合起笔**：能不用连接词就不用；长句拆成流水短句；被动改主动；定语不要堆在名词前（第 9、10 法）。
- **翻译单位随档位变**：硬文本偏小，软文本偏大，默认以句子为单位（第 11 法）。

### 第 3 步：修订，一轮对照两张清单
1. **对着中文改**：
   - 按 `references/translationese-symptoms.md` 第八节的快速诊断清单，查形合迁移、前置定语过长、「的的不休」、被动滥用、抽象名词主语、习语硬译、语义关系不清。
   - 修法查 `references/techniques.md`。
   - 软文本读出声来打磨节奏：用双音节和四字结构，「偶字易适」。硬文本点到为止。
2. **对着原文改**：
   - 查准确性六项：重心、遗漏、结构意义、过度详解、逻辑、语域（第 15 法）。
   - 脏度 ≥ 3 时逐段核对语域：原文粗，中文不能洗白；原文雅，中文不能加码。
   - 软文本再查两项：作者刻意的形式保住了没有，有没有释义过度（第 13、14 法）。
   - 隐喻按档位决定（`references/text-analysis-and-qa.md` 小节 B）。

**理解错误零容忍**：放宽准确性，不等于可以理解错。

### 第 4 步：终审（大档每章一次，中档视篇幅）
对定稿后的整章跑一次 `humanizer`（翻译模式，只改中文行，不动英文 blockquote）。`humanizer-zh`、`prose-reviewer` 是可选项，用户要求或篇幅很长时再加。

### 第 5 步：机检与交付
```bash
python3 "$SKILL_DIR/scripts/check.py" zh "<名称> 翻译(中英对照).md" --fix     # 标点残留必须为 0，翻译腔信号逐处判断
python3 "$SKILL_DIR/scripts/strip-version-markers.py" "<名称> 翻译(中英对照).md"  # 清残留，补「译者：Lilipuut + Claude」署名和项目地址
```
- `$SKILL_DIR` 指本技能所在目录。
- check.py 报出的是信号，不是错误：「被」字、「一个」、「通过」等列出了每千字密度，结合档位判断。
- 需要 HTML、EPUB、MOBI 时，见 `references/output-formats.md`；PDF 用 `scripts/bilingual-to-pdf.py`。
- 小档聊天回复里的对照，也要手动套用中文全角标点。

## 3. 英中对照格式
- **逐段配对**：英文原段放进 blockquote（`> `），紧跟中文译文。
- **标点**：中文用全角。英文原文、链接、行内英文词句、数字缩写、代码保持半角。圆括号紧邻中文时才转全角。引号统一用 “ ” 和 ‘ ’。
- **只清提取噪声**：接回断行处的连字符，删掉页眉页脚，不要从中文反推英文。
- **标题**：译成中文 `##` 或 `###`，可以把英文标题放在上一行作 blockquote。
- **不放进 blockquote 的内容**：图片、表格、标题块，免得派生「全中文」版时被删掉。

```markdown
> It is a truth universally acknowledged that a single man in possession of a good fortune must be in want of a wife.

凡是有钱的单身汉，总想娶位太太，这是一条举世公认的真理。
```

## 4. 性和身体的直白描写
用户要求「不回避、直译」时，语域对齐优先于流畅归化：
- 不用委婉语（那话儿、玉茎、私处、后庭），也不换成医学术语。
- 原文用粗词，中文用同等直接的口语词：prick → 鸡巴，cunt → 屄，ass/anus → 屁眼，sodomite → 鸡奸者，fuck → 操、干，sperm → 精液。
- 原文用迂回、文雅的词（member、love-juice），中文也按原文的雅俗处理。
- 词表见：
  - `references/libertine-vocabulary.md`：萨德式浪荡文学。
  - `references/literary-fiction-sexual-register.md`：当代文学里临床语与口语混用的情况。

## 5. 文件路由
| 需要 | 读 |
|---|---|
| 15 个方法的做法和书中例子 | `references/methods.md` |
| 翻译腔症状和修法、西化的边界 | `references/translationese-symptoms.md` |
| 技巧库：词性转换、增减词、分句合句、语序、从句、被动、正反译 | `references/techniques.md` |
| 文本分析、隐喻决策、质检清单 | `references/text-analysis-and-qa.md` |
| 大档项目初始化（source/ 归位） | `references/project-init.md` |
| 大档分会话：交接、续接、自动接力 | `references/handoff.md` |
| EPUB、MOBI 原文提取 | `references/epub-extraction.md`、`references/mobi-extraction.md` |
| 派生全中文版、EPUB、MOBI、PDF | `references/output-formats.md`、`references/bilingual-html-template.md`、`references/playwright-pdf-generation.md` |
| 流程图 | `references/workflow.md` |

## 6. 润色边界（叶子南警告的三种过头）
- **不要过度归化**：别为了「地道」抹掉原文该留的风格、术语精度和文化标记。西化是一个连续体，有永久价值的文本能容纳更多异化。
- **不要堆砌四字成语**：音韵是手段，不是目的。
- **文学翻译不要释义**。

拿不准该改多狠时，回到第 0 步的档位：自由度越低，越克制。最终仍以读者为准。

## 7. 示例
> The confidence that the West would remain a dominant force in the 21st century is giving way to a sense of foreboding.

西方曾笃信自己将在 21 世纪稳居主导地位，如今这份自信，正让位于一种隐隐的不祥之感。

这句的定性：偏硬的政论文，自由度约 3，准确优先，音韵点到为止。
