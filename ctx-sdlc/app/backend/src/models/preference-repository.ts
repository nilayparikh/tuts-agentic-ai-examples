// ---------------------------------------------------------------------------
// Notification Preference Repository
// ---------------------------------------------------------------------------
// Database operations for notification preferences.
//
// KEY NUANCE — UPSERT BEHAVIOR:
//   The `setPreference` function uses INSERT OR REPLACE on the composite
//   primary key (user_id, event, channel).  This means updating a preference
//   replaces the entire row — there is no partial update.  The `updated_by`
//   field MUST always be set (it tracks who last changed the preference).
// ---------------------------------------------------------------------------

import { getDb } from "../db/connection.js";
import type {
  NotificationPreference,
  NotificationEvent,
  NotificationChannel,
} from "./types.js";

const PREFERENCE_COLUMNS = `
  user_id AS userId,
  event,
  channel,
  enabled,
  updated_at AS updatedAt,
  updated_by AS updatedBy
`;

type PreferenceRow = NotificationPreference & { enabled: number | boolean };

export function findPreferencesForUser(
  userId: string,
): NotificationPreference[] {
  const db = getDb();
  return db
    .prepare(
      `SELECT ${PREFERENCE_COLUMNS} FROM notification_preferences WHERE user_id = ?`,
    )
    .all(userId)
    .map((pref) => pref as PreferenceRow)
    .map((pref) => ({
      ...pref,
      enabled: Boolean(pref.enabled),
    })) as NotificationPreference[];
}

export function findPreference(
  userId: string,
  event: NotificationEvent,
  channel: NotificationChannel,
): NotificationPreference | undefined {
  const db = getDb();
  const pref = db
    .prepare(
      `SELECT ${PREFERENCE_COLUMNS} FROM notification_preferences WHERE user_id = ? AND event = ? AND channel = ?`,
    )
    .get(userId, event, channel) as
    | (NotificationPreference & { enabled: number | boolean })
    | undefined;

  return pref ? { ...pref, enabled: Boolean(pref.enabled) } : undefined;
}

export function setPreference(pref: NotificationPreference): void {
  const db = getDb();
  db.prepare(
    `INSERT OR REPLACE INTO notification_preferences (user_id, event, channel, enabled, updated_at, updated_by)
     VALUES (?, ?, ?, ?, ?, ?)`,
  ).run(
    pref.userId,
    pref.event,
    pref.channel,
    pref.enabled ? 1 : 0,
    pref.updatedAt,
    pref.updatedBy,
  );
}

export function deletePreferencesForUser(userId: string): number {
  const db = getDb();
  const result = db
    .prepare("DELETE FROM notification_preferences WHERE user_id = ?")
    .run(userId);
  return result.changes;
}
