"""
Lesson 10 — A2A client for the LoanValidatorLangGraph server.

Usage (server on port 10003 must be running first):
    python client.py                     # validate all 3 applicants
    python client.py APP-2024-003        # validate a specific applicant
"""

# pylint: disable=wrong-import-position,wrong-import-order

from __future__ import annotations

import asyncio
import sys
from typing import Any
from uuid import uuid4

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(raise_error_if_not_found=False))

try:
    import httpx
    from a2a.client import A2ACardResolver, A2AClient
    from a2a.types import MessageSendParams, SendMessageRequest
except ImportError as _imp_err:
    print(
        f'ERROR: {_imp_err}\n\npip install "a2a-sdk[http-server]" httpx python-dotenv'
    )
    sys.exit(1)


SERVER_URL = "http://localhost:10003"
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
    """Discover the LangGraph-backed agent via A2A Agent Card."""
    async with httpx.AsyncClient(timeout=120.0) as httpx_client:
        _, card = await _create_client(httpx_client)
        return {
            "name": card.name,
            "description": card.description,
            "url": card.url,
            "version": getattr(card, "version", "n/a"),
            "skills": [{"id": s.id, "name": s.name} for s in (card.skills or [])],
        }


async def validate_applicant(applicant_id: str) -> str:
    """Send one validation request and return extracted response text."""
    async with httpx.AsyncClient(timeout=120.0) as httpx_client:
        client, _ = await _create_client(httpx_client)
        response = await client.send_message(_build_request(f"Validate {applicant_id}"))
        return _extract_text(response)


async def main(applicant_ids: list[str] | None = None) -> None:
    """Run discovery and validation flow for one or more applicant IDs."""
    target_ids = applicant_ids or DEFAULT_APPLICANTS
    print("\n--- Agent Discovery (LangGraph) ---")
    try:
        info = await discover_agent()
    except httpx.ConnectError:
        print(f"ERROR: Cannot connect to {SERVER_URL}. Start server first.")
        sys.exit(1)
    print(f"  Name: {info['name']}  Version: {info['version']}")
    for skill in info["skills"]:
        print(f"    - {skill['name']}")

    for app_id in target_ids:
        print(f"\n--- Validating {app_id} ---")
        print(await validate_applicant(app_id))

    print("\n--- Done ---\n")


if __name__ == "__main__":
    ids = sys.argv[1:] if len(sys.argv) > 1 else None
    asyncio.run(main(ids))
