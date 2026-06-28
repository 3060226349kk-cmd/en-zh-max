# en-zh-max — 英译汉翻译 Claude Code Skill

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-9cf)](https://docs.anthropic.com/en/docs/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Release](https://img.shields.io/badge/release-v3.1.0-blue)](https://github.com/3060226349kk-cmd/en-zh-max/releases/latest)
[![Version](https://img.shields.io/badge/version-3.1.0)](SKILL.md)

[🇨🇳 中文](#en-zh-max--英译汉翻译-claude-code-skill) · [🇬🇧 English](#en-zh-max-english%E2%86%92chinese-translation-for-claude-code)

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

1. **Fork 本仓库**到您的 GitHub 账户
2. **创建特性分支**：`git checkout -b feature/your-feature`
3. **修改后提交**：
   - 不要修改 `SKILL.md` 的 version 字段（维护者统一管理版本号）
   - 保持 `ultra/SKILL_MAP.md` 中的阶段映射同步
4. **发起 Pull Request** 到 main 分支

### 适合的贡献方向

- **补充 `references/`**：翻译腔症状、技巧库、文本分析指南等文档化
- **改进脚本**：`scripts/` 下的辅助脚本（标点归一、版本标记清理、PDF 生成等）
- **方法论扩展**：`ultra/SKILL_MAP.md` 新增方法论技能的映射
- **Bug 修复**：工作流中的逻辑遗漏、门禁条件缺陷、路径问题
- **测试**：实际翻译测试、边缘案例覆盖

### 不适合的贡献方向

- 改变翻译策略层的核心方法论（叶子南体系是锚定框架）
- 删除语域脏度管线或校验链步骤（这些是必选质量关卡）
- 大幅重写 SKILL.md 的工作流阶段编号体系

---

## 致谢

- **叶子南**《高级英汉翻译理论与实践》（清华大学出版社，2020）——方法论基石
- **obra/superpowers** — 提供 `verification-before-completion` 校验
- **blader/humanizer** — 提供四维验证与 AI 模式检测
- **Claude Code** — 运行本 skill 的宿主平台

本 skill 的开发建立在以上开源社区与学术成果的基础之上。

---

## 许可

[MIT](LICENSE) © 2026 Lilipuut
