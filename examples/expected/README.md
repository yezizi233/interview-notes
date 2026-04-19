# Expected Example Outputs

This directory stores reproducible example outputs for the sample transcript.

Contents:

- `sample-transcript_clear.docx`
- `sample-transcript_traceability.docx`
- `sample-transcript_report.json`

They are generated with:

```powershell
python interview-notes/scripts/run_interview_notes.py `
  --transcript examples/sample_transcript.txt `
  --outdir examples/expected `
  --slug sample-transcript `
  --provider none `
  --network-mode offline
```

The expected outputs are intentionally generated without a network dependency and without an LLM provider so they remain stable in CI and local development.
