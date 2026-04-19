# interview-notes

Auditable interview notes with template fidelity and evidence traceability.

可审计的访谈纪要工作流：严格贴合模板格式，并为每个要点保留证据映射。

## Why This Repo Exists / 这个仓库解决什么问题

### English

Most public note-taking skills stop at transcript summarization. This repository is narrower and stricter:

- interview notes only, not generic meeting minutes
- template-constrained output
- selective audio verification instead of blind full re-transcription
- online proper-name checks from official sources when available
- dual deliverables: `clear.docx` and `traceability.docx`

### 中文

很多公开的纪要 skill 只做到“把 transcript 摘要化”。这个仓库更窄、更严格：

- 只做访谈纪要，不做泛化会议纪要
- 输出必须受模板约束
- 音频只补核模糊片段，而不是盲目全量重转
- 联网时对专有名词做校验
- 默认双文件输出：`clear.docx` 和 `traceability.docx`

## Installation / 安装

### English

Clone the repository:

```powershell
git clone https://github.com/yezizi233/interview-notes.git
cd interview-notes
```

Install into Codex:

```powershell
# PowerShell
.\scripts\install-for-codex.ps1

# or Bash
./scripts/install-for-codex.sh
```

What the install script does:

- copies `interview-notes/` into `$CODEX_HOME/skills/interview-notes` or `~/.codex/skills/interview-notes`
- installs core Python dependencies
- leaves audio dependencies as an explicit optional step

Optional audio dependencies:

```powershell
python -m pip install -r interview-notes/requirements-audio.txt
```

### 中文

先克隆仓库：

```powershell
git clone https://github.com/yezizi233/interview-notes.git
cd interview-notes
```

安装到 Codex：

```powershell
# PowerShell
.\scripts\install-for-codex.ps1

# 或 Bash
./scripts/install-for-codex.sh
```

安装脚本会：

- 把 `interview-notes/` 复制到 `$CODEX_HOME/skills/interview-notes` 或 `~/.codex/skills/interview-notes`
- 安装核心 Python 依赖
- 把音频依赖保留为显式的可选步骤

可选音频依赖：

```powershell
python -m pip install -r interview-notes/requirements-audio.txt
```

## Quick Start / 快速开始

### English

Run the local pipeline with a transcript:

```powershell
python interview-notes/scripts/run_interview_notes.py `
  --transcript examples/sample_transcript.txt `
  --outdir output
```

### 中文

使用 transcript 运行本地流程：

```powershell
python interview-notes/scripts/run_interview_notes.py `
  --transcript examples/sample_transcript.txt `
  --outdir output
```

Common options / 常用参数：

- `--audio path/to/file.wav`
- `--template path/to/template.docx`
- `--output-language zh|en|auto`
- `--provider auto|openai|anthropic|none`
- `--network-mode auto|online|offline`

## Input Support Matrix / 输入条件矩阵

| Scenario / 场景 | Supported / 支持内容 | Degraded or unavailable / 降级或不可用功能 |
| --- | --- | --- |
| Transcript only / 仅 transcript | note generation, template matching, clear + traceability DOCX | no audio correction |
| Audio only / 仅录音 | full transcription, note generation, clear + traceability DOCX | depends on optional audio dependencies |
| Transcript + audio / transcript + 录音 | transcript-first workflow, selective ambiguous-span verification, dual DOCX outputs | narrow-span verification depends on usable timestamps or nearby cues |
| Online mode / 联网模式 | proper-name verification adapters, standard-name correction when supported | still no silent fact injection |
| Offline mode / 离线模式 | full note workflow, template matching, traceability output | authoritative proper-name verification disabled; names marked `unverified offline` |
| No LLM provider / 无 LLM provider | local source-grounded formatter, deterministic DOCX generation | weaker synthesis and translation quality |
| With LLM provider / 有 LLM provider | stronger structure, better topic grouping, better bilingual output | still bound by source fidelity rules |

## Output Contract / 输出约定

Default outputs:

- `<slug>_clear.docx`
- `<slug>_traceability.docx`

The clean file is reader-facing.

最终稿面向阅读。

The traceability file is audit-facing and maps each point back to source evidence.

对照文件面向核查，会把每条要点映射回原始证据。

## Official Name Verification Coverage / 官方名称核验覆盖范围

### English

Current automatic adapters use official sources only:

- `SEC EDGAR`: public-company names and ticker symbols
- `DailyMed`: official drug or product names covered by DailyMed
- `ClinicalTrials.gov`: trial identifiers plus sponsor or collaborator organization names

If a term does not resolve with high confidence against one of these sources, the pipeline preserves the source form and marks it as unverified.

### 中文

当前自动核验只使用官方来源：

- `SEC EDGAR`：上市公司名称和股票代码
- `DailyMed`：DailyMed 收录的官方药品/产品名称
- `ClinicalTrials.gov`：试验编号，以及 sponsor / collaborator 机构名称

如果某个名称无法在这些官方来源上高置信命中，流程会保留原始写法，并把它标记为 `unverified`。

## Validation / 验证方式

### English

This repository now includes:

- a runnable smoke test: `tests/test_smoke.py`
- a GitHub Actions workflow: `.github/workflows/smoke-test.yml`
- deterministic sample input: `examples/sample_transcript.txt`
- expected example outputs under `examples/expected/`

Run locally:

```powershell
python tests/test_smoke.py
```

### 中文

这个仓库目前包含：

- 可运行的 smoke test：`tests/test_smoke.py`
- GitHub Actions 工作流：`.github/workflows/smoke-test.yml`
- 可复现的样例输入：`examples/sample_transcript.txt`
- 放在 `examples/expected/` 下的示例输出

本地运行：

```powershell
python tests/test_smoke.py
```

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
- `interview-notes/scripts/name_verification/`
  - EN: Adapter-based online name-verification layer.
  - 中文：adapter 化的在线名称核验层。
- `scripts/install-for-codex.sh` and `scripts/install-for-codex.ps1`
  - EN: One-step installation helpers.
  - 中文：一键安装辅助脚本。
- `tests/test_smoke.py`
  - EN: Repository smoke test.
  - 中文：仓库 smoke test。
- `.github/workflows/smoke-test.yml`
  - EN: CI workflow that validates the pipeline.
  - 中文：自动验证流程的 CI 工作流。
