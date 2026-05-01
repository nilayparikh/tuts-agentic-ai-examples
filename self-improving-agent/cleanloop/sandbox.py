"""sandbox.py — Subprocess Isolation for Genome Execution.

Runs the genome (clean_data.py) in an isolated subprocess with:
  - Timeout enforcement (prevents infinite loops)
  - Separate process memory (genome can't access loop state)
  - Captured stdout/stderr for logging

Course alignment:
    - Lesson 07: safety and autonomy

Usage:
    Preferred from cleanloop/:
        python util.py sandbox
        python util.py sandbox --timeout 10

    Direct module alternative:
        python -m cleanloop.sandbox
        python -m cleanloop.sandbox --timeout 10

No environment variables required.
"""

import argparse
import json
import subprocess
import sys
import textwrap
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from cleanloop import datasets as cleanloop_datasets  # noqa: E402

GENOME_PATH = PROJECT_ROOT / "cleanloop" / "clean_data.py"
INPUT_DIR = PROJECT_ROOT / "cleanloop" / ".input"
OUTPUT_DIR = PROJECT_ROOT / "cleanloop" / ".output"
SANDBOX_AUDIT_FILENAME = "sandbox_runs.jsonl"


def _utc_now() -> str:
    """Return the current UTC timestamp for audit records."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


# =====================================================================
# SECTION: Sandboxed Execution
# Lesson 07 — The genome runs in a separate Python process.
# This means:
#   1. It can't access the loop's memory or variables
#   2. If it crashes, the loop survives
#   3. If it hangs, the timeout kills it
#   4. Its stdout/stderr are captured for debugging
#
# Why subprocess and not just try/except?
# Because the agent rewrites code — a malformed genome could import
# dangerous modules, enter infinite loops, or corrupt shared state.
# Process isolation is the only reliable defense.
# =====================================================================


def run_sandboxed(
    genome_path: Path,
    input_dir: Path,
    output_path: Path,
    timeout: int = 30,
) -> dict:
    """Run the genome in an isolated subprocess.

    Returns a result dict with: success, stdout, stderr,
    return_code, timed_out.
    """
    # Build a minimal runner script that imports and calls the genome
    runner = textwrap.dedent(f"""\
        import sys
        sys.path.insert(0, r"{genome_path.parent.parent}")
        from pathlib import Path
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "genome", r"{genome_path}"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.clean(Path(r"{input_dir}"), Path(r"{output_path}"))
        print("SANDBOX_OK")
    """)

    try:
        result = subprocess.run(
            [sys.executable, "-c", runner],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(PROJECT_ROOT),
            check=False,
        )

        return {
            "success": (result.returncode == 0 and "SANDBOX_OK" in result.stdout),
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode,
            "timed_out": False,
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Timed out after {timeout}s",
            "return_code": -1,
            "timed_out": True,
        }

    except Exception as exc:  # pylint: disable=broad-exception-caught
        return {
            "success": False,
            "stdout": "",
            "stderr": str(exc),
            "return_code": -1,
            "timed_out": False,
        }


def append_sandbox_audit(
    output_dir: Path,
    *,
    timeout: int,
    output_path: Path,
    result: dict,
) -> Path:
    """Append one sandbox outcome to an audit JSONL artifact."""
    output_dir.mkdir(parents=True, exist_ok=True)
    audit_path = output_dir / SANDBOX_AUDIT_FILENAME
    payload = {
        "timestamp": _utc_now(),
        "timeout_seconds": timeout,
        "output_path": str(output_path),
        "success": result.get("success", False),
        "timed_out": result.get("timed_out", False),
        "return_code": result.get("return_code"),
        "stderr_preview": str(result.get("stderr", ""))[:300],
    }
    with audit_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")
    return audit_path


# =====================================================================
# SECTION: Standalone Demo
# Run the sandbox directly to demonstrate the safety shell end to end:
# isolated execution first, deterministic referee second.
# =====================================================================


def main() -> None:
    """Run sandbox demo."""
    parser = argparse.ArgumentParser(description="Sandbox — Isolated genome execution")
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Timeout in seconds (default: 30)",
    )
    args = parser.parse_args()

    if not GENOME_PATH.exists():
        print("ERROR: clean_data.py not found. Check project structure.")
        sys.exit(1)

    OUTPUT_DIR.mkdir(exist_ok=True)
    config = cleanloop_datasets.get_dataset_config()
    output_path = cleanloop_datasets.get_output_path(OUTPUT_DIR, config.name)

    print(f"Running genome in sandbox for {config.name} (timeout={args.timeout}s)...")
    result = run_sandboxed(GENOME_PATH, INPUT_DIR, output_path, args.timeout)
    audit_path = append_sandbox_audit(
        OUTPUT_DIR,
        timeout=args.timeout,
        output_path=output_path,
        result=result,
    )

    if result["success"]:
        print("  [OK] Genome completed successfully")
    elif result["timed_out"]:
        print(f"  [FAIL] Timed out after {args.timeout}s")
    else:
        print(f"  [FAIL] Exit code: {result['return_code']}")

    if result["stderr"]:
        print(f"  stderr: {result['stderr'][:300]}")
    print(f"  Audit: {audit_path}")

    # Evaluate if output was produced
    if result["success"] and output_path.exists():
        from cleanloop import prepare

        eval_result = prepare.evaluate(output_path)
        prepare.print_results(eval_result)


if __name__ == "__main__":
    main()
