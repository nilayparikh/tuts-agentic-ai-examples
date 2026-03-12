// ---------------------------------------------------------------------------
// Application Detail Page
// ---------------------------------------------------------------------------
// Shows a single loan application with its decisions and transition buttons.
// ---------------------------------------------------------------------------

import {
  getApplication,
  getDecisions,
  transitionApplication,
} from "../api/client.js";
import { renderStatusBadge } from "../components/status-badge.js";

export async function renderApplicationDetail(
  container: HTMLElement,
): Promise<void> {
  const params = new URLSearchParams(window.location.hash.split("?")[1] ?? "");
  const id = params.get("id");

  if (!id) {
    container.innerHTML = `<p class="error">No application ID specified.</p>`;
    return;
  }

  container.innerHTML = `<p class="loading">Loading application...</p>`;

  try {
    const [loan, decisions] = await Promise.all([
      getApplication(id),
      getDecisions(id),
    ]);

    container.innerHTML = `
      <section class="application-detail">
        <h2>${loan.borrowerName}</h2>
        <div class="detail-grid">
          <div class="detail-field"><strong>ID:</strong> ${loan.id}</div>
          <div class="detail-field"><strong>Amount:</strong> $${loan.amount.toLocaleString()}</div>
          <div class="detail-field"><strong>State:</strong> ${loan.loanState}</div>
          <div class="detail-field"><strong>Status:</strong> ${renderStatusBadge(loan.status)}</div>
          <div class="detail-field"><strong>Risk Score:</strong> ${loan.riskScore ?? "—"}</div>
          <div class="detail-field"><strong>Created:</strong> ${new Date(loan.createdAt).toLocaleDateString()}</div>
        </div>

        <h3>Decisions (${decisions.length})</h3>
        ${
          decisions.length === 0
            ? `<p class="empty-state">No decisions recorded.</p>`
            : decisions
                .map(
                  (d) => `
            <div class="decision-card">
              <strong>${d.type}</strong> by ${d.decidedBy} on ${new Date(d.decidedAt).toLocaleDateString()}
              <p>${d.rationale}</p>
            </div>
          `,
                )
                .join("")
        }

        <div id="transition-actions" class="actions"></div>
      </section>
    `;
  } catch (err) {
    container.innerHTML = `<p class="error">Failed to load application: ${(err as Error).message}</p>`;
  }
}
