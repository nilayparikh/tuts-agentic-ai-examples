#!/usr/bin/env python3
"""Lesson 04 — Validation script.

Tests shallow vs. deep planning by running with and without spec attachments.
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
    "shallow": {
        "name": "Scenario 1 — Shallow Planning (no specs)",
        "prompt": (
            "Plan the implementation for notification preferences in the "
            "Loan Workbench. Look at the source code to understand the current system."
        ),
        "custom_instructions": True,
    },
    "deep": {
        "name": "Scenario 2 — Deep Planning (specs + NFRs)",
        "prompt": (
            "#file:specs/product-spec-notification-preferences.md "
            "#file:specs/non-functional-requirements.md "
            "#file:docs/architecture.md "
            "#file:feature-request.md\n\n"
            "Plan the implementation for the feature described in the "
            "feature request. Read all attached files before generating "
            "the plan. For each task, trace it to a specific FR, NFR, "
            "or special condition in the product spec."
        ),
        "custom_instructions": True,
    },
    "no-context": {
        "name": "Baseline — No Context",
        "prompt": (
            "Plan the implementation for notification preferences in a "
            "loan management application."
        ),
        "custom_instructions": False,
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
    parser = argparse.ArgumentParser(description="Lesson 04 validation")
    parser.add_argument("--all", action="store_true", help="Run all scenarios")
    parser.add_argument("--scenario", choices=list(SCENARIOS), help="Run a specific scenario")
    parser.add_argument("--model", default=MODEL_HEAVY, help=f"Model to use (default: {MODEL_HEAVY})")
    args = parser.parse_args()

    if not args.all and not args.scenario:
        parser.print_help()
        sys.exit(1)

    print("─" * 50)
    print("  Lesson 04 — Validation")
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
