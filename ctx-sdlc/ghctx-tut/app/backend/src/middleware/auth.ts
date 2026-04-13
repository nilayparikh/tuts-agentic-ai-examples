// ---------------------------------------------------------------------------
// Authentication & Authorization Middleware
// ---------------------------------------------------------------------------
//
// KEY NUANCE — DELEGATED SESSIONS:
//   When the `x-delegated-for` header is present, the session is marked as
//   delegated.  Delegated sessions allow READ operations on the delegate's
//   data but BLOCK writes.  An AI assistant without context would likely
//   skip this distinction, producing code that allows delegated writes.
//
// KEY NUANCE — COMPLIANCE REVIEWER:
//   Compliance reviewers can view notification preferences and audit logs
//   but cannot modify operational settings.  This is a read-only role for
//   the notification feature, even though the role has write permissions
//   in other parts of the system.
// ---------------------------------------------------------------------------

import type { Request, Response, NextFunction } from "express";
import type { UserRole, SessionContext } from "../models/types.js";
import { findUserById } from "../models/user-repository.js";

// Extend Express Request to carry session context.
declare global {
  namespace Express {
    interface Request {
      session?: SessionContext;
    }
  }
}

/**
 * Authenticate the request and attach a SessionContext.
 *
 * In production this would validate a JWT or session cookie.  For the
 * demo we resolve the user from an `x-user-id` header and optionally
 * attach delegated-session context from `x-delegated-for`.
 */
export function authMiddleware(
  req: Request,
  res: Response,
  next: NextFunction,
): void {
  // Skip auth for health check.
  if (req.path === "/health") {
    next();
    return;
  }

  const userId = req.headers["x-user-id"] as string | undefined;
  if (!userId) {
    res.status(401).json({ error: "Missing x-user-id header." });
    return;
  }

  const actor = findUserById(userId);
  if (!actor) {
    res.status(401).json({ error: `Unknown user '${userId}'.` });
    return;
  }

  const session: SessionContext = { actor };

  // Check for delegated session.
  const delegatedId = req.headers["x-delegated-for"] as string | undefined;
  if (delegatedId) {
    const delegate = findUserById(delegatedId);
    if (!delegate) {
      res.status(400).json({ error: `Unknown delegate '${delegatedId}'.` });
      return;
    }
    session.delegatedFor = delegate;
  }

  req.session = session;
  next();
}

/**
 * Role-gate middleware factory.
 * Returns 403 if the actor's role is not in the allowed set.
 */
export function requireRole(...roles: UserRole[]) {
  const allowed = new Set(roles);
  return (req: Request, res: Response, next: NextFunction): void => {
    if (!req.session) {
      res.status(401).json({ error: "Not authenticated." });
      return;
    }
    if (!allowed.has(req.session.actor.role)) {
      res.status(403).json({
        error: `Role '${req.session.actor.role}' is not authorized for this operation.`,
      });
      return;
    }
    next();
  };
}
