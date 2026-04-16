#!/usr/bin/env python3
"""PreToolUse hook: enforce barrel-file imports for TypeScript files.

Reads hook JSON from stdin when present, inspects changed .ts/.tsx files, and
denies imports that bypass a sibling index.ts barrel and reach into an internal
module path.
"""

from __future__ import annotations

import json
import posixpath
import re
import sys
from dataclasses import dataclass
from pathlib import Path

SRC_ROOTS = ("src/backend/src", "src/frontend/src")
TS_FILE_SUFFIXES = {".ts", ".tsx"}
IMPORT_PATTERN = re.compile(
    r"""
    ^\s*
    (?:
        import(?:\s+type)?(?:[\s\w{},*]*?\s+from\s+)?
        |
        export(?:\s+type)?[\s\w{},*]*?\s+from\s+
    )
    ["'](?P<path>[^"']+)["']
    """,
    re.MULTILINE | re.VERBOSE,
)


@dataclass(frozen=True)
class ChangedFile:
    path: str
    text: str


@dataclass(frozen=True)
class ImportViolation:
    file_path: str
    import_path: str
    barrel_path: str
    module_name: str


def load_hook_payload() -> dict | None:
    """Read hook JSON from stdin when present."""
    if sys.stdin.isatty():
        return None

    raw = sys.stdin.read()
    if not raw.strip():
        return None

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"Invalid hook payload JSON: {exc}", file=sys.stderr)
        sys.exit(1)


def extract_text(entry: dict) -> str | None:
    """Return the first known text field from a hook payload entry."""
    for key in ("file_text", "text", "content", "contents", "newText", "updatedText"):
        value = entry.get(key)
        if isinstance(value, str):
            return value
    return None


def resolve_workspace_path(repo_root: Path, path_value: str) -> Path:
    """Resolve a repo-relative or absolute path against the lesson root."""
    candidate = Path(path_value)
    if not candidate.is_absolute():
        candidate = repo_root / candidate
    return candidate.resolve(strict=False)


def load_changed_files(payload: dict | None, repo_root: Path) -> list[ChangedFile]:
    """Extract changed TypeScript files and their candidate contents from hook input."""
    if payload is None:
        return []

    tool_name = payload.get("tool_name", "")
    if tool_name not in {"createFile", "editFiles"}:
        return []

    tool_input = payload.get("tool_input", {})
    raw_entries: list[tuple[str, str | None]] = []

    files = tool_input.get("files", [])
    if isinstance(files, list):
        for item in files:
            if isinstance(item, str):
                raw_entries.append((item, None))
            elif isinstance(item, dict):
                file_path = item.get("filePath") or item.get("path")
                if isinstance(file_path, str):
                    raw_entries.append((file_path, extract_text(item)))

    top_level_path = tool_input.get("filePath") or tool_input.get("path")
    if isinstance(top_level_path, str):
        raw_entries.append((top_level_path, extract_text(tool_input)))

    changed_files: dict[str, ChangedFile] = {}
    for file_path, provided_text in raw_entries:
        normalized_path = Path(file_path).as_posix()
        if Path(normalized_path).suffix not in TS_FILE_SUFFIXES:
            continue

        file_text = provided_text
        if file_text is None:
            absolute_path = resolve_workspace_path(repo_root, normalized_path)
            if absolute_path.exists():
                file_text = absolute_path.read_text(encoding="utf-8")

        if file_text is None:
            continue

        changed_files[normalized_path] = ChangedFile(path=normalized_path, text=file_text)

    return list(changed_files.values())


def find_src_root(file_path: Path, repo_root: Path) -> Path | None:
    """Return the matching lesson src root for a file, if any."""
    for src_root in SRC_ROOTS:
        candidate = (repo_root / src_root).resolve(strict=False)
        try:
            file_path.relative_to(candidate)
            return candidate
        except ValueError:
            continue
    return None


def extract_import_paths(file_text: str) -> list[str]:
    """Collect import/export module specifiers from file contents."""
    return [match.group("path") for match in IMPORT_PATTERN.finditer(file_text)]


def normalize_relative_import(importer_rel_path: Path, import_path: str) -> str | None:
    """Resolve a relative import to a normalized src-root-relative posix path."""
    if not import_path.startswith("."):
        return None

    importer_dir = importer_rel_path.parent.as_posix()
    normalized = posixpath.normpath(posixpath.join(importer_dir, import_path))
    if normalized.startswith("../") or normalized == "..":
        return None
    return normalized


def is_barrel_reference(target_parts: tuple[str, ...]) -> bool:
    """Return True when the import already points at the module barrel."""
    if len(target_parts) == 1:
        return True

    if len(target_parts) == 2 and Path(target_parts[1]).stem == "index":
        return True

    return False


def build_barrel_import(importer_rel_path: Path, module_name: str) -> str:
    """Build the relative specifier for a sibling module barrel import."""
    importer_dir = importer_rel_path.parent.as_posix()
    relative = posixpath.relpath(module_name, importer_dir)
    if not relative.startswith("."):
        relative = f"./{relative}"
    return relative.replace("\\", "/")


def find_import_violation(
    changed_file: ChangedFile,
    repo_root: Path,
) -> list[ImportViolation]:
    """Return any barrel-bypassing imports for a changed TypeScript file."""
    absolute_file_path = resolve_workspace_path(repo_root, changed_file.path)
    src_root = find_src_root(absolute_file_path, repo_root)
    if src_root is None:
        return []

    importer_rel_path = absolute_file_path.relative_to(src_root)
    importer_parts = importer_rel_path.parts
    importer_module = importer_parts[0] if len(importer_parts) > 1 else None

    violations: list[ImportViolation] = []
    for import_path in extract_import_paths(changed_file.text):
        target_rel_path = normalize_relative_import(importer_rel_path, import_path)
        if target_rel_path is None:
            continue

        target_parts = tuple(part for part in Path(target_rel_path).parts if part not in {".", ""})
        if len(target_parts) < 2 or is_barrel_reference(target_parts):
            continue

        target_module = target_parts[0]
        if target_module == importer_module:
            continue

        violations.append(
            ImportViolation(
                file_path=changed_file.path,
                import_path=import_path,
                barrel_path=build_barrel_import(importer_rel_path, target_module),
                module_name=target_module,
            )
        )

    return violations


def format_violation_details(violations: list[ImportViolation]) -> str:
    """Render human-readable detail lines for a deny decision."""
    return "\n".join(
        (
            f"- {violation.file_path}: import '{violation.import_path}' reaches into "
            f"the internal '{violation.module_name}' module path. Use "
            f"'{violation.barrel_path}' so the import resolves through "
            f"{violation.module_name}/index.ts."
        )
        for violation in violations
    )


def deny_imports(violations: list[ImportViolation]) -> None:
    """Emit a standard PreToolUse deny payload."""
    details = format_violation_details(violations)
    first = violations[0]
    result = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "Import validation failed: "
                f"{first.file_path} would violate the barrel-file import convention. "
                "Import from the module's barrel file (index.ts) rather than directly "
                "from internal module paths.\n\n"
                f"{details}"
            ),
        }
    }
    json.dump(result, sys.stdout)
    sys.exit(0)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    payload = load_hook_payload()
    changed_files = load_changed_files(payload, repo_root)

    violations: list[ImportViolation] = []
    for changed_file in changed_files:
        violations.extend(find_import_violation(changed_file, repo_root))

    if violations:
        deny_imports(violations)

    sys.exit(0)


if __name__ == "__main__":
    main()
