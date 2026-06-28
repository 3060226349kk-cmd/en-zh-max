# en-zh-max Ultra 技能映射表

> 快速查阅：每个 en-zh 阶段对应的 ultra 技能及执行方式。
> 完整设计见 `docs/superpowers/specs/2026-06-25-en-zh-max-design.md`

## 预读取批（P0）—— 阶段 -1 之后执行

一次性 Read 以下文件，建立方法论地基（不 invoke Skill）：

| # | 文件 | Read 路径 |
|---|------|-----------|
| 1 | INDEX | `$SKILL_DIR/../en-zh-ultra/INDEX.md` |
| 2 | BOOK_OVERVIEW | `$SKILL_DIR/../en-zh-ultra/BOOK_OVERVIEW.md` |
| 3 | 翻译基本问题决策框架 | `$SKILL_DIR/../en-zh-ultra/ec-translation-basic-decisions/SKILL.md` |
| 4 | 三大语义类型分析法 | `$SKILL_DIR/../en-zh-ultra/ec-translation-semantic-analysis/SKILL.md` |
| 5 | 翻译思维三阶段法 | `$SKILL_DIR/../en-zh-ultra/ec-translation-image-formation/SKILL.md` |
| 6 | 英汉语言五层次对比分析法 | `$SKILL_DIR/../en-zh-ultra/ec-translation-contrastive-analysis/SKILL.md` |
| 7 | 翻译单位动态选择法 | `$SKILL_DIR/../en-zh-ultra/ec-translation-unit-selection/SKILL.md` |
| 8 | 套语"水vs冰"识别与翻译法 | `$SKILL_DIR/../en-zh-ultra/ec-translation-formula-recognition/SKILL.md` |
| 9 | 前景化翻译处理法 | `$SKILL_DIR/../en-zh-ultra/ec-translation-foregrounding/SKILL.md` |
| 10 | 西化表达六维评估法 | `$SKILL_DIR/../en-zh-ultra/ec-translation-westernization/SKILL.md` |
| 11 | 文本分析七维度与自由度评估法 | `$SKILL_DIR/../en-zh-ultra/ec-translation-pretext-analysis/SKILL.md` |
| 12 | 奈达功能对等三支柱操作法 | `$SKILL_DIR/../en-zh-ultra/ec-translation-nida-functional-equivalence/SKILL.md` |
| 13 | 纽马克文本分类翻译策略法 | `$SKILL_DIR/../en-zh-ultra/ec-translation-newmark-text-typology/SKILL.md` |
| 14 | 认知隐喻发现与翻译法 | `$SKILL_DIR/../en-zh-ultra/ec-translation-cognitive-metaphor/SKILL.md` |
| 15 | 解包袱法 | `$SKILL_DIR/../en-zh-ultra/ec-translation-unpacking/SKILL.md` |
| 16 | 文学翻译反释义法 | `$SKILL_DIR/../en-zh-ultra/ec-translation-literary-anti-paraphrase/SKILL.md` |
| 17 | 翻译准确性六维校验法 | `$SKILL_DIR/../en-zh-ultra/ec-translation-accuracy-checklist/SKILL.md` |

## 阶段级 Invoke

| 阶段 | 技能 | Invoke 参数 | 触发条件 |
|------|------|------------|---------|
| 0 | 文本分析七维度与自由度评估法 | `Skill("en-zh-ultra:ec-translation-pretext-analysis")` | 始终 |
| 0 | 纽马克文本分类翻译策略法 | `Skill("en-zh-ultra:ec-translation-newmark-text-typology")` | 始终 |
| 0 | 翻译基本问题决策框架 | `Skill("en-zh-ultra:ec-translation-basic-decisions")` | 始终 |
| 1 | 解包袱法 | `Skill("en-zh-ultra:ec-translation-unpacking")` | 始终 |
| 2 | 英汉语言五层次对比分析法 | `Skill("en-zh-ultra:ec-translation-contrastive-analysis")` | 始终 |
| 2 | 翻译单位动态选择法 | `Skill("en-zh-ultra:ec-translation-unit-selection")` | 始终 |
| 3 | 套语"水vs冰"识别与翻译法 | `Skill("en-zh-ultra:ec-translation-formula-recognition")` | 始终 |
| 3 | 西化表达六维评估法 | `Skill("en-zh-ultra:ec-translation-westernization")` | 始终 |
| 5 | 翻译准确性六维校验法 | `Skill("en-zh-ultra:ec-translation-accuracy-checklist")` | 始终 |
| 7 | 前景化翻译处理法 | `Skill("en-zh-ultra:ec-translation-foregrounding")` | 软文本（自由度≥4）；硬文本跳过 |
| 7 | 文学翻译反释义法 | `Skill("en-zh-ultra:ec-translation-literary-anti-paraphrase")` | 同上（配对 invoke） |

## 跳过规则速查

| 场景 | 跳过哪些 |
|------|---------|
| 硬文本（自由度 1-3） | 步骤 2.5 双技能 invoke（前景化 + 文学反释义） |
| 聊天小段翻译（不落盘） | 全部 ultra 接入（预读取 + invoke） |
| 用户要求快速出稿 | 全部 ultra 接入 |
| 短篇（< 2,000 词） | P0 预读取仅保留 INDEX + BOOK_OVERVIEW + 5 个核心框架（#3,6,9,11,17） |

## ultra 技能依赖关系速查

```
翻译基本问题决策框架 ← 纽马克文本分类, 奈达三支柱, 文本分析七维度
英汉语言五层次对比 ← 翻译单位动态选择, 前景化翻译处理
解包袱法 ↔ 奈达功能对等三支柱            (composes-with)
套语水vs冰识别 ↔ 西化表达六维评估        (composes-with)
认知隐喻发现 → 文学翻译反释义             (supplements)
文本分析七维度 → 翻译准确性六维校验       (precedes)
前景化翻译处理 ↔ 文学翻译反释义           (composes-with)
三大语义类型分析 ↔ 认知隐喻发现           (composes-with)
```
