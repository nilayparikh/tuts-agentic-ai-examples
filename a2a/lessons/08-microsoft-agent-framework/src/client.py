"""
Lesson 08 — A2A client for the LoanValidatorOrchestrator server.

Demonstrates the full A2A protocol round-trip:
  1. Discover the agent via GET /.well-known/agent-card.json
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
from typing import Any  # noqa: E402
from uuid import uuid4  # noqa: E402

try:
    import httpx  # noqa: E402
    from a2a.client import (  # noqa: E402
        A2ACardResolver,
        A2AClient,
    )
    from a2a.types import (  # noqa: E402
        MessageSendParams,
        SendMessageRequest,
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


async def discover_agent() -> dict:
    """Discover the LoanValidatorOrchestrator via A2A Agent Card."""
    async with httpx.AsyncClient(timeout=120.0) as httpx_client:
        _, card = await _create_client(httpx_client)
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
    async with httpx.AsyncClient(timeout=120.0) as httpx_client:
        client, _ = await _create_client(httpx_client)
        response = await client.send_message(_build_request(f"Validate {applicant_id}"))
        return _extract_text(response)


async def main(applicant_ids: list[str] | None = None) -> None:
    """Run the A2A client demo against LoanValidatorOrchestrator."""
    target_ids = applicant_ids or DEFAULT_APPLICANTS

    # Step 1: Discover
    print("\n--- Agent Discovery ---")
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
        print(f"    - {skill['name']}: {skill['description']}")

    # Step 2: Validate each applicant via A2A
    for app_id in target_ids:
        print(f"\n--- Validating {app_id} ---")
        result = await validate_applicant(app_id)
        print(result)

    print("\n--- Done ---\n")


if __name__ == "__main__":
    ids = sys.argv[1:] if len(sys.argv) > 1 else None
    asyncio.run(main(ids))
