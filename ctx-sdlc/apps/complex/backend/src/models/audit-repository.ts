// ---------------------------------------------------------------------------
// Audit Entry Repository
// ---------------------------------------------------------------------------
// Database operations for the audit trail.  Audit entries are immutable —
// there is no update or delete.
//
// IMPORTANT: The audit trail is append-only.  Never expose a DELETE or
// UPDATE endpoint for audit entries.  Compliance requires the full history.
// ---------------------------------------------------------------------------

import { v4 as uuid } from "uuid";
import { getDb } from "../db/connection.js";
import type { AuditEntry } from "./types.js";

export function createAuditEntry(data: {
  action: string;
  actor: string;
  delegatedFor?: string | null;
  previousValue?: unknown;
  newValue?: unknown;
  source: string;
}): AuditEntry {
  const db = getDb();
  const id = uuid();
  const now = new Date().toISOString();

  db.prepare(
    `INSERT INTO audit_entries (id, action, actor, delegated_for, timestamp, previous_value, new_value, source)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
  ).run(
    id,
    data.action,
    data.actor,
    data.delegatedFor ?? null,
    now,
    data.previousValue != null ? JSON.stringify(data.previousValue) : null,
    data.newValue != null ? JSON.stringify(data.newValue) : null,
    data.source,
  );

  return {
    id,
    action: data.action,
    actor: data.actor,
    delegatedFor: data.delegatedFor ?? null,
    timestamp: now,
    previousValue: null,
    newValue: null,
    source: data.source,
  };
}

export function findAuditEntries(opts?: {
  actor?: string;
  limit?: number;
}): AuditEntry[] {
  const db = getDb();
  let sql = "SELECT * FROM audit_entries";
  const params: unknown[] = [];

  if (opts?.actor) {
    sql += " WHERE actor = ?";
    params.push(opts.actor);
  }

  sql += " ORDER BY timestamp DESC";

  if (opts?.limit) {
    sql += " LIMIT ?";
    params.push(opts.limit);
  }

  return db.prepare(sql).all(...params) as AuditEntry[];
}

export function findAuditEntriesByAction(action: string): AuditEntry[] {
  const db = getDb();
  return db
    .prepare(
      "SELECT * FROM audit_entries WHERE action = ? ORDER BY timestamp DESC",
    )
    .all(action) as AuditEntry[];
}
