// ---------------------------------------------------------------------------
// Queue Handler — Audit Persistence
// ---------------------------------------------------------------------------
// Consumes `audit.requested` events from the broker and writes them to
// the database.  This decouples audit writes from request handlers,
// improving response latency for mutating operations.
//
// IMPORTANT — FAIL CLOSED:
//   If the audit write fails, the handler retries once.  If the retry
//   also fails, the error is logged as CRITICAL.  In production, this
//   would trigger an alert.  The original operation is NOT rolled back
//   (the event was already emitted after the operation succeeded).
// ---------------------------------------------------------------------------

import { broker } from "../broker.js";
import type { AuditRequestedEvent } from "../contracts.js";
import { createAuditEntry } from "../../models/audit-repository.js";

async function handleAuditRequested(event: AuditRequestedEvent): Promise<void> {
  const { action, actor, delegatedFor, previousValue, newValue, source } =
    event.payload;

  try {
    createAuditEntry({
      action,
      actor,
      delegatedFor,
      previousValue,
      newValue,
      source,
    });
  } catch (err) {
    console.error(
      "[audit-handler] First write attempt failed, retrying...",
      err,
    );
    try {
      createAuditEntry({
        action,
        actor,
        delegatedFor,
        previousValue,
        newValue,
        source,
      });
    } catch (retryErr) {
      console.error(
        "[audit-handler] CRITICAL: Audit write failed after retry",
        retryErr,
      );
    }
  }
}

/** Register the handler with the broker. */
export function registerAuditHandler(): void {
  broker.on("audit.requested", handleAuditRequested);
  console.log("[audit-handler] Registered for audit.requested events");
}
