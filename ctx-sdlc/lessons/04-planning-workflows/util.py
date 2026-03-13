#!/usr/bin/env python3
"""Lesson 04 — Planning Workflows - Workspace utility.

Usage:
  python util.py --setup    Copy Loan Workbench app source into src/
  python util.py --clean    Remove copied src/ and build artifacts
"""

import argparse
import shutil
import sys
from pathlib import Path

LESSON = Path(__file__).resolve().parent
APP_SOURCE = LESSON.parent.parent / "app"


def clean() -> None:
    """Remove copied app source and build artifacts."""
    for name in ("src", "node_modules", "dist"):
        target = LESSON / name
        if target.is_dir():
            shutil.rmtree(target)
            print(f"  Removed {name}/")
    for name in (".env",):
        target = LESSON / name
        if target.is_file():
            target.unlink()
            print(f"  Removed {name}")
    for db in LESSON.glob("*.db"):
        db.unlink()
        print(f"  Removed {db.name}")


def setup() -> None:
    """Clean workspace then copy Loan Workbench app into src/."""
    print("Lesson 04 — Planning Workflows\n")
    clean()
    if not APP_SOURCE.exists():
        print(f"ERROR: App source not found at {APP_SOURCE}", file=sys.stderr)
        sys.exit(1)
    shutil.copytree(
        APP_SOURCE,
        LESSON / "src",
        ignore=shutil.ignore_patterns("node_modules", ".env", "*.db"),
    )
    print("  Copied app/ -> src/")
    print("\n\u2713 Setup complete. Run: cd src && npm install")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Lesson 04 workspace utility")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--setup", action="store_true", help="Clean + copy app source")
    g.add_argument("--clean", action="store_true", help="Remove copied src/ and artifacts")
    args = p.parse_args()
    if args.setup:
        setup()
    else:
        clean()
