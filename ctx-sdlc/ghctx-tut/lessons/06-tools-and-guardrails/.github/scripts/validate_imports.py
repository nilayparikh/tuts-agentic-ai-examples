#!/usr/bin/env python3
"""PreToolUse hook: enforce barrel-file import convention.

Reads JSON from stdin (VS Code hook input) and checks if TypeScript files
in src/backend/src/ are importing directly from internal module paths
instead of going through barrel files (index.ts).

The barrel-file convention requires:
  - Imports from sibling directories use the directory name (e.g., '../rules')
  - Do not import directly from specific files (e.g., '../rules/business-rules')
  - Exception: package imports (e.g., 'express') and non-src files are allowed
"""
import json
import re
import sys
from pathlib import PurePosixPath


def is_src_backend_file(filepath: str) -> bool:
    """Check if file is in src/backend/src/."""
    p = PurePosixPath(filepath)
    parts = p.parts
    if len(parts) >= 3:
        return parts[0] == "src" and parts[1] == "backend" and parts[2] == "src"
    return False


def extract_imports(content: str) -> list[str]:
    """Extract import paths from TypeScript/JavaScript content.
    
    Returns list of import paths (e.g., ['../rules/business-rules', 'express']).
    """
    # Match both ES6 import and CommonJS require patterns
    # Captures: import ... from "path" or import ... from 'path'
    import_pattern = r'(?:import|from)\s+["\']([^"\']+)["\']'
    matches = re.findall(import_pattern, content)
    return matches


def is_relative_import(path: str) -> bool:
    """Check if path is a relative import (starts with . or ..)."""
    return path.startswith(".") or path.startswith("..")


def is_package_import(path: str) -> bool:
    """Check if path is a package import (no / in path, doesn't start with .)."""
    return "/" not in path and not is_relative_import(path)


def violates_barrel_convention(import_path: str) -> bool:
    """Check if import violates barrel-file convention.
    
    Violation: relative import that targets a specific file (contains hyphen
    or filename.ts pattern) rather than a directory.
    
    Examples of violations:
      - '../rules/business-rules' (hyphenated filename)
      - '../services/audit-service' (hyphenated filename)
      - '../models/state-machine' (hyphenated filename)
    
    Examples of allowed imports:
      - '../rules' (barrel directory)
      - '../services' (barrel directory)
      - 'express' (package import)
    """
    if not is_relative_import(import_path):
        return False
    
    # Extract the last component of the path
    parts = import_path.split("/")
    last_part = parts[-1]
    
    # If the last part contains a hyphen, it's a specific file import (violation)
    # Example: 'business-rules', 'audit-service', 'state-machine'
    if "-" in last_part:
        return True
    
    return False


def main() -> None:
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    
    # Only check file-creating/editing tools that have content
    if tool_name not in ("createFile", "editFiles"):
        sys.exit(0)
    
    # Get file path and content
    file_path = tool_input.get("filePath", "")
    file_text = tool_input.get("file_text", "")
    
    # Only validate TypeScript/JavaScript files in src/backend/src/
    if not file_path or not (file_path.endswith(".ts") or file_path.endswith(".tsx")):
        sys.exit(0)
    
    if not is_src_backend_file(file_path):
        sys.exit(0)
    
    # Extract imports and check for violations
    imports = extract_imports(file_text)
    for import_path in imports:
        if violates_barrel_convention(import_path):
            result = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        f"Import blocked: '{import_path}' violates barrel-file convention. "
                        f"Import from the parent directory instead (e.g., "
                        f"'from \"../{import_path.split('/')[1]}\"'). "
                        f"Barrel files (index.ts) should re-export internal module contents."
                    ),
                }
            }
            json.dump(result, sys.stdout)
            sys.exit(0)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
