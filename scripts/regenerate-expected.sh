#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$REPO_ROOT/examples/expected"
mkdir -p "$OUT_DIR"

python3 "$REPO_ROOT/interview-notes/scripts/run_interview_notes.py" \
  --transcript "$REPO_ROOT/examples/sample_transcript.txt" \
  --outdir "$OUT_DIR" \
  --slug sample-transcript \
  --provider none \
  --network-mode offline | tee "$OUT_DIR/sample-transcript_report.json"
