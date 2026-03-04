"""
Lesson 12 — A2A Client for the OpenAI Agents SDK-based Loan Validation Agent.

Usage:
    python client.py          # expects the server on http://localhost:10005

Demonstrates:
    1. Discover agent via Agent Card
    2. Send validation request for each test applicant
    3. Print the structured validation report
"""

# mypy: disable-error-code=import-not-found

# pylint: disable=wrong-import-position,wrong-import-order

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Any
from uuid import uuid4

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]

# ─── path setup: import shared data from _common ─────────────────────
_COMMON = str(Path(__file__).resolve().parents[2] / "_common" / "src")
_PROJECT_ROOT = str(Path(__file__).resolve().parents[3])
if _COMMON not in sys.path:
    sys.path.insert(0, _COMMON)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from loan_data import APPLICANTS  # noqa: E402  # pylint: disable=import-error

DEMO_APPLICANTS = APPLICANTS[:3]

import httpx  # noqa: E402
from a2a.client import A2ACardResolver, A2AClient  # noqa: E402
from a2a.types import MessageSendParams, SendMessageRequest  # noqa: E402


SERVER_URL = "http://localhost:10005"


def _build_request(text: str) -> SendMessageRequest:
    """Build a SendMessageRequest payload using A2A message schema."""
    payload = {
        "message": {
            "role": "user",
            "parts": [{"kind": "text", "text": text}],
            "messageId": uuid4().hex,
        }
    }
    return SendMessageRequest(
        id=str(uuid4()),
        params=MessageSendParams(**payload),  # type: ignore[arg-type]
    )


def _extract_text(response: object) -> str:
    """Extract text from a SendMessageResponse object."""
    root = getattr(response, "root", None)
    result = getattr(root, "result", None)
    parts = getattr(result, "parts", None)
    if parts:
        texts = [getattr(getattr(part, "root", None), "text", None) for part in parts]
        clean = [text for text in texts if isinstance(text, str) and text]
        if clean:
            return "\n".join(clean)

    if hasattr(response, "model_dump"):
        dump = response.model_dump(mode="json", exclude_none=True)
        task = dump.get("result", {})
        task_message = task.get("status", {}).get("message", {})
        task_parts = task_message.get("parts", [])
        texts = [
            part.get("text")
            for part in task_parts
            if isinstance(part, dict) and part.get("kind") == "text"
        ]
        clean = [text for text in texts if isinstance(text, str) and text]
        if clean:
            return "\n".join(clean)

    return "(no text in response)"


async def _create_client(httpx_client: httpx.AsyncClient) -> tuple[A2AClient, Any]:
    """Resolve agent card and construct an A2AClient."""
    resolver = A2ACardResolver(httpx_client=httpx_client, base_url=SERVER_URL)
    card = await resolver.get_agent_card()
    return A2AClient(httpx_client=httpx_client, agent_card=card), card


async def _run() -> None:
    """Connect to the OpenAI Agents SDK agent and validate all test applicants."""
    async with httpx.AsyncClient(timeout=300.0) as httpx_client:
        client, card = await _create_client(httpx_client)
        print(f"Connected to A2A agent at {SERVER_URL}")
        print(f"   Agent: {card.name}")
        print(f"   Skills: {[s.name for s in (card.skills or [])]}\n")

        for app in DEMO_APPLICANTS:
            print(f"--- Validating {app.full_name} " f"({app.applicant_id}) ---")
            response = await client.send_message(
                _build_request(f"Validate {app.applicant_id}")
            )
            print(_extract_text(response))
            print()


def main() -> None:
    """Run the A2A client demo."""
    asyncio.run(_run())


if __name__ == "__main__":
    main()
