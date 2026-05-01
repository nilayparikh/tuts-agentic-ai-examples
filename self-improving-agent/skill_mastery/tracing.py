"""Structured tracing helpers for Skill Mastery runs."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

SCOPE_VERSION = "skill-mastery-otel-v1"


def _iso_now() -> str:
    """Return a stable UTC timestamp for trace records."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _span_id() -> str:
    """Return a compact OpenTelemetry-style span id."""
    return uuid4().hex[:16]


def _json_safe(value: Any) -> Any:
    """Convert values to JSON-safe primitives for trace attributes."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    return str(value)


def normalize_run_instance(value: str | None) -> str:
    """Normalize a provided run-instance name into a safe folder segment."""
    text = str(value or "").strip().lower()
    if not text:
        return ""
    normalized = re.sub(r"[^a-z0-9._-]+", "-", text).strip(".-_")
    normalized = re.sub(r"-+", "-", normalized)
    return normalized[:80] or "run"


def generate_run_instance(named_instance: str | None = None) -> str:
    """Return the provided run instance or generate a unique one."""
    normalized = normalize_run_instance(named_instance)
    if normalized:
        return normalized
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"run-{timestamp}-{uuid4().hex[:8]}"


@dataclass
class TraceRecorder:
    """Write structured Skill Mastery trace records beside output artifacts."""

    output_dir: Path
    component: str = "skill_mastery"
    trace_id: str | None = None
    run_id: str | None = None
    run_instance: str | None = None
    root_span_id: str | None = None
    traces_dir: Path = field(init=False)
    run_traces_dir: Path = field(init=False)
    run_events_path: Path = field(init=False)
    run_instance_events_path: Path = field(init=False)
    habit_events_path: Path = field(init=False)
    run_instance_habit_events_path: Path = field(init=False)
    llm_requests_path: Path = field(init=False)
    run_instance_llm_requests_path: Path = field(init=False)
    evaluator_events_path: Path = field(init=False)
    run_instance_evaluator_events_path: Path = field(init=False)
    otel_spans_path: Path = field(init=False)
    run_instance_otel_spans_path: Path = field(init=False)
    otel_events_path: Path = field(init=False)
    run_instance_otel_events_path: Path = field(init=False)
    otel_logs_path: Path = field(init=False)
    run_instance_otel_logs_path: Path = field(init=False)

    def __post_init__(self) -> None:
        """Prepare the trace directory and stable identifiers."""
        self.trace_id = self.trace_id or uuid4().hex
        self.run_id = self.run_id or uuid4().hex
        self.run_instance = generate_run_instance(self.run_instance)
        self.root_span_id = self.root_span_id or _span_id()
        self.traces_dir = self.output_dir / "traces"
        self.run_traces_dir = self.traces_dir / "runs" / self.run_instance
        self.traces_dir.mkdir(parents=True, exist_ok=True)
        self.run_traces_dir.mkdir(parents=True, exist_ok=True)
        self.run_events_path = self.traces_dir / "run_events.jsonl"
        self.run_instance_events_path = self.run_traces_dir / "run_events.jsonl"
        self.habit_events_path = self.traces_dir / "habit_events.jsonl"
        self.run_instance_habit_events_path = self.run_traces_dir / "habit_events.jsonl"
        self.llm_requests_path = self.traces_dir / "llm_requests.jsonl"
        self.run_instance_llm_requests_path = self.run_traces_dir / "llm_requests.jsonl"
        self.evaluator_events_path = self.traces_dir / "evaluator_events.jsonl"
        self.run_instance_evaluator_events_path = (
            self.run_traces_dir / "evaluator_events.jsonl"
        )
        self.otel_spans_path = self.traces_dir / "otel_spans.jsonl"
        self.run_instance_otel_spans_path = self.run_traces_dir / "otel_spans.jsonl"
        self.otel_events_path = self.traces_dir / "otel_events.jsonl"
        self.run_instance_otel_events_path = self.run_traces_dir / "otel_events.jsonl"
        self.otel_logs_path = self.traces_dir / "otel_logs.jsonl"
        self.run_instance_otel_logs_path = self.run_traces_dir / "otel_logs.jsonl"

    def metadata(self) -> dict[str, str]:
        """Return the trace identifiers stored in the saved session payload."""
        return {
            "trace_id": str(self.trace_id),
            "run_id": str(self.run_id),
            "run_instance": str(self.run_instance),
            "root_span_id": str(self.root_span_id),
            "traces_dir": str(self.traces_dir),
        }

    def _append(self, path: Path, payload: dict[str, Any]) -> None:
        """Append one JSON record to a trace file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, sort_keys=True) + "\n")

    def _append_each(self, paths: tuple[Path, Path], payload: dict[str, Any]) -> None:
        """Append one payload to both global and per-run files."""
        for path in paths:
            self._append(path, payload)

    def _base_payload(self, stage: str, decision: str, **fields: Any) -> dict[str, Any]:
        """Build the common payload shared by all trace records."""
        payload: dict[str, Any] = {
            "timestamp": _iso_now(),
            "trace_id": self.trace_id,
            "run_id": self.run_id,
            "run_instance": self.run_instance,
            "component": self.component,
            "stage": stage,
            "decision": decision,
        }
        payload.update({key: _json_safe(value) for key, value in fields.items()})
        return payload

    def _resource(self) -> dict[str, Any]:
        """Return common resource attributes for OTEL-shaped records."""
        return {
            "service.name": "skill-mastery",
            "service.namespace": "localm.tuts",
            "skill_mastery.run_id": self.run_id,
            "skill_mastery.run_instance": self.run_instance,
        }

    def _attributes(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Return JSON-safe OTEL attributes from one trace payload."""
        attributes = {
            "skill_mastery.component": self.component,
            "skill_mastery.stage": payload.get("stage"),
            "skill_mastery.decision": payload.get("decision"),
            "skill_mastery.run_id": self.run_id,
            "skill_mastery.run_instance": self.run_instance,
        }
        for key, value in payload.items():
            if key in {"timestamp", "trace_id", "run_id", "run_instance"}:
                continue
            if key in {"component", "stage", "decision"}:
                continue
            attributes[f"skill_mastery.{key}"] = _json_safe(value)
        return attributes

    def _append_otel_records(
        self,
        payload: dict[str, Any],
        *,
        event_type: str,
        body: str | None = None,
        severity_text: str = "INFO",
    ) -> None:
        """Write span, event, and log records for one trace payload."""
        timestamp = str(payload["timestamp"])
        span_id = _span_id()
        attributes = self._attributes(payload)
        event_name = f"{payload.get('stage')}.{payload.get('decision')}"
        common = {
            "timestamp": timestamp,
            "trace_id": self.trace_id,
            "span_id": span_id,
            "scope_name": f"skill_mastery.{self.component}",
            "scope_version": SCOPE_VERSION,
            "resource": self._resource(),
            "attributes": attributes,
            "run_id": self.run_id,
            "run_instance": self.run_instance,
            "component": self.component,
            "stage": payload.get("stage"),
            "decision": payload.get("decision"),
            "round": payload.get("round"),
            "usecase_slug": payload.get("usecase_slug"),
        }
        span = {
            **common,
            "parent_span_id": self.root_span_id,
            "name": f"{self.component}.{payload.get('stage')}",
            "kind": "INTERNAL",
            "start_time": timestamp,
            "end_time": timestamp,
            "status_code": "ERROR" if severity_text == "ERROR" else "OK",
        }
        event = {**common, "name": event_name, "event_type": event_type}
        log_record = {
            **common,
            "severity_text": severity_text,
            "body": body or event_name,
        }
        self._append_each(
            (self.otel_spans_path, self.run_instance_otel_spans_path), span
        )
        self._append_each(
            (self.otel_events_path, self.run_instance_otel_events_path), event
        )
        self._append_each(
            (self.otel_logs_path, self.run_instance_otel_logs_path), log_record
        )

    def record_event(self, stage: str, decision: str, **fields: Any) -> None:
        """Record one run-level event."""
        payload = self._base_payload(stage, decision, **fields)
        self._append_each(
            (self.run_events_path, self.run_instance_events_path), payload
        )
        self._append_otel_records(payload, event_type="run")

    def record_habits(
        self,
        *,
        stage: str,
        decision: str,
        habit_slugs: list[str],
        usecase_slug: str | None,
        **fields: Any,
    ) -> None:
        """Record learned or selected habit-card events."""
        payload = self._base_payload(
            stage,
            decision,
            habit_slugs=habit_slugs,
            habit_count=len(habit_slugs),
            usecase_slug=usecase_slug,
            **fields,
        )
        self._append_each(
            (self.habit_events_path, self.run_instance_habit_events_path), payload
        )
        self._append_otel_records(payload, event_type="habit")

    def record_llm_request(
        self,
        *,
        round_number: int,
        request: dict[str, Any],
        usecase_slug: str | None,
    ) -> None:
        """Record one LLM request summary."""
        payload = self._base_payload(
            "llm_request",
            str(request.get("kind") or "unknown"),
            round=round_number,
            usecase_slug=usecase_slug,
            **request,
        )
        self._append_each(
            (self.llm_requests_path, self.run_instance_llm_requests_path), payload
        )
        self._append_otel_records(payload, event_type="llm")

    def record_evaluation(
        self,
        *,
        round_number: int,
        score: int,
        total: int,
        issues: list[str],
        strengths: list[str],
        usecase_slug: str | None,
    ) -> None:
        """Record one deterministic evaluator result."""
        payload = self._base_payload(
            "evaluation",
            "scored",
            round=round_number,
            usecase_slug=usecase_slug,
            score=score,
            total=total,
            issue_count=len(issues),
            strength_count=len(strengths),
            issues=issues,
            strengths=strengths,
        )
        self._append_each(
            (
                self.evaluator_events_path,
                self.run_instance_evaluator_events_path,
            ),
            payload,
        )
        self._append_otel_records(payload, event_type="evaluation")
