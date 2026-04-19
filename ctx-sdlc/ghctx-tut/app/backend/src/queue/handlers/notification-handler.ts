// ---------------------------------------------------------------------------
// Queue Handler — Notification Delivery
// ---------------------------------------------------------------------------
// Consumes `notification.requested` events from the broker and delivers
// notifications through the appropriate channel.
//
// IMPORTANT — SMS FALLBACK:
//   When the SMS provider is unavailable and the feature flag is enabled,
//   delivery falls back to email IF the user has email enabled for that
//   event.  The fallback does NOT change stored preferences — it is a
//   runtime delivery decision only.
// ---------------------------------------------------------------------------

import { broker } from "../broker.js";
import type { NotificationRequestedEvent } from "../contracts.js";
import { findPreferencesForUser } from "../../models/preference-repository.js";
import { featureFlags } from "../../config/feature-flags.js";

/** Simulated provider health.  Toggle in tests. */
const providerHealth = { email: true, sms: true };

export function setProviderHealth(
  channel: "email" | "sms",
  healthy: boolean,
): void {
  providerHealth[channel] = healthy;
}

export function getProviderHealth(): { email: boolean; sms: boolean } {
  return { ...providerHealth };
}

async function handleNotificationRequested(
  event: NotificationRequestedEvent,
): Promise<void> {
  const {
    userId,
    event: notifEvent,
    subject,
    body,
    preferredChannel,
  } = event.payload;

  const prefs = findPreferencesForUser(userId);
  const enabledChannels = prefs
    .filter((p) => p.event === notifEvent && p.enabled)
    .map((p) => p.channel);

  if (enabledChannels.length === 0) {
    console.log(
      `[notification-handler] No enabled channels for user=${userId} event=${notifEvent}`,
    );
    return;
  }

  for (const channel of enabledChannels) {
    if (providerHealth[channel]) {
      // Provider is healthy — deliver normally
      console.log(
        `[notification-handler] Delivered via ${channel}: "${subject}" to user=${userId}`,
      );
    } else if (
      featureFlags.smsFallback &&
      channel === "sms" &&
      providerHealth.email &&
      enabledChannels.includes("email")
    ) {
      // SMS is down, email is healthy, user has email enabled → fall back
      console.log(
        `[notification-handler] SMS unavailable — falling back to email: "${subject}" to user=${userId}`,
      );
    } else {
      console.warn(
        `[notification-handler] Cannot deliver via ${channel} — provider unhealthy, no fallback`,
      );
    }
  }
}

/** Register the handler with the broker. */
export function registerNotificationHandler(): void {
  broker.on("notification.requested", handleNotificationRequested);
  console.log(
    "[notification-handler] Registered for notification.requested events",
  );
}
