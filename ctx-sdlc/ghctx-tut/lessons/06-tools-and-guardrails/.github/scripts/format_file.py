#!/usr/bin/env python3
"""Post-save formatting script (Python replacement for format-file.sh).

Called by the post-save hook to auto-format TypeScript files.
Usage: python format_file.py <filepath>
"""
import subprocess
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python format_file.py <filepath>", file=sys.stderr)
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if filepath.suffix in (".ts", ".tsx"):
        subprocess.run(["npx", "prettier", "--write", str(filepath)], check=True)


if __name__ == "__main__":
    main()
