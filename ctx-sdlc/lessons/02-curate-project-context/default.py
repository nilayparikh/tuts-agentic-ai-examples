#!/usr/bin/env python3
"""Lesson 02 — Setup script.

Copies the Loan Workbench template into src/.
Context files (.github/, docs/) are checked in with the lesson.
"""
import argparse
import sys
from pathlib import Path

LESSON_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(LESSON_DIR.parent.parent / "scripts"))
from setup_utils import clean_workspace, copy_template, print_setup_complete


def setup(*, clean: bool = False) -> None:
    print("─" * 50)
    print("  Lesson 02 — Curate Project Context")
    print("─" * 50)

    if clean:
        print("\nCleaning workspace...")
        clean_workspace(LESSON_DIR)

    print("\nCopying template app (complex)...")
    copy_template(LESSON_DIR, "complex")

    print_setup_complete()


def main() -> None:
    parser = argparse.ArgumentParser(description="Lesson 02 setup")
    parser.add_argument("--clean", action="store_true", help="Remove existing files before setup")
    parser.add_argument("--reset", action="store_true", help="Alias for --clean (delete and re-copy)")
    args = parser.parse_args()
    setup(clean=args.clean or args.reset)


if __name__ == "__main__":
    main()
