// ---------------------------------------------------------------------------
// User Repository
// ---------------------------------------------------------------------------
// Database operations for users.
// ---------------------------------------------------------------------------

import { getDb } from "../db/connection.js";
import type { User } from "./types.js";

export function findUserById(id: string): User | undefined {
  const db = getDb();
  return db.prepare("SELECT * FROM users WHERE id = ?").get(id) as
    | User
    | undefined;
}

export function findAllUsers(): User[] {
  const db = getDb();
  return db.prepare("SELECT * FROM users ORDER BY name").all() as User[];
}

export function findUsersByRole(role: string): User[] {
  const db = getDb();
  return db
    .prepare("SELECT * FROM users WHERE role = ? ORDER BY name")
    .all(role) as User[];
}
