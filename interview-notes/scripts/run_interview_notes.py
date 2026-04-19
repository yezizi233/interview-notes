from __future__ import annotations

import argparse
import json
import sys

from interview_notes import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate clear and traceability interview-notes DOCX files from transcripts, recordings, and optional templates."
    )
    parser.add_argument("--transcript", help="Path to transcript input (.txt, .md, or .docx).")
    parser.add_argument("--audio", help="Path to audio input for full transcription or selective verification.")
    parser.add_argument("--template", help="Optional path to a finished interview-notes template (.docx preferred).")
    parser.add_argument("--title", help="Optional title override.")
    parser.add_argument("--slug", help="Optional output slug override.")
    parser.add_argument("--outdir", default="output", help="Output directory for generated DOCX files.")
    parser.add_argument("--output-language", choices=["auto", "zh", "en"], default="auto")
    parser.add_argument("--provider", choices=["auto", "openai", "anthropic", "none"], default="auto")
    parser.add_argument("--model", help="Optional provider model override.")
    parser.add_argument("--network-mode", choices=["auto", "online", "offline"], default="auto")
    parser.add_argument("--whisper-model", default="base", help="faster_whisper model size for audio paths.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        report = run_pipeline(args)
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps({"ok": True, **report}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
