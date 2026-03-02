"""
Lesson 09 — A2A client for the LoanValidatorADK server.

Demonstrates the full A2A protocol round-trip — identical pattern to
Lesson 08's client, proving cross-framework interoperability.

Usage (server on port 10002 must be running first):
    python client.py                     # validate all 3 applicants
    python client.py APP-2024-003        # validate a specific applicant
"""

# pylint: disable=wrong-import-position,wrong-import-order

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]

from dotenv import find_dotenv, load_dotenv  # noqa: E402

load_dotenv(find_dotenv(raise_error_if_not_found=False))

import asyncio  # noqa: E402
from uuid import uuid4  # noqa: E402

try:
    import httpx  # noqa: E402
    from a2a.client import ClientConfig, ClientFactory  # noqa: E402
    from a2a.types import Message, Part, Role, TextPart  # noqa: E402
except ImportError as _imp_err:
    print(
        f"ERROR: {_imp_err}\n\n"
        "Make sure you activate the project virtual environment:\n"
        '    pip install "a2a-sdk[http-server]" httpx python-dotenv'
    )
    sys.exit(1)


SERVER_URL = "http://localhost:10002"
DEFAULT_APPLICANTS = ["APP-2024-001", "APP-2024-002", "APP-2024-003"]


def _get_client_config() -> ClientConfig:
    return ClientConfig(httpx_client=httpx.AsyncClient(timeout=120.0), streaming=False)


def _build_message(applicant_id: str) -> Message:
    return Message(
        message_id=uuid4().hex,
        role=Role.user,
        parts=[Part(root=TextPart(kind="text", text=f"Validate {applicant_id}"))],
    )


def _extract_text(item: object) -> str:
    """Extract text from a response item (Message or Task tuple)."""
    if isinstance(item, Message):
        texts = [p.root.text for p in item.parts if hasattr(p.root, "text")]
        return "\n".join(texts) if texts else "(no text in response)"
    if isinstance(item, tuple):
        task = item[0]
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
        status = getattr(task, "status", None)
        if status and hasattr(status, "message") and status.message:
            texts = [
                p.root.text
                for p in status.message.parts
                if hasattr(p, "root") and hasattr(p.root, "text")
            ]
            if texts:
                return "\n".join(texts)
    return f"(unexpected type: {type(item).__name__})"


async def discover_agent() -> dict:
    client = await ClientFactory.connect(
        agent=SERVER_URL, client_config=_get_client_config()
    )
    card = await client.get_card()
    return {
        "name": card.name,
        "description": card.description,
        "url": card.url,
        "version": getattr(card, "version", "n/a"),
        "skills": [
            {"id": s.id, "name": s.name, "description": s.description}
            for s in (card.skills or [])
        ],
    }


async def validate_applicant(applicant_id: str) -> str:
    client = await ClientFactory.connect(
        agent=SERVER_URL, client_config=_get_client_config()
    )
    msg = _build_message(applicant_id)
    async for item in client.send_message(msg):
        return _extract_text(item)
    return "(no response received)"


async def main(applicant_ids: list[str] | None = None) -> None:
    target_ids = applicant_ids or DEFAULT_APPLICANTS

    print("\n--- Agent Discovery (Google ADK) ---")
    try:
        info = await discover_agent()
    except httpx.ConnectError:
        print(f"ERROR: Cannot connect to server at {SERVER_URL}.")
        print("Start it first:  python server.py")
        sys.exit(1)

    print(f"  Name    : {info['name']}")
    print(f"  Version : {info['version']}")
    print(f"  URL     : {info['url']}")
    for skill in info["skills"]:
        print(f"    - {skill['name']}: {skill['description']}")

    for app_id in target_ids:
        print(f"\n--- Validating {app_id} ---")
        result = await validate_applicant(app_id)
        print(result)

    print("\n--- Done ---\n")


if __name__ == "__main__":
    ids = sys.argv[1:] if len(sys.argv) > 1 else None
    asyncio.run(main(ids))
