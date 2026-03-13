// ---------------------------------------------------------------------------
// Decision Service
// ---------------------------------------------------------------------------
// Records underwriting decisions and triggers downstream notification
// delivery.  Decisions can only be recorded for applications in the
// "decision" state — the state-machine guard is enforced here.
// ---------------------------------------------------------------------------

import { v4 as uuid } from "uuid";
import { getDb } from "../db/connection.js";
import type {
  Decision,
  LoanApplication,
  SessionContext,
} from "../models/types.js";
import { findLoanById } from "../models/loan-repository.js";
import { canApprove } from "../rules/business-rules.js";
import { broker } from "../queue/broker.js";
import type {
  AuditRequestedEvent,
  NotificationRequestedEvent,
} from "../queue/contracts.js";

/**
 * Record a decision against a loan application.
 *
 * Validation:
 *  - Application must be in "decision" state.
 *  - Only authorized roles can record decisions (based on loan amount).
 *  - Delegated sessions cannot record decisions.
 *  - The decision is audited via the message queue.
 */
export function recordDecision(
  session: SessionContext,
  applicationId: string,
  type: Decision["type"],
  rationale: string,
  conditions?: string[],
): Decision {
  // Guard: delegated sessions cannot record decisions.
  if (session.delegatedFor) {
    throw new Error(
      "FORBIDDEN: Decisions cannot be recorded in delegated sessions.",
    );
  }

  const application = findLoanById(applicationId);
  if (!application) {
    throw new Error(`NOT_FOUND: Application '${applicationId}' not found.`);
  }

  // Guard: application state.
  if (application.status !== "decision") {
    throw new Error(
      `INVALID_STATE: Cannot record a decision for application in ` +
        `'${application.status}' state. Expected 'decision'.`,
    );
  }

  // Guard: role + amount check.
  if (!canApprove(session.actor.role, application.amount)) {
    throw new Error(
      `FORBIDDEN: Role '${session.actor.role}' cannot approve loans of $${application.amount.toLocaleString()}.`,
    );
  }

  const id = uuid();
  const now = new Date().toISOString();
  const decision: Decision = {
    id,
    applicationId,
    type,
    rationale,
    decidedBy: session.actor.id,
    decidedAt: now,
    conditions,
  };

  // Persist decision
  const db = getDb();
  db.prepare(
    `INSERT INTO decisions (id, application_id, type, rationale, decided_by, decided_at, conditions)
     VALUES (?, ?, ?, ?, ?, ?, ?)`,
  ).run(
    id,
    applicationId,
    type,
    rationale,
    session.actor.id,
    now,
    conditions ? JSON.stringify(conditions) : null,
  );

  // Emit audit event
  const auditEvent: AuditRequestedEvent = {
    eventId: uuid(),
    timestamp: now,
    source: "decision-service",
    type: "audit.requested",
    payload: {
      action: "decision.recorded",
      actor: session.actor.id,
      previousValue: undefined,
      newValue: decision,
      source: "decision-service",
    },
  };
  broker.emit(auditEvent);

  // Emit notification for the assigned underwriter
  const notifEvent: NotificationRequestedEvent = {
    eventId: uuid(),
    timestamp: now,
    source: "decision-service",
    type: "notification.requested",
    payload: {
      userId: application.assignedUnderwriter,
      event: type === "declined" ? "decline" : "approval",
      subject: `Decision recorded: ${type} for ${applicationId}`,
      body: `A ${type} decision has been recorded for application ${applicationId}. Rationale: ${rationale}`,
      preferredChannel: "email",
    },
  };
  broker.emit(notifEvent);

  return decision;
}

/**
 * Retrieve all decisions for a given application.
 */
export function getDecisionsForApplication(applicationId: string): Decision[] {
  const db = getDb();
  return db
    .prepare(
      "SELECT * FROM decisions WHERE application_id = ? ORDER BY decided_at DESC",
    )
    .all(applicationId) as Decision[];
}
