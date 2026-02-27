#!/usr/bin/env python3
"""
Lesson 06 — A2A Server
Interactive scenario: wrap QAAgent as a full A2A-compliant server.

Usage (from _examples/a2a/):
    python scripts/lesson_06.py

What this scenario covers:
  - Agent Card: name, description, skills, capabilities
  - AgentExecutor: bridges QAAgent to the A2A protocol
  - A2AStarletteApplication: serves JSON-RPC on port 10001
  - Endpoints:  GET /.well-known/agent.json  |  POST /
  - Server runs until Ctrl+C

Requirements:
  - GITHUB_TOKEN set in _examples/.env
  - .venv with a2a-sdk installed (python scripts/setup.py)
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# ── Resolve paths ────────────────────────────────────────────────
SCRIPTS_DIR = Path(__file__).parent.resolve()
ROOT = SCRIPTS_DIR.parent  # _examples/a2a/
EXAMPLES = ROOT.parent  # _examples/
SERVER_SRC = ROOT / "lessons" / "06-a2a-server" / "src"
LESSON_SRC05 = ROOT / "lessons" / "05-first-a2a-agent" / "src"

sys.path.insert(0, str(SERVER_SRC))
sys.path.insert(0, str(LESSON_SRC05))

SERVER_PORT = 10001


# ── ANSI colours ─────────────────────────────────────────────────
def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m"


cyan = lambda t: _c("36", t)
green = lambda t: _c("32", t)
yellow = lambda t: _c("33", t)
red = lambda t: _c("31", t)
magenta = lambda t: _c("35", t)
bold = lambda t: _c("1", t)
dim = lambda t: _c("2", t)

HR = dim("─" * 60)

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


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
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)


# ── Main scenario ────────────────────────────────────────────────
def main() -> None:
    print()
    print(cyan(bold("━━━  Lesson 06 — A2A Server  ━━━")))
    print(cyan("     QAAgent wrapped as a fully A2A-compliant API"))
    print()

    # ── Step 1: Environment ──────────────────────────────────────
    print(magenta("Step 1 — Environment"))
    _load_env()

    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print(red("  ❌ GITHUB_TOKEN not set"))
        print("     Edit _examples/.env → GITHUB_TOKEN=ghp_your_token_here")
        sys.exit(1)
    print(green(f"  ✅ GITHUB_TOKEN set ({token[:8]}...)"))
    print()

    # ── Step 2: Explain the Agent Card ───────────────────────────
    print(magenta("Step 2 — Agent Card"))
    print(dim("  Every A2A agent advertises itself via a JSON document at"))
    print(dim("  GET /.well-known/agent.json  (the discovery endpoint)"))
    print()
    print(dim("  This server's Agent Card:"))
    print(f"    {dim('name')}         QAAgent")
    print(f"    {dim('version')}      1.0.0")
    print(f"    {dim('url')}          http://localhost:{SERVER_PORT}/")
    print(f"    {dim('streaming')}    true")
    print(
        f"    {dim('skill')}        policy-qa — answer questions about insurance policy docs"
    )
    print()
    _pause()

    # ── Step 3: Explain the AgentExecutor ────────────────────────
    print(magenta("Step 3 — AgentExecutor"))
    print(dim("  QAAgentExecutor bridges your QAAgent to the A2A protocol:"))
    print()
    print(dim("  ┌──────────────────┐   execute()   ┌──────────────────┐"))
    print(dim("  │  A2A SDK Request │ ──────────────▶│  QAAgent.query() │"))
    print(dim("  │  (JSON-RPC)      │               │  (GitHub Phi-4)  │"))
    print(dim("  └──────────────────┘   ◀──────────── └──────────────────┘"))
    print(dim("                event_queue.enqueue_event(answer)"))
    print()
    _pause()

    # ── Step 4: Explain the server stack ─────────────────────────
    print(magenta("Step 4 — Server Stack"))
    print(dim("  A2AStarletteApplication builds an ASGI app:"))
    print()
    print(dim("  client HTTP POST /"))
    print(dim("    → DefaultRequestHandler   (routes JSON-RPC methods)"))
    print(dim("    → QAAgentExecutor.execute()"))
    print(dim("    → EventQueue → SSE stream or single response"))
    print()
    print(dim("  Run with uvicorn on 0.0.0.0:10001"))
    print()
    _pause()

    # ── Step 5: Start server ──────────────────────────────────────
    print(magenta("Step 5 — Starting Server"))
    print()
    print(green(f"  🚀 QAAgent A2A Server"))
    print(f"     Listening on:  {bold(f'http://localhost:{SERVER_PORT}')}")
    print(
        f"     Agent Card:    {bold(f'http://localhost:{SERVER_PORT}/.well-known/agent.json')}"
    )
    print(f"     JSON-RPC:      {bold(f'POST http://localhost:{SERVER_PORT}')}")
    print()
    print(dim("  Keep this terminal open."))
    print(dim("  Run  python scripts/lesson_07.py  in a second terminal to connect."))
    print(dim("  Press Ctrl+C to stop the server."))
    print()
    print(HR)
    print()

    try:
        # Determine the venv Python to use for running server.py
        venv_python = (
            ROOT
            / ".venv"
            / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        )
        python_exe = str(venv_python) if venv_python.exists() else sys.executable

        result = subprocess.run(
            [python_exe, "server.py"],
            cwd=SERVER_SRC,
        )
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print()
        print()
        print(HR)
        print(green("  ✅ Server stopped"))
        print()


if __name__ == "__main__":
    main()
