# en-zh-max 翻译工作流流程图

> 完整管线：从输入到交付，含校验链 ★ 不可跳过

```mermaid
flowchart TB
    subgraph INPUT["📥 输入"]
        A1["用户提供待译内容"]
    end

    subgraph PREP["⚙️ 预备阶段"]
        B1["阶段 -1<br/>项目目录初始化<br/>source/ 目录 + 归位验证"]
        B2["阶段 -0.5<br/>Ultra 预读取批<br/>17 个方法论 SKILL.md"]
        B1 --> B2
    end

    subgraph CORE["🔄 核心翻译管线（阶段 0→6）"]
        C0["阶段 0<br/>文本分析<br/>定归化档位 + text-profile"]
        C1["阶段 1<br/>理解与脱壳<br/>解包袱法"]
        C2["阶段 2<br/>初译<br/>英汉五层次对比 + 翻译单位选择"]
        C2_5["阶段 2.5<br/>语域对齐<br/>脏度≥3 强制逐段核验"]
        C3["阶段 3<br/>润色诊断<br/>翻译腔清除 + 套语识别 + 西化评估"]
        C4["阶段 4<br/>音韵打磨<br/>节奏/停顿/四字结构"]
        C5["阶段 5<br/>质检<br/>12 项自检 + 六维校验"]
        C6["阶段 6<br/>标点规范化<br/>normalize-punctuation.py"]
        
        C0 --> C1 --> C2 --> C2_5 --> C3 --> C4 --> C5 --> C6
    end

    subgraph VERIFY["🔍 校验链 ★ 不可跳过"]
        V0["步骤 0<br/>整书一致性预检<br/>（混合模式专属）"]
        V1["scribe:prose-reviewer<br/>AI腔/翻译腔/语感漂移"]
        V2["verification-before-completion<br/>交付物完整性 + 英中对齐验证"]
        V2_5["步骤 2.5<br/>前景化 + 反释义评估<br/>（软文本专属）"]
        V3["humanizer<br/>四维验证 + 对抗自审"]
        V4["humanizer-zh<br/>中文 AI 痕迹终审（24 模）"]
        
        V0 --> V1 --> V2 --> V2_5 --> V3 --> V4
    end

    subgraph OUTPUT["📦 交付"]
        D1["阶段 8<br/>交付物生成"]
        D2["英中对照.md"]
        D3["英中对照.html"]
        D4["全中文.md（按需）"]
        D5["EPUB + MOBI + PDF（全文翻译）"]
        
        D1 --> D2
        D1 --> D3
        D1 --> D4
        D1 --> D5
    end

    subgraph PARALLEL["⚡ 超长文本并行模式（≥7章）"]
        P1["阶段 B1<br/>基线章串行翻译<br/>前 1-2 章建立风格基线"]
        P2["阶段 B2<br/>批量章并行翻译<br/>剩余章注入风格基线"]
        P3["阶段 B3<br/>合并 + 整书校验链 ★"]
        
        P1 --> P2 --> P3
    end

    INPUT --> PREP
    PREP --> CORE
    CORE --> VERIFY
    VERIFY --> OUTPUT
    CORE -.->|超长文本| PARALLEL
    PARALLEL -.->|校验链通过| OUTPUT
```

## 阶段说明

| 阶段 | 名称 | 核心产出 | 准出条件 |
|------|------|---------|---------|
| **-2** | 预扫描与策略决定 | `translation-plan.md` | 总章数 + 词数统计，模式判定 |
| **-1** | 项目初始化 | `source/` 目录 + 归位验证 | 原始文件移入，提取产物生成 |
| **-0.5** | Ultra 预读取 ★ | 17 个方法论文件已读 | INDEX + 16 skill 全部 Read 完成 |
| **0** | 文本分析 | text-profile 写入头部 | 档位/自由度/文本类型/语域 四项非占位符 |
| **1** | 理解与脱壳 | 脱壳摘要注释 | 3-5 句中文概括，不含英文词 |
| **2** | 初译 | 英中对照初稿 | 每段标记 `[v1]` |
| **2.5** | 语域对齐 | 语域偏差修正 | 每段标注 R 状态（脏度≥3 时强制） |
| **3** | 润色诊断 | 翻译腔消除稿 | 每段标 `[v2·操作类型]` |
| **4** | 音韵打磨 | 节奏优化稿 | 每段标 `[v3]` |
| **5** | 质检 | 自检通过稿 | 每段标 `[v3·Q✓]` |
| **6** | 标点规范 | 标点标准化 | `normalize-punctuation.py` 残留 = 0 |
| **7** | 校验链 ★ | 四道审查全部通过 | see below ↓ |
| **8** | 交付 | .md + .html + 按需格式 | 五项清理验证全部通过 |

## 校验链详解 ★

```
阶段 6 通过
    ↓
步骤 0：整书一致性预检（混合模式）
    └── 术语一致性扫描 + 语感漂移检测 + 衔接质量抽查
    └── 纯串行模式跳过
    ↓
① scribe:prose-reviewer
    └── 整书级 AI 腔/翻译腔/语感漂移审查
    └── 未通过 → 标记问题段落，退回阶段 3
    ↓
② verification-before-completion
    └── 交付物完整性检查
    └── 英中对齐验证（每段英文有对应中文）
    └── 未通过 → 补全缺失部分
    ↓
步骤 2.5：前景化 + 反释义评估
    └── 软文本（自由度≥4）专属
    └── 硬文本跳过此步
    ↓
③ humanizer
    └── 四维验证：Fidelity / Naturalness / Grammar / AI Patterns
    └── 强制对抗自审，原位修复
    └── 混合模式分层执行（Tier 1-3）
    ↓
④ humanizer-zh
    └── 24 条中文 AI 痕迹规则（四大类 × 6）
    └── 仅扫中文译文，不动英文 blockquote
    ↓
阶段 8 — 交付物生成
```

## 方法论引用

本 skill 方法论基于叶子南《高级英汉翻译理论与实践》（清华大学出版社，2020），经 book2skill 蒸馏为 17 个 ultra 技能。详见 [`ultra/SKILL_MAP.md`](SKILL_MAP.md)。
