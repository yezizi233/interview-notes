---
name: interview-notes
description: >
  Generate high-fidelity interview notes from transcripts and/or recordings.
  Use whenever the user asks to write, organize, verify, rewrite, format, or
  template-match interview notes / 访谈纪要 from transcript text, audio
  recordings, or both. Also use when the user uploads a finished
  interview-notes example and wants the new output to strictly follow its
  section structure, indentation, numbering, bullet logic, or table style.
  Supports bilingual input, user-selected Chinese or English output, selective
  audio verification, evidence mapping, and dual deliverables: a clean final
  note file plus a traceability file.
---

# Interview Notes

Produce faithful interview notes, not generic summaries.

This skill is for interview notes only. Do not silently turn it into a meeting-minutes workflow.

## Non-Negotiable Rules

- Do not omit valid information points.
- Do not fabricate.
- Do not guess speaker identity, terminology, numbers, or names.
- Do not add background knowledge, industry context, or explanatory notes unless the user explicitly provided that material.
- Do not de-identify or redact unless the user asks.
- Every point in the clean deliverable must be traceable to at least one source excerpt in the traceability deliverable.

## Inputs

Accepted input combinations:

- transcript only
- recording only
- transcript + recording
- any of the above plus a completed interview-notes template

Accepted transcript languages:

- Chinese
- English
- mixed Chinese and English

Output language:

- Chinese or English, based on user choice
- If the user does not choose, follow the template language when a template is provided
- If there is no template, follow the dominant source language

## Online vs Offline Mode

At the start, determine whether network access is available.

If online:

- You may cross-check proper nouns, company names, product names, trial names, institution names, and acronym expansions against authoritative sources
- Use that check only for name normalization and spelling correction, not to inject new facts

If offline:

- Tell the user which name-verification features are unavailable before proceeding
- Continue with note generation, template matching, and traceability output
- Mark any unverified names as `unverified offline` in the traceability file
- Never present an unverified normalized name as confirmed

## Proper-Name Verification

When online, verify names before finalizing the clean file.

Preferred source order:

1. official company or product site
2. official registry or regulator page
3. ClinicalTrials.gov or equivalent official trial registry
4. official paper, official database entry, or issuer IR/newsroom page

Rules:

- Use online verification only to standardize the name already present in the source material
- If the source text says `Arsenal` but the official name is longer or differently styled, use the verified standard form in the clean file when confidence is high
- Record the original form, corrected form, source URL, and reason in the traceability file
- If confidence is not high, preserve the source form and mark it `unverified`

## Source Priority

### Transcript + Recording

Use the transcript as the primary source.

Only review audio when the transcript contains:

- unclear wording
- missing fragments
- contradictory wording
- suspicious technical terms
- suspicious proper nouns
- suspicious numbers, dates, rankings, or amounts
- segments whose wording materially changes meaning

Use `faster_whisper` only on the smallest necessary audio span.

If the transcript has timestamps, use them to isolate the review span.

If the transcript lacks timestamps:

- try to identify the smallest reasonable audio span from nearby cues
- if precise isolation is not possible, tell the user that narrow-segment audio verification is not possible from the current materials
- do not silently run broad audio re-transcription unless the user only provided audio

### Recording Only

Full transcription is allowed.

If local transcription tooling required for this step is unavailable, say so immediately.

### Transcript Only

Do not pretend audio verification happened.

## Template Priority

When the user provides a completed interview-notes template, follow it strictly for visible document structure:

- section ordering
- heading style
- numbering style
- indentation
- bullet logic
- table style
- quote style
- note style

Do not automatically copy:

- cover pages
- headers or footers
- document metadata
- unrelated boilerplate

Hard rules still outrank the template:

- fidelity
- no fabrication
- traceability
- dual-file output
- explicit uncertainty marking

## Default Structure

Use this only when the user does not provide a template.

Default pattern:

1. document title
2. major sections using `一、 / 二、 / 三、` style in Chinese or equivalent numbered sections in English
3. theme sub-sections using bracketed labels such as `【主题】`
4. first-level bullets for main findings or topic sentences
5. second-level bullets for detail, conditions, comparisons, exceptions, and support

The clean file should read like topic-organized interview notes, not a chronological transcript dump.

## Tables for Numeric Content

When a section contains many comparable numbers, use a table to improve readability.

Typical triggers:

- multiple vendors or products compared on numeric dimensions
- rankings
- counts across categories
- dates, phases, percentages, ranges, budgets, volumes, pricing, or timelines

Rules:

- Use tables only when they improve clarity
- Do not compress away conditions, caveats, or exceptions
- Keep any limiting statements below the table as bullets if needed
- Add row-level traceability in the traceability file

If the imported template never uses tables, you may still insert a local table for numeric-heavy sections. Readability wins over a purely list-only default.

## Clean Deliverable

Unless the user explicitly asks for another format, produce:

- `<slug>_clear.docx`
- `<slug>_traceability.docx`

The clean deliverable is reader-facing.

It should:

- follow the chosen template or default structure
- preserve all valid information points
- state uncertainty only where the source is uncertain
- use direct quotes sparingly and only when they add fidelity
- avoid provenance clutter unless the template explicitly expects it

## Traceability Deliverable

The traceability deliverable is audit-facing.

Each entry must map one clean-file point to source evidence.

Minimum fields per entry:

- entry ID
- location in clean file
- source medium: transcript / recording / both
- speaker label if reliably available
- timestamp or timestamp range
- raw source excerpt
- final wording used in the clean file
- transformation method
- proper-name verification status
- uncertainty flag

Accepted transformation methods:

- direct quote
- compressed rewrite
- merged from multiple adjacent sentences
- merged from multiple source locations
- translated
- audio-corrected
- table-normalized

If no timestamp is available from the provided materials, write `timestamp unavailable` instead of inventing one.

## Speaker Attribution

Only preserve speaker labels when they are reliable in the source.

If the source does not reliably distinguish interviewer, interviewee, or third parties:

- do not guess
- write content without false attribution
- mark attribution as unavailable in the traceability file

## Writing Behavior

During drafting:

- preserve meaning over wording
- preserve conditions, scope limits, exceptions, and comparisons
- preserve ranking direction and numeric precision when present
- preserve ambiguity when ambiguity is real

Do not:

- sharpen vague statements into hard claims
- merge distinct facts into one sentence if that hides detail
- move unsupported interpretation into the clean file

## Workflow

1. Inventory the inputs.
2. Determine output language.
3. Determine whether network access is available.
4. If offline, tell the user which name-verification functions are unavailable.
5. If a template exists, extract its visible structure and formatting logic.
6. Build an evidence ledger from the transcript first.
7. If audio review is allowed and needed, review only the minimal ambiguous spans.
8. Verify proper nouns online when available.
9. Draft the clean file.
10. Draft the traceability file.
11. Run the final checks below.

## Final Checks

Before finishing, verify all of the following:

- every clean-file point has at least one traceability entry
- no traceability entry points to unsupported wording
- unresolved names are marked `unverified` or `unverified offline`
- no timestamp is invented
- no speaker is guessed
- no externally sourced explanatory note leaked into the clean file
- any audio correction is marked as such
- any table row with normalized numbers can be mapped back to source evidence

## References

Read these only when needed:

- `references/default-output-structure.md` for the default note layout
- `references/traceability-contract.md` for the traceability file contract
