#!/usr/bin/env python3
"""Lesson 02 — Validation script.

Tests behavior-only vs. both-halves context by toggling docs/.
"""
import argparse
import sys
from pathlib import Path

LESSON_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(LESSON_DIR.parent.parent / "scripts"))
sys.path.insert(0, str(LESSON_DIR))
from setup_utils import run_copilot, print_result, ensure_output_dir, MODEL_HEAVY
from default import setup as setup_workspace

PROMPT = (
    "Add a route for preference management. Let users save their "
    "notification channel preferences (email, SMS) per event type."
)

SCENARIOS = {
    "no-context": {
        "name": "Scenario 1 — No Context (baseline)",
        "custom_instructions": False,
    },
    "behavior-only": {
        "name": "Scenario 2 — Behavior Only (.github/ but no docs/)",
        "custom_instructions": True,
    },
    "both-halves": {
        "name": "Scenario 3 — Both Halves (.github/ + docs/)",
        "custom_instructions": True,
    },
}


def run_scenario(key: str, model: str) -> None:
    s = SCENARIOS[key]
    outdir = ensure_output_dir(LESSON_DIR)
    outfile = outdir / f"{key}.md"

    prompt = PROMPT
    if key == "both-halves":
        prompt = (
            "#file:docs/architecture.md #file:docs/api-conventions.md\n\n"
            + PROMPT
        )

    print(f"\nRunning: {s['name']}...")
    rc, stdout, stderr = run_copilot(
        prompt, LESSON_DIR,
        model=model,
        custom_instructions=s["custom_instructions"],
        output_file=outfile,
        log_dir=outdir / "logs" / key,
    )
    print_result(s["name"], stdout, outfile)


def main() -> None:
    parser = argparse.ArgumentParser(description="Lesson 02 validation")
    parser.add_argument("--all", action="store_true", help="Run all scenarios")
    parser.add_argument("--scenario", choices=list(SCENARIOS), help="Run a specific scenario")
    parser.add_argument("--model", default=MODEL_HEAVY, help=f"Model to use (default: {MODEL_HEAVY})")
    args = parser.parse_args()

    if not args.all and not args.scenario:
        parser.print_help()
        sys.exit(1)

    print("─" * 50)
    print("  Lesson 02 — Validation")
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
