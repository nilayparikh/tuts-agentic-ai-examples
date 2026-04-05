// ---------------------------------------------------------------------------
// Queue Status Routes — Event Broker Visibility
// ---------------------------------------------------------------------------
// Provides read-only endpoints to inspect the in-process event broker:
// subscriptions, recent event history, and pending event count.
// Useful for debugging and understanding the event-driven architecture.
// ---------------------------------------------------------------------------

import { Router } from "express";
import { broker } from "../queue/broker.js";

export const queueStatusRoutes = Router();

/** GET /api/queue/subscriptions — list registered event handlers. */
queueStatusRoutes.get("/subscriptions", (_req, res) => {
  const subs = broker.getSubscriptions().map((s) => ({
    event: s.type,
    handlerCount: s.handlerCount,
  }));
  res.json(subs);
});

/** GET /api/queue/history — recent events processed by the broker. */
queueStatusRoutes.get("/history", (req, res) => {
  const limit = Math.min(
    parseInt(String(req.query.limit ?? "50"), 10) || 50,
    200,
  );
  const history = broker.getHistory(limit).map((h) => ({
    event: h.event.type,
    processedAt: h.processedAt,
    dataKeys: Object.keys(h.event).filter((k) => k !== "type"),
  }));
  res.json(history);
});

/** GET /api/queue/status — broker health summary. */
queueStatusRoutes.get("/status", (_req, res) => {
  const subs = broker.getSubscriptions().map((s) => ({
    event: s.type,
    handlerCount: s.handlerCount,
  }));
  res.json({
    pendingCount: broker.getPendingCount(),
    subscriptions: subs,
    recentEventCount: broker.getHistory(5).length,
  });
});
