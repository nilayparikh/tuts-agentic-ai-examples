#!/usr/bin/env bash
# scripts/run_lesson05.sh — Run Lesson 05 standalone QA agent (Linux/macOS)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"
PYTHON="$ROOT/.venv/bin/python"

ENV_FILE="$(dirname "$ROOT")/.env"
[[ -f "$ENV_FILE" ]] && { set -a; source "$ENV_FILE"; set +a; }

[[ -z "${GITHUB_TOKEN:-}" ]] && { echo "❌ GITHUB_TOKEN not set"; exit 1; }

echo "=== Lesson 05 — Standalone QA Agent ==="
cd "$ROOT/lessons/05-first-a2a-agent/src"
"$PYTHON" qa_agent.py
