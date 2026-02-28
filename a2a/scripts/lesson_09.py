#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
Lesson 09 — A2A with Google Agent Development Kit (ADK).

Interactive scenario: build a cybersecurity threat-intelligence agent
using Google ADK, expose it with the to_a2a() one-liner, and query
it via the A2A protocol.

Usage (from _examples/a2a/):
    python scripts/lesson_09.py

What this scenario covers:
  - Google ADK: LlmAgent, FunctionTool, Runner
  - LiteLlm model adapter: Azure Kimi-K2 without Vertex AI
  - to_a2a() one-liner: simplest A2A server integration
  - Full A2A round-trip: discover + query + response extraction
  - Cross-framework interop: same protocol as Lesson 08

Requirements:
  - AZURE_OPENAI_ENDPOINT, AZURE_AI_API_KEY in _examples/.env
  - .venv with google-adk[a2a] and litellm installed
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# ── Resolve paths ────────────────────────────────────────────────
SCRIPTS_DIR = Path(__file__).parent.resolve()
ROOT = SCRIPTS_DIR.parent  # _examples/a2a/
EXAMPLES = ROOT.parent  # _examples/
LESSON_SRC = ROOT / "lessons" / "09-google-adk" / "src"

sys.path.insert(0, str(LESSON_SRC))


# ── ANSI helpers ─────────────────────────────────────────────────
def _c(code: str, text: str) -> str:
    """Wrap text in an ANSI colour code."""
    return f"\033[{code}m{text}\033[0m"


def cyan(t: str) -> str:
    """Cyan ANSI colour."""
    return _c("36", t)


def green(t: str) -> str:
    """Green ANSI colour."""
    return _c("32", t)


def yellow(t: str) -> str:
    """Yellow ANSI colour."""
    return _c("33", t)


def red(t: str) -> str:
    """Red ANSI colour."""
    return _c("31", t)


def magenta(t: str) -> str:
    """Magenta ANSI colour."""
    return _c("35", t)


def bold(t: str) -> str:
    """Bold ANSI style."""
    return _c("1", t)


def dim(t: str) -> str:
    """Dim ANSI style."""
    return _c("2", t)


HR = dim("-" * 62)

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]


# ── Utilities ────────────────────────────────────────────────────
def _load_env() -> None:
    """Load key=value pairs from _examples/.env into os.environ."""
    env_file = EXAMPLES / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())


def _pause(prompt: str = "  Press Enter to continue...") -> None:
    """Pause execution and wait for the user to press Enter."""
    try:
        input(dim(prompt))
    except (EOFError, KeyboardInterrupt) as exc:
        print()
        raise SystemExit(0) from exc


def _print_cve_table(entries: list) -> None:
    """Render CVE entries as a summary table."""
    header = f"  {'CVE ID':<18} {'Severity':<12} " f"{'CVSS':<7} Title"
    print(header)
    print(f"  {'_'*18} {'_'*12} {'_'*7} {'_'*30}")
    for entry in entries:
        sev = entry.severity
        colour = red if sev == "CRITICAL" else (yellow if sev == "HIGH" else green)
        print(
            f"  {entry.cve_id:<18} "
            f"{colour(sev):<21} "
            f"{entry.cvss_score:<7} "
            f"{entry.title}"
        )
    print()


# ── Step functions ───────────────────────────────────────────────


def _step1_environment() -> None:
    """Check environment variables."""
    print(magenta("Step 1 -- Environment & Requirements"))
    _load_env()

    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    api_key = os.environ.get("AZURE_AI_API_KEY", "")
    model = os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME", "Kimi-K2")

    if not endpoint:
        print(red("  X  AZURE_OPENAI_ENDPOINT not set"))
        sys.exit(1)
    if not api_key:
        print(red("  X  AZURE_AI_API_KEY not set"))
        sys.exit(1)

    ep_short = endpoint[:55] + "..." if len(endpoint) > 55 else endpoint
    print(green(f"  OK AZURE_OPENAI_ENDPOINT  {dim(ep_short)}"))
    print(green(f"  OK AZURE_AI_API_KEY       {dim('[set]')}"))
    print(green(f"  OK Model                  {dim(model)}"))
    print()


def _step2_imports() -> None:
    """Verify Google ADK imports are available."""
    print(magenta("Step 2 -- Importing Google ADK"))
    try:
        from google.adk.agents import (  # pylint: disable=import-outside-toplevel
            LlmAgent,
        )
        from google.adk.models.lite_llm import (  # pylint: disable=import-outside-toplevel
            LiteLlm,
        )
        from google.adk.tools import (  # pylint: disable=import-outside-toplevel
            FunctionTool,
        )
        from google.adk.a2a.utils.agent_to_a2a import (  # pylint: disable=import-outside-toplevel
            to_a2a,
        )

        print(green("  OK google.adk.agents.LlmAgent"))
        print(green("  OK google.adk.models.lite_llm.LiteLlm"))
        print(green("  OK google.adk.tools.FunctionTool"))
        print(green("  OK google.adk.a2a...to_a2a"))
        _ = (LlmAgent, LiteLlm, FunctionTool, to_a2a)
    except ImportError as exc:
        print(red(f"  X  {exc}"))
        print('     pip install "google-adk[a2a]" litellm')
        sys.exit(1)
    print()
    _pause()


def _step3_knowledge_base() -> None:
    """Explore the threat intelligence data."""
    print(HR)
    print()
    print(magenta("Step 3 -- Threat Intelligence Knowledge Base"))
    print()
    print(dim("  Five synthetic CVE records:"))
    print()

    from knowledge_base import (  # type: ignore[import-not-found]  # pylint: disable=import-outside-toplevel,import-error
        THREAT_DB,
        search_threat_intel,
        get_cve_detail,
    )

    _print_cve_table(THREAT_DB)

    print(dim("  Testing search_threat_intel('ssh') ..."))
    for rec in search_threat_intel("ssh"):
        print(f"    -> {rec['cve_id']}  {rec['title']}")
    print()

    print(dim("  Testing get_cve_detail('CVE-2024-3094')..."))
    detail = get_cve_detail("CVE-2024-3094")
    if detail:
        print(f"    -> {detail['title']}")
        sev = detail["severity"]
        cvss = detail["cvss_score"]
        print(f"    -> {sev} (CVSS {cvss})")
    print()
    _pause()


def _step4_build_agent() -> None:
    """Build the ThreatBriefing agent."""
    print(HR)
    print()
    print(magenta("Step 4 -- Build the ThreatBriefing Agent"))
    print()
    print(dim("  Creating an LlmAgent with:"))
    print(dim("    - LiteLlm adapter (Azure Kimi-K2)"))
    print(dim("    - FunctionTool: search_threats"))
    print(dim("    - FunctionTool: lookup_cve"))
    print()

    from research_agent import build_research_agent  # type: ignore[import-not-found]  # pylint: disable=import-outside-toplevel,import-error

    try:
        agent = build_research_agent()
        print(green(f"  OK Agent: {dim(agent.name)}"))
        desc = (agent.description or "")[:55]
        print(green(f"  OK Desc:  {dim(desc)}..."))
        names = [t.name for t in (agent.tools or [])]  # type: ignore[union-attr]
        print(green(f"  OK Tools: {dim(', '.join(names))}"))
    except Exception as exc:  # pylint: disable=broad-exception-caught
        print(red(f"  X  Failed: {exc}"))
        sys.exit(1)
    print()
    _pause()


def _step5_comparison() -> None:
    """Compare server setup across frameworks."""
    print(HR)
    print()
    print(magenta("Step 5 -- The to_a2a() One-Liner"))
    print()
    print(bold("  Lesson 08 (Microsoft AF -- manual):"))
    print(dim("    executor = LoanValidatorExecutor()"))
    print(dim("    handler  = DefaultRequestHandler(...)"))
    print(dim("    server   = A2AStarletteApplication(...)"))
    print(dim("    app      = server.build()"))
    print(dim("    # ~50 lines of boilerplate"))
    print()
    print(bold("  Lesson 09 (Google ADK -- one-liner):"))
    print(cyan("    app = to_a2a(agent, port=10002)"))
    print(dim("    # That's it."))
    print()
    print(dim("  Both produce the same A2A endpoints:"))
    print(dim("    GET  /.well-known/agent-card.json"))
    print(dim("    POST /  (JSON-RPC)"))
    print()
    _pause()


def _step6_a2a_demo() -> None:
    """Live A2A server + client demo."""
    import asyncio as aio  # pylint: disable=import-outside-toplevel

    print(HR)
    print()
    print(magenta("Step 6 -- Live A2A Server & Client Demo"))
    print()
    _pause("  Press Enter to start the A2A server ...")
    print()

    proc = _start_a2a_server()
    if proc is None:
        print(red("  X  Server failed to start"))
        return

    print(green(f"  OK Server PID {proc.pid} on port 10002"))
    print()

    _step6a_discover(aio)
    _step6b_query(aio)

    _stop_a2a_server(proc)
    print(dim("  A2A server stopped."))
    print()


def _step6a_discover(aio) -> None:  # type: ignore[no-untyped-def]
    """Discover agent via A2A Agent Card."""
    print(magenta("  Step 6a -- Agent Discovery via A2A"))
    card_url = "http://localhost:10002/.well-known/agent-card.json"
    print(dim(f"  GET {card_url}"))
    print()

    try:
        from client import discover_agent  # type: ignore[import-not-found]  # pylint: disable=import-outside-toplevel,import-error

        info = aio.run(discover_agent())
        print(green(f"    Name : {info['name']}"))
        print(green(f"    URL  : {info['url']}"))
        desc = info["description"][:65]
        print(green(f"    Desc : {desc}..."))
        for skill in info.get("skills", []):
            tags = skill["tags"]
            print(green(f"    Skill: {skill['name']} {tags}"))
        print()
    except Exception as exc:  # pylint: disable=broad-exception-caught
        print(red(f"    X  Discovery failed: {exc}"))
        print()
    _pause()


def _step6b_query(aio) -> None:  # type: ignore[no-untyped-def]
    """Send threat queries via A2A protocol."""
    print()
    print(magenta("  Step 6b -- Threat Query via A2A"))

    queries = [
        "CVE-2024-3094 xz backdoor",
        "ssh vulnerabilities",
    ]

    for query in queries:
        print()
        print(dim(f"  Querying: {query!r}"))
        print()
        try:
            from client import query_agent  # type: ignore[import-not-found]  # pylint: disable=import-outside-toplevel,import-error,no-name-in-module

            result = aio.run(query_agent(query))
            print(cyan("    -- A2A Response --"))
            lines = result.splitlines()
            for line in lines[:25]:
                print(f"    {line}")
            if len(lines) > 25:
                extra = len(lines) - 25
                print(dim(f"    ... ({extra} more lines)"))
            print()
        except Exception as exc:  # pylint: disable=broad-exception-caught
            print(red(f"    X  Query failed: {exc}"))
            print()
        _pause()


def _step7_summary() -> None:
    """Cross-framework interop summary."""
    print(HR)
    print()
    print(magenta("Step 7 -- Cross-Framework Interop Summary"))
    print()
    box = [
        "+---------------------------------------------------+",
        "|  client.py (A2A SDK)                               |",
        "|       |  message/send (JSON-RPC)                   |",
        "|       v                                            |",
        "|  ThreatBriefing (port 10002, Google ADK)           |",
        "|       |  to_a2a() one-liner                        |",
        "|       v                                            |",
        "|  LoanValidator (port 10008, Microsoft AF)          |",
        "|       |  manual A2A wiring                         |",
        "|       v                                            |",
        "|  QAAgent (port 10001, A2A SDK)                     |",
        "+---------------------------------------------------+",
    ]
    for line in box:
        print(dim(f"  {line}"))
    print()
    print(dim("  Three agents, three frameworks, one protocol."))
    print(dim("  ADK's to_a2a() -- one line of code."))
    print()
    _pause("  Press Enter to exit ...")
    print()
    print(green(bold("  Lesson 09 complete!")))
    print(dim("  Next: Lesson 10 -- LangGraph Integration"))
    print()


# ── Main scenario ────────────────────────────────────────────────
def main() -> None:
    """Run the Lesson 09 interactive demonstration."""
    print()
    print(cyan(bold("===  Lesson 09 -- A2A with Google ADK  ===")))
    print(cyan("     ThreatBriefing: cyber intel via ADK + Kimi-K2"))
    print()

    _step1_environment()
    _step2_imports()
    _step3_knowledge_base()
    _step4_build_agent()
    _step5_comparison()
    _step6_a2a_demo()
    _step7_summary()


# ── A2A server lifecycle helpers ─────────────────────────────────


def _run_server() -> None:  # pylint: disable=too-many-locals
    """Entry point for the server subprocess."""
    import warnings  # pylint: disable=import-outside-toplevel

    # Suppress Google ADK experimental warnings (informational only)
    warnings.filterwarnings("ignore", category=UserWarning, module=r"google\.adk")

    import os as _os  # pylint: disable=import-outside-toplevel,reimported
    from pathlib import Path as _P  # pylint: disable=import-outside-toplevel,reimported

    env_file = _P(__file__).parent.parent.parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                _os.environ.setdefault(key.strip(), val.strip())

    src = _P(__file__).parent.parent / "lessons" / "09-google-adk" / "src"
    import sys as _sys  # pylint: disable=import-outside-toplevel,reimported

    _sys.path.insert(0, str(src))

    # Map env vars for litellm
    ep = _os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    ak = _os.environ.get("AZURE_AI_API_KEY", "")
    if ep:
        _os.environ.setdefault("AZURE_API_BASE", ep)
    if ak:
        _os.environ.setdefault("AZURE_API_KEY", ak)
    _os.environ.setdefault("AZURE_API_VERSION", "2025-04-01-preview")

    from research_agent import build_research_agent  # type: ignore[import-not-found]  # pylint: disable=import-outside-toplevel,import-error
    from google.adk.a2a.utils.agent_to_a2a import (  # pylint: disable=import-outside-toplevel
        to_a2a,
    )

    agent = build_research_agent()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        app = to_a2a(agent, host="localhost", port=10002)

    import uvicorn  # pylint: disable=import-outside-toplevel

    uvicorn.run(app, host="0.0.0.0", port=10002, log_level="warning")


def _start_a2a_server():  # type: ignore[no-untyped-def]
    """Start the A2A server in a background process."""
    import multiprocessing  # pylint: disable=import-outside-toplevel
    import time  # pylint: disable=import-outside-toplevel

    proc = multiprocessing.Process(target=_run_server, daemon=True)
    proc.start()

    import httpx  # pylint: disable=import-outside-toplevel

    url = "http://localhost:10002/.well-known/agent-card.json"
    for _ in range(45):
        time.sleep(1)
        try:
            if httpx.get(url, timeout=2.0).status_code == 200:
                return proc
        except (httpx.ConnectError, httpx.ReadTimeout):
            pass

    proc.terminate()
    return None


def _stop_a2a_server(proc) -> None:  # type: ignore[no-untyped-def]
    """Terminate the server subprocess."""
    if proc and proc.is_alive():
        proc.terminate()
        proc.join(timeout=5)


if __name__ == "__main__":
    main()
