# en-zh-translation-polish skill

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main workflow: 7-stage translation pipeline (analysis → deverbalization → draft → polish → rhythm check → accuracy QA → punctuation normalize → output) |
| `references/libertine-vocabulary.md` | 直白性/身体词汇硬词映射表（鸡巴/屄/屁眼/操等） |
| `references/techniques.md` | 英译汉技巧库（词性转换、增/减词、分句/合句等） |
| `references/translationese-symptoms.md` | 翻译腔病症对照表及归化/异化取舍 |
| `references/text-analysis-and-qa.md` | 纽马克文本分类、隐喻决策法则、准确性质检标准 |
| `references/mobi-extraction.md` | 从 `.mobi` 提取纯文本（Python mobi 模块） |
| `references/epub-extraction.md` | 从 `.epub` 提取纯文本（Python zipfile / Pandoc / Calibre） |
| `references/parallel-delegation.md` | 超长文本并行翻译（含连续文本分割策略 → 分批派发 → 集成合并） |
| `references/playwright-pdf-generation.md` | Playwright HTML→PDF 封装方案 |
| `references/bilingual-html-template.md` | 双语 Markdown 解析器模式 + CEU Navy CSS 模板 |
| `scripts/normalize-punctuation.py` | 中文标点全角归一化脚本（Windows 适配） |
| `scripts/bilingual-to-pdf.py` | 英中对照 Markdown → CEU Academic Navy HTML + PDF 一键脚本（Playwright） |
