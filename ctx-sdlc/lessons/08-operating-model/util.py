#!/usr/bin/env python3
"""Lesson 08 — Operating Model workspace utility.

Usage:
  python util.py --setup    Copy app source into src/, create .env interactively
  python util.py --run      Install deps + start backend & frontend dev servers
  python util.py --clean    Remove copied src/ and build artifacts
  python util.py --demo     Run a Copilot CLI context-maintenance demo and capture artifacts
"""

from __future__ import annotations

import difflib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

MODEL_OVERRIDE_FLAG = "--model"
LESSON = Path(__file__).resolve().parent
APP_SOURCE = LESSON.parent.parent / "app"
CONFIG_PATH = LESSON.parent / "_common" / "assessment-config.json"
OUTPUT_DIR = LESSON / ".output"
LOG_DIR = OUTPUT_DIR / "logs"
CHANGE_DIR = OUTPUT_DIR / "change"
KEPT_LOG_FILES = {"command.txt", "prompt.txt", "session.md", "copilot.log"}
RUNNER_LOG_PATH = LOG_DIR / "runner.log"
DRIFTED_EXAMPLE_PATH = LESSON / ".github" / "examples" / "drifted" / "copilot-instructions.md"
DRIFTED_EXAMPLE_BASELINE = """# Loan Workbench — Project Context

> **This file intentionally contains drift for Lesson 08.**

## Project

Loan Workbench API — TypeScript + Express REST service managing loan
application lifecycles with regulatory compliance, role-based access, and
audit-first persistence.

## Tech Stack

- Runtime: Node.js 18 LTS
- Language: TypeScript 5.x (strict mode)
- Framework: Express 4
- Tests: Vitest
- Modules: ESM only
- Logging: structured JSON via winston
- Database: Prisma ORM
- Deploy: Azure Container Apps

## Architecture

Three-layer separation:

1. **Routes** — HTTP handling, parameter extraction, delegation
2. **Rules** — pure business logic, no I/O
3. **Services** — persistence, external integrations, audit

Request flow: Route -> authenticate -> authorize -> validate -> Rule ->
Service -> respond.

Audit events are recorded before persistence. Use `console.log()` for quick
debugging, but prefer structured logging in long-lived services.

## Coding Conventions

- `const` over `let`; never `var`
- All route handlers are `async`
- All errors return structured JSON: `{ error: string, code: string }`
- No stack traces in error responses
- Feature flags use 404, not 403
- Shared helpers live in `app/backend/src/helpers/`
- Keep global instructions concise, but include this example route snippet:

```ts
app.post('/notifications', async (req, res) => {
  console.log('saving notification preferences');
  res.status(202).json({ ok: true });
});
```

## References

- Canonical project context: see `.github/copilot-instructions.md`
- Maintenance cadence: see `/docs/maintenance-schedule.md`
- Lesson scope and expected output: see `/docs/operating-model-example.md`
- Context audit script: see `.github/scripts/audit_context.py`
- Stale reference detector: see `.github/scripts/detect_stale_refs.py`
- Healthy reference example: see `.github/examples/clean/copilot-instructions.md`
"""
TEXT_EXTENSIONS = {
  ".css", ".html", ".js", ".json", ".md", ".mjs", ".py", ".ts", ".tsx", ".txt", ".yaml", ".yml",
}

sys.path.insert(0, str(LESSON.parent / "_common"))
from util_base import clean, compare_with_expected, main  # noqa: E402


def _extract_model_override(argv: list[str]) -> tuple[list[str], str | None]:
  if MODEL_OVERRIDE_FLAG not in argv:
    return argv, None
  index = argv.index(MODEL_OVERRIDE_FLAG)
  if index + 1 >= len(argv):
    raise SystemExit("ERROR: --model requires a value.")
  model_name = argv[index + 1]
  trimmed = argv[:index] + argv[index + 2 :]
  return trimmed, model_name


sys.argv, _MODEL_OVERRIDE = _extract_model_override(sys.argv)
if _MODEL_OVERRIDE:
  os.environ["CTX_SDLC_COPILOT_MODEL"] = _MODEL_OVERRIDE


def _load_assessment_config() -> dict[str, object]:
  if not CONFIG_PATH.exists():
    return {}
  return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


ASSESSMENT_CONFIG = _load_assessment_config()
DEMO_TIMEOUT_SECONDS = int(os.environ.get("CTX_SDLC_DEMO_TIMEOUT", str(ASSESSMENT_CONFIG.get("defaultDemoTimeoutSeconds", 180))))
DEMO_MODEL = os.environ.get("CTX_SDLC_COPILOT_MODEL", str(ASSESSMENT_CONFIG.get("defaultAssessmentModel", "claude-haiku-4.5")))


def _is_text_file(path: Path) -> bool:
  return path.suffix.lower() in TEXT_EXTENSIONS


def _snapshot_tree(root: Path) -> dict[str, str]:
  snapshot: dict[str, str] = {}
  if not root.exists():
    return snapshot
  for path in sorted(root.rglob("*")):
    if not path.is_file() or not _is_text_file(path):
      continue
    if any(part in {"node_modules", "dist", "data", ".git", ".output"} for part in path.parts):
      continue
    snapshot[path.relative_to(root).as_posix()] = path.read_text(encoding="utf-8")
  return snapshot


def _reset_output_dirs() -> None:
  preserved_expected = {
    path.name: path.read_text(encoding="utf-8")
    for path in CHANGE_DIR.glob("expected-*.json")
  }
  for directory in (LOG_DIR, CHANGE_DIR):
    if directory.exists():
      shutil.rmtree(directory)
    directory.mkdir(parents=True, exist_ok=True)
  for name, content in preserved_expected.items():
    _write_text_atomic(CHANGE_DIR / name, content)


def _reset_demo_workspace() -> Path:
  clean(LESSON)
  _write_text_atomic(DRIFTED_EXAMPLE_PATH, DRIFTED_EXAMPLE_BASELINE)
  src_dir = LESSON / "src"
  shutil.copytree(APP_SOURCE, src_dir, ignore=shutil.ignore_patterns("node_modules", ".env", "*.db", "data"))
  return src_dir


def _demo_prompt() -> str:
  return (
    "Inspect the lesson's context-maintenance artifacts before answering. "
    "Discover the relevant project instructions, audit scripts, clean and drifted examples, and maintenance docs that exist here rather than assuming a fixed file list. "
    "Then fix the drifted example at .github/examples/drifted/copilot-instructions.md by resolving all drift issues you find. "
    "Specifically: update stale technology references (Node.js version, logging library), remove contradictory rules (console.log vs structured logging), "
    "fix dead file path references (deleted helpers directory), remove over-specified inline code blocks that belong in scoped instructions, "
    "and align the drifted file with the clean example's conventions for accuracy and conciseness. "
    "Apply the fixes directly in the file. Do not run shell commands and do not use SQL."
  )


def _resolve_copilot_executable() -> str:
  copilot_executable = shutil.which("copilot.cmd") or shutil.which("copilot.bat") or shutil.which("copilot")
  if copilot_executable is None:
    raise FileNotFoundError("Could not resolve the Copilot CLI executable on PATH.")
  return copilot_executable


def _validate_demo_model() -> str:
  if not DEMO_MODEL.strip():
    raise RuntimeError("Assessment model configuration is empty.")
  return DEMO_MODEL


def _write_text_atomic(path: Path, content: str) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=path.parent, prefix=f".{path.name}.", suffix=".tmp") as handle:
    handle.write(content)
    temp_path = Path(handle.name)
  temp_path.replace(path)


def _write_json(path: Path, payload: object) -> None:
  _write_text_atomic(path, json.dumps(payload, indent=2) + "\n")


def _write_diff(before: dict[str, str], after: dict[str, str]) -> dict[str, list[str]]:
  keys = sorted(set(before) | set(after))
  patch_chunks: list[str] = []
  changed = {"added": [], "modified": [], "deleted": []}
  for key in keys:
    old_text = before.get(key)
    new_text = after.get(key)
    if old_text == new_text:
      continue
    if old_text is None:
      changed["added"].append(key)
    elif new_text is None:
      changed["deleted"].append(key)
    else:
      changed["modified"].append(key)
    diff = difflib.unified_diff((old_text or "").splitlines(keepends=True), (new_text or "").splitlines(keepends=True), fromfile=f"a/{key}", tofile=f"b/{key}", n=3)
    patch_chunks.append("".join(diff))
  _write_text_atomic(CHANGE_DIR / "demo.patch", "\n".join(chunk for chunk in patch_chunks if chunk))
  _write_json(CHANGE_DIR / "changed-files.json", changed)
  return changed


def _wait_for_fresh_artifacts(run_started_at: float) -> None:
  required_paths = [LOG_DIR / "command.txt", LOG_DIR / "prompt.txt", LOG_DIR / "session.md", LOG_DIR / "copilot.log", CHANGE_DIR / "demo.patch", CHANGE_DIR / "changed-files.json"]
  stable_hits = 0
  previous_state: tuple[tuple[str, int, int], ...] | None = None
  deadline = time.time() + 15
  while time.time() < deadline:
    if not all(path.exists() for path in required_paths):
      time.sleep(0.5)
      continue
    current_state = tuple((str(path), path.stat().st_size, int(path.stat().st_mtime_ns)) for path in required_paths)
    if any(state[2] < int(run_started_at * 1_000_000_000) for state in current_state):
      time.sleep(0.5)
      previous_state = current_state
      stable_hits = 0
      continue
    if current_state == previous_state:
      stable_hits += 1
    else:
      stable_hits = 0
      previous_state = current_state
    if stable_hits >= 2:
      return
    time.sleep(0.5)


def _kill_process_tree(pid: int) -> None:
  if os.name == "nt":
    subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True, check=False, shell=False)
    return
  try:
    os.kill(pid, 9)
  except ProcessLookupError:
    return


def _finalize_log_dir() -> None:
  process_logs = sorted(LOG_DIR.glob("process-*.log"), key=lambda path: path.stat().st_mtime, reverse=True)
  target_log = LOG_DIR / "copilot.log"
  if target_log.exists():
    target_log.unlink()
  if process_logs:
    process_logs[0].replace(target_log)
    process_logs = process_logs[1:]
    if RUNNER_LOG_PATH.exists() and RUNNER_LOG_PATH.stat().st_size > 0:
      existing = target_log.read_text(encoding="utf-8", errors="replace")
      runner_text = RUNNER_LOG_PATH.read_text(encoding="utf-8", errors="replace")
      target_log.write_text(existing + "\n\n--- Runner Output ---\n" + runner_text, encoding="utf-8")
  elif RUNNER_LOG_PATH.exists():
    RUNNER_LOG_PATH.replace(target_log)
  for extra_log in process_logs:
    extra_log.unlink()
  for path in list(LOG_DIR.iterdir()):
    if path.name in KEPT_LOG_FILES:
      continue
    if path.is_dir():
      shutil.rmtree(path)
    else:
      path.unlink()


def _run_copilot_demo(prompt: str, src_dir: Path, copilot_executable: str, demo_model: str) -> tuple[int, str]:
  session_path = LOG_DIR / "session.md"
  command = [copilot_executable, "--model", demo_model, "--log-dir", str(LOG_DIR), "--log-level", "debug", "--stream", "off", "--share", str(LOG_DIR / "session.md"), "--add-dir", str(src_dir), "--allow-all-tools", "--allow-all-paths", "--deny-tool=powershell", "--deny-tool=sql", "--no-ask-user"]
  command.extend(["-p", prompt])
  _write_text_atomic(LOG_DIR / "prompt.txt", prompt + "\n")
  _write_text_atomic(LOG_DIR / "command.txt", " ".join(command) + "\n")
  with open(RUNNER_LOG_PATH, "wb") as runner_log:
    process = subprocess.Popen(command, cwd=str(LESSON), stdout=runner_log, stderr=subprocess.STDOUT, shell=False)
    deadline = time.time() + DEMO_TIMEOUT_SECONDS
    last_size = -1
    stable_hits = 0
    session_export_detected = False
    while time.time() < deadline:
      if session_path.exists():
        current_size = session_path.stat().st_size
        if current_size > 0 and current_size == last_size:
          stable_hits += 1
        else:
          stable_hits = 0
          last_size = current_size
        if stable_hits >= 2:
          session_export_detected = True
          break
      if process.poll() is not None:
        break
      time.sleep(2)
    return_code = process.poll()
    if session_export_detected:
      if return_code is None:
        _kill_process_tree(process.pid)
        try:
          process.wait(timeout=10)
        except subprocess.TimeoutExpired:
          _kill_process_tree(process.pid)
      result = (0, "session-export-detected")
    elif return_code is None:
      _kill_process_tree(process.pid)
      try:
        process.wait(timeout=10)
      except subprocess.TimeoutExpired:
        _kill_process_tree(process.pid)
      result = (124, "timeout")
    else:
      result = (return_code, "completed" if return_code == 0 else "failed")
  _finalize_log_dir()
  return result


def demo() -> int:
  print("Running lesson 08 Copilot CLI demo...")
  try:
    copilot_executable = _resolve_copilot_executable()
    demo_model = _validate_demo_model()
  except (FileNotFoundError, RuntimeError) as exc:
    print(f"ERROR: {exc}")
    return 3
  print(f"Using GitHub Copilot CLI model: {demo_model}")
  run_started_at = time.time()
  src_dir = _reset_demo_workspace()
  _reset_output_dirs()
  before = _snapshot_tree(LESSON)
  prompt = _demo_prompt()
  return_code, status = _run_copilot_demo(prompt, src_dir, copilot_executable, demo_model)
  after = _snapshot_tree(LESSON)
  changed = _write_diff(before, after)
  _wait_for_fresh_artifacts(run_started_at)
  if return_code == 124:
    print("ERROR: Copilot CLI did not export a completed session before timeout. See .output/logs/copilot.log.")
    return return_code
  if return_code != 0:
    print("ERROR: Copilot CLI demo failed. See .output/logs for details.")
    return return_code
  if not any(changed.values()):
    print("NOTE: Copilot completed but did not modify tracked text files.")
    return 2

  report = compare_with_expected(CHANGE_DIR, changed)
  if not report["files_match"]:
    print("WARNING: Actual file changes do not match expected. See .output/change/comparison.md.")
  if not report["patterns_match"]:
    print("WARNING: Some expected patterns not found in patch. See .output/change/comparison.md.")

  if status == "session-export-detected":
    print("Demo complete. Session export detected; Copilot process tree was terminated cleanly.")
    return 0
  print("Demo complete. Review .output/logs and .output/change.")
  return 0


if __name__ == "__main__":
  main("08", "Operating Model", LESSON, APP_SOURCE, extra_commands={"demo": ("Run a Copilot CLI context-maintenance demo and capture logs plus a git-style diff", demo)})
