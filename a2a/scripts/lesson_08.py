#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
Lesson 08 — A2A with Microsoft Agent Framework
Interactive scenario: build an orchestrator using Microsoft AF + Kimi-K2-Thinking
that validates loan applications via hard rules and LLM reasoning.

Usage (from _examples/a2a/):
    python scripts/lesson_08.py

What this scenario covers:
  - Microsoft Agent Framework: Agent class, tool decoration, chat client
  - Azure OpenAI: AzureOpenAIChatClient with API-key auth
  - Kimi-K2-Thinking: multi-step reasoning over structured evidence
  - Cross-framework A2A: OrchestratorAgent exposes itself as an A2A server
  - Tool calling: three tools for hard checks, soft checks, policy lookup

Requirements:
  - AZURE_OPENAI_ENDPOINT and AZURE_AI_API_KEY set in _examples/.env
  - .venv with agent-framework and agent-framework-azure-ai installed
    (python scripts/setup.py  or  pip install agent-framework agent-framework-azure-ai --pre)
  - (Optional) Lesson 06 server running on port 10001 for policy lookups
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# ── Resolve paths ────────────────────────────────────────────────
SCRIPTS_DIR = Path(__file__).parent.resolve()
ROOT = SCRIPTS_DIR.parent  # _examples/a2a/
EXAMPLES = ROOT.parent  # _examples/
LESSON_SRC = ROOT / "lessons" / "08-microsoft-agent-framework" / "src"

sys.path.insert(0, str(LESSON_SRC))


# ── ANSI colours ─────────────────────────────────────────────────
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


def white(t: str) -> str:
    """White/bright ANSI colour."""
    return _c("97", t)


HR = dim("─" * 62)

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]


# ── Load .env ────────────────────────────────────────────────────
def _load_env() -> None:
    """Load key=value pairs from _examples/.env into os.environ."""
    env_file = EXAMPLES / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())


def _pause(prompt: str = "  Press Enter to continue…") -> None:
    """Pause execution and wait for the user to press Enter."""
    try:
        input(dim(prompt))
    except (EOFError, KeyboardInterrupt) as exc:
        print()
        raise SystemExit(0) from exc


# ── Rule result table printer ────────────────────────────────────
def _print_rule_table(results: list[dict], label: str) -> None:
    """Render check results as a formatted table."""
    print(f"\n  {bold(label)}")
    print(f"  {'Rule':<33} {'Status':<22} {'Detail'}")
    print(f"  {'─'*33} {'─'*22} {'─'*30}")
    for r in results:
        if r["passed"]:
            sym = green("PASS ✓")
            sev = green(r["severity"])
        else:
            sym = red("FAIL ✗")
            sev = red(r["severity"].upper())
        rule = r["rule"]
        msg = r["message"][:60] + ("…" if len(r["message"]) > 60 else "")
        print(f"  {rule:<33} {sym} ({sev:<12}) {dim(msg)}")
    print()


# ── Applicant summary printer ─────────────────────────────────────
def _print_applicant(app, idx: int) -> None:
    """Print a compact applicant profile."""
    profile = app.to_dict()
    computed = profile["computed"]
    loan_type_label = f"{app.loan_type.upper()}"
    fthb = "Yes" if app.first_time_homebuyer else "No"
    loe = "Yes" if app.has_letter_of_explanation else "No"

    print(f"\n  {bold(f'Applicant {idx}: {app.full_name}')} ({dim(app.applicant_id)})")
    print(f"  {'Credit score':<28} {app.credit_score}")
    print(f"  {'Loan type':<28} {loan_type_label}")
    print(f"  {'Annual income':<28} ${app.annual_income_usd:>10,.0f}")
    print(f"  {'Loan amount':<28} ${app.loan_amount:>10,.0f}")
    print(f"  {'Property value':<28} ${app.property_value:>10,.0f}")
    print(f"  {'DTI ratio (computed)':<28} {computed['dti_ratio']:.1%}")
    print(f"  {'LTV ratio (computed)':<28} {computed['ltv_ratio']:.1%}")
    print(f"  {'Employment months':<28} {app.employment_months}")
    print(f"  {'Derogatory marks':<28} {app.derogatory_marks}")
    if app.derogatory_mark_notes:
        note = (
            (app.derogatory_mark_notes[:72] + "…")
            if len(app.derogatory_mark_notes) > 72
            else app.derogatory_mark_notes
        )
        print(f"  {'  Notes':<28} {dim(note)}")
    print(f"  {'First-time homebuyer':<28} {fthb}")
    print(f"  {'Has LOE':<28} {loe}")


# ── Main scenario ────────────────────────────────────────────────
def main() -> (
    None
):  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    """Run the Lesson 08 interactive demonstration."""
    print()
    print(cyan(bold("━━━  Lesson 08 — A2A with Microsoft Agent Framework  ━━━")))
    print(cyan("     Kimi-K2-Thinking orchestrates a loan pre-screening validator"))
    print()

    # ── Step 1: Environment ──────────────────────────────────────
    print(magenta("Step 1 — Environment & Requirements"))
    _load_env()

    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    api_key = os.environ.get("AZURE_AI_API_KEY", "")
    model = os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME", "Kimi-K2-Thinking")

    if not endpoint:
        print(red("  ❌ AZURE_OPENAI_ENDPOINT not set"))
        print("     Set AZURE_OPENAI_ENDPOINT in _examples/.env")
        sys.exit(1)
    if not api_key:
        print(red("  ❌ AZURE_AI_API_KEY not set"))
        print("     Set AZURE_AI_API_KEY in _examples/.env")
        sys.exit(1)

    ep_display = endpoint[:60] + "…" if len(endpoint) > 60 else endpoint
    print(green(f"  ✓  AZURE_OPENAI_ENDPOINT  {dim(ep_display)}"))
    print(green(f"  ✓  AZURE_AI_API_KEY       {dim('[set]')}"))
    print(green(f"  ✓  Model                  {dim(model)}"))
    print()

    # ── Step 2: Import check ────────────────────────────────────
    print(magenta("Step 2 — Importing Microsoft Agent Framework"))
    try:
        from agent_framework import Agent  # pylint: disable=import-outside-toplevel
        from agent_framework.azure import (  # pylint: disable=import-outside-toplevel
            AzureOpenAIChatClient,
        )

        print(
            green(
                f"  \u2713  agent_framework {Agent.__module__.split('.', maxsplit=1)[0]}"
            )
        )
        print(green(f"  \u2713  {AzureOpenAIChatClient.__name__}"))
    except ImportError as exc:
        print(red(f"  ❌ {exc}"))
        print(
            '     Run: pip install "agent-framework" "agent-framework-azure-ai" --pre'
        )
        sys.exit(1)

    print()
    _pause()

    # ── Step 3: What we're validating ───────────────────────────
    print(HR)
    print()
    print(magenta("Step 3 — Meet the Applicants"))
    print()
    print(dim("  Three loan applications with deliberately different risk profiles:"))
    print()

    from loan_data import APPLICANTS  # type: ignore[import-not-found]  # pylint: disable=import-outside-toplevel,import-error

    labels = [
        yellow("  1 — Alice Chen    (clean approve)"),
        red("  2 — Bob Kwan      (clear decline)"),
        cyan("  3 — Carol Martinez (edge case — FHA exceptions)"),
    ]
    for label, app in zip(labels, APPLICANTS):
        print(bold(label))
        _print_applicant(app, APPLICANTS.index(app) + 1)
        print()

    _pause()

    # ── Step 4: Build the orchestrator ──────────────────────────
    print(HR)
    print()
    print(magenta("Step 4 — Build OrchestratorAgent"))
    print()
    print(dim("  Creating an Agent with three tools:"))
    print(dim("    • run_hard_checks      — deterministic hard-fail rules"))
    print(dim("    • run_soft_checks      — advisory / compensating factor checks"))
    print(
        dim(
            "    • lookup_policy_notes  — policy lookup (A2A → QAAgent on :10001, or memo fallback)"
        )
    )
    print()

    from orchestrator import (  # type: ignore[import-not-found]  # pylint: disable=import-outside-toplevel,import-error
        OrchestratorAgent,
    )

    try:
        orchestrator = OrchestratorAgent()
        print(green(f"  ✓  Agent built — model: {dim(model)}"))
    except Exception as exc:  # pylint: disable=broad-exception-caught
        print(red(f"  ❌ Failed to build agent: {exc}"))
        sys.exit(1)

    print()
    _pause()

    # ── Step 5: Validate all three applications ──────────────────
    from validation_rules import (  # type: ignore[import-not-found]  # pylint: disable=import-outside-toplevel,import-error
        run_hard_checks as _hc,
        run_soft_checks as _sc,
    )

    for idx, app in enumerate(APPLICANTS, 1):
        print(HR)
        print()
        case_labels = ["Clean Approve", "Clear Decline", "Edge Case — FHA Exceptions"]
        print(
            magenta(
                f"Step 5.{idx} — Validating: {bold(app.full_name)}  [{case_labels[idx-1]}]"
            )
        )
        print()

        # Show deterministic results first
        hard_json = json.loads(_hc(json.dumps(app.to_dict())))
        soft_json = json.loads(_sc(json.dumps(app.to_dict())))
        _print_rule_table(hard_json, "Hard-fail rule checks")
        _print_rule_table(soft_json, "Soft advisory checks")

        # Run the full orchestrator
        if idx == 3:
            print(dim("  ⏳ Kimi-K2-Thinking is reasoning through FHA exceptions…"))
            print(
                dim(
                    "     (this is the hard part — conflicting signals require careful analysis)"
                )
            )
            print()

        print(dim("  ⏳ Running OrchestratorAgent.validate() …"))
        try:
            import asyncio as _aio_validate  # pylint: disable=import-outside-toplevel

            report = _aio_validate.run(orchestrator.validate(app))
        except Exception as exc:  # pylint: disable=broad-exception-caught
            print(red(f"  ❌ Validation failed: {exc}"))
            _pause()
            continue

        # Print report
        verdict_colour = {
            "APPROVED": green,
            "NEEDS_REVIEW": yellow,
            "DECLINED": red,
        }.get(report.verdict, white)

        print()
        print(verdict_colour(str(report)))
        print()

        if idx < len(APPLICANTS):
            _pause()

    # ── Step 6: A2A server + client demo ────────────────────────
    print(HR)
    print()
    print(magenta("Step 6 — Expose as an A2A Server & Connect via A2A Client"))
    print()
    print(
        dim("  Now we demonstrate the key A2A capability: wrap the OrchestratorAgent")
    )
    print(dim("  in an A2A server (port 10008) and connect to it using a standard"))
    print(dim("  A2A client — the same SDK used in Lesson 07."))
    print()
    print(dim("  This means any agent framework (LangGraph, CrewAI, Google ADK …)"))
    print(dim("  can call the validator without knowing anything about Microsoft AF."))
    print()
    _pause("  Press Enter to start the A2A server …")
    print()

    import asyncio as _async  # pylint: disable=import-outside-toplevel

    server_proc = _start_a2a_server()
    if server_proc is None:
        print(red("  ❌ Failed to start A2A server — skipping A2A demo"))
    else:
        print(green(f"  ✓  A2A server running (PID {server_proc.pid}) on port 10008"))
        print()

        # ── Step 6a: discover via A2A ────────────────────────────
        print(magenta("  Step 6a — Agent Discovery via A2A"))
        print(dim("  GET http://localhost:10008/.well-known/agent-card.json"))
        print()

        try:
            from client import (  # type: ignore[import-not-found]  # pylint: disable=import-outside-toplevel,import-error
                discover_agent,
            )

            card_info = _async.run(discover_agent())
            print(green(f"    Name    : {card_info['name']}"))
            print(green(f"    Version : {card_info['version']}"))
            print(green(f"    URL     : {card_info['url']}"))
            for skill in card_info.get("skills", []):
                print(green(f"    Skill   : {skill['name']} — {skill['description']}"))
            print()
        except Exception as exc:  # pylint: disable=broad-exception-caught
            print(red(f"    ❌ Discovery failed: {exc}"))
            print()

        _pause()

        # ── Step 6b: validate via A2A ────────────────────────────
        print()
        print(magenta("  Step 6b — Validate Applicant via A2A Protocol"))
        print(dim("  Sending Carol Martinez (edge case) through A2A JSON-RPC …"))
        print()

        try:
            from client import (  # type: ignore[import-not-found]  # pylint: disable=import-outside-toplevel,import-error
                validate_applicant,
            )

            result = _async.run(validate_applicant("APP-2024-003"))
            print(cyan("    ── A2A Response ──"))
            for line in result.splitlines():
                print(f"    {line}")
            print()
        except Exception as exc:  # pylint: disable=broad-exception-caught
            print(red(f"    ❌ A2A validation failed: {exc}"))
            print()

        # Shut down the server
        _stop_a2a_server(server_proc)
        print(dim("  A2A server stopped."))
        print()

    # ── Step 7: Summary ──────────────────────────────────────────
    print(HR)
    print()
    print(magenta("Step 7 — A2A Interoperability Summary"))
    print()
    print(dim("  ┌─────────────────────────────────────────────────────────┐"))
    print(dim("  │  Any A2A Client                                        │"))
    print(dim("  │       │  tasks/send (JSON-RPC)                         │"))
    print(dim("  │       ▼                                                │"))
    print(dim("  │  LoanValidator (port 10008, Microsoft AF)              │"))
    print(dim("  │       │  lookup_policy_notes (A2A call)                │"))
    print(dim("  │       ▼                                                │"))
    print(dim("  │  QAAgent (port 10001, A2A SDK)                         │"))
    print(dim("  └─────────────────────────────────────────────────────────┘"))
    print()
    print(dim("  The framework used to build each agent is invisible to the"))
    print(dim("  A2A protocol consumer.  That's the core A2A promise."))
    print()

    _pause("  Press Enter to exit …")
    print()
    print(green(bold("  Lesson 08 complete!")))
    print(dim("  Next: Lesson 09 — Google Agent Development Kit (ADK)"))
    print()


# ─── A2A server lifecycle helpers ─────────────────────────────────


def _run_server() -> None:
    """Entry point for the server subprocess."""
    import os as _os  # pylint: disable=import-outside-toplevel,reimported
    from pathlib import (  # pylint: disable=import-outside-toplevel,reimported
        Path as _Path,
    )

    # Load .env
    env_file = _Path(__file__).parent.parent.parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                _os.environ.setdefault(key.strip(), val.strip())

    src = (
        _Path(__file__).parent.parent
        / "lessons"
        / "08-microsoft-agent-framework"
        / "src"
    )
    import sys as _sys  # pylint: disable=import-outside-toplevel,reimported

    _sys.path.insert(0, str(src))

    import uvicorn  # pylint: disable=import-outside-toplevel

    from server import server as starlette_app  # type: ignore[import-not-found]  # pylint: disable=import-outside-toplevel,import-error  # noqa: E501

    uvicorn.run(
        starlette_app.build(),
        host="0.0.0.0",
        port=10008,
        log_level="warning",
    )


def _start_a2a_server():  # type: ignore[no-untyped-def]
    """Start the A2A server in a background process. Return the Process or None."""
    import multiprocessing  # pylint: disable=import-outside-toplevel
    import time  # pylint: disable=import-outside-toplevel

    proc = multiprocessing.Process(target=_run_server, daemon=True)
    proc.start()

    # Wait for the server to become reachable
    import httpx  # pylint: disable=import-outside-toplevel

    for _ in range(30):
        time.sleep(1)
        try:
            r = httpx.get(
                "http://localhost:10008/.well-known/agent-card.json",
                timeout=2.0,
            )
            if r.status_code == 200:
                return proc
        except (httpx.ConnectError, httpx.ReadTimeout):
            pass

    # Server didn't start in time
    proc.terminate()
    return None


def _stop_a2a_server(proc) -> None:  # type: ignore[no-untyped-def]
    """Terminate the server subprocess."""
    if proc and proc.is_alive():
        proc.terminate()
        proc.join(timeout=5)


if __name__ == "__main__":
    main()
