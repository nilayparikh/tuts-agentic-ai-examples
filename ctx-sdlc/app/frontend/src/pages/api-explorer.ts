// ---------------------------------------------------------------------------
// API Explorer Page
// ---------------------------------------------------------------------------
// Interactive interface to test and validate all backend API endpoints.
// Branded with LocalM™ Tuts design tokens.
// ---------------------------------------------------------------------------

const ENDPOINTS = [
  { method: "GET", path: "/api/applications", label: "List Applications", body: false },
  {
    method: "POST",
    path: "/api/applications",
    label: "Create Application",
    body: true,
    template: JSON.stringify(
      { borrowerName: "Jane Doe", amount: 500000, loanState: "CA" },
      null,
      2,
    ),
  },
  { method: "GET", path: "/api/applications/:id", label: "Get Application", body: false, param: "id" },
  {
    method: "PATCH",
    path: "/api/applications/:id/status",
    label: "Transition Status",
    body: true,
    param: "id",
    template: JSON.stringify({ status: "underwriting" }, null, 2),
  },
  { method: "GET", path: "/api/decisions/:applicationId", label: "Get Decisions", body: false, param: "applicationId" },
  {
    method: "POST",
    path: "/api/decisions",
    label: "Create Decision",
    body: true,
    template: JSON.stringify(
      { applicationId: "", outcome: "approved", reason: "Meets all criteria" },
      null,
      2,
    ),
  },
  { method: "GET", path: "/api/notifications/preferences/:userId", label: "Get Preferences", body: false, param: "userId" },
  {
    method: "PUT",
    path: "/api/notifications/preferences",
    label: "Set Preference",
    body: true,
    template: JSON.stringify(
      { userId: "u-1", event: "loan.state-changed", channel: "email", enabled: true },
      null,
      2,
    ),
  },
  { method: "GET", path: "/api/audit", label: "Audit Log", body: false },
  { method: "GET", path: "/api/queue/status", label: "Queue Status", body: false },
  { method: "GET", path: "/api/queue/history?limit=20", label: "Queue History", body: false },
  { method: "GET", path: "/health", label: "Health Check", body: false },
] as const;

type Endpoint = (typeof ENDPOINTS)[number];

function buildUrl(ep: Endpoint, paramValue: string): string {
  let url = ep.path;
  if ("param" in ep && ep.param) {
    url = url.replace(`:${ep.param}`, encodeURIComponent(paramValue));
  }
  return url;
}

export function renderApiExplorer(container: HTMLElement): void {
  container.innerHTML = `
    <section class="api-explorer">
      <div class="page-header">
        <h2>API Explorer</h2>
        <p>Select an endpoint, fill parameters, and send requests to the backend.</p>
      </div>

      <div class="explorer-layout">
        <div class="endpoint-sidebar">
          <div class="endpoint-sidebar-title">Endpoints</div>
          <div class="endpoint-list">
            ${ENDPOINTS.map(
              (ep, i) => `
              <button class="endpoint-btn" data-idx="${i}">
                <span class="method-badge method-${ep.method.toLowerCase()}">${ep.method}</span>
                <span>${ep.label}</span>
              </button>`,
            ).join("")}
          </div>
        </div>

        <div class="request-panel">
          <div id="request-form" class="request-card">
            <p class="text-muted" style="padding: 2rem; text-align: center;">Select an endpoint from the sidebar to get started.</p>
          </div>
          <div id="response-output" class="response-card">
            <div class="response-header">
              <span class="card-title">Response</span>
            </div>
            <pre class="response-pre"><code class="text-muted">// Response will appear here</code></pre>
          </div>
        </div>
      </div>
    </section>
  `;

  container.querySelectorAll<HTMLButtonElement>(".endpoint-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      container.querySelectorAll(".endpoint-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      const idx = Number(btn.dataset.idx);
      renderRequestForm(container, ENDPOINTS[idx]);
    });
  });
}

function renderRequestForm(container: HTMLElement, ep: Endpoint): void {
  const form = container.querySelector<HTMLElement>("#request-form")!;

  const hasParam = "param" in ep && ep.param;
  const hasBody = ep.body;

  form.innerHTML = `
    <h3>
      <span class="method-badge method-${ep.method.toLowerCase()}">${ep.method}</span>
      ${ep.path}
    </h3>
    ${
      hasParam
        ? `<label class="form-label">
            ${ep.param}
            <input type="text" id="param-input" class="form-input" placeholder="Enter ${ep.param}" />
          </label>`
        : ""
    }
    ${
      hasBody && "template" in ep
        ? `<label class="form-label">
            Request Body (JSON)
            <textarea id="body-input" class="form-textarea" rows="6">${ep.template}</textarea>
          </label>`
        : ""
    }
    <button id="send-btn" class="btn btn-primary">Send Request</button>
  `;

  form.querySelector("#send-btn")?.addEventListener("click", () => sendRequest(container, ep));
}

async function sendRequest(container: HTMLElement, ep: Endpoint): Promise<void> {
  const output = container.querySelector<HTMLElement>("#response-output")!;
  output.innerHTML = `
    <div class="response-header"><span class="card-title">Response</span></div>
    <pre class="response-pre"><code class="text-muted">Sending\u2026</code></pre>
  `;

  const paramInput = container.querySelector<HTMLInputElement>("#param-input");
  const bodyInput = container.querySelector<HTMLTextAreaElement>("#body-input");

  const paramValue = paramInput?.value.trim() ?? "";
  if ("param" in ep && ep.param && !paramValue) {
    output.innerHTML = `
      <div class="response-header"><span class="card-title">Response</span></div>
      <pre class="response-pre"><code class="error">Please enter a value for ${ep.param}</code></pre>
    `;
    return;
  }

  const url = buildUrl(ep, paramValue);

  const headers: Record<string, string> = {
    "x-user-id": (document.querySelector<HTMLSelectElement>("#user-select")?.value) ?? "u-1",
  };

  const init: RequestInit = { method: ep.method, headers };
  if (ep.body && bodyInput?.value.trim()) {
    headers["Content-Type"] = "application/json";
    try {
      JSON.parse(bodyInput.value);
    } catch {
      output.innerHTML = `
        <div class="response-header"><span class="card-title">Response</span></div>
        <pre class="response-pre"><code class="error">Invalid JSON in request body</code></pre>
      `;
      return;
    }
    init.body = bodyInput.value;
  }

  const startTime = performance.now();

  try {
    const res = await fetch(url, init);
    const elapsed = Math.round(performance.now() - startTime);
    const body = await res.text();

    let formatted: string;
    try {
      formatted = JSON.stringify(JSON.parse(body), null, 2);
    } catch {
      formatted = body;
    }

    const statusClass = res.ok ? "status-ok" : "status-error";

    output.innerHTML = `
      <div class="response-meta">
        <span class="${statusClass}">${res.status} ${res.statusText}</span>
        <span class="response-time">${elapsed}ms</span>
      </div>
      <pre class="response-pre"><code>${syntaxHighlight(formatted)}</code></pre>
    `;
  } catch (err) {
    output.innerHTML = `
      <div class="response-header"><span class="card-title">Response</span></div>
      <pre class="response-pre"><code class="error">Network error: ${escapeHtml((err as Error).message)}</code></pre>
    `;
  }
}

function escapeHtml(text: string): string {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

function syntaxHighlight(json: string): string {
  const escaped = escapeHtml(json);
  return escaped.replace(
    /("(\\u[\da-fA-F]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false)\b|-?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?|\bnull\b)/g,
    (match) => {
      if (/^"/.test(match)) {
        if (/:$/.test(match)) {
          return `<span class="json-key">${match}</span>`;
        }
        return `<span class="json-string">${match}</span>`;
      }
      if (/true|false/.test(match)) {
        return `<span class="json-boolean">${match}</span>`;
      }
      if (/null/.test(match)) {
        return `<span class="json-null">${match}</span>`;
      }
      return `<span class="json-number">${match}</span>`;
    },
  );
}
