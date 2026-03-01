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


# ─── Full processed-loan history store ───────────────────────────────────────

_LoanDecision = Literal["APPROVED", "DECLINED", "PENDING_REVIEW", "REJECTED"]
_LoanAction = Literal["AUTO_APPROVE", "AUTO_DECLINE", "ESCALATE", "INTAKE_REJECTED"]


class ProcessedLoanRecord(BaseModel):
    """A fully processed loan application — all pipeline stages captured."""

    id: str
    applicant_id: str
    full_name: str
    decision: _LoanDecision
    action: _LoanAction
    reason: str
    score: int
    compliant: bool
    risk_factors: list[str] = []
    compensating_factors: list[str] = []
    flags: list[dict] = []
    conditions: list[str] = []
    reasoning: str = ""
    application_data: dict = {}
    processed_at: str = ""
    thresholds: dict = {}
    escalation_id: str | None = None
    # Set when a human makes a decision on an escalated application
    human_decision: str | None = None
    human_decided_at: str | None = None
    human_decided_by: str | None = None
    human_decision_notes: str | None = None


class LoanHistoryStore:
    """In-memory store for all processed loan applications."""

    def __init__(self) -> None:
        self._records: dict[str, ProcessedLoanRecord] = {}

    def add(self, record: ProcessedLoanRecord) -> str:
        """Add a processed loan record. Returns its ID."""
        self._records[record.id] = record
        logger.info(
            "[%s] Loan history stored (id=%s, decision=%s, score=%d)",
            record.applicant_id,
            record.id,
            record.decision,
            record.score,
        )
        return record.id

    def get_all(self) -> list[ProcessedLoanRecord]:
        """Return all records, newest first."""
        return sorted(
            self._records.values(), key=lambda r: r.processed_at, reverse=True
        )

    def get(self, record_id: str) -> ProcessedLoanRecord | None:
        """Get a specific record by ID."""
        return self._records.get(record_id)

    def update_human_decision(
        self,
        record_id: str,
        human_decision: Literal["APPROVED", "DECLINED", "INFO_REQUESTED"],
        decided_by: str,
        notes: str = "",
    ) -> ProcessedLoanRecord | None:
        """Sync human decision back into the loan history record."""
        record = self._records.get(record_id)
        if record is None:
            return None
        record.human_decision = human_decision
        record.human_decided_at = datetime.now(timezone.utc).isoformat()
        record.human_decided_by = decided_by
        record.human_decision_notes = notes
        if human_decision == "APPROVED":
            record.decision = "APPROVED"
        elif human_decision == "DECLINED":
            record.decision = "DECLINED"
        return record


# Singleton shared between REST API and orchestrator callbacks
loan_history_store = LoanHistoryStore()


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


class DecisionRequest(BaseModel):
    """Request body for submitting a human decision."""

    decision: Literal["APPROVED", "DECLINED", "INFO_REQUESTED"]
    reviewer: str = "Reviewer"
    notes: str | None = ""


class LoanRecordIn(BaseModel):
    """Payload posted by the orchestrator after each pipeline run."""

    applicant_id: str
    full_name: str = "Unknown"
    decision: str
    action: str
    reason: str = ""
    score: int = 0
    compliant: bool = True
    risk_factors: list[str] = []
    compensating_factors: list[str] = []
    flags: list[dict] = []
    conditions: list[str] = []
    reasoning: str = ""
    application_data: dict = {}
    thresholds: dict = {}
    escalation_id: str | None = None
    decided_at: str | None = None


# ─── FastAPI REST API for React frontend ─────────────────────────────────────


def create_rest_app():
    """Create the FastAPI app for the escalation REST API."""
    from fastapi import (  # pylint: disable=import-outside-toplevel
        Body,
        FastAPI,
        HTTPException,
        Request,
    )
    from fastapi.exceptions import (  # pylint: disable=import-outside-toplevel
        RequestValidationError,
    )
    from fastapi.middleware.cors import (  # pylint: disable=import-outside-toplevel
        CORSMiddleware,
    )
    from fastapi.responses import (  # pylint: disable=import-outside-toplevel
        JSONResponse,
    )

    app = FastAPI(title="Escalation Review API", version="1.0.0")

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        """Log and return a structured 422 with full details."""
        logger.error(
            "Validation error on %s %s: %s", request.method, request.url, exc.errors()
        )
        return JSONResponse(status_code=422, content={"detail": exc.errors()})

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
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

    @app.post("/api/escalations/{record_id}/decide")
    async def submit_decision(
        record_id: str,
        req: DecisionRequest = Body(...),
    ):
        """Submit a human decision on an escalated application."""
        record = escalation_store.decide(
            record_id, req.decision, req.reviewer, req.notes or ""
        )
        if record is None:
            raise HTTPException(status_code=404, detail="Record not found")
        # Sync back to loan history store via escalation_id match
        for loan in loan_history_store.get_all():
            if loan.escalation_id == record_id:
                loan_history_store.update_human_decision(
                    loan.id, req.decision, req.reviewer, req.notes or ""
                )
                break
        return record.model_dump()

    @app.get("/api/stats")
    async def get_stats():
        """Return aggregate statistics for the dashboard — includes all processed loans."""
        loans = loan_history_store.get_all()
        esc_records = escalation_store.get_all()
        return {
            "total": len(loans),
            "approved": len([r for r in loans if r.decision == "APPROVED"]),
            "declined": len([r for r in loans if r.decision == "DECLINED"]),
            "escalated": len([r for r in loans if r.action == "ESCALATE"]),
            "pending": len([r for r in esc_records if r.status == "PENDING"]),
            "human_approved": len([r for r in esc_records if r.status == "APPROVED"]),
            "human_declined": len([r for r in esc_records if r.status == "DECLINED"]),
            "info_requested": len(
                [r for r in esc_records if r.status == "INFO_REQUESTED"]
            ),
        }

    # ── Loan history endpoints ────────────────────────────────────────────────

    @app.post("/api/loans")
    async def ingest_loan(payload: LoanRecordIn = Body(...)):
        """Accept a processed loan record from the orchestrator."""
        record = ProcessedLoanRecord(
            id=str(uuid4()),
            applicant_id=payload.applicant_id,
            full_name=payload.full_name,
            decision=payload.decision,  # type: ignore[arg-type]
            action=payload.action,  # type: ignore[arg-type]
            reason=payload.reason,
            score=payload.score,
            compliant=payload.compliant,
            risk_factors=payload.risk_factors,
            compensating_factors=payload.compensating_factors,
            flags=payload.flags,
            conditions=payload.conditions,
            reasoning=payload.reasoning,
            application_data=payload.application_data,
            processed_at=payload.decided_at or datetime.now(timezone.utc).isoformat(),
            thresholds=payload.thresholds,
            escalation_id=payload.escalation_id,
        )
        loan_history_store.add(record)
        return record.model_dump()

    @app.get("/api/loans")
    async def get_loans():
        """Return all processed loan records ordered newest first."""
        return [r.model_dump() for r in loan_history_store.get_all()]

    @app.get("/api/loans/{loan_id}")
    async def get_loan(loan_id: str):
        """Return a specific processed loan record."""
        record = loan_history_store.get(loan_id)
        if record is None:
            raise HTTPException(status_code=404, detail="Loan record not found")
        return record.model_dump()

    return app
