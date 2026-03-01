/**
 * API client for the Escalation REST API.
 */

import type {
  Decision,
  EscalatedApplication,
  ProcessedLoanRecord,
  Stats,
} from "./types";

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
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`Failed to submit decision (${res.status}): ${detail}`);
  }
  return res.json();
}

/** Fetch all processed loan records from the loan history store. */
export async function fetchLoans(): Promise<ProcessedLoanRecord[]> {
  const res = await fetch(`${BASE}/loans`);
  if (!res.ok) throw new Error(`Failed to fetch loans: ${res.statusText}`);
  return res.json();
}

/** Fetch a single processed loan record by ID. */
export async function fetchLoan(loanId: string): Promise<ProcessedLoanRecord> {
  const res = await fetch(`${BASE}/loans/${loanId}`);
  if (!res.ok) throw new Error(`Failed to fetch loan: ${res.statusText}`);
  return res.json();
}
