# en-zh-max — 英译汉翻译 Skill

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-9cf)](https://docs.anthropic.com/en/docs/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Release](https://img.shields.io/badge/release-v4.0.0-blue)](https://github.com/3060226349kk-cmd/en-zh-max/releases/latest)

[中文](#这是什么) · [English](#english)

> 英文→中文翻译与润色，输出英中对照译文。方法论基于叶子南《高级英汉翻译理论与实践》，按工作量分三档，附机检脚本。
> 📊 [工作流图](references/workflow.md)

## 这是什么

en-zh-max 是一个翻译 skill，Claude Code、DeepSeek Harness 等支持 Agent Skills 的工具都能用。它把英文译成地道中文，产出英中对照译文。
- 方法论来自叶子南《高级英汉翻译理论与实践》（第 4 版，清华大学出版社，2020）。
- 书中 15 个方法经 book2skill 蒸馏，压缩成一页一法的速查表 `references/methods.md`。

英译汉有三处根本差异，本 skill 的设计围绕它们展开：
1. 英语形合，汉语意合。
2. 英语常用名词化的抽象主语，汉语偏爱具体主语。
3. 英语长定语从句向右扩展，汉语定语前置、容量有限。

## v4 的变化
| | v3 | v4 |
|---|---|---|
| 动笔前必读 | 17 个文件，约 2 万汉字 | 小档不读；中档、大档读一页速查表和翻译腔清单 |
| 每段改写 | v1 → v2 → v3 三轮，并逐段打版本标记 | 初译 → 对照两张清单修订一轮 |
| 校验链 | 4 个 skill 全量过，不可跳过 | 大档每章过一次 humanizer，其余可选 |
| 机检 | 只查标点 | 新增 `check.py`：标点残留，以及「的」字链、被动、万能动词、介词腔、代词密度、超长分句等信号（附每千字密度） |
| 自包含 | 依赖仓库外的 en-zh-ultra 目录（未随仓库发布） | 速查表随仓库提供，不再依赖外部目录 |
| 交付清理 | 只认 Windows 路径 | 也清理 macOS、Linux 路径；署名里的项目地址自动补齐 |

## 工作流
| 档 | 场景 | 流程 |
|---|---|---|
| 小 | 聊天里几句、一段 | 定性 → 理解 → 初译 → 自查，在回复里给对照 |
| 中 | 一篇文档 | 定性 → 理解 → 初译 → 修订 → 机检 → 交付 |
| 大 | 整本书 | 项目初始化，然后逐章走中档流程，每章加一次 humanizer 终审；全书合订后派生 HTML、EPUB、MOBI |

- **定性**：判断软硬、纽马克类型、自由度（1–10）、语域，原文有粗话或性描写时再定语域脏度（1–5）。
- **修订**：对着中文查翻译腔诊断清单，对着原文查准确性六项（重心、遗漏、结构意义、过度详解、逻辑、语域）。软文本再查前景化和反释义。
- 详见 [SKILL.md](SKILL.md)。

## 安装
```bash
cd ~/.claude/skills/        # 或你的 agent 的 skills 目录
git clone https://github.com/3060226349kk-cmd/en-zh-max.git en-zh-max
```

**依赖**：
- Python 3.8+，运行 `scripts/`。
- 可选：`playwright`（PDF）、`ebooklib`（EPUB）、Calibre `ebook-convert`（AZW3、MOBI）、Pandoc。只在需要对应格式时安装。
- 可选 skill：[humanizer](https://github.com/blader/humanizer)，大档终审时用；没装也能完成翻译。

## 使用
```
英译中：
（英文原文）
```
也可以说「把这个文件翻译成中文」。

## 项目结构
```
en-zh-max/
├── SKILL.md                 # 运行时指令：三档工作量、流程、格式、文件路由
├── references/              # 15 法速查 methods.md、工作流图 workflow.md、翻译腔症状、技巧库、文本分析与质检、语域词表、提取与输出
└── scripts/
    ├── check.py                    # 机检：标点残留 + 翻译腔信号（--fix 修标点）
    ├── normalize-punctuation.py    # 兼容入口，调用 check.py 修标点
    ├── strip-version-markers.py    # 交付清理 + 译者署名 + 项目地址
    └── bilingual-to-pdf.py         # 英中对照 MD → HTML + PDF
```

## 贡献
欢迎提 Issue 和 PR，适合的方向有：补充翻译腔症状和技巧、改进脚本、修 bug、加测试用例。叶子南体系是锚定框架，请不要改动核心方法论。

## 致谢
- [HoraceLuBFA/en-zh-translation-polish](https://github.com/HoraceLuBFA/en-zh-translation-polish)：最初的架构基础。
- 叶子南《高级英汉翻译理论与实践》：方法论基石。
- [blader/humanizer](https://github.com/blader/humanizer)：终审用的四维验证。

## 许可
[MIT](LICENSE) © 2026 Lilipuut

## English
en-zh-max is an English→Chinese translation skill for agents that support Agent Skills (Claude Code, DeepSeek Harness and others). It produces paragraph-aligned bilingual Markdown, with the English source in blockquotes and the Chinese translation below.

- **Method**: Ye Zinan's *Advanced English-Chinese Translation: Theory and Practice* (4th ed., 2020). Fifteen methods are distilled into a one-page-per-method cheat sheet, `references/methods.md`.
- **Tiers**: work is sized in three tiers (snippet, document, book).
  - Every tier: profile the text, understand, then draft.
  - Document and book: revise once against two checklists, one for translationese and one for six-point accuracy, then run `scripts/check.py zh --fix`, which fixes punctuation and reports translationese signals.
  - Book: also one `humanizer` pass per chapter.

Install by cloning this repo into your skills folder. MIT licensed.
