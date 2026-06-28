# en-zh-max — 英译汉翻译 Claude Code Skill

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-9cf)](https://docs.anthropic.com/en/docs/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Release](https://img.shields.io/badge/release-v3.1.0-blue)](https://github.com/3060226349kk-cmd/en-zh-max/releases/latest)
[![Version](https://img.shields.io/badge/version-3.1.0)](SKILL.md)

[🇨🇳 中文](#en-zh-max--英译汉翻译-claude-code-skill) · [🇬🇧 English](#en-zh-max--english-to-chinese-translation-for-claude-code)

> 英文→中文翻译与润色。9 阶段工作流 + 叶子南《高级英汉翻译理论与实践》17 个蒸馏技能 + 4 层校验链 + 语域脏度管线。
> 专为 Claude Code 设计，输出英中对照译文。
>
> 📊 [完整工作流流程图（含校验链）](ultra/WORKFLOW.md)

---

## 目录

- [这是什么？](#这是什么)
- [方法论基石](#方法论基石)
- [工作流管线](#工作流管线)
- [校验链](#校验链)
- [快速安装](#快速安装)
- [快速使用](#快速使用)
- [项目结构](#项目结构)
- [贡献指南](#贡献指南)
- [致谢](#致谢)
- [许可](#许可)

---

## 这是什么？

**en-zh-max** 是 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 的翻译 skill，将英文译为地道中文并产出英中对照译文。集成了叶子南《高级英汉翻译理论与实践》（清华大学出版社，2020）经 book2skill 蒸馏的 **17 个翻译技能**。

### 英译汉三大核心差异

英译汉有三重根本不同，en-zh-max 的设计围绕这三者展开：

1. **形合 vs 意合的根本对立**——英语靠连接词、关系代词、介词显化逻辑关系（形合），汉语靠语序、语境、对偶暗示关系（意合）。英译汉最大错误是把 `because` `although` `which` `that` 逐个机械对应为「因为」「虽然」「它/其」「的」——结果句子臃肿、「的的不休」。

2. **名词化抽象主语的汉语困境**——英语偏好抽象名词作主语（`The confidence that...`、`The realization of...`），中文偏好具体的人/物作主语。直译抽象主语造成译文漂浮、无人味。

3. **长定语从句的堆叠压力**——英语定语从句可以右向无限扩展（`the man who... which... that...`），中文定语必须前置且容量有限。核心策略是拆成流水短句或转状语从句。

---

## 方法论基石

本 skill 的方法论根基是叶子南《高级英汉翻译理论与实践》（清华大学出版社，2020），经 book2skill 管线蒸馏为可执行的 17 个技能。核心理论框架如下。

### 五大统领原则

> **「翻译前先分析文本」**——七维度诊断 + 自由度评分，先定位再动笔（第十五章）
>
> **「以译入语为依归」**——总方向是靠近读者、发挥汉语优势（第一章）
>
> **「灵活变通为核心能力」**——摆脱原文语言结构的束缚（奈达理论，第十一章）
>
> **「保护汉语纯洁性」**——警惕西化汉语蔓延，译者肩负纯洁本国语言的使命（第九章）
>
> **「文学翻译忌释义」**——文学翻译中保留原文语言形式优先于转述内容（第十四章）

### 17 个蒸馏技能覆盖

四组方法论：

| 分组 | 技能 | 应用阶段 |
|------|------|---------|
| **文本分析与策略**（4 技能） | 文本分析七维度与自由度评估、纽马克文本分类翻译策略、翻译基本问题决策框架、奈达功能对等三支柱 | 预读取 + 阶段 0 |
| **理解与转换**（5 技能） | 三大语义类型分析、翻译思维三阶段、解包袱法、英汉五层次对比分析、翻译单位动态选择 | 阶段 0-2 |
| **润色与质量**（5 技能） | 套语"水vs冰"识别、西化表达六维评估、认知隐喻发现、翻译准确性六维校验、文学反释义 | 阶段 3-7 |
| **风格与修辞**（3 技能） | 前景化翻译处理、文学翻译反释义法、翻译思维三阶段法 | 阶段 7（软文本） |

详见 [`ultra/SKILL_MAP.md`](ultra/SKILL_MAP.md) 查看每个技能与工作流阶段的精确映射关系。

---

## 工作流管线

en-zh-max 的工作流由 **9 个阶段** 组成，其中 6 个阶段引入了叶子南方法论的具体技能。各阶段概述如下（具体门禁条件与脚本路径见 [SKILL.md](SKILL.md)）。

### 预备阶段

| 阶段 | 名称 | 职责 |
|------|------|------|
| **-2** | 预扫描与策略决定 | 统计字数、决定串行/混合模式、产出 `translation-plan.md` |
| **-1** | 项目目录初始化 | 创建 `source/` 目录、文件归位、格式提取 |
| **-0.5** | 方法论预读取批 | 一次性读取 17 个方法论 SKILL.md，建立全流程方法论地基 |

### 核心翻译管线（阶段 0→6）

| 阶段 | 名称 | 职责 |
|------|------|------|
| **0** | 文本分析 | 定归化档位（偏硬/偏中/偏软）、text-profile（含**语域脏度 1-5**）、七维度诊断 + 自由度评分 |
| **1** | 理解与脱壳 | 脱离英文语言外壳、解包袱法、核心句转换 |
| **2** | 初译 | 意合优先起译、拆长句、形合→意合转换；应用五层次对比 + 翻译单位选择 |
| **2.5** | 语域对齐 ★ | 脏度≥3 时强制逐段核验语域对等，修正脏度偏差 |
| **3** | 润色诊断 | 翻译腔清除（8 类症状）、套语识别、西化六维评估 |
| **4** | 音韵打磨 | 朗读校准、双音节/四字结构、节奏重组（软文本放开，硬文本点到为止） |
| **5** | 质检 | **16 项自检**（12 项通用 + 4 项语域专项）、原文对照修正；应用准确性六维校验 |
| **6** | 标点规范化 | 机械执行 `normalize-punctuation.py`，中文标点全角→残留 0 |

### 交付（阶段 8）

| 步骤 | 职责 |
|------|------|
| **8A** | 最终清理：剥夺版本标记、删除 text-profile、添加译者署名（`strip-version-markers.py`）、清理 AI 流程残留 |
| **8B** | 派生交付物：英中对照 MD/HTML/EPUB/MOBI/PDF（按需） |

### 超长文本并行翻译（混合模式）

当全书 ≥ 7 章时，采用 B1/B2/B3 混合管线：

- **阶段 B1**：基线章串行翻译（前 1-2 章，建立风格基线、术语决策记录、句法先例）
- **阶段 B2**：批量章并行翻译（剩余章，子代理执行精简管线，注入风格基线）
- **阶段 B3**：合并与整书串行校验（按序拼接 → 阶段 7 完整校验链 → 阶段 8 清理与交付）

≤ 6 章时完全串行，无需混合模式。详见 [SKILL.md](SKILL.md)「全文翻译混合模式管线」。

---

## 校验链

翻译文本落盘后、交付物生成前，必须经过以下 **4 步校验**。任一步发现问题 → 回到对应阶段修复 → 重走校验链。**不可跳过任一步骤。**

```
阶段 6（标点规范化）
       ↓
① scribe:prose-reviewer       — AI 腔 / 翻译腔 / 语感漂移
       ↓
② verification-before-completion — 交付物完整性 + 英中对齐
       ↓
③ humanizer                   — 四维验证（Fidelity / Naturalness / Grammar / AI Patterns）
                                 + 强制对抗式自审
       ↓
④ humanizer-zh                — 中文 AI 痕迹终审（24 条规则）
       ↓
阶段 8（交付）
```

### 步骤 1：scribe:prose-reviewer

审查中文译文的 AI 写作腔、翻译腔残留、禁用短语、语感漂移、结构单调。**参考意见**——所建议的修改由 humanizer（步骤 3）拥有最终裁量权。

### 步骤 2：verification-before-completion

全交付物完整性检查：MD/HTML 是否齐全、标点残留是否为 0、英中对齐是否完整、原文件是否在 `source/` 内。确认「humanizer 尚未执行」等运行状态。

软文本（自由度 ≥ 4）在此步后插入修辞技能：前景化 + 反释义。

### 步骤 3：humanizer

将中文译文按段落切割为 chunk（每块 3-5 段），对每个 chunk 执行四维验证：

- **Fidelity**（忠实度：逐句对照源文，检查语义等价/否定/情态/专名）
- **Naturalness**（自然度：翻译腔/语感/语域）
- **Grammar**（语法错字：搭配/标点/一致）
- **AI Patterns**（AI 痕迹：29 种模式）

通过后执行**强制对抗式自审**——对全部已通过的 chunk 重新逐句审查，防止系统性盲区遗漏。

humanizer 对 prose-reviewer 的建议拥有**最终裁量权**：批准、拒绝、或发现其遗漏的问题。

### 步骤 4：humanizer-zh

仅处理中文译文行（过滤英文 blockquote），按 chunk 逐块过 **24 条中文 AI 痕迹规则**（四大类 × 6 条：内容模式 / 语言语法 / 风格模式 / 交流填充）。检测并修复 AI 高频词汇、破折号滥用、三段式排比、否定式排比、系动词回避、虚假范围、填充短语、通用积极结论等。

**职责边界**：humanizer 负责「译得对」（Fidelity + Naturalness + Grammar），humanizer-zh 负责「读起来像人写的」（中文 AI 痕迹清除）。两者各司其职。

### 自动修正规则

校验链四步中发现的任何错误或问题，**默认自动修正**并直接写入对照 MD 文件，不等待逐条批准。修正后的 MD 是阶段 8 派生 HTML/EPUB/MOBI 的唯一输入源。

---

## 快速安装

### 方式 1：克隆到 Claude Code skills 目录（推荐）

```bash
cd ~/.claude/skills/
git clone https://github.com/3060226349kk-cmd/en-zh-max.git en-zh-max
```

克隆完成后，`references/`、`scripts/`、`ultra/` 子目录自动就位，工作流脚本路径自洽。

### 方式 2：手动复制

将仓库内以下内容完整复制到 `~/.claude/skills/en-zh-max/`：

```
SKILL.md
references/
scripts/
ultra/
```

**注意**：工作流脚本（`normalize-punctuation.py`、`strip-version-markers.py`）和 `ultra/` 方法论文件通过相对路径引用。手动复制必须保持目录结构完整，否则阶段 6 标点规范化与阶段 8A 最终清理的脚本执行会失败。

### 环境要求

| 依赖 | 版本要求 | 用途 | 必需/可选 |
|------|---------|------|----------|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | 最新版推荐 | 运行本 skill 的宿主 CLI | **必需** |
| Python | 3.8+ | 运行 `scripts/` 下辅助脚本 | **必需** |
| Git | — | 克隆仓库、版本管理 | **必需** |
| pip: `playwright` | 最新 | HTML → PDF 渲染（`bilingual-to-pdf.py`） | 可选① |
| pip: `ebooklib` | 最新 | EPUB 生成（`output-formats.md` 脚本） | 可选① |
| pip: `PyMuPDF` (`fitz`) | 最新 | PDF 文本提取（`project-init.md` 脚本） | 可选② |
| [Pandoc](https://pandoc.org) | 最新 | 文本格式转换（EPUB/MOBI/PDF 输出中间件） | 可选① |
| [Kindle Previewer 3](https://www.amazon.com/gp/feature.html?docId=1000765261)（含 `kindlegen`） | 3.x | EPUB → MOBI 转换 | 可选① |
| [Calibre](https://calibre-ebook.com)（`ebook-convert`） | 最新 | AZW3/MOBI 格式转换 | 可选① |
| [marker-pdf](https://github.com/VikParuchuri/marker)（`marker`） | 最新 | 扫描版 PDF OCR→文本 | 可选② |

> **①** 仅当需要该输出格式时安装（英中对照 MD 是所有格式的源头，MD 本身不需要任何额外工具）。
> **②** 仅当待译原文为扫描版 PDF 或特殊格式时安装。普通文本文件/EPUB 无需。

脚本依赖路径配置：

```bash
# Playwright（PDF 渲染）— 安装一次即可
pip install playwright && python3 -m playwright install chromium

# Kindlegen（MOBI 生成）— 通过 Kindle Previewer 3 安装，确认 PATH 或脚本路径
# 修改 references/output-formats.md 中的 KINDLEGEN 变量指向你的实际安装路径
```

### 所需 Skill 依赖

本 skill 的校验链和方法论依赖以下 Claude Code skill：

| Skill | 官方来源 | 用途 | 安装方式 |
|-------|---------|------|---------|
| [superpowers](https://github.com/obra/superpowers) | `obra/superpowers` | 校验链步骤：`verification-before-completion` | `cd ~/.claude/skills/ && git clone https://github.com/obra/superpowers.git` |
| scribe | [Claude Code 内置工具](https://docs.anthropic.com/en/docs/claude-code/plugins) | 校验链步骤：`scribe:prose-reviewer`（AI 腔/翻译腔审查） | Claude Code 自带，无需额外安装 |
| [humanizer](https://github.com/blader/humanizer) | `blader/humanizer` | 校验链步骤：四维验证（Fidelity / Naturalness / Grammar / AI Patterns）+ 强制对抗自审 | `cd ~/.claude/skills/ && wget -O SKILL.md https://raw.githubusercontent.com/blader/humanizer/main/SKILL.md` |
| humanizer-zh | 派生自 `blader/humanizer`（中文适配） | 校验链步骤：中文 AI 痕迹终审（24 条规则） | 同 `humanizer`，中文规则已翻译适配 |

> en-zh-max 的工作流本身不依赖以上 skill 即可运行基础翻译（阶段 0-6），但校验链（阶段 7）和方法论增强阶段（阶段 -0.5/0/1/2/3/5）需要对应 skill 就位。
>
> 安装命令均在 Claude Code skills 目录下执行 `git clone`，与 en-zh-max 本身的安装方式一致。

---

## 快速使用

在 Claude Code 中提出翻译请求：

```
英译中：
（你的英文原文）
```

或从文件翻译：

```
把这个文件翻译成中文
```

Claude Code 将自动触发 en-zh-max skill，执行完整工作流管线。首次使用会自动加载方法论预读取批（阶段 -0.5），建立方法论地基。

---

## 项目结构

```
en-zh-max/
├── SKILL.md                       # 运行时指令：完整工作流、准入/准出门禁、脚本路径
├── README.md                      # 本文件
├── LICENSE                        # MIT
├── .gitignore
├── references/                    # 方法论文档（翻译技巧、陷阱清单、文本分析框架）
│   ├── bilingual-html-template.md      # 英中对照 HTML 模板（CEU Navy CSS）
│   ├── epub-extraction.md              # EPUB 文本提取方法
│   ├── libertine-vocabulary.md          # 性/身体直白内容语域对等词汇表
│   ├── literary-fiction-sexual-register.md  # 当代文学性描写混合语域指南
│   ├── mobi-extraction.md              # MOBI 文本提取方法
│   ├── output-formats.md               # 派生交付物（HTML/EPUB/MOBI/PDF）生成脚本
│   ├── parallel-delegation.md          # 超长文本并行翻译（分割→派发→集成）
│   ├── playwright-pdf-generation.md    # Playwright HTML→PDF 封装方案
│   ├── project-init.md                 # 阶段 -1 项目目录初始化详细步骤
│   ├── techniques.md                   # 英译汉技巧库（词性转换、增减词、分句合句等）
│   ├── text-analysis-and-qa.md         # 文本分析框架 + 归化尺度 + 质检标准
│   └── translationese-symptoms.md      # 翻译腔 8 类症状清单与修正方法
├── scripts/                       # 工作流辅助脚本
│   ├── normalize-punctuation.py        # 阶段 6：中文标点全角归一化（机械执行）
│   ├── strip-version-markers.py        # 阶段 8A：剥夺版本标记 + 清理 + 译者署名
│   └── bilingual-to-pdf.py             # 英中对照 MD → HTML + PDF（按需）
└── ultra/                         # 方法论组件（叶子南 17 技能的文件映射与流程图）
    ├── SKILL_MAP.md                   # 17 个技能与工作流阶段映射表（含跳过规则速查）
    └── WORKFLOW.md                    # 翻译工作流流程图（Mermaid，含校验链）
```

---

## 贡献指南

**维护者：** [Lilipuut](https://github.com/3060226349kk-cmd) — 项目创建者，负责核心工作流设计与方法论集成。

本 skill 欢迎贡献。以下指引帮助您理解项目结构并有效参与。

### 开发环境准备

1. 安装 [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
2. 克隆本仓库到 `~/.claude/skills/en-zh-max/`

### 贡献流程

1. **开 issue**：在 [Issues](https://github.com/3060226349kk-cmd/en-zh-max/issues) 描述改动目标，确保与其他贡献者不冲突
2. **Fork + Branch**：从 `main` 创建 feature branch（如 `fix/punctuation-typo`、`feat/new-reference`）
3. **改动范围**：
   - `SKILL.md`：工作流阶段的门禁条件、脚本路径、方法论引用
   - `references/*.md`：翻译技巧、陷阱清单的增补或修正
   - `scripts/*.py`：辅助脚本的功能扩展或 bug 修复
   - `ultra/*.md`：方法论映射表或工作流流程图的更新
   - `README.md`：中文版 + 英文版同时更新（精确对称原则）
4. **提交**：commit message 以前置标签开头，如 `[SKILL]` `[REF]` `[SCRIPT]` `[ULTRA]` `[DOC]`
5. **PR**：关联 issue，描述改动内容与验证方式

### 代码规范

- SKILL.md：保留 YAML frontmatter（`name` / `description` / `version` / `allowed-tools`），工作流阶段标注准入/准出门禁
- references/*.md：每条技巧以有编号的列表条目呈现，引用原文出处（叶子南原书页码）
- scripts/*.py：兼容 Python 3.8+，不接受外部依赖；文件路径通过 `$SKILL_DIR` 环境变量或相对路径解析
- 跨平台注意：脚本路径在 Windows（git-bash）和 macOS/Linux 下均需可运行
- 新增方法论文档需在 `SKILL_MAP.md` 中注册其阶段映射

### 发布流程

1. 版本号更新：`SKILL.md` 的 YAML `version` 字段 + README badge 链接
2. CHANGELOG（可选）记录每次版本的主要变更
3. 合并到 `main` 后即通过 `git clone` 可获取最新版本

---

## 致谢

**项目作者：** [Lilipuut](https://github.com/3060226349kk-cmd) — en-zh-max 整体架构设计、方法论集成与实现。

本 skill 的基本框架源自 [en-zh-translation-polish](https://github.com/HoraceLuBFA/en-zh-translation-polish)（英汉翻译打磨），在其 7 阶段工作流基础上扩展为完整版。感谢原技能的架构设计。

书中 17 个翻译技能的蒸馏提取通过 [cangjie-skill](https://github.com/3060226349kk-cmd/cangjie-skill) 的 book2skill 管线完成。

特别鸣谢 **叶子南** 教授——《高级英汉翻译理论与实践》（清华大学出版社，2020）为整套方法论提供了系统理论基石。本书的文本分析七维度法、解包袱法、英汉五层次对比、套语水冰识别、西化表达六维评估等核心概念，构成了本 skill 每个阶段的学理支撑。

校验链中的 `verification-before-completion` 步骤来自 [Superpowers](https://github.com/obra/superpowers) 技能集、`scribe:prose-reviewer` 来自 [scribe](https://github.com/anthrxc/scribe)、`humanizer` 与 `humanizer-zh` 为独立校验管线。感谢各技能的开放架构。

---

## 许可

[MIT](LICENSE) © 2026 Lilipuut

[↑ 回到顶部](#en-zh-max--英译汉翻译-claude-code-skill) · [🇬🇧 English](#en-zh-max--english-to-chinese-translation-for-claude-code)

---

---

# en-zh-max — English to Chinese Translation for Claude Code

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-9cf)](https://docs.anthropic.com/en/docs/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.1.0)](SKILL.md)

> English→Chinese translation & polish. 9-stage workflow + 17 distilled skills from Ye Zinan's *Advanced English-Chinese Translation Theory and Practice* + 4-step validation chain + register dirtiness pipeline.
> Designed for Claude Code, outputs bilingual parallel text.
>
> 📊 [Full workflow diagram (with validation chain)](ultra/WORKFLOW.md)

---

## Table of Contents

- [What Is This?](#what-is-this)
- [Theoretical Foundation](#theoretical-foundation)
- [Workflow Pipeline](#workflow-pipeline)
- [Validation Pipeline](#validation-pipeline)
- [Quick Install](#quick-install)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)
- [License](#license)

---

## What Is This?

**en-zh-max** is a [Claude Code](https://docs.anthropic.com/en/docs/claude-code) translation skill that renders English into idiomatic Chinese with bilingual parallel output. It integrates **17 distilled skills** from Ye Zinan's *Advanced English-Chinese Translation Theory and Practice* (Tsinghua University Press, 2020) via the book2skill pipeline.

### Three Fundamental English→Chinese Challenges

en-zh-max is designed around three challenges that distinguish English→Chinese from other language pairs:

1. **Hypotaxis vs Parataxis**—English uses conjunctions, relative pronouns, and prepositions to make logical relationships explicit (hypotaxis); Chinese relies on word order, context, and parallelism to imply those relationships (parataxis). The single deadliest habit in E→C translation is mechanically mapping every `because`, `although`, `which`, and `that` to Chinese equivalents, producing bloated sentences littered with "因为"s and "的"s.

2. **Nominalized Abstract Subjects**—English favors abstract nouns as subjects ("The confidence that...", "The realization of..."); Chinese prefers concrete persons or things as subjects. Translating abstract subjects literally makes the Chinese feel disembodied and bloodless.

3. **Stacked Attributive Clauses**—English relative clauses can extend rightward indefinitely ("the man who... which... that..."), but Chinese modifiers must precede the noun with strict length limits. The core strategy is to break long attributives into short flowing clauses or convert them to adverbial clauses.

---

## Theoretical Foundation

The skill's methodology is rooted in Ye Zinan's *Advanced English-Chinese Translation Theory and Practice* (Tsinghua University Press, 2020), distilled into 17 executable skills via the book2skill pipeline.

### Five Governing Principles

> **"Analyze before you translate"**—Seven-dimension diagnosis + freedom score; position yourself before moving the pen (Chapter 15)
>
> **"The target language has the last word"**—The overall direction is toward the reader, leveraging the strengths of Chinese (Chapter 1)
>
> **"Flexibility is the core competence"**—Free yourself from the source language's structural cage (Nida's theory, Chapter 11)
>
> **"Protect the purity of Chinese"**—Beware of the spread of Westernized Chinese; the translator has a duty to preserve the native language (Chapter 9)
>
> **"Paraphrase is the enemy of literary translation"**—In literary translation, preserving the source text's linguistic form takes priority over paraphrasing content (Chapter 14)

### 17 Distilled Skills

Four methodology groups:

| Group | Skills | Applied In |
|-------|--------|-----------|
| **Text analysis & strategy** (4) | Seven-dimension diagnosis & freedom assessment, Newmark's text typology translation strategy, Basic translation problem decision framework, Nida's three-pillar functional equivalence | Preload + Phase 0 |
| **Comprehension & conversion** (5) | Three-type semantic analysis, Three-stage translation thinking, Unpacking method, Five-level E-C contrastive analysis, Dynamic translation unit selection | Phases 0-2 |
| **Polish & quality** (5) | Formulaic language "water vs ice" identification, Six-dimension Westernization assessment, Cognitive metaphor discovery, Six-dimension accuracy checklist, Literary anti-paraphrase | Phases 3-7 |
| **Style & rhetoric** (3) | Foregrounding processing, Literary anti-paraphrase method, Three-stage translation thinking method | Phase 7 (soft texts) |

See [`ultra/SKILL_MAP.md`](ultra/SKILL_MAP.md) for the complete mapping between each skill and its workflow phase.

---

## Workflow Pipeline

en-zh-max's workflow comprises **9 phases**, 6 of which incorporate specific skills from Ye Zinan's methodology. The following is a structural overview; gate conditions and script paths are documented in [SKILL.md](SKILL.md).

### Preparation Phases

| Phase | Name | Responsibility |
|-------|------|---------------|
| **-2** | Pre-scan & strategy decision | Word count, decide serial/hybrid mode, output `translation-plan.md` |
| **-1** | Project directory init | Create `source/`, move files, extract formats |
| **-0.5** | Methodology preload batch | Read 17 methodology SKILL.md files in one pass to establish a full-pipeline foundation |

### Core Translation Pipeline (Phases 0→6)

| Phase | Name | Responsibility |
|-------|------|---------------|
| **0** | Text analysis | Set domestication level (hard/mid/soft), write text-profile (with **register dirtiness 1-5**), seven-dimension diagnosis + freedom score |
| **1** | Comprehension & deverbalization | Strip English surface forms, unpacking method, kernel sentence conversion |
| **2** | First draft | Parataxis-first drafting, long sentence splitting, hypotaxis→parataxis conversion; apply five-level contrastive analysis + translation unit selection |
| **2.5** | Register alignment ★ | Forced per-paragraph register parity check when dirtiness ≥ 3, correct dirtiness drift |
| **3** | Polish diagnosis | Translationese cleanup (8 symptom classes), formulaic language identification, six-dimension Westernization assessment |
| **4** | Prosody polish | Read-aloud calibration, disyllabic/tetrasyllabic rhythm, pace restructuring (soft texts only) |
| **5** | Quality check | **16-item self-check** (12 general + 4 register-specific), source-target comparison; apply six-dimension accuracy checklist |
| **6** | Punctuation normalization | Mechanical: `normalize-punctuation.py`, Chinese fullwidth conversion → residual 0 |

### Delivery (Phase 8)

| Step | Responsibility |
|------|---------------|
| **8A** | Final cleanup: strip version markers, delete text-profile, add translator credit (`strip-version-markers.py`), clean AI workflow artifacts |
| **8B** | Generate deliverables: bilingual MD/HTML/EPUB/MOBI/PDF (on demand) |

### Parallel Translation for Long Texts (Hybrid Mode)

When the full text has ≥ 7 chapters, the B1/B2/B3 hybrid pipeline activates:

- **Phase B1**: Baseline chapter serial translation (first 1-2 chapters, establishes style baseline, terminology decision record, syntax precedents)
- **Phase B2**: Batch chapter parallel translation (remaining chapters, sub-agents run streamlined pipeline, inject style baseline)
- **Phase B3**: Merge & full-text serial validation (concatenate → Phase 7 full validation chain → Phase 8 cleanup & delivery)

≤ 6 chapters: fully serial, no hybrid mode. See [SKILL.md](SKILL.md) for details.

---

## Validation Pipeline

After the translation is written to disk and before deliverables are generated, the following **4-step chain** must execute in order. Any failure → return to the relevant phase → re-run the chain. **No step may be skipped.**

```
Phase 6 (Punctuation Normalization)
       ↓
① scribe:prose-reviewer            — AI-isms / translationese / prosodic drift
       ↓
② verification-before-completion   — deliverable integrity + bilingual alignment
       ↓
③ humanizer                        — 4-dimension validation (Fidelity / Naturalness /
                                       Grammar / AI Patterns)
                                     + forced adversarial self-review
       ↓
④ humanizer-zh                     — Chinese AI-trace final review (24 rules)
       ↓
Phase 8 (Delivery)
```

### Step 1: scribe:prose-reviewer

Audits the Chinese translation for AI writing patterns, residual translationese, banned phrases, register drift, and structural monotony. **Advisory**—proposed edits are subject to final approval by humanizer (Step 3).

### Step 2: verification-before-completion

Full deliverable integrity check: MD/HTML completeness, punctuation residual (must be 0), bilingual segment alignment, source file presence in `source/`. Confirms operational state ("humanizer not yet executed," etc.).

For soft texts (freedom ≥ 4), inserts rhetorical skills after this step: foregrounding + anti-paraphrase.

### Step 3: humanizer

Splits the Chinese translation into chunks (3-5 paragraphs each) and runs 4-dimension validation on each:

- **Fidelity**: sentence-by-sentence source comparison (semantic equivalence, negation, modality, proper nouns)
- **Naturalness**: translationese, prosodic feel, register fit
- **Grammar**: collocation, punctuation, agreement
- **AI Patterns**: 29 AI writing pattern rules

After all chunks pass, executes **forced adversarial self-review**—re-examines every already-passed chunk from scratch to catch systematic blind spots.

humanizer has **final authority** over prose-reviewer's suggestions: approve, reject, or detect issues prose-reviewer missed.

### Step 4: humanizer-zh

Processes only Chinese translation lines (filters English blockquote lines). Runs each chunk against **24 Chinese AI-trace rules** (4 categories × 6: content patterns / language grammar / style patterns / conversational fillers). Detects and fixes: AI high-frequency vocabulary, em-dash overuse, three-part parallelism, negative parallelism, copula avoidance, false scope, filler phrases, generic positive conclusions, etc.

**Role boundary**: humanizer ensures "correctness" (Fidelity + Naturalness + Grammar); humanizer-zh ensures "reads like human writing" (Chinese AI trace removal). The two are complementary and non-substitutable.

### Auto-fix Rules

Any error or issue discovered during the 4-step chain is **auto-fixed by default** and written directly into the bilingual MD file. No per-item approval is required. The corrected MD is the sole input source for Phase 8 deliverable generation (HTML/EPUB/MOBI).

---

## Quick Install

### Method 1: Clone to Claude Code skills directory (recommended)

```bash
cd ~/.claude/skills/
git clone https://github.com/3060226349kk-cmd/en-zh-max.git en-zh-max
```

After cloning, all subdirectories (`references/`, `scripts/`, `ultra/`) are in place with self-consistent script paths.

### Method 2: Manual copy

Copy the following to `~/.claude/skills/en-zh-max/`:

```
SKILL.md
references/
scripts/
ultra/
```

**Note**: Workflow scripts (`normalize-punctuation.py`, `strip-version-markers.py`) and `ultra/` methodology files rely on relative path resolution. Manual copy must preserve the full directory structure, otherwise Phase 6 normalization and Phase 8A cleanup scripts will fail.

### Requirements

| Dependency | Version | Purpose | Required |
|-----------|---------|---------|----------|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | latest | Host CLI for this skill | **Required** |
| Python | 3.8+ | Helper scripts in `scripts/` | **Required** |
| Git | — | Clone & version management | **Required** |
| pip: `playwright` | latest | HTML → PDF rendering (`bilingual-to-pdf.py`) | Optional¹ |
| pip: `ebooklib` | latest | EPUB generation (`output-formats.md` scripts) | Optional¹ |
| pip: `PyMuPDF` (`fitz`) | latest | PDF text extraction (`project-init.md` scripts) | Optional² |
| [Pandoc](https://pandoc.org) | latest | Format conversion (EPUB/MOBI/PDF intermediary) | Optional¹ |
| [Kindle Previewer 3](https://www.amazon.com/gp/feature.html?docId=1000765261) (incl. `kindlegen`) | 3.x | EPUB → MOBI conversion | Optional¹ |
| [Calibre](https://calibre-ebook.com) (`ebook-convert`) | latest | AZW3/MOBI format conversion | Optional¹ |
| [marker-pdf](https://github.com/VikParuchuri/marker) (`marker`) | latest | Scanned PDF OCR → text | Optional² |

> ¹ Only needed when generating that specific output format (bilingual MD is the source of all formats and requires no extra tools).
> ² Only needed when the source text is a scanned PDF or special format. Plain text/EPUB files need none.

Script path configuration:

```bash
# Playwright (PDF rendering) — install once
pip install playwright && python3 -m playwright install chromium

# Kindlegen (MOBI) — installed via Kindle Previewer 3; update KINDLEGEN path
# in references/output-formats.md to match your installation
```

### Required Skills

The validation pipeline and methodology enhancements rely on these Claude Code skills:

| Skill | Official Source | Purpose | Install |
|-------|----------------|---------|---------|
| [superpowers](https://github.com/obra/superpowers) | `obra/superpowers` | Validation chain: `verification-before-completion` | `cd ~/.claude/skills/ && git clone https://github.com/obra/superpowers.git` |
| scribe | [Claude Code built-in](https://docs.anthropic.com/en/docs/claude-code/plugins) | Validation chain: `scribe:prose-reviewer` (AI-isms/translationese audit) | Ships with Claude Code, no extra install needed |
| [humanizer](https://github.com/blader/humanizer) | `blader/humanizer` | Validation chain: 4-dimension check (Fidelity/Naturalness/Grammar/AI Patterns) + adversarial self-review | `cd ~/.claude/skills/ && wget -O SKILL.md https://raw.githubusercontent.com/blader/humanizer/main/SKILL.md` |
| humanizer-zh | Derived from `blader/humanizer` (Chinese adaptation) | Validation chain: Chinese AI-trace final review (24 rules) | Same as `humanizer`, with translated Chinese rules |

> en-zh-max's base translation workflow (Phases 0-6) runs without these skills, but the validation chain (Phase 7) and methodology-enhanced phases (-0.5/0/1/2/3/5) require them.
>
> All install via `git clone` in `~/.claude/skills/`, same as en-zh-max itself.

---

## Quick Start

In Claude Code, make a translation request:

```
Translate this English to Chinese:
(your text here)
```

Or translate from a file:

```
Translate this file to Chinese
```

Claude Code will automatically invoke the en-zh-max skill and execute the full workflow pipeline. On first run, the methodology preload batch (Phase -0.5) loads automatically to establish the full-pipeline foundation.

---

## Project Structure

```
en-zh-max/
├── SKILL.md                       # Runtime instructions: full workflow, gate conditions, script paths
├── README.md                      # This file
├── LICENSE                        # MIT
├── .gitignore
├── references/                    # Methodology documents (techniques, trap lists, text analysis)
│   ├── bilingual-html-template.md      # Bilingual HTML template (CEU Navy CSS)
│   ├── epub-extraction.md              # EPUB text extraction method
│   ├── libertine-vocabulary.md          # Register-matched vocabulary for explicit content
│   ├── literary-fiction-sexual-register.md  # Mixed register guide for contemporary literary sex scenes
│   ├── mobi-extraction.md              # MOBI text extraction method
│   ├── output-formats.md               # Deliverable generation scripts (HTML/EPUB/MOBI/PDF)
│   ├── parallel-delegation.md          # Parallel translation for long texts (split→dispatch→merge)
│   ├── playwright-pdf-generation.md    # Playwright HTML→PDF wrapper
│   ├── project-init.md                 # Phase -1 project init detailed steps
│   ├── techniques.md                   # E→C technique inventory (conversion, addition/omission, splitting/merging)
│   ├── text-analysis-and-qa.md         # Text analysis framework + domestication scale + QA standards
│   └── translationese-symptoms.md      # 8-class translationese symptom list with fixes
├── scripts/                       # Workflow helper scripts
│   ├── normalize-punctuation.py        # Phase 6: Chinese fullwidth normalization (mechanical)
│   ├── strip-version-markers.py        # Phase 8A: strip markers + cleanup + translator credit
│   └── bilingual-to-pdf.py             # Bilingual MD → HTML + PDF (on demand)
└── ultra/                         # Methodology components (Ye Zinan 17-skill file mapping & diagram)
    ├── SKILL_MAP.md                   # 17-skill to workflow-phase mapping table (with skip rules)
    └── WORKFLOW.md                    # Translation workflow diagram (Mermaid, with validation chain)
```

---

## Contributing

**Maintainer:** [Lilipuut](https://github.com/3060226349kk-cmd) — project creator, responsible for core workflow design and methodology integration.

Contributions are welcome. The following guidelines explain the project structure and how to participate effectively.

### Setting Up a Development Environment

1. Install [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
2. Clone this repository to `~/.claude/skills/en-zh-max/`

### Contribution Workflow

1. **Open an issue**: Describe the proposed change in [Issues](https://github.com/3060226349kk-cmd/en-zh-max/issues) to avoid conflicting work
2. **Fork + Branch**: Create a feature branch from `main` (e.g. `fix/punctuation-typo`, `feat/new-reference`)
3. **Scope of changes**:
   - `SKILL.md`: phase gate conditions, script paths, methodology references
   - `references/*.md`: additions or corrections to technique inventories and trap lists
   - `scripts/*.py`: feature extensions or bug fixes
   - `ultra/*.md`: skill mapping table or workflow diagram updates
   - `README.md`: update Chinese and English versions simultaneously (precise symmetry)
4. **Commit**: prefix with scope tag (e.g. `[SKILL]`, `[REF]`, `[SCRIPT]`, `[ULTRA]`, `[DOC]`)
5. **PR**: link the issue, describe the change and verification method

### Code Conventions

- SKILL.md: preserve YAML frontmatter (`name`, `description`, `version`, `allowed-tools`); annotate phase gate conditions (entry/exit criteria)
- references/*.md: numbered list entries with source attribution (Ye Zinan page numbers)
- scripts/*.py: Python 3.8+ compatible, zero external dependencies; resolve file paths via `$SKILL_DIR` env var or relative paths
- Cross-platform: scripts must run on Windows (git-bash), macOS, and Linux
- New methodology documents must register their phase mapping in `SKILL_MAP.md`

### Release Process

1. Bump version in `SKILL.md` YAML `version` field + README badge link
2. (Optional) Maintain a CHANGELOG for notable changes per release
3. Merge to `main`—the latest version is then available via `git clone`

---

## Acknowledgements

**Author:** [Lilipuut](https://github.com/3060226349kk-cmd) — overall architecture design, methodology integration, and implementation of en-zh-max.

The skill's base framework derives from [en-zh-translation-polish](https://github.com/HoraceLuBFA/en-zh-translation-polish), an English→Chinese translation polish skill. The original 7-stage workflow was expanded into the full version presented here.

Distillation of the 17 textbook skills was performed via the book2skill pipeline in [cangjie-skill](https://github.com/3060226349kk-cmd/cangjie-skill).

Special thanks to **Prof. Ye Zinan**—his *Advanced English-Chinese Translation Theory and Practice* (Tsinghua University Press, 2020) provides the systematic theoretical foundation for this skill's methodology. The book's seven-dimension text analysis, unpacking method, five-level E-C contrastive analysis, formulaic language "water vs ice" identification, and six-dimension Westernization assessment constitute the scholarly backbone of every phase in this skill.

The validation pipeline's `verification-before-completion` step is powered by [Superpowers](https://github.com/obra/superpowers), `scribe:prose-reviewer` by [scribe](https://github.com/anthrxc/scribe), and `humanizer`/`humanizer-zh` by their respective validation skills. Thanks to each project's open architecture.

---

## License

[MIT](LICENSE) © 2026 Lilipuut

[↑ Back to top](#en-zh-max--english-to-chinese-translation-for-claude-code) · [🇨🇳 中文](#en-zh-max--英译汉翻译-claude-code-skill)

---

## 关键词 / Tags

`english-to-chinese` `英译汉` `英译中` `chinese-translation` `translation` `localization` `nlp` `book2skill` `claude-code` `claude-skill` `ye-zinan` `translation-pipeline` `中英对照` `润色`
