// ---------------------------------------------------------------------------
// Centralized Error Handler
// ---------------------------------------------------------------------------
// Express error middleware — must be registered LAST in the middleware chain.
// Maps known error patterns to appropriate HTTP status codes.
// ---------------------------------------------------------------------------

import type { Request, Response, NextFunction } from "express";

export function errorHandler(
  err: Error,
  _req: Request,
  res: Response,
  _next: NextFunction,
): void {
  // Map known error prefixes to HTTP status codes.
  if (err.message.startsWith("FORBIDDEN:")) {
    res.status(403).json({ error: err.message });
    return;
  }
  if (err.message.startsWith("INVALID_STATE:")) {
    res.status(409).json({ error: err.message });
    return;
  }
  if (err.message.startsWith("NOT_FOUND:")) {
    res.status(404).json({ error: err.message });
    return;
  }
  if (err.message.startsWith("VALIDATION:")) {
    res.status(400).json({ error: err.message });
    return;
  }

  console.error("[error-handler] Unhandled error:", err);
  res.status(500).json({ error: "Internal server error." });
}
