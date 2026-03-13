#!/usr/bin/env python3
"""PreToolUse hook: block edits to protected files.

Reads JSON from stdin (VS Code hook input) and checks if the tool is
attempting to edit a protected file. Returns a deny decision if so.

Protected files:
  - .env, .env.*
  - app/backend/src/config/feature-flags.ts
  - app/backend/src/db/connection.ts
"""
import json
import sys
from pathlib import PurePosixPath

PROTECTED_PATTERNS = [
    ".env",
    "app/backend/src/config/feature-flags.ts",
    "app/backend/src/db/connection.ts",
]


def is_protected(filepath: str) -> bool:
    p = PurePosixPath(filepath)
    for pattern in PROTECTED_PATTERNS:
        if p.name.startswith(".env") or str(p) == pattern:
            return True
    return False


def main() -> None:
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Only check file-editing tools
    if tool_name not in ("editFiles", "createFile"):
        sys.exit(0)

    files = tool_input.get("files", [])
    file_path = tool_input.get("filePath", "")
    paths_to_check = files if files else ([file_path] if file_path else [])

    for fp in paths_to_check:
        if is_protected(fp):
            result = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        f"Edit blocked: '{fp}' is protected by security policy. "
                        "See docs/security-policy.md for the change approval process."
                    ),
                }
            }
            json.dump(result, sys.stdout)
            sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    main()
