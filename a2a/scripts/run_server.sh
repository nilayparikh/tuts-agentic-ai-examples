#!/usr/bin/env bash
# scripts/run_server.sh — Start Lesson 06 A2A server (Linux/macOS)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"
PYTHON="$ROOT/.venv/bin/python"

ENV_FILE="$(dirname "$ROOT")/.env"
[[ -f "$ENV_FILE" ]] && { set -a; source "$ENV_FILE"; set +a; }

[[ -z "${GITHUB_TOKEN:-}" ]] && { echo "❌ GITHUB_TOKEN not set"; exit 1; }

echo "=== Lesson 06 — A2A Server ==="
echo "Starting QAAgent on http://localhost:10001"
echo "Agent Card: http://localhost:10001/.well-known/agent.json"
echo "Press Ctrl+C to stop."
echo ""

cd "$ROOT/lessons/06-a2a-server/src"
"$PYTHON" server.py
