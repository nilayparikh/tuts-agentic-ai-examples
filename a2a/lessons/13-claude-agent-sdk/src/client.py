"""
Lesson 13 — A2A Client for the Claude-style Loan Validation Agent.

Usage:
    python client.py          # expects the server on http://localhost:10006

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
from uuid import uuid4

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]

# ─── path setup: import shared data from _common ─────────────────────────────
_COMMON = str(Path(__file__).resolve().parents[2] / "_common" / "src")
_PROJECT_ROOT = str(Path(__file__).resolve().parents[3])
if _COMMON not in sys.path:
    sys.path.insert(0, _COMMON)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from loan_data import APPLICANTS  # noqa: E402
DEMO_APPLICANTS = APPLICANTS[:3]

import httpx  # noqa: E402
from a2a.client import ClientConfig, ClientFactory  # noqa: E402
from a2a.types import Message, Part, Role, TextPart  # noqa: E402


SERVER_URL = "http://localhost:10006"


def _get_client_config() -> ClientConfig:
    """Create a fresh ClientConfig with an httpx client."""
    return ClientConfig(
        httpx_client=httpx.AsyncClient(timeout=300.0),
        streaming=False,
    )


def _build_message(applicant_id: str) -> Message:
    """Build an A2A Message for the given applicant ID."""
    return Message(
        message_id=uuid4().hex,
        role=Role.user,
        parts=[
            Part(root=TextPart(kind="text", text=f"Validate {applicant_id}")),
        ],
    )


def _extract_text(item: object) -> str:
    """Extract text from a response item (Message or Task tuple)."""
    if isinstance(item, Message):
        texts = [p.root.text for p in item.parts if hasattr(p.root, "text")]
        return "\n".join(texts) if texts else "(no text in response)"

    # Handle (Task, Event) tuple
    if isinstance(item, tuple):
        task = item[0]
        if hasattr(task, "history") and task.history:
            for msg in reversed(task.history):
                if getattr(msg, "role", None) != Role.agent:
                    continue
                texts = [
                    p.root.text
                    for p in msg.parts
                    if hasattr(p, "root") and hasattr(p.root, "text")
                ]
                if texts:
                    return "\n".join(texts)
        status = getattr(task, "status", None)
        if status and hasattr(status, "message") and status.message:
            msg = status.message
            texts = [
                p.root.text
                for p in msg.parts
                if hasattr(p, "root") and hasattr(p.root, "text")
            ]
            if texts:
                return "\n".join(texts)

    return f"(unexpected type: {type(item).__name__})"


async def _run() -> None:
    """Connect to the Claude-style agent and validate all test applicants."""
    client = await ClientFactory.connect(
        agent=SERVER_URL,
        client_config=_get_client_config(),
    )
    card = await client.get_card()

    print(f"Connected to A2A agent at {SERVER_URL}")
    print(f"   Agent: {card.name}")
    print(f"   Skills: {[s.name for s in (card.skills or [])]}\n")

    for app in DEMO_APPLICANTS:
        print(f"--- Validating {app.full_name} " f"({app.applicant_id}) ---")
        msg = _build_message(app.applicant_id)
        async for item in client.send_message(msg):
            print(_extract_text(item))
        print()


def main() -> None:
    """Run the A2A client demo."""
    asyncio.run(_run())


if __name__ == "__main__":
    main()
