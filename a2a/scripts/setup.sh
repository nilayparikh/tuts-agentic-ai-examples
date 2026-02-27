#!/usr/bin/env bash
# scripts/setup.sh — One-time environment setup
# Usage: bash scripts/setup.sh
# Run from: _examples/a2a/

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"

echo "=== A2A Examples — Environment Setup ==="
echo ""

# ── .env check ────────────────────────────────────────────────
ENV_FILE="$(dirname "$ROOT")/.env"
if [[ ! -f "$ENV_FILE" ]]; then
  echo "⚠  .env file not found at $ENV_FILE"
  echo "   Copy .env.example → .env and fill in GITHUB_TOKEN:"
  echo "   cp $(dirname "$ROOT")/.env.example $(dirname "$ROOT")/.env"
  exit 1
fi

if ! grep -q "GITHUB_TOKEN=" "$ENV_FILE"; then
  echo "❌ GITHUB_TOKEN not set in $ENV_FILE"
  echo "   Get a GitHub PAT at https://github.com/settings/tokens"
  exit 1
fi
echo "✅ .env found with GITHUB_TOKEN"

# ── Create .venv ───────────────────────────────────────────────
cd "$ROOT"
if [[ ! -d ".venv" ]]; then
  echo ""
  echo "Creating .venv with uv..."
  uv venv .venv --python 3.11
else
  echo "✅ .venv already exists"
fi

# ── Install dependencies ───────────────────────────────────────
echo ""
echo "Installing dependencies..."
uv pip install -r requirements.txt

# ── Register Jupyter kernel ────────────────────────────────────
echo ""
echo "Registering Jupyter kernel 'a2a-examples'..."
.venv/bin/python -m ipykernel install --user --name a2a-examples --display-name "A2A Examples (Python 3.11)"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  Start the A2A server:  bash scripts/run_server.sh"
echo "  Run Lesson 05:         bash scripts/run_lesson05.sh"
echo "  Run all scenarios:     bash scripts/run_all.sh"
