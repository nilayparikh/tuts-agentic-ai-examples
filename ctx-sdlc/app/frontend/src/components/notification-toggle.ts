// ---------------------------------------------------------------------------
// Notification Toggle Component
// ---------------------------------------------------------------------------
// Renders a toggle switch for a notification preference.
// ---------------------------------------------------------------------------

import type { ApiPreference } from "../api/types.js";
import { setPreference } from "../api/client.js";

export function renderNotificationToggle(
  container: HTMLElement,
  pref: ApiPreference,
  userId: string,
): void {
  const id = `toggle-${pref.event}-${pref.channel}`;
  const checked = pref.enabled ? "checked" : "";

  const wrapper = document.createElement("div");
  wrapper.className = "notification-toggle";
  wrapper.innerHTML = `
    <label for="${id}" class="toggle-label">
      <span class="toggle-event">${pref.event}</span>
      <span class="toggle-channel">${pref.channel}</span>
    </label>
    <input type="checkbox" id="${id}" class="toggle-input" ${checked} />
  `;

  const input = wrapper.querySelector<HTMLInputElement>("input")!;
  input.addEventListener("change", async () => {
    try {
      await setPreference({
        userId,
        event: pref.event,
        channel: pref.channel,
        enabled: input.checked,
      });
    } catch (err) {
      // Revert on failure
      input.checked = !input.checked;
      console.error("Failed to update preference:", err);
    }
  });

  container.appendChild(wrapper);
}
