#!/usr/bin/env python3
"""Lesson 09 — Setup script.

Copies the Loan Workbench template into src/, then applies cumulative delta
stages to build the context progressively.
Each stage folder contains ONLY the files that are NEW or CHANGED at that point.
Running --stage N applies stages 1..N, so the result is cumulative.
"""
import argparse
import sys
from pathlib import Path

LESSON_DIR = Path(__file__).resolve().parent
STAGES_DIR = LESSON_DIR / "stages"
sys.path.insert(0, str(LESSON_DIR.parent.parent / "scripts"))
from setup_utils import clean_workspace, copy_template, copy_overlay, clean_context

STAGE_MAP = {
    1: "1-day-one",
    2: "2-week-one",
    3: "3-week-two",
    4: "4-month-one",
    5: "5-mature",
}

STAGE_DESCRIPTIONS = {
    1: "Day One   — copilot-instructions.md only",
    2: "Week One  — + .instructions.md + docs/architecture.md",
    3: "Week Two  — + .prompt.md files + ADRs",
    4: "Month One — + .agent.md files + SKILL.md",
    5: "Mature    — + mcp.json + hooks + CLI guide",
}


def setup(*, stage: int, clean: bool = False) -> None:
    print("─" * 50)
    print("  Lesson 09 — AI-Assisted SDLC Capstone")
    print(f"  Target: Stage {stage} — {STAGE_DESCRIPTIONS[stage]}")
    print("─" * 50)

    if clean:
        print("\nCleaning workspace...")
        clean_workspace(LESSON_DIR)

    print("\nCopying template app (complex)...")
    copy_template(LESSON_DIR, "complex")

    print(f"\nApplying stages 1–{stage} cumulatively...\n")

    # Clean context dirs so stage overlays start fresh
    clean_context(LESSON_DIR)

    for n in range(1, stage + 1):
        slug = STAGE_MAP[n]
        stage_dir = STAGES_DIR / slug
        if not stage_dir.exists():
            print(f"  ERROR: Stage directory not found: {stage_dir}", file=sys.stderr)
            sys.exit(1)
        print(f"  Stage {n}: {STAGE_DESCRIPTIONS[n]}")
        copy_overlay(stage_dir, LESSON_DIR)

    print("\n✓ Setup complete. Next steps:")
    print("  cd src && npm install")
    print("  # Open lesson folder in VS Code — Copilot auto-loads .github/ context")
    print("  # Or test with CLI:")
    print('  copilot -p "Add a task comments feature with @mentions" --allow-all')
    print()
    print("  # Compare output across stages by running:")
    for n in range(1, 6):
        marker = " ◄ current" if n == stage else ""
        print(f"  python default.py --stage {n}  # {STAGE_DESCRIPTIONS[n]}{marker}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Lesson 09 — AI-Assisted SDLC Capstone setup"
    )
    parser.add_argument(
        "--stage", type=int, choices=range(1, 6), required=True,
        help="Apply stages 1..N cumulatively (1=Day One, 5=Mature)",
    )
    parser.add_argument("--clean", action="store_true", help="Remove existing files before setup")
    args = parser.parse_args()
    setup(stage=args.stage, clean=args.clean)


if __name__ == "__main__":
    main()
