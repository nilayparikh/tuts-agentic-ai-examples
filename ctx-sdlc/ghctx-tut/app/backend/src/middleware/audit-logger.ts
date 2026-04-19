// ---------------------------------------------------------------------------
// Audit Logger Middleware
// ---------------------------------------------------------------------------
// Emits an `audit.requested` event for every mutating request (POST, PUT,
// PATCH, DELETE) that completes successfully.  The event is processed
// asynchronously by the queue's audit handler.
//
// Fine-grained audit entries (e.g. per-preference-field changes) are
// emitted by route handlers themselves; this middleware provides a
// baseline request-level audit log.
// ---------------------------------------------------------------------------

import type { Request, Response, NextFunction } from "express";
import { v4 as uuid } from "uuid";
import { broker } from "../queue/broker.js";
import type { AuditRequestedEvent } from "../queue/contracts.js";
import { featureFlags } from "../config/feature-flags.js";
import { createAuditEntry } from "../models/audit-repository.js";

const MUTATING_METHODS = new Set(["POST", "PUT", "PATCH", "DELETE"]);

export function auditLoggerMiddleware(
  req: Request,
  res: Response,
  next: NextFunction,
): void {
  if (!MUTATING_METHODS.has(req.method)) {
    next();
    return;
  }

  // Capture the original end() to inject audit logging after response.
  const originalEnd = res.end.bind(res);

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  (res as any).end = function (...args: unknown[]) {
    // Only audit successful operations.
    if (res.statusCode >= 200 && res.statusCode < 400 && req.session) {
      const auditPayload = {
        action: `${req.method} ${req.path}`,
        actor: req.session.actor.id,
        delegatedFor: req.session.delegatedFor?.id,
        previousValue: undefined,
        newValue: { statusCode: res.statusCode },
        source: "audit-logger-middleware",
      };

      if (featureFlags.queueAudit) {
        // Route through the message queue for async persistence
        const event: AuditRequestedEvent = {
          eventId: uuid(),
          timestamp: new Date().toISOString(),
          source: "audit-logger-middleware",
          type: "audit.requested",
          payload: auditPayload,
        };
        broker.emit(event);
      } else {
        // Synchronous fallback — write directly to DB
        try {
          createAuditEntry(auditPayload);
        } catch (err) {
          console.error("[audit-logger] Failed to write audit entry:", err);
        }
      }
    }
    return originalEnd(...(args as Parameters<Response["end"]>));
  };

  next();
}
