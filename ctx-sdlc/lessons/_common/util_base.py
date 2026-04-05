#!/usr/bin/env python3
"""Shared lesson utility — used by all per-lesson util.py files.

Provides setup (copy app → src/, create .env interactively), clean, and run
commands for the Loan Workbench example app.
"""

import argparse
import json
import os
import stat
import shutil
import subprocess
import sys
import time
from collections.abc import Callable
from pathlib import Path

# ── LocalM™ Tuts CLI Brand Banner ──────────────────────────────────────────

BRAND_BANNER = r"""
  ╭─────────────────────────────────────────╮
  │                                         │
  │    < / >   localm™  TUTS               │
  │                                         │
  │    Context Engineering for              │
  │    GitHub Copilot — Examples            │
  │                                         │
  ╰─────────────────────────────────────────╯
"""

BRAND_COLORS = {
    "cyan": "\033[96m",
    "purple": "\033[35m",
    "green": "\033[92m",
    "gold": "\033[93m",
    "dim": "\033[2m",
    "bold": "\033[1m",
    "reset": "\033[0m",
}


def _print_banner(title: str) -> None:
    """Print the branded CLI banner with lesson title."""
    c = BRAND_COLORS
    print(f"{c['cyan']}{BRAND_BANNER}{c['reset']}")
    print(f"  {c['bold']}{title}{c['reset']}")
    print(f"  {c['dim']}{'─' * 45}{c['reset']}\n")


def _parse_env_example(env_example: Path) -> list[tuple[str, str, str]]:
    """Parse .env.example into (key, default_value, comment) triples."""
    entries: list[tuple[str, str, str]] = []
    comment = ""
    for line in env_example.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            comment = stripped.lstrip("# ").strip()
            continue
        if "=" in stripped and not stripped.startswith("#"):
            key, _, value = stripped.partition("=")
            entries.append((key.strip(), value.strip(), comment))
            comment = ""
    return entries


def _create_env_interactive(lesson_dir: Path) -> None:
    """Create .env from .env.example, prompting user for each value."""
    src_dir = lesson_dir / "src"
    env_example = src_dir / ".env.example"
    env_target = src_dir / ".env"

    if not env_example.exists():
        print("  No .env.example found — skipping .env creation")
        return

    if env_target.exists():
        print("  .env already exists — skipping")
        return

    entries = _parse_env_example(env_example)
    if not entries:
        shutil.copy2(env_example, env_target)
        print("  Copied .env.example → .env (no variables found)")
        return

    print("\n  Configure environment variables (press Enter to accept default):\n")
    lines: list[str] = []
    for key, default, comment in entries:
        if comment:
            lines.append(f"# {comment}")
        prompt = f"    {key} [{default}]: "
        user_input = input(prompt).strip()
        value = user_input if user_input else default
        lines.append(f"{key}={value}")

    env_target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n  Created .env")


def _repair_package_json(src_dir: Path) -> None:
    """Patch known script issues in copied lesson workspaces."""
    package_json = src_dir / "package.json"
    if not package_json.exists():
        return

    data = json.loads(package_json.read_text(encoding="utf-8"))
    scripts = data.get("scripts") or {}
    current = scripts.get("dev:frontend")
    expected = "vite frontend --port 5173"

    if current == expected:
        return

    if current == "vite --root frontend --port 5173":
        scripts["dev:frontend"] = expected
        data["scripts"] = scripts
        package_json.write_text(
            json.dumps(data, indent=2) + "\n",
            encoding="utf-8",
        )
        print("  Repaired frontend dev script in src/package.json")


def _ensure_dependencies(src_dir: Path) -> None:
    """Install npm dependencies when src/node_modules is missing."""
    node_modules = src_dir / "node_modules"
    if node_modules.exists():
        return

    print("  Installing dependencies...")
    subprocess.run(
        ["npm", "install"],
        cwd=str(src_dir),
        check=True,
        shell=(os.name == "nt"),
    )
    print()


def _seed_database(src_dir: Path) -> None:
    """Create the lesson database with demo seed data."""
    print("  Seeding database...")
    subprocess.run(
        ["npm", "run", "db:seed"],
        cwd=str(src_dir),
        check=True,
        shell=(os.name == "nt"),
    )
    print()


def _clear_readonly_and_retry(func, path: str, _exc_info: object) -> None:
    """Allow shutil.rmtree to remove read-only files on Windows."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def _kill_lesson_node_processes(lesson_dir: Path) -> int:
    """Terminate Node/npm processes whose command lines reference this lesson."""
    if os.name != "nt":
        return 0

    target = str(lesson_dir.resolve()).lower().replace("'", "''")
    current_pid = os.getpid()
    script = f"""
$target = '{target}'
$currentPid = {current_pid}
$killed = 0
Get-CimInstance Win32_Process | Where-Object {{
  $_.ProcessId -ne $currentPid -and
  $_.Name -in @('node.exe', 'npm.exe') -and
  $_.CommandLine -and
  $_.CommandLine.ToLower().Contains($target)
}} | ForEach-Object {{
  try {{
    Stop-Process -Id $_.ProcessId -Force -ErrorAction Stop
    Write-Output ("  Stopped locking process: {0} ({1})" -f $_.Name, $_.ProcessId)
    $killed++
  }} catch {{
    Write-Output ("  Failed to stop process: {0} ({1})" -f $_.Name, $_.ProcessId)
  }}
}}
Write-Output ("__KILLED__=" + $killed)
"""

    result = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            script,
        ],
        capture_output=True,
        text=True,
        check=False,
        shell=False,
    )

    killed = 0
    for line in result.stdout.splitlines():
        if line.startswith("__KILLED__="):
            killed = int(line.split("=", 1)[1])
        elif line.strip():
            print(line)
    return killed


def _remove_tree(target: Path, lesson_dir: Path) -> None:
    """Remove a directory tree, recovering from common Windows file locks."""
    try:
        shutil.rmtree(target, onerror=_clear_readonly_and_retry)
        return
    except PermissionError:
        print(f"  Detected file lock while removing {target.name}/")

    killed = _kill_lesson_node_processes(lesson_dir)
    if killed:
        time.sleep(1)
        shutil.rmtree(target, onerror=_clear_readonly_and_retry)
        return

    raise PermissionError(
        f"Unable to remove {target}. Close lesson-scoped Node/Vite processes and retry."
    )


def clean(lesson_dir: Path) -> None:
    """Remove copied app source and build artifacts."""
    for name in ("src", "node_modules", "dist"):
        target = lesson_dir / name
        if target.is_dir():
            _remove_tree(target, lesson_dir)
            if not target.exists():
                print(f"  Removed {name}/")
    for name in (".env",):
        target = lesson_dir / name
        if target.is_file():
            target.unlink()
            print(f"  Removed {name}")
    for db in lesson_dir.glob("*.db"):
        db.unlink()
        print(f"  Removed {db.name}")


def setup(lesson_dir: Path, app_source: Path, title: str) -> None:
    """Clean workspace then copy Loan Workbench app into src/."""
    _print_banner(title)
    clean(lesson_dir)
    if not app_source.exists():
        print(f"ERROR: App source not found at {app_source}", file=sys.stderr)
        sys.exit(1)
    shutil.copytree(
        app_source,
        lesson_dir / "src",
        ignore=shutil.ignore_patterns("node_modules", ".env", "*.db", "data"),
    )
    print("  Copied app/ → src/")

    _create_env_interactive(lesson_dir)
    src_dir = lesson_dir / "src"
    _repair_package_json(src_dir)
    _ensure_dependencies(src_dir)
    _seed_database(src_dir)

    print(
        f"\n{BRAND_COLORS['green']}✓ Setup complete.{BRAND_COLORS['reset']} "
        "Dependencies installed and demo data seeded. Run: python util.py --run"
    )


def run(lesson_dir: Path, title: str) -> None:
    """Install dependencies (if needed) and start the dev servers."""
    src_dir = lesson_dir / "src"
    if not src_dir.exists():
        print(f"ERROR: src/ not found. Run --setup first.", file=sys.stderr)
        sys.exit(1)

    _print_banner(f"{title} — Starting...")

    _repair_package_json(src_dir)
    _ensure_dependencies(src_dir)

    # Seed database if no .db file exists
    data_dir = src_dir / "data"
    db_files = list(data_dir.glob("*.db")) if data_dir.exists() else []
    if not db_files:
        _seed_database(src_dir)

    print("  Starting backend (API) + frontend (Vite)...\n")
    print("  Backend  → http://localhost:3100")
    print("  Frontend → http://localhost:5173")
    print("  Press Ctrl+C to stop.\n")

    try:
        subprocess.run(
            ["npm", "run", "dev"],
            cwd=str(src_dir),
            check=True,
            shell=(os.name == "nt"),
        )
    except KeyboardInterrupt:
        print("\n  Stopped.")


def compare_with_expected(change_dir: Path, changed: dict[str, list[str]]) -> dict[str, object]:
    """Compare actual changed-files against expected-files.json and expected-patterns.json.

    Returns a comparison report dict with match/mismatch details.
    """
    import re as _re

    report: dict[str, object] = {"files_match": False, "patterns_match": False, "details": []}

    expected_files_path = change_dir / "expected-files.json"
    if expected_files_path.exists():
        expected = json.loads(expected_files_path.read_text(encoding="utf-8"))
        actual_added = set(changed.get("added", []))
        actual_modified = set(changed.get("modified", []))
        actual_deleted = set(changed.get("deleted", []))
        expected_added = set(expected.get("added", []))
        expected_modified = set(expected.get("modified", []))
        expected_deleted = set(expected.get("deleted", []))

        files_match = (
            actual_added == expected_added
            and actual_modified == expected_modified
            and actual_deleted == expected_deleted
        )
        report["files_match"] = files_match

        if not files_match:
            if actual_added != expected_added:
                report["details"].append(f"Added files — expected: {sorted(expected_added)}, actual: {sorted(actual_added)}")
            if actual_modified != expected_modified:
                report["details"].append(f"Modified files — expected: {sorted(expected_modified)}, actual: {sorted(actual_modified)}")
            if actual_deleted != expected_deleted:
                report["details"].append(f"Deleted files — expected: {sorted(expected_deleted)}, actual: {sorted(actual_deleted)}")
        else:
            report["details"].append("File manifest matches expected.")

        # Check for zero changes when changes are expected
        if (expected_added or expected_modified or expected_deleted) and not any(changed.values()):
            report["details"].append("ERROR: Expected code changes but got 0 changes.")
    else:
        report["details"].append("No expected-files.json found — skipping file manifest comparison.")

    expected_patterns_path = change_dir / "expected-patterns.json"
    patch_path = change_dir / "demo.patch"
    if expected_patterns_path.exists() and patch_path.exists():
        patterns = json.loads(expected_patterns_path.read_text(encoding="utf-8"))
        patch_text = patch_path.read_text(encoding="utf-8", errors="replace")
        all_matched = True
        for entry in patterns:
            pattern = entry.get("pattern", "")
            description = entry.get("description", pattern)
            if _re.search(pattern, patch_text, _re.IGNORECASE):
                report["details"].append(f"Pattern matched: {description}")
            else:
                report["details"].append(f"Pattern MISSING: {description}")
                all_matched = False
        report["patterns_match"] = all_matched
    else:
        report["details"].append("No expected-patterns.json or demo.patch — skipping pattern comparison.")

    # Write comparison report
    comparison_path = change_dir / "comparison.md"
    lines = ["# Actual vs Expected Comparison\n"]
    lines.append(f"- **Files match:** {report['files_match']}")
    lines.append(f"- **Patterns match:** {report['patterns_match']}\n")
    lines.append("## Details\n")
    for detail in report["details"]:
        lines.append(f"- {detail}")
    comparison_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return report


def main(
    lesson_num: str,
    lesson_title: str,
    lesson_dir: Path,
    app_source: Path,
    extra_commands: dict[str, tuple[str, Callable[[], int | None]]] | None = None,
) -> None:
    """Common CLI entry point for all lesson util.py files."""
    title = f"Lesson {lesson_num} — {lesson_title}"
    p = argparse.ArgumentParser(description=f"{title} workspace utility")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--setup", action="store_true", help="Clean + copy app source + create .env")
    g.add_argument("--clean", action="store_true", help="Remove copied src/ and artifacts")
    g.add_argument("--run", action="store_true", help="Install deps + start backend & frontend")
    for command_name, (help_text, _) in (extra_commands or {}).items():
        g.add_argument(f"--{command_name}", action="store_true", help=help_text)
    args = p.parse_args()

    if args.setup:
        setup(lesson_dir, app_source, title)
    elif args.run:
        run(lesson_dir, title)
    elif extra_commands:
        for command_name, (_help_text, handler) in extra_commands.items():
            if getattr(args, command_name, False):
                result = handler()
                if isinstance(result, int):
                    raise SystemExit(result)
                return
    else:
        clean(lesson_dir)
