// ---------------------------------------------------------------------------
// Dashboard Page
// ---------------------------------------------------------------------------
// Shows all loan applications in a table with branded summary stats.
// ---------------------------------------------------------------------------

import { getApplications } from "../api/client.js";
import { renderLoanTable } from "../components/loan-table.js";

export async function renderDashboard(container: HTMLElement): Promise<void> {
  container.innerHTML = `<p class="loading">Loading applications\u2026</p>`;

  try {
    const loans = await getApplications();

    const stats = {
      total: loans.length,
      intake: loans.filter((l) => l.status === "intake").length,
      underwriting: loans.filter((l) => l.status === "underwriting").length,
      finalized: loans.filter((l) => l.status === "finalized").length,
    };

    container.innerHTML = `
      <section class="dashboard">
        <div class="page-header">
          <h2>Loan Applications</h2>
          <p>Overview of all applications and their current status.</p>
        </div>
        <div class="stats-bar">
          <div class="stat">
            <span class="stat-value">${stats.total}</span>
            <span class="stat-label">Total</span>
          </div>
          <div class="stat">
            <span class="stat-value">${stats.intake}</span>
            <span class="stat-label">Intake</span>
          </div>
          <div class="stat">
            <span class="stat-value">${stats.underwriting}</span>
            <span class="stat-label">Underwriting</span>
          </div>
          <div class="stat">
            <span class="stat-value">${stats.finalized}</span>
            <span class="stat-label">Finalized</span>
          </div>
        </div>
        <div id="loan-table-container"></div>
      </section>
    `;

    const tableContainer = container.querySelector<HTMLElement>(
      "#loan-table-container",
    )!;
    renderLoanTable(tableContainer, loans);
  } catch (err) {
    container.innerHTML = `<p class="error">Failed to load applications: ${(err as Error).message}</p>`;
  }
}
