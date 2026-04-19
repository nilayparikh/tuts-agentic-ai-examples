// ---------------------------------------------------------------------------
// Loan Service
// ---------------------------------------------------------------------------
// Orchestrates loan operations: creation, state transitions, and risk
// scoring.  Delegates persistence to the loan repository, rule validation
// to the rules layer, and event emission to the broker.
// ---------------------------------------------------------------------------

import { v4 as uuid } from "uuid";
import * as loanRepo from "../models/loan-repository.js";
import { assertTransition } from "../rules/state-machine.js";
import { validateLoanRules, canApprove } from "../rules/business-rules.js";
import { getMandatoryEvents } from "../rules/mandatory-events.js";
import { broker } from "../queue/broker.js";
import type {
  LoanApplication,
  SessionContext,
  ApplicationState,
} from "../models/types.js";
import type {
  LoanStateChangedEvent,
  NotificationRequestedEvent,
} from "../queue/contracts.js";

/**
 * Create a new loan application.
 * Validates business rules before persisting.
 */
export function createLoan(
  session: SessionContext,
  data: { borrowerName: string; amount: number; loanState: string },
): LoanApplication {
  if (session.delegatedFor) {
    throw new Error("FORBIDDEN: Delegated sessions cannot create loans.");
  }

  // Build a partial loan to validate rules
  const draft = {
    ...data,
    loanState: data.loanState.toUpperCase(),
  } as LoanApplication;
  const violations = validateLoanRules(draft);
  if (violations.length > 0) {
    throw new Error(
      `VALIDATION: ${violations.map((v) => v.message).join("; ")}`,
    );
  }

  return loanRepo.createLoan({
    borrowerName: data.borrowerName,
    amount: data.amount,
    loanState: data.loanState,
    assignedUnderwriter: session.actor.id,
  });
}

/**
 * Transition a loan to a new state.
 * Enforces state machine rules, emits state-changed events,
 * and triggers mandatory notifications.
 */
export function transitionLoan(
  session: SessionContext,
  applicationId: string,
  newStatus: ApplicationState,
): LoanApplication {
  if (session.delegatedFor) {
    throw new Error("FORBIDDEN: Delegated sessions cannot transition loans.");
  }

  const loan = loanRepo.findLoanById(applicationId);
  if (!loan) {
    throw new Error(`NOT_FOUND: Application '${applicationId}' not found.`);
  }

  // Enforce state machine
  assertTransition(loan.status, newStatus);

  const previousStatus = loan.status;
  const updated = loanRepo.updateLoanStatus(applicationId, newStatus);
  if (!updated) {
    throw new Error(`NOT_FOUND: Application '${applicationId}' not found.`);
  }

  // Emit state-changed event
  const stateEvent: LoanStateChangedEvent = {
    eventId: uuid(),
    timestamp: new Date().toISOString(),
    source: "loan-service",
    type: "loan.state-changed",
    payload: {
      applicationId,
      previousStatus,
      newStatus,
      changedBy: session.actor.id,
    },
  };
  broker.emit(stateEvent);

  // Emit mandatory notification events
  const mandatoryEvents = getMandatoryEvents(previousStatus, newStatus);
  for (const event of mandatoryEvents) {
    const notifEvent: NotificationRequestedEvent = {
      eventId: uuid(),
      timestamp: new Date().toISOString(),
      source: "loan-service",
      type: "notification.requested",
      payload: {
        userId: loan.assignedUnderwriter,
        event,
        subject: `Loan ${applicationId}: ${previousStatus} → ${newStatus}`,
        body: `Application ${applicationId} transitioned from ${previousStatus} to ${newStatus}.`,
        preferredChannel: "email",
      },
    };
    broker.emit(notifEvent);
  }

  return updated;
}
