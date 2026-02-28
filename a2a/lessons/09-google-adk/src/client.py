"""
Lesson 09 — A2A client for the ThreatBriefing agent.

Discovers the agent via the A2A Agent Card endpoint, then sends a
threat-intel query through the A2A JSON-RPC protocol.

Usage (from lessons/09-google-adk/src/):
    python client.py                        # default CVE query
    python client.py "ssh vulnerabilities"  # custom query

Requires the server to be running first:
    python server.py

Required env vars: none (client talks to local A2A server only).
"""

# pylint: disable=wrong-import-position,wrong-import-order

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]

# ── Ensure venv packages are importable ──────────────────────────
_SRC = Path(__file__).parent.resolve()
sys.path.insert(0, str(_SRC))

from dotenv import find_dotenv, load_dotenv  # noqa: E402

load_dotenv(find_dotenv(raise_error_if_not_found=False))

try:
    import httpx  # noqa: E402
    from a2a.client import ClientConfig, ClientFactory  # noqa: E402
    from a2a.types import (  # noqa: E402
        Message,
        Part,
        Role,
        TextPart,
    )
except ImportError as exc:
    print(
        f"Import error: {exc}\n\n"
        "Make sure you activate the project virtual environment:\n"
        "  cd _examples/a2a\n"
        "  .venv\\Scripts\\Activate.ps1   (Windows)\n"
        "  source .venv/bin/activate       (macOS/Linux)\n"
        "  pip install -r requirements.txt\n"
    )
    sys.exit(1)

SERVER_URL = "http://localhost:10002"
DEFAULT_QUERY = "CVE-2024-3094 xz backdoor"


def _get_client_config() -> ClientConfig:
    """Create a fresh ClientConfig with a new httpx client (avoids closed loop issues)."""
    return ClientConfig(
        httpx_client=httpx.AsyncClient(timeout=120.0),
        streaming=False,
    )


# ─── Helpers ─────────────────────────────────────────────────────


async def discover_agent(base_url: str = SERVER_URL) -> dict:
    """Fetch and summarise the remote agent's A2A Agent Card."""
    client = await ClientFactory.connect(
        agent=base_url,
        client_config=_get_client_config(),
    )
    card = await client.get_card()
    return {
        "name": card.name,
        "version": getattr(card, "version", "n/a"),
        "description": card.description,
        "url": card.url,
        "skills": [
            {"id": s.id, "name": s.name, "tags": s.tags} for s in (card.skills or [])
        ],
    }


async def query_agent(
    query: str,
    base_url: str = SERVER_URL,
) -> str:
    """Send a threat-intel query via A2A and return the response."""
    client = await ClientFactory.connect(
        agent=base_url,
        client_config=_get_client_config(),
    )

    msg = Message(
        message_id="client-msg-001",
        role=Role.user,
        parts=[
            Part(root=TextPart(kind="text", text=query)),
        ],
    )

    async for item in client.send_message(msg):
        if isinstance(item, Message):
            texts = [p.root.text for p in item.parts if hasattr(p.root, "text")]
            if texts:
                return "\n".join(texts)

        # Handle (Task, Event) tuple — extract from last agent message
        if isinstance(item, tuple):
            task = item[0]
            if hasattr(task, "history") and task.history:
                for hist_msg in reversed(task.history):
                    if getattr(hist_msg, "role", None) != Role.agent:
                        continue
                    texts = [
                        p.root.text
                        for p in hist_msg.parts
                        if hasattr(p, "root")
                        and hasattr(p.root, "text")
                        and not (getattr(p.root, "metadata", None) or {}).get(
                            "adk_thought"
                        )
                    ]
                    if texts:
                        return "\n".join(texts)

        return f"(unhandled response: {type(item).__name__})"

    return "(no response received)"


async def main(query: str = DEFAULT_QUERY) -> None:
    """Run an end-to-end A2A demo: discover -> query -> display."""
    print("=" * 60)
    print("  A2A ThreatBriefing Client  (Lesson 09)")
    print("=" * 60)

    # Step 1: discover
    print("\n[1] Discovering agent ...")
    info = await discover_agent()
    print(f"    Name : {info['name']}")
    print(f"    URL  : {info['url']}")
    print(f"    Desc : {info['description'][:80]}...")
    for skill in info["skills"]:
        print(f"    Skill: {skill['name']}  tags={skill['tags']}")

    # Step 2: query
    print(f"\n[2] Querying: {query!r}")
    text = await query_agent(query)

    print("\n[3] Response:")
    print("-" * 60)
    print(text)
    print("-" * 60)


if __name__ == "__main__":
    import asyncio

    _cli_query = " ".join(sys.argv[1:]) or DEFAULT_QUERY  # pylint: disable=invalid-name
    asyncio.run(main(_cli_query))
