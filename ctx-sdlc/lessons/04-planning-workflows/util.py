#!/usr/bin/env python3
"""Lesson 04 — Planning Workflows - Workspace utility.

Usage:
  python util.py --setup    Copy app source into src/, create .env interactively
  python util.py --run      Install deps + start backend & frontend dev servers
  python util.py --clean    Remove copied src/ and build artifacts
"""

import sys
from pathlib import Path

LESSON = Path(__file__).resolve().parent
sys.path.insert(0, str(LESSON.parent / "_common"))
from util_base import main  # noqa: E402

if __name__ == "__main__":
    main("04", "Planning Workflows", LESSON, LESSON.parent.parent / "app")
