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

const NEXT_STATES: Record<string, string[]> = {
  intake: ["review"],
  review: ["underwriting", "intake"],
  underwriting: ["decision"],
  decision: ["finalized", "underwriting"],
  finalized: [],
};

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
    const nextStates = NEXT_STATES[loan.status] ?? [];

    container.innerHTML = `
      <section class="application-detail">
        <div class="page-header">
          <h2>${loan.borrowerName}</h2>
          <p>${loan.id} · ${loan.loanState} · Assigned to ${loan.assignedUnderwriter}</p>
        </div>
        <div class="detail-grid">
          <div class="detail-field"><span class="field-label">ID</span><span class="field-value">${loan.id}</span></div>
          <div class="detail-field"><span class="field-label">Amount</span><span class="field-value">$${loan.amount.toLocaleString()}</span></div>
          <div class="detail-field"><span class="field-label">State</span><span class="field-value">${loan.loanState}</span></div>
          <div class="detail-field"><span class="field-label">Status</span><span class="field-value">${renderStatusBadge(loan.status)}</span></div>
          <div class="detail-field"><span class="field-label">Risk Score</span><span class="field-value">${loan.riskScore ?? "—"}</span></div>
          <div class="detail-field"><span class="field-label">Created</span><span class="field-value">${new Date(loan.createdAt).toLocaleDateString()}</span></div>
        </div>

        <div class="actions">
          ${
            nextStates.length === 0
              ? `<p class="subtitle">This application is finalized. No further transitions are available.</p>`
              : nextStates
                  .map(
                    (state) => `<button class="btn btn-primary transition-btn" data-next-state="${state}">Move to ${state}</button>`,
                  )
                  .join("")
          }
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

    container
      .querySelectorAll<HTMLButtonElement>(".transition-btn")
      .forEach((button) => {
        button.addEventListener("click", async () => {
          const nextState = button.dataset.nextState;
          if (!nextState) {
            return;
          }

          button.disabled = true;
          try {
            await transitionApplication(id, nextState);
            await renderApplicationDetail(container);
          } catch (err) {
            button.disabled = false;
            container
              .querySelector(".actions")
              ?.insertAdjacentHTML(
                "beforeend",
                `<p class="error">Failed to transition application: ${(err as Error).message}</p>`,
              );
          }
        });
      });
  } catch (err) {
    container.innerHTML = `<p class="error">Failed to load application: ${(err as Error).message}</p>`;
  }
}
