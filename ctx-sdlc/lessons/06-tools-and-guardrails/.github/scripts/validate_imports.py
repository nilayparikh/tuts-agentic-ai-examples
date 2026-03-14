#!/usr/bin/env python3
"""PreToolUse hook: enforce barrel-file imports for TypeScript code.

Reads hook JSON from stdin when available and blocks changes that import from
internal module files when a sibling barrel/index.ts file exists. This keeps
TypeScript imports pointed at the public index.ts barrel instead of deep paths.
"""
import json
import os
import re
import sys
from pathlib import Path

TS_SUFFIXES = {".ts", ".tsx"}
EXCLUDED_DIRS = {"dist", "node_modules", ".git"}
IMPORT_PATTERNS = (
    re.compile(r"""\bimport\s+(?:type\s+)?[^;"']*?\bfrom\s+["']([^"']+)["']"""),
    re.compile(r"""\bexport\s+[^;"']*?\bfrom\s+["']([^"']+)["']"""),
    re.compile(r"""\bimport\(\s*["']([^"']+)["']\s*\)"""),
)
REPO_ROOT = Path(__file__).resolve().parents[2]


def load_hook_payload() -> dict:
    raw = sys.stdin.read().strip()
    if not raw:
        return {}

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return {}

    return payload if isinstance(payload, dict) else {}


def is_typescript_file(path: Path) -> bool:
    return path.suffix in TS_SUFFIXES and not any(part in EXCLUDED_DIRS for part in path.parts)


def normalize_candidate_path(raw_path: str) -> Path:
    path = Path(raw_path)
    return path if path.is_absolute() else REPO_ROOT / path


def collect_candidate_files(payload: dict) -> list[Path]:
    tool_name = str(payload.get("tool_name", ""))
    tool_input = payload.get("tool_input", {})
    paths: list[Path] = []

    if isinstance(tool_input, dict):
        files = tool_input.get("files", [])
        if isinstance(files, list):
            for file_path in files:
                if isinstance(file_path, str) and file_path:
                    paths.append(normalize_candidate_path(file_path))

        file_path = tool_input.get("filePath")
        if isinstance(file_path, str) and file_path:
            paths.append(normalize_candidate_path(file_path))

    candidates = [path for path in paths if path.exists() and is_typescript_file(path)]
    if candidates:
        return sorted(set(candidates))

    if tool_name and "commit" not in tool_name.lower():
        return []

    return sorted(
        path
        for path in (REPO_ROOT / "src").rglob("*")
        if path.is_file() and is_typescript_file(path) and "src" in path.parts
    )


def extract_imports(source: str) -> list[str]:
    specifiers: list[str] = []
    for pattern in IMPORT_PATTERNS:
        specifiers.extend(pattern.findall(source))
    return specifiers


def resolve_import_target(source_file: Path, specifier: str) -> Path | None:
    if not specifier.startswith("."):
        return None

    base_path = (source_file.parent / specifier).resolve(strict=False)
    candidates: list[Path] = []

    if base_path.suffix in {".js", ".jsx", ".mjs", ".cjs"}:
        candidates.extend(
            [
                base_path.with_suffix(".ts"),
                base_path.with_suffix(".tsx"),
                base_path.with_suffix(".mts"),
                base_path.with_suffix(".cts"),
            ]
        )
    elif base_path.suffix:
        candidates.append(base_path)
    else:
        candidates.extend(
            [
                base_path / "index.ts",
                base_path / "index.tsx",
                base_path.with_suffix(".ts"),
                base_path.with_suffix(".tsx"),
            ]
        )

    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate

    return None


def to_import_specifier(source_file: Path, target_file: Path) -> str:
    relative = Path(os.path.relpath(target_file, start=source_file.parent))

    specifier = relative.as_posix()
    if not specifier.startswith("."):
        specifier = f"./{specifier}"

    if specifier.endswith(".ts"):
        return f"{specifier[:-3]}.js"
    if specifier.endswith(".tsx"):
        return f"{specifier[:-4]}.js"
    return specifier


def barrel_for_target(target_file: Path) -> Path | None:
    barrel = target_file.parent / "index.ts"
    if target_file.name == "index.ts" or not barrel.exists():
        return None
    return barrel


def find_violations(files: list[Path]) -> list[str]:
    violations: list[str] = []

    for source_file in files:
        source = source_file.read_text(encoding="utf-8")
        for specifier in extract_imports(source):
            target = resolve_import_target(source_file, specifier)
            if target is None or not target.is_relative_to(REPO_ROOT):
                continue

            barrel = barrel_for_target(target)
            if barrel is None:
                continue

            suggested = to_import_specifier(source_file, barrel)
            relative_source = source_file.relative_to(REPO_ROOT).as_posix()
            relative_barrel = barrel.relative_to(REPO_ROOT).as_posix()
            violations.append(
                f"{relative_source}: import '{specifier}' reaches into an internal module path. "
                f"Use the barrel '{suggested}' ({relative_barrel}) instead."
            )

    return violations


def emit_deny(message: str) -> None:
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": message,
            }
        },
        sys.stdout,
    )


def main() -> None:
    payload = load_hook_payload()
    files = collect_candidate_files(payload)
    if not files:
        sys.exit(0)

    violations = find_violations(files)
    if not violations:
        sys.exit(0)

    summary = "Import validation failed: " + " | ".join(violations[:3])
    if len(violations) > 3:
        summary += f" | ...and {len(violations) - 3} more violation(s)."

    if payload:
        emit_deny(summary)
        sys.exit(0)

    print(summary, file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
