# Traceability Contract

The traceability file exists to prove that the clean file is complete, faithful, and auditable.

## Purpose

Use the traceability file to show:

- where each point came from
- how the wording was derived
- whether any correction or normalization happened
- whether any uncertainty remains

## Required Fields

Each traceability entry must include:

- `Entry ID`
- `Clean File Location`
- `Source Medium`
- `Speaker`
- `Timestamp`
- `Raw Excerpt`
- `Final Wording`
- `Transformation Method`
- `Name Verification`
- `Uncertainty`

## Field Guidance

### Entry ID

Use a stable ID such as `T-001`, `T-002`, and so on.

### Clean File Location

Point to the exact place in the clean file:

- section
- topic header
- bullet number
- table row when relevant

### Source Medium

Use one of:

- `transcript`
- `recording`
- `transcript + recording`

### Speaker

Use the source label only if reliable.

If unreliable or missing, write:

- `unknown`
- `not reliably labeled`

### Timestamp

Use the best available form:

- exact timestamp
- start-end range
- `timestamp unavailable`

Never invent a precise timestamp.

### Raw Excerpt

Keep it short but sufficient to support the point.

If the excerpt is translated in the clean file, preserve the original-language excerpt here whenever practical.

### Final Wording

Copy the wording used in the clean file, or summarize the exact table row content when the clean file uses a table.

### Transformation Method

Use one or more of:

- `direct quote`
- `compressed rewrite`
- `merged adjacent lines`
- `merged non-adjacent lines`
- `translated`
- `audio-corrected`
- `table-normalized`

### Name Verification

Use one of:

- `verified online`
- `unverified`
- `unverified offline`

If verified online, include the authority used.

### Uncertainty

Use one of:

- `none`
- `wording uncertain`
- `speaker uncertain`
- `number uncertain`
- `name uncertain`
- `timestamp unavailable`

## Completeness Rule

The traceability file must cover every information-bearing point in the clean file.

That includes:

- sentences in bullets
- meaningful clause-level caveats
- table rows
- ranking claims
- quoted language
- normalized proper names

## Audio-Correction Rule

If any wording was corrected using audio review:

- mark the transformation method as `audio-corrected`
- keep the pre-correction transcript wording when useful
- show the corrected wording used in the clean file

## Name-Normalization Rule

If a proper noun was standardized:

- preserve the source form
- preserve the final normalized form
- record the authority used
- do not add unrelated new facts from the verification source
