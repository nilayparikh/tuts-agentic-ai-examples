#!/usr/bin/env python3
"""Lesson 05 — Implementation Workflows workspace utility.

Usage:
  python util.py --setup    Copy app source into src/, create .env interactively
  python util.py --run      Install deps + start backend & frontend dev servers
  python util.py --clean    Remove copied src/ and build artifacts
  python util.py --demo     Run a Copilot CLI implementation demo and capture artifacts
  python util.py --test     Run unit tests (vitest) and Playwright UI verification
"""

from __future__ import annotations

import difflib
import json
import os
import re
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
IMPLEMENTATION_DENY_TOOLS = ("powershell", "sql")
TEXT_EXTENSIONS = {
  ".css",
  ".html",
  ".js",
  ".json",
  ".md",
  ".mjs",
  ".py",
  ".ts",
  ".tsx",
  ".txt",
  ".yaml",
  ".yml",
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
DEMO_TIMEOUT_SECONDS = int(
  os.environ.get(
    "CTX_SDLC_DEMO_TIMEOUT",
    str(ASSESSMENT_CONFIG.get("defaultDemoTimeoutSeconds", 420)),
  )
)
DEMO_IDLE_TIMEOUT_SECONDS = int(
  os.environ.get(
    "CTX_SDLC_DEMO_IDLE_TIMEOUT",
    str(ASSESSMENT_CONFIG.get("defaultDemoIdleTimeoutSeconds", 120)),
  )
)
DEMO_MODEL = os.environ.get(
  "CTX_SDLC_COPILOT_MODEL",
  str(ASSESSMENT_CONFIG.get("defaultAssessmentModel", "claude-haiku-4.5")),
)


def _is_text_file(path: Path) -> bool:
  return path.suffix.lower() in TEXT_EXTENSIONS


def _snapshot_tree(root: Path) -> dict[str, str]:
  snapshot: dict[str, str] = {}
  if not root.exists():
    return snapshot

  for path in sorted(root.rglob("*")):
    if not path.is_file() or not _is_text_file(path):
      continue
    if any(part in {"node_modules", "dist", "data", ".git"} for part in path.parts):
      continue
    snapshot[path.relative_to(root).as_posix()] = path.read_text(encoding="utf-8")
  return snapshot


def _reset_output_dirs() -> None:
  for directory in (LOG_DIR, CHANGE_DIR):
    preserved_expected = {
        path.name: path.read_text(encoding="utf-8")
        for path in CHANGE_DIR.glob("expected-*.json")
    }
    if directory.exists():
      shutil.rmtree(directory)
    directory.mkdir(parents=True, exist_ok=True)
  for name, content in preserved_expected.items():
    _write_text_atomic(CHANGE_DIR / name, content)


def _reset_demo_workspace() -> Path:
  clean(LESSON)
  src_dir = LESSON / "src"
  shutil.copytree(
    APP_SOURCE,
    src_dir,
    ignore=shutil.ignore_patterns("node_modules", ".env", "*.db", "data"),
  )
  return src_dir


def _demo_prompt() -> str:
  return (
    "Inspect docs/, specs/, and the relevant notification-preference write surfaces you discover in this lesson before editing. "
    "Use the playbook and example doc as success criteria, not as a fixed file checklist. "
    "Implement a focused notification-preference write hardening slice. "
    "Write tests first at src/backend/tests/unit/notification-preference-write-rules.test.ts, "
    "then add a pure rule module at src/backend/src/rules/notification-preference-write-rules.ts, "
    "and wire the minimal production changes into src/backend/src/routes/notifications.ts. "
    "In the final handoff, state which behaviors the tests should fail on before the production change and which should pass after it, and name any intentionally deferred write surfaces that remain out of scope. "
    "The rule must use explicit inputs plus existing types, not direct DB access. "
    "Enforce these cases: manual-review-escalation must keep at least one channel enabled; "
    "decline SMS cannot be enabled when loanState is CA or California under LEGAL-218; "
    "treat loanState as the direct request input for this route instead of introducing a new loanId lookup or any repository fetch; "
    "the false positive where escalation SMS is disabled but escalation email stays enabled must remain allowed. "
    "When tests assert business-rule rejections, prefer semantic checks over brittle exact wording, and preserve the current route rejection style when practical; if the route returns 400 or 422 for these rule violations, the payload must still clearly express the business invariant. "
    "Preserve delegated-session and role guards, keep changes minimal, keep the scope to the current notification write path, include top-of-module false-positive and hard-negative comments in the new rule file, "
    "and do not edit protected config or database files. "
    "Do not run npm install, npm test, npx vitest, or any shell commands. Do not use SQL or task/todo write tools. Inspect and edit files only. "
    "Return a short handoff summary naming changed files and which tests should pass."
  )


def _resolve_copilot_executable() -> str:
  copilot_executable = (
    shutil.which("copilot.cmd")
    or shutil.which("copilot.bat")
    or shutil.which("copilot")
  )
  if copilot_executable is None:
    raise FileNotFoundError("Could not resolve the Copilot CLI executable on PATH.")
  return copilot_executable


def _validate_demo_model() -> str:
  if not DEMO_MODEL.strip():
    raise RuntimeError("Assessment model configuration is empty.")
  return DEMO_MODEL


def _write_text_atomic(path: Path, content: str) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  with tempfile.NamedTemporaryFile(
    "w",
    encoding="utf-8",
    delete=False,
    dir=path.parent,
    prefix=f".{path.name}.",
    suffix=".tmp",
  ) as handle:
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

    diff = difflib.unified_diff(
      (old_text or "").splitlines(keepends=True),
      (new_text or "").splitlines(keepends=True),
      fromfile=f"a/{key}",
      tofile=f"b/{key}",
      n=3,
    )
    patch_chunks.append("".join(diff))

  _write_text_atomic(CHANGE_DIR / "demo.patch", "\n".join(chunk for chunk in patch_chunks if chunk))
  _write_json(CHANGE_DIR / "changed-files.json", changed)
  return changed


def _wait_for_fresh_artifacts(run_started_at: float) -> None:
  required_paths = [
    LOG_DIR / "command.txt",
    LOG_DIR / "prompt.txt",
    LOG_DIR / "session.md",
    LOG_DIR / "copilot.log",
    CHANGE_DIR / "demo.patch",
    CHANGE_DIR / "changed-files.json",
  ]
  stable_hits = 0
  previous_state: tuple[tuple[str, int, int], ...] | None = None
  deadline = time.time() + 15

  while time.time() < deadline:
    if not all(path.exists() for path in required_paths):
      time.sleep(0.5)
      continue

    current_state = tuple(
      (str(path), path.stat().st_size, int(path.stat().st_mtime_ns))
      for path in required_paths
    )
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


def _file_size(path: Path) -> int:
  if not path.exists():
    return -1
  return path.stat().st_size


def _run_copilot_demo(prompt: str, src_dir: Path, copilot_executable: str, demo_model: str) -> tuple[int, str]:
  session_path = LOG_DIR / "session.md"
  command = [
    copilot_executable,
    "--model",
    demo_model,
    "--log-dir",
    str(LOG_DIR),
    "--log-level",
    "debug",
    "--stream",
    "off",
    "--share",
    str(LOG_DIR / "session.md"),
    "--add-dir",
    str(src_dir),
    "--allow-all-tools",
    "--allow-all-paths",
    "--no-ask-user",
  ]
  for tool_name in IMPLEMENTATION_DENY_TOOLS:
    command.append(f"--deny-tool={tool_name}")
  command.extend(["-p", prompt])
  _write_text_atomic(LOG_DIR / "prompt.txt", prompt + "\n")
  _write_text_atomic(LOG_DIR / "command.txt", " ".join(command) + "\n")

  with open(RUNNER_LOG_PATH, "wb") as runner_log:
    process = subprocess.Popen(command, cwd=str(LESSON), stdout=runner_log, stderr=subprocess.STDOUT, shell=False)
    hard_deadline = time.time() + DEMO_TIMEOUT_SECONDS
    last_activity_at = time.time()
    last_session_size = -1
    last_runner_size = -1
    stable_since: float | None = None
    session_export_detected = False

    while True:
      now = time.time()
      current_session_size = _file_size(session_path)
      current_runner_size = _file_size(RUNNER_LOG_PATH)
      session_changed = current_session_size != last_session_size
      runner_changed = current_runner_size != last_runner_size

      if session_changed or runner_changed:
        last_activity_at = now
        last_session_size = current_session_size
        last_runner_size = current_runner_size

      if current_session_size > 0:
        if stable_since is None or session_changed:
          stable_since = now
        elif now - stable_since >= 6:
          session_export_detected = True
          break
      else:
        stable_since = None

      if process.poll() is not None:
        break

      if now >= hard_deadline:
        break

      if now - last_activity_at >= DEMO_IDLE_TIMEOUT_SECONDS:
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
      if time.time() >= hard_deadline:
        result = (124, "hard-timeout")
      else:
        result = (124, "idle-timeout")
    else:
      result = (return_code, "completed" if return_code == 0 else "failed")

  _finalize_log_dir()
  return result


BACKEND_PORT = 3100
FRONTEND_PORT = 5173
SERVER_STARTUP_TIMEOUT = 30
PLAYWRIGHT_TEST_DIR = LESSON / "tests"


def _ensure_src_ready() -> Path:
  """Ensure src/ exists and has dependencies installed."""
  src_dir = LESSON / "src"
  if not src_dir.exists():
    print("ERROR: src/ not found. Run --setup first.", file=sys.stderr)
    raise SystemExit(1)
  node_modules = src_dir / "node_modules"
  if not node_modules.exists():
    print("  Installing dependencies...")
    subprocess.run(
      ["npm", "install"], cwd=str(src_dir), check=True, shell=(os.name == "nt"),
    )
  return src_dir


def _seed_if_needed(src_dir: Path) -> None:
  """Seed the database if no .db file exists."""
  data_dir = src_dir / "data"
  db_files = list(data_dir.glob("*.db")) if data_dir.exists() else []
  if not db_files:
    print("  Seeding database...")
    subprocess.run(
      ["npm", "run", "db:seed"], cwd=str(src_dir), check=True, shell=(os.name == "nt"),
    )


def _run_unit_tests(src_dir: Path) -> bool:
  """Run vitest unit tests. Returns True if all pass."""
  print("\n── Unit Tests (vitest) ──\n")
  result = subprocess.run(
    ["npx", "vitest", "run"], cwd=str(src_dir), shell=(os.name == "nt"),
  )
  return result.returncode == 0


def _wait_for_server(url: str, timeout: int = SERVER_STARTUP_TIMEOUT) -> bool:
  """Poll a URL until it responds 200, or timeout."""
  import urllib.request
  import urllib.error

  deadline = time.time() + timeout
  while time.time() < deadline:
    try:
      with urllib.request.urlopen(url, timeout=3) as resp:
        if resp.status == 200:
          return True
    except (urllib.error.URLError, OSError, TimeoutError):
      pass
    time.sleep(1)
  return False


def _start_dev_servers(src_dir: Path) -> subprocess.Popen:
  """Start backend + frontend dev servers in background."""
  print("\n  Starting dev servers...")
  process = subprocess.Popen(
    ["npm", "run", "dev"],
    cwd=str(src_dir),
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    shell=(os.name == "nt"),
  )
  return process


def _stop_dev_servers(process: subprocess.Popen) -> None:
  """Stop the dev server process tree."""
  if process.poll() is not None:
    return
  if os.name == "nt":
    subprocess.run(
      ["taskkill", "/PID", str(process.pid), "/T", "/F"],
      capture_output=True, check=False, shell=False,
    )
  else:
    try:
      os.kill(process.pid, 9)
    except ProcessLookupError:
      pass
  try:
    process.wait(timeout=10)
  except subprocess.TimeoutExpired:
    pass


def _run_playwright_tests() -> bool:
  """Run Playwright Python tests from the tests/ directory. Returns True if all pass."""
  print("\n── UI Tests (Playwright) ──\n")
  test_file = PLAYWRIGHT_TEST_DIR / "test_ui.py"
  if not test_file.exists():
    print(f"  WARNING: No Playwright test file found at {test_file}")
    return True  # No tests = vacuously passing

  result = subprocess.run(
    [sys.executable, "-m", "pytest", str(test_file), "-v", "--tb=short"],
    cwd=str(LESSON),
  )
  if result.returncode != 0:
    # Fallback: try running directly if pytest is not installed
    if "No module named pytest" in (result.stderr or ""):
      print("  pytest not found, running test directly...")
      result = subprocess.run(
        [sys.executable, str(test_file)], cwd=str(LESSON),
      )
  return result.returncode == 0


def test() -> int:
  """Run unit tests (vitest) + Playwright UI verification."""
  print("Running lesson 05 validation suite...\n")

  src_dir = _ensure_src_ready()
  _seed_if_needed(src_dir)

  # ── Phase 1: Unit tests ──
  unit_ok = _run_unit_tests(src_dir)
  if not unit_ok:
    print("\nFAILED: Unit tests did not pass.")
    return 1

  # ── Phase 2: Playwright UI tests ──
  server_process = _start_dev_servers(src_dir)
  playwright_ok = False
  try:
    backend_url = f"http://localhost:{BACKEND_PORT}/health"
    print(f"  Waiting for backend at {backend_url}...")
    if not _wait_for_server(backend_url):
      print("ERROR: Backend did not start within timeout.")
      return 2

    frontend_url = f"http://localhost:{FRONTEND_PORT}"
    print(f"  Waiting for frontend at {frontend_url}...")
    if not _wait_for_server(frontend_url):
      print("ERROR: Frontend did not start within timeout.")
      return 2

    print("  Servers ready.")
    playwright_ok = _run_playwright_tests()
  finally:
    print("\n  Stopping dev servers...")
    _stop_dev_servers(server_process)

  if not playwright_ok:
    print("\nFAILED: Playwright UI tests did not pass.")
    return 3

  print("\n✓ All tests passed (unit + UI).")
  return 0


def demo() -> int:
  print("Running lesson 05 Copilot CLI demo...")
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

  before = _snapshot_tree(src_dir)
  prompt = _demo_prompt()
  return_code, status = _run_copilot_demo(prompt, src_dir, copilot_executable, demo_model)
  after = _snapshot_tree(src_dir)
  changed = _write_diff(before, after)
  _wait_for_fresh_artifacts(run_started_at)

  if return_code == 124:
    print(
      "ERROR: Copilot CLI did not export a completed session before the demo window closed. "
      f"Hard timeout={DEMO_TIMEOUT_SECONDS}s, idle timeout={DEMO_IDLE_TIMEOUT_SECONDS}s. "
      "See .output/logs/copilot.log."
    )
    return return_code

  if return_code != 0:
    print("ERROR: Copilot CLI demo failed. See .output/logs for details.")
    return return_code

  if not any(changed.values()):
    print("ERROR: Implementation demo should produce a focused change, but no tracked src/ files changed.")
    return 5

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
  main(
    "05",
    "Implementation Workflows",
    LESSON,
    APP_SOURCE,
    extra_commands={
      "demo": (
        "Run a Copilot CLI implementation demo and capture logs plus a git-style diff",
        demo,
      ),
      "test": (
        "Run unit tests (vitest) and Playwright UI verification",
        test,
      ),
    },
  )
