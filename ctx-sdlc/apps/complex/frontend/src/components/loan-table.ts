// ---------------------------------------------------------------------------
// Loan Table Component
// ---------------------------------------------------------------------------
// Renders a sortable table of loan applications.
// ---------------------------------------------------------------------------

import type { ApiLoanApplication } from "../api/types.js";
import { renderStatusBadge } from "./status-badge.js";

export function renderLoanTable(
  container: HTMLElement,
  loans: ApiLoanApplication[],
): void {
  if (loans.length === 0) {
    container.innerHTML = `<p class="empty-state">No loan applications found.</p>`;
    return;
  }

  const rows = loans
    .map(
      (loan) => `
    <tr>
      <td><a href="#application?id=${loan.id}" class="loan-link">${loan.id}</a></td>
      <td>${loan.borrowerName}</td>
      <td class="amount">$${loan.amount.toLocaleString()}</td>
      <td>${loan.loanState}</td>
      <td>${renderStatusBadge(loan.status)}</td>
      <td>${loan.riskScore != null ? loan.riskScore.toFixed(1) : "—"}</td>
      <td>${new Date(loan.createdAt).toLocaleDateString()}</td>
    </tr>`,
    )
    .join("");

  container.innerHTML = `
    <table class="loan-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Borrower</th>
          <th>Amount</th>
          <th>State</th>
          <th>Status</th>
          <th>Risk Score</th>
          <th>Created</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
  `;
}
