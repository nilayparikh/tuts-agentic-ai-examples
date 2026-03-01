/**
 * API client for the Escalation REST API.
 */

import type { Decision, EscalatedApplication, Stats } from "./types";

const BASE = "/api";

export async function fetchPending(): Promise<EscalatedApplication[]> {
  const res = await fetch(`${BASE}/escalations/pending`);
  if (!res.ok) throw new Error(`Failed to fetch pending: ${res.statusText}`);
  return res.json();
}

export async function fetchAll(): Promise<EscalatedApplication[]> {
  const res = await fetch(`${BASE}/escalations`);
  if (!res.ok) throw new Error(`Failed to fetch all: ${res.statusText}`);
  return res.json();
}

export async function fetchStats(): Promise<Stats> {
  const res = await fetch(`${BASE}/stats`);
  if (!res.ok) throw new Error(`Failed to fetch stats: ${res.statusText}`);
  return res.json();
}

export async function submitDecision(
  recordId: string,
  decision: Decision,
  reviewer: string,
  notes: string = "",
): Promise<EscalatedApplication> {
  const res = await fetch(`${BASE}/escalations/${recordId}/decide`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ decision, reviewer, notes }),
  });
  if (!res.ok) throw new Error(`Failed to submit decision: ${res.statusText}`);
  return res.json();
}
