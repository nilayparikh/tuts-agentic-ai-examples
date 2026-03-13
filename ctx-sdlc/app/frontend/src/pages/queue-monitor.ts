// ---------------------------------------------------------------------------
// Queue Monitor Page
// ---------------------------------------------------------------------------
// Shows event broker subscriptions, recent event history, and broker health.
// ---------------------------------------------------------------------------

import { apiFetch } from "../api/client.js";

interface QueueSubscription {
  event: string;
  handlerCount: number;
}

interface QueueEvent {
  event: string;
  processedAt: string;
  dataKeys: string[];
}

interface QueueStatus {
  pendingCount: number;
  subscriptions: QueueSubscription[];
  recentEventCount: number;
}

export async function renderQueueMonitor(
  container: HTMLElement,
): Promise<void> {
  container.innerHTML = `<p class="loading">Loading queue status...</p>`;

  try {
    const [status, history] = await Promise.all([
      apiFetch<QueueStatus>("/queue/status"),
      apiFetch<QueueEvent[]>("/queue/history?limit=50"),
    ]);

    container.innerHTML = `
      <section class="queue-monitor">
        <h2>Event Queue Monitor</h2>

        <div class="stats-bar">
          <div class="stat"><span class="stat-value">${status.subscriptions.length}</span> Subscriptions</div>
          <div class="stat"><span class="stat-value">${status.pendingCount}</span> Pending</div>
          <div class="stat"><span class="stat-value">${status.recentEventCount}</span> Recent Events</div>
        </div>

        <h3>Subscriptions</h3>
        <table class="loan-table">
          <thead>
            <tr><th>Event</th><th>Handlers</th></tr>
          </thead>
          <tbody>
            ${status.subscriptions
              .map(
                (s) => `
              <tr>
                <td><code>${s.event}</code></td>
                <td>${s.handlerCount}</td>
              </tr>`,
              )
              .join("")}
          </tbody>
        </table>

        <h3>Recent Events</h3>
        ${
          history.length === 0
            ? `<p class="empty-state">No events recorded yet. Try creating a loan application or changing its status.</p>`
            : `
          <table class="loan-table">
            <thead>
              <tr><th>Event</th><th>Time</th><th>Data Keys</th></tr>
            </thead>
            <tbody>
              ${history
                .map(
                  (e) => `
                <tr>
                  <td><code>${e.event}</code></td>
                  <td class="timestamp">${new Date(e.processedAt).toLocaleTimeString()}</td>
                  <td class="data-keys">${e.dataKeys.join(", ")}</td>
                </tr>`,
                )
                .join("")}
            </tbody>
          </table>`
        }

        <div class="queue-actions">
          <button id="queue-refresh" class="btn btn-primary">Refresh</button>
        </div>
      </section>
    `;

    container
      .querySelector("#queue-refresh")
      ?.addEventListener("click", () => renderQueueMonitor(container));
  } catch (err) {
    container.innerHTML = `<p class="error">Failed to load queue status: ${(err as Error).message}</p>`;
  }
}
