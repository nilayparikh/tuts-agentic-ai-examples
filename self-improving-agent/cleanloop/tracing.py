"""Structured tracing helpers for CleanLoop runs, rounds, and row decisions."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


def _iso_now() -> str:
    """Return a stable UTC timestamp for trace events."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class TraceRecorder:
    """Write structured JSONL trace records beside CleanLoop artifacts."""

    output_dir: Path
    component: str
    trace_id: str | None = None
    run_id: str | None = None
    traces_dir: Path = field(init=False)
    run_events_path: Path = field(init=False)
    row_decisions_path: Path = field(init=False)
    proposal_events_path: Path = field(init=False)

    def __post_init__(self) -> None:
        """Prepare the trace directory and stable identifiers."""
        self.trace_id = self.trace_id or uuid4().hex
        self.run_id = self.run_id or uuid4().hex
        self.traces_dir = self.output_dir / "traces"
        self.traces_dir.mkdir(parents=True, exist_ok=True)
        self.run_events_path = self.traces_dir / "run-events.jsonl"
        self.row_decisions_path = self.traces_dir / "row-decisions.jsonl"
        self.proposal_events_path = self.traces_dir / "proposal-events.jsonl"

    def child(self, component: str) -> "TraceRecorder":
        """Create a child recorder that shares the run and trace identifiers."""
        return TraceRecorder(
            output_dir=self.output_dir,
            component=component,
            trace_id=self.trace_id,
            run_id=self.run_id,
        )

    def _append(self, path: Path, payload: dict[str, Any]) -> None:
        """Append one JSON record to a trace file."""
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, sort_keys=True) + "\n")

    def _base_payload(self, stage: str, decision: str, **fields: Any) -> dict[str, Any]:
        """Build the common payload shared by all trace records."""
        payload: dict[str, Any] = {
            "timestamp": _iso_now(),
            "trace_id": self.trace_id,
            "run_id": self.run_id,
            "component": self.component,
            "stage": stage,
            "decision": decision,
        }
        payload.update(fields)
        return payload

    def record_run_event(self, stage: str, decision: str, **fields: Any) -> None:
        """Record one run-level event."""
        self._append(
            self.run_events_path,
            self._base_payload(stage, decision, **fields),
        )

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
        self._append(
            self.row_decisions_path,
            self._base_payload(
                stage,
                decision,
                invoice_id=invoice_id,
                source_file=source_file,
                **fields,
            ),
        )

    def record_proposal_event(self, stage: str, decision: str, **fields: Any) -> None:
        """Record one proposal or selection event."""
        self._append(
            self.proposal_events_path,
            self._base_payload(stage, decision, **fields),
        )
