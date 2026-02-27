#!/usr/bin/env bash
# scripts/run_client.sh — Send test requests to a running A2A server (Linux/macOS)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"

echo "=== Lesson 07 — A2A Client Tests ==="
echo ""

# Check server
if ! curl -sf "http://localhost:10001/.well-known/agent.json" > /dev/null 2>&1; then
  echo "❌ Server not reachable at http://localhost:10001"
  echo "   Start it: bash scripts/run_server.sh"
  exit 1
fi
echo "✅ Server is running"
echo ""

QUESTIONS=(
  "What is the annual deductible?"
  "How much is the monthly premium?"
  "Are cosmetic procedures covered?"
  "How do I file a claim?"
)

for Q in "${QUESTIONS[@]}"; do
  echo "Q: $Q"
  MSG_ID=$(python3 -c "import uuid; print(uuid.uuid4().hex)")
  REQ_ID=$(python3 -c "import uuid; print(str(uuid.uuid4()))")
  RESPONSE=$(curl -sf -X POST "http://localhost:10001" \
    -H "Content-Type: application/json" \
    -d "{\"jsonrpc\":\"2.0\",\"id\":\"$REQ_ID\",\"method\":\"message/send\",\"params\":{\"message\":{\"role\":\"user\",\"parts\":[{\"kind\":\"text\",\"text\":\"$Q\"}],\"messageId\":\"$MSG_ID\"}}}" \
    --max-time 60)
  TEXT=$(echo "$RESPONSE" | python3 -c "import sys,json; r=json.load(sys.stdin); p=r.get('result',{}).get('status',{}).get('message',{}).get('parts',[]); print(p[0].get('text','')[:200] if p else '(empty)')" 2>/dev/null || echo "(error)")
  echo "A: $TEXT"
  echo ""
done

echo "✅ Client test complete."
