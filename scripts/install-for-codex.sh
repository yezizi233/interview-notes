#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_SOURCE="$REPO_ROOT/interview-notes"
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
TARGET_DIR="$CODEX_HOME_DIR/skills/interview-notes"

mkdir -p "$CODEX_HOME_DIR/skills"
rm -rf "$TARGET_DIR"
cp -R "$SKILL_SOURCE" "$TARGET_DIR"

if command -v python3 >/dev/null 2>&1; then
  python3 -m pip install -r "$TARGET_DIR/requirements.txt"
fi

cat <<EOF
Installed interview-notes to:
  $TARGET_DIR

Core Python dependencies were installed from:
  $TARGET_DIR/requirements.txt

For audio support, also run:
  python3 -m pip install -r "$TARGET_DIR/requirements-audio.txt"
EOF
