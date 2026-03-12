// ---------------------------------------------------------------------------
// Loan Application Routes
// ---------------------------------------------------------------------------

import { Router } from "express";
import { requireRole } from "../middleware/auth.js";
import { validateBody } from "../middleware/request-validator.js";
import { auditAction } from "../services/audit-service.js";
import * as loanService from "../services/loan-service.js";
import * as loanRepo from "../models/loan-repository.js";
import type { SessionContext, ApplicationState } from "../models/types.js";

export const applicationRoutes = Router();

/** GET /api/applications — list all applications. */
applicationRoutes.get(
  "/",
  requireRole("underwriter", "analyst-manager", "compliance-reviewer"),
  (req, res) => {
    const { status, underwriter } = req.query;
    if (status) {
      res.json(loanRepo.findLoansByStatus(status as ApplicationState));
    } else if (underwriter) {
      res.json(loanRepo.findLoansByUnderwriter(underwriter as string));
    } else {
      res.json(loanRepo.findAllLoans());
    }
  },
);

/** GET /api/applications/:id — get a single application. */
applicationRoutes.get(
  "/:id",
  requireRole("underwriter", "analyst-manager", "compliance-reviewer"),
  (req, res) => {
    const app = loanRepo.findLoanById(req.params.id);
    if (!app) {
      res.status(404).json({ error: "Application not found." });
      return;
    }
    res.json(app);
  },
);

/** POST /api/applications — create a new loan application. */
applicationRoutes.post(
  "/",
  requireRole("underwriter", "analyst-manager"),
  validateBody([
    { field: "borrowerName", type: "string", required: true },
    { field: "amount", type: "number", required: true },
    { field: "loanState", type: "string", required: true },
  ]),
  (req, res, next) => {
    try {
      const session = req.session as SessionContext;
      const loan = loanService.createLoan(session, req.body);
      res.status(201).json(loan);
    } catch (err) {
      next(err);
    }
  },
);

/**
 * PATCH /api/applications/:id/status — transition application state.
 *
 * The request body must include `{ status: ApplicationState }`.
 * Only legal transitions (per VALID_TRANSITIONS) are allowed.
 * Finalized applications cannot be transitioned at all.
 */
applicationRoutes.patch(
  "/:id/status",
  requireRole("underwriter", "analyst-manager"),
  validateBody([{ field: "status", type: "string", required: true }]),
  (req, res, next) => {
    try {
      const session = req.session as SessionContext;
      const updated = loanService.transitionLoan(
        session,
        req.params.id,
        req.body.status,
      );
      res.json(updated);
    } catch (err) {
      next(err);
    }
  },
);
