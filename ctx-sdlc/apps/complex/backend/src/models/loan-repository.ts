// ---------------------------------------------------------------------------
// Loan Application Repository
// ---------------------------------------------------------------------------
// Database operations for loan applications.  All SQL lives here — services
// and routes interact with loans only through this module.
//
// IMPORTANT: The `loan_state` column stores the US state/jurisdiction, NOT
// the application lifecycle state.  The lifecycle is in `status`.
// ---------------------------------------------------------------------------

import { v4 as uuid } from "uuid";
import { getDb } from "../db/connection.js";
import type { LoanApplication, ApplicationState } from "./types.js";

export function findAllLoans(): LoanApplication[] {
  const db = getDb();
  return db
    .prepare("SELECT * FROM loan_applications ORDER BY created_at DESC")
    .all() as LoanApplication[];
}

export function findLoanById(id: string): LoanApplication | undefined {
  const db = getDb();
  return db.prepare("SELECT * FROM loan_applications WHERE id = ?").get(id) as
    | LoanApplication
    | undefined;
}

export function findLoansByStatus(status: ApplicationState): LoanApplication[] {
  const db = getDb();
  return db
    .prepare(
      "SELECT * FROM loan_applications WHERE status = ? ORDER BY created_at DESC",
    )
    .all(status) as LoanApplication[];
}

export function findLoansByUnderwriter(
  underwriterId: string,
): LoanApplication[] {
  const db = getDb();
  return db
    .prepare(
      "SELECT * FROM loan_applications WHERE assigned_underwriter = ? ORDER BY created_at DESC",
    )
    .all(underwriterId) as LoanApplication[];
}

export function createLoan(data: {
  borrowerName: string;
  amount: number;
  loanState: string;
  assignedUnderwriter: string;
}): LoanApplication {
  const db = getDb();
  const id = uuid();
  const now = new Date().toISOString();

  db.prepare(
    `INSERT INTO loan_applications (id, borrower_name, amount, loan_state, status, assigned_underwriter, created_at, updated_at)
     VALUES (?, ?, ?, ?, 'intake', ?, ?, ?)`,
  ).run(
    id,
    data.borrowerName,
    data.amount,
    data.loanState.toUpperCase(),
    data.assignedUnderwriter,
    now,
    now,
  );

  return findLoanById(id)!;
}

export function updateLoanStatus(
  id: string,
  status: ApplicationState,
): LoanApplication | undefined {
  const db = getDb();
  const now = new Date().toISOString();

  const result = db
    .prepare(
      "UPDATE loan_applications SET status = ?, updated_at = ? WHERE id = ?",
    )
    .run(status, now, id);

  if (result.changes === 0) return undefined;
  return findLoanById(id);
}

export function updateLoanRiskScore(
  id: string,
  riskScore: number,
): LoanApplication | undefined {
  const db = getDb();
  const now = new Date().toISOString();

  const result = db
    .prepare(
      "UPDATE loan_applications SET risk_score = ?, updated_at = ? WHERE id = ?",
    )
    .run(riskScore, now, id);

  if (result.changes === 0) return undefined;
  return findLoanById(id);
}
