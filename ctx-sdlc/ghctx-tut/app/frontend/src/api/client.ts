// ---------------------------------------------------------------------------
// API Client
// ---------------------------------------------------------------------------
// Typed HTTP client for the Loan Workbench backend API.
// All API calls go through this module — routes/pages never use fetch directly.
// ---------------------------------------------------------------------------

import type {
  ApiLoanApplication,
  ApiDecision,
  ApiPreference,
  ApiAuditEntry,
} from "./types.js";

const BASE_URL = "/api";

/** Current user ID — set by the app shell. */
let currentUserId = "u-1";

export function setCurrentUser(userId: string): void {
  currentUserId = userId;
}

export async function apiFetch<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    "x-user-id": currentUserId,
    ...((options.headers as Record<string, string>) ?? {}),
  };

  const res = await fetch(`${BASE_URL}${path}`, { ...options, headers });

  if (!res.ok) {
    const body = await res.json().catch(() => ({ error: res.statusText }));
    throw new Error(body.error ?? `HTTP ${res.status}`);
  }

  return res.json() as Promise<T>;
}

// ── Applications ──

export function getApplications(): Promise<ApiLoanApplication[]> {
  return apiFetch("/applications");
}

export function getApplication(id: string): Promise<ApiLoanApplication> {
  return apiFetch(`/applications/${encodeURIComponent(id)}`);
}

export function createApplication(data: {
  borrowerName: string;
  amount: number;
  loanState: string;
}): Promise<ApiLoanApplication> {
  return apiFetch("/applications", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function transitionApplication(
  id: string,
  status: string,
): Promise<ApiLoanApplication> {
  return apiFetch(`/applications/${encodeURIComponent(id)}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status }),
  });
}

// ── Decisions ──

export function getDecisions(applicationId: string): Promise<ApiDecision[]> {
  return apiFetch(`/decisions/${encodeURIComponent(applicationId)}`);
}

// ── Notifications ──

export function getPreferences(userId: string): Promise<ApiPreference[]> {
  return apiFetch(`/notifications/preferences/${encodeURIComponent(userId)}`);
}

export function setPreference(pref: {
  userId: string;
  event: string;
  channel: string;
  enabled: boolean;
}): Promise<ApiPreference> {
  return apiFetch("/notifications/preferences", {
    method: "PUT",
    body: JSON.stringify(pref),
  });
}

// ── Audit ──

export function getAuditEntries(limit = 50): Promise<ApiAuditEntry[]> {
  return apiFetch(`/audit?limit=${limit}`);
}
