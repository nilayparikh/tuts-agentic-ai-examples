// ---------------------------------------------------------------------------
// Notification Preferences Page
// ---------------------------------------------------------------------------
// Shows notification preferences for the current user and allows toggling.
// ---------------------------------------------------------------------------

import { getPreferences } from "../api/client.js";
import { renderNotificationToggle } from "../components/notification-toggle.js";

export async function renderPreferences(container: HTMLElement): Promise<void> {
  container.innerHTML = `<p class="loading">Loading preferences...</p>`;

  const userSelect = document.querySelector<HTMLSelectElement>("#user-select");
  const userId = userSelect?.value ?? "u-1";

  try {
    const prefs = await getPreferences(userId);

    container.innerHTML = `
      <section class="preferences-page">
        <h2>Notification Preferences</h2>
        <p class="subtitle">Manage how you receive notifications for loan events.</p>
        <div id="pref-list" class="pref-list"></div>
      </section>
    `;

    const prefList = container.querySelector<HTMLElement>("#pref-list")!;

    if (prefs.length === 0) {
      prefList.innerHTML = `<p class="empty-state">No preferences configured. Defaults will be used.</p>`;
      return;
    }

    for (const pref of prefs) {
      renderNotificationToggle(prefList, pref, userId);
    }
  } catch (err) {
    container.innerHTML = `<p class="error">Failed to load preferences: ${(err as Error).message}</p>`;
  }
}
