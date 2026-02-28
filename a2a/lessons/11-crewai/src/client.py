"""
Lesson 11 — A2A Client for the CrewAI-based Loan Validation Agent.

Usage:
    python client.py          # expects the server on http://localhost:10004

Demonstrates:
    1. Discover agent via Agent Card
    2. Send validation request for each test applicant
    3. Print the structured validation report
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

# ─── path setup: import shared data from _common ─────────────────────────────
_COMMON = str(Path(__file__).resolve().parents[2] / "_common" / "src")
if _COMMON not in sys.path:
    sys.path.insert(0, _COMMON)

from loan_data import APPLICANTS

# ─── A2A client imports ──────────────────────────────────────────────────────

from a2a.client import A2AClient, httpx


SERVER_URL = "http://localhost:10004"


def _extract_text(response) -> str:
    """Pull plain text from an A2A response (handles Message, Task, and Event tuple)."""
    # response may be a Message, Task, or tuple (Task | None, Event | None)
    obj = response
    if isinstance(response, tuple):
        obj = response[0] or response[1]

    # Walk into the message parts
    message = getattr(obj, "message", None) or getattr(obj, "result", None)
    if message is None and hasattr(obj, "status"):
        message = getattr(obj.status, "message", None)

    if message and hasattr(message, "parts"):
        texts = []
        for part in message.parts:
            root = getattr(part, "root", part)
            if hasattr(root, "text"):
                texts.append(root.text)
        if texts:
            return "\n".join(texts)

    return f"(unexpected response — {type(obj).__name__})"


async def _run() -> None:
    async with httpx.AsyncClient() as httpx_client:
        client = await A2AClient.get_client_from_agent_card_url(
            httpx_client, f"{SERVER_URL}/.well-known/agent.json"
        )

        print(f"✅ Connected to A2A agent at {SERVER_URL}")
        print(f"   Agent: {client.agent_card.name}")
        print(f"   Skills: {[s.name for s in client.agent_card.skills]}\n")

        for app in APPLICANTS:
            print(f"━━━ Validating {app.full_name} ({app.applicant_id}) ━━━")
            response = await client.send_message(
                message={
                    "role": "user",
                    "parts": [
                        {"text": f"Validate loan application {app.applicant_id}"}
                    ],
                    "messageId": f"msg-{app.applicant_id}",
                },
            )
            print(_extract_text(response))
            print()


def main() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    main()
