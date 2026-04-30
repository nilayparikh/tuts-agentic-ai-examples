"""Structured tracing helpers for CleanLoop runs, rounds, and row decisions."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from cleanloop import datasets as cleanloop_datasets

TRACE_ID_ENV = "CLEANLOOP_TRACE_ID"
RUN_ID_ENV = "CLEANLOOP_RUN_ID"
RUN_INSTANCE_ENV = "CLEANLOOP_RUN_INSTANCE"
ROOT_SPAN_ID_ENV = "CLEANLOOP_ROOT_SPAN_ID"
TRACE_CONTEXT_ENV_KEYS = (
    TRACE_ID_ENV,
    RUN_ID_ENV,
    RUN_INSTANCE_ENV,
    ROOT_SPAN_ID_ENV,
)
SCOPE_VERSION = "cleanloop-otel-v1"


def _iso_now() -> str:
    """Return a stable UTC timestamp for trace events."""
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
    """Write structured JSONL trace records beside CleanLoop artifacts."""

    output_dir: Path
    component: str
    trace_id: str | None = None
    run_id: str | None = None
    run_instance: str | None = None
    root_span_id: str | None = None
    traces_dir: Path = field(init=False)
    run_traces_dir: Path = field(init=False)
    run_events_path: Path = field(init=False)
    run_instance_events_path: Path = field(init=False)
    row_decisions_path: Path = field(init=False)
    run_instance_row_decisions_path: Path = field(init=False)
    proposal_events_path: Path = field(init=False)
    run_instance_proposal_events_path: Path = field(init=False)
    otel_spans_path: Path = field(init=False)
    run_instance_otel_spans_path: Path = field(init=False)
    otel_events_path: Path = field(init=False)
    run_instance_otel_events_path: Path = field(init=False)
    otel_logs_path: Path = field(init=False)
    run_instance_otel_logs_path: Path = field(init=False)

    def __post_init__(self) -> None:
        """Prepare the trace directory and stable identifiers."""
        self.trace_id = self.trace_id or os.getenv(TRACE_ID_ENV) or uuid4().hex
        self.run_id = self.run_id or os.getenv(RUN_ID_ENV) or uuid4().hex
        self.run_instance = generate_run_instance(
            self.run_instance or os.getenv(RUN_INSTANCE_ENV)
        )
        self.root_span_id = (
            self.root_span_id or os.getenv(ROOT_SPAN_ID_ENV) or _span_id()
        )
        self.traces_dir = cleanloop_datasets.get_traces_dir(self.output_dir)
        self.traces_dir.mkdir(parents=True, exist_ok=True)
        self.run_traces_dir = cleanloop_datasets.get_run_traces_dir(
            self.output_dir,
            self.run_instance,
        )
        self.run_traces_dir.mkdir(parents=True, exist_ok=True)
        self.run_events_path = cleanloop_datasets.get_run_events_path(self.output_dir)
        self.run_instance_events_path = cleanloop_datasets.get_run_events_path(
            self.output_dir,
            self.run_instance,
        )
        self.row_decisions_path = cleanloop_datasets.get_row_decisions_path(
            self.output_dir
        )
        self.run_instance_row_decisions_path = (
            cleanloop_datasets.get_row_decisions_path(
                self.output_dir,
                self.run_instance,
            )
        )
        self.proposal_events_path = cleanloop_datasets.get_proposal_events_path(
            self.output_dir
        )
        self.run_instance_proposal_events_path = (
            cleanloop_datasets.get_proposal_events_path(
                self.output_dir,
                self.run_instance,
            )
        )
        self.otel_spans_path = cleanloop_datasets.get_otel_spans_path(self.output_dir)
        self.run_instance_otel_spans_path = cleanloop_datasets.get_otel_spans_path(
            self.output_dir,
            self.run_instance,
        )
        self.otel_events_path = cleanloop_datasets.get_otel_events_path(self.output_dir)
        self.run_instance_otel_events_path = cleanloop_datasets.get_otel_events_path(
            self.output_dir,
            self.run_instance,
        )
        self.otel_logs_path = cleanloop_datasets.get_otel_logs_path(self.output_dir)
        self.run_instance_otel_logs_path = cleanloop_datasets.get_otel_logs_path(
            self.output_dir,
            self.run_instance,
        )

    def child(self, component: str) -> "TraceRecorder":
        """Create a child recorder that shares the run and trace identifiers."""
        return TraceRecorder(
            output_dir=self.output_dir,
            component=component,
            trace_id=self.trace_id,
            run_id=self.run_id,
            run_instance=self.run_instance,
            root_span_id=self.root_span_id,
        )

    def install_context(self) -> dict[str, str | None]:
        """Publish this recorder's trace context to environment variables."""
        previous = {key: os.environ.get(key) for key in TRACE_CONTEXT_ENV_KEYS}
        os.environ[TRACE_ID_ENV] = str(self.trace_id)
        os.environ[RUN_ID_ENV] = str(self.run_id)
        os.environ[RUN_INSTANCE_ENV] = str(self.run_instance)
        os.environ[ROOT_SPAN_ID_ENV] = str(self.root_span_id)
        return previous

    def restore_context(self, previous: dict[str, str | None]) -> None:
        """Restore trace context environment variables after a run."""
        for key in TRACE_CONTEXT_ENV_KEYS:
            value = previous.get(key)
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

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
        payload.update(fields)
        return payload

    def _scope_name(self) -> str:
        """Return the instrumentation scope name for this recorder."""
        return f"cleanloop.{self.component}"

    def _resource(self) -> dict[str, Any]:
        """Return common resource attributes for OTEL-shaped records."""
        return {
            "service.name": "cleanloop",
            "service.namespace": "localm.tuts",
            "cleanloop.run_id": self.run_id,
            "cleanloop.run_instance": self.run_instance,
        }

    def _attributes(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Return JSON-safe OTEL attributes from one trace payload."""
        attributes = {
            "cleanloop.component": self.component,
            "cleanloop.stage": payload.get("stage"),
            "cleanloop.decision": payload.get("decision"),
            "cleanloop.run_id": self.run_id,
            "cleanloop.run_instance": self.run_instance,
        }
        for key, value in payload.items():
            if key in {"timestamp", "trace_id", "run_id", "run_instance"}:
                continue
            if key in {"component", "stage", "decision"}:
                continue
            attributes[f"cleanloop.{key}"] = _json_safe(value)
        return attributes

    def _correlation_fields(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Return top-level fields useful for dashboard business correlation."""
        fields: dict[str, Any] = {}
        for key in ("round", "invoice_id", "source_file", "dataset", "decision"):
            value = payload.get(key)
            if value is not None:
                fields[key] = _json_safe(value)
        return fields

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
        correlation = self._correlation_fields(payload)
        event_name = f"{payload.get('stage')}.{payload.get('decision')}"
        span = {
            "timestamp": timestamp,
            "trace_id": self.trace_id,
            "span_id": span_id,
            "parent_span_id": self.root_span_id,
            "name": f"{self.component}.{payload.get('stage')}",
            "kind": "INTERNAL",
            "start_time": timestamp,
            "end_time": timestamp,
            "status_code": "ERROR" if severity_text == "ERROR" else "OK",
            "scope_name": self._scope_name(),
            "scope_version": SCOPE_VERSION,
            "resource": self._resource(),
            "attributes": attributes,
            "run_id": self.run_id,
            "run_instance": self.run_instance,
            "component": self.component,
            "stage": payload.get("stage"),
            "decision": payload.get("decision"),
            **correlation,
        }
        event = {
            "timestamp": timestamp,
            "trace_id": self.trace_id,
            "span_id": span_id,
            "name": event_name,
            "event_type": event_type,
            "scope_name": self._scope_name(),
            "scope_version": SCOPE_VERSION,
            "resource": self._resource(),
            "attributes": attributes,
            "run_id": self.run_id,
            "run_instance": self.run_instance,
            "component": self.component,
            "stage": payload.get("stage"),
            "decision": payload.get("decision"),
            **correlation,
        }
        log_record = {
            "timestamp": timestamp,
            "trace_id": self.trace_id,
            "span_id": span_id,
            "severity_text": severity_text,
            "body": body or event_name,
            "scope_name": self._scope_name(),
            "scope_version": SCOPE_VERSION,
            "resource": self._resource(),
            "attributes": attributes,
            "run_id": self.run_id,
            "run_instance": self.run_instance,
            "component": self.component,
            "stage": payload.get("stage"),
            "decision": payload.get("decision"),
            **correlation,
        }
        self._append_each(
            (self.otel_spans_path, self.run_instance_otel_spans_path), span
        )
        self._append_each(
            (self.otel_events_path, self.run_instance_otel_events_path),
            event,
        )
        self._append_each(
            (self.otel_logs_path, self.run_instance_otel_logs_path), log_record
        )

    def record_run_event(self, stage: str, decision: str, **fields: Any) -> None:
        """Record one run-level event."""
        payload = self._base_payload(stage, decision, **fields)
        self._append_each(
            (self.run_events_path, self.run_instance_events_path), payload
        )
        self._append_otel_records(payload, event_type="run")

    def record_row_decision(
        self,
        *,
        stage: str,
        decision: str,
        invoice_id: str,
        source_file: str,
        **fields: Any,
    ) -> None:
        """Record one row-level decision for the finance fixture."""
        payload = self._base_payload(
            stage,
            decision,
            invoice_id=invoice_id,
            source_file=source_file,
            **fields,
        )
        self._append_each(
            (self.row_decisions_path, self.run_instance_row_decisions_path),
            payload,
        )
        self._append_otel_records(payload, event_type="row-decision")

    def record_proposal_event(self, stage: str, decision: str, **fields: Any) -> None:
        """Record one proposal or selection event."""
        payload = self._base_payload(stage, decision, **fields)
        self._append_each(
            (self.proposal_events_path, self.run_instance_proposal_events_path),
            payload,
        )
        self._append_otel_records(payload, event_type="proposal")

    def record_log(
        self,
        stage: str,
        message: str,
        *,
        severity_text: str = "INFO",
        **fields: Any,
    ) -> None:
        """Record one OTEL-style log line correlated to the current trace."""
        payload = self._base_payload(
            stage,
            "log",
            message=message,
            severity_text=severity_text,
            **fields,
        )
        self._append_otel_records(
            payload,
            event_type="log",
            body=message,
            severity_text=severity_text,
        )
