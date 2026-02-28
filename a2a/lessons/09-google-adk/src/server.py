"""
Lesson 09 — A2A server wrapping the OrchestratorAgent (Google ADK).

Demonstrates ADK's ``to_a2a()`` one-liner that converts any ADK agent into
a standards-compliant A2A server — the simplest A2A integration of any
framework.  Solves the **same loan validation problem** as Lesson 08 to
highlight framework differences while keeping the domain constant.

Usage (from lessons/09-google-adk/src/):
    python server.py

Endpoints:
    GET  http://localhost:10002/.well-known/agent.json  → Agent Card
    POST http://localhost:10002/                        → JSON-RPC
"""

# pylint: disable=wrong-import-position,wrong-import-order

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]

# ── Ensure src/ and _common/src/ are on the path ─────────────────
_SRC = Path(__file__).parent.resolve()
_COMMON = (_SRC / "../../_common/src").resolve()
sys.path.insert(0, str(_SRC))
sys.path.insert(0, str(_COMMON))

import uvicorn  # noqa: E402
from dotenv import find_dotenv, load_dotenv  # noqa: E402

load_dotenv(find_dotenv(raise_error_if_not_found=False))

from google.adk.a2a.utils.agent_to_a2a import to_a2a  # noqa: E402

from orchestrator import OrchestratorAgent  # noqa: E402

SERVER_HOST = "localhost"
SERVER_PORT = 10002

# ─── Build the agent and the A2A app ────────────────────────────

orch = OrchestratorAgent()

# This is the hero line: one call turns any ADK agent into a full
# A2A server — agent card, JSON-RPC handler, task store, all wired.
app = to_a2a(
    orch.agent,
    host=SERVER_HOST,
    port=SERVER_PORT,
)

# ─── Run ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Starting LoanValidatorADK A2A server on port {SERVER_PORT} ...")
    print(f"  Agent Card : http://{SERVER_HOST}:{SERVER_PORT}/.well-known/agent.json")
    print(f"  JSON-RPC   : POST http://{SERVER_HOST}:{SERVER_PORT}/")
    print()
    uvicorn.run(app, host="0.0.0.0", port=SERVER_PORT)
