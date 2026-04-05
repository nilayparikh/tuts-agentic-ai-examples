// ---------------------------------------------------------------------------
// Audit Service
// ---------------------------------------------------------------------------
// High-level audit API.  Provides convenience methods that emit events
// to the message queue (or write directly depending on feature flags).
// ---------------------------------------------------------------------------

import { v4 as uuid } from "uuid";
import { broker } from "../queue/broker.js";
import { featureFlags } from "../config/feature-flags.js";
import { createAuditEntry } from "../models/audit-repository.js";
import type { AuditRequestedEvent } from "../queue/contracts.js";
import type { SessionContext } from "../models/types.js";

/**
 * Write an audit entry for an action performed in a session context.
 */
export function auditAction(
  session: SessionContext,
  action: string,
  previousValue: unknown,
  newValue: unknown,
  source: string,
): void {
  const payload = {
    action,
    actor: session.actor.id,
    delegatedFor: session.delegatedFor?.id,
    previousValue,
    newValue,
    source,
  };

  if (featureFlags.queueAudit) {
    const event: AuditRequestedEvent = {
      eventId: uuid(),
      timestamp: new Date().toISOString(),
      source,
      type: "audit.requested",
      payload,
    };
    broker.emit(event);
  } else {
    createAuditEntry(payload);
  }
}
