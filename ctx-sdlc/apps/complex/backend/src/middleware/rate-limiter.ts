// ---------------------------------------------------------------------------
// Rate Limiter Middleware
// ---------------------------------------------------------------------------
// Token-bucket rate limiter applied per user (by x-user-id header).
// Unauthenticated requests are rate-limited by IP.
//
// NFR REQUIREMENT:
//   Rate limits must be configurable via environment variables.
//   When a client exceeds the limit, respond with 429 and a Retry-After
//   header.  Do NOT block the request silently — the client must know.
// ---------------------------------------------------------------------------

import type { Request, Response, NextFunction } from "express";
import { config } from "../config/env.js";

interface Bucket {
  tokens: number;
  lastRefill: number;
}

const buckets = new Map<string, Bucket>();

function getBucketKey(req: Request): string {
  const userId = req.headers["x-user-id"] as string | undefined;
  return userId ?? req.ip ?? "unknown";
}

export function rateLimiterMiddleware(
  req: Request,
  res: Response,
  next: NextFunction,
): void {
  // Skip rate limiting for health checks
  if (req.path === "/health") {
    next();
    return;
  }

  const key = getBucketKey(req);
  const now = Date.now();
  const { windowMs, maxRequests } = config.rateLimiter;

  let bucket = buckets.get(key);
  if (!bucket) {
    bucket = { tokens: maxRequests, lastRefill: now };
    buckets.set(key, bucket);
  }

  // Refill tokens based on elapsed time
  const elapsed = now - bucket.lastRefill;
  if (elapsed >= windowMs) {
    bucket.tokens = maxRequests;
    bucket.lastRefill = now;
  }

  if (bucket.tokens <= 0) {
    const retryAfter = Math.ceil((windowMs - (now - bucket.lastRefill)) / 1000);
    res.set("Retry-After", String(retryAfter));
    res.status(429).json({ error: "Rate limit exceeded.", retryAfter });
    return;
  }

  bucket.tokens--;
  next();
}
