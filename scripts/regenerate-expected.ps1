$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$OutDir = Join-Path $RepoRoot "examples\expected"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

python (Join-Path $RepoRoot "interview-notes\scripts\run_interview_notes.py") `
  --transcript (Join-Path $RepoRoot "examples\sample_transcript.txt") `
  --outdir $OutDir `
  --slug sample-transcript `
  --provider none `
  --network-mode offline | Tee-Object -FilePath (Join-Path $OutDir "sample-transcript_report.json")
