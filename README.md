# interview-notes

Interview-notes skill repository.

Primary skill:

- `interview-notes/` — generate faithful interview notes from transcripts and/or recordings, with template matching, selective audio verification, name cross-checking, and a dual-output workflow (`clear` file + traceability file).

Runnable local pipeline:

```powershell
python interview-notes/scripts/run_interview_notes.py `
  --transcript examples/sample_transcript.txt `
  --outdir output
```

Optional inputs:

- `--audio path/to/file.wav`
- `--template path/to/template.docx`
- `--output-language zh|en|auto`
- `--provider auto|openai|anthropic|none`
- `--network-mode auto|online|offline`

Notes:

- If `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` is configured, the script uses an LLM to build higher-quality structured notes.
- Without an LLM provider, it falls back to a source-grounded local formatter.
- Online name verification currently auto-verifies `ClinicalTrials.gov` trial IDs and preserves other names as `unverified` unless a future authoritative adapter is added.
