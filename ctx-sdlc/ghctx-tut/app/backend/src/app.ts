// ---------------------------------------------------------------------------
// Loan Workbench — Application Entry Point
// ---------------------------------------------------------------------------
// Express server with middleware chain, route mounting, database init,
// and message queue handler registration.
//
// MIDDLEWARE ORDER (matters!):
//   1. express.json()          — Parse JSON bodies
//   2. rateLimiterMiddleware   — Rate limit before auth (prevent brute force)
//   3. authMiddleware          — Authenticate & attach session context
//   4. auditLoggerMiddleware   — Log mutating requests (needs session)
//   5. Routes                  — Business logic
//   6. errorHandler            — Catch-all error handler (MUST be last)
// ---------------------------------------------------------------------------

import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import { config } from "./config/env.js";
import { getDb } from "./db/connection.js";
import { seedDatabase } from "./db/seed.js";
import { authMiddleware } from "./middleware/auth.js";
import { auditLoggerMiddleware } from "./middleware/audit-logger.js";
import { rateLimiterMiddleware } from "./middleware/rate-limiter.js";
import { errorHandler } from "./middleware/error-handler.js";
import { applicationRoutes } from "./routes/applications.js";
import { decisionRoutes } from "./routes/decisions.js";
import { notificationRoutes } from "./routes/notifications.js";
import { auditRoutes } from "./routes/audit.js";
import { queueStatusRoutes } from "./routes/queue-status.js";
import { registerNotificationHandler } from "./queue/handlers/notification-handler.js";
import { registerAuditHandler } from "./queue/handlers/audit-handler.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const app = express();

// ── Initialize database ──
getDb();
seedDatabase();

// ── Register queue handlers ──
registerNotificationHandler();
registerAuditHandler();

// ── Middleware chain (ORDER MATTERS) ──
app.use(express.json());
app.use(rateLimiterMiddleware);
app.use(authMiddleware);
app.use(auditLoggerMiddleware);

// ── API Routes ──
app.use("/api/applications", applicationRoutes);
app.use("/api/decisions", decisionRoutes);
app.use("/api/notifications", notificationRoutes);
app.use("/api/audit", auditRoutes);
app.use("/api/queue", queueStatusRoutes);

// ── Health check (no auth required — placed before auth middleware in request flow) ──
app.get("/health", (_req, res) => {
  res.json({ status: "ok", timestamp: new Date().toISOString() });
});

// ── Serve frontend static files ──
const frontendDir = path.resolve(__dirname, "../../frontend");
app.use(express.static(frontendDir));

// ── SPA fallback — serve index.html for non-API routes ──
app.get("*", (_req, res) => {
  res.sendFile(path.join(frontendDir, "index.html"));
});

// ── Error handler (MUST be last) ──
app.use(errorHandler);

app.listen(config.port, () => {
  console.log(`Loan Workbench API listening on port ${config.port}`);
  console.log(`Database: ${config.dbPath}`);
});

export default app;
