// ---------------------------------------------------------------------------
// Request Validator Middleware
// ---------------------------------------------------------------------------
// Validates request bodies against expected shapes before they reach
// route handlers.  Returns 400 with descriptive errors on failure.
//
// This is intentionally simple — no JSON Schema library dependency.
// For production, consider ajv or zod.
// ---------------------------------------------------------------------------

import type { Request, Response, NextFunction } from "express";

export type ValidationRule = {
  field: string;
  type: "string" | "number" | "boolean";
  required?: boolean;
};

/**
 * Factory that returns middleware validating req.body against the given rules.
 */
export function validateBody(rules: ValidationRule[]) {
  return (req: Request, res: Response, next: NextFunction): void => {
    const errors: string[] = [];

    for (const rule of rules) {
      const value = req.body?.[rule.field];

      if (value === undefined || value === null) {
        if (rule.required) {
          errors.push(`Missing required field: '${rule.field}'`);
        }
        continue;
      }

      if (typeof value !== rule.type) {
        errors.push(
          `Field '${rule.field}' must be ${rule.type}, got ${typeof value}`,
        );
      }
    }

    if (errors.length > 0) {
      res.status(400).json({ error: "Validation failed.", details: errors });
      return;
    }

    next();
  };
}
