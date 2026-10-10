# en-zh-max 工作流（v4）

```mermaid
flowchart TB
    IN["待译英文"] --> TIER{"工作量"}
    TIER -->|"小：聊天几句"| S["定性 → 理解 → 初译 → 自查<br/>回复里直接给对照"]
    TIER -->|"中：一篇文档"| M0
    TIER -->|"大：整本书"| L0["项目初始化 source/<br/>translation-plan.md + TERMS_GLOSSARY.md"]
    L0 --> M0

    subgraph CH["每篇（大档为每章）"]
        M0["0 定性<br/>软硬 · 纽马克类型 · 自由度 · 语域（脏度）"]
        M1["1 理解<br/>形成图像 · 解包袱 · 套语替换测试"]
        M2["2 初译<br/>意合起笔 · 单位随档位 · 术语表语域标记"]
        M3["3 修订（一轮）<br/>中文侧：翻译腔诊断清单、音韵<br/>原文侧：准确性六项、语域、前景化与反释义"]
        M4["4 终审<br/>humanizer 一次（大档每章）"]
        M5["5 机检与交付<br/>check.py zh --fix → strip-version-markers.py"]
        M0 --> M1 --> M2 --> M3 --> M4 --> M5
    end

    M5 --> OUT["英中对照 md<br/>按需：HTML · EPUB · MOBI · PDF"]
    M5 -->|"大档每章收尾"| HM{"handoff.py meter"}
    HM -->|"→ 继续"| M0
    HM -->|"→ 交接"| HO["落盘 → 写 HANDOFF.md → 停下<br/>新会话：续译 &lt;目录&gt;"]
```

| 步骤 | 依据（references/methods.md） | 准出 |
|---|---|---|
| 0 定性 | 第 1、2、3 法 | 档位、自由度、类型、语域四项已定（大档写进 translation-plan.md） |
| 1 理解 | 第 4、5、6、7、8 法 | 能用中文说出每段的意思 |
| 2 初译 | 第 9、10、11 法 | 全文初稿完成，术语表的语域标记已逐一落实 |
| 3 修订 | 第 12、13、14、15 法 + translationese-symptoms.md | 两张清单都过完一遍 |
| 4 终审 | humanizer | 整章过一次 |
| 5 机检交付 | check.py、strip-version-markers.py | 标点残留为 0，署名和项目地址齐全 |
| 大档收尾 | references/handoff.md、handoff.py | 跑过 meter；报「→ 交接」时已落盘、写好 HANDOFF.md、会话停下 |
