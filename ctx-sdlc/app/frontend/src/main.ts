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
    const route = hash.split("?")[0];

    switch (route) {
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
      case "queue":
        import("./pages/queue-monitor.js").then((m) =>
          m.renderQueueMonitor(content),
        );
        break;
      case "api":
        import("./pages/api-explorer.js").then((m) =>
          m.renderApiExplorer(content),
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
