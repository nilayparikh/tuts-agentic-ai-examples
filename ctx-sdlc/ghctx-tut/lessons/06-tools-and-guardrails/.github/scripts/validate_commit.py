#!/usr/bin/env python3
"""Pre-commit validation script (Python replacement for validate-commit.sh).

Called by the pre-commit hook to ensure code quality before committing.
Usage: python validate_commit.py
"""
import subprocess
import sys
from pathlib import Path


def run_step(name: str, cmd: list[str]) -> bool:
    """Run a validation step and return True if it passed."""
    print(f"  {name}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  FAIL: {name}")
        if result.stdout:
            print(result.stdout[:500])
        if result.stderr:
            print(result.stderr[:500])
        return False
    print(f"  OK")
    return True


def main() -> None:
    print("=== Pre-commit validation ===")

    steps = [
        ("[1/3] TypeScript compilation", ["npx", "tsc", "--noEmit"]),
    ]

    # Only run eslint if config exists
    if Path(".eslintrc.json").exists() or Path("eslint.config.js").exists():
        steps.append(("[2/3] Lint", ["npx", "eslint", "src/", "tests/", "--max-warnings", "0"]))
    else:
        print("  [2/3] Lint skipped (no eslint config found)")

    steps.append(("[3/3] Tests", ["npx", "vitest", "run", "--reporter=verbose"]))

    for name, cmd in steps:
        if not run_step(name, cmd):
            print(f"\nFAIL: {name} failed. Fix issues before committing.")
            sys.exit(1)

    print("\n=== All checks passed ===")


if __name__ == "__main__":
    main()
