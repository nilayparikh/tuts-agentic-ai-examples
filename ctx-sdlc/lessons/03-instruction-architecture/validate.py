#!/usr/bin/env python3
"""Lesson 03 — Validation script.

Tests that scoped instructions change output for different file contexts.
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
    "route-layer": {
        "name": "Scenario 1 — Route Layer",
        "prompt": (
            "Add a DELETE /notifications/preferences/:event endpoint that "
            "resets a single event to defaults for the current user."
        ),
    },
    "business-rule": {
        "name": "Scenario 2 — Business Rule Layer",
        "prompt": (
            "Add a New York restriction: email for decline events is "
            "under review (LEGAL-305). Block email for decline on NY loans."
        ),
    },
    "test-layer": {
        "name": "Scenario 4 — Test Layer",
        "prompt": (
            "Add a test that verifies the California SMS restriction "
            "applies case-insensitively (CA, ca, Ca all blocked)."
        ),
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
        custom_instructions=True,
        output_file=outfile,
        log_dir=outdir / "logs" / key,
    )
    print_result(s["name"], stdout, outfile)


def main() -> None:
    parser = argparse.ArgumentParser(description="Lesson 03 validation")
    parser.add_argument("--all", action="store_true", help="Run all scenarios")
    parser.add_argument("--scenario", choices=list(SCENARIOS), help="Run a specific scenario")
    parser.add_argument("--model", default=MODEL_HEAVY, help=f"Model to use (default: {MODEL_HEAVY})")
    args = parser.parse_args()

    if not args.all and not args.scenario:
        parser.print_help()
        sys.exit(1)

    print("─" * 50)
    print("  Lesson 03 — Validation")
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
