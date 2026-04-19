# interview-notes

Interview-notes skill repository and runnable local pipeline.

访谈纪要 skill 仓库，包含可运行的本地脚本。

## Overview / 简介

- `interview-notes/`
  - EN: Generate faithful interview notes from transcripts and/or recordings, with template matching, selective audio verification, online proper-name checks, and dual outputs: a clean file plus a traceability file.
  - 中文：基于转写和/或录音生成高保真的访谈纪要，支持模板对齐、模糊片段音频补核、专有名词联网核验，以及双文件输出：最终稿 + 对照文件。

## Quick Start / 快速开始

### English

Run the local pipeline with a transcript:

```powershell
python interview-notes/scripts/run_interview_notes.py `
  --transcript examples/sample_transcript.txt `
  --outdir output
```

Common options:

- `--audio path/to/file.wav`
- `--template path/to/template.docx`
- `--output-language zh|en|auto`
- `--provider auto|openai|anthropic|none`
- `--network-mode auto|online|offline`

Behavior:

- If `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` is configured, the script uses an LLM to produce more structured notes.
- Without an LLM provider, it falls back to a conservative local formatter that stays source-grounded.
- Online proper-name verification currently auto-verifies `ClinicalTrials.gov` trial IDs and preserves other names as `unverified` unless a future adapter is added.

### 中文

使用 transcript 运行本地脚本：

```powershell
python interview-notes/scripts/run_interview_notes.py `
  --transcript examples/sample_transcript.txt `
  --outdir output
```

常用参数：

- `--audio path/to/file.wav`
- `--template path/to/template.docx`
- `--output-language zh|en|auto`
- `--provider auto|openai|anthropic|none`
- `--network-mode auto|online|offline`

运行行为：

- 如果配置了 `OPENAI_API_KEY` 或 `ANTHROPIC_API_KEY`，脚本会调用 LLM 生成更结构化的纪要。
- 如果没有 LLM provider，脚本会回退到保守的本地格式化流程，但仍然保持内容可追溯。
- 联网专有名词核验目前对 `ClinicalTrials.gov` 的 `NCT` 试验号支持自动核验；其他名称会先保留并标记为 `unverified`，后续可继续扩展适配器。

## Similar Skills Landscape / 类似 Skill 对比

The table below summarizes publicly available skills or skill collections that overlap with this repository.

下表总结了目前公开可见、与本仓库方向相近的 skill 或 skill 集合。

| Skill / 项目 | What it does / 功能 | Closest overlap / 最接近点 | Main gap vs this repo / 与本仓库的主要差异 | Source / 来源 |
| --- | --- | --- | --- | --- |
| `meeting-minutes-taker` in `daymade/claude-code-skills` | Turns raw meeting transcripts into structured, evidence-based minutes. / 将原始会议转写整理成结构化、基于证据的会议纪要。 | High-fidelity transcript-to-notes workflow. / 高保真 transcript 到纪要的流程。 | Meeting-oriented, not interview-specific; no built-in template cloning plus `clear/traceability` DOCX pair described here. / 偏会议纪要，不是访谈纪要；未体现模板严格复刻和 `clear/traceability` 双 DOCX 输出。 | [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills/blob/main/README.zh-CN.md) |
| `transcript-fixer` in `daymade/claude-code-skills` | Fixes ASR/STT transcript errors for meetings, lectures, and interviews. / 修正会议、讲座、访谈中的 ASR/STT 转写错误。 | Transcript cleanup before note generation. / 在生成纪要前清洗 transcript。 | Focused on transcript correction, not end-to-end interview-note generation or evidence mapping. / 重点是转写纠错，不是端到端访谈纪要和出处映射。 | [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills/blob/main/README.zh-CN.md) |
| `meeting-notes-and-actions` in `ComposioHQ/awesome-codex-skills` | Turns meeting transcripts into summaries, decisions, and owner-tagged action items. / 将会议转写变成摘要、决策和带负责人的行动项。 | Structured transcript post-processing. / 结构化处理 transcript。 | Action-item oriented; does not target interview-note template fidelity or dual audit outputs. / 更偏行动项，不是访谈纪要模板复刻或双审计输出。 | [ComposioHQ/awesome-codex-skills](https://github.com/ComposioHQ/awesome-codex-skills/blob/master/README.md) |
| `meeting-insights-analyzer` in `ComposioHQ/awesome-codex-skills` | Analyzes meeting transcripts for themes, risks, and follow-ups. / 分析会议转写中的主题、风险和后续事项。 | Theme extraction from transcripts. / 从 transcript 中提炼主题。 | Analytics-oriented rather than faithful note drafting with per-point traceability. / 更偏分析，不是逐点可追溯的忠实纪要生成。 | [ComposioHQ/awesome-codex-skills](https://github.com/ComposioHQ/awesome-codex-skills/blob/master/README.md) |
| `meeting-summarizer` in `VoltAgent/awesome-openclaw-skills` | Transforms raw meeting transcripts into structured actionable summaries. / 将原始会议转写变成结构化、可执行摘要。 | Summarization of transcript content. / transcript 内容摘要。 | Summary-first workflow; does not describe template import, selective audio verification, or traceability DOCX output. / 偏摘要，不强调模板导入、选择性音频补核或 traceability DOCX。 | [VoltAgent/awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills/blob/main/categories/ai-and-llms.md) |
| `interview-synthesis` in `product-on-purpose/pm-skills` | Synthesizes user research interviews into actionable product insights. / 将用户访谈整理成可执行的产品洞察。 | Interview-focused processing. / 面向访谈内容处理。 | Research-synthesis oriented, not document-grade interview notes with formatting fidelity and source mapping. / 偏研究洞察，不是文档级访谈纪要、格式复刻和来源映射。 | [product-on-purpose/pm-skills](https://github.com/product-on-purpose/pm-skills) |

## Why This Repo Is Different / 本仓库的差异化

- EN: This repository combines template-constrained interview-note drafting, selective audio verification, online proper-name cross-checking, and dual deliverables (`clear.docx` + `traceability.docx`) in one workflow.
- 中文：本仓库把“模板约束下的访谈纪要生成、选择性音频补核、专有名词联网校验、双文件输出（`clear.docx` + `traceability.docx`）”整合到同一个工作流里。

## Repository Structure / 仓库结构

- `interview-notes/SKILL.md`
  - EN: Main skill instructions and behavioral contract.
  - 中文：skill 主说明和行为约束。
- `interview-notes/scripts/run_interview_notes.py`
  - EN: CLI entry point.
  - 中文：命令行入口脚本。
- `interview-notes/scripts/interview_notes.py`
  - EN: Core pipeline implementation.
  - 中文：核心处理逻辑。
- `interview-notes/references/`
  - EN: Supporting reference documents for default structure and traceability rules.
  - 中文：默认结构与 traceability 规则的参考文档。
