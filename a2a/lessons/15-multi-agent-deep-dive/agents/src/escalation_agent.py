"""
EscalationAgent — Queue borderline loan applications for human review.

Manages an in-memory escalation queue and exposes a FastAPI REST API
for the React frontend to poll pending reviews and submit decisions.

The A2A side accepts escalation requests from the DecisionAgent.
The REST side serves the React approval dashboard.

Environment variables
---------------------
  ESCALATION_API_PORT  Port for the REST API (default: 8080)
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel

from telemetry import tracer

logger = logging.getLogger("escalation_agent")

# ─── In-memory escalation store ──────────────────────────────────────────────

_EscalationStatus = Literal["PENDING", "APPROVED", "DECLINED", "INFO_REQUESTED"]


class EscalationRecord(BaseModel):
    """A single escalated loan application awaiting human review."""

    id: str
    applicant_id: str
    full_name: str
    application_data: dict
    risk_score: int
    reasoning: str
    risk_factors: list[str]
    compensating_factors: list[str]
    compliance_flags: list[dict]
    compliance_conditions: list[str]
    status: _EscalationStatus = "PENDING"
    escalated_at: str = ""
    decided_at: str | None = None
    decided_by: str | None = None
    decision_notes: str | None = None


class EscalationStore:
    """Thread-safe in-memory store for escalated applications."""

    def __init__(self) -> None:
        self._records: dict[str, EscalationRecord] = {}

    def add(self, record: EscalationRecord) -> str:
        """Add a new escalation record. Return its ID."""
        self._records[record.id] = record
        logger.info(
            "[%s] Escalation record stored (id=%s, score=%d)",
            record.applicant_id,
            record.id,
            record.risk_score,
        )
        return record.id

    def get_pending(self) -> list[EscalationRecord]:
        """Return all pending escalation records."""
        return [r for r in self._records.values() if r.status == "PENDING"]

    def get_all(self) -> list[EscalationRecord]:
        """Return all escalation records."""
        return list(self._records.values())

    def get(self, record_id: str) -> EscalationRecord | None:
        """Get a specific record by ID."""
        return self._records.get(record_id)

    def decide(
        self,
        record_id: str,
        decision: _EscalationStatus,
        reviewer: str,
        notes: str = "",
    ) -> EscalationRecord | None:
        """Record a human decision on an escalated application."""
        record = self._records.get(record_id)
        if record is None:
            logger.warning("Decision on unknown escalation id=%s", record_id)
            return None
        record.status = decision
        record.decided_at = datetime.now(timezone.utc).isoformat()
        record.decided_by = reviewer
        record.decision_notes = notes
        logger.info(
            "[%s] Human decision: %s by %s (id=%s)",
            record.applicant_id,
            decision,
            reviewer,
            record_id,
        )
        return record


# Singleton store shared between A2A agent and REST API
escalation_store = EscalationStore()


class EscalationAgent:
    """Queue borderline applications for human review."""

    def __init__(self, store: EscalationStore | None = None) -> None:
        self._store = store or escalation_store

    async def escalate(self, decision_data_json: str) -> str:
        """Create an escalation record from a DecisionAgent result.

        Returns JSON confirmation with the escalation ID.
        """
        with tracer.start_as_current_span("queue_for_review") as span:
            data = json.loads(decision_data_json)
            app_id = data.get("applicant_id", "unknown")
            span.set_attribute("applicant_id", app_id)

            logger.info(
                "[%s] ── Escalation Queued ──────────────────────────",
                app_id,
            )
            logger.info(
                "[%s] Name: %s | Score: %s | Reason: %s",
                app_id,
                data.get("application", {}).get("full_name", "Unknown"),
                data.get("score", "N/A"),
                data.get("reasoning", "N/A")[:120],
            )

            record = EscalationRecord(
                id=str(uuid4()),
                applicant_id=app_id,
                full_name=data.get("application", {}).get("full_name", "Unknown"),
                application_data=data.get("application", {}),
                risk_score=data.get("score", 0),
                reasoning=data.get("reasoning", ""),
                risk_factors=data.get("risk_factors", []),
                compensating_factors=data.get("compensating_factors", []),
                compliance_flags=data.get("flags", []),
                compliance_conditions=data.get("conditions", []),
                escalated_at=datetime.now(timezone.utc).isoformat(),
            )

            esc_id = self._store.add(record)
            span.set_attribute("escalation_id", esc_id)

            return json.dumps(
                {
                    "applicant_id": app_id,
                    "escalation_id": esc_id,
                    "status": "PENDING",
                    "message": "Application queued for human review",
                }
            )


# ─── FastAPI REST API for React frontend ─────────────────────────────────────


def create_rest_app():
    """Create the FastAPI app for the escalation REST API."""
    from fastapi import (
        FastAPI,
        HTTPException,
    )  # pylint: disable=import-outside-toplevel
    from fastapi.middleware.cors import (
        CORSMiddleware,
    )  # pylint: disable=import-outside-toplevel

    app = FastAPI(title="Escalation Review API", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/escalations/pending")
    async def get_pending():
        """Return all pending escalation records."""
        return [r.model_dump() for r in escalation_store.get_pending()]

    @app.get("/api/escalations")
    async def get_all():
        """Return all escalation records."""
        return [r.model_dump() for r in escalation_store.get_all()]

    @app.get("/api/escalations/{record_id}")
    async def get_record(record_id: str):
        """Return a specific escalation record."""
        record = escalation_store.get(record_id)
        if record is None:
            raise HTTPException(status_code=404, detail="Record not found")
        return record.model_dump()

    class DecisionRequest(BaseModel):
        """Request body for submitting a human decision."""

        decision: Literal["APPROVED", "DECLINED", "INFO_REQUESTED"]
        reviewer: str
        notes: str = ""

    @app.post("/api/escalations/{record_id}/decide")
    async def submit_decision(record_id: str, req: DecisionRequest):
        """Submit a human decision on an escalated application."""
        record = escalation_store.decide(
            record_id, req.decision, req.reviewer, req.notes
        )
        if record is None:
            raise HTTPException(status_code=404, detail="Record not found")
        return record.model_dump()

    @app.get("/api/stats")
    async def get_stats():
        """Return aggregate statistics for the dashboard."""
        all_records = escalation_store.get_all()
        return {
            "total": len(all_records),
            "pending": len([r for r in all_records if r.status == "PENDING"]),
            "approved": len([r for r in all_records if r.status == "APPROVED"]),
            "declined": len([r for r in all_records if r.status == "DECLINED"]),
            "info_requested": len(
                [r for r in all_records if r.status == "INFO_REQUESTED"]
            ),
        }

    return app
