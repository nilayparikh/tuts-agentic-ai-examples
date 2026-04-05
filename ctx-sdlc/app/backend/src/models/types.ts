// ---------------------------------------------------------------------------
// Loan Workbench — Domain Types
// ---------------------------------------------------------------------------
// This file defines the core domain model for the Loan Workbench platform.
// Business rules, state machines, authorization logic, queue contracts, and
// database schema all depend on these types.  Changes here affect nearly
// every module in the project.
// ---------------------------------------------------------------------------

/** Lifecycle states for a commercial loan application. */
export type ApplicationState =
  | "intake"
  | "review"
  | "underwriting"
  | "decision"
  | "finalized";

/**
 * Valid state transitions.
 * Transitions not listed here are forbidden — the system must never allow
 * a finalized application to move backward.
 */
export const VALID_TRANSITIONS: Record<ApplicationState, ApplicationState[]> = {
  intake: ["review"],
  review: ["underwriting", "intake"], // can return to intake for rework
  underwriting: ["decision"],
  decision: ["finalized", "underwriting"], // can push back to underwriting
  finalized: [], // terminal — no transitions allowed
};

/** Organizational roles recognized by the Loan Workbench. */
export type UserRole =
  | "underwriter"
  | "analyst-manager"
  | "compliance-reviewer";

/** Notification event types that can trigger user-facing alerts. */
export type NotificationEvent =
  | "approval"
  | "decline"
  | "document-request"
  | "manual-review-escalation";

/** Delivery channels available for notifications. */
export type NotificationChannel = "email" | "sms";

// ---------------------------------------------------------------------------
// Entity interfaces
// ---------------------------------------------------------------------------

export interface User {
  id: string;
  role: UserRole;
  name: string;
  email: string;
  phone?: string;
}

/**
 * Session context attached to every authenticated request.
 *
 * When `delegatedFor` is present the actor is operating on behalf of another
 * user.  Delegated sessions restrict write operations — see auth middleware.
 */
export interface SessionContext {
  actor: User;
  delegatedFor?: User;
}

export interface LoanApplication {
  id: string;
  borrowerName: string;
  amount: number;
  /** US state / jurisdiction — affects business rules (e.g. California). */
  loanState: string;
  status: ApplicationState;
  assignedUnderwriter: string;
  riskScore: number | null;
  createdAt: string;
  updatedAt: string;
}

export interface Decision {
  id: string;
  applicationId: string;
  type: "approved" | "declined" | "conditional";
  rationale: string;
  decidedBy: string;
  decidedAt: string;
  conditions?: string[];
}

export interface NotificationPreference {
  userId: string;
  event: NotificationEvent;
  channel: NotificationChannel;
  enabled: boolean;
  updatedAt: string;
  updatedBy: string;
}

export interface AuditEntry {
  id: string;
  action: string;
  actor: string;
  delegatedFor: string | null;
  timestamp: string;
  previousValue: string | null;
  newValue: string | null;
  source: string;
}
