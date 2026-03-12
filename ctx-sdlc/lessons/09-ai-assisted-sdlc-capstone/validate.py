#!/usr/bin/env python3
"""Lesson 09 — Validation script.

Runs the SAME prompt at each stage to demonstrate how progressive context
improves the output. Uses default.py to swap stages before each run.
"""
import argparse
import subprocess
import sys
from pathlib import Path

LESSON_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(LESSON_DIR.parent.parent / "scripts"))
from setup_utils import run_copilot, print_result, ensure_output_dir, MODEL_HEAVY

PROMPT = (
    "Add a task comments feature. Users should be able to comment on "
    "tasks with @mentions that notify the mentioned user."
)

STAGE_LABELS = {
    1: "Day One   — copilot-instructions.md only",
    2: "Week One  — + .instructions.md + docs/",
    3: "Week Two  — + .prompt.md + ADRs",
    4: "Month One — + .agent.md + SKILL.md",
    5: "Mature    — + mcp.json + hooks + CLI",
}


def apply_stage(n: int) -> None:
    """Call default.py --stage N to set up the context."""
    subprocess.run(
        [sys.executable, str(LESSON_DIR / "default.py"), "--stage", str(n)],
        check=True, capture_output=True,
    )


def run_stage(n: int, model: str) -> None:
    outdir = ensure_output_dir(LESSON_DIR)
    outfile = outdir / f"stage-{n}.md"

    print(f"\n  Applying stage {n}...")
    apply_stage(n)

    name = f"Stage {n} — {STAGE_LABELS[n]}"
    print(f"  Running: {name}...")
    rc, stdout, stderr = run_copilot(
        PROMPT, LESSON_DIR,
        model=model,
        custom_instructions=True,
        output_file=outfile,
        log_dir=outdir / "logs" / f"stage-{n}",
    )
    print_result(name, stdout, outfile)


def main() -> None:
    parser = argparse.ArgumentParser(description="Lesson 09 validation")
    parser.add_argument("--all", action="store_true", help="Run all 5 stages")
    parser.add_argument("--stage", type=int, choices=range(1, 6), help="Run a specific stage")
    parser.add_argument("--model", default=MODEL_HEAVY, help=f"Model to use (default: {MODEL_HEAVY})")
    args = parser.parse_args()

    if not args.all and not args.stage:
        parser.print_help()
        sys.exit(1)

    print("─" * 50)
    print("  Lesson 09 — Validation (Same Prompt, Five Stages)")
    print("─" * 50)

    if args.all:
        for n in range(1, 6):
            run_stage(n, args.model)
    else:
        run_stage(args.stage, args.model)


if __name__ == "__main__":
    main()
