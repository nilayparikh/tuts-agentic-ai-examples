#!/usr/bin/env python3
"""Shared utilities for ctx-sdlc lesson setup and validation scripts."""

import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

COURSE_ROOT = Path(__file__).resolve().parent.parent
APPS_DIR = COURSE_ROOT / "apps"


def _find_copilot() -> str:
    """Resolve the copilot CLI executable path."""
    # Prefer npm global install (.cmd works reliably with shell=True)
    npm_global = Path(os.environ.get("APPDATA", "")) / "npm" / "copilot.cmd"
    if npm_global.exists():
        return str(npm_global)
    # Fall back to whatever shutil.which finds (.bat, .exe, etc.)
    found = shutil.which("copilot")
    if found:
        return found
    return "copilot"  # let subprocess raise FileNotFoundError

# Model presets — use GPT-5.4 for validation, lighter models for quick tasks
MODEL_HEAVY = "gpt-5.4"           # full validation scenarios
MODEL_LIGHT = "claude-sonnet-4.6"  # quick / small tasks
MODEL_FAST  = "gemini-3-flash"     # fastest option for trivial checks


# ---------------------------------------------------------------------------
# Workspace setup helpers
# ---------------------------------------------------------------------------

def _rm_readonly(func, path, _exc_info):
    """Error handler for shutil.rmtree — clears read-only flag and retries."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def clean_workspace(workdir: Path, *, keep: set[str] | None = None) -> None:
    """Remove template-sourced directories and runtime artifacts from a lesson workspace."""
    keep = keep or set()
    for d in ("src", "node_modules", "dist"):
        if d in keep:
            continue
        target = workdir / d
        if target.exists():
            shutil.rmtree(target, onerror=_rm_readonly)
            print(f"  Removed {d}/")
    for f in (".env",):
        if f in keep:
            continue
        target = workdir / f
        if target.exists():
            target.unlink()
            print(f"  Removed {f}")
    # Remove any sqlite database files
    for db_file in workdir.glob("*.db"):
        db_file.unlink()
        print(f"  Removed {db_file.name}")


def copy_template(workdir: Path, template: str = "complex") -> None:
    """Copy a template app into the lesson's src/ subdirectory."""
    src = APPS_DIR / template
    if not src.exists():
        print(f"ERROR: Template '{template}' not found at {src}", file=sys.stderr)
        sys.exit(1)
    dest = workdir / "src"
    if dest.exists():
        shutil.rmtree(dest, onerror=_rm_readonly)
    shutil.copytree(src, dest, dirs_exist_ok=True)
    print(f"  Copied {template}/ → src/")


def copy_overlay(source: Path, target: Path) -> None:
    """Recursively copy overlay files from *source* into *target*, preserving directory structure."""
    for src_file in source.rglob("*"):
        if src_file.is_file():
            rel = src_file.relative_to(source)
            dest = target / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dest)
            print(f"  + {rel}")


def clean_context(workdir: Path) -> None:
    """Remove all context directories (.github/, docs/, specs/, scripts/) from workdir."""
    for d in (".github", "docs", "cli", "specs", "scripts", "checklists", "examples"):
        target = workdir / d
        if target.exists():
            shutil.rmtree(target)


def ensure_output_dir(workdir: Path) -> Path:
    """Ensure the output/ directory exists and return its path."""
    out = workdir / "output"
    out.mkdir(parents=True, exist_ok=True)
    return out


# ---------------------------------------------------------------------------
# Copilot CLI helpers
# ---------------------------------------------------------------------------

def run_copilot(
    prompt: str,
    workdir: Path,
    *,
    model: str = MODEL_HEAVY,
    custom_instructions: bool = True,
    output_file: Path | None = None,
    log_dir: Path | None = None,
    timeout: int = 300,
) -> tuple[int, str, str]:
    """Run GitHub Copilot CLI non-interactively and return (returncode, stdout, stderr).

    When *log_dir* is provided the CLI writes debug-level logs (thinking,
    context, tool calls) into that directory.
    """
    copilot = _find_copilot()
    cmd = [copilot, "-p", prompt, "--allow-all", "-s", "--model", model]
    if not custom_instructions:
        cmd.append("--no-custom-instructions")
    if output_file:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        cmd.extend(["--share", str(output_file)])
    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        cmd.extend(["--log-dir", str(log_dir), "--log-level", "debug"])
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=workdir, timeout=timeout,
            shell=(sys.platform == "win32"),  # .cmd/.bat need shell on Windows
            encoding="utf-8", errors="replace",
        )
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError:
        print(
            "ERROR: 'copilot' CLI not found. "
            "Install from https://docs.github.com/copilot/how-tos/copilot-cli",
            file=sys.stderr,
        )
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print(f"WARNING: copilot timed out after {timeout}s", file=sys.stderr)
        return 1, "", "Timeout"


def print_result(name: str, output: str, output_file: Path | None = None) -> None:
    """Print a scenario result summary."""
    print(f"\n{'─' * 60}")
    print(f"  {name}")
    print(f"{'─' * 60}")
    preview = output.strip()[:500]
    if preview:
        print(preview)
    else:
        print("  (no output)")
    if output_file and output_file.exists():
        print(f"\n  Full session saved to: {output_file}")


def print_setup_complete(*, install: bool = True) -> None:
    """Print standard next-steps message after setup."""
    print("\n✓ Setup complete. Next steps:")
    if install:
        print("  cd src && npm install")
    print("  # Open lesson folder in VS Code — Copilot auto-loads .github/ context")
    print("  # Or use CLI:")
    print('  copilot -p "your prompt" --allow-all')
