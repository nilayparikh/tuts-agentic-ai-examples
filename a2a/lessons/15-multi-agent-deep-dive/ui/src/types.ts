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
  info_requested: number;
}

export type Decision = "APPROVED" | "DECLINED" | "INFO_REQUESTED";
