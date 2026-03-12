#!/usr/bin/env python3
"""Dead reference detection script (Python replacement for detect-stale-refs.sh).

Scans all .md files in .github/ and docs/ for internal path references
and reports any that point to files or directories that don't exist.

Usage: python detect_stale_refs.py [--project-dir <path>]
"""
import argparse
import re
import sys
from pathlib import Path


def scan(project_dir: Path) -> int:
    stale = 0
    checked = 0

    print("Scanning for stale references...")
    print()

    search_dirs = [project_dir / ".github", project_dir / "docs"]
    md_files: list[Path] = []
    for d in search_dirs:
        if d.is_dir():
            md_files.extend(d.rglob("*.md"))

    for md_file in md_files:
        text = md_file.read_text(encoding="utf-8", errors="replace")
        rel_name = md_file.relative_to(project_dir)

        # Match file references: backtick-wrapped, markdown links, "see" references
        file_refs = re.findall(
            r'(?:`|(?:[Ss]ee\s+)|\]\()/?([a-zA-Z][\w./-]+\.(?:md|ts|js|json|yaml|yml))',
            text,
        )
        dir_refs = re.findall(
            r'(?:`|(?:[Ss]ee\s+)|\]\()/?([a-zA-Z][\w/-]+/)',
            text,
        )

        for ref in file_refs:
            checked += 1
            clean = ref.lstrip("/")
            if not (project_dir / clean).is_file():
                print(f"  ✗ STALE {rel_name} → {clean} (file not found)")
                stale += 1

        for ref in dir_refs:
            checked += 1
            clean = ref.lstrip("/")
            if not (project_dir / clean).is_dir():
                print(f"  ✗ STALE {rel_name} → {clean} (directory not found)")
                stale += 1

    print()
    print("─" * 30)
    print(f"Checked: {checked} references")
    if stale > 0:
        print(f"Found: {stale} stale reference(s)")
        return 1
    else:
        print("All references valid.")
        return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect stale references in context files")
    parser.add_argument("--project-dir", type=Path, default=Path.cwd(),
                        help="Project root to scan (default: cwd)")
    args = parser.parse_args()
    sys.exit(scan(args.project_dir))


if __name__ == "__main__":
    main()
