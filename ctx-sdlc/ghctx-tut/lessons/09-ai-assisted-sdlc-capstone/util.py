#!/usr/bin/env python3
"""Lesson 09 — AI-Assisted SDLC Capstone workspace utility.

Usage:
  python util.py --setup    Copy app source into src/, install deps, seed data
"""

from __future__ import annotations

from pathlib import Path
import sys

LESSON = Path(__file__).resolve().parent
APP_SOURCE = LESSON.parent.parent / "app"

sys.path.insert(0, str(LESSON.parent / "_common"))
from util_base import main  # noqa: E402

if __name__ == "__main__":
    main(
        lesson_num="09",
        lesson_title="AI-Assisted SDLC Capstone",
        lesson_dir=LESSON,
        app_source=APP_SOURCE,
    )
