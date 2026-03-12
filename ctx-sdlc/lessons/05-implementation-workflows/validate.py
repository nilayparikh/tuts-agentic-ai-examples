#!/usr/bin/env python3
"""Lesson 05 — Validation script.

Tests role-separated agent behavior vs. single-agent approach.
"""
import argparse
import sys
from pathlib import Path

LESSON_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(LESSON_DIR.parent.parent / "scripts"))
sys.path.insert(0, str(LESSON_DIR))
from setup_utils import run_copilot, print_result, ensure_output_dir, MODEL_HEAVY
from default import setup as setup_workspace

SCENARIOS = {
    "single-agent": {
        "name": "Scenario 1 — Single Agent (no role separation)",
        "prompt": (
            "Add a new fraud-alert mandatory notification event to the "
            "Loan Workbench. Write the business rule, update the route "
            "handler, add tests, and review your own changes."
        ),
        "custom_instructions": False,
    },
    "tdd-first": {
        "name": "Scenario 2 — TDD Handoff (tester writes failing tests first)",
        "prompt": (
            "#file:specs/non-functional-requirements.md "
            "#file:src/backend/src/rules/mandatory-events.ts\n\n"
            "Write failing tests that verify: when a new fraud-alert "
            "mandatory event is added, users without it in their "
            "preferences get it auto-enabled on next GET. Include: "
            "1) happy-path test, 2) FALSE POSITIVE test, 3) HARD NEGATIVE test."
        ),
        "custom_instructions": True,
    },
    "implementer": {
        "name": "Scenario 3 — Implementer makes tests pass",
        "prompt": (
            "#file:docs/implementation-playbook.md\n\n"
            "The tester wrote 3 failing tests for the fraud-alert "
            "mandatory event. Make minimal changes to pass all 3 tests. "
            "Do NOT modify test files. Call writeAuditEntry() BEFORE "
            "persisting any change."
        ),
        "custom_instructions": True,
    },
}


def run_scenario(key: str, model: str) -> None:
    s = SCENARIOS[key]
    outdir = ensure_output_dir(LESSON_DIR)
    outfile = outdir / f"{key}.md"

    print(f"\nRunning: {s['name']}...")
    rc, stdout, stderr = run_copilot(
        s["prompt"], LESSON_DIR,
        model=model,
        custom_instructions=s["custom_instructions"],
        output_file=outfile,
        log_dir=outdir / "logs" / key,
    )
    print_result(s["name"], stdout, outfile)


def main() -> None:
    parser = argparse.ArgumentParser(description="Lesson 05 validation")
    parser.add_argument("--all", action="store_true", help="Run all scenarios")
    parser.add_argument("--scenario", choices=list(SCENARIOS), help="Run a specific scenario")
    parser.add_argument("--model", default=MODEL_HEAVY, help=f"Model to use (default: {MODEL_HEAVY})")
    args = parser.parse_args()

    if not args.all and not args.scenario:
        parser.print_help()
        sys.exit(1)

    print("─" * 50)
    print("  Lesson 05 — Validation")
    print("─" * 50)

    print("\nSetting up workspace (clean copy from template)...")
    setup_workspace(clean=True)

    if args.all:
        for key in SCENARIOS:
            run_scenario(key, args.model)
    else:
        run_scenario(args.scenario, args.model)


if __name__ == "__main__":
    main()
