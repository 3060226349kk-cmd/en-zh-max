# en-zh-max — English-to-Chinese Translation Claude Code Skill

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-9cf)](https://docs.anthropic.com/en/docs/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Release](https://img.shields.io/badge/release-v3.1.0-blue)](https://github.com/3060226349kk-cmd/en-zh-max/releases/latest)
[![Version](https://img.shields.io/badge/version-3.1.0)](SKILL.md)

[🇨🇳 中文](#en-zh-max--英译汉翻译-claude-code-skill) · [🇬🇧 English](#en-zh-max-english%E2%86%92chinese-translation-for-claude-code)

> English $\rightarrow$ Chinese translation and polishing. A 9-stage workflow + 17 distilled skills from Ye Zinan's *Advanced English-Chinese Translation Theory and Practice* + a 4-layer verification chain + a register "dirtiness" pipeline.
> Specifically designed for Claude Code, producing bilingual English-Chinese parallel translations.
>
> 📊 [Full Workflow Diagram (including Verification Chain)](ultra/WORKFLOW.md)

---

## Table of Contents

- [What is this?](#what-is-this)
- [Methodological Foundation](#methodological-foundation)
- [Workflow Pipeline](#workflow-pipeline)
- [Verification Chain](#verification-chain)
- [Quick Installation](#quick-installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Contribution Guide](#contribution-guide)
- [Acknowledgements](#acknowledgements)
- [License](#license)

---

## What is this?

**en-zh-max** is a translation skill for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) that translates English into idiomatic Chinese and produces bilingual parallel texts. It integrates **17 translation skills** distilled via the `book2skill` process from Ye Zinan's *Advanced English-Chinese Translation Theory and Practice* (Tsinghua University Press, 2020).

### Three Core Differences in English-to-Chinese Translation

English-to-Chinese translation faces three fundamental challenges, which form the basis of en-zh-max's design:

1. **Hypotaxis vs. Parataxis** — English relies on conjunctions, relative pronouns, and prepositions to make logical relationships explicit (hypotaxis), while Chinese relies on word order, context, and parallelism to imply relationships (parataxis). The biggest mistake in translation is mechanically mapping `because`, `although`, `which`, and `that` to 「因为」, 「虽然」, 「它/其」, and 「的」—resulting in bloated sentences plagued by repetitive particles.

2. **The Dilemma of Nominalized Abstract Subjects** — English prefers abstract nouns as subjects (`The confidence that...`, `The realization of...`), whereas Chinese prefers concrete people or objects as subjects. Literal translation of abstract subjects makes the text feel floating and inhuman.

3. **The Pressure of Long Attributive Clauses** — English attributive clauses can expand infinitely to the right (`the man who... which... that...`), but Chinese modifiers must be placed before the noun and have limited capacity. The core strategy is to break these into sequential short sentences or convert them into adverbial clauses.

---

## Methodological Foundation

The methodological root of this skill is Ye Zinan's *Advanced English-Chinese Translation Theory and Practice* (Tsinghua University Press, 2020), distilled via the `book2skill` pipeline into 17 executable skills. The core theoretical framework is as follows:

### Five Governing Principles

> **"Analyze text before translating"** — Seven-dimensional diagnosis + degree-of-freedom scoring; locate before you write (Chapter 15).
>
> **"Depend on the target language"** — The general direction is to stay close to the reader and leverage the strengths of Chinese (Chapter 1).
>
> **"Flexibility as a core competency"** — Break free from the constraints of the source language structure (Nida's theory, Chapter 11).
>
> **"Protect the purity of Chinese"** — Beware the spread of "Westernized Chinese"; the translator bears the mission of keeping the native language pure (Chapter 9).
>
> **"Avoid paraphrasing in literary translation"** — In literary translation, preserving the original linguistic form takes priority over paraphrasing content (Chapter 14).

### 17 Distilled Skills Coverage

Four methodology groups:

| Group | Skills | Application Stage |
|------|------|---------|
| **Text Analysis & Strategy** (4 skills) | 7D Text Analysis & Freedom Assessment, Newmark Text Classification Strategy, Basic Translation Problem Decision Framework, Nida's Three Pillars of Functional Equivalence | Pre-reading + Stage 0 |
| **Understanding & Conversion** (5 skills) | Three Semantic Type Analysis, Three Stages of Translation Thinking, "Unpacking" Method, 5-Level English-Chinese Comparative Analysis, Dynamic Selection of Translation Units | Stages 0-2 |
| **Polishing & Quality** (5 skills) | "Water vs. Ice" Cliché Identification, 6D Westernized Expression Assessment, Cognitive Metaphor Discovery, 6D Accuracy Verification, Literary Anti-Paraphrasing | Stages 3-7 |
| **Style & Rhetoric** (3 skills) | Foregrounding Processing, Literary Anti-Paraphrasing Method, Three-Stage Translation Thinking | Stage 7 (Soft Text) |

See [`ultra/SKILL_MAP.md`](ultra/SKILL_MAP.md) for the precise mapping between each skill and the workflow stages.

---

## Workflow Pipeline

The en-zh-max workflow consists of **9 stages**, 6 of which introduce specific skills from the Ye Zinan methodology. An overview of each stage is provided below (see [SKILL.md](SKILL.md) for specific gate conditions and script paths).

### Preparatory Stages

| Stage | Name | Responsibility |
|------|------|------|
| **-2** | Pre-scan | Word count statistics, produce `translation-plan.md` (Single-agent serial execution, no sub-agents) |
| **-1** | Project Init | Create `source/` directory, organize files, extract formats |
| **-0.5** | Methodology Pre-read | One-time reading of 17 methodology SKILL.mds to establish the methodological foundation |

### Core Translation Pipeline (Stages 0 $\rightarrow$ 6)

| Stage | Name | Responsibility |
|------|------|------|
| **0** | Text Analysis | Determine domestication level (Hard/Medium/Soft), text-profile (including **Register Dirtiness 1-5**), 7D diagnosis + freedom score |
| **1** | Understanding & Unshelling | Strip English linguistic shell, apply "unpacking" method, convert core sentences |
| **2** | First Draft | Prioritize parataxis, break long sentences, convert hypotaxis $\rightarrow$ parataxis; apply 5-level comparison + translation unit selection |
| **2.5** | Register Alignment ★ | Forced paragraph-by-paragraph register equivalence check when dirtiness $\ge 3$; correct register deviations |
| **3** | Polishing Diagnosis | Remove "translationese" (8 symptoms), identify clichés, perform 6D westernization assessment |
| **4** | Phonetic Refinement | Read-aloud calibration, disyllabic/four-character structures, rhythm reorganization (relaxed for soft text, minimal for hard text) |
| **5** | Quality Assurance | **16 self-check items** (12 general + 4 register-specific), cross-reference with source; apply 6D accuracy verification |
| **6** | Punctuation Normalization | Mechanically execute `normalize-punctuation.py`, ensuring zero remaining half-width Chinese punctuation |

### Delivery (Stage 8)

| Step | Responsibility |
|------|------|
| **8A** | Final Cleanup: Strip version markers, delete text-profile, add translator attribution (`strip-version-markers.py`), clean AI process residue |
| **8B** | Derived Deliverables: Bilingual MD/HTML/EPUB/MOBI/PDF (as needed) |

---

## Verification Chain

After the translation text is written to disk and before deliverables are generated, it must pass the following **4-step verification**. If a problem is found at any step $\rightarrow$ return to the corresponding stage for repair $\rightarrow$ re-run the verification chain. **No step may be skipped.**

```
Stage 6 (Punctuation Normalization)
       ↓
① scribe:prose-reviewer       — AI-speak / Translationese / Tone drift
       ↓
② verification-before-completion — Deliverable integrity + Bilingual alignment
       ↓
③ humanizer                   — 4D Verification (Fidelity / Naturalness / Grammar / AI Patterns)
                                 + Forced Adversarial Self-Review
       ↓
④ humanizer-zh                — Final Chinese AI Trace Review (24 rules)
       ↓
Stage 8 (Delivery)
```

### Step 1: scribe:prose-reviewer

Reviews the Chinese translation for AI writing style, remaining translationese, forbidden phrases, tone drift, and monotonous structure. **Reference only** — final discretion over suggested changes lies with the humanizer (Step 3).

### Step 2: verification-before-completion

Complete deliverable integrity check: Are MD/HTML files complete? Is punctuation residue zero? Is bilingual alignment intact? Is the source file in `source/`? Confirm state (e.g., "humanizer not yet executed").

For soft text (Freedom $\ge 4$), rhetoric skills (Foregrounding + Anti-paraphrasing) are inserted after this step.

### Step 3: humanizer

Cuts the Chinese translation into chunks (3-5 paragraphs each) and performs 4D verification on each chunk:

- **Fidelity** (Sentence-by-sentence comparison with source for semantic equivalence/negation/modality/proper nouns)
- **Naturalness** (Translationese/Tone/Register)
- **Grammar** (Typos/Collocation/Punctuation/Consistency)
- **AI Patterns** (29 common AI patterns)

After passing, it performs **Forced Adversarial Self-Review** — reviewing all passed chunks sentence-by-sentence again to prevent systematic blind spots.

The humanizer has **final discretion** over `prose-reviewer` suggestions: approve, reject, or identify missed issues.

### Step 4: humanizer-zh

Processes only the Chinese translation lines (filtering out English blockquotes) and runs each chunk through **24 Chinese AI Trace Rules** (4 categories $\times$ 6 rules: content patterns / grammar / style patterns / filler phrases). Detects and fixes high-frequency AI vocabulary, dash abuse, ternary parallelism, negative parallelism, avoidance of copulas, fake scope, filler phrases, and generic positive conclusions.

**Boundary of Responsibility**: `humanizer` is responsible for "translating correctly" (Fidelity + Naturalness + Grammar), while `humanizer-zh` is responsible for "making it sound human" (Chinese AI trace removal).

### Automatic Correction Rules

Any errors or issues found during the four steps of the verification chain are **automatically corrected** and written directly to the bilingual MD file without waiting for single-item approval. The corrected MD is the sole input source for Stage 8's derived HTML/EPUB/MOBI files.

---

## Quick Installation

### Method 1: Clone to Claude Code skills directory (Recommended)

```bash
cd ~/.claude/skills/
git clone https://github.com/3060226349kk-cmd/en-zh-max.git en-zh-max
```

Once cloned, the `references/`, `scripts/`, and `ultra/` subdirectories are automatically in place, and workflow script paths are self-consistent.

### Method 2: Manual Copy

Copy the following contents from the repository into `~/.claude/skills/en-zh-max/`:

```
SKILL.md
references/
scripts/
ultra/
```

**Note**: Workflow scripts (`normalize-punctuation.py`, `strip-version-markers.py`) and `ultra/` methodology files are referenced via relative paths. Manual copying must maintain the directory structure, otherwise, Stage 6 (Punctuation Normalization) and Stage 8A (Final Cleanup) scripts will fail.

### Environment Requirements

| Dependency | Version | Purpose | Required/Optional |
|------------|---------|---------|------------------|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | Latest recommended | Host CLI for this skill | **Required** |
| Python | 3.8+ | Run auxiliary scripts in `scripts/` | **Required** |
| Git | — | Clone repo, version management | **Required** |
| pip: `playwright` | Latest | HTML $\rightarrow$ PDF rendering (`bilingual-to-pdf.py`) | Optional ① |
| pip: `ebooklib` | Latest | EPUB generation (`output-formats.md` scripts) | Optional ① |
| pip: `PyMuPDF` (`fitz`) | Latest | PDF text extraction (`project-init.md` scripts) | Optional ② |
| [Pandoc](https://pandoc.org) | Latest | Text format conversion (Intermediate for EPUB/MOBI/PDF) | Optional ① |
| [Kindle Previewer 3](https://www.amazon.com/gp/feature.html?docId=1000765261) (inc. `kindlegen`) | 3.x | EPUB $\rightarrow$ MOBI conversion | Optional ① |
| [Calibre](https://calibre-ebook.com) (`ebook-convert`) | Latest | AZW3/MOBI format conversion | Optional ① |
| [marker-pdf](https://github.com/VikParuchuri/marker) (`marker`) | Latest | Scanned PDF OCR $\rightarrow$ Text | Optional ② |

> **①** Install only if the specific output format is required (Bilingual MD is the source for all formats and requires no extra tools).
> **②** Install only if the source text is a scanned PDF or special format. Not needed for plain text or EPUB.

Script dependency configuration:

```bash
# Playwright (PDF Rendering) — Install once
pip install playwright && python3 -m playwright install chromium

# Kindlegen (MOBI Generation) — Install via Kindle Previewer 3, verify PATH or script path
# Modify the KINDLEGEN variable in references/output-formats.md to point to your installation path
```

### Required Skill Dependencies

The verification chain and methodology of this skill depend on the following Claude Code skills:

| Skill | Official Source | Purpose | Installation Method |
|-------|---------|------|---------|
| [superpowers](https://github.com/obra/superpowers) | `obra/superpowers` | Verification step: `verification-before-completion` | `cd ~/.claude/skills/ && git clone https://github.com/obra/superpowers.git` |
| scribe | [Claude Code Built-in](https://docs.anthropic.com/en/docs/claude-code/plugins) | Verification step: `scribe:prose-reviewer` (AI/Translationese review) | Built into Claude Code, no installation needed |
| [humanizer](https://github.com/blader/humanizer) | `blader/humanizer` | Verification step: 4D Verification + Forced Adversarial Review | `cd ~/.claude/skills/ && wget -O SKILL.md https://raw.githubusercontent.com/blader/humanizer/main/SKILL.md` |
| humanizer-zh | Derived from `blader/humanizer` (CN adapter) | Verification step: Final Chinese AI Trace Review (24 rules) | Same as `humanizer`, rules translated for Chinese |

> The en-zh-max workflow itself can run basic translation (Stages 0-6) without the above skills, but the verification chain (Stage 7) and methodology enhancement stages (Stages -0.5/0/1/2/3/5) require the corresponding skills to be present.
>
> Installation commands should all be executed via `git clone` within the Claude Code skills directory, consistent with the installation of en-zh-max.

---

## Quick Start

Request a translation in Claude Code:

```
Translate to Chinese:
(Your English text)
```

Or translate from a file:

```
Translate this file into Chinese
```

Claude Code will automatically trigger the en-zh-max skill and execute the full workflow pipeline. Upon first use, the Methodology Pre-read (Stage -0.5) will be loaded automatically to establish the methodological foundation.

---

## Project Structure

```
en-zh-max/
├── SKILL.md                       # Runtime instructions: Workflow, Gates, Script paths
├── README.md                      # This file
├── LICENSE                        # MIT
├── .gitignore
├── references/                    # Methodology docs (tips, pitfall lists, analysis frameworks)
│   ├── bilingual-html-template.md      # Bilingual HTML template (CEU Navy CSS)
│   ├── epub-extraction.md              # EPUB text extraction method
│   ├── libertine-vocabulary.md          # Register-equivalent vocabulary for explicit sexual/body content
│   ├── literary-fiction-sexual-register.md  # Mixed register guide for contemporary literary descriptions
│   ├── mobi-extraction.md              # MOBI text extraction method
│   ├── output-formats.md               # Scripts for derived deliverables (HTML/EPUB/MOBI/PDF)
│   ├── playwright-pdf-generation.md    # Playwright HTML→PDF wrapper solution
│   ├── project-init.md                 # Stage -1 detailed project directory initialization steps
│   ├── techniques.md                   # English-to-Chinese technique library (POS conversion, addition/deletion, etc.)
│   ├── text-analysis-and-qa.md         # Text analysis framework + Domestication scale + QA standards
│   └── translationese-symptoms.md      # 8 categories of translationese symptoms and fixes
├── scripts/                       # Workflow auxiliary scripts
│   ├── normalize-punctuation.py        # Stage 6: Full-width Chinese punctuation normalization
│   ├── strip-version-markers.py        # Stage 8A: Remove version markers + cleanup + translator attribution
│   └── bilingual-to-pdf.py             # Bilingual MD → HTML + PDF (as needed)
└── ultra/                         # Methodology components (Ye Zinan 17 skills mapping & flowcharts)
    ├── SKILL_MAP.md                   # Mapping of 17 skills to workflow stages (incl. skip rules)
    └── WORKFLOW.md                    # Translation workflow flowchart (Mermaid, incl. verification chain)
```

---

## Contribution Guide

**Maintainer:** [Lilipuut](https://github.com/3060226349kk-cmd) — Project creator, responsible for core workflow design and methodology integration.

Contributions to this skill are welcome. The following guidelines will help you understand the project structure and participate effectively.

### Development Environment Setup

1. Install [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
2. Clone this repository to `~/.claude/skills/en-zh-max/`

### Contribution Process

1. **Fork this repository** to your GitHub account
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Submit changes**:
   - Do not modify the `version` field in `SKILL.md` (Version numbers are managed by the maintainer)
   - Keep the stage mapping in `ultra/SKILL_MAP.md` synchronized
4. **Open a Pull Request** to the main branch

### Recommended Contribution Areas

- **Supplement `references/`**: Documenting more translationese symptoms, technique libraries, and text analysis guides.
- **Improve scripts**: Enhancing auxiliary scripts in `scripts/` (punctuation normalization, version cleaning, PDF generation, etc.).
- **Methodology expansion**: Adding mappings for new methodological skills in `ultra/SKILL_MAP.md`.
- **Bug fixes**: Fixing logic gaps in the workflow, gate condition flaws, or path issues.
- **Testing**: Real-world translation tests and edge-case coverage.

### Non-recommended Contribution Areas

- Changing the core methodology of the translation strategy layer (The Ye Zinan system is the anchoring framework).
- Removing the register dirtiness pipeline or verification chain steps (These are mandatory quality gates).
- Substantially rewriting the stage numbering system of the workflow in `SKILL.md`.

---

## Acknowledgements

- **[HoraceLuBFA/en-zh-translation-polish](https://github.com/HoraceLuBFA/en-zh-translation-polish)** — The original foundation of this skill, providing the initial basic architecture and reference framework.
- **Ye Zinan**, *Advanced English-Chinese Translation Theory and Practice* (Tsinghua University Press, 2020) — Methodological foundation.
- **obra/superpowers** — Provided `verification-before-completion` verification.
- **blader/humanizer** — Provided 4D verification and AI pattern detection.
- **Claude Code** — The host platform running this skill.

The development of this skill is built upon the foundations of the aforementioned open-source community and academic achievements.

---

## License

[MIT](LICENSE) © 2026 Lilipuut

---

## Keywords / Tags

`english-to-chinese` `chinese-translation` `translation` `localization` `nlp` `book2skill` `claude-code` `claude-skill` `ye-zinan` `translation-pipeline` `bilingual` `polishing`
