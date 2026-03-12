#!/usr/bin/env python3
"""Lesson 07 — Validation script.

Tests portability by running the same prompt with and without custom instructions
to simulate VS Code (full context) vs. CLI (foundation only).
"""
import argparse
import sys
from pathlib import Path

LESSON_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(LESSON_DIR.parent.parent / "scripts"))
sys.path.insert(0, str(LESSON_DIR))
from setup_utils import run_copilot, print_result, ensure_output_dir, MODEL_HEAVY, MODEL_LIGHT
from default import setup as setup_workspace

PROMPT = "Add a route for archiving loan applications."

SCENARIOS = {
    "full-context": {
        "name": "Scenario 1 — Full Context (VS Code equivalent)",
        "custom_instructions": True,
        "model": MODEL_HEAVY,
    },
    "foundation-only": {
        "name": "Scenario 2 — Foundation Only (CLI equivalent)",
        "custom_instructions": True,  # CLI still reads copilot-instructions.md
        "model": MODEL_LIGHT,
    },
    "no-context": {
        "name": "Baseline — No Context",
        "custom_instructions": False,
        "model": MODEL_LIGHT,
    },
}


def run_scenario(key: str, model_override: str | None = None) -> None:
    s = SCENARIOS[key]
    outdir = ensure_output_dir(LESSON_DIR)
    outfile = outdir / f"{key}.md"
    model = model_override or s["model"]

    print(f"\nRunning: {s['name']}...")
    rc, stdout, stderr = run_copilot(
        PROMPT, LESSON_DIR,
        model=model,
        custom_instructions=s["custom_instructions"],
        output_file=outfile,
        log_dir=outdir / "logs" / key,
    )
    print_result(s["name"], stdout, outfile)


def main() -> None:
    parser = argparse.ArgumentParser(description="Lesson 07 validation")
    parser.add_argument("--all", action="store_true", help="Run all scenarios")
    parser.add_argument("--scenario", choices=list(SCENARIOS), help="Run a specific scenario")
    parser.add_argument("--model", default=None, help="Override model for all scenarios")
    args = parser.parse_args()

    if not args.all and not args.scenario:
        parser.print_help()
        sys.exit(1)

    print("─" * 50)
    print("  Lesson 07 — Validation")
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
