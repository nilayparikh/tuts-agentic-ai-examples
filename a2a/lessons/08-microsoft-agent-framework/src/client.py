"""
Lesson 08 — A2A client for the LoanValidatorOrchestrator server.

Demonstrates the full A2A protocol round-trip:
  1. Discover the agent via GET /.well-known/agent.json
  2. Send a loan validation request via JSON-RPC message/send
  3. Receive the structured ValidationReport response

Usage (server must be running on port 10008 first):
    python client.py                     # validate all 3 applicants
    python client.py APP-2024-003        # validate a specific applicant

Environment:
    Activate the project venv first:
        .venv/Scripts/activate   (Windows)
        source .venv/bin/activate (macOS/Linux)

Requires:
    pip install "a2a-sdk[http-server]" httpx python-dotenv
"""

# pylint: disable=wrong-import-position,wrong-import-order

from __future__ import annotations

import sys

sys.stdout.reconfigure(  # type: ignore[union-attr]
    encoding="utf-8",
    errors="replace",
)

from dotenv import find_dotenv, load_dotenv  # noqa: E402

load_dotenv(find_dotenv(raise_error_if_not_found=False))

import asyncio  # noqa: E402
from uuid import uuid4  # noqa: E402

try:
    import httpx  # noqa: E402
    from a2a.client import (  # noqa: E402
        ClientConfig,
        ClientFactory,
    )
    from a2a.types import (  # noqa: E402
        Message,
        Part,
        Role,
        TextPart,
    )
except ImportError as _imp_err:
    print(
        f"ERROR: {_imp_err}\n\n"
        "Make sure you activate the project virtual environment:\n"
        "    .venv\\Scripts\\activate   (Windows)\n"
        "    source .venv/bin/activate (macOS/Linux)\n\n"
        "Then install deps:\n"
        '    pip install "a2a-sdk[http-server]" httpx python-dotenv'
    )
    sys.exit(1)


SERVER_URL = "http://localhost:10008"

DEFAULT_APPLICANTS = ["APP-2024-001", "APP-2024-002", "APP-2024-003"]


def _get_client_config() -> ClientConfig:
    """Create a fresh ClientConfig with a new httpx client (avoids closed loop issues)."""
    return ClientConfig(
        httpx_client=httpx.AsyncClient(timeout=120.0),
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

    # Handle (Task, Event) tuple — extract from last agent message in history
    if isinstance(item, tuple):
        task = item[0]
        # Check task.history for agent messages
        if hasattr(task, "history") and task.history:
            for msg in reversed(task.history):
                if getattr(msg, "role", None) != Role.agent:
                    continue
                texts = [
                    p.root.text
                    for p in msg.parts
                    if hasattr(p, "root")
                    and hasattr(p.root, "text")
                    and not (getattr(p.root, "metadata", None) or {}).get("adk_thought")
                ]
                if texts:
                    return "\n".join(texts)
        # Fallback: check status.message
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


async def discover_agent() -> dict:
    """Discover the LoanValidatorOrchestrator via A2A Agent Card."""
    client = await ClientFactory.connect(
        agent=SERVER_URL,
        client_config=_get_client_config(),
    )
    card = await client.get_card()
    return {
        "name": card.name,
        "description": card.description,
        "url": card.url,
        "version": card.version,
        "skills": [
            {"id": s.id, "name": s.name, "description": s.description}
            for s in (card.skills or [])
        ],
    }


async def validate_applicant(applicant_id: str) -> str:
    """Send a loan validation request via A2A protocol and return the result."""
    client = await ClientFactory.connect(
        agent=SERVER_URL,
        client_config=_get_client_config(),
    )
    msg = _build_message(applicant_id)

    async for item in client.send_message(msg):
        return _extract_text(item)

    return "(no response received)"


async def main(applicant_ids: list[str] | None = None) -> None:
    """Run the A2A client demo against LoanValidatorOrchestrator."""
    target_ids = applicant_ids or DEFAULT_APPLICANTS

    # Step 1: Discover
    print("\n── Agent Discovery ──────────────────────────────")
    try:
        info = await discover_agent()
    except httpx.ConnectError:
        print(
            "ERROR: Cannot connect to server at "
            f"{SERVER_URL}.\n"
            "Start it first:  python server.py"
        )
        sys.exit(1)

    print(f"  Name    : {info['name']}")
    print(f"  Version : {info['version']}")
    print(f"  URL     : {info['url']}")
    print(f"  Skills  : {len(info['skills'])}")
    for skill in info["skills"]:
        print(f"    • {skill['name']}: {skill['description']}")

    # Step 2: Validate each applicant via A2A
    for app_id in target_ids:
        print(f"\n── Validating {app_id} via A2A ─────────────────")
        result = await validate_applicant(app_id)
        print(result)

    print("\n── Done ────────────────────────────────────────\n")


if __name__ == "__main__":
    ids = sys.argv[1:] if len(sys.argv) > 1 else None
    asyncio.run(main(ids))
