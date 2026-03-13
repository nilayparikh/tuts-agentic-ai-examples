// ---------------------------------------------------------------------------
// App Shell Component
// ---------------------------------------------------------------------------
// Renders the branded application layout: header with brand lockup,
// navigation bar, main content area, and footer.
// ---------------------------------------------------------------------------

export function renderAppShell(root: HTMLElement): void {
  root.innerHTML = `
    <header class="app-header">
      <a href="#dashboard" class="brand-lockup" aria-label="LocalM Tuts Examples">
        <img src="/brand/icon-mark-gradient.svg" alt="" class="brand-mark" width="35" height="35" />
        <div class="brand-wordmark">
          <span class="brand-primary">localm<span class="brand-tm">™</span></span>
          <span class="brand-tuts">TUTS</span>
        </div>
        <span class="brand-separator">|</span>
        <span class="brand-context">Examples</span>
      </a>
      <nav class="app-nav" id="main-nav">
        <a href="#dashboard" class="nav-link" data-page="dashboard">Dashboard</a>
        <a href="#preferences" class="nav-link" data-page="preferences">Preferences</a>
        <a href="#queue" class="nav-link" data-page="queue">Queue</a>
        <a href="#api" class="nav-link" data-page="api">API Explorer</a>
      </nav>
      <div class="user-info">
        <select id="user-select" class="user-select" aria-label="Switch user">
          <option value="u-1">Dana Chu (Underwriter)</option>
          <option value="u-2">Raj Patel (Analyst Manager)</option>
          <option value="u-3">Kim Nakamura (Compliance)</option>
        </select>
      </div>
    </header>
    <main id="main-content" class="main-content"></main>
    <footer class="app-footer">
      <span>&copy; ${new Date().getFullYear()} LocalM\u2122. All rights reserved.</span>
    </footer>
  `;

  // Active nav tracking
  const updateActiveNav = (): void => {
    const hash = window.location.hash.slice(1) || "dashboard";
    const page = hash.split("?")[0];
    root.querySelectorAll<HTMLAnchorElement>(".nav-link").forEach((link) => {
      link.classList.toggle("active", link.dataset.page === page);
    });
  };
  window.addEventListener("hashchange", updateActiveNav);
  updateActiveNav();

  // User switcher
  const select = root.querySelector<HTMLSelectElement>("#user-select");
  select?.addEventListener("change", async () => {
    const { setCurrentUser } = await import("../api/client.js");
    setCurrentUser(select.value);
    window.dispatchEvent(new HashChangeEvent("hashchange"));
  });
}
