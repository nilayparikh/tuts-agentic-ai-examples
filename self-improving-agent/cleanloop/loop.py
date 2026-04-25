"""loop.py — The Karpathy Loop (orchestrator).

The core self-improving loop. Each iteration:
  1. Run the genome (clean_data.py) against messy input
  2. Evaluate output with the referee (prepare.py)
  3. If all assertions pass: done
  4. Send code + failures to the LLM for a hypothesis + fix
  5. Write the new genome
  6. Re-evaluate
  7. If score improved: git commit. Else: git revert.

Lesson references:
  - Lesson 04: Lines 55-85   (system prompt — how we constrain the LLM)
  - Lesson 06: Lines 88-195  (the main loop — the Karpathy Loop itself)
  - Lesson 06: Lines 130-160 (commit-or-revert — Git as selection pressure)
  - Lesson 08: Lines 88-120  (eval history — how failures compound context)
  - Lesson 10: Lines 88-195  (where reranker.propose() plugs in)

Usage:
    python -m cleanloop.loop
    python -m cleanloop.loop --max-iterations 10
    python -m cleanloop.loop --use-reranker --candidates 5

Environment variables (from .env):
    LLM_ENDPOINT    — Agnostic OpenAI-compatible endpoint
    LLM_API_KEY     — Agnostic API key
    MODEL_NAME      — Model deployment or model name
    LLM_API_VERSION — Optional provider-specific API version
    OPENAI_BASE_URL — Legacy fallback
    OPENAI_API_KEY  — Legacy fallback
    AZURE_ENDPOINT  — Legacy fallback
    AZURE_API_KEY   — Legacy fallback
"""

import argparse
import importlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

import util
from cleanloop import dashboard_metrics
from cleanloop import datasets as cleanloop_datasets

# Resolve paths relative to project root (one level up from cleanloop/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

GENOME_PATH = PROJECT_ROOT / "cleanloop" / "clean_data.py"
STARTER_GENOME_PATH = PROJECT_ROOT / "cleanloop" / "clean_data_starter.py"
INPUT_DIR = PROJECT_ROOT / "cleanloop" / ".input"
OUTPUT_DIR = PROJECT_ROOT / "cleanloop" / ".output"
PROPOSAL_MAX_TOKENS = 2200
COMPACT_RETRY_MAX_TOKENS = 1200
STRATEGY_FILENAME = "finance_strategy.json"


def _iso_now() -> str:
    """Return the current UTC timestamp in ISO-8601 form."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _extract_usage_stats(response) -> dict[str, int | None]:
    """Extract token usage metadata from an OpenAI chat completion response."""
    usage = getattr(response, "usage", None)
    if usage is None:
        return {
            "prompt_tokens": None,
            "completion_tokens": None,
            "total_tokens": None,
        }
    return {
        "prompt_tokens": getattr(usage, "prompt_tokens", None),
        "completion_tokens": getattr(usage, "completion_tokens", None),
        "total_tokens": getattr(usage, "total_tokens", None),
    }


def _message_outline(messages: list[dict[str, str]]) -> list[dict[str, int | str]]:
    """Summarize chat messages for dashboard diagnostics."""
    outline: list[dict[str, int | str]] = []
    for message in messages:
        content = message.get("content", "")
        outline.append(
            {
                "role": message.get("role", "unknown"),
                "chars": len(content),
                "lines": len(content.splitlines()),
                "preview": content[:180],
            }
        )
    return outline


def _build_attempt_diagnostic(
    label: str,
    model: str,
    messages: list[dict[str, str]],
    response,
    text: str,
    code: str | None,
    hypothesis: str,
    max_tokens: int,
) -> dict[str, object]:
    """Record one LLM attempt for later dashboard inspection."""
    usage = _extract_usage_stats(response)
    return {
        "label": label,
        "model": model,
        "max_tokens": max_tokens,
        "code_found": bool(code),
        "hypothesis": hypothesis,
        "usage": usage,
        "prompt_chars": sum(len(msg.get("content", "")) for msg in messages),
        "response_chars": len(text),
        "messages": _message_outline(messages),
        "response_preview": text[:400],
    }


def _summarize_attempts(attempts: list[dict[str, object]]) -> dict[str, object]:
    """Summarize aggregate LLM attempt diagnostics for one loop round."""
    prompt_tokens = 0
    completion_tokens = 0
    total_tokens = 0
    saw_usage = False
    selected_attempt = "none"

    for attempt in attempts:
        usage = attempt.get("usage", {})
        attempt_total = usage.get("total_tokens") if isinstance(usage, dict) else None
        attempt_prompt = usage.get("prompt_tokens") if isinstance(usage, dict) else None
        attempt_completion = usage.get("completion_tokens") if isinstance(usage, dict) else None
        if attempt_total is not None:
            total_tokens += int(attempt_total)
            saw_usage = True
        if attempt_prompt is not None:
            prompt_tokens += int(attempt_prompt)
        if attempt_completion is not None:
            completion_tokens += int(attempt_completion)
        if selected_attempt == "none" and attempt.get("code_found"):
            selected_attempt = str(attempt.get("label", "none"))

    return {
        "selected_attempt": selected_attempt,
        "attempts": attempts,
        "prompt_tokens": prompt_tokens if saw_usage else None,
        "completion_tokens": completion_tokens if saw_usage else None,
        "total_tokens": total_tokens if saw_usage else None,
    }


def _artifact_manifest(config, output_path: Path, history_path: Path) -> dict[str, object]:
    """Describe the main files involved in one dataset run."""
    strategy_path = output_path.parent / STRATEGY_FILENAME
    return {
        "dataset": config.name,
        "input_files": list(config.input_filenames),
        "output_csv": _path_for_history(output_path),
        "history_json": _path_for_history(history_path),
        "genome_path": _path_for_history(GENOME_PATH),
        "strategy_json": _path_for_history(strategy_path),
    }


def _path_for_history(path: Path) -> str:
    """Prefer repo-relative artifact paths, but tolerate temp directories in tests."""
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def _result_metrics_snapshot(results: dict) -> dict[str, object]:
    """Copy judge metrics into a history-safe dict for dashboard inspection."""
    metrics = results.get("metrics")
    if isinstance(metrics, dict):
        return dict(metrics)
    return {}


def _focus_area_for_failure(failure: str) -> str:
    """Map one failed assertion to a metacognitive focus area."""
    if failure.startswith("value_is_numeric") or failure.startswith("no_nan_value"):
        return "value_normalization"
    if failure.startswith("date_is_parseable") or failure.startswith("no_nan_date"):
        return "date_normalization"
    if failure.startswith("no_nan_entity"):
        return "entity_cleanup"
    if failure.startswith("matches_reference_output"):
        return "row_reconciliation"
    return "baseline_stability"


def _guidance_for_focus_area(focus_area: str) -> str:
    """Return one coaching hint for the current metacognitive focus."""
    guidance = {
        "value_normalization": (
            "Normalize currency symbols, accounting markers, and sentinels before "
            "numeric coercion."
        ),
        "date_normalization": "Unify mixed invoice date formats before sorting or filtering rows.",
        "entity_cleanup": "Preserve valid customer names while trimming whitespace and blanks.",
        "row_reconciliation": (
            "Compare missing and unexpected rows to see which transformations are still "
            "dropping or inventing records."
        ),
        "baseline_stability": "Keep the genome runnable while you reduce the remaining judge failures.",
    }
    return guidance[focus_area]


def _build_metacognition_snapshot(history: list[dict], results: dict) -> dict[str, object]:
    """Summarize recurring failure patterns into a small strategy snapshot."""
    recent_failures: list[str] = []
    for entry in history[-2:]:
        failed = entry.get("failed", [])
        if isinstance(failed, list):
            recent_failures.extend(str(item) for item in failed)

    current_failures = results.get("failed", [])
    if isinstance(current_failures, list):
        recent_failures.extend(str(item) for item in current_failures)

    if not recent_failures:
        return {
            "focus_area": "done",
            "repeated_failure_count": 0,
            "recent_failures": [],
            "guidance": "The judge is satisfied. Keep the current genome stable.",
        }

    counts: dict[str, int] = {}
    for failure in recent_failures:
        focus_area = _focus_area_for_failure(failure)
        counts[focus_area] = counts.get(focus_area, 0) + 1

    priority = [
        "value_normalization",
        "date_normalization",
        "entity_cleanup",
        "row_reconciliation",
        "baseline_stability",
    ]
    focus_area = max(priority, key=lambda item: (counts.get(item, 0), -priority.index(item)))
    return {
        "focus_area": focus_area,
        "repeated_failure_count": counts.get(focus_area, 0),
        "recent_failures": recent_failures[-5:],
        "guidance": _guidance_for_focus_area(focus_area),
    }


def _write_metacognition_snapshot(output_dir: Path, snapshot: dict[str, object]) -> Path:
    """Persist the current strategy snapshot beside the other loop artifacts."""
    output_dir.mkdir(parents=True, exist_ok=True)
    strategy_path = output_dir / STRATEGY_FILENAME
    strategy_path.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    return strategy_path


def _append_log(
    logs: list[dict[str, object]],
    tag: str,
    message: str,
    *,
    prompt_tokens: int | None = None,
    completion_tokens: int | None = None,
    total_tokens: int | None = None,
) -> None:
    """Append one structured log entry and print it in teaching format."""
    entry: dict[str, object] = {"tag": tag, "message": message}
    if prompt_tokens is not None:
        entry["prompt_tokens"] = prompt_tokens
    if completion_tokens is not None:
        entry["completion_tokens"] = completion_tokens
    if total_tokens is not None:
        entry["total_tokens"] = total_tokens
    logs.append(entry)
    print(f"[{tag}] {message}")


def _prepare_fresh_run(
    config,
    output_path: Path,
    history_path: Path,
    *,
    genome_path: Path = GENOME_PATH,
    starter_genome_path: Path = STARTER_GENOME_PATH,
) -> list[dict[str, object]]:
    """Reset one CleanLoop run to the starter genome and empty dataset artifacts."""
    logs: list[dict[str, object]] = []
    _append_log(
        logs,
        "FRESH_START",
        f"Starting from the immutable starter genome for dataset {config.name}",
    )

    removed_artifacts: list[str] = []
    for artifact in [output_path, history_path]:
        if artifact.exists():
            artifact.unlink()
            removed_artifacts.append(artifact.name)
    if removed_artifacts:
        _append_log(
            logs,
            "RESET_DATASET_ARTIFACTS",
            f"Removed stale artifacts: {', '.join(removed_artifacts)}",
        )
    else:
        _append_log(
            logs,
            "RESET_DATASET_ARTIFACTS",
            "No stale dataset artifacts were present",
        )

    starter_code = starter_genome_path.read_text(encoding="utf-8")
    genome_path.write_text(starter_code, encoding="utf-8")
    _append_log(
        logs,
        "RESTORE_STARTER_GENOME",
        f"Restored {genome_path.name} from {starter_genome_path.name}",
    )
    return logs


def _capture_output_snapshot(output_path: Path) -> str | None:
    """Capture the last known-good output artifact so a revert can restore it."""
    if not output_path.exists():
        return None
    return output_path.read_text(encoding="utf-8")


def _restore_output_snapshot(output_path: Path, snapshot: str | None) -> None:
    """Restore the last known-good output artifact after a candidate is reverted."""
    if snapshot is None:
        if output_path.exists():
            output_path.unlink()
        return
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(snapshot, encoding="utf-8")


def _restore_genome_snapshot(genome_path: Path, snapshot: str) -> None:
    """Restore the last known-good genome source after a rejected mutation."""
    genome_path.write_text(snapshot, encoding="utf-8")


def _validate_candidate_code(source: str, genome_path: Path) -> None:
    """Raise immediately if a candidate mutation is not valid Python."""
    compile(source, str(genome_path), "exec")


def _attempt_usage_value(attempt: dict[str, object], key: str) -> int | None:
    """Return one usage metric from a recorded LLM attempt."""
    usage = attempt.get("usage") if isinstance(attempt, dict) else None
    if not isinstance(usage, dict):
        return None
    value = usage.get(key)
    if isinstance(value, int):
        return value
    return None


def _print_llm_attempt_trace(llm_diagnostics: dict[str, object]) -> None:
    """Print a compact learning trace for each recorded LLM attempt."""
    logs: list[dict[str, object]] = []
    _print_llm_attempt_trace_to_logs(logs, llm_diagnostics)


def _print_llm_attempt_trace_to_logs(
    logs: list[dict[str, object]],
    llm_diagnostics: dict[str, object],
) -> None:
    """Record and print a compact learning trace for each recorded LLM attempt."""
    attempts = llm_diagnostics.get("attempts") if isinstance(llm_diagnostics, dict) else None
    if not isinstance(attempts, list) or not attempts:
        _append_log(logs, "NO_LLM_ATTEMPTS_RECORDED", "No LLM attempts recorded")
        return

    total_attempts = len(attempts)
    for index, attempt in enumerate(attempts, start=1):
        if not isinstance(attempt, dict):
            continue
        max_tokens = attempt.get("max_tokens", PROPOSAL_MAX_TOKENS)
        if not isinstance(max_tokens, int):
            max_tokens = PROPOSAL_MAX_TOKENS
        prompt_tokens = _attempt_usage_value(attempt, "prompt_tokens")
        completion_tokens = _attempt_usage_value(attempt, "completion_tokens")
        total_tokens = _attempt_usage_value(attempt, "total_tokens")
        response_chars = attempt.get("response_chars", 0)
        if not isinstance(response_chars, int):
            response_chars = 0
        code_found = bool(attempt.get("code_found", False))
        diagnosis = dashboard_metrics.diagnose_attempt_outcome(attempt, max_tokens)

        _append_log(
            logs,
            "LLM_ATTEMPT",
            f"Attempt {index}/{total_attempts}: {attempt.get('label', 'LLM attempt')}",
        )
        _append_log(logs, "TOKEN_BUDGET", f"{max_tokens} max completion tokens")
        _append_log(
            logs,
            "TOKEN_USAGE",
            f"prompt={prompt_tokens}, completion={completion_tokens}, total={total_tokens}",
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
        )
        _append_log(logs, "RESPONSE_CHARS", str(response_chars))
        _append_log(logs, "CODE_FOUND", "yes" if code_found else "no")
        _append_log(logs, "ATTEMPT_DIAGNOSIS", diagnosis)

    summary_total = llm_diagnostics.get("total_tokens")
    summary_prompt = llm_diagnostics.get("prompt_tokens")
    summary_completion = llm_diagnostics.get("completion_tokens")
    if isinstance(summary_total, int):
        _append_log(
            logs,
            "LLM_SUMMARY",
            f"prompt={summary_prompt}, completion={summary_completion}, total={summary_total}",
            prompt_tokens=summary_prompt if isinstance(summary_prompt, int) else None,
            completion_tokens=summary_completion if isinstance(summary_completion, int) else None,
            total_tokens=summary_total,
        )


# =====================================================================
# SECTION: LLM Prompt Construction
# Lesson 04 — The system prompt defines the agent's constraints.
# Notice how we feed it the agenda (README.md), the dataset-specific
# assertion registry, and strict rules about what it can modify.
# This is "Software 3.0" — programming via natural language constraints.
# =====================================================================

def build_system_prompt(dataset_name: str | None = None) -> str:
    """Build the system prompt with agenda and assertion context."""
    config = cleanloop_datasets.get_dataset_config(dataset_name)
    agenda = cleanloop_datasets.build_program_text(config.name)
    registry = json.dumps(
        cleanloop_datasets.build_assertion_registry(config.name),
        indent=2,
    )
    finance_scalar_guardrail = (
        "- Values may already be floats or NaN after pandas parsing.\n"
        "- Amount strings may include currency symbols or accounting markers like USD, EUR, or CR.\n"
        "- Never call .strip() on raw pandas scalars; coerce safely before trimming.\n"
    )

    return (
        "You are a self-improving data engineer agent.\n\n"
        f"## Selected Dataset\n{config.label} (`{config.name}`)\n\n"
        "## Agenda\n"
        f"{agenda}\n\n"
        "## Assertion Registry\n"
        f"{registry}\n\n"
        "## Rules\n"
        "- You may ONLY modify the `clean` function in clean_data.py.\n"
        "- Do NOT change function signatures or imports.\n"
        "- Do NOT modify prepare.py, datasets.py, or README.md.\n"
        f"{finance_scalar_guardrail}"
        "- Return ONLY the complete file content for clean_data.py.\n"
        "- Wrap your response in a ```python code block.\n"
        "- Before the code block, write a ONE-LINE hypothesis.\n"
    )


def build_user_prompt(
    genome_code: str,
    results: dict,
    history: list[dict],
    dataset_name: str | None = None,
    metacognition: dict[str, object] | None = None,
) -> str:
    """Build the user prompt with current state and eval history."""
    config = cleanloop_datasets.get_dataset_config(dataset_name)
    failed = "\n".join(f"  - {f}" for f in results.get("failed", []))
    passed = "\n".join(f"  - {p}" for p in results.get("passed", []))

    # Include last 3 rounds of history so the LLM learns from mistakes
    history_block = ""
    if history:
        history_block = "\n## Previous Attempts\n"
        for entry in history[-3:]:
            history_block += (
                f"- Round {entry['round']}: "
                f"{entry['score']}/{entry['total']} passed. "
                f"Hypothesis: {entry['hypothesis']}\n"
            )

    metacognition_block = ""
    if isinstance(metacognition, dict):
        focus_area = metacognition.get("focus_area", "baseline_stability")
        guidance = metacognition.get("guidance", "")
        metacognition_block = (
            "\n## Metacognition\n"
            f"Current focus: {focus_area}\n"
            f"Guidance: {guidance}\n"
        )

    return (
        f"## Target Dataset\n{config.label} (`{config.name}`)\n\n"
        "## Current clean_data.py\n"
        f"```python\n{genome_code}\n```\n\n"
        f"## Failed Assertions\n{failed}\n\n"
        f"## Passed Assertions\n{passed}\n"
        f"{history_block}\n"
        f"{metacognition_block}\n"
        "Fix the code so more assertions pass. "
        "Return the COMPLETE updated clean_data.py."
    )


# =====================================================================
# SECTION: The Karpathy Loop
# Lesson 06 — This is the heart of the course. The loop:
#   1. Runs the genome and evaluates it
#   2. Asks the LLM for a fix (with failure context)
#   3. Writes the new code
#   4. Re-evaluates
#   5. Commits if better, reverts if not
#
# The key insight: Git acts as selection pressure. Good mutations
# survive (commit). Bad mutations die (revert). Over iterations,
# the genome evolves toward correctness — just like biological
# evolution, but with an LLM as the mutation operator.
# =====================================================================

def run_loop(
    max_iterations: int = 5,
    use_reranker: bool = False,
    n_candidates: int = 3,
) -> list[dict]:
    """Execute the self-improving loop.

    Returns the eval history for dashboard consumption.
    """
    config = cleanloop_datasets.get_dataset_config()
    output_path = cleanloop_datasets.get_output_path(OUTPUT_DIR)
    history_path = cleanloop_datasets.get_history_path(OUTPUT_DIR)
    llm_config = util.resolve_llm_env()
    client = util.build_llm_client(
        llm_config["endpoint"],
        llm_config["api_key"],
        llm_config["api_version"],
    )
    model = llm_config["model"]
    system_prompt = build_system_prompt(config.name)
    history: list[dict] = []

    OUTPUT_DIR.mkdir(exist_ok=True)
    pre_run_logs = _prepare_fresh_run(config, output_path, history_path)

    # Import genome module for reloading
    from cleanloop import (  # pylint: disable=import-outside-toplevel
        clean_data, prepare,
    )

    for i in range(1, max_iterations + 1):
        round_started_at = _iso_now()
        round_logs = list(pre_run_logs) if i == 1 else []
        print(f"\n--- Round {i}/{max_iterations} ---")
        print(f"Dataset: {config.name}")
        _append_log(
            round_logs,
            "ROUND_START",
            f"Starting round {i} of {max_iterations} for dataset {config.name}",
        )

        # Step 1: Run genome and evaluate
        _append_log(
            round_logs,
            "RUN_GENOME_AND_EVALUATE",
            f"Running {GENOME_PATH.name} against {config.name} inputs and evaluating the result",
        )
        importlib.reload(clean_data)
        results = _run_and_evaluate(clean_data, prepare, INPUT_DIR, output_path)
        genome_before = _read_utf8_text(GENOME_PATH)
        score = results["score"]
        total = results["total"]
        baseline_output_snapshot = _capture_output_snapshot(output_path)
        metacognition = _build_metacognition_snapshot(history, results)
        _write_metacognition_snapshot(output_path.parent, metacognition)
        print(f"Score: {score}/{total}")
        _append_log(round_logs, "CURRENT_SCORE", f"Score {score}/{total}")
        _append_log(
            round_logs,
            "METACOGNITION",
            f"Focus {metacognition['focus_area']}: {metacognition['guidance']}",
        )

        # Step 2: Check if done
        if not results["failed"]:
            print("All assertions passed.")
            _append_log(
                round_logs,
                "ALL_ASSERTIONS_PASSED",
                f"Dataset {config.name} already satisfies every assertion",
            )
            _git_commit(f"loop: round {i} -- all {total} assertions pass")
            history.append({
                "round": i,
                "dataset": config.name,
                "model": model,
                "score": score,
                "total": total,
                "before_score": score,
                "score_delta": 0,
                "metrics": _result_metrics_snapshot(results),
                "before_metrics": _result_metrics_snapshot(results),
                "hypothesis": "all passed",
                "action": "done",
                "failed": results.get("failed", []),
                "passed": results.get("passed", []),
                "before_failed": results.get("failed", []),
                "before_passed": results.get("passed", []),
                "started_at": round_started_at,
                "finished_at": _iso_now(),
                "artifacts": _artifact_manifest(config, output_path, history_path),
                "metacognition": metacognition,
                "genome_before": genome_before,
                "genome_after": genome_before,
                "llm": _summarize_attempts([]),
                "logs": round_logs,
            })
            break

        for f in results["failed"]:
            print(f"  [FAIL] {f}")
            _append_log(round_logs, "FAILED_ASSERTION", f)

        # Step 3: Get a fix from the LLM
        genome_code = _read_utf8_text(GENOME_PATH)
        _append_log(
            round_logs,
            "REQUESTING_LLM_PROPOSAL",
            f"Requesting mutation proposal from model {model}",
        )
        llm_diagnostics: dict[str, object]

        if use_reranker:
            # Lesson 10 — Best-of-N: generate multiple candidates
            from cleanloop import reranker  # pylint: disable=import-outside-toplevel
            new_code, hypothesis = reranker.propose(
                client, model, genome_code,
                results["failed"], n_candidates,
            )
            llm_diagnostics = {
                "selected_attempt": "reranker",
                "attempts": [],
                "prompt_tokens": None,
                "completion_tokens": None,
                "total_tokens": None,
            }
        else:
            # Standard single-shot proposal
            try:
                new_code, hypothesis, llm_diagnostics = _propose_fix(
                    client, model, system_prompt,
                    genome_code, results, history, config.name, metacognition,
                )
                _print_llm_attempt_trace_to_logs(round_logs, llm_diagnostics)
            except Exception as exc:  # noqa: BLE001
                error_message = str(exc)
                if "Endpoint busy (429 capacity)" not in error_message:
                    error_message = util._format_llm_exception(exc)
                print(f"WARNING: {error_message}")
                _append_log(round_logs, "LLM_PROPOSAL_UNAVAILABLE", error_message)
                history.append({
                    "round": i,
                    "dataset": config.name,
                    "model": model,
                    "score": score,
                    "total": total,
                    "before_score": score,
                    "score_delta": 0,
                    "metrics": _result_metrics_snapshot(results),
                    "before_metrics": _result_metrics_snapshot(results),
                    "hypothesis": "llm proposal unavailable",
                    "action": "skip",
                    "failed": results.get("failed", []),
                    "passed": results.get("passed", []),
                    "before_failed": results.get("failed", []),
                    "before_passed": results.get("passed", []),
                    "started_at": round_started_at,
                    "finished_at": _iso_now(),
                    "artifacts": _artifact_manifest(config, output_path, history_path),
                    "metacognition": metacognition,
                    "genome_before": genome_before,
                    "genome_after": genome_before,
                    "llm": {
                        "selected_attempt": "none",
                        "attempts": [],
                        "prompt_tokens": None,
                        "completion_tokens": None,
                        "total_tokens": None,
                        "error": error_message,
                    },
                    "logs": round_logs,
                })
                continue

        if not new_code:
            attempts = llm_diagnostics.get("attempts", []) if isinstance(llm_diagnostics, dict) else []
            attempt_count = len(attempts) if isinstance(attempts, list) else 0
            warning_message = (
                f"No candidate code returned after {attempt_count} attempts. Skipping round."
            )
            print(f"WARNING: {warning_message}")
            _append_log(round_logs, "NO_CODE_RETURNED", warning_message)
            history.append({
                "round": i,
                "dataset": config.name,
                "model": model,
                "score": score,
                "total": total,
                "before_score": score,
                "score_delta": 0,
                "metrics": _result_metrics_snapshot(results),
                "before_metrics": _result_metrics_snapshot(results),
                "hypothesis": hypothesis,
                "action": "skip",
                "failed": results.get("failed", []),
                "passed": results.get("passed", []),
                "before_failed": results.get("failed", []),
                "before_passed": results.get("passed", []),
                "started_at": round_started_at,
                "finished_at": _iso_now(),
                "artifacts": _artifact_manifest(config, output_path, history_path),
                "metacognition": metacognition,
                "genome_before": genome_before,
                "genome_after": genome_before,
                "llm": llm_diagnostics,
                "logs": round_logs,
            })
            continue

        print(f"Hypothesis: {hypothesis}")
        _append_log(round_logs, "HYPOTHESIS_SELECTED", hypothesis)

        # Step 4: Write new genome and re-evaluate
        _append_log(round_logs, "WRITE_MUTATED_GENOME", f"Writing candidate mutation to {GENOME_PATH.name}")
        try:
            _validate_candidate_code(new_code, GENOME_PATH)
            GENOME_PATH.write_text(new_code, encoding="utf-8")
            importlib.reload(clean_data)
            _append_log(round_logs, "RE_EVALUATE_MUTATION", "Re-running the mutated genome against the referee")
            new_results = _run_and_evaluate(clean_data, prepare, INPUT_DIR, output_path)
        except Exception as exc:  # noqa: BLE001
            failure_message = f"can_run_genome: {exc}"
            _append_log(round_logs, "MUTATION_EXECUTION_FAILED", failure_message)
            new_results = {
                "passed": [],
                "failed": [failure_message],
                "score": 0,
                "total": 1,
            }
        new_score = new_results["score"]
        new_total = new_results["total"]
        _append_log(round_logs, "MUTATION_SCORE", f"Candidate scored {new_score}/{new_total}")

        # ─────────────────────────────────────────────────────────
        # SECTION: Commit or Revert (Git as Selection Pressure)
        # Lesson 06 — This is the selection mechanism.
        # If the new code scores higher: commit (mutation survives).
        # If not: revert to last known good (mutation dies).
        # This prevents the genome from regressing — it can only
        # improve or stay the same, never get worse.
        # ─────────────────────────────────────────────────────────
        if new_score > score:
            _git_commit(
                f"loop: round {i} -- {new_score}/{new_total} "
                f"(+{new_score - score}) {hypothesis[:40]}"
            )
            action = "commit"
            print(f"  Committed: {new_score}/{new_total}")
            _append_log(
                round_logs,
                "COMMIT_MUTATION",
                f"Committed improved mutation at {new_score}/{new_total}",
            )
        else:
            _git_revert()
            _restore_genome_snapshot(GENOME_PATH, genome_before)
            _restore_output_snapshot(output_path, baseline_output_snapshot)
            importlib.reload(clean_data)
            action = "revert"
            print(f"  Reverted: no improvement ({new_score}/{new_total})")
            _append_log(
                round_logs,
                "REVERT_MUTATION",
                f"Reverted mutation with score {new_score}/{new_total}",
            )

        history.append({
            "round": i,
            "dataset": config.name,
            "model": model,
            "score": new_score,
            "total": new_total,
            "before_score": score,
            "score_delta": new_score - score,
            "metrics": _result_metrics_snapshot(new_results),
            "before_metrics": _result_metrics_snapshot(results),
            "hypothesis": hypothesis,
            "action": action,
            "failed": new_results.get("failed", []),
            "passed": new_results.get("passed", []),
            "before_failed": results.get("failed", []),
            "before_passed": results.get("passed", []),
            "started_at": round_started_at,
            "finished_at": _iso_now(),
            "artifacts": _artifact_manifest(config, output_path, history_path),
            "metacognition": metacognition,
            "genome_before": genome_before,
            "genome_after": new_code,
            "llm": llm_diagnostics,
            "logs": round_logs,
        })

    # Save history for dashboard
    history_path.write_text(json.dumps(history, indent=2), encoding="utf-8")
    print(f"\nHistory saved to {history_path}")
    return history


def _read_utf8_text(path: Path) -> str:
    """Read a text file as UTF-8."""
    return path.read_text(encoding="utf-8")


def _run_and_evaluate(clean_data_module, prepare_module, input_dir: Path, output_path: Path) -> dict:
    """Run the genome and convert execution errors into structured failures."""
    try:
        clean_data_module.clean(input_dir, output_path)
    except Exception as exc:  # noqa: BLE001
        return {
            "passed": [],
            "failed": [f"can_run_genome: {exc}"],
            "score": 0,
            "total": 1,
        }
    return prepare_module.evaluate(output_path)


def _propose_fix(
    client: Any,
    model: str,
    system_prompt: str,
    genome_code: str,
    results: dict,
    history: list[dict],
    dataset_name: str | None = None,
    metacognition: dict[str, object] | None = None,
) -> tuple[str | None, str, dict[str, object]]:
    """Ask the LLM for a single code fix. Returns (code, hypothesis)."""
    user_prompt = build_user_prompt(
        genome_code,
        results,
        history,
        dataset_name,
        metacognition,
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    response = util._create_chat_completion_with_backoff(
        client,
        model=model,
        messages=messages,
        retry_label="CleanLoop proposal",
        **util._chat_completion_options(max_tokens=PROPOSAL_MAX_TOKENS, temperature=0.3),
    )
    text = response.choices[0].message.content or ""
    code = _extract_code(text)
    hypothesis = _extract_hypothesis(text)
    attempts = [
        _build_attempt_diagnostic(
            "CleanLoop proposal",
            model,
            messages,
            response,
            text,
            code,
            hypothesis,
            PROPOSAL_MAX_TOKENS,
        )
    ]

    if code:
        return code, hypothesis, _summarize_attempts(attempts)

    retry_system_prompt, retry_user_prompt = _build_compact_retry_prompts(
        genome_code,
        results,
    )
    retry_messages = [
        {"role": "system", "content": retry_system_prompt},
        {"role": "user", "content": retry_user_prompt},
    ]
    retry_response = util._create_chat_completion_with_backoff(
        client,
        model=model,
        messages=retry_messages,
        retry_label="CleanLoop compact retry",
        **util._chat_completion_options(max_tokens=COMPACT_RETRY_MAX_TOKENS, temperature=0.2),
    )
    retry_text = retry_response.choices[0].message.content or ""
    retry_code = _extract_code(retry_text)
    retry_hypothesis = _extract_hypothesis(retry_text)
    attempts.append(
        _build_attempt_diagnostic(
            "CleanLoop compact retry",
            model,
            retry_messages,
            retry_response,
            retry_text,
            retry_code,
            retry_hypothesis,
            COMPACT_RETRY_MAX_TOKENS,
        )
    )
    if retry_code:
        return retry_code, retry_hypothesis, _summarize_attempts(attempts)

    return code, hypothesis, _summarize_attempts(attempts)


def _build_compact_retry_prompts(genome_code: str, results: dict) -> tuple[str, str]:
    """Build a compact retry prompt for reasoning-heavy models that returned no code."""
    failed = "\n".join(results.get("failed", [])) or "unknown failure"
    system_prompt = (
        "You fix Python code. Return ONLY the complete clean_data.py file "
        "inside one ```python code block. Do not add explanation."
    )
    user_prompt = (
        f"Current failure:\n{failed}\n\n"
        "Fix the clean function so it can read every CSV in the input folder, "
        "handle malformed rows safely, and write the dataset-specific master CSV. "
        "Values may already be floats or NaN after pandas parsing, so coerce "
        "float or NaN values safely before trimming and never call .strip() on "
        "raw pandas scalars. "
        "Return the full file only.\n\n"
        f"```python\n{genome_code}\n```"
    )
    return system_prompt, user_prompt


def _extract_code(text: str) -> str | None:
    """Extract Python code block from LLM response."""
    if "```python" not in text:
        return None
    start = text.index("```python") + len("```python")
    end = text.find("```", start)
    if end == -1:
        return text[start:].strip() or None
    return text[start:end].strip() or None


def _extract_hypothesis(text: str) -> str:
    """Extract hypothesis line before the code block."""
    parts = text.split("```python")
    if len(parts) < 2:
        return "no hypothesis"
    lines = parts[0].strip().split("\n")
    for line in reversed(lines):
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return stripped[:120]
    return "no hypothesis"


# =====================================================================
# SECTION: Git Operations
# Lesson 06 — Git is the selection mechanism. We use subprocess
# calls to stage, commit, and revert the genome file.
# =====================================================================

def _git_commit(message: str) -> None:
    """Stage the genome file and commit with a descriptive message."""
    try:
        subprocess.run(
            ["git", "add", str(GENOME_PATH)],
            check=True, capture_output=True, cwd=str(PROJECT_ROOT),
        )
        subprocess.run(
            ["git", "commit", "-m", message],
            check=True, capture_output=True, cwd=str(PROJECT_ROOT),
        )
    except subprocess.CalledProcessError:
        pass  # Git not initialized — skip silently


def _git_revert() -> None:
    """Revert the genome file to the last committed version."""
    try:
        subprocess.run(
            ["git", "checkout", "--", str(GENOME_PATH)],
            check=True, capture_output=True, cwd=str(PROJECT_ROOT),
        )
    except subprocess.CalledProcessError:
        pass  # Git not initialized — skip silently


# =====================================================================
# SECTION: CLI Entry Point
# =====================================================================

def main() -> None:
    """Parse arguments and run the loop."""
    parser = argparse.ArgumentParser(
        description="CleanLoop — Self-Improving Data Engineer"
    )
    parser.add_argument(
        "--max-iterations", type=int, default=5,
        help="Maximum loop iterations (default: 5)",
    )
    parser.add_argument(
        "--use-reranker", action="store_true",
        help="Use Best-of-N reranking (Lesson 10)",
    )
    parser.add_argument(
        "--candidates", type=int, default=3,
        help="Number of reranker candidates (default: 3)",
    )
    args = parser.parse_args()
    run_loop(
        max_iterations=args.max_iterations,
        use_reranker=args.use_reranker,
        n_candidates=args.candidates,
    )


if __name__ == "__main__":
    main()
