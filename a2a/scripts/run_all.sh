#!/usr/bin/env bash
# scripts/run_all.sh — Full end-to-end scenario runner (Linux/macOS)
# Usage: bash scripts/run_all.sh
# Run from: _examples/a2a/

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"
EXAMPLES_ROOT="$(dirname "$ROOT")"
PYTHON="$ROOT/.venv/bin/python"
SERVER_PORT=10001
SERVER_PID=""

# ── Cleanup on exit ────────────────────────────────────────────
cleanup() {
  if [[ -n "$SERVER_PID" ]] && kill -0 "$SERVER_PID" 2>/dev/null; then
    echo ""
    echo "Stopping server (PID $SERVER_PID)..."
    kill "$SERVER_PID" 2>/dev/null || true
    echo "✅ Server stopped"
  fi
}
trap cleanup EXIT INT TERM

# ── Banner ─────────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  A2A Examples — Full Scenario Run"
echo "  Lessons 05 → 06 → 07"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ── Load .env ─────────────────────────────────────────────────
ENV_FILE="$EXAMPLES_ROOT/.env"
if [[ ! -f "$ENV_FILE" ]]; then
  echo "❌ .env not found at $ENV_FILE"
  echo "   Run: bash scripts/setup.sh"
  exit 1
fi
set -a; source "$ENV_FILE"; set +a
echo "✅ Loaded $ENV_FILE"

if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "❌ GITHUB_TOKEN not set in .env"
  exit 1
fi
echo "✅ GITHUB_TOKEN configured"
echo ""

# ══════════════════════════════════════════════════════════════
# LESSON 05 — Standalone QA Agent
# ══════════════════════════════════════════════════════════════
echo "─── LESSON 05 — Standalone QA Agent ───"
echo ""

cd "$ROOT/lessons/05-first-a2a-agent/src"
"$PYTHON" qa_agent.py
echo ""
echo "✅ Lesson 05 complete"
echo ""

# ══════════════════════════════════════════════════════════════
# LESSON 06 — Start A2A Server
# ══════════════════════════════════════════════════════════════
echo "─── LESSON 06 — Starting A2A Server ───"
echo ""

cd "$ROOT/lessons/06-a2a-server/src"
"$PYTHON" server.py &
SERVER_PID=$!
echo "Server starting (PID $SERVER_PID)..."

# Wait for server to become ready
MAX_WAIT=20
READY=false
for i in $(seq 1 $MAX_WAIT); do
  sleep 1
  if curl -sf "http://localhost:${SERVER_PORT}/.well-known/agent.json" > /dev/null 2>&1; then
    READY=true
    break
  fi
  echo "  Waiting for server... ($i/${MAX_WAIT}s)"
done

if [[ "$READY" != "true" ]]; then
  echo "❌ Server did not start within ${MAX_WAIT}s"
  exit 1
fi
echo "✅ Server ready at http://localhost:${SERVER_PORT}"
echo ""

# ══════════════════════════════════════════════════════════════
# LESSON 07 — Client Tests
# ══════════════════════════════════════════════════════════════
echo "─── LESSON 07 — A2A Client Tests ───"
echo ""

QUESTIONS=(
  "What is the annual deductible?"
  "How much is the monthly premium?"
  "Are cosmetic procedures covered?"
  "How do I file a claim?"
  "What is NOT covered by this policy?"
)

PASSED=0
FAILED=0

for Q in "${QUESTIONS[@]}"; do
  MSG_ID=$(python3 -c "import uuid; print(uuid.uuid4().hex)")
  REQ_ID=$(python3 -c "import uuid; print(str(uuid.uuid4()))")

  BODY=$(cat <<EOF
{
  "jsonrpc": "2.0",
  "id": "$REQ_ID",
  "method": "message/send",
  "params": {
    "message": {
      "role": "user",
      "parts": [{"kind": "text", "text": "$Q"}],
      "messageId": "$MSG_ID"
    }
  }
}
EOF
)

  echo "Q: $Q"
  RESPONSE=$(curl -sf -X POST "http://localhost:${SERVER_PORT}" \
    -H "Content-Type: application/json" \
    -d "$BODY" \
    --max-time 60 || echo '{"error": "request failed"}')

  TEXT=$(echo "$RESPONSE" | python3 -c "
import sys, json
try:
    r = json.load(sys.stdin)
    parts = r.get('result', {}).get('status', {}).get('message', {}).get('parts', [])
    text = parts[0].get('text', '') if parts else ''
    print(text[:200] + ('...' if len(text) > 200 else ''))
except Exception as e:
    print(f'(parse error: {e})')
")

  if [[ -n "$TEXT" ]]; then
    echo "A: $TEXT"
    PASSED=$((PASSED + 1))
  else
    echo "A: (empty response)"
    FAILED=$((FAILED + 1))
  fi
  echo ""
done

echo "─── Results ───"
echo "  Passed: $PASSED / ${#QUESTIONS[@]}"
[[ $FAILED -gt 0 ]] && echo "  Failed: $FAILED"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  All scenarios complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
