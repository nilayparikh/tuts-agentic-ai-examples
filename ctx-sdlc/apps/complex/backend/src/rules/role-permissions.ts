// ---------------------------------------------------------------------------
// Role Permissions Matrix
// ---------------------------------------------------------------------------
// Defines what each role can do across the system.  This is the single
// source of truth for authorization decisions beyond route-level guards.
//
// IMPORTANT — COMPLIANCE REVIEWER NUANCE:
//   Compliance reviewers have READ access to most resources but WRITE access
//   only to compliance-specific actions (sign-offs, compliance notes).
//   They CANNOT modify notification preferences, even though they can view
//   them.  This is frequently missed by code generators.
// ---------------------------------------------------------------------------

import type { UserRole } from "../models/types.js";

export type Permission =
  | "loan:read"
  | "loan:create"
  | "loan:transition"
  | "decision:read"
  | "decision:create"
  | "notification-pref:read"
  | "notification-pref:write"
  | "audit:read"
  | "compliance:sign-off";

const ROLE_PERMISSIONS: Record<UserRole, Set<Permission>> = {
  underwriter: new Set([
    "loan:read",
    "loan:create",
    "loan:transition",
    "decision:read",
    "decision:create",
    "notification-pref:read",
    "notification-pref:write",
    "audit:read",
  ]),
  "analyst-manager": new Set([
    "loan:read",
    "loan:create",
    "loan:transition",
    "decision:read",
    "decision:create",
    "notification-pref:read",
    "notification-pref:write",
    "audit:read",
  ]),
  "compliance-reviewer": new Set([
    "loan:read",
    "decision:read",
    "notification-pref:read", // READ only — no write
    "audit:read",
    "compliance:sign-off",
  ]),
};

export function hasPermission(role: UserRole, permission: Permission): boolean {
  return ROLE_PERMISSIONS[role]?.has(permission) ?? false;
}

export function getPermissions(role: UserRole): Permission[] {
  return [...(ROLE_PERMISSIONS[role] ?? [])];
}
