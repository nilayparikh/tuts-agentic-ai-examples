// ---------------------------------------------------------------------------
// Notification Preference Routes
// ---------------------------------------------------------------------------
//
// IMPORTANT — AUTHORIZATION:
//   All roles can READ preferences (for display purposes).
//   Only underwriters and analyst-managers can WRITE preferences.
//   Compliance reviewers are READ-ONLY for notification preferences.
//
// IMPORTANT — DELEGATED SESSIONS:
//   A delegated session (x-delegated-for header) can read the delegate's
//   preferences but CANNOT modify them.  The route handler must check
//   session.delegatedFor before allowing writes.
// ---------------------------------------------------------------------------

import { Router } from "express";
import { requireRole } from "../middleware/auth.js";
import { validateBody } from "../middleware/request-validator.js";
import { hasPermission } from "../rules/role-permissions.js";
import { auditAction } from "../services/audit-service.js";
import * as prefRepo from "../models/preference-repository.js";
import type {
  SessionContext,
  NotificationPreference,
} from "../models/types.js";

export const notificationRoutes = Router();

/** GET /api/notifications/preferences/:userId — get preferences for a user. */
notificationRoutes.get(
  "/preferences/:userId",
  requireRole("underwriter", "analyst-manager", "compliance-reviewer"),
  (req, res) => {
    const prefs = prefRepo.findPreferencesForUser(req.params.userId);
    res.json(prefs);
  },
);

/** PUT /api/notifications/preferences — set a notification preference. */
notificationRoutes.put(
  "/preferences",
  requireRole("underwriter", "analyst-manager"),
  validateBody([
    { field: "userId", type: "string", required: true },
    { field: "event", type: "string", required: true },
    { field: "channel", type: "string", required: true },
    { field: "enabled", type: "boolean", required: true },
  ]),
  (req, res, next) => {
    try {
      const session = req.session as SessionContext;

      // Block writes in delegated sessions
      if (session.delegatedFor) {
        res.status(403).json({
          error: "Delegated sessions cannot modify notification preferences.",
        });
        return;
      }

      // Additional permission check
      if (!hasPermission(session.actor.role, "notification-pref:write")) {
        res.status(403).json({
          error: `Role '${session.actor.role}' cannot modify notification preferences.`,
        });
        return;
      }

      const { userId, event, channel, enabled } = req.body;
      const now = new Date().toISOString();

      const previous = prefRepo.findPreference(userId, event, channel);

      const pref: NotificationPreference = {
        userId,
        event,
        channel,
        enabled,
        updatedAt: now,
        updatedBy: session.actor.id,
      };

      prefRepo.setPreference(pref);

      // Audit the preference change
      auditAction(
        session,
        "preference.updated",
        previous ?? null,
        pref,
        "notification-routes",
      );

      res.json(pref);
    } catch (err) {
      next(err);
    }
  },
);
