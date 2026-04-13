// ---------------------------------------------------------------------------
// Frontend API Response Types
// ---------------------------------------------------------------------------
// Mirror the backend types for use in the frontend.
// These MUST stay in sync with backend/src/models/types.ts.
// ---------------------------------------------------------------------------

export interface ApiLoanApplication {
  id: string;
  borrowerName: string;
  amount: number;
  loanState: string;
  status: string;
  assignedUnderwriter: string;
  riskScore: number | null;
  createdAt: string;
  updatedAt: string;
}

export interface ApiDecision {
  id: string;
  applicationId: string;
  type: "approved" | "declined" | "conditional";
  rationale: string;
  decidedBy: string;
  decidedAt: string;
  conditions?: string[];
}

export interface ApiPreference {
  userId: string;
  event: string;
  channel: string;
  enabled: boolean;
  updatedAt: string;
  updatedBy: string;
}

export interface ApiAuditEntry {
  id: string;
  action: string;
  actor: string;
  delegatedFor: string | null;
  timestamp: string;
  source: string;
}
