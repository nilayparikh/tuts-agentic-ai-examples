#!/usr/bin/env python3
"""PreToolUse hook: enforce barrel-file imports for TypeScript modules.

This validator blocks imports that reach through another module's internal file
path when the import should go through that module's `index.ts` barrel instead.
Barrel files themselves are exempt because they aggregate those internal files.
"""
import json
import re
import sys
from pathlib import Path, PurePosixPath

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = PROJECT_ROOT / "src"
TS_EXTENSIONS = {".ts", ".tsx", ".mts", ".cts"}
JS_TO_TS_EXTENSIONS = {
    ".js": [".ts", ".tsx"],
    ".jsx": [".tsx", ".ts"],
    ".mjs": [".mts", ".ts"],
    ".cjs": [".cts", ".ts"],
}
EDIT_TOOLS = {"editFiles", "createFile"}
IMPORT_RE = re.compile(
    r"""
    ^\s*
    (?:
      import
      (?:
        \s+(?:type\s+)?[\s\S]*?\s+from
      )?
      |
      export
      \s+(?:type\s+)?
      [\s\S]*?\s+from
    )
    \s*["'](?P<specifier>[^"']+)["']
    """,
    re.MULTILINE | re.VERBOSE,
)


def is_typescript_file(path: Path) -> bool:
    return path.suffix in TS_EXTENSIONS


def is_barrel_file(path: Path) -> bool:
    return path.name.startswith("index.") and is_typescript_file(path)


def normalize_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    posix_path = PurePosixPath(raw_path.replace("\\", "/"))
    return PROJECT_ROOT.joinpath(*posix_path.parts)


def relative_path(path: Path) -> str:
    try:
        return path.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def strip_relative_segments(specifier: str) -> list[str]:
    parts = PurePosixPath(specifier).parts
    return [part for part in parts if part not in (".", "..")]


def resolve_base_target(source_path: Path, specifier: str) -> Path:
    specifier_path = PurePosixPath(specifier)
    return source_path.parent.joinpath(*specifier_path.parts).resolve(strict=False)


def has_barrel_file(directory: Path) -> bool:
    return any((directory / f"index{extension}").exists() for extension in TS_EXTENSIONS)


def is_barrel_import(source_path: Path, specifier: str) -> bool:
    base_target = resolve_base_target(source_path, specifier)

    if base_target.is_dir():
        return has_barrel_file(base_target)

    if base_target.exists() and base_target.stem == "index":
        return True

    if base_target.suffix in JS_TO_TS_EXTENSIONS:
        for extension in JS_TO_TS_EXTENSIONS[base_target.suffix]:
            if base_target.with_suffix(extension).exists() and base_target.stem == "index":
                return True

    if not base_target.suffix and has_barrel_file(base_target):
        return True

    return False


def is_deep_relative_import(source_path: Path, specifier: str) -> bool:
    if not specifier.startswith("."):
        return False

    if is_barrel_import(source_path, specifier):
        return False

    path_parts = strip_relative_segments(specifier)
    if len(path_parts) <= 1:
        return False

    if PurePosixPath(path_parts[-1]).stem == "index":
        return False

    return True


def suggested_barrel(specifier: str) -> str:
    path = PurePosixPath(specifier)
    parent = path.parent
    if str(parent) == ".":
        return "./index.ts"
    return f"{parent.as_posix()}/index.ts"


def collect_violations(source_path: Path, content: str) -> list[str]:
    if is_barrel_file(source_path):
        return []

    violations: list[str] = []
    for match in IMPORT_RE.finditer(content):
        specifier = match.group("specifier")
        if is_deep_relative_import(source_path, specifier):
            violations.append(
                f"{relative_path(source_path)} imports '{specifier}'. "
                f"Use the barrel file '{suggested_barrel(specifier)}' "
                "instead of an internal module path."
            )
    return violations


def collect_repository_violations() -> list[str]:
    violations: list[str] = []
    if not SOURCE_ROOT.exists():
        return violations

    for path in sorted(SOURCE_ROOT.rglob("*")):
        if not path.is_file() or not is_typescript_file(path):
            continue
        if any(part in {"node_modules", "dist"} for part in path.parts):
            continue
        violations.extend(collect_violations(path, path.read_text(encoding="utf-8")))
    return violations


def read_hook_payload() -> dict | None:
    if sys.stdin.isatty():
        return None

    raw = sys.stdin.read().strip()
    if not raw:
        return None

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def is_commit_operation(payload: dict) -> bool:
    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {})

    if tool_name in {"runTerminalCommand", "powershell", "bash"}:
        command = " ".join(
            str(part)
            for part in (
                tool_input.get("command"),
                tool_input.get("input"),
                tool_input.get("args"),
            )
            if part
        )
        return "git commit" in command

    return False


def collect_hook_violations(payload: dict) -> list[str]:
    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {})

    if is_commit_operation(payload):
        return collect_repository_violations()

    if tool_name not in EDIT_TOOLS:
        return []

    file_path = tool_input.get("filePath")
    files = tool_input.get("files", [])
    paths_to_check = files if files else ([file_path] if file_path else [])

    content = (
        tool_input.get("content")
        or tool_input.get("newContent")
        or tool_input.get("newString")
        or ""
    )

    violations: list[str] = []
    for raw_path in paths_to_check:
        path = normalize_path(raw_path)
        if not is_typescript_file(path):
            continue

        if content:
            violations.extend(collect_violations(path, content))
            continue

        if path.exists():
            violations.extend(collect_violations(path, path.read_text(encoding="utf-8")))

    return violations


def emit_deny(violations: list[str]) -> None:
    result = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "Import validation failed. "
                + " ".join(violations[:3])
            ),
        }
    }
    json.dump(result, sys.stdout)


def main() -> None:
    payload = read_hook_payload()
    if payload is not None:
        violations = collect_hook_violations(payload)
        if violations:
            emit_deny(violations)
        return

    print("=== Import validation ===")
    violations = collect_repository_violations()
    if violations:
        print("FAIL: TypeScript imports must use barrel files (index.ts).")
        for violation in violations[:20]:
            print(f"  - {violation}")
        sys.exit(1)

    print("OK")


if __name__ == "__main__":
    main()
