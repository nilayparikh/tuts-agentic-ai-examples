"""Helpers for loading exported CleanLoop traces and raw loop logs."""

from __future__ import annotations

import json
from pathlib import Path

from cleanloop import datasets as cleanloop_datasets


def _read_jsonl_records(path: Path) -> list[dict[str, object]]:
    """Load one JSONL file into dashboard-safe record dicts."""
    if not path.exists():
        return []

    records: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            payload = json.loads(stripped)
            if isinstance(payload, dict):
                records.append(payload)
    return records


def _read_json_object(path: Path) -> dict[str, object]:
    """Load one JSON object file for dashboard rendering."""
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if isinstance(payload, dict):
        return payload
    return {}


def _read_json_list(path: Path) -> list[dict[str, object]]:
    """Load one JSON list file into dashboard-safe record dicts."""
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, list):
        return []
    return [item for item in payload if isinstance(item, dict)]


def get_dashboard_artifact_paths(
    output_dir: Path,
    dataset_name: str | None = None,
    run_instance: str | None = None,
) -> dict[str, Path]:
    """Return the active artifact paths for current or per-run dashboard state."""
    config = cleanloop_datasets.get_dataset_config(dataset_name)
    if run_instance is None:
        return {
            "history": cleanloop_datasets.get_history_path(output_dir, config.name),
            "strategy": cleanloop_datasets.get_strategy_path(output_dir, config.name),
            "output_csv": cleanloop_datasets.get_output_path(output_dir, config.name),
            "mutation_success": cleanloop_datasets.get_mutation_success_path(
                output_dir,
                config.name,
            ),
            "mutation_failures": cleanloop_datasets.get_mutation_failures_path(
                output_dir,
                config.name,
            ),
            "exported_logs": cleanloop_datasets.get_exported_logs_path(
                output_dir,
                config.name,
            ),
            "run_events": cleanloop_datasets.get_run_events_path(output_dir),
            "row_decisions": cleanloop_datasets.get_row_decisions_path(output_dir),
            "proposal_events": cleanloop_datasets.get_proposal_events_path(output_dir),
            "otel_spans": cleanloop_datasets.get_otel_spans_path(output_dir),
            "otel_events": cleanloop_datasets.get_otel_events_path(output_dir),
            "otel_logs": cleanloop_datasets.get_otel_logs_path(output_dir),
        }

    return {
        "history": cleanloop_datasets.get_run_history_path(
            output_dir,
            run_instance,
            config.name,
        ),
        "strategy": cleanloop_datasets.get_run_strategy_path(
            output_dir,
            run_instance,
            config.name,
        ),
        "output_csv": cleanloop_datasets.get_run_output_path(
            output_dir,
            run_instance,
            config.name,
        ),
        "mutation_success": cleanloop_datasets.get_run_mutation_success_path(
            output_dir,
            run_instance,
            config.name,
        ),
        "mutation_failures": cleanloop_datasets.get_run_mutation_failures_path(
            output_dir,
            run_instance,
            config.name,
        ),
        "exported_logs": cleanloop_datasets.get_exported_logs_path(
            output_dir,
            config.name,
            run_instance=run_instance,
        ),
        "run_events": cleanloop_datasets.get_run_events_path(output_dir, run_instance),
        "row_decisions": cleanloop_datasets.get_row_decisions_path(
            output_dir,
            run_instance,
        ),
        "proposal_events": cleanloop_datasets.get_proposal_events_path(
            output_dir,
            run_instance,
        ),
        "otel_spans": cleanloop_datasets.get_otel_spans_path(output_dir, run_instance),
        "otel_events": cleanloop_datasets.get_otel_events_path(
            output_dir, run_instance
        ),
        "otel_logs": cleanloop_datasets.get_otel_logs_path(output_dir, run_instance),
        "manifest": cleanloop_datasets.get_run_manifest_path(output_dir, run_instance),
        "diagnostics": cleanloop_datasets.get_run_diagnostics_path(
            output_dir,
            run_instance,
        ),
    }


def load_history_snapshot(
    output_dir: Path,
    dataset_name: str | None = None,
    run_instance: str | None = None,
) -> list[dict[str, object]]:
    """Load current or per-run history for dashboard rendering."""
    paths = get_dashboard_artifact_paths(output_dir, dataset_name, run_instance)
    return _read_json_list(paths["history"])


def load_strategy_snapshot(
    output_dir: Path,
    dataset_name: str | None = None,
    run_instance: str | None = None,
) -> dict[str, object]:
    """Load the lightweight metacognition strategy snapshot."""
    paths = get_dashboard_artifact_paths(output_dir, dataset_name, run_instance)
    return _read_json_object(paths["strategy"])


def _artifact_row(path: Path, purpose: str, command: str) -> dict[str, object]:
    """Build one dashboard row for a generated artifact path."""
    exists = path.exists()
    return {
        "Artifact": path.name,
        "Status": "present" if exists else "missing",
        "Bytes": path.stat().st_size if exists else 0,
        "Path": str(path),
        "Purpose": purpose,
        "Regenerate": command,
    }


def build_artifact_health_rows(
    output_dir: Path,
    dataset_name: str | None = None,
    run_instance: str | None = None,
) -> list[dict[str, object]]:
    """Report whether each dashboard input artifact exists."""
    paths = get_dashboard_artifact_paths(output_dir, dataset_name, run_instance)
    expected_paths = [
        (
            paths["history"],
            "judged round history",
            "python util.py loop --max-iterations 1",
        ),
        (
            paths["strategy"],
            "latest focus area and guidance",
            "python util.py loop --max-iterations 1",
        ),
        (
            paths["output_csv"],
            "current master CSV",
            "python util.py loop --max-iterations 1",
        ),
        (
            paths["mutation_success"],
            "mutation success sidecar",
            "python util.py loop --max-iterations 1",
        ),
        (
            paths["mutation_failures"],
            "mutation failure sidecar",
            "python util.py loop --max-iterations 1",
        ),
        (
            paths["exported_logs"],
            "structured round logs",
            "python util.py loop --max-iterations 1",
        ),
        (
            paths["run_events"],
            "run-level trace events",
            "python util.py loop --max-iterations 1",
        ),
        (
            paths["proposal_events"],
            "proposal and result trace events",
            "python util.py loop --max-iterations 1",
        ),
        (
            paths["row_decisions"],
            "per-invoice trace decisions",
            "python util.py loop --max-iterations 1",
        ),
        (
            paths["otel_spans"],
            "OTEL-style span stream",
            "python util.py loop --max-iterations 1",
        ),
        (
            paths["otel_events"],
            "OTEL-style event stream",
            "python util.py loop --max-iterations 1",
        ),
        (
            paths["otel_logs"],
            "OTEL-style log stream",
            "python util.py loop --max-iterations 1",
        ),
    ]
    if run_instance is not None:
        expected_paths.extend(
            [
                (
                    paths["manifest"],
                    "run selector manifest",
                    "python util.py loop --named-instance <name>",
                ),
                (
                    paths["diagnostics"],
                    "run diagnostics summary",
                    "python util.py loop --named-instance <name>",
                ),
            ]
        )
    return [
        _artifact_row(path, purpose, command)
        for path, purpose, command in expected_paths
    ]


def list_run_summaries(output_dir: Path) -> list[dict[str, object]]:
    """Return manifest-backed run summaries for dashboard selection."""
    runs_dir = cleanloop_datasets.get_runs_dir(output_dir)
    if not runs_dir.exists():
        return []

    summaries: list[dict[str, object]] = []
    for run_dir in sorted(runs_dir.iterdir()):
        if not run_dir.is_dir():
            continue
        manifest_path = cleanloop_datasets.get_run_manifest_path(
            output_dir, run_dir.name
        )
        manifest = _read_json_object(manifest_path)
        if not manifest:
            manifest = {"run_instance": run_dir.name, "status": "unknown"}
        summaries.append(
            {
                "Run Instance": manifest.get("run_instance", run_dir.name),
                "Dataset": manifest.get("dataset", "finance"),
                "Started": manifest.get("started_at", ""),
                "Finished": manifest.get("finished_at", ""),
                "Rounds": manifest.get("rounds", 0),
                "Latest Score": manifest.get("latest_score", "0/0"),
                "Status": manifest.get("status", "unknown"),
                "Trace ID": manifest.get("trace_id", ""),
                "Run ID": manifest.get("run_id", ""),
                "Path": str(run_dir),
            }
        )
    return sorted(summaries, key=lambda row: str(row.get("Started", "")), reverse=True)


def latest_run_instance(output_dir: Path) -> str | None:
    """Return the newest run instance if one has been saved."""
    summaries = list_run_summaries(output_dir)
    if not summaries:
        return None
    return str(summaries[0]["Run Instance"])


def load_dashboard_artifacts(
    output_dir: Path,
    dataset_name: str | None = None,
    run_instance: str | None = None,
) -> dict[str, list[dict[str, object]]]:
    """Load the exported trace and raw-log artifacts for dashboard rendering."""
    paths = get_dashboard_artifact_paths(output_dir, dataset_name, run_instance)
    return {
        "run_events": _read_jsonl_records(paths["run_events"]),
        "row_decisions": _read_jsonl_records(paths["row_decisions"]),
        "proposal_events": _read_jsonl_records(paths["proposal_events"]),
        "exported_logs": _read_jsonl_records(paths["exported_logs"]),
        "otel_spans": _read_jsonl_records(paths["otel_spans"]),
        "otel_events": _read_jsonl_records(paths["otel_events"]),
        "otel_logs": _read_jsonl_records(paths["otel_logs"]),
    }


def load_run_diagnostics(
    output_dir: Path,
    run_instance: str | None = None,
) -> dict[str, object]:
    """Load per-run diagnostics when a run instance is selected."""
    if run_instance is None:
        return {}
    return _read_json_object(
        cleanloop_datasets.get_run_diagnostics_path(output_dir, run_instance)
    )
