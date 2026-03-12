// ---------------------------------------------------------------------------
// Database Connection
// ---------------------------------------------------------------------------
// Provides a singleton better-sqlite3 connection to the Loan Workbench
// SQLite database.  The connection is created lazily on first access.
//
// IMPORTANT: better-sqlite3 is synchronous — all queries block the event
// loop.  This is acceptable for this application's scale.  Do NOT wrap
// calls in Promises — it adds overhead without benefit.
// ---------------------------------------------------------------------------

import Database from "better-sqlite3";
import { readFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { mkdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { config } from "../config/env.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

let _db: Database.Database | null = null;

/**
 * Get the database connection, creating it if necessary.
 * On first call, runs schema.sql to ensure tables exist.
 */
export function getDb(): Database.Database {
  if (_db) return _db;

  // Ensure the data directory exists
  const dbDir = dirname(config.dbPath);
  mkdirSync(dbDir, { recursive: true });

  _db = new Database(config.dbPath);
  _db.pragma("journal_mode = WAL");
  _db.pragma("foreign_keys = ON");

  // Apply schema
  const schema = readFileSync(join(__dirname, "schema.sql"), "utf-8");
  _db.exec(schema);

  return _db;
}

/**
 * Close the database connection.  Used in tests and graceful shutdown.
 */
export function closeDb(): void {
  if (_db) {
    _db.close();
    _db = null;
  }
}
