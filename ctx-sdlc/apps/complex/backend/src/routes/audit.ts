// ---------------------------------------------------------------------------
// Audit Routes
// ---------------------------------------------------------------------------
// Read-only access to the audit trail.  No mutations allowed via API.
// ---------------------------------------------------------------------------

import { Router } from "express";
import { requireRole } from "../middleware/auth.js";
import * as auditRepo from "../models/audit-repository.js";

export const auditRoutes = Router();

/** GET /api/audit — list recent audit entries. */
auditRoutes.get(
  "/",
  requireRole("underwriter", "analyst-manager", "compliance-reviewer"),
  (req, res) => {
    const limit = parseInt(req.query.limit as string, 10) || 100;
    const actor = req.query.actor as string | undefined;
    res.json(auditRepo.findAuditEntries({ actor, limit }));
  },
);

/** GET /api/audit/action/:action — filter by action type. */
auditRoutes.get(
  "/action/:action",
  requireRole("underwriter", "analyst-manager", "compliance-reviewer"),
  (req, res) => {
    res.json(auditRepo.findAuditEntriesByAction(req.params.action));
  },
);
