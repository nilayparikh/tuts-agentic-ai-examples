// ---------------------------------------------------------------------------
// Notification Service
// ---------------------------------------------------------------------------
// High-level API for sending notifications.  Route handlers call this
// service, which emits events to the message broker.  Actual delivery is
// handled by queue/handlers/notification-handler.ts.
//
// NFR REQUIREMENT — DEGRADED MODE:
//   When the SMS provider is unavailable, delivery must fall back to email
//   IF email is enabled for that event.  The fallback must NOT change the
//   user's stored preferences — it is a runtime delivery decision only.
//
// KEY NUANCE — FALSE POSITIVE:
//   A user receiving an email instead of an SMS during an SMS outage is NOT
//   a preference bug.  The stored preference still says "sms: true" — the
//   delivery system silently fell back.  Support agents must check delivery
//   logs, not the preference store, to diagnose delivery complaints.
// ---------------------------------------------------------------------------

import { v4 as uuid } from "uuid";
import { broker } from "../queue/broker.js";
import type { NotificationRequestedEvent } from "../queue/contracts.js";
import type {
  NotificationEvent,
  NotificationChannel,
} from "../models/types.js";

/**
 * Request notification delivery for a user.
 * The actual delivery is asynchronous via the message queue.
 */
export function requestNotification(
  userId: string,
  event: NotificationEvent,
  subject: string,
  body: string,
  preferredChannel: NotificationChannel = "email",
): void {
  const notifEvent: NotificationRequestedEvent = {
    eventId: uuid(),
    timestamp: new Date().toISOString(),
    source: "notification-service",
    type: "notification.requested",
    payload: { userId, event, subject, body, preferredChannel },
  };
  broker.emit(notifEvent);
}
