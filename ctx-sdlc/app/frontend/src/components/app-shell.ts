// ---------------------------------------------------------------------------
// App Shell Component
// ---------------------------------------------------------------------------
// Renders the application layout: navigation bar, main content area.
// ---------------------------------------------------------------------------

export function renderAppShell(root: HTMLElement): void {
  root.innerHTML = `
    <header class="app-header">
      <h1 class="app-title">Loan Workbench</h1>
      <nav class="app-nav">
        <a href="#dashboard" class="nav-link">Dashboard</a>
        <a href="#preferences" class="nav-link">Preferences</a>
        <a href="#queue" class="nav-link">Queue</a>
        <a href="#api" class="nav-link">API Explorer</a>
      </nav>
      <div class="user-info">
        <select id="user-select" class="user-select">
          <option value="u-1">Dana Chu (Underwriter)</option>
          <option value="u-2">Raj Patel (Analyst Manager)</option>
          <option value="u-3">Kim Nakamura (Compliance)</option>
        </select>
      </div>
    </header>
    <main id="main-content" class="main-content"></main>
  `;

  // User switcher
  const select = root.querySelector<HTMLSelectElement>("#user-select");
  select?.addEventListener("change", async () => {
    const { setCurrentUser } = await import("../api/client.js");
    setCurrentUser(select.value);
    // Re-trigger current page
    window.dispatchEvent(new HashChangeEvent("hashchange"));
  });
}
