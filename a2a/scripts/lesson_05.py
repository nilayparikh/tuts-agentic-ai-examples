#!/usr/bin/env python3
"""
Lesson 05 — Building Your First A2A Agent
Interactive scenario: standalone QA agent powered by GitHub Phi-4.

Usage (from _examples/a2a/):
    python scripts/lesson_05.py

What this scenario covers:
  - Load .env and verify GITHUB_TOKEN
  - Configure OpenAI-compatible GitHub Models client
  - Load domain knowledge (insurance policy)
  - Build and run the QAAgent class
  - Interactive Q&A loop
"""
from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

# ── Resolve paths ────────────────────────────────────────────────
SCRIPTS_DIR = Path(__file__).parent.resolve()
ROOT = SCRIPTS_DIR.parent  # _examples/a2a/
EXAMPLES = ROOT.parent  # _examples/
LESSON_SRC = ROOT / "lessons" / "05-first-a2a-agent" / "src"

# Add lesson 05 src so we can import QAAgent
sys.path.insert(0, str(LESSON_SRC))


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


HR = dim("─" * 60)

# ── Reconfigure stdout for Windows ───────────────────────────────
sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]


# ── Load .env ────────────────────────────────────────────────────
def _load_env() -> None:
    """Load .env variables from the _examples/ root, if present."""
    env_file = EXAMPLES / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())


# ── Main scenario ────────────────────────────────────────────────
async def main() -> None:
    print()
    print(cyan(bold("━━━  Lesson 05 — Building Your First A2A Agent  ━━━")))
    print(cyan("     Standalone QA Agent · GitHub Phi-4"))
    print()

    # ── Step 1: Environment ──────────────────────────────────────
    print(magenta("Step 1 — Environment"))
    _load_env()

    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print(red("  ❌ GITHUB_TOKEN not set"))
        print("     Edit _examples/.env → GITHUB_TOKEN=ghp_your_token_here")
        print("     https://github.com/settings/tokens")
        sys.exit(1)
    print(green(f"  ✅ GITHUB_TOKEN set ({token[:8]}...)"))
    print()

    # ── Step 2: Import and configure client ──────────────────────
    print(magenta("Step 2 — Configuring GitHub Models client (Phi-4)"))
    try:
        from openai import AsyncOpenAI  # pylint: disable=import-outside-toplevel

        client = AsyncOpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=token,
        )
        print(green(f"  ✅ Client ready → {client.base_url}"))
    except ImportError:
        print(red("  ❌ openai package not found — run: pip install openai"))
        sys.exit(1)
    print()

    # ── Step 3: Load domain knowledge ────────────────────────────
    print(magenta("Step 3 — Loading domain knowledge"))
    from qa_agent import QAAgent, load_knowledge  # type: ignore[import-not-found]  # pylint: disable=import-error,import-outside-toplevel

    knowledge_path = str(LESSON_SRC / "data" / "insurance_policy.txt")
    knowledge = load_knowledge(knowledge_path)
    print(green(f"  ✅ Loaded {len(knowledge):,} chars from insurance_policy.txt"))
    print()

    # ── Step 4: Create agent ──────────────────────────────────────
    print(magenta("Step 4 — Creating QAAgent"))
    agent = QAAgent(knowledge_path, model="Phi-4", temperature=0.2)
    print(green("  ✅ QAAgent ready"))
    print(
        dim("     model=Phi-4  temperature=0.2  knowledge injected into system prompt")
    )
    print()

    # ── Step 5: Demo questions ────────────────────────────────────
    print(magenta("Step 5 — Running demo questions"))
    print(HR)

    demo_questions = [
        "What is the deductible for the Standard plan?",
        "Are cosmetic procedures covered?",
        "How do I file a claim?",
    ]

    for q in demo_questions:
        print(f"  {yellow('❓')} {q}")
        answer = await agent.query(q)
        for line in answer.strip().splitlines():
            print(f"     {line}")
        print()

    print(HR)
    print()

    # ── Step 6: Interactive REPL ──────────────────────────────────
    print(magenta("Step 6 — Interactive mode"))
    print(
        dim("  Type a question and press Enter.  Type 'quit' or press Ctrl+C to exit.")
    )
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
        try:
            answer = await agent.query(question)
            for line in answer.strip().splitlines():
                print(f"  {line}")
        except Exception as exc:  # pylint: disable=broad-exception-caught
            print(red(f"  ❌ Error: {exc}"))
        print()

    print()
    print(green("✅ Lesson 05 complete"))
    print(dim("   Next → python scripts/lesson_06.py  (start A2A server)"))
    print()


if __name__ == "__main__":
    asyncio.run(main())
