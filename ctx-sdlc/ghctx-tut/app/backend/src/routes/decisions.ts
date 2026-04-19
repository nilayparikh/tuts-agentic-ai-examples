// ---------------------------------------------------------------------------
// Decision Routes
// ---------------------------------------------------------------------------

import { Router } from "express";
import { requireRole } from "../middleware/auth.js";
import { validateBody } from "../middleware/request-validator.js";
import * as decisionService from "../services/decision-service.js";
import type { SessionContext } from "../models/types.js";

export const decisionRoutes = Router();

function firstParam(value: string | string[]): string {
  return Array.isArray(value) ? value[0] : value;
}

/** GET /api/decisions/:applicationId — get decisions for an application. */
decisionRoutes.get(
  "/:applicationId",
  requireRole("underwriter", "analyst-manager", "compliance-reviewer"),
  (req, res) => {
    const decisions = decisionService.getDecisionsForApplication(
      firstParam(req.params.applicationId),
    );
    res.json(decisions);
  },
);

/** POST /api/decisions — record a new decision. */
decisionRoutes.post(
  "/",
  requireRole("underwriter", "analyst-manager"),
  validateBody([
    { field: "applicationId", type: "string", required: true },
    { field: "type", type: "string", required: true },
    { field: "rationale", type: "string", required: true },
  ]),
  (req, res, next) => {
    try {
      const session = req.session as SessionContext;
      const { applicationId, type, rationale, conditions } = req.body;
      const decision = decisionService.recordDecision(
        session,
        applicationId,
        type,
        rationale,
        conditions,
      );
      res.status(201).json(decision);
    } catch (err) {
      next(err);
    }
  },
);
