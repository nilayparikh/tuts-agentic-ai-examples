/**
 * Shared TypeScript types for the loan approval UI.
 */

export type EscalationStatus =
  | "PENDING"
  | "APPROVED"
  | "DECLINED"
  | "INFO_REQUESTED";

export interface ComplianceFlag {
  rule: string;
  severity: "hard" | "soft";
  message: string;
}

export interface EscalatedApplication {
  id: string;
  applicant_id: string;
  full_name: string;
  application_data: Record<string, unknown>;
  risk_score: number;
  reasoning: string;
  risk_factors: string[];
  compensating_factors: string[];
  compliance_flags: ComplianceFlag[];
  compliance_conditions: string[];
  status: EscalationStatus;
  escalated_at: string;
  decided_at: string | null;
  decided_by: string | null;
  decision_notes: string | null;
}

export interface Stats {
  total: number;
  pending: number;
  approved: number;
  declined: number;
  escalated: number;
  human_approved: number;
  human_declined: number;
  info_requested: number;
}

export type Decision = "APPROVED" | "DECLINED" | "INFO_REQUESTED";

/** A fully processed loan — all pipeline stages captured. */
export interface ProcessedLoanRecord {
  id: string;
  applicant_id: string;
  full_name: string;
  decision: "APPROVED" | "DECLINED" | "PENDING_REVIEW" | "REJECTED" | string;
  action:
    | "AUTO_APPROVE"
    | "AUTO_DECLINE"
    | "ESCALATE"
    | "INTAKE_REJECTED"
    | string;
  reason: string;
  score: number;
  compliant: boolean;
  risk_factors: string[];
  compensating_factors: string[];
  flags: ComplianceFlag[];
  conditions: string[];
  reasoning: string;
  application_data: Record<string, unknown>;
  processed_at: string;
  thresholds: { auto_approve?: number; auto_decline?: number };
  escalation_id: string | null;
  // Human decision (if escalated and reviewed)
  human_decision: string | null;
  human_decided_at: string | null;
  human_decided_by: string | null;
  human_decision_notes: string | null;
}
