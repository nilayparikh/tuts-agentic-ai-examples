#!/usr/bin/env python3
"""Lesson 08 — Validation script.

Runs the audit script against drifted and clean examples, and tests
stale-tech and contradictory-rule prompts.
"""
import argparse
import subprocess
import sys
from pathlib import Path

LESSON_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(LESSON_DIR.parent.parent / "scripts"))
sys.path.insert(0, str(LESSON_DIR))
from setup_utils import run_copilot, print_result, ensure_output_dir, MODEL_HEAVY, MODEL_LIGHT
from default import setup as setup_workspace

SCENARIOS = {
    "audit-drifted": {
        "name": "Scenario 1 — Audit Drifted Context",
        "type": "script",
    },
    "stale-tech": {
        "name": "Scenario 3 — Stale Technology Problem",
        "prompt": "Add structured logging to the new route handler.",
        "type": "copilot",
    },
    "contradictory": {
        "name": "Scenario 4 — Contradictory Rules Problem",
        "prompt": "Add error logging to the state machine transition handler.",
        "type": "copilot",
    },
}


def run_audit(key: str) -> None:
    """Run the Python audit script against the drifted example."""
    audit_script = LESSON_DIR / "scripts" / "audit_context.py"
    print(f"\nRunning audit on drifted example...")
    outdir = ensure_output_dir(LESSON_DIR)
    outfile = outdir / f"{key}.txt"

    result = subprocess.run(
        [sys.executable, str(audit_script), "--project-dir", str(LESSON_DIR)],
        capture_output=True, text=True,
    )
    output = result.stdout + result.stderr
    outfile.write_text(output, encoding="utf-8")
    print_result("Audit Drifted Context", output, outfile)


def run_copilot_scenario(key: str, model: str) -> None:
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
    parser = argparse.ArgumentParser(description="Lesson 08 validation")
    parser.add_argument("--all", action="store_true", help="Run all scenarios")
    parser.add_argument("--scenario", choices=list(SCENARIOS), help="Run a specific scenario")
    parser.add_argument("--model", default=MODEL_HEAVY, help=f"Model to use (default: {MODEL_HEAVY})")
    args = parser.parse_args()

    if not args.all and not args.scenario:
        parser.print_help()
        sys.exit(1)

    print("─" * 50)
    print("  Lesson 08 — Validation")
    print("─" * 50)

    print("\nSetting up workspace (clean copy from template)...")
    setup_workspace(clean=True)

    targets = list(SCENARIOS) if args.all else [args.scenario]
    for key in targets:
        s = SCENARIOS[key]
        if s["type"] == "script":
            run_audit(key)
        else:
            run_copilot_scenario(key, args.model)


if __name__ == "__main__":
    main()
