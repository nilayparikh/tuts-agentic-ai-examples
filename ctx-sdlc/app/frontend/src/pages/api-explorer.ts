// ---------------------------------------------------------------------------
// API Explorer Page
// ---------------------------------------------------------------------------
// Interactive interface to test and validate all backend API endpoints.
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
      <h2>API Explorer</h2>
      <p class="text-muted">Select an endpoint, fill parameters, and send requests to the backend.</p>

      <div class="explorer-layout">
        <div class="endpoint-list">
          <h3>Endpoints</h3>
          ${ENDPOINTS.map(
            (ep, i) => `
            <button class="endpoint-btn" data-idx="${i}">
              <span class="method-badge method-${ep.method.toLowerCase()}">${ep.method}</span>
              ${ep.label}
            </button>`,
          ).join("")}
        </div>

        <div class="request-panel">
          <div id="request-form" class="request-form">
            <p class="text-muted">Select an endpoint from the list.</p>
          </div>
          <div id="response-output" class="response-output">
            <pre class="response-pre"><code>// Response will appear here</code></pre>
          </div>
        </div>
      </div>
    </section>
  `;

  // Event delegation for endpoint buttons
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
    <h3>${ep.method} ${ep.path}</h3>
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
  output.innerHTML = `<pre class="response-pre"><code>Sending...</code></pre>`;

  const paramInput = container.querySelector<HTMLInputElement>("#param-input");
  const bodyInput = container.querySelector<HTMLTextAreaElement>("#body-input");

  const paramValue = paramInput?.value.trim() ?? "";
  if ("param" in ep && ep.param && !paramValue) {
    output.innerHTML = `<pre class="response-pre error"><code>Please enter a value for ${ep.param}</code></pre>`;
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
      output.innerHTML = `<pre class="response-pre error"><code>Invalid JSON in request body</code></pre>`;
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
      <pre class="response-pre"><code>${escapeHtml(formatted)}</code></pre>
    `;
  } catch (err) {
    output.innerHTML = `<pre class="response-pre error"><code>Network error: ${(err as Error).message}</code></pre>`;
  }
}

function escapeHtml(text: string): string {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}
