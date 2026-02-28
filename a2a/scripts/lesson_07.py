#!/usr/bin/env python3
"""
Lesson 07 — A2A Client Fundamentals
Interactive scenario: discover, connect, query, and stream an A2A agent.

Usage (from _examples/a2a/):
    python scripts/lesson_07.py

What this scenario covers:
  - Discover agent with A2ACardResolver
  - Blocking request with A2AClient.send_message()
  - Streaming request with A2AClient.send_message_streaming()
  - Graceful error handling (JSON-RPC + connection errors)
  - Interactive Q&A loop

Requirements:
  - Lesson 06 server running on http://localhost:10001
    → python scripts/lesson_06.py   (in a separate terminal)
"""
from __future__ import annotations

import asyncio
import os
import sys
import warnings
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.resolve()
ROOT = SCRIPTS_DIR.parent
EXAMPLES = ROOT.parent


# ── ANSI colours ─────────────────────────────────────────────────
def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m"


def cyan(t):
    """Wrap text in cyan ANSI colour."""
    return _c("36", t)


def green(t):
    """Wrap text in green ANSI colour."""
    return _c("32", t)


def yellow(t):
    """Wrap text in yellow ANSI colour."""
    return _c("33", t)


def red(t):
    """Wrap text in red ANSI colour."""
    return _c("31", t)


def magenta(t):
    """Wrap text in magenta ANSI colour."""
    return _c("35", t)


def bold(t):
    """Wrap text in bold ANSI style."""
    return _c("1", t)


def dim(t):
    """Wrap text in dim ANSI style."""
    return _c("2", t)


def white(t):
    """Wrap text in white ANSI colour."""
    return _c("97", t)


HR = dim("─" * 60)

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]


# ── Load .env ────────────────────────────────────────────────────
def _load_env() -> None:
    env_file = EXAMPLES / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())


def _pause(prompt: str = "  Press Enter to continue...") -> None:
    try:
        input(dim(prompt))
    except (EOFError, KeyboardInterrupt) as exc:
        print()
        raise SystemExit(0) from exc


# ── Response helpers (a2a-sdk v0.3.x) ────────────────────────────
def _extract_text(response) -> str:
    """Extract text from a Message response (a2a-sdk v0.3.x).

    message/send returns a Message at response.root.result.
    Each part is a discriminated union accessed via part.root.
    """
    try:
        msg = response.root.result
    except AttributeError:
        return f"(unexpected shape — {type(response).__name__})"

    texts = [
        part.root.text
        for part in msg.parts
        if getattr(part.root, "kind", None) == "text"
    ]
    return "\n".join(texts) if texts else "(no text in response)"


async def _safe_query(client, question: str, build_request_fn) -> str:
    """Send a question and return answer text or a structured error string."""
    import httpx  # pylint: disable=import-outside-toplevel

    try:
        req = build_request_fn(question)
        resp = await client.send_message(req)

        root = getattr(resp, "root", None)
        if root is not None and hasattr(root, "error") and root.error:
            err = root.error
            return f"[Error {getattr(err, 'code', '?')}] {getattr(err, 'message', err)}"

        return _extract_text(resp)
    except httpx.ConnectError:
        return "[Connection Error] Is the server running? → python scripts/lesson_06.py"
    except Exception as exc:  # pylint: disable=broad-exception-caught
        return f"[{type(exc).__name__}] {exc}"


# ── Main scenario ────────────────────────────────────────────────
async def main() -> None:
    """Run the Lesson 07 interactive A2A client scenario."""
    _load_env()

    print()
    print(cyan(bold("━━━  Lesson 07 — A2A Client Fundamentals  ━━━")))
    print(cyan("     Discover · Request · Stream · Handle Errors"))
    print()

    # Check SDK deps
    try:
        import httpx  # pylint: disable=import-outside-toplevel
        from a2a.client import (  # pylint: disable=import-outside-toplevel
            A2ACardResolver,
            A2AClient,
        )
        from a2a.types import (  # pylint: disable=import-outside-toplevel
            MessageSendParams,
            SendMessageRequest,
            SendStreamingMessageRequest,
        )
        from uuid import uuid4  # pylint: disable=import-outside-toplevel
    except ImportError as exc:
        print(red(f"  ❌ Missing package: {exc}"))
        print('     Run: pip install "a2a-sdk[http-server]" httpx')
        sys.exit(1)

    warnings.filterwarnings("ignore", category=DeprecationWarning)

    BASE_URL = "http://localhost:10001"  # pylint: disable=invalid-name

    # ── Helper to build requests ──────────────────────────────────
    def build_request(question: str) -> SendMessageRequest:
        return SendMessageRequest(
            id=str(uuid4()),
            params=MessageSendParams(
                **{  # type: ignore[arg-type]
                    "message": {
                        "role": "user",
                        "parts": [{"kind": "text", "text": question}],
                        "messageId": uuid4().hex,
                    }
                }
            ),
        )

    def build_streaming_request(question: str) -> SendStreamingMessageRequest:
        return SendStreamingMessageRequest(
            id=str(uuid4()),
            params=MessageSendParams(
                **{  # type: ignore[arg-type]
                    "message": {
                        "role": "user",
                        "parts": [{"kind": "text", "text": question}],
                        "messageId": uuid4().hex,
                    }
                }
            ),
        )

    # ── Step 1: Discover Agent Card ───────────────────────────────
    print(magenta("Step 1 — Discover the Agent Card"))
    print(dim(f"  Fetching {BASE_URL}/.well-known/agent.json ..."))
    print()

    try:
        async with httpx.AsyncClient(timeout=10.0) as hc:
            resolver = A2ACardResolver(httpx_client=hc, base_url=BASE_URL)
            agent_card = await resolver.get_agent_card()
    except httpx.ConnectError:
        print(red(f"  ❌ Cannot reach {BASE_URL}"))
        print()
        print("     Start the server first (in a separate terminal):")
        print(f"     {yellow('python scripts/lesson_06.py')}")
        sys.exit(1)

    print(green("  ✅ Agent Card received"))
    print(f"     Name:       {bold(agent_card.name)}")
    print(f"     Version:    {agent_card.version}")
    print(f"     Streaming:  {agent_card.capabilities.streaming}")
    print(f"     Skills:     {[s.name for s in agent_card.skills]}")
    print()
    _pause()

    # Keep a persistent httpx client for the rest of the session
    http_client = httpx.AsyncClient(timeout=60.0)
    client = A2AClient(httpx_client=http_client, agent_card=agent_card)

    try:
        # ── Step 2: Blocking call ─────────────────────────────────
        print(magenta("Step 2 — Blocking request (message/send)"))
        print(dim("  Sends a question and waits for the complete response."))
        print()

        q = "What is the annual deductible?"
        print(f"  {yellow('❓')} {q}")
        response = await client.send_message(build_request(q))

        msg = response.root.result  # type: ignore[union-attr]
        print(green(f"  ✅ Message ID: {msg.message_id}"))  # type: ignore[union-attr]
        print(f"     Role: {msg.role.value}  |  Kind: {msg.kind}")  # type: ignore[union-attr]
        print()
        for part in msg.parts:  # type: ignore[union-attr]
            if part.root.kind == "text":
                for line in part.root.text.strip().splitlines():  # type: ignore[union-attr]
                    print(f"     {line}")
        print()
        _pause()

        # ── Step 3: Multiple questions ────────────────────────────
        print(magenta("Step 3 — Multiple blocking questions"))
        print()

        demo_q = [
            "How much is the monthly premium?",
            "Are cosmetic procedures covered?",
            "How do I file a claim?",
            "What is the meaning of life?",  # out-of-scope — should say "not in document"
        ]

        for question in demo_q:
            print(f"  {yellow('❓')} {question}")
            answer = await _safe_query(client, question, build_request)
            for line in answer.strip().splitlines():
                print(f"     {line}")
            print()

        print(HR)
        _pause()

        # ── Step 4: Streaming ─────────────────────────────────────
        print(magenta("Step 4 — Streaming request (message/stream)"))
        print(dim("  Returns partial tokens as Server-Sent Events (SSE)."))
        print(dim("  Useful for real-time UIs — you see text arrive incrementally."))
        print()

        stream_q = "Explain the claims process step by step."
        print(f"  {yellow('❓')} {stream_q}")
        print()
        print(dim("  Streaming events:"))

        async for event in client.send_message_streaming(
            build_streaming_request(stream_q)
        ):
            event_type = type(event).__name__
            root = getattr(event, "root", event)
            result = getattr(root, "result", None)
            if result is None:
                continue

            parts_iter = None
            if hasattr(result, "parts"):
                parts_iter = result.parts
            elif hasattr(result, "status") and result.status and result.status.message:
                parts_iter = result.status.message.parts

            if parts_iter:
                for part in parts_iter:
                    pr = getattr(part, "root", part)
                    if getattr(pr, "kind", None) == "text":
                        preview = pr.text[:100].replace("\n", " ")
                        ellipsis = "..." if len(pr.text) > 100 else ""
                        print(f"  [{dim(event_type)}] {preview}{ellipsis}")

        print()
        print(green("  ✅ Streaming complete"))
        print()
        _pause()

        # ── Step 5: Error handling ────────────────────────────────
        print(magenta("Step 5 — Error handling"))
        print(dim("  A2A uses JSON-RPC error codes:"))
        print(
            dim("  -32700 Parse error  -32600 Invalid request  -32601 Method not found")
        )
        print(dim("  -32001 Task not found  -32002 Task not cancelable"))
        print()

        answer = await _safe_query(
            client, "What medications are excluded?", build_request
        )
        print(f"  {yellow('❓')} What medications are excluded?")
        for line in answer.strip().splitlines():
            print(f"     {line}")
        print()
        print(green("  ✅ Error handling works (connection errors, JSON-RPC errors)"))
        print()
        _pause()

        # ── Step 6: Interactive Q&A ───────────────────────────────
        print(magenta("Step 6 — Interactive mode"))
        print(dim("  Ask anything about the ACME Insurance policy."))
        print(dim("  The agent can only answer from the loaded document."))
        print(dim("  Type 'quit' or press Ctrl+C to exit."))
        print()

        while True:
            try:
                question = input(cyan("  ❓ Your question: ")).strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if not question:
                continue
            if question.lower() in {"quit", "exit", "q"}:
                break

            print()
            answer = await _safe_query(client, question, build_request)
            for line in answer.strip().splitlines():
                print(f"  {line}")
            print()

    finally:
        await http_client.aclose()

    print()
    print(green("✅ Lesson 07 complete"))
    print(dim("   You've completed the full A2A loop: Agent → Server → Client"))
    print()


if __name__ == "__main__":
    asyncio.run(main())
