// ---------------------------------------------------------------------------
// Frontend Entry Point
// ---------------------------------------------------------------------------
// Initializes the single-page application, sets up routing, and renders
// the initial page (dashboard).
// ---------------------------------------------------------------------------

import { renderAppShell } from "./components/app-shell.js";
import { renderDashboard } from "./pages/dashboard.js";

function init(): void {
  const root = document.getElementById("app");
  if (!root) return;

  renderAppShell(root);

  // Simple hash-based routing
  const navigate = (): void => {
    const content = document.getElementById("main-content");
    if (!content) return;

    const hash = window.location.hash.slice(1) || "dashboard";

    switch (hash) {
      case "dashboard":
        renderDashboard(content);
        break;
      case "preferences":
        import("./pages/preferences.js").then((m) =>
          m.renderPreferences(content),
        );
        break;
      case "application":
        import("./pages/application-detail.js").then((m) =>
          m.renderApplicationDetail(content),
        );
        break;
      default:
        renderDashboard(content);
    }
  };

  window.addEventListener("hashchange", navigate);
  navigate();
}

document.addEventListener("DOMContentLoaded", init);
