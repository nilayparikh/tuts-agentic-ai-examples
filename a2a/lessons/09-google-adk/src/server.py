"""
Lesson 09 — A2A server for the ThreatBriefing agent (Google ADK).

Demonstrates the ADK ``to_a2a()`` one-liner that converts any ADK agent
into a standards-compliant A2A server — the simplest A2A integration of
any framework.

Usage (from lessons/09-google-adk/src/):
    python server.py

Endpoints:
    GET  http://localhost:10002/.well-known/agent.json  -> Agent Card
    POST http://localhost:10002/                        -> JSON-RPC

Required env vars (loaded from ``_examples/.env``):
    AZURE_OPENAI_ENDPOINT
    AZURE_AI_API_KEY
    AZURE_AI_MODEL_DEPLOYMENT_NAME
"""

# pylint: disable=wrong-import-position,wrong-import-order

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]

# ── Ensure src/ is on the path ────────────────────────────────────
_SRC = Path(__file__).parent.resolve()
sys.path.insert(0, str(_SRC))

import uvicorn  # noqa: E402
from dotenv import find_dotenv, load_dotenv  # noqa: E402

load_dotenv(find_dotenv(raise_error_if_not_found=False))

# ADK imports — placed after dotenv so env vars are available
from google.adk.a2a.utils.agent_to_a2a import (  # noqa: E402
    to_a2a,
)

from research_agent import build_research_agent  # noqa: E402


SERVER_HOST = "localhost"
SERVER_PORT = 10002

# ─── Build the agent and the A2A app ────────────────────────────

agent = build_research_agent()

# This is the hero line: one call turns any ADK agent into a full
# A2A server — agent card, JSON-RPC handler, task store, all wired.
app = to_a2a(
    agent,
    host=SERVER_HOST,
    port=SERVER_PORT,
)

# ─── Run ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Starting ThreatBriefingAgent A2A server " f"on port {SERVER_PORT} ...")
    print(
        f"  Agent Card : http://{SERVER_HOST}:{SERVER_PORT}" f"/.well-known/agent.json"
    )
    print(f"  JSON-RPC   : POST http://{SERVER_HOST}:{SERVER_PORT}/")
    print()
    uvicorn.run(app, host="0.0.0.0", port=SERVER_PORT)
