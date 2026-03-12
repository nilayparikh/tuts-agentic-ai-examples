// ---------------------------------------------------------------------------
// Environment Configuration
// ---------------------------------------------------------------------------
// Typed configuration loaded from environment variables.
// Defaults are suitable for local development.
// ---------------------------------------------------------------------------

export const config = {
  port: parseInt(process.env.PORT ?? "3100", 10),
  dbPath: process.env.DB_PATH ?? "./data/loan-workbench.db",
  logLevel: process.env.LOG_LEVEL ?? "info",

  rateLimiter: {
    windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS ?? "60000", 10),
    maxRequests: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS ?? "100", 10),
  },

  features: {
    californiaRules: process.env.FEATURE_CALIFORNIA_RULES !== "false",
    smsFallback: process.env.FEATURE_SMS_FALLBACK !== "false",
    queueAudit: process.env.FEATURE_QUEUE_AUDIT !== "false",
  },
} as const;
