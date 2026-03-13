#!/usr/bin/env python3
"""Shared lesson utility — used by all per-lesson util.py files.

Provides setup (copy app → src/, create .env interactively), clean, and run
commands for the Loan Workbench example app.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


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


def clean(lesson_dir: Path) -> None:
    """Remove copied app source and build artifacts."""
    for name in ("src", "node_modules", "dist"):
        target = lesson_dir / name
        if target.is_dir():
            shutil.rmtree(target)
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
    print(f"{title}\n")
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

    print("\n✓ Setup complete. Run: python util.py --run")


def run(lesson_dir: Path, title: str) -> None:
    """Install dependencies (if needed) and start the dev servers."""
    src_dir = lesson_dir / "src"
    if not src_dir.exists():
        print(f"ERROR: src/ not found. Run --setup first.", file=sys.stderr)
        sys.exit(1)

    print(f"{title} — Starting...\n")

    _repair_package_json(src_dir)

    node_modules = src_dir / "node_modules"
    if not node_modules.exists():
        print("  Installing dependencies...")
        subprocess.run(
            ["npm", "install"],
            cwd=str(src_dir),
            check=True,
            shell=(os.name == "nt"),
        )
        print()

    # Seed database if no .db file exists
    data_dir = src_dir / "data"
    db_files = list(data_dir.glob("*.db")) if data_dir.exists() else []
    if not db_files:
        print("  Seeding database...")
        subprocess.run(
            ["npm", "run", "db:seed"],
            cwd=str(src_dir),
            check=True,
            shell=(os.name == "nt"),
        )
        print()

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


def main(lesson_num: str, lesson_title: str, lesson_dir: Path, app_source: Path) -> None:
    """Common CLI entry point for all lesson util.py files."""
    title = f"Lesson {lesson_num} — {lesson_title}"
    p = argparse.ArgumentParser(description=f"{title} workspace utility")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--setup", action="store_true", help="Clean + copy app source + create .env")
    g.add_argument("--clean", action="store_true", help="Remove copied src/ and artifacts")
    g.add_argument("--run", action="store_true", help="Install deps + start backend & frontend")
    args = p.parse_args()

    if args.setup:
        setup(lesson_dir, app_source, title)
    elif args.run:
        run(lesson_dir, title)
    else:
        clean(lesson_dir)
