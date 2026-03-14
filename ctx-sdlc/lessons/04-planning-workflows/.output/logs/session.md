# 🤖 Copilot CLI Session

> [!NOTE]
> - **Session ID:** `cd551e9d-6f2a-4c2f-8cac-4ad81ea916f4`  
> - **Started:** 14/03/2026, 01:47:47  
> - **Duration:** 3m 40s  
> - **Exported:** 14/03/2026, 01:51:28  

---

<sub>⏱️ 5s</sub>

### 👤 User

Inspect the relevant docs/, specs/, and existing source surfaces for notification preferences in this lesson before answering. Discover the architecture, ADR, product, and NFR context you need rather than assuming a fixed file list. Produce a structured implementation plan and save it to docs/notification-preferences-plan.md. The plan must include: summary, source-backed confirmed requirements with references to FR/SC/ADR/NFR identifiers, open questions with file references, inferred implementation choices separated from confirmed requirements, constraints and special conditions, numbered tasks with acceptance criteria and source references, validation steps, and risks/dependencies. Explicitly call out delegated sessions, LEGAL-218, mandatory-event delivery, fail-closed audit behavior, degraded-mode fallback, at least one false positive, and at least one hard negative. If the sources overlap or conflict, identify the canonical source for the plan and explain why. Do not run shell commands and do not use SQL.

---

<sub>⏱️ 14s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows**

"docs\**\*.md" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows

```
No files matched the pattern.
```


---

<sub>⏱️ 14s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows**

"specs\**\*.md" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows

```
No files matched the pattern.
```


---

<sub>⏱️ 14s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "notification|delegated|LEGAL-218|mandatory|audit|degraded",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\04-planning-workflows\\docs",
  "output_mode": "content",
  "glob": "*.md",
  "-n": true,
  "head_limit": 200
}
```

</details>

<details>
<summary>16 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\planning-workflow-example.md:7:Show that a planning workflow can turn a visible feature request into a grounded, written implementation plan. The CLI writes the plan to `docs/notification-preferences-plan.md` so the output is assessable as a code change.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\planning-workflow-example.md:11:The demo must produce a new file `docs/notification-preferences-plan.md` containing:
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\planning-workflow-example.md:31:1. The plan must be written to `docs/notification-preferences-plan.md` as a real file change.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\planning-workflow-example.md:34:4. The plan must explicitly call out delegated-session behavior, LEGAL-218, mandatory-event delivery, fail-closed audit semantics, and degraded-mode fallback.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\planning-workflow-example.md:43:Use the notification preferences feature request and supporting docs to produce a plan that is deeper than "add a settings page and API route".
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\planning-workflow-example.md:47:- delegated sessions
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\planning-workflow-example.md:50:- audit fail-closed semantics
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\planning-workflow-example.md:58:- identify affected route, rule, service, UI, state, and audit surfaces
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\architecture.md:17:      middleware/           ← Auth, audit logger, error handler, rate limiter
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\architecture.md:21:        handlers/           ← Notification + audit event consumers
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\architecture.md:42:2. Underwriting decisions require API support and audit coverage.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\architecture.md:45:5. Product rules may vary by role, loan jurisdiction, and delegated-session mode.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\architecture.md:46:6. Audit is mandatory for all writes — via queue broker or direct DB write.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\architecture.md:57:- identify the frontend, route, rule, service, audit, and observability surfaces that would likely change
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\adr\ADR-003-frontend-state.md:10:application lists, decision forms, notification settings, and audit viewers.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\adr\ADR-003-frontend-state.md:35:An AI assistant generating a notification-preferences UI will default to
```

</details>


---

<sub>⏱️ 14s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "notification|delegated|LEGAL-218|mandatory|audit|degraded",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\04-planning-workflows\\specs",
  "output_mode": "content",
  "glob": "*.md",
  "-n": true,
  "head_limit": 300
}
```

</details>

<details>
<summary>55 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:15:notifications. The current Loan Workbench sends a fixed set of email alerts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:17:requests and missed high-severity escalation events when all notifications are
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:22:Allow authorized users to configure notification preferences by channel and
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:23:event type without breaking auditability, workflow SLAs, or regulatory
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:30:- Settings UI for notification preferences in `apps/web/`
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:40:- Push notifications
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:41:- Per-loan notification overrides
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:50:- Can edit their own notification preferences
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:51:- **Cannot suppress mandatory manual-review-escalation notifications**
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:55:- Can edit their own notification preferences
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:56:- Receives additional portfolio-level digest notifications (later release)
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:57:- Can operate in **delegated mode** on behalf of another user
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:61:- **Read-only** access to effective preference configuration for audit review
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:83:Manual-review escalation is a **mandatory notification**. Users may change the
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:108:the legal review tracked in `LEGAL-218` is complete.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:151:affect notifications already queued** for that application.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:155:If an analyst manager is operating in delegated mode:
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:157:- They may **view** the delegate's notification preferences.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:159:- The UI must visually indicate delegated-session mode.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:160:- Audit entries must record both the actor and the delegated-for user.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:162:> **HARD NEGATIVE pattern:** A delegated save that shows a "success" toast but
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:185:- Zero Sev2 incidents caused by suppressed mandatory escalation alerts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:189:1. Should compliance reviewers access audit history from the same settings page
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:190:   or a separate audit viewer?
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\feature-request.md:3:Add notification preferences to the Loan Workbench settings area.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\feature-request.md:7:- Underwriters can control email and SMS notifications per event type.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\feature-request.md:11:- The plan must account for delegated sessions, audit logging, and state-based restrictions.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\feature-request.md:15:- Full product specification: `specs/product-spec-notification-preferences.md`
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\feature-request.md:21:- **California loans** cannot enable SMS for decline decisions (LEGAL-218).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\feature-request.md:23:- **SMS degraded mode**: email fallback must preserve the stored preference model.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\feature-request.md:25:- **Audit writes** must fail closed — no silent saves without an audit trail.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\feature-request.md:30:- Current settings screens do not expose notification preferences.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:3:These NFRs constrain the notification preferences feature. Each requirement
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:23:- Preference reads must tolerate notification-provider degradation (the provider
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:25:- **If audit logging is unavailable, writes must FAIL CLOSED** rather than
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:26:  silently saving preferences without an audit trail.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:29:> will generate `try { auditLog(...) } catch { /* ignore */ }` unless the NFR
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:33:> **FALSE POSITIVE:** Preference reads succeeding during an audit-service
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:34:> outage is NOT a bug — only writes require audit availability.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:43:- Delegated sessions must be explicitly identified in audit logs.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:53:- Disabled mandatory-event controls must have **persistent explanatory text**,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:71:| `audit.write.failure`       | Counter   | Tracks fail-closed rejections                 |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:72:| `notification.sms.fallback` | Counter   | SMS→email fallback invocations                |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:110:> job to audit records without checking the retention policy.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:6:delegated sessions; save succeeds visually but reverts on refresh.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:10:An analyst manager opened notification settings while acting on behalf of an
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:11:underwriter (`x-delegated-for: u-1`) for a California loan (`app-100`). They
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:14:1. The SMS toggle for decline notifications was **enabled and editable** even
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:15:   though California loans restrict decline SMS (LEGAL-218).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:43:| Business rule | CA decline SMS is restricted                              | FR-4 / LEGAL-218 |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:45:| Audit         | If audit write failed, the save should have been rejected | NFR-2            |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:60:- Compare UI behavior against `specs/product-spec-notification-preferences.md` sections SC-2 and FR-4.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:61:- Check `src/backend/src/routes/notifications.ts` for the `blockDelegatedWrites` middleware attachment.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:63:- Verify that the audit service was healthy at the time of the report.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:64:- Check `src/backend/src/middleware/auth.ts` for delegated-session detection logic.
```

</details>


---

<sub>⏱️ 14s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "notification|delegated|LEGAL-218|mandatory|audit|degraded",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\04-planning-workflows\\src",
  "output_mode": "content",
  "glob": "*.{ts,tsx,js,json,md}",
  "-n": true,
  "head_limit": 300
}
```

</details>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\integration\decisions.test.ts:12:  it("placeholder — delegated sessions cannot record decisions", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\unit\notification-service.test.ts:7:// These tests verify the notification routing logic at the service level.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\unit\notification-service.test.ts:11:  it("placeholder — notification service emits queue events", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\unit\notification-service.test.ts:12:    // Integration tests for notification delivery live in the queue handler tests.
```


---

<sub>⏱️ 22s</sub>

### 💬 Copilot

I’ve found the core spec references and now I’m mapping them to the actual route, rule, auth, audit, and UI surfaces so the plan is grounded in both docs and code.

---

<sub>⏱️ 22s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs

```
adr
architecture.md
planning-workflow-example.md
```


---

<sub>⏱️ 22s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs

```
bug-report.md
feature-request.md
non-functional-requirements.md
product-spec-notification-preferences.md
```


---

<sub>⏱️ 22s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src

<details>
<summary>6 lines</summary>

```
.env.example
backend
frontend
package-lock.json
package.json
tsconfig.json
```

</details>


---

<sub>⏱️ 22s</sub>

### ❌ `view`

**view the file at C:\Users\nilay\.copilot\session-state\cd551e9d-6f2a-4c2f-8cac-4ad81ea916f4\plan.md.**

C:\Users\nilay\.copilot\session-state\cd551e9d-6f2a-4c2f-8cac-4ad81ea916f4\plan.md

```
Path does not exist
```


---

<sub>⏱️ 28s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\adr.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\adr

```
ADR-003-frontend-state.md
```


---

<sub>⏱️ 28s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "notifications?\\.ts|notification|preferences|delegated|audit|LEGAL-218|mandatory|fallback",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\04-planning-workflows\\src\\backend\\src",
  "output_mode": "files_with_matches",
  "glob": "*.ts",
  "head_limit": 200
}
```

</details>

<details>
<summary>21 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\notification-service.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\loan-service.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\decision-service.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\audit-service.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\role-permissions.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\mandatory-events.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\app.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\audit-logger.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\auth.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\applications.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\models\types.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\models\preference-repository.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\audit.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\broker.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\config\feature-flags.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\notifications.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers\audit-handler.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\contracts.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\db\seed.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\models\audit-repository.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers\notification-handler.ts
```

</details>


---

<sub>⏱️ 28s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "notification|preferences|delegated|audit|LEGAL-218|mandatory|fallback",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\04-planning-workflows\\src\\frontend\\src",
  "output_mode": "files_with_matches",
  "glob": "*.ts",
  "head_limit": 200
}
```

</details>

<details>
<summary>7 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\main.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\pages\api-explorer.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\api\types.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\api\client.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\pages\preferences.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\components\notification-toggle.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\components\app-shell.ts
```

</details>


---

<sub>⏱️ 28s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\architecture.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\architecture.md (lines 1-220)

<details>
<summary>69 lines</summary>

````
1. # Loan Workbench Architecture
2. 
3. ## Product Scope
4. 
5. Loan Workbench supports intake, underwriting review, document collection, and
6. final decision workflows for commercial loan applications.
7. 
8. ## System Shape
9. 
10. ```
11. src/
12.   backend/
13.     src/
14.       app.ts                ← Express entry point, middleware chain
15.       config/               ← Environment config, feature flags
16.       db/                   ← SQLite connection, schema, seed, migrations
17.       middleware/           ← Auth, audit logger, error handler, rate limiter
18.       queue/                ← In-process event broker + handlers
19.         contracts.ts        ← Typed message contracts (breaking-change surface)
20.         broker.ts           ← Pub/sub: on(), emit(), flush()
21.         handlers/           ← Notification + audit event consumers
22.       models/               ← Domain types + DB repository classes
23.       routes/               ← HTTP route handlers
24.       rules/                ← State machine, business rules, role permissions
25.       services/             ← Business logic orchestration
26.     tests/
27.   frontend/
28.     src/
29.       api/                  ← Typed HTTP client matching backend routes
30.       pages/                ← Dashboard, application detail, preferences
31.       components/           ← UI building blocks
32.     styles/
33. ```
34. 
35. - `docs/` stores architecture documentation.
36. - `docs/adr/` stores design decisions that guide planning.
37. - `specs/` stores product specs and NFRs that constrain implementation.
38. 
39. ## Key Architectural Rules
40. 
41. 1. Backend API and frontend SPA communicate via typed HTTP client.
42. 2. Underwriting decisions require API support and audit coverage.
43. 3. Features affecting workflow states must specify migration and validation steps.
44. 4. Pilot-gated features must call out rollout, observability, and fallback behavior.
45. 5. Product rules may vary by role, loan jurisdiction, and delegated-session mode.
46. 6. Audit is mandatory for all writes — via queue broker or direct DB write.
47. 7. Message contracts in `src/backend/src/queue/contracts.ts` are a breaking-change surface.
48. 
49. ## Lesson 04 Planning Target
50. 
51. The lesson demo is intentionally read-only.
52. 
53. The preferred planning output should:
54. 
55. - read the architecture, ADR, product spec, and NFRs together
56. - separate confirmed requirements from inferred implementation choices
57. - identify the frontend, route, rule, service, audit, and observability surfaces that would likely change
58. - stop short of editing code
59. 
60. ## State Machine
61. 
62. Loan applications follow a strict lifecycle:
63. 
64. ```
65. submitted → under_review → approved → funded
66.                          → denied   → closed
67. ```
68. 
69. `funded` and `closed` are terminal — no transitions are allowed after them.
````

</details>


---

<sub>⏱️ 28s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\planning-workflow-example.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\planning-workflow-example.md (lines 1-160)

<details>
<summary>60 lines</summary>

```
1. # Lesson 04 — Planning Workflow Example
2. 
3. This document defines the concrete example used in Lesson 04.
4. 
5. ## Objective
6. 
7. Show that a planning workflow can turn a visible feature request into a grounded, written implementation plan. The CLI writes the plan to `docs/notification-preferences-plan.md` so the output is assessable as a code change.
8. 
9. ## Expected Output Shape
10. 
11. The demo must produce a new file `docs/notification-preferences-plan.md` containing:
12. 
13. 1. Summary
14. 2. Source-backed confirmed requirements with FR/SC/ADR/NFR references
15. 3. Open questions with file references
16. 4. Inferred implementation choices separated from confirmed requirements
17. 5. Constraints and special conditions
18. 6. Numbered tasks with acceptance criteria and source references
19. 7. Validation steps
20. 8. Risks and dependencies
21. 
22. ## Expected Change Artifacts
23. 
24. Assessment compares the actual `demo.patch` and `changed-files.json` against:
25. 
26. - `.output/change/expected-files.json` — expected added/modified/deleted files
27. - `.output/change/expected-patterns.json` — regex patterns that must appear in the patch
28. 
29. ## Required Constraints
30. 
31. 1. The plan must be written to `docs/notification-preferences-plan.md` as a real file change.
32. 2. The plan must cite product spec, NFR, ADR, or special-condition references where relevant.
33. 3. The plan must separate confirmed requirements from inferred implementation choices.
34. 4. The plan must explicitly call out delegated-session behavior, LEGAL-218, mandatory-event delivery, fail-closed audit semantics, and degraded-mode fallback.
35. 5. The plan must identify both backend and frontend impact surfaces.
36. 6. The plan must surface at least one false positive and one hard negative pattern from the provided specs.
37. 7. Do not run shell commands during the assessment run.
38. 8. If lesson artifacts overlap or conflict, the plan must identify the canonical source and explain why.
39. 9. Do not use SQL during the assessment run.
40. 
41. ## Concrete Scenario
42. 
43. Use the notification preferences feature request and supporting docs to produce a plan that is deeper than "add a settings page and API route".
44. 
45. Good output should identify hidden complexity around:
46. 
47. - delegated sessions
48. - California decline SMS restrictions
49. - optimistic UI rollback behavior
50. - audit fail-closed semantics
51. - release-flag rollout and observability
52. 
53. ## What Good Output Looks Like
54. 
55. Good output will usually:
56. 
57. - cite FR-2, FR-4, FR-5, FR-6, SC-2, ADR-003, and relevant NFRs
58. - identify affected route, rule, service, UI, state, and audit surfaces
59. - list validation steps that cover false-positive and hard-negative cases
60. - produce a written plan file that the comparison tooling can verify against expected patterns
```

</details>


---

<sub>⏱️ 33s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Add File: C:\\Users\\nilay\\.copilot\\session-state\\cd551e9d-6f2a-4c2f-8cac-4ad81ea916f4\\plan.md\n+1. Read architecture, ADR, product, NFR, feature request, bug report, and relevant source surfaces for notification preferences.\n+2. Synthesize confirmed requirements, conflicts, open questions, inferred choices, tasks, validation, and risks.\n+3. Write the implementation plan to docs/notification-preferences-plan.md.\n*** End Patch\n"
```

</details>

```
Added 1 file(s): C:\Users\nilay\.copilot\session-state\cd551e9d-6f2a-4c2f-8cac-4ad81ea916f4\plan.md
```


---

<sub>⏱️ 39s</sub>

### 💬 Copilot

I’ve got the map of relevant files now. Next I’m reading the spec/ADR text alongside the current backend and frontend notification code so the plan can separate what’s truly required from what’s just a sensible implementation choice.

---

<sub>⏱️ 39s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md (lines 1-260)

<details>
<summary>193 lines</summary>

```
1. # Product Specification: Notification Preferences
2. 
3. ## Document Status
4. 
5. | Field    | Value                             |
6. | -------- | --------------------------------- |
7. | Owner    | Lending Platform Product          |
8. | Status   | Draft for implementation planning |
9. | Target   | 2026 Q2 pilot                     |
10. | Tracking | PROJ-412                          |
11. 
12. ## Problem Statement
13. 
14. Underwriters and analyst managers need finer control over operational
15. notifications. The current Loan Workbench sends a fixed set of email alerts
16. with no user-level preferences. Teams report alert fatigue for routine document
17. requests and missed high-severity escalation events when all notifications are
18. treated the same.
19. 
20. ## Goal
21. 
22. Allow authorized users to configure notification preferences by channel and
23. event type without breaking auditability, workflow SLAs, or regulatory
24. communications that must always be delivered.
25. 
26. ---
27. 
28. ## In Scope
29. 
30. - Settings UI for notification preferences in `apps/web/`
31. - API support in `services/api/` for reading and updating preferences
32. - Persistence across sessions and devices
33. - Role-aware defaults for underwriters and analyst managers
34. - Event-specific preferences for: approval, decline, document-request,
35.   manual-review-escalation
36. 
37. ## Out of Scope
38. 
39. - SMS provider migration
40. - Push notifications
41. - Per-loan notification overrides
42. - Customer-facing borrower communications
43. 
44. ---
45. 
46. ## User Roles
47. 
48. ### Underwriter
49. 
50. - Can edit their own notification preferences
51. - **Cannot suppress mandatory manual-review-escalation notifications**
52. 
53. ### Analyst Manager
54. 
55. - Can edit their own notification preferences
56. - Receives additional portfolio-level digest notifications (later release)
57. - Can operate in **delegated mode** on behalf of another user
58. 
59. ### Compliance Reviewer
60. 
61. - **Read-only** access to effective preference configuration for audit review
62. - Cannot change operational preferences from the UI
63. 
64. ---
65. 
66. ## Functional Requirements
67. 
68. ### FR-1: Preference Matrix
69. 
70. Users can configure email and SMS independently for these event types:
71. 
72. | Event                    | Email        | SMS            |
73. | ------------------------ | ------------ | -------------- |
74. | Approval decision issued | configurable | configurable   |
75. | Decline decision issued  | configurable | configurable\* |
76. | Document request created | configurable | configurable   |
77. | Manual-review escalation | configurable | configurable   |
78. 
79. \*Subject to state-specific restrictions — see FR-4.
80. 
81. ### FR-2: Mandatory Event Rules
82. 
83. Manual-review escalation is a **mandatory notification**. Users may change the
84. secondary channel, but **at least one channel must remain enabled**.
85. 
86. > **HARD NEGATIVE pattern:** Without this rule, an AI generating the preference
87. > update handler will produce code that allows disabling all channels. The UI
88. > and API must both enforce this constraint.
89. 
90. > **FALSE POSITIVE pattern:** A user disabling SMS for escalation while email
91. > remains enabled is NOT a violation. The constraint is about having zero
92. > channels, not about which specific channel is active.
93. 
94. ### FR-3: Role-Based Defaults
95. 
96. | Role                | Email default                            | SMS default     |
97. | ------------------- | ---------------------------------------- | --------------- |
98. | Underwriter         | All events enabled                       | Escalation only |
99. | Analyst Manager     | All events enabled                       | Escalation only |
100. | Compliance Reviewer | No operational defaults (read-only role) | N/A             |
101. 
102. New users without saved preferences must receive these defaults on first access
103. **without requiring a data backfill migration**.
104. 
105. ### FR-4: Temporary SMS Restriction — California
106. 
107. SMS for decline decisions must remain **disabled for California loans** until
108. the legal review tracked in `LEGAL-218` is complete.
109. 
110. - The UI must explain why the option is unavailable when the active loan context
111.   is California.
112. - The restriction is based on loan jurisdiction (`loanState`), not borrower
113.   address, when the two differ.
114. - From a **multi-state portfolio view**, state-specific restrictions should be
115.   shown as conditional rules rather than blanket-disabling all SMS controls.
116. 
117. > **HARD NEGATIVE pattern:** Enabling decline SMS on a CA loan looks like normal
118. > toggle behavior in code. The restriction is invisible without this spec.
119. 
120. ### FR-5: Degraded Delivery Fallback
121. 
122. If the SMS provider is unavailable:
123. 
124. 1. Delivery falls back to email when email is enabled for that event.
125. 2. **Stored preferences must NOT be modified by the fallback.**
126. 3. Fallback invocations must be logged with a separate metric.
127. 
128. > **FALSE POSITIVE pattern:** A user receiving an email instead of SMS during
129. > an outage is NOT a preference bug. Support agents must check delivery logs,
130. > not the preference store, to diagnose delivery complaints.
131. 
132. ### FR-6: Auditability
133. 
134. Every preference change must record:
135. 
136. - Actor identity
137. - Timestamp
138. - Previous value
139. - New value
140. - Source channel
141. - Delegated-for user (if applicable)
142. 
143. ---
144. 
145. ## Special Conditions
146. 
147. ### SC-1: Locked (Finalized) Applications
148. 
149. When a loan application is in `finalized` state, users can still update their
150. preferences globally, but the settings screen must clarify that changes **do not
151. affect notifications already queued** for that application.
152. 
153. ### SC-2: Delegated Sessions
154. 
155. If an analyst manager is operating in delegated mode:
156. 
157. - They may **view** the delegate's notification preferences.
158. - They may **not modify** the delegate's preferences.
159. - The UI must visually indicate delegated-session mode.
160. - Audit entries must record both the actor and the delegated-for user.
161. 
162. > **HARD NEGATIVE pattern:** A delegated save that shows a "success" toast but
163. > reverts on refresh indicates the UI is optimistically updating local state
164. > without checking the server rejection. This is a real bug already reported.
165. 
166. ### SC-3: Mixed Portfolio Context
167. 
168. When the settings screen is opened from a portfolio view containing loans
169. across multiple states, state-specific restrictions should be explained as
170. conditional rules rather than blanket-disabling controls.
171. 
172. ---
173. 
174. ## UX Notes
175. 
176. - Show channel controls in a matrix grid by event type.
177. - Mandatory events should be **visually marked** and explained inline.
178. - Disabled controls must include persistent helper text, not just tooltips.
179. - Saving should be optimistic **only if rollback is supported by the store**.
180. 
181. ## Success Metrics
182. 
183. - 30% reduction in document-request alert-mute requests within 60 days
184. - < 1% failed preference saves during pilot
185. - Zero Sev2 incidents caused by suppressed mandatory escalation alerts
186. 
187. ## Open Questions
188. 
189. 1. Should compliance reviewers access audit history from the same settings page
190.    or a separate audit viewer?
191. 2. Is the California decline SMS restriction loan-state based or borrower-state
192.    based when they differ? **Answer: loan-state** (per legal review 2026-02).
193. 3. Should portfolio-view restrictions show a summary banner or per-row indicators?
```

</details>


---

<sub>⏱️ 39s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md (lines 1-220)

<details>
<summary>110 lines</summary>

```
1. # Non-Functional Requirements
2. 
3. These NFRs constrain the notification preferences feature. Each requirement
4. is annotated with the kind of mistake an AI assistant is likely to make
5. when the NFR is missing from context.
6. 
7. ---
8. 
9. ## NFR-1: Performance
10. 
11. - Settings page initial load must add ≤ 150 ms p95 over the existing settings
12.   route baseline.
13. - Preference save API must complete within 400 ms p95 under normal load.
14. 
15. > **AI mistake without context:** An assistant might generate a preference save
16. > that does multiple sequential DB writes and a synchronous email-validation
17. > round-trip, exceeding the latency budget.
18. 
19. ---
20. 
21. ## NFR-2: Availability and Resilience
22. 
23. - Preference reads must tolerate notification-provider degradation (the provider
24.   is not the source of truth for preferences).
25. - **If audit logging is unavailable, writes must FAIL CLOSED** rather than
26.   silently saving preferences without an audit trail.
27. 
28. > **HARD NEGATIVE:** Most services treat logging as fire-and-forget. An AI
29. > will generate `try { auditLog(...) } catch { /* ignore */ }` unless the NFR
30. > explicitly overrides that pattern. The correct behavior is to abort the
31. > enclosing save operation.
32. 
33. > **FALSE POSITIVE:** Preference reads succeeding during an audit-service
34. > outage is NOT a bug — only writes require audit availability.
35. 
36. ---
37. 
38. ## NFR-3: Security and Privacy
39. 
40. - Only authenticated internal users can access the preferences endpoint.
41. - SMS destination values (phone numbers) are **sensitive operational data** and
42.   must not appear in client logs or analytics events.
43. - Delegated sessions must be explicitly identified in audit logs.
44. 
45. > **AI mistake without context:** An assistant might log the full preference
46. > object (including phone number metadata) in a debug statement.
47. 
48. ---
49. 
50. ## NFR-4: Accessibility
51. 
52. - Preference controls must be keyboard-reachable and screen-reader labeled.
53. - Disabled mandatory-event controls must have **persistent explanatory text**,
54.   not just a tooltip that disappears.
55. - Status messages for save success and failure must be announced via ARIA live
56.   regions.
57. 
58. > **AI mistake without context:** An assistant will generate a disabled toggle
59. > with a title attribute (tooltip) instead of visible helper text.
60. 
61. ---
62. 
63. ## NFR-5: Observability
64. 
65. Emit metrics for:
66. 
67. | Metric                      | Type      | Purpose                                       |
68. | --------------------------- | --------- | --------------------------------------------- |
69. | `preference.read.failure`   | Counter   | Store read errors                             |
70. | `preference.save.failure`   | Counter   | Distinguishes validation from provider errors |
71. | `audit.write.failure`       | Counter   | Tracks fail-closed rejections                 |
72. | `notification.sms.fallback` | Counter   | SMS→email fallback invocations                |
73. | `preference.save.latency`   | Histogram | p50/p95/p99 save duration                     |
74. 
75. Logs must distinguish **validation failures** (4xx, user error) from
76. **downstream provider failures** (5xx, infrastructure) so alerting routes
77. correctly.
78. 
79. > **AI mistake without context:** An assistant might use a single generic
80. > error counter, making it impossible to filter signal from noise in dashboards.
81. 
82. ---
83. 
84. ## NFR-6: Change Safety
85. 
86. - Feature must ship behind a **release flag** for the initial pilot cohort.
87. - Non-pilot users must see no change — feature-flagged endpoints should return
88.   404 (not 403) to avoid leaking feature existence.
89. - Existing users without saved preferences must receive role-based defaults
90.   without requiring a data backfill before first load.
91. 
92. > **HARD NEGATIVE:** An assistant generating the feature-flag guard might use
93. > 403 Forbidden, which tells non-pilot users the feature exists but they lack
94. > access. The spec requires 404 to completely hide the feature.
95. 
96. > **FALSE POSITIVE:** A pilot user getting role-based defaults on first access
97. > (even though no migration ran) is correct behavior, not a data-integrity bug.
98. 
99. ---
100. 
101. ## NFR-7: Compliance
102. 
103. - Audit records for preference changes must be **retained for 24 months**.
104. - Mandatory escalation delivery rules must be testable and documented in the
105.   release checklist.
106. - The compliance reviewer's read-only view must show the effective preference
107.   state including applied defaults.
108. 
109. > **AI mistake without context:** An assistant might apply a TTL or cleanup
110. > job to audit records without checking the retention policy.
```

</details>


---

<sub>⏱️ 39s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\feature-request.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\feature-request.md (lines 1-200)

<details>
<summary>40 lines</summary>

```
1. # Feature Request: Notification Preferences
2. 
3. Add notification preferences to the Loan Workbench settings area.
4. 
5. ## Requested Behavior
6. 
7. - Underwriters can control email and SMS notifications per event type.
8. - Preferences persist across sessions and devices.
9. - Separate toggles for: approval, decline, document-request, and manual-review-escalation.
10. - Manual-review escalation requires at least one enabled channel.
11. - The plan must account for delegated sessions, audit logging, and state-based restrictions.
12. 
13. ## Product Context
14. 
15. - Full product specification: `specs/product-spec-notification-preferences.md`
16. - Non-functional requirements: `specs/non-functional-requirements.md`
17. - The release is **pilot-gated** and must not change behavior for non-pilot users.
18. 
19. ## Special Conditions To Account For
20. 
21. - **California loans** cannot enable SMS for decline decisions (LEGAL-218).
22. - **Delegated sessions**: analyst managers may inspect but not edit another user's preferences.
23. - **SMS degraded mode**: email fallback must preserve the stored preference model.
24. - **Mandatory escalation events** must remain deliverable even when users change preferences.
25. - **Audit writes** must fail closed — no silent saves without an audit trail.
26. - **Existing users** may not have stored preferences and need role-based defaults on first access.
27. 
28. ## Known Constraints
29. 
30. - Current settings screens do not expose notification preferences.
31. - Shared workflow state follows [ADR-003](docs/adr/ADR-003-frontend-state.md).
32. - Backend routes live under `src/backend/src/routes/`.
33. - Business rules live under `src/backend/src/rules/`.
34. - The team wants a **plan before implementation begins**.
35. 
36. ## Deliverable Expectation
37. 
38. The plan should identify open questions, affected surfaces, validation steps,
39. and risks that come specifically from the product spec and NFRs — not just from
40. the visible UI request. A shallow "add a toggle page" plan is insufficient.
```

</details>


---

<sub>⏱️ 39s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md (lines 1-220)

<details>
<summary>64 lines</summary>

```
1. # Bug Report: Delegated Session + California SMS Toggle
2. 
3. ## Title
4. 
5. Manual-review escalation SMS toggle appears enabled for California loans in
6. delegated sessions; save succeeds visually but reverts on refresh.
7. 
8. ## Reported Behavior
9. 
10. An analyst manager opened notification settings while acting on behalf of an
11. underwriter (`x-delegated-for: u-1`) for a California loan (`app-100`). They
12. observed:
13. 
14. 1. The SMS toggle for decline notifications was **enabled and editable** even
15.    though California loans restrict decline SMS (LEGAL-218).
16. 2. They were able to click the SMS toggle and press Save.
17. 3. A success toast appeared.
18. 4. On page refresh, the value had reverted to the previous state.
19. 
20. ## Expected Behavior
21. 
22. - **Delegated sessions should be read-only** for another user's preferences (SC-2).
23. - **California loan restrictions** should disable the decline SMS toggle and show
24.   an explanation (FR-4).
25. - A save **should not appear successful** if the backend rejects it (ADR-003
26.   optimistic-update rollback).
27. 
28. ## Environment
29. 
30. - Web app build: `2026.03.1-rc2`
31. - Reported by: Pilot cohort underwriter ops team
32. - Frequency: 3 of 8 attempts in staging
33. 
34. ## Why This Is Nuanced
35. 
36. This bug report is deliberately designed to demonstrate overlapping constraints.
37. The visible symptom looks like a simple UI toggle issue, but the actual problem
38. touches **four** independent rules:
39. 
40. | Layer         | Rule                                                      | Source           |
41. | ------------- | --------------------------------------------------------- | ---------------- |
42. | Authorization | Delegated sessions are read-only                          | SC-2             |
43. | Business rule | CA decline SMS is restricted                              | FR-4 / LEGAL-218 |
44. | UI pattern    | Optimistic update must support rollback                   | ADR-003          |
45. | Audit         | If audit write failed, the save should have been rejected | NFR-2            |
46. 
47. ### Possible Root Causes (ranked by likelihood)
48. 
49. 1. **Delegated-session write guard** is not applied to the preference save route.
50.    The `blockDelegatedWrites` middleware may be missing from the PUT handler.
51. 2. **State restriction check** is not being called during save because `loanState`
52.    is not passed in the request body.
53. 3. **Optimistic store update** fires on HTTP 200 without checking the response body
54.    for partial rejections (207 status).
55. 4. **Audit service outage** may have caused the save to fail closed, but the error
56.    was swallowed by the frontend error boundary.
57. 
58. ### Investigation Inputs
59. 
60. - Compare UI behavior against `specs/product-spec-notification-preferences.md` sections SC-2 and FR-4.
61. - Check `src/backend/src/routes/notifications.ts` for the `blockDelegatedWrites` middleware attachment.
62. - Check whether the preference save sends `loanState` to the API.
63. - Verify that the audit service was healthy at the time of the report.
64. - Check `src/backend/src/middleware/auth.ts` for delegated-session detection logic.
```

</details>


---

<sub>⏱️ 39s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\adr\ADR-003-frontend-state.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\adr\ADR-003-frontend-state.md (lines 1-220)

<details>
<summary>37 lines</summary>

```
1. # ADR-003: Frontend State Strategy
2. 
3. ## Status
4. 
5. Accepted
6. 
7. ## Context
8. 
9. The Loan Workbench has multiple screens that share underwriting workflow state:
10. application lists, decision forms, notification settings, and audit viewers.
11. The team evaluated component-local state, context providers, and a central
12. client store.
13. 
14. ## Decision
15. 
16. Loan Workbench uses a **central client store** for cross-screen workflow state.
17. Local component state is acceptable for purely presentational concerns (e.g.
18. form input focus, tooltip visibility), but NOT for:
19. 
20. - Shared underwriting workflow state
21. - Persisted user preferences
22. - Any data that survives navigation or page refresh
23. 
24. ## Consequences
25. 
26. - Feature plans must NOT default to component-local state for persisted data.
27. - Planning outputs should explicitly call out state ownership for every new
28.   data entity.
29. - UI features that survive navigation or refresh need both store and API changes.
30. - Optimistic updates in the store must be paired with rollback logic that fires
31.   when the API rejects the change.
32. 
33. ## Implications for AI-Assisted Development
34. 
35. An AI assistant generating a notification-preferences UI will default to
36. `useState` or component-local state. The instruction context must surface
37. ADR-003 so the assistant uses the central store pattern instead.
```

</details>


---

<sub>⏱️ 45s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\notifications.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\notifications.ts (lines 1-320)

<details>
<summary>271 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Notification Preference Routes
3. // ---------------------------------------------------------------------------
4. //
5. // IMPORTANT — AUTHORIZATION:
6. //   All roles can READ preferences (for display purposes).
7. //   Only underwriters and analyst-managers can WRITE preferences.
8. //   Compliance reviewers are READ-ONLY for notification preferences.
9. //
10. // IMPORTANT — DELEGATED SESSIONS:
11. //   A delegated session (x-delegated-for header) can read the delegate's
12. //   preferences but CANNOT modify them.  The route handler must check
13. //   session.delegatedFor before allowing writes.
14. // ---------------------------------------------------------------------------
15. 
16. import { Router } from "express";
17. import { requireRole } from "../middleware/auth.js";
18. import { validateBody } from "../middleware/request-validator.js";
19. import { hasPermission } from "../rules/role-permissions.js";
20. import { auditAction } from "../services/audit-service.js";
21. import * as prefRepo from "../models/preference-repository.js";
22. import type {
23.   SessionContext,
24.   NotificationPreference,
25. } from "../models/types.js";
26. 
27. export const notificationRoutes = Router();
28. 
29. function firstParam(value: string | string[]): string {
30.   return Array.isArray(value) ? value[0] : value;
31. }
32. 
33. /** GET /api/notifications/preferences/:userId — get preferences for a user. */
34. notificationRoutes.get(
35.   "/preferences/:userId",
36.   requireRole("underwriter", "analyst-manager", "compliance-reviewer"),
37.   (req, res) => {
38.     const prefs = prefRepo.findPreferencesForUser(
39.       firstParam(req.params.userId),
40.     );
41.     res.json(prefs);
42.   },
43. );
44. 
45. /** PUT /api/notifications/preferences — set a notification preference. */
46. notificationRoutes.put(
47.   "/preferences",
48.   requireRole("underwriter", "analyst-manager"),
49.   validateBody([
50.     { field: "userId", type: "string", required: true },
51.     { field: "event", type: "string", required: true },
52.     { field: "channel", type: "string", required: true },
53.     { field: "enabled", type: "boolean", required: true },
54.   ]),
55.   (req, res, next) => {
56.     try {
57.       const session = req.session as SessionContext;
58. 
59.       // Block writes in delegated sessions
60.       if (session.delegatedFor) {
61.         res.status(403).json({
62.           error: "Delegated sessions cannot modify notification preferences.",
63.         });
64.         return;
65.       }
66. 
67.       // Additional permission check
68.       if (!hasPermission(session.actor.role, "notification-pref:write")) {
69.         res.status(403).json({
70.           error: `Role '${session.actor.role}' cannot modify notification preferences.`,
71.         });
72.         return;
73.       }
74. 
75.       const { userId, event, channel, enabled } = req.body;
76.       const now = new Date().toISOString();
77. 
78.       const previous = prefRepo.findPreference(userId, event, channel);
79. 
80.       const pref: NotificationPreference = {
81.         userId,
82.         event,
83.         channel,
84.         enabled,
85.         updatedAt: now,
86.         updatedBy: session.actor.id,
87.       };
88. 
89.       prefRepo.setPreference(pref);
90. 
91.       // Audit the preference change
92.       auditAction(
93.         session,
94.         "preference.updated",
95.         previous ?? null,
96.         pref,
97.         "notification-routes",
98.       );
99. 
100.       res.json(pref);
101.     } catch (err) {
102.       next(err);
103.     }
104.   },
105. );
106. 
107. /**
108.  * PUT /api/notifications/preferences/:userId/email — set email notification preferences for all events.
109.  * Updates the enabled flag for all notification events on the email channel.
110.  * Only the owner can modify their own preferences. Delegated sessions are blocked.
111.  */
112. notificationRoutes.put(
113.   "/preferences/:userId/email",
114.   requireRole("underwriter", "analyst-manager"),
115.   validateBody([
116.     { field: "enabled", type: "boolean", required: true },
117.   ]),
118.   (req, res, next) => {
119.     try {
120.       const session = req.session as SessionContext;
121.       const targetUserId = firstParam(req.params.userId);
122. 
123.       // Block writes in delegated sessions
124.       if (session.delegatedFor) {
125.         res.status(403).json({
126.           error: "FORBIDDEN: Delegated sessions cannot modify notification preferences.",
127.         });
128.         return;
129.       }
130. 
131.       // Enforce owner-only writes
132.       if (session.actor.id !== targetUserId) {
133.         res.status(403).json({
134.           error: `FORBIDDEN: Users can only modify their own notification preferences.`,
135.         });
136.         return;
137.       }
138. 
139.       // Permission check
140.       if (!hasPermission(session.actor.role, "notification-pref:write")) {
141.         res.status(403).json({
142.           error: `FORBIDDEN: Role '${session.actor.role}' cannot modify notification preferences.`,
143.         });
144.         return;
145.       }
146. 
147.       const { enabled } = req.body;
148.       const now = new Date().toISOString();
149.       const events: Array<"approval" | "decline" | "document-request" | "manual-review-escalation"> = [
150.         "approval",
151.         "decline",
152.         "document-request",
153.         "manual-review-escalation",
154.       ];
155. 
156.       const updates: NotificationPreference[] = [];
157. 
158.       for (const event of events) {
159.         const previous = prefRepo.findPreference(targetUserId, event, "email");
160. 
161.         const pref: NotificationPreference = {
162.           userId: targetUserId,
163.           event,
164.           channel: "email",
165.           enabled,
166.           updatedAt: now,
167.           updatedBy: session.actor.id,
168.         };
169. 
170.         prefRepo.setPreference(pref);
171.         updates.push(pref);
172. 
173.         // Audit each preference change
174.         auditAction(
175.           session,
176.           "preference.updated",
177.           previous ?? null,
178.           pref,
179.           "notification-routes",
180.         );
181.       }
182. 
183.       res.json(updates);
184.     } catch (err) {
185.       next(err);
186.     }
187.   },
188. );
189. 
190. /**
191.  * PUT /api/notifications/preferences/:userId/sms — set SMS notification preferences for all events.
192.  * Updates the enabled flag for all notification events on the SMS channel.
193.  * Only the owner can modify their own preferences. Delegated sessions are blocked.
194.  */
195. notificationRoutes.put(
196.   "/preferences/:userId/sms",
197.   requireRole("underwriter", "analyst-manager"),
198.   validateBody([
199.     { field: "enabled", type: "boolean", required: true },
200.   ]),
201.   (req, res, next) => {
202.     try {
203.       const session = req.session as SessionContext;
204.       const targetUserId = firstParam(req.params.userId);
205. 
206.       // Block writes in delegated sessions
207.       if (session.delegatedFor) {
208.         res.status(403).json({
209.           error: "FORBIDDEN: Delegated sessions cannot modify notification preferences.",
210.         });
211.         return;
212.       }
213. 
214.       // Enforce owner-only writes
215.       if (session.actor.id !== targetUserId) {
216.         res.status(403).json({
217.           error: `FORBIDDEN: Users can only modify their own notification preferences.`,
218.         });
219.         return;
220.       }
221. 
222.       // Permission check
223.       if (!hasPermission(session.actor.role, "notification-pref:write")) {
224.         res.status(403).json({
225.           error: `FORBIDDEN: Role '${session.actor.role}' cannot modify notification preferences.`,
226.         });
227.         return;
228.       }
229. 
230.       const { enabled } = req.body;
231.       const now = new Date().toISOString();
232.       const events: Array<"approval" | "decline" | "document-request" | "manual-review-escalation"> = [
233.         "approval",
234.         "decline",
235.         "document-request",
236.         "manual-review-escalation",
237.       ];
238. 
239.       const updates: NotificationPreference[] = [];
240. 
241.       for (const event of events) {
242.         const previous = prefRepo.findPreference(targetUserId, event, "sms");
243. 
244.         const pref: NotificationPreference = {
245.           userId: targetUserId,
246.           event,
247.           channel: "sms",
248.           enabled,
249.           updatedAt: now,
250.           updatedBy: session.actor.id,
251.         };
252. 
253.         prefRepo.setPreference(pref);
254.         updates.push(pref);
255. 
256.         // Audit each preference change
257.         auditAction(
258.           session,
259.           "preference.updated",
260.           previous ?? null,
261.           pref,
262.           "notification-routes",
263.         );
264.       }
265. 
266.       res.json(updates);
267.     } catch (err) {
268.       next(err);
269.     }
270.   },
271. );
```

</details>


---

<sub>⏱️ 45s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\auth.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\auth.ts (lines 1-260)

<details>
<summary>97 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Authentication & Authorization Middleware
3. // ---------------------------------------------------------------------------
4. //
5. // KEY NUANCE — DELEGATED SESSIONS:
6. //   When the `x-delegated-for` header is present, the session is marked as
7. //   delegated.  Delegated sessions allow READ operations on the delegate's
8. //   data but BLOCK writes.  An AI assistant without context would likely
9. //   skip this distinction, producing code that allows delegated writes.
10. //
11. // KEY NUANCE — COMPLIANCE REVIEWER:
12. //   Compliance reviewers can view notification preferences and audit logs
13. //   but cannot modify operational settings.  This is a read-only role for
14. //   the notification feature, even though the role has write permissions
15. //   in other parts of the system.
16. // ---------------------------------------------------------------------------
17. 
18. import type { Request, Response, NextFunction } from "express";
19. import type { UserRole, SessionContext } from "../models/types.js";
20. import { findUserById } from "../models/user-repository.js";
21. 
22. // Extend Express Request to carry session context.
23. declare global {
24.   namespace Express {
25.     interface Request {
26.       session?: SessionContext;
27.     }
28.   }
29. }
30. 
31. /**
32.  * Authenticate the request and attach a SessionContext.
33.  *
34.  * In production this would validate a JWT or session cookie.  For the
35.  * demo we resolve the user from an `x-user-id` header and optionally
36.  * attach delegated-session context from `x-delegated-for`.
37.  */
38. export function authMiddleware(
39.   req: Request,
40.   res: Response,
41.   next: NextFunction,
42. ): void {
43.   // Skip auth for health check.
44.   if (req.path === "/health") {
45.     next();
46.     return;
47.   }
48. 
49.   const userId = req.headers["x-user-id"] as string | undefined;
50.   if (!userId) {
51.     res.status(401).json({ error: "Missing x-user-id header." });
52.     return;
53.   }
54. 
55.   const actor = findUserById(userId);
56.   if (!actor) {
57.     res.status(401).json({ error: `Unknown user '${userId}'.` });
58.     return;
59.   }
60. 
61.   const session: SessionContext = { actor };
62. 
63.   // Check for delegated session.
64.   const delegatedId = req.headers["x-delegated-for"] as string | undefined;
65.   if (delegatedId) {
66.     const delegate = findUserById(delegatedId);
67.     if (!delegate) {
68.       res.status(400).json({ error: `Unknown delegate '${delegatedId}'.` });
69.       return;
70.     }
71.     session.delegatedFor = delegate;
72.   }
73. 
74.   req.session = session;
75.   next();
76. }
77. 
78. /**
79.  * Role-gate middleware factory.
80.  * Returns 403 if the actor's role is not in the allowed set.
81.  */
82. export function requireRole(...roles: UserRole[]) {
83.   const allowed = new Set(roles);
84.   return (req: Request, res: Response, next: NextFunction): void => {
85.     if (!req.session) {
86.       res.status(401).json({ error: "Not authenticated." });
87.       return;
88.     }
89.     if (!allowed.has(req.session.actor.role)) {
90.       res.status(403).json({
91.         error: `Role '${req.session.actor.role}' is not authorized for this operation.`,
92.       });
93.       return;
94.     }
95.     next();
96.   };
97. }
```

</details>


---

<sub>⏱️ 45s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\role-permissions.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\role-permissions.ts (lines 1-220)

<details>
<summary>63 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Role Permissions Matrix
3. // ---------------------------------------------------------------------------
4. // Defines what each role can do across the system.  This is the single
5. // source of truth for authorization decisions beyond route-level guards.
6. //
7. // IMPORTANT — COMPLIANCE REVIEWER NUANCE:
8. //   Compliance reviewers have READ access to most resources but WRITE access
9. //   only to compliance-specific actions (sign-offs, compliance notes).
10. //   They CANNOT modify notification preferences, even though they can view
11. //   them.  This is frequently missed by code generators.
12. // ---------------------------------------------------------------------------
13. 
14. import type { UserRole } from "../models/types.js";
15. 
16. export type Permission =
17.   | "loan:read"
18.   | "loan:create"
19.   | "loan:transition"
20.   | "decision:read"
21.   | "decision:create"
22.   | "notification-pref:read"
23.   | "notification-pref:write"
24.   | "audit:read"
25.   | "compliance:sign-off";
26. 
27. const ROLE_PERMISSIONS: Record<UserRole, Set<Permission>> = {
28.   underwriter: new Set([
29.     "loan:read",
30.     "loan:create",
31.     "loan:transition",
32.     "decision:read",
33.     "decision:create",
34.     "notification-pref:read",
35.     "notification-pref:write",
36.     "audit:read",
37.   ]),
38.   "analyst-manager": new Set([
39.     "loan:read",
40.     "loan:create",
41.     "loan:transition",
42.     "decision:read",
43.     "decision:create",
44.     "notification-pref:read",
45.     "notification-pref:write",
46.     "audit:read",
47.   ]),
48.   "compliance-reviewer": new Set([
49.     "loan:read",
50.     "decision:read",
51.     "notification-pref:read", // READ only — no write
52.     "audit:read",
53.     "compliance:sign-off",
54.   ]),
55. };
56. 
57. export function hasPermission(role: UserRole, permission: Permission): boolean {
58.   return ROLE_PERMISSIONS[role]?.has(permission) ?? false;
59. }
60. 
61. export function getPermissions(role: UserRole): Permission[] {
62.   return [...(ROLE_PERMISSIONS[role] ?? [])];
63. }
```

</details>


---

<sub>⏱️ 45s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\mandatory-events.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\mandatory-events.ts (lines 1-220)

<details>
<summary>37 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Mandatory Notification Events
3. // ---------------------------------------------------------------------------
4. // Defines which notification events MUST fire for each state transition.
5. // These are non-negotiable business requirements — skipping a mandatory
6. // event is a compliance violation.
7. //
8. // When a transition occurs, the loan service must emit notification events
9. // for ALL mandatory events listed here.
10. // ---------------------------------------------------------------------------
11. 
12. import type { ApplicationState, NotificationEvent } from "../models/types.js";
13. 
14. type TransitionKey = `${ApplicationState}->${ApplicationState}`;
15. 
16. /**
17.  * Map of state transitions to mandatory notification events.
18.  * If a transition is not listed, no mandatory notifications are required.
19.  */
20. export const MANDATORY_EVENTS: Partial<
21.   Record<TransitionKey, NotificationEvent[]>
22. > = {
23.   "decision->finalized": ["approval"],
24.   "underwriting->decision": ["manual-review-escalation"],
25.   "review->intake": ["document-request"],
26. };
27. 
28. /**
29.  * Get the mandatory notification events for a given state transition.
30.  */
31. export function getMandatoryEvents(
32.   from: ApplicationState,
33.   to: ApplicationState,
34. ): NotificationEvent[] {
35.   const key: TransitionKey = `${from}->${to}`;
36.   return MANDATORY_EVENTS[key] ?? [];
37. }
```

</details>


---

<sub>⏱️ 45s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\notification-service.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\notification-service.ts (lines 1-260)

<details>
<summary>47 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Notification Service
3. // ---------------------------------------------------------------------------
4. // High-level API for sending notifications.  Route handlers call this
5. // service, which emits events to the message broker.  Actual delivery is
6. // handled by queue/handlers/notification-handler.ts.
7. //
8. // NFR REQUIREMENT — DEGRADED MODE:
9. //   When the SMS provider is unavailable, delivery must fall back to email
10. //   IF email is enabled for that event.  The fallback must NOT change the
11. //   user's stored preferences — it is a runtime delivery decision only.
12. //
13. // KEY NUANCE — FALSE POSITIVE:
14. //   A user receiving an email instead of an SMS during an SMS outage is NOT
15. //   a preference bug.  The stored preference still says "sms: true" — the
16. //   delivery system silently fell back.  Support agents must check delivery
17. //   logs, not the preference store, to diagnose delivery complaints.
18. // ---------------------------------------------------------------------------
19. 
20. import { v4 as uuid } from "uuid";
21. import { broker } from "../queue/broker.js";
22. import type { NotificationRequestedEvent } from "../queue/contracts.js";
23. import type {
24.   NotificationEvent,
25.   NotificationChannel,
26. } from "../models/types.js";
27. 
28. /**
29.  * Request notification delivery for a user.
30.  * The actual delivery is asynchronous via the message queue.
31.  */
32. export function requestNotification(
33.   userId: string,
34.   event: NotificationEvent,
35.   subject: string,
36.   body: string,
37.   preferredChannel: NotificationChannel = "email",
38. ): void {
39.   const notifEvent: NotificationRequestedEvent = {
40.     eventId: uuid(),
41.     timestamp: new Date().toISOString(),
42.     source: "notification-service",
43.     type: "notification.requested",
44.     payload: { userId, event, subject, body, preferredChannel },
45.   };
46.   broker.emit(notifEvent);
47. }
```

</details>


---

<sub>⏱️ 45s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\audit-service.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\audit-service.ts (lines 1-260)

<details>
<summary>46 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Audit Service
3. // ---------------------------------------------------------------------------
4. // High-level audit API.  Provides convenience methods that emit events
5. // to the message queue (or write directly depending on feature flags).
6. // ---------------------------------------------------------------------------
7. 
8. import { v4 as uuid } from "uuid";
9. import { broker } from "../queue/broker.js";
10. import { featureFlags } from "../config/feature-flags.js";
11. import { createAuditEntry } from "../models/audit-repository.js";
12. import type { AuditRequestedEvent } from "../queue/contracts.js";
13. import type { SessionContext } from "../models/types.js";
14. 
15. /**
16.  * Write an audit entry for an action performed in a session context.
17.  */
18. export function auditAction(
19.   session: SessionContext,
20.   action: string,
21.   previousValue: unknown,
22.   newValue: unknown,
23.   source: string,
24. ): void {
25.   const payload = {
26.     action,
27.     actor: session.actor.id,
28.     delegatedFor: session.delegatedFor?.id,
29.     previousValue,
30.     newValue,
31.     source,
32.   };
33. 
34.   if (featureFlags.queueAudit) {
35.     const event: AuditRequestedEvent = {
36.       eventId: uuid(),
37.       timestamp: new Date().toISOString(),
38.       source,
39.       type: "audit.requested",
40.       payload,
41.     };
42.     broker.emit(event);
43.   } else {
44.     createAuditEntry(payload);
45.   }
46. }
```

</details>


---

<sub>⏱️ 51s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\models\preference-repository.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\models\preference-repository.ts (lines 1-260)

<details>
<summary>85 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Notification Preference Repository
3. // ---------------------------------------------------------------------------
4. // Database operations for notification preferences.
5. //
6. // KEY NUANCE — UPSERT BEHAVIOR:
7. //   The `setPreference` function uses INSERT OR REPLACE on the composite
8. //   primary key (user_id, event, channel).  This means updating a preference
9. //   replaces the entire row — there is no partial update.  The `updated_by`
10. //   field MUST always be set (it tracks who last changed the preference).
11. // ---------------------------------------------------------------------------
12. 
13. import { getDb } from "../db/connection.js";
14. import type {
15.   NotificationPreference,
16.   NotificationEvent,
17.   NotificationChannel,
18. } from "./types.js";
19. 
20. const PREFERENCE_COLUMNS = `
21.   user_id AS userId,
22.   event,
23.   channel,
24.   enabled,
25.   updated_at AS updatedAt,
26.   updated_by AS updatedBy
27. `;
28. 
29. type PreferenceRow = NotificationPreference & { enabled: number | boolean };
30. 
31. export function findPreferencesForUser(
32.   userId: string,
33. ): NotificationPreference[] {
34.   const db = getDb();
35.   return db
36.     .prepare(
37.       `SELECT ${PREFERENCE_COLUMNS} FROM notification_preferences WHERE user_id = ?`,
38.     )
39.     .all(userId)
40.     .map((pref) => pref as PreferenceRow)
41.     .map((pref) => ({
42.       ...pref,
43.       enabled: Boolean(pref.enabled),
44.     })) as NotificationPreference[];
45. }
46. 
47. export function findPreference(
48.   userId: string,
49.   event: NotificationEvent,
50.   channel: NotificationChannel,
51. ): NotificationPreference | undefined {
52.   const db = getDb();
53.   const pref = db
54.     .prepare(
55.       `SELECT ${PREFERENCE_COLUMNS} FROM notification_preferences WHERE user_id = ? AND event = ? AND channel = ?`,
56.     )
57.     .get(userId, event, channel) as
58.     | (NotificationPreference & { enabled: number | boolean })
59.     | undefined;
60. 
61.   return pref ? { ...pref, enabled: Boolean(pref.enabled) } : undefined;
62. }
63. 
64. export function setPreference(pref: NotificationPreference): void {
65.   const db = getDb();
66.   db.prepare(
67.     `INSERT OR REPLACE INTO notification_preferences (user_id, event, channel, enabled, updated_at, updated_by)
68.      VALUES (?, ?, ?, ?, ?, ?)`,
69.   ).run(
70.     pref.userId,
71.     pref.event,
72.     pref.channel,
73.     pref.enabled ? 1 : 0,
74.     pref.updatedAt,
75.     pref.updatedBy,
76.   );
77. }
78. 
79. export function deletePreferencesForUser(userId: string): number {
80.   const db = getDb();
81.   const result = db
82.     .prepare("DELETE FROM notification_preferences WHERE user_id = ?")
83.     .run(userId);
84.   return result.changes;
85. }
```

</details>


---

<sub>⏱️ 51s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\models\types.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\models\types.ts (lines 1-260)

<details>
<summary>111 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Loan Workbench — Domain Types
3. // ---------------------------------------------------------------------------
4. // This file defines the core domain model for the Loan Workbench platform.
5. // Business rules, state machines, authorization logic, queue contracts, and
6. // database schema all depend on these types.  Changes here affect nearly
7. // every module in the project.
8. // ---------------------------------------------------------------------------
9. 
10. /** Lifecycle states for a commercial loan application. */
11. export type ApplicationState =
12.   | "intake"
13.   | "review"
14.   | "underwriting"
15.   | "decision"
16.   | "finalized";
17. 
18. /**
19.  * Valid state transitions.
20.  * Transitions not listed here are forbidden — the system must never allow
21.  * a finalized application to move backward.
22.  */
23. export const VALID_TRANSITIONS: Record<ApplicationState, ApplicationState[]> = {
24.   intake: ["review"],
25.   review: ["underwriting", "intake"], // can return to intake for rework
26.   underwriting: ["decision"],
27.   decision: ["finalized", "underwriting"], // can push back to underwriting
28.   finalized: [], // terminal — no transitions allowed
29. };
30. 
31. /** Organizational roles recognized by the Loan Workbench. */
32. export type UserRole =
33.   | "underwriter"
34.   | "analyst-manager"
35.   | "compliance-reviewer";
36. 
37. /** Notification event types that can trigger user-facing alerts. */
38. export type NotificationEvent =
39.   | "approval"
40.   | "decline"
41.   | "document-request"
42.   | "manual-review-escalation";
43. 
44. /** Delivery channels available for notifications. */
45. export type NotificationChannel = "email" | "sms";
46. 
47. // ---------------------------------------------------------------------------
48. // Entity interfaces
49. // ---------------------------------------------------------------------------
50. 
51. export interface User {
52.   id: string;
53.   role: UserRole;
54.   name: string;
55.   email: string;
56.   phone?: string;
57. }
58. 
59. /**
60.  * Session context attached to every authenticated request.
61.  *
62.  * When `delegatedFor` is present the actor is operating on behalf of another
63.  * user.  Delegated sessions restrict write operations — see auth middleware.
64.  */
65. export interface SessionContext {
66.   actor: User;
67.   delegatedFor?: User;
68. }
69. 
70. export interface LoanApplication {
71.   id: string;
72.   borrowerName: string;
73.   amount: number;
74.   /** US state / jurisdiction — affects business rules (e.g. California). */
75.   loanState: string;
76.   status: ApplicationState;
77.   assignedUnderwriter: string;
78.   riskScore: number | null;
79.   createdAt: string;
80.   updatedAt: string;
81. }
82. 
83. export interface Decision {
84.   id: string;
85.   applicationId: string;
86.   type: "approved" | "declined" | "conditional";
87.   rationale: string;
88.   decidedBy: string;
89.   decidedAt: string;
90.   conditions?: string[];
91. }
92. 
93. export interface NotificationPreference {
94.   userId: string;
95.   event: NotificationEvent;
96.   channel: NotificationChannel;
97.   enabled: boolean;
98.   updatedAt: string;
99.   updatedBy: string;
100. }
101. 
102. export interface AuditEntry {
103.   id: string;
104.   action: string;
105.   actor: string;
106.   delegatedFor: string | null;
107.   timestamp: string;
108.   previousValue: string | null;
109.   newValue: string | null;
110.   source: string;
111. }
```

</details>


---

<sub>⏱️ 51s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\config\feature-flags.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\config\feature-flags.ts (lines 1-220)

<details>
<summary>27 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Feature Flags
3. // ---------------------------------------------------------------------------
4. // Runtime feature flags that control business behavior.
5. // These are loaded from environment variables via config/env.ts.
6. //
7. // IMPORTANT: Feature flags affect business rules, notification delivery,
8. // and audit behavior.  When adding a new flag, update:
9. //   1. config/env.ts  — add the env var mapping
10. //   2. This file      — add the typed accessor
11. //   3. docs/          — document the flag's behavior and rollout plan
12. // ---------------------------------------------------------------------------
13. 
14. import { config } from "./env.js";
15. 
16. export const featureFlags = {
17.   /** Enable California-specific lending regulations (higher thresholds, extra disclosures). */
18.   californiaRules: config.features.californiaRules,
19. 
20.   /** Enable SMS → email fallback when SMS provider is unavailable. */
21.   smsFallback: config.features.smsFallback,
22. 
23.   /** Route audit writes through the message queue instead of synchronous DB writes. */
24.   queueAudit: config.features.queueAudit,
25. } as const;
26. 
27. export type FeatureFlag = keyof typeof featureFlags;
```

</details>


---

<sub>⏱️ 51s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\contracts.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\contracts.ts (lines 1-260)

<details>
<summary>72 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Message Queue — Event Contracts
3. // ---------------------------------------------------------------------------
4. // Defines the typed message contracts for the in-process event broker.
5. // All producers and consumers MUST use these types.
6. //
7. // IMPORTANT — CONTRACT CHANGES:
8. //   Changing a message contract is a BREAKING CHANGE.  When modifying:
9. //   1. Update the type here
10. //   2. Update ALL handlers that consume the event
11. //   3. Update ALL producers that emit the event
12. //   4. Add an audit entry for the contract change
13. //
14. // This is a common source of bugs when AI assistants generate code without
15. // seeing the consumer side of a contract.
16. // ---------------------------------------------------------------------------
17. 
18. import type {
19.   NotificationEvent,
20.   NotificationChannel,
21. } from "../models/types.js";
22. 
23. /** Base event structure — all events must include these fields. */
24. export interface BaseEvent {
25.   eventId: string;
26.   timestamp: string;
27.   source: string;
28. }
29. 
30. /** Emitted when a notification must be delivered to a user. */
31. export interface NotificationRequestedEvent extends BaseEvent {
32.   type: "notification.requested";
33.   payload: {
34.     userId: string;
35.     event: NotificationEvent;
36.     subject: string;
37.     body: string;
38.     preferredChannel: NotificationChannel;
39.   };
40. }
41. 
42. /** Emitted when an audit entry must be persisted. */
43. export interface AuditRequestedEvent extends BaseEvent {
44.   type: "audit.requested";
45.   payload: {
46.     action: string;
47.     actor: string;
48.     delegatedFor?: string;
49.     previousValue?: unknown;
50.     newValue?: unknown;
51.     source: string;
52.   };
53. }
54. 
55. /** Emitted when a loan application changes state. */
56. export interface LoanStateChangedEvent extends BaseEvent {
57.   type: "loan.state-changed";
58.   payload: {
59.     applicationId: string;
60.     previousStatus: string;
61.     newStatus: string;
62.     changedBy: string;
63.   };
64. }
65. 
66. /** Union of all event types the broker can handle. */
67. export type BrokerEvent =
68.   | NotificationRequestedEvent
69.   | AuditRequestedEvent
70.   | LoanStateChangedEvent;
71. 
72. export type EventType = BrokerEvent["type"];
```

</details>


---

<sub>⏱️ 51s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers\notification-handler.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers\notification-handler.ts (lines 1-260)

<details>
<summary>86 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Queue Handler — Notification Delivery
3. // ---------------------------------------------------------------------------
4. // Consumes `notification.requested` events from the broker and delivers
5. // notifications through the appropriate channel.
6. //
7. // IMPORTANT — SMS FALLBACK:
8. //   When the SMS provider is unavailable and the feature flag is enabled,
9. //   delivery falls back to email IF the user has email enabled for that
10. //   event.  The fallback does NOT change stored preferences — it is a
11. //   runtime delivery decision only.
12. // ---------------------------------------------------------------------------
13. 
14. import { broker } from "../broker.js";
15. import type { NotificationRequestedEvent } from "../contracts.js";
16. import { findPreferencesForUser } from "../../models/preference-repository.js";
17. import { featureFlags } from "../../config/feature-flags.js";
18. 
19. /** Simulated provider health.  Toggle in tests. */
20. const providerHealth = { email: true, sms: true };
21. 
22. export function setProviderHealth(
23.   channel: "email" | "sms",
24.   healthy: boolean,
25. ): void {
26.   providerHealth[channel] = healthy;
27. }
28. 
29. export function getProviderHealth(): { email: boolean; sms: boolean } {
30.   return { ...providerHealth };
31. }
32. 
33. async function handleNotificationRequested(
34.   event: NotificationRequestedEvent,
35. ): Promise<void> {
36.   const {
37.     userId,
38.     event: notifEvent,
39.     subject,
40.     body,
41.     preferredChannel,
42.   } = event.payload;
43. 
44.   const prefs = findPreferencesForUser(userId);
45.   const enabledChannels = prefs
46.     .filter((p) => p.event === notifEvent && p.enabled)
47.     .map((p) => p.channel);
48. 
49.   if (enabledChannels.length === 0) {
50.     console.log(
51.       `[notification-handler] No enabled channels for user=${userId} event=${notifEvent}`,
52.     );
53.     return;
54.   }
55. 
56.   for (const channel of enabledChannels) {
57.     if (providerHealth[channel]) {
58.       // Provider is healthy — deliver normally
59.       console.log(
60.         `[notification-handler] Delivered via ${channel}: "${subject}" to user=${userId}`,
61.       );
62.     } else if (
63.       featureFlags.smsFallback &&
64.       channel === "sms" &&
65.       providerHealth.email &&
66.       enabledChannels.includes("email")
67.     ) {
68.       // SMS is down, email is healthy, user has email enabled → fall back
69.       console.log(
70.         `[notification-handler] SMS unavailable — falling back to email: "${subject}" to user=${userId}`,
71.       );
72.     } else {
73.       console.warn(
74.         `[notification-handler] Cannot deliver via ${channel} — provider unhealthy, no fallback`,
75.       );
76.     }
77.   }
78. }
79. 
80. /** Register the handler with the broker. */
81. export function registerNotificationHandler(): void {
82.   broker.on("notification.requested", handleNotificationRequested);
83.   console.log(
84.     "[notification-handler] Registered for notification.requested events",
85.   );
86. }
```

</details>


---

<sub>⏱️ 51s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers\audit-handler.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers\audit-handler.ts (lines 1-220)

<details>
<summary>59 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Queue Handler — Audit Persistence
3. // ---------------------------------------------------------------------------
4. // Consumes `audit.requested` events from the broker and writes them to
5. // the database.  This decouples audit writes from request handlers,
6. // improving response latency for mutating operations.
7. //
8. // IMPORTANT — FAIL CLOSED:
9. //   If the audit write fails, the handler retries once.  If the retry
10. //   also fails, the error is logged as CRITICAL.  In production, this
11. //   would trigger an alert.  The original operation is NOT rolled back
12. //   (the event was already emitted after the operation succeeded).
13. // ---------------------------------------------------------------------------
14. 
15. import { broker } from "../broker.js";
16. import type { AuditRequestedEvent } from "../contracts.js";
17. import { createAuditEntry } from "../../models/audit-repository.js";
18. 
19. async function handleAuditRequested(event: AuditRequestedEvent): Promise<void> {
20.   const { action, actor, delegatedFor, previousValue, newValue, source } =
21.     event.payload;
22. 
23.   try {
24.     createAuditEntry({
25.       action,
26.       actor,
27.       delegatedFor,
28.       previousValue,
29.       newValue,
30.       source,
31.     });
32.   } catch (err) {
33.     console.error(
34.       "[audit-handler] First write attempt failed, retrying...",
35.       err,
36.     );
37.     try {
38.       createAuditEntry({
39.         action,
40.         actor,
41.         delegatedFor,
42.         previousValue,
43.         newValue,
44.         source,
45.       });
46.     } catch (retryErr) {
47.       console.error(
48.         "[audit-handler] CRITICAL: Audit write failed after retry",
49.         retryErr,
50.       );
51.     }
52.   }
53. }
54. 
55. /** Register the handler with the broker. */
56. export function registerAuditHandler(): void {
57.   broker.on("audit.requested", handleAuditRequested);
58.   console.log("[audit-handler] Registered for audit.requested events");
59. }
```

</details>


---

<sub>⏱️ 57s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\pages\preferences.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\pages\preferences.ts (lines 1-320)

<details>
<summary>40 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Notification Preferences Page
3. // ---------------------------------------------------------------------------
4. // Shows notification preferences for the current user and allows toggling.
5. // ---------------------------------------------------------------------------
6. 
7. import { getPreferences } from "../api/client.js";
8. import { renderNotificationToggle } from "../components/notification-toggle.js";
9. 
10. export async function renderPreferences(container: HTMLElement): Promise<void> {
11.   container.innerHTML = `<p class="loading">Loading preferences...</p>`;
12. 
13.   const userSelect = document.querySelector<HTMLSelectElement>("#user-select");
14.   const userId = userSelect?.value ?? "u-1";
15. 
16.   try {
17.     const prefs = await getPreferences(userId);
18. 
19.     container.innerHTML = `
20.       <section class="preferences-page">
21.         <h2>Notification Preferences</h2>
22.         <p class="subtitle">Manage how you receive notifications for loan events.</p>
23.         <div id="pref-list" class="pref-list"></div>
24.       </section>
25.     `;
26. 
27.     const prefList = container.querySelector<HTMLElement>("#pref-list")!;
28. 
29.     if (prefs.length === 0) {
30.       prefList.innerHTML = `<p class="empty-state">No preferences configured. Defaults will be used.</p>`;
31.       return;
32.     }
33. 
34.     for (const pref of prefs) {
35.       renderNotificationToggle(prefList, pref, userId);
36.     }
37.   } catch (err) {
38.     container.innerHTML = `<p class="error">Failed to load preferences: ${(err as Error).message}</p>`;
39.   }
40. }
```

</details>


---

<sub>⏱️ 57s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\components\notification-toggle.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\components\notification-toggle.ts (lines 1-260)

<details>
<summary>45 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Notification Toggle Component
3. // ---------------------------------------------------------------------------
4. // Renders a toggle switch for a notification preference.
5. // ---------------------------------------------------------------------------
6. 
7. import type { ApiPreference } from "../api/types.js";
8. import { setPreference } from "../api/client.js";
9. 
10. export function renderNotificationToggle(
11.   container: HTMLElement,
12.   pref: ApiPreference,
13.   userId: string,
14. ): void {
15.   const id = `toggle-${pref.event}-${pref.channel}`;
16.   const checked = pref.enabled ? "checked" : "";
17. 
18.   const wrapper = document.createElement("div");
19.   wrapper.className = "notification-toggle";
20.   wrapper.innerHTML = `
21.     <label for="${id}" class="toggle-label">
22.       <span class="toggle-event">${pref.event}</span>
23.       <span class="toggle-channel">${pref.channel}</span>
24.     </label>
25.     <input type="checkbox" id="${id}" class="toggle-input" ${checked} />
26.   `;
27. 
28.   const input = wrapper.querySelector<HTMLInputElement>("input")!;
29.   input.addEventListener("change", async () => {
30.     try {
31.       await setPreference({
32.         userId,
33.         event: pref.event,
34.         channel: pref.channel,
35.         enabled: input.checked,
36.       });
37.     } catch (err) {
38.       // Revert on failure
39.       input.checked = !input.checked;
40.       console.error("Failed to update preference:", err);
41.     }
42.   });
43. 
44.   container.appendChild(wrapper);
45. }
```

</details>


---

<sub>⏱️ 57s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\api\client.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\api\client.ts (lines 1-280)

<details>
<summary>103 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // API Client
3. // ---------------------------------------------------------------------------
4. // Typed HTTP client for the Loan Workbench backend API.
5. // All API calls go through this module — routes/pages never use fetch directly.
6. // ---------------------------------------------------------------------------
7. 
8. import type {
9.   ApiLoanApplication,
10.   ApiDecision,
11.   ApiPreference,
12.   ApiAuditEntry,
13. } from "./types.js";
14. 
15. const BASE_URL = "/api";
16. 
17. /** Current user ID — set by the app shell. */
18. let currentUserId = "u-1";
19. 
20. export function setCurrentUser(userId: string): void {
21.   currentUserId = userId;
22. }
23. 
24. export async function apiFetch<T>(
25.   path: string,
26.   options: RequestInit = {},
27. ): Promise<T> {
28.   const headers: Record<string, string> = {
29.     "Content-Type": "application/json",
30.     "x-user-id": currentUserId,
31.     ...((options.headers as Record<string, string>) ?? {}),
32.   };
33. 
34.   const res = await fetch(`${BASE_URL}${path}`, { ...options, headers });
35. 
36.   if (!res.ok) {
37.     const body = await res.json().catch(() => ({ error: res.statusText }));
38.     throw new Error(body.error ?? `HTTP ${res.status}`);
39.   }
40. 
41.   return res.json() as Promise<T>;
42. }
43. 
44. // ── Applications ──
45. 
46. export function getApplications(): Promise<ApiLoanApplication[]> {
47.   return apiFetch("/applications");
48. }
49. 
50. export function getApplication(id: string): Promise<ApiLoanApplication> {
51.   return apiFetch(`/applications/${encodeURIComponent(id)}`);
52. }
53. 
54. export function createApplication(data: {
55.   borrowerName: string;
56.   amount: number;
57.   loanState: string;
58. }): Promise<ApiLoanApplication> {
59.   return apiFetch("/applications", {
60.     method: "POST",
61.     body: JSON.stringify(data),
62.   });
63. }
64. 
65. export function transitionApplication(
66.   id: string,
67.   status: string,
68. ): Promise<ApiLoanApplication> {
69.   return apiFetch(`/applications/${encodeURIComponent(id)}/status`, {
70.     method: "PATCH",
71.     body: JSON.stringify({ status }),
72.   });
73. }
74. 
75. // ── Decisions ──
76. 
77. export function getDecisions(applicationId: string): Promise<ApiDecision[]> {
78.   return apiFetch(`/decisions/${encodeURIComponent(applicationId)}`);
79. }
80. 
81. // ── Notifications ──
82. 
83. export function getPreferences(userId: string): Promise<ApiPreference[]> {
84.   return apiFetch(`/notifications/preferences/${encodeURIComponent(userId)}`);
85. }
86. 
87. export function setPreference(pref: {
88.   userId: string;
89.   event: string;
90.   channel: string;
91.   enabled: boolean;
92. }): Promise<ApiPreference> {
93.   return apiFetch("/notifications/preferences", {
94.     method: "PUT",
95.     body: JSON.stringify(pref),
96.   });
97. }
98. 
99. // ── Audit ──
100. 
101. export function getAuditEntries(limit = 50): Promise<ApiAuditEntry[]> {
102.   return apiFetch(`/audit?limit=${limit}`);
103. }
```

</details>


---

<sub>⏱️ 57s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\api\types.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\api\types.ts (lines 1-260)

<details>
<summary>46 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Frontend API Response Types
3. // ---------------------------------------------------------------------------
4. // Mirror the backend types for use in the frontend.
5. // These MUST stay in sync with backend/src/models/types.ts.
6. // ---------------------------------------------------------------------------
7. 
8. export interface ApiLoanApplication {
9.   id: string;
10.   borrowerName: string;
11.   amount: number;
12.   loanState: string;
13.   status: string;
14.   assignedUnderwriter: string;
15.   riskScore: number | null;
16.   createdAt: string;
17.   updatedAt: string;
18. }
19. 
20. export interface ApiDecision {
21.   id: string;
22.   applicationId: string;
23.   type: "approved" | "declined" | "conditional";
24.   rationale: string;
25.   decidedBy: string;
26.   decidedAt: string;
27.   conditions?: string[];
28. }
29. 
30. export interface ApiPreference {
31.   userId: string;
32.   event: string;
33.   channel: string;
34.   enabled: boolean;
35.   updatedAt: string;
36.   updatedBy: string;
37. }
38. 
39. export interface ApiAuditEntry {
40.   id: string;
41.   action: string;
42.   actor: string;
43.   delegatedFor: string | null;
44.   timestamp: string;
45.   source: string;
46. }
```

</details>


---

<sub>⏱️ 57s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\main.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\main.ts (lines 1-260)

<details>
<summary>58 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Frontend Entry Point
3. // ---------------------------------------------------------------------------
4. // Initializes the single-page application, sets up routing, and renders
5. // the initial page (dashboard).
6. // ---------------------------------------------------------------------------
7. 
8. import { renderAppShell } from "./components/app-shell.js";
9. import { renderDashboard } from "./pages/dashboard.js";
10. 
11. function init(): void {
12.   const root = document.getElementById("app");
13.   if (!root) return;
14. 
15.   renderAppShell(root);
16. 
17.   // Simple hash-based routing
18.   const navigate = (): void => {
19.     const content = document.getElementById("main-content");
20.     if (!content) return;
21. 
22.     const hash = window.location.hash.slice(1) || "dashboard";
23.     const route = hash.split("?")[0];
24. 
25.     switch (route) {
26.       case "dashboard":
27.         renderDashboard(content);
28.         break;
29.       case "preferences":
30.         import("./pages/preferences.js").then((m) =>
31.           m.renderPreferences(content),
32.         );
33.         break;
34.       case "application":
35.         import("./pages/application-detail.js").then((m) =>
36.           m.renderApplicationDetail(content),
37.         );
38.         break;
39.       case "queue":
40.         import("./pages/queue-monitor.js").then((m) =>
41.           m.renderQueueMonitor(content),
42.         );
43.         break;
44.       case "api":
45.         import("./pages/api-explorer.js").then((m) =>
46.           m.renderApiExplorer(content),
47.         );
48.         break;
49.       default:
50.         renderDashboard(content);
51.     }
52.   };
53. 
54.   window.addEventListener("hashchange", navigate);
55.   navigate();
56. }
57. 
58. document.addEventListener("DOMContentLoaded", init);
```

</details>


---

<sub>⏱️ 57s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\app.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\app.ts (lines 1-260)

<details>
<summary>81 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Loan Workbench — Application Entry Point
3. // ---------------------------------------------------------------------------
4. // Express server with middleware chain, route mounting, database init,
5. // and message queue handler registration.
6. //
7. // MIDDLEWARE ORDER (matters!):
8. //   1. express.json()          — Parse JSON bodies
9. //   2. rateLimiterMiddleware   — Rate limit before auth (prevent brute force)
10. //   3. authMiddleware          — Authenticate & attach session context
11. //   4. auditLoggerMiddleware   — Log mutating requests (needs session)
12. //   5. Routes                  — Business logic
13. //   6. errorHandler            — Catch-all error handler (MUST be last)
14. // ---------------------------------------------------------------------------
15. 
16. import express from "express";
17. import path from "path";
18. import { fileURLToPath } from "url";
19. import { config } from "./config/env.js";
20. import { getDb } from "./db/connection.js";
21. import { seedDatabase } from "./db/seed.js";
22. import { authMiddleware } from "./middleware/auth.js";
23. import { auditLoggerMiddleware } from "./middleware/audit-logger.js";
24. import { rateLimiterMiddleware } from "./middleware/rate-limiter.js";
25. import { errorHandler } from "./middleware/error-handler.js";
26. import { applicationRoutes } from "./routes/applications.js";
27. import { decisionRoutes } from "./routes/decisions.js";
28. import { notificationRoutes } from "./routes/notifications.js";
29. import { auditRoutes } from "./routes/audit.js";
30. import { queueStatusRoutes } from "./routes/queue-status.js";
31. import { registerNotificationHandler } from "./queue/handlers/notification-handler.js";
32. import { registerAuditHandler } from "./queue/handlers/audit-handler.js";
33. 
34. const __dirname = path.dirname(fileURLToPath(import.meta.url));
35. 
36. const app = express();
37. 
38. // ── Initialize database ──
39. getDb();
40. seedDatabase();
41. 
42. // ── Register queue handlers ──
43. registerNotificationHandler();
44. registerAuditHandler();
45. 
46. // ── Middleware chain (ORDER MATTERS) ──
47. app.use(express.json());
48. app.use(rateLimiterMiddleware);
49. app.use(authMiddleware);
50. app.use(auditLoggerMiddleware);
51. 
52. // ── API Routes ──
53. app.use("/api/applications", applicationRoutes);
54. app.use("/api/decisions", decisionRoutes);
55. app.use("/api/notifications", notificationRoutes);
56. app.use("/api/audit", auditRoutes);
57. app.use("/api/queue", queueStatusRoutes);
58. 
59. // ── Health check (no auth required — placed before auth middleware in request flow) ──
60. app.get("/health", (_req, res) => {
61.   res.json({ status: "ok", timestamp: new Date().toISOString() });
62. });
63. 
64. // ── Serve frontend static files ──
65. const frontendDir = path.resolve(__dirname, "../../frontend");
66. app.use(express.static(frontendDir));
67. 
68. // ── SPA fallback — serve index.html for non-API routes ──
69. app.get("*", (_req, res) => {
70.   res.sendFile(path.join(frontendDir, "index.html"));
71. });
72. 
73. // ── Error handler (MUST be last) ──
74. app.use(errorHandler);
75. 
76. app.listen(config.port, () => {
77.   console.log(`Loan Workbench API listening on port ${config.port}`);
78.   console.log(`Database: ${config.dbPath}`);
79. });
80. 
81. export default app;
```

</details>


---

<sub>⏱️ 1m 7s</sub>

### 💬 Copilot

I’ve confirmed the current implementation already has some notification plumbing, but it also exposes the gaps the plan needs to address: no release flag for the feature, no source-backed rule enforcement in the save path, and a UI that’s still mostly raw toggles rather than a governed preference workflow.

---

<sub>⏱️ 1m 7s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "blockDelegatedWrites|loanState|404|notificationPreferences|pilot|feature flag|queueAudit|smsFallback|audit.write.failure|preference.save.failure|preference.read.failure|notification.sms.fallback",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\04-planning-workflows\\src",
  "output_mode": "content",
  "glob": "*.{ts,tsx}",
  "-n": true,
  "head_limit": 300
}
```

</details>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\unit\business-rules.test.ts:17:  loanState: "NY",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\unit\business-rules.test.ts:39:      loanState: "CA",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\unit\business-rules.test.ts:48:      loanState: "CA",
```


---

<sub>⏱️ 1m 7s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\audit-logger.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\audit-logger.ts (lines 1-220)

<details>
<summary>71 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Audit Logger Middleware
3. // ---------------------------------------------------------------------------
4. // Emits an `audit.requested` event for every mutating request (POST, PUT,
5. // PATCH, DELETE) that completes successfully.  The event is processed
6. // asynchronously by the queue's audit handler.
7. //
8. // Fine-grained audit entries (e.g. per-preference-field changes) are
9. // emitted by route handlers themselves; this middleware provides a
10. // baseline request-level audit log.
11. // ---------------------------------------------------------------------------
12. 
13. import type { Request, Response, NextFunction } from "express";
14. import { v4 as uuid } from "uuid";
15. import { broker } from "../queue/broker.js";
16. import type { AuditRequestedEvent } from "../queue/contracts.js";
17. import { featureFlags } from "../config/feature-flags.js";
18. import { createAuditEntry } from "../models/audit-repository.js";
19. 
20. const MUTATING_METHODS = new Set(["POST", "PUT", "PATCH", "DELETE"]);
21. 
22. export function auditLoggerMiddleware(
23.   req: Request,
24.   res: Response,
25.   next: NextFunction,
26. ): void {
27.   if (!MUTATING_METHODS.has(req.method)) {
28.     next();
29.     return;
30.   }
31. 
32.   // Capture the original end() to inject audit logging after response.
33.   const originalEnd = res.end.bind(res);
34. 
35.   // eslint-disable-next-line @typescript-eslint/no-explicit-any
36.   (res as any).end = function (...args: unknown[]) {
37.     // Only audit successful operations.
38.     if (res.statusCode >= 200 && res.statusCode < 400 && req.session) {
39.       const auditPayload = {
40.         action: `${req.method} ${req.path}`,
41.         actor: req.session.actor.id,
42.         delegatedFor: req.session.delegatedFor?.id,
43.         previousValue: undefined,
44.         newValue: { statusCode: res.statusCode },
45.         source: "audit-logger-middleware",
46.       };
47. 
48.       if (featureFlags.queueAudit) {
49.         // Route through the message queue for async persistence
50.         const event: AuditRequestedEvent = {
51.           eventId: uuid(),
52.           timestamp: new Date().toISOString(),
53.           source: "audit-logger-middleware",
54.           type: "audit.requested",
55.           payload: auditPayload,
56.         };
57.         broker.emit(event);
58.       } else {
59.         // Synchronous fallback — write directly to DB
60.         try {
61.           createAuditEntry(auditPayload);
62.         } catch (err) {
63.           console.error("[audit-logger] Failed to write audit entry:", err);
64.         }
65.       }
66.     }
67.     return originalEnd(...(args as Parameters<Response["end"]>));
68.   };
69. 
70.   next();
71. }
```

</details>


---

<sub>⏱️ 1m 7s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\audit.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\audit.ts (lines 1-220)

<details>
<summary>35 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Audit Routes
3. // ---------------------------------------------------------------------------
4. // Read-only access to the audit trail.  No mutations allowed via API.
5. // ---------------------------------------------------------------------------
6. 
7. import { Router } from "express";
8. import { requireRole } from "../middleware/auth.js";
9. import * as auditRepo from "../models/audit-repository.js";
10. 
11. export const auditRoutes = Router();
12. 
13. function firstParam(value: string | string[]): string {
14.   return Array.isArray(value) ? value[0] : value;
15. }
16. 
17. /** GET /api/audit — list recent audit entries. */
18. auditRoutes.get(
19.   "/",
20.   requireRole("underwriter", "analyst-manager", "compliance-reviewer"),
21.   (req, res) => {
22.     const limit = parseInt(req.query.limit as string, 10) || 100;
23.     const actor = req.query.actor as string | undefined;
24.     res.json(auditRepo.findAuditEntries({ actor, limit }));
25.   },
26. );
27. 
28. /** GET /api/audit/action/:action — filter by action type. */
29. auditRoutes.get(
30.   "/action/:action",
31.   requireRole("underwriter", "analyst-manager", "compliance-reviewer"),
32.   (req, res) => {
33.     res.json(auditRepo.findAuditEntriesByAction(firstParam(req.params.action)));
34.   },
35. );
```

</details>


---

<sub>⏱️ 1m 7s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\models\audit-repository.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\models\audit-repository.ts (lines 1-220)

<details>
<summary>94 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Audit Entry Repository
3. // ---------------------------------------------------------------------------
4. // Database operations for the audit trail.  Audit entries are immutable —
5. // there is no update or delete.
6. //
7. // IMPORTANT: The audit trail is append-only.  Never expose a DELETE or
8. // UPDATE endpoint for audit entries.  Compliance requires the full history.
9. // ---------------------------------------------------------------------------
10. 
11. import { v4 as uuid } from "uuid";
12. import { getDb } from "../db/connection.js";
13. import type { AuditEntry } from "./types.js";
14. 
15. const AUDIT_COLUMNS = `
16.   id,
17.   action,
18.   actor,
19.   delegated_for AS delegatedFor,
20.   timestamp,
21.   previous_value AS previousValue,
22.   new_value AS newValue,
23.   source
24. `;
25. 
26. export function createAuditEntry(data: {
27.   action: string;
28.   actor: string;
29.   delegatedFor?: string | null;
30.   previousValue?: unknown;
31.   newValue?: unknown;
32.   source: string;
33. }): AuditEntry {
34.   const db = getDb();
35.   const id = uuid();
36.   const now = new Date().toISOString();
37. 
38.   db.prepare(
39.     `INSERT INTO audit_entries (id, action, actor, delegated_for, timestamp, previous_value, new_value, source)
40.      VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
41.   ).run(
42.     id,
43.     data.action,
44.     data.actor,
45.     data.delegatedFor ?? null,
46.     now,
47.     data.previousValue != null ? JSON.stringify(data.previousValue) : null,
48.     data.newValue != null ? JSON.stringify(data.newValue) : null,
49.     data.source,
50.   );
51. 
52.   return {
53.     id,
54.     action: data.action,
55.     actor: data.actor,
56.     delegatedFor: data.delegatedFor ?? null,
57.     timestamp: now,
58.     previousValue: null,
59.     newValue: null,
60.     source: data.source,
61.   };
62. }
63. 
64. export function findAuditEntries(opts?: {
65.   actor?: string;
66.   limit?: number;
67. }): AuditEntry[] {
68.   const db = getDb();
69.   let sql = `SELECT ${AUDIT_COLUMNS} FROM audit_entries`;
70.   const params: unknown[] = [];
71. 
72.   if (opts?.actor) {
73.     sql += " WHERE actor = ?";
74.     params.push(opts.actor);
75.   }
76. 
77.   sql += " ORDER BY timestamp DESC";
78. 
79.   if (opts?.limit) {
80.     sql += " LIMIT ?";
81.     params.push(opts.limit);
82.   }
83. 
84.   return db.prepare(sql).all(...params) as AuditEntry[];
85. }
86. 
87. export function findAuditEntriesByAction(action: string): AuditEntry[] {
88.   const db = getDb();
89.   return db
90.     .prepare(
91.       `SELECT ${AUDIT_COLUMNS} FROM audit_entries WHERE action = ? ORDER BY timestamp DESC`,
92.     )
93.     .all(action) as AuditEntry[];
94. }
```

</details>


---

<sub>⏱️ 1m 7s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\loan-service.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\loan-service.ts (lines 1-260)

<details>
<summary>120 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Loan Service
3. // ---------------------------------------------------------------------------
4. // Orchestrates loan operations: creation, state transitions, and risk
5. // scoring.  Delegates persistence to the loan repository, rule validation
6. // to the rules layer, and event emission to the broker.
7. // ---------------------------------------------------------------------------
8. 
9. import { v4 as uuid } from "uuid";
10. import * as loanRepo from "../models/loan-repository.js";
11. import { assertTransition } from "../rules/state-machine.js";
12. import { validateLoanRules, canApprove } from "../rules/business-rules.js";
13. import { getMandatoryEvents } from "../rules/mandatory-events.js";
14. import { broker } from "../queue/broker.js";
15. import type {
16.   LoanApplication,
17.   SessionContext,
18.   ApplicationState,
19. } from "../models/types.js";
20. import type {
21.   LoanStateChangedEvent,
22.   NotificationRequestedEvent,
23. } from "../queue/contracts.js";
24. 
25. /**
26.  * Create a new loan application.
27.  * Validates business rules before persisting.
28.  */
29. export function createLoan(
30.   session: SessionContext,
31.   data: { borrowerName: string; amount: number; loanState: string },
32. ): LoanApplication {
33.   if (session.delegatedFor) {
34.     throw new Error("FORBIDDEN: Delegated sessions cannot create loans.");
35.   }
36. 
37.   // Build a partial loan to validate rules
38.   const draft = {
39.     ...data,
40.     loanState: data.loanState.toUpperCase(),
41.   } as LoanApplication;
42.   const violations = validateLoanRules(draft);
43.   if (violations.length > 0) {
44.     throw new Error(
45.       `VALIDATION: ${violations.map((v) => v.message).join("; ")}`,
46.     );
47.   }
48. 
49.   return loanRepo.createLoan({
50.     borrowerName: data.borrowerName,
51.     amount: data.amount,
52.     loanState: data.loanState,
53.     assignedUnderwriter: session.actor.id,
54.   });
55. }
56. 
57. /**
58.  * Transition a loan to a new state.
59.  * Enforces state machine rules, emits state-changed events,
60.  * and triggers mandatory notifications.
61.  */
62. export function transitionLoan(
63.   session: SessionContext,
64.   applicationId: string,
65.   newStatus: ApplicationState,
66. ): LoanApplication {
67.   if (session.delegatedFor) {
68.     throw new Error("FORBIDDEN: Delegated sessions cannot transition loans.");
69.   }
70. 
71.   const loan = loanRepo.findLoanById(applicationId);
72.   if (!loan) {
73.     throw new Error(`NOT_FOUND: Application '${applicationId}' not found.`);
74.   }
75. 
76.   // Enforce state machine
77.   assertTransition(loan.status, newStatus);
78. 
79.   const previousStatus = loan.status;
80.   const updated = loanRepo.updateLoanStatus(applicationId, newStatus);
81.   if (!updated) {
82.     throw new Error(`NOT_FOUND: Application '${applicationId}' not found.`);
83.   }
84. 
85.   // Emit state-changed event
86.   const stateEvent: LoanStateChangedEvent = {
87.     eventId: uuid(),
88.     timestamp: new Date().toISOString(),
89.     source: "loan-service",
90.     type: "loan.state-changed",
91.     payload: {
92.       applicationId,
93.       previousStatus,
94.       newStatus,
95.       changedBy: session.actor.id,
96.     },
97.   };
98.   broker.emit(stateEvent);
99. 
100.   // Emit mandatory notification events
101.   const mandatoryEvents = getMandatoryEvents(previousStatus, newStatus);
102.   for (const event of mandatoryEvents) {
103.     const notifEvent: NotificationRequestedEvent = {
104.       eventId: uuid(),
105.       timestamp: new Date().toISOString(),
106.       source: "loan-service",
107.       type: "notification.requested",
108.       payload: {
109.         userId: loan.assignedUnderwriter,
110.         event,
111.         subject: `Loan ${applicationId}: ${previousStatus} → ${newStatus}`,
112.         body: `Application ${applicationId} transitioned from ${previousStatus} to ${newStatus}.`,
113.         preferredChannel: "email",
114.       },
115.     };
116.     broker.emit(notifEvent);
117.   }
118. 
119.   return updated;
120. }
```

</details>


---

<sub>⏱️ 1m 15s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "x-delegated-for|delegated|store|useState|central store|preferences",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\04-planning-workflows\\src\\frontend\\src",
  "output_mode": "content",
  "glob": "*.ts",
  "-n": true,
  "head_limit": 300
}
```

</details>

<details>
<summary>13 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\main.ts:29:      case "preferences":
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\main.ts:30:        import("./pages/preferences.js").then((m) =>
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\pages\api-explorer.ts:42:  { method: "GET", path: "/api/notifications/preferences/:userId", label: "Get Preferences", body: false, param: "userId" },
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\pages\api-explorer.ts:45:    path: "/api/notifications/preferences",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\pages\preferences.ts:4:// Shows notification preferences for the current user and allows toggling.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\pages\preferences.ts:11:  container.innerHTML = `<p class="loading">Loading preferences...</p>`;
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\pages\preferences.ts:20:      <section class="preferences-page">
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\pages\preferences.ts:30:      prefList.innerHTML = `<p class="empty-state">No preferences configured. Defaults will be used.</p>`;
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\pages\preferences.ts:38:    container.innerHTML = `<p class="error">Failed to load preferences: ${(err as Error).message}</p>`;
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\api\types.ts:43:  delegatedFor: string | null;
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\api\client.ts:84:  return apiFetch(`/notifications/preferences/${encodeURIComponent(userId)}`);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\api\client.ts:93:  return apiFetch("/notifications/preferences", {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\components\app-shell.ts:22:        <a href="#preferences" class="nav-link" data-page="preferences">Preferences</a>
```

</details>


---

<sub>⏱️ 1m 15s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\components\app-shell.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\components\app-shell.ts (lines 1-260)

<details>
<summary>58 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // App Shell Component
3. // ---------------------------------------------------------------------------
4. // Renders the branded application layout: header with brand lockup,
5. // navigation bar, main content area, and footer.
6. // ---------------------------------------------------------------------------
7. 
8. export function renderAppShell(root: HTMLElement): void {
9.   root.innerHTML = `
10.     <header class="app-header">
11.       <a href="#dashboard" class="brand-lockup" aria-label="LocalM Tuts Examples">
12.         <img src="/brand/icon-mark-gradient.svg" alt="" class="brand-mark" width="35" height="35" />
13.         <div class="brand-wordmark">
14.           <span class="brand-primary">localm<span class="brand-tm">™</span></span>
15.           <span class="brand-tuts">TUTS</span>
16.         </div>
17.         <span class="brand-separator">|</span>
18.         <span class="brand-context">Examples</span>
19.       </a>
20.       <nav class="app-nav" id="main-nav">
21.         <a href="#dashboard" class="nav-link" data-page="dashboard">Dashboard</a>
22.         <a href="#preferences" class="nav-link" data-page="preferences">Preferences</a>
23.         <a href="#queue" class="nav-link" data-page="queue">Queue</a>
24.         <a href="#api" class="nav-link" data-page="api">API Explorer</a>
25.       </nav>
26.       <div class="user-info">
27.         <select id="user-select" class="user-select" aria-label="Switch user">
28.           <option value="u-1">Dana Chu (Underwriter)</option>
29.           <option value="u-2">Raj Patel (Analyst Manager)</option>
30.           <option value="u-3">Kim Nakamura (Compliance)</option>
31.         </select>
32.       </div>
33.     </header>
34.     <main id="main-content" class="main-content"></main>
35.     <footer class="app-footer">
36.       <span>&copy; ${new Date().getFullYear()} LocalM\u2122. All rights reserved.</span>
37.     </footer>
38.   `;
39. 
40.   // Active nav tracking
41.   const updateActiveNav = (): void => {
42.     const hash = window.location.hash.slice(1) || "dashboard";
43.     const page = hash.split("?")[0];
44.     root.querySelectorAll<HTMLAnchorElement>(".nav-link").forEach((link) => {
45.       link.classList.toggle("active", link.dataset.page === page);
46.     });
47.   };
48.   window.addEventListener("hashchange", updateActiveNav);
49.   updateActiveNav();
50. 
51.   // User switcher
52.   const select = root.querySelector<HTMLSelectElement>("#user-select");
53.   select?.addEventListener("change", async () => {
54.     const { setCurrentUser } = await import("../api/client.js");
55.     setCurrentUser(select.value);
56.     window.dispatchEvent(new HashChangeEvent("hashchange"));
57.   });
58. }
```

</details>


---

<sub>⏱️ 1m 15s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "pilot|404|feature flag|notification-pref:read|notification-pref:write|mandatory|fallback|audit",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\04-planning-workflows\\src\\backend\\src",
  "output_mode": "content",
  "glob": "*.ts",
  "-n": true,
  "head_limit": 300
}
```

</details>

<details>
<summary>103 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\notification-service.ts:10://   IF email is enabled for that event.  The fallback must NOT change the
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\audit-service.ts:4:// High-level audit API.  Provides convenience methods that emit events
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\audit-service.ts:5:// to the message queue (or write directly depending on feature flags).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\audit-service.ts:11:import { createAuditEntry } from "../models/audit-repository.js";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\audit-service.ts:16: * Write an audit entry for an action performed in a session context.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\audit-service.ts:18:export function auditAction(
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\audit-service.ts:39:      type: "audit.requested",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\decision-service.ts:33: *  - The decision is audited via the message queue.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\decision-service.ts:96:  // Emit audit event
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\decision-service.ts:97:  const auditEvent: AuditRequestedEvent = {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\decision-service.ts:101:    type: "audit.requested",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\decision-service.ts:110:  broker.emit(auditEvent);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\broker.ts:14://   handlers from running.  For critical operations (like audit writes),
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\db\seed.ts:36:    `INSERT OR IGNORE INTO audit_entries (id, action, actor, delegated_for, timestamp, previous_value, new_value, source)
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\loan-service.ts:13:import { getMandatoryEvents } from "../rules/mandatory-events.js";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\loan-service.ts:60: * and triggers mandatory notifications.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\loan-service.ts:100:  // Emit mandatory notification events
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\loan-service.ts:101:  const mandatoryEvents = getMandatoryEvents(previousStatus, newStatus);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\loan-service.ts:102:  for (const event of mandatoryEvents) {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\applications.ts:8:import { auditAction } from "../services/audit-service.js";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\applications.ts:42:      res.status(404).json({ error: "Application not found." });
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers\notification-handler.ts:8://   When the SMS provider is unavailable and the feature flag is enabled,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers\notification-handler.ts:10://   event.  The fallback does NOT change stored preferences — it is a
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers\notification-handler.ts:74:        `[notification-handler] Cannot deliver via ${channel} — provider unhealthy, no fallback`,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\contracts.ts:12://   4. Add an audit entry for the contract change
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\contracts.ts:42:/** Emitted when an audit entry must be persisted. */
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\contracts.ts:44:  type: "audit.requested";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers\audit-handler.ts:4:// Consumes `audit.requested` events from the broker and writes them to
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers\audit-handler.ts:5:// the database.  This decouples audit writes from request handlers,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers\audit-handler.ts:9://   If the audit write fails, the handler retries once.  If the retry
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers\audit-handler.ts:17:import { createAuditEntry } from "../../models/audit-repository.js";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers\audit-handler.ts:34:      "[audit-handler] First write attempt failed, retrying...",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers\audit-handler.ts:48:        "[audit-handler] CRITICAL: Audit write failed after retry",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers\audit-handler.ts:57:  broker.on("audit.requested", handleAuditRequested);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers\audit-handler.ts:58:  console.log("[audit-handler] Registered for audit.requested events");
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\app.ts:11://   4. auditLoggerMiddleware   — Log mutating requests (needs session)
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\app.ts:23:import { auditLoggerMiddleware } from "./middleware/audit-logger.js";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\app.ts:29:import { auditRoutes } from "./routes/audit.js";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\app.ts:32:import { registerAuditHandler } from "./queue/handlers/audit-handler.js";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\app.ts:50:app.use(auditLoggerMiddleware);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\app.ts:56:app.use("/api/audit", auditRoutes);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\app.ts:68:// ── SPA fallback — serve index.html for non-API routes ──
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\error-handler.ts:26:    res.status(404).json({ error: err.message });
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\audit-logger.ts:4:// Emits an `audit.requested` event for every mutating request (POST, PUT,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\audit-logger.ts:6:// asynchronously by the queue's audit handler.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\audit-logger.ts:8:// Fine-grained audit entries (e.g. per-preference-field changes) are
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\audit-logger.ts:10:// baseline request-level audit log.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\audit-logger.ts:18:import { createAuditEntry } from "../models/audit-repository.js";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\audit-logger.ts:22:export function auditLoggerMiddleware(
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\audit-logger.ts:32:  // Capture the original end() to inject audit logging after response.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\audit-logger.ts:37:    // Only audit successful operations.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\audit-logger.ts:39:      const auditPayload = {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\audit-logger.ts:45:        source: "audit-logger-middleware",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\audit-logger.ts:53:          source: "audit-logger-middleware",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\audit-logger.ts:54:          type: "audit.requested",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\audit-logger.ts:55:          payload: auditPayload,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\audit-logger.ts:59:        // Synchronous fallback — write directly to DB
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\audit-logger.ts:61:          createAuditEntry(auditPayload);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\audit-logger.ts:63:          console.error("[audit-logger] Failed to write audit entry:", err);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\mandatory-events.ts:5:// These are non-negotiable business requirements — skipping a mandatory
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\mandatory-events.ts:9:// for ALL mandatory events listed here.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\mandatory-events.ts:17: * Map of state transitions to mandatory notification events.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\mandatory-events.ts:18: * If a transition is not listed, no mandatory notifications are required.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\mandatory-events.ts:29: * Get the mandatory notification events for a given state transition.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\auth.ts:12://   Compliance reviewers can view notification preferences and audit logs
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\business-rules.ts:14://   These rules are gated behind the `californiaRules` feature flag.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\models\audit-repository.ts:4:// Database operations for the audit trail.  Audit entries are immutable —
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\models\audit-repository.ts:7:// IMPORTANT: The audit trail is append-only.  Never expose a DELETE or
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\models\audit-repository.ts:8:// UPDATE endpoint for audit entries.  Compliance requires the full history.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\models\audit-repository.ts:39:    `INSERT INTO audit_entries (id, action, actor, delegated_for, timestamp, previous_value, new_value, source)
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\models\audit-repository.ts:69:  let sql = `SELECT ${AUDIT_COLUMNS} FROM audit_entries`;
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\models\audit-repository.ts:91:      `SELECT ${AUDIT_COLUMNS} FROM audit_entries WHERE action = ? ORDER BY timestamp DESC`,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\audit.ts:4:// Read-only access to the audit trail.  No mutations allowed via API.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\audit.ts:9:import * as auditRepo from "../models/audit-repository.js";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\audit.ts:11:export const auditRoutes = Router();
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\audit.ts:17:/** GET /api/audit — list recent audit entries. */
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\audit.ts:18:auditRoutes.get(
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\audit.ts:24:    res.json(auditRepo.findAuditEntries({ actor, limit }));
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\audit.ts:28:/** GET /api/audit/action/:action — filter by action type. */
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\audit.ts:29:auditRoutes.get(
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\audit.ts:33:    res.json(auditRepo.findAuditEntriesByAction(firstParam(req.params.action)));
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\role-permissions.ts:22:  | "notification-pref:read"
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\role-permissions.ts:23:  | "notification-pref:write"
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\role-permissions.ts:24:  | "audit:read"
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\role-permissions.ts:34:    "notification-pref:read",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\role-permissions.ts:35:    "notification-pref:write",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\role-permissions.ts:36:    "audit:read",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\role-permissions.ts:44:    "notification-pref:read",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\role-permissions.ts:45:    "notification-pref:write",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\role-permissions.ts:46:    "audit:read",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\role-permissions.ts:51:    "notification-pref:read", // READ only — no write
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\role-permissions.ts:52:    "audit:read",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\notifications.ts:20:import { auditAction } from "../services/audit-service.js";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\notifications.ts:68:      if (!hasPermission(session.actor.role, "notification-pref:write")) {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\notifications.ts:92:      auditAction(
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\notifications.ts:140:      if (!hasPermission(session.actor.role, "notification-pref:write")) {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\notifications.ts:174:        auditAction(
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\notifications.ts:223:      if (!hasPermission(session.actor.role, "notification-pref:write")) {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\notifications.ts:257:        auditAction(
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\config\feature-flags.ts:4:// Runtime feature flags that control business behavior.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\config\feature-flags.ts:8:// and audit behavior.  When adding a new flag, update:
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\config\feature-flags.ts:20:  /** Enable SMS → email fallback when SMS provider is unavailable. */
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\config\feature-flags.ts:23:  /** Route audit writes through the message queue instead of synchronous DB writes. */
```

</details>


---

<sub>⏱️ 1m 15s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "metrics|Counter|Histogram|latency",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\04-planning-workflows\\src",
  "output_mode": "content",
  "glob": "*.ts",
  "-n": true,
  "head_limit": 200
}
```

</details>

```
No matches found.
```


---

<sub>⏱️ 1m 21s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\business-rules.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\business-rules.ts (lines 1-260)

<details>
<summary>83 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Business Rules
3. // ---------------------------------------------------------------------------
4. // Domain-specific validation rules.  These are checked by services BEFORE
5. // persisting changes.
6. //
7. // CALIFORNIA RULES — REGULATORY REQUIREMENT:
8. //   Loans in California (loan_state = "CA") have additional requirements:
9. //   - Minimum loan amount: $50,000
10. //   - Maximum loan amount: $5,000,000
11. //   - Mandatory 3-day cooling-off period between "review" → "underwriting"
12. //   - Additional disclosure document required before finalization
13. //
14. //   These rules are gated behind the `californiaRules` feature flag.
15. //   When disabled, California loans follow standard rules.
16. //
17. // AMOUNT THRESHOLDS:
18. //   - Loans over $1,000,000 require analyst-manager approval (not just underwriter)
19. //   - Loans over $2,500,000 require compliance-reviewer sign-off
20. // ---------------------------------------------------------------------------
21. 
22. import { featureFlags } from "../config/feature-flags.js";
23. import type { LoanApplication, UserRole } from "../models/types.js";
24. 
25. export interface RuleViolation {
26.   rule: string;
27.   message: string;
28. }
29. 
30. /**
31.  * Validate a loan application against all business rules.
32.  * Returns an empty array if all rules pass.
33.  */
34. export function validateLoanRules(loan: LoanApplication): RuleViolation[] {
35.   const violations: RuleViolation[] = [];
36. 
37.   // Standard rules
38.   if (loan.amount <= 0) {
39.     violations.push({
40.       rule: "positive-amount",
41.       message: "Loan amount must be positive.",
42.     });
43.   }
44. 
45.   // California-specific rules
46.   if (featureFlags.californiaRules && loan.loanState === "CA") {
47.     if (loan.amount < 50_000) {
48.       violations.push({
49.         rule: "ca-min-amount",
50.         message: "California loans must be at least $50,000.",
51.       });
52.     }
53.     if (loan.amount > 5_000_000) {
54.       violations.push({
55.         rule: "ca-max-amount",
56.         message: "California loans cannot exceed $5,000,000.",
57.       });
58.     }
59.   }
60. 
61.   return violations;
62. }
63. 
64. /**
65.  * Determine which roles are required to approve a loan at the given amount.
66.  */
67. export function requiredApprovalRoles(amount: number): UserRole[] {
68.   if (amount > 2_500_000) {
69.     return ["analyst-manager", "compliance-reviewer"];
70.   }
71.   if (amount > 1_000_000) {
72.     return ["analyst-manager"];
73.   }
74.   return ["underwriter"];
75. }
76. 
77. /**
78.  * Check if a role is authorized to approve a loan of the given amount.
79.  */
80. export function canApprove(role: UserRole, amount: number): boolean {
81.   const required = requiredApprovalRoles(amount);
82.   return required.includes(role);
83. }
```

</details>


---

<sub>⏱️ 1m 21s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\error-handler.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\error-handler.ts (lines 1-220)

<details>
<summary>36 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Centralized Error Handler
3. // ---------------------------------------------------------------------------
4. // Express error middleware — must be registered LAST in the middleware chain.
5. // Maps known error patterns to appropriate HTTP status codes.
6. // ---------------------------------------------------------------------------
7. 
8. import type { Request, Response, NextFunction } from "express";
9. 
10. export function errorHandler(
11.   err: Error,
12.   _req: Request,
13.   res: Response,
14.   _next: NextFunction,
15. ): void {
16.   // Map known error prefixes to HTTP status codes.
17.   if (err.message.startsWith("FORBIDDEN:")) {
18.     res.status(403).json({ error: err.message });
19.     return;
20.   }
21.   if (err.message.startsWith("INVALID_STATE:")) {
22.     res.status(409).json({ error: err.message });
23.     return;
24.   }
25.   if (err.message.startsWith("NOT_FOUND:")) {
26.     res.status(404).json({ error: err.message });
27.     return;
28.   }
29.   if (err.message.startsWith("VALIDATION:")) {
30.     res.status(400).json({ error: err.message });
31.     return;
32.   }
33. 
34.   console.error("[error-handler] Unhandled error:", err);
35.   res.status(500).json({ error: "Internal server error." });
36. }
```

</details>


---

<sub>⏱️ 1m 21s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\decision-service.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\decision-service.ts (lines 1-220)

<details>
<summary>158 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Decision Service
3. // ---------------------------------------------------------------------------
4. // Records underwriting decisions and triggers downstream notification
5. // delivery.  Decisions can only be recorded for applications in the
6. // "decision" state — the state-machine guard is enforced here.
7. // ---------------------------------------------------------------------------
8. 
9. import { v4 as uuid } from "uuid";
10. import { getDb } from "../db/connection.js";
11. import type {
12.   Decision,
13.   LoanApplication,
14.   SessionContext,
15. } from "../models/types.js";
16. import { findLoanById } from "../models/loan-repository.js";
17. import { canApprove } from "../rules/business-rules.js";
18. import { broker } from "../queue/broker.js";
19. import type {
20.   AuditRequestedEvent,
21.   NotificationRequestedEvent,
22. } from "../queue/contracts.js";
23. 
24. type DecisionRow = Decision & { conditions?: string | null };
25. 
26. /**
27.  * Record a decision against a loan application.
28.  *
29.  * Validation:
30.  *  - Application must be in "decision" state.
31.  *  - Only authorized roles can record decisions (based on loan amount).
32.  *  - Delegated sessions cannot record decisions.
33.  *  - The decision is audited via the message queue.
34.  */
35. export function recordDecision(
36.   session: SessionContext,
37.   applicationId: string,
38.   type: Decision["type"],
39.   rationale: string,
40.   conditions?: string[],
41. ): Decision {
42.   // Guard: delegated sessions cannot record decisions.
43.   if (session.delegatedFor) {
44.     throw new Error(
45.       "FORBIDDEN: Decisions cannot be recorded in delegated sessions.",
46.     );
47.   }
48. 
49.   const application = findLoanById(applicationId);
50.   if (!application) {
51.     throw new Error(`NOT_FOUND: Application '${applicationId}' not found.`);
52.   }
53. 
54.   // Guard: application state.
55.   if (application.status !== "decision") {
56.     throw new Error(
57.       `INVALID_STATE: Cannot record a decision for application in ` +
58.         `'${application.status}' state. Expected 'decision'.`,
59.     );
60.   }
61. 
62.   // Guard: role + amount check.
63.   if (!canApprove(session.actor.role, application.amount)) {
64.     throw new Error(
65.       `FORBIDDEN: Role '${session.actor.role}' cannot approve loans of $${application.amount.toLocaleString()}.`,
66.     );
67.   }
68. 
69.   const id = uuid();
70.   const now = new Date().toISOString();
71.   const decision: Decision = {
72.     id,
73.     applicationId,
74.     type,
75.     rationale,
76.     decidedBy: session.actor.id,
77.     decidedAt: now,
78.     conditions,
79.   };
80. 
81.   // Persist decision
82.   const db = getDb();
83.   db.prepare(
84.     `INSERT INTO decisions (id, application_id, type, rationale, decided_by, decided_at, conditions)
85.      VALUES (?, ?, ?, ?, ?, ?, ?)`,
86.   ).run(
87.     id,
88.     applicationId,
89.     type,
90.     rationale,
91.     session.actor.id,
92.     now,
93.     conditions ? JSON.stringify(conditions) : null,
94.   );
95. 
96.   // Emit audit event
97.   const auditEvent: AuditRequestedEvent = {
98.     eventId: uuid(),
99.     timestamp: now,
100.     source: "decision-service",
101.     type: "audit.requested",
102.     payload: {
103.       action: "decision.recorded",
104.       actor: session.actor.id,
105.       previousValue: undefined,
106.       newValue: decision,
107.       source: "decision-service",
108.     },
109.   };
110.   broker.emit(auditEvent);
111. 
112.   // Emit notification for the assigned underwriter
113.   const notifEvent: NotificationRequestedEvent = {
114.     eventId: uuid(),
115.     timestamp: now,
116.     source: "decision-service",
117.     type: "notification.requested",
118.     payload: {
119.       userId: application.assignedUnderwriter,
120.       event: type === "declined" ? "decline" : "approval",
121.       subject: `Decision recorded: ${type} for ${applicationId}`,
122.       body: `A ${type} decision has been recorded for application ${applicationId}. Rationale: ${rationale}`,
123.       preferredChannel: "email",
124.     },
125.   };
126.   broker.emit(notifEvent);
127. 
128.   return decision;
129. }
130. 
131. /**
132.  * Retrieve all decisions for a given application.
133.  */
134. export function getDecisionsForApplication(applicationId: string): Decision[] {
135.   const db = getDb();
136.   return db
137.     .prepare(
138.       `SELECT
139.         id,
140.         application_id AS applicationId,
141.         type,
142.         rationale,
143.         decided_by AS decidedBy,
144.         decided_at AS decidedAt,
145.         conditions
146.       FROM decisions
147.       WHERE application_id = ?
148.       ORDER BY decided_at DESC`,
149.     )
150.     .all(applicationId)
151.     .map((decision) => decision as DecisionRow)
152.     .map((decision) => ({
153.       ...decision,
154.       conditions: decision.conditions
155.         ? (JSON.parse(decision.conditions as string) as string[])
156.         : undefined,
157.     })) as Decision[];
158. }
```

</details>


---

<sub>⏱️ 1m 21s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\unit\notification-service.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\unit\notification-service.test.ts (lines 1-220)

<details>
<summary>16 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Notification Service Tests
3. // ---------------------------------------------------------------------------
4. 
5. import { describe, it, expect, vi, beforeEach } from "vitest";
6. 
7. // These tests verify the notification routing logic at the service level.
8. // Queue handler tests verify actual delivery behavior (fallback, etc.).
9. 
10. describe("Notification Service", () => {
11.   it("placeholder — notification service emits queue events", () => {
12.     // Integration tests for notification delivery live in the queue handler tests.
13.     // This file tests the service API contract.
14.     expect(true).toBe(true);
15.   });
16. });
```

</details>


---

<sub>⏱️ 1m 21s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\integration\decisions.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\integration\decisions.test.ts (lines 1-220)

<details>
<summary>15 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Decision Routes Integration Tests
3. // ---------------------------------------------------------------------------
4. 
5. import { describe, it, expect } from "vitest";
6. 
7. describe("Decision Routes (integration)", () => {
8.   it("placeholder — POST /api/decisions requires decision state", () => {
9.     expect(true).toBe(true);
10.   });
11. 
12.   it("placeholder — delegated sessions cannot record decisions", () => {
13.     expect(true).toBe(true);
14.   });
15. });
```

</details>


---

<sub>⏱️ 1m 28s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "notification|preference|audit|delegated|fallback|California|LEGAL-218",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\04-planning-workflows\\src\\backend\\tests",
  "output_mode": "files_with_matches",
  "glob": "*.ts",
  "head_limit": 200
}
```

</details>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\unit\notification-service.test.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\unit\business-rules.test.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\integration\decisions.test.ts
```


---

<sub>⏱️ 1m 28s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "preferences|notification|delegated|aria|helper text|rollback",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\04-planning-workflows\\src\\frontend",
  "output_mode": "files_with_matches",
  "glob": "*.ts",
  "head_limit": 200
}
```

</details>

```
No matches found.
```


---

<sub>⏱️ 3m 23s</sub>

### 💬 Copilot

I’ve got enough evidence to write the plan now, including a couple of important source conflicts: the bug report title conflicts with the spec on which event LEGAL-218 applies to, and the current audit path conflicts with the fail-closed NFR. I’m encoding those directly in the plan so implementation starts from the right canonical sources.

---

<sub>⏱️ 3m 23s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Add File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\04-planning-workflows\\docs\\notification-preferences-plan.md\n+# Notification Preferences Implementation Plan\n+\n+## 1. Summary\n+\n+Implement notification preferences as a pilot-gated, source-of-truth-backed feature spanning backend rules/services/routes, frontend state/UI, audit, and observability. The feature must let authorized users manage email/SMS per event type while preserving mandatory escalation delivery, delegated-session read-only behavior, California decline SMS restrictions (`LEGAL-218`), degraded-mode delivery fallback, and fail-closed audit semantics. Relevant architecture surfaces already exist in `src/backend/src/routes/notifications.ts`, `src/backend/src/services/audit-service.ts`, `src/backend/src/queue/handlers/*.ts`, `src/frontend/src/pages/preferences.ts`, and `src/frontend/src/components/notification-toggle.ts` (see `docs/architecture.md:10-32`, `src/backend/src/routes/notifications.ts:33-271`, `src/frontend/src/pages/preferences.ts:10-39`).\n+\n+### Canonical source hierarchy for this plan\n+\n+1. **Product spec + NFRs are canonical for feature behavior and quality bars** because this lesson explicitly asks for planning against those sources, and the product spec is the only source with FR/SC identifiers (`docs/planning-workflow-example.md:31-39`, `specs/product-spec-notification-preferences.md:66-193`, `specs/non-functional-requirements.md:9-110`).\n+2. **ADR-003 is canonical for frontend state ownership and optimistic-save behavior** (`docs/adr/ADR-003-frontend-state.md:14-31`).\n+3. **Architecture doc is canonical for affected layers and breaking-change surfaces** such as rules/services/routes/queue contracts and pilot-gated rollout expectations (`docs/architecture.md:39-58`).\n+4. **Existing source is canonical only for the current baseline**, not for desired behavior when it conflicts with the spec/NFRs. Example conflicts:\n+   - The current audit path is asynchronous or best-effort and does **not** fail closed (`src/backend/src/services/audit-service.ts:18-45`, `src/backend/src/queue/handlers/audit-handler.ts:8-13`, `src/backend/src/middleware/audit-logger.ts:59-64`) but NFR-2 requires writes to abort if audit is unavailable (`specs/non-functional-requirements.md:23-34`).\n+   - The bug report title says \"manual-review escalation SMS toggle\" but the body and FR-4 both describe **decline SMS** as the California-restricted case; this plan treats FR-4 and the bug body/expected behavior as canonical (`specs/bug-report.md:5-6`, `specs/bug-report.md:14-26`, `specs/product-spec-notification-preferences.md:105-119`).\n+\n+## 2. Source-backed confirmed requirements\n+\n+| ID | Confirmed requirement | Key sources | Current implementation impact |\n+| --- | --- | --- | --- |\n+| FR-1 | Support email and SMS preferences for `approval`, `decline`, `document-request`, and `manual-review-escalation`, persisted across sessions/devices. | `specs/product-spec-notification-preferences.md:68-79`, `:30-35`; `specs/feature-request.md:7-10` | Current repository and routes already model these events/channels, but the UI is a flat toggle list rather than a governed preference matrix (`src/backend/src/models/types.ts:37-45`, `src/backend/src/models/preference-repository.ts:31-77`, `src/frontend/src/pages/preferences.ts:19-36`). |\n+| FR-2 | Manual-review escalation is mandatory: users may change the secondary channel, but at least one channel must remain enabled; UI and API must both enforce this. | `specs/product-spec-notification-preferences.md:81-92` | No current route/rule enforcement exists in `notifications.ts`; current PUT handlers can disable all SMS or all email values blindly (`src/backend/src/routes/notifications.ts:45-271`). Mandatory notification emission already exists for workflow transitions and must remain compatible (`src/backend/src/rules/mandatory-events.ts:17-37`, `src/backend/src/services/loan-service.ts:100-117`). |\n+| FR-3 | Defaults are role-based and generated on first access without a backfill migration. | `specs/product-spec-notification-preferences.md:94-104`; `specs/non-functional-requirements.md:86-97` | Current preferences page just shows empty state when no rows exist; no effective-default synthesis is present (`src/frontend/src/pages/preferences.ts:29-31`, `src/backend/src/models/preference-repository.ts:31-45`). |\n+| FR-4 / LEGAL-218 | Decline SMS must remain disabled for California loans; rule keys off `loanState`, not borrower address; mixed portfolio context must explain conditional restrictions rather than blanket-disable all SMS. | `specs/product-spec-notification-preferences.md:105-119`, `:166-170`; `specs/feature-request.md:21-25`; `specs/bug-report.md:22-24`, `:42-45` | Current notification preference API does not accept or validate loan context; current UI has no restriction messaging (`src/backend/src/routes/notifications.ts:49-54`, `:75-100`; `src/frontend/src/components/notification-toggle.ts:15-41`). |\n+| FR-5 | When SMS provider is unavailable, delivery may fall back to email if email is enabled; stored preferences must not change; fallback must emit a separate metric. | `specs/product-spec-notification-preferences.md:120-130`; `specs/feature-request.md:23-24`; `specs/non-functional-requirements.md:65-74` | Runtime fallback behavior exists in the notification handler, but no metrics surface exists yet (`src/backend/src/queue/handlers/notification-handler.ts:7-12`, `:62-76`). |\n+| FR-6 | Every preference change must audit actor, timestamp, previous value, new value, source channel, and delegated-for user when applicable. | `specs/product-spec-notification-preferences.md:132-142` | Current route-level audit includes actor/delegatedFor/previous/new/source but timestamp is implicit inside the repository, and writes are not fail-closed (`src/backend/src/services/audit-service.ts:18-45`, `src/backend/src/models/audit-repository.ts:26-61`). |\n+| SC-1 | In `finalized` state, global preferences can still change, but the UI must explain that already queued notifications for that application are unaffected. | `specs/product-spec-notification-preferences.md:147-152` | Current page has no application-context messaging. Source state names include `finalized`, which aligns with this special condition (`src/backend/src/models/types.ts:10-17`). |\n+| SC-2 | Delegated sessions may view the delegate's preferences but may not modify them; the UI must indicate delegated mode; audit must record actor and delegated-for; optimistic UI must not show success on rejected delegated writes. | `specs/product-spec-notification-preferences.md:153-165`; `specs/bug-report.md:20-27`, `:47-64`; `docs/adr/ADR-003-frontend-state.md:24-31` | Backend session context already captures `delegatedFor`, and current write routes block delegated writes, but GET scoping and frontend delegated indicators/rollback behavior are incomplete (`src/backend/src/middleware/auth.ts:61-75`, `src/backend/src/routes/notifications.ts:59-65`, `:123-129`, `:206-212`, `src/frontend/src/components/notification-toggle.ts:29-41`). |\n+| SC-3 | Mixed-portfolio restrictions must be presented as conditional rules rather than blanket disabling controls. | `specs/product-spec-notification-preferences.md:166-170` | No current portfolio-aware UI or API metadata exists (`src/frontend/src/pages/preferences.ts:19-36`, `src/frontend/src/api/client.ts:83-97`). |\n+| ADR-003 | Persisted preferences belong in the central client store, not component-local state; optimistic updates require store rollback on server rejection. | `docs/adr/ADR-003-frontend-state.md:14-31`, `:33-37`; `specs/product-spec-notification-preferences.md:179-180` | Current UI uses local DOM state per checkbox and direct API calls, not a central store (`src/frontend/src/components/notification-toggle.ts:18-44`). |\n+| NFR-2 | Reads must tolerate provider degradation, but preference writes must **fail closed** if audit logging is unavailable. | `specs/non-functional-requirements.md:21-34` | Current audit middleware and queue handler tolerate failures instead of rejecting writes, which is explicitly non-compliant (`src/backend/src/middleware/audit-logger.ts:37-65`, `src/backend/src/queue/handlers/audit-handler.ts:8-13`, `:23-52`). |\n+| NFR-3 | Only authenticated internal users may access preferences; delegated sessions must be explicit in audit logs; sensitive SMS destination data must stay out of logs/analytics. | `specs/non-functional-requirements.md:38-47` | Auth exists and delegated context is propagated, but the plan should keep logs/analytics limited to preference state and identifiers, not phone data (`src/backend/src/middleware/auth.ts:38-75`, `src/backend/src/models/types.ts:51-57`). |\n+| NFR-4 | Controls must be keyboard-reachable and screen-reader labeled; disabled mandatory/legal controls need persistent text; save status needs ARIA live announcement. | `specs/non-functional-requirements.md:50-60`; `specs/product-spec-notification-preferences.md:176-180` | Current checkbox UI lacks helper text, group semantics, and save-status announcements (`src/frontend/src/components/notification-toggle.ts:18-26`, `src/frontend/src/pages/preferences.ts:19-38`). |\n+| NFR-5 | Emit metrics for read/save failures, audit write failures, fallback invocations, and save latency; distinguish validation failures from downstream failures. | `specs/non-functional-requirements.md:63-80` | No metrics implementation is present in the current source (`src/backend/src`, search results for metrics were empty). |\n+| NFR-6 | Ship behind a release flag; non-pilot users must get 404, not 403; defaults on first access are expected and not a data bug. | `specs/non-functional-requirements.md:84-97`; `docs/architecture.md:43-47` | Existing feature flags do not include a notification-preferences pilot flag, and current routes are always mounted (`src/backend/src/config/feature-flags.ts:16-25`, `src/backend/src/app.ts:52-57`). |\n+| NFR-7 | Retain audit records for 24 months; mandatory escalation delivery rules must be testable and documented; compliance review must show effective preference state including defaults. | `specs/non-functional-requirements.md:101-110` | Audit repository is append-only, which aligns with retention expectations, but the effective-default/read-only reviewer view still needs design and implementation (`src/backend/src/models/audit-repository.ts:1-9`, `src/backend/src/routes/audit.ts:17-34`). |\n+\n+## 3. Open questions with file references\n+\n+1. **Should compliance reviewers access audit history from the same settings page or a separate audit viewer?** The product spec leaves this open, while the codebase already has a separate audit route that could be linked instead of embedded.  \n+   Sources: `specs/product-spec-notification-preferences.md:187-193`, `src/backend/src/routes/audit.ts:17-34`.\n+\n+2. **Should mixed-portfolio restrictions render as a summary banner, per-row indicators, or both?** The product spec explicitly asks this, and the current frontend has no portfolio-aware model yet.  \n+   Sources: `specs/product-spec-notification-preferences.md:166-170`, `:187-193`, `src/frontend/src/pages/preferences.ts:19-36`.\n+\n+3. **What is the authoritative read-scope rule for non-delegated underwriters and analyst managers?** The product spec clearly defines self-edit and delegated inspection, but the current GET endpoint accepts any `userId` for any allowed role.  \n+   Sources: `specs/product-spec-notification-preferences.md:48-62`, `:153-160`, `src/backend/src/routes/notifications.ts:33-43`.\n+\n+4. **How should loan context reach the preference API for FR-4/SC-3 validation?** The current save payload contains only `userId`, `event`, `channel`, and `enabled`, yet the California rule depends on `loanState`, and the bug report already calls out this gap as a likely root cause.  \n+   Sources: `src/backend/src/routes/notifications.ts:49-54`, `:75-100`, `src/frontend/src/api/client.ts:87-97`, `specs/bug-report.md:49-56`, `:60-63`.\n+\n+5. **How should fail-closed auditability work when `queueAudit` is enabled?** The NFR requires rejecting the save before success is reported, but the current queue model emits after persistence and does not roll the write back on handler failure.  \n+   Sources: `specs/non-functional-requirements.md:23-34`, `src/backend/src/services/audit-service.ts:34-45`, `src/backend/src/queue/handlers/audit-handler.ts:8-13`.\n+\n+## 4. Inferred implementation choices (not confirmed requirements)\n+\n+These are recommended plan assumptions based on source structure and architecture rules, but they are **not** directly mandated by the specs.\n+\n+1. **Add a dedicated pilot flag for notification preferences** instead of overloading unrelated flags like `smsFallback` or `californiaRules`, because NFR-6 requires release gating and the current feature-flag surface does not model it (`specs/non-functional-requirements.md:84-95`, `src/backend/src/config/feature-flags.ts:16-25`).\n+\n+2. **Move preference validation into a dedicated rules/service layer** so routes remain orchestration-only, matching the architecture rule that business rules live under `src/backend/src/rules/` and services handle orchestration/I/O (`docs/architecture.md:22-25`, `specs/feature-request.md:31-34`).\n+\n+3. **Return an \"effective preferences\" response model** that includes synthesized defaults, disabled reasons, mandatory-event metadata, delegated-session mode, and contextual restriction explanations. This best fits FR-3, FR-4, SC-2, SC-3, and NFR-4 without forcing the frontend to reconstruct business rules (`specs/product-spec-notification-preferences.md:94-119`, `:153-180`).\n+\n+4. **Use a central client store for the preference matrix and save lifecycle** rather than direct DOM mutation, to comply with ADR-003 and support rollback, ARIA status, and contextual banners (`docs/adr/ADR-003-frontend-state.md:16-31`, `src/frontend/src/components/notification-toggle.ts:18-44`).\n+\n+5. **Prefer a transactional or preflight audit-write strategy for preference saves** so the main write cannot succeed unless auditability is guaranteed. This is the clearest way to satisfy NFR-2 given the current asynchronous audit path. (`specs/non-functional-requirements.md:23-34`, `src/backend/src/services/audit-service.ts:18-45`).\n+\n+## 5. Constraints and special conditions\n+\n+- **Delegated sessions are read-only for writes**: delegated users may inspect but not save another user's preferences, and the UI must make that mode obvious (`specs/product-spec-notification-preferences.md:153-160`, `src/backend/src/middleware/auth.ts:63-72`).\n+\n+- **`LEGAL-218` applies to California decline SMS, not manual-review escalation SMS**: use `loanState` as the jurisdiction source, show persistent explanation text, and present multi-state restrictions conditionally rather than globally (`specs/product-spec-notification-preferences.md:105-119`, `:166-170`).\n+\n+- **Mandatory-event delivery must stay intact**: manual-review escalation may not be reduced to zero channels, and existing workflow-triggered mandatory-event emission in `loan-service.ts` / `mandatory-events.ts` must continue to produce deliverable events (`specs/product-spec-notification-preferences.md:81-92`, `src/backend/src/rules/mandatory-events.ts:17-37`, `src/backend/src/services/loan-service.ts:100-117`).\n+\n+- **Audit must fail closed for writes**: do not treat audit as fire-and-forget for preference saves. A read succeeding during audit trouble is a **false positive** and not a bug; a successful-looking write without an audit trail is a **hard negative** and a real bug (`specs/non-functional-requirements.md:23-34`).\n+\n+- **Degraded-mode fallback is runtime delivery logic, not preference mutation**: receiving email during SMS outage is a **false positive** for \"bad preferences\" if stored SMS is still enabled; metrics must capture fallback separately (`specs/product-spec-notification-preferences.md:120-130`, `src/backend/src/queue/handlers/notification-handler.ts:62-76`).\n+\n+- **Pilot gating must hide the feature with 404 for non-pilot users**: returning 403 would leak feature existence and is a **hard negative** against NFR-6 (`specs/non-functional-requirements.md:84-95`).\n+\n+- **Accessibility constraints are explicit**: disabled controls need persistent helper text, not just a tooltip, and save outcomes need ARIA live messaging (`specs/non-functional-requirements.md:50-60`, `specs/product-spec-notification-preferences.md:176-180`).\n+\n+- **Queued-notification caveat for finalized applications**: preference changes remain global, but the UI must say they do not affect notifications already queued for that finalized application (`specs/product-spec-notification-preferences.md:147-152`).\n+\n+## 6. Numbered tasks with acceptance criteria and source references\n+\n+1. **Define and gate the feature entry points**\n+   - Scope: introduce a notification-preferences pilot flag, guard backend endpoints and frontend navigation/page loading, and return 404 for non-pilot users.\n+   - Acceptance criteria:\n+     - Non-pilot users receive 404, not 403, for notification-preference routes/pages.\n+     - Pilot users see the feature without changing unrelated app behavior.\n+     - Rollout notes include observability and fallback expectations.\n+   - Sources: NFR-6 (`specs/non-functional-requirements.md:84-97`), architecture rule on pilot-gated features (`docs/architecture.md:43-47`), current flag surface (`src/backend/src/config/feature-flags.ts:16-25`).\n+\n+2. **Introduce backend preference-domain logic for effective defaults and validation**\n+   - Scope: add/centralize rules for role-based defaults, mandatory-event zero-channel protection, California decline SMS restriction, delegated-session/owner checks, and compliance reviewer read-only semantics.\n+   - Acceptance criteria:\n+     - First access returns effective defaults without requiring seeded rows or migration.\n+     - Disabling both channels for `manual-review-escalation` is rejected in both granular and bulk-save flows.\n+     - Decline SMS rejects for California context with an explicit reason tied to `loanState`.\n+     - Delegated sessions and compliance reviewers cannot write preferences.\n+   - Sources: FR-2/3/4 (`specs/product-spec-notification-preferences.md:81-119`), SC-2 (`:153-165`), NFR-6 (`specs/non-functional-requirements.md:86-97`), current route gaps (`src/backend/src/routes/notifications.ts:45-271`).\n+\n+3. **Refactor notification preference API routes/services around the rules layer**\n+   - Scope: keep routes thin, return effective preferences plus disabled/helper metadata, and ensure GET/PUT semantics reflect the agreed read/write scope.\n+   - Acceptance criteria:\n+     - GET returns effective preference state, including defaults and restriction explanations.\n+     - PUT rejects invalid saves before persistence and returns enough structured error information for UI rollback.\n+     - API surfaces identify delegated-session mode and restriction reasons without exposing sensitive phone data.\n+   - Sources: architecture layering (`docs/architecture.md:22-25`, `:53-58`), ADR-003 (`docs/adr/ADR-003-frontend-state.md:24-31`), NFR-3 (`specs/non-functional-requirements.md:38-47`), current route/client shape (`src/backend/src/routes/notifications.ts:33-271`, `src/frontend/src/api/client.ts:83-97`).\n+\n+4. **Make preference saves fail closed on auditability**\n+   - Scope: redesign preference-save flow so audit failure prevents a successful mutation response; ensure audit entries capture actor, delegated-for, previous/new values, source, and timestamp.\n+   - Acceptance criteria:\n+     - A preference save cannot return success if the audit path is unavailable.\n+     - Audit records contain actor, delegated-for, previous/new values, source, and timestamp for every successful save.\n+     - Validation failures remain 4xx and audit/provider failures are distinguishable for logging/metrics.\n+   - Sources: FR-6 (`specs/product-spec-notification-preferences.md:132-142`), NFR-2/NFR-5/NFR-7 (`specs/non-functional-requirements.md:21-34`, `:63-80`, `:101-107`), current conflicting audit path (`src/backend/src/services/audit-service.ts:18-45`, `src/backend/src/queue/handlers/audit-handler.ts:8-13`, `src/backend/src/middleware/audit-logger.ts:37-65`).\n+\n+5. **Preserve mandatory-event delivery and degraded-mode fallback behavior**\n+   - Scope: ensure preference validation and delivery logic work together so mandatory escalation remains deliverable and SMS outages fall back to email without rewriting stored preferences.\n+   - Acceptance criteria:\n+     - Workflow transitions that require `manual-review-escalation` continue to emit the event.\n+     - Preference state never mutates because of runtime SMS fallback.\n+     - Fallback invocations emit a dedicated metric and are distinguishable from preference-save errors.\n+   - Sources: FR-2/FR-5 (`specs/product-spec-notification-preferences.md:81-92`, `:120-130`), NFR-5 (`specs/non-functional-requirements.md:63-80`), current mandatory/fallback surfaces (`src/backend/src/rules/mandatory-events.ts:17-37`, `src/backend/src/services/loan-service.ts:100-117`, `src/backend/src/queue/handlers/notification-handler.ts:33-77`).\n+\n+6. **Rebuild the frontend preferences experience around central state and explicit UX constraints**\n+   - Scope: replace direct-toggle local mutation with a store-backed matrix page that supports optimistic rollback, delegated banners, persistent helper text, finalized-state messaging, and ARIA live announcements.\n+   - Acceptance criteria:\n+     - Persisted preference state lives in the central client store, not component-local state.\n+     - Delegated mode is visually obvious and save actions are disabled or blocked before request.\n+     - Mandatory/legal restriction explanations are persistently visible.\n+     - Save success/failure is announced accessibly, and optimistic changes roll back correctly on server rejection.\n+     - Finalized application context warns that queued notifications are unaffected.\n+   - Sources: ADR-003 (`docs/adr/ADR-003-frontend-state.md:16-31`), SC-1/SC-2/SC-3 (`specs/product-spec-notification-preferences.md:147-180`), NFR-4 (`specs/non-functional-requirements.md:50-60`), current simplistic UI (`src/frontend/src/pages/preferences.ts:10-39`, `src/frontend/src/components/notification-toggle.ts:18-44`).\n+\n+7. **Add compliance/audit viewing behavior for effective preferences**\n+   - Scope: expose read-only effective preferences for compliance reviewers and resolve whether audit history is embedded or linked.\n+   - Acceptance criteria:\n+     - Compliance reviewers can inspect effective preferences including defaults but cannot modify operational settings.\n+     - The chosen audit-view pattern is documented and consistent with existing audit routes.\n+     - Audit retention assumptions remain compatible with the append-only repository.\n+   - Sources: product roles + open question (`specs/product-spec-notification-preferences.md:59-63`, `:187-193`), NFR-7 (`specs/non-functional-requirements.md:101-107`), current audit route/repository (`src/backend/src/routes/audit.ts:17-34`, `src/backend/src/models/audit-repository.ts:1-9`).\n+\n+8. **Close the testing and observability gaps**\n+   - Scope: add backend/frontend tests and telemetry for validation, audit failure, rollout gating, delegated behavior, fallback, and accessibility.\n+   - Acceptance criteria:\n+     - Unit/integration coverage exists for all hard negatives and false positives listed below.\n+     - Metrics exist for read/save failure, audit write failure, fallback, and save latency.\n+     - Logs distinguish validation issues from downstream failures without leaking sensitive SMS destination data.\n+   - Sources: NFR-3/NFR-5 (`specs/non-functional-requirements.md:38-47`, `:63-80`), lesson expectations (`docs/planning-workflow-example.md:33-39`, `:55-60`), current sparse tests (`src/backend/tests/unit/notification-service.test.ts:10-15`, `src/backend/tests/integration/decisions.test.ts:7-14`).\n+\n+## 7. Validation steps\n+\n+1. **Defaults and first access**\n+   - Verify a pilot underwriter with no stored rows receives FR-3 defaults on first load without migration.\n+   - Confirm compliance reviewer sees effective read-only state, including defaults.  \n+   Sources: FR-3, NFR-6, NFR-7 (`specs/product-spec-notification-preferences.md:94-104`, `specs/non-functional-requirements.md:86-107`).\n+\n+2. **Mandatory-event hard negative / false positive**\n+   - Hard negative: attempt to disable both channels for `manual-review-escalation`; API and UI must reject it.\n+   - False positive: disable only SMS while email remains enabled; this must succeed.  \n+   Sources: FR-2 (`specs/product-spec-notification-preferences.md:81-92`).\n+\n+3. **Delegated-session hard negative**\n+   - In delegated mode, verify preferences are viewable but save is blocked and no success toast/state commit survives.\n+   - Confirm audit records include both actor and delegated-for for allowed reads/surfaced operations.  \n+   Sources: SC-2, ADR-003, bug report (`specs/product-spec-notification-preferences.md:153-165`, `docs/adr/ADR-003-frontend-state.md:24-31`, `specs/bug-report.md:20-27`).\n+\n+4. **California restriction / LEGAL-218**\n+   - Hard negative: attempt to enable decline SMS for a California loan context; control must be disabled or save rejected with persistent explanation.\n+   - Confirm the rule keys off `loanState`, not borrower address.\n+   - In mixed-portfolio context, verify restrictions render conditionally rather than blanket-disabling all SMS.  \n+   Sources: FR-4, SC-3 (`specs/product-spec-notification-preferences.md:105-119`, `:166-170`).\n+\n+5. **Fail-closed audit behavior**\n+   - Hard negative: simulate audit unavailability and confirm preference save fails without persisting the new preference.\n+   - False positive: reads should still succeed during the same outage.  \n+   Sources: NFR-2 (`specs/non-functional-requirements.md:21-34`).\n+\n+6. **Degraded-mode fallback**\n+   - False positive: simulate SMS outage with email enabled and confirm delivery falls back to email without mutating stored preferences.\n+   - Verify `notification.sms.fallback` metric increments separately.  \n+   Sources: FR-5, NFR-5 (`specs/product-spec-notification-preferences.md:120-130`, `specs/non-functional-requirements.md:65-74`).\n+\n+7. **Pilot gating**\n+   - Hard negative: a non-pilot user must see 404, not 403, for backend endpoints and the UI entry point.  \n+   Sources: NFR-6 (`specs/non-functional-requirements.md:86-95`).\n+\n+8. **Accessibility and finalized-state messaging**\n+   - Validate keyboard navigation, screen-reader labels, persistent helper text, and ARIA live status updates.\n+   - In finalized context, confirm the UI warns that already queued notifications are unaffected.  \n+   Sources: SC-1, NFR-4 (`specs/product-spec-notification-preferences.md:147-180`, `specs/non-functional-requirements.md:50-60`).\n+\n+## 8. Risks and dependencies\n+\n+- **Audit architecture risk**: the current queue-based audit flow is fundamentally at odds with fail-closed preference saves. Resolving this may require a synchronous write path, a transactional outbox, or another design that guarantees auditability before success is returned (`src/backend/src/services/audit-service.ts:18-45`, `src/backend/src/queue/handlers/audit-handler.ts:8-13`).\n+\n+- **Frontend state dependency**: the current preferences UI is not built on a central store, so ADR-003 compliance is a non-trivial refactor rather than a small toggle patch (`src/frontend/src/components/notification-toggle.ts:18-44`, `docs/adr/ADR-003-frontend-state.md:16-31`).\n+\n+- **API contract dependency**: FR-4 and SC-3 need contextual restriction data, but current client/server payloads do not carry loan or portfolio context (`src/frontend/src/api/client.ts:83-97`, `src/backend/src/routes/notifications.ts:49-54`).\n+\n+- **Telemetry gap**: NFR-5 calls for metrics, but no metrics layer appears in the current source. Implementation may need a new observability abstraction or integration point.\n+\n+- **Read-scope ambiguity**: the desired read behavior for non-delegated internal roles is not fully specified and should be resolved before implementation to avoid shipping an over-broad read surface.\n+\n+- **Bug-report wording conflict**: if the team uses the bug title instead of FR-4/body details, they could incorrectly apply `LEGAL-218` to manual-review escalation SMS instead of decline SMS. The plan should keep FR-4 as canonical.\n*** End Patch\n"
```

</details>

```
Added 1 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\notification-preferences-plan.md
```


---

<sub>⏱️ 3m 30s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\notification-preferences-plan.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\notification-preferences-plan.md (lines 1-260)

<details>
<summary>123 lines</summary>

```
1. # Notification Preferences Implementation Plan
2. 
3. ## 1. Summary
4. 
5. Implement notification preferences as a pilot-gated, source-of-truth-backed feature spanning backend rules/services/routes, frontend state/UI, audit, and observability. The feature must let authorized users manage email/SMS per event type while preserving mandatory escalation delivery, delegated-session read-only behavior, California decline SMS restrictions (`LEGAL-218`), degraded-mode delivery fallback, and fail-closed audit semantics. Relevant architecture surfaces already exist in `src/backend/src/routes/notifications.ts`, `src/backend/src/services/audit-service.ts`, `src/backend/src/queue/handlers/*.ts`, `src/frontend/src/pages/preferences.ts`, and `src/frontend/src/components/notification-toggle.ts` (see `docs/architecture.md:10-32`, `src/backend/src/routes/notifications.ts:33-271`, `src/frontend/src/pages/preferences.ts:10-39`).
6. 
7. ### Canonical source hierarchy for this plan
8. 
9. 1. **Product spec + NFRs are canonical for feature behavior and quality bars** because this lesson explicitly asks for planning against those sources, and the product spec is the only source with FR/SC identifiers (`docs/planning-workflow-example.md:31-39`, `specs/product-spec-notification-preferences.md:66-193`, `specs/non-functional-requirements.md:9-110`).
10. 2. **ADR-003 is canonical for frontend state ownership and optimistic-save behavior** (`docs/adr/ADR-003-frontend-state.md:14-31`).
11. 3. **Architecture doc is canonical for affected layers and breaking-change surfaces** such as rules/services/routes/queue contracts and pilot-gated rollout expectations (`docs/architecture.md:39-58`).
12. 4. **Existing source is canonical only for the current baseline**, not for desired behavior when it conflicts with the spec/NFRs. Example conflicts:
13.    - The current audit path is asynchronous or best-effort and does **not** fail closed (`src/backend/src/services/audit-service.ts:18-45`, `src/backend/src/queue/handlers/audit-handler.ts:8-13`, `src/backend/src/middleware/audit-logger.ts:59-64`) but NFR-2 requires writes to abort if audit is unavailable (`specs/non-functional-requirements.md:23-34`).
14.    - The bug report title says "manual-review escalation SMS toggle" but the body and FR-4 both describe **decline SMS** as the California-restricted case; this plan treats FR-4 and the bug body/expected behavior as canonical (`specs/bug-report.md:5-6`, `specs/bug-report.md:14-26`, `specs/product-spec-notification-preferences.md:105-119`).
15. 
16. ## 2. Source-backed confirmed requirements
17. 
18. | ID | Confirmed requirement | Key sources | Current implementation impact |
19. | --- | --- | --- | --- |
20. | FR-1 | Support email and SMS preferences for `approval`, `decline`, `document-request`, and `manual-review-escalation`, persisted across sessions/devices. | `specs/product-spec-notification-preferences.md:68-79`, `:30-35`; `specs/feature-request.md:7-10` | Current repository and routes already model these events/channels, but the UI is a flat toggle list rather than a governed preference matrix (`src/backend/src/models/types.ts:37-45`, `src/backend/src/models/preference-repository.ts:31-77`, `src/frontend/src/pages/preferences.ts:19-36`). |
21. | FR-2 | Manual-review escalation is mandatory: users may change the secondary channel, but at least one channel must remain enabled; UI and API must both enforce this. | `specs/product-spec-notification-preferences.md:81-92` | No current route/rule enforcement exists in `notifications.ts`; current PUT handlers can disable all SMS or all email values blindly (`src/backend/src/routes/notifications.ts:45-271`). Mandatory notification emission already exists for workflow transitions and must remain compatible (`src/backend/src/rules/mandatory-events.ts:17-37`, `src/backend/src/services/loan-service.ts:100-117`). |
22. | FR-3 | Defaults are role-based and generated on first access without a backfill migration. | `specs/product-spec-notification-preferences.md:94-104`; `specs/non-functional-requirements.md:86-97` | Current preferences page just shows empty state when no rows exist; no effective-default synthesis is present (`src/frontend/src/pages/preferences.ts:29-31`, `src/backend/src/models/preference-repository.ts:31-45`). |
23. | FR-4 / LEGAL-218 | Decline SMS must remain disabled for California loans; rule keys off `loanState`, not borrower address; mixed portfolio context must explain conditional restrictions rather than blanket-disable all SMS. | `specs/product-spec-notification-preferences.md:105-119`, `:166-170`; `specs/feature-request.md:21-25`; `specs/bug-report.md:22-24`, `:42-45` | Current notification preference API does not accept or validate loan context; current UI has no restriction messaging (`src/backend/src/routes/notifications.ts:49-54`, `:75-100`; `src/frontend/src/components/notification-toggle.ts:15-41`). |
24. | FR-5 | When SMS provider is unavailable, delivery may fall back to email if email is enabled; stored preferences must not change; fallback must emit a separate metric. | `specs/product-spec-notification-preferences.md:120-130`; `specs/feature-request.md:23-24`; `specs/non-functional-requirements.md:65-74` | Runtime fallback behavior exists in the notification handler, but no metrics surface exists yet (`src/backend/src/queue/handlers/notification-handler.ts:7-12`, `:62-76`). |
25. | FR-6 | Every preference change must audit actor, timestamp, previous value, new value, source channel, and delegated-for user when applicable. | `specs/product-spec-notification-preferences.md:132-142` | Current route-level audit includes actor/delegatedFor/previous/new/source but timestamp is implicit inside the repository, and writes are not fail-closed (`src/backend/src/services/audit-service.ts:18-45`, `src/backend/src/models/audit-repository.ts:26-61`). |
26. | SC-1 | In `finalized` state, global preferences can still change, but the UI must explain that already queued notifications for that application are unaffected. | `specs/product-spec-notification-preferences.md:147-152` | Current page has no application-context messaging. Source state names include `finalized`, which aligns with this special condition (`src/backend/src/models/types.ts:10-17`). |
27. | SC-2 | Delegated sessions may view the delegate's preferences but may not modify them; the UI must indicate delegated mode; audit must record actor and delegated-for; optimistic UI must not show success on rejected delegated writes. | `specs/product-spec-notification-preferences.md:153-165`; `specs/bug-report.md:20-27`, `:47-64`; `docs/adr/ADR-003-frontend-state.md:24-31` | Backend session context already captures `delegatedFor`, and current write routes block delegated writes, but GET scoping and frontend delegated indicators/rollback behavior are incomplete (`src/backend/src/middleware/auth.ts:61-75`, `src/backend/src/routes/notifications.ts:59-65`, `:123-129`, `:206-212`, `src/frontend/src/components/notification-toggle.ts:29-41`). |
28. | SC-3 | Mixed-portfolio restrictions must be presented as conditional rules rather than blanket disabling controls. | `specs/product-spec-notification-preferences.md:166-170` | No current portfolio-aware UI or API metadata exists (`src/frontend/src/pages/preferences.ts:19-36`, `src/frontend/src/api/client.ts:83-97`). |
29. | ADR-003 | Persisted preferences belong in the central client store, not component-local state; optimistic updates require store rollback on server rejection. | `docs/adr/ADR-003-frontend-state.md:14-31`, `:33-37`; `specs/product-spec-notification-preferences.md:179-180` | Current UI uses local DOM state per checkbox and direct API calls, not a central store (`src/frontend/src/components/notification-toggle.ts:18-44`). |
30. | NFR-2 | Reads must tolerate provider degradation, but preference writes must **fail closed** if audit logging is unavailable. | `specs/non-functional-requirements.md:21-34` | Current audit middleware and queue handler tolerate failures instead of rejecting writes, which is explicitly non-compliant (`src/backend/src/middleware/audit-logger.ts:37-65`, `src/backend/src/queue/handlers/audit-handler.ts:8-13`, `:23-52`). |
31. | NFR-3 | Only authenticated internal users may access preferences; delegated sessions must be explicit in audit logs; sensitive SMS destination data must stay out of logs/analytics. | `specs/non-functional-requirements.md:38-47` | Auth exists and delegated context is propagated, but the plan should keep logs/analytics limited to preference state and identifiers, not phone data (`src/backend/src/middleware/auth.ts:38-75`, `src/backend/src/models/types.ts:51-57`). |
32. | NFR-4 | Controls must be keyboard-reachable and screen-reader labeled; disabled mandatory/legal controls need persistent text; save status needs ARIA live announcement. | `specs/non-functional-requirements.md:50-60`; `specs/product-spec-notification-preferences.md:176-180` | Current checkbox UI lacks helper text, group semantics, and save-status announcements (`src/frontend/src/components/notification-toggle.ts:18-26`, `src/frontend/src/pages/preferences.ts:19-38`). |
33. | NFR-5 | Emit metrics for read/save failures, audit write failures, fallback invocations, and save latency; distinguish validation failures from downstream failures. | `specs/non-functional-requirements.md:63-80` | No metrics implementation is present in the current source (`src/backend/src`, search results for metrics were empty). |
34. | NFR-6 | Ship behind a release flag; non-pilot users must get 404, not 403; defaults on first access are expected and not a data bug. | `specs/non-functional-requirements.md:84-97`; `docs/architecture.md:43-47` | Existing feature flags do not include a notification-preferences pilot flag, and current routes are always mounted (`src/backend/src/config/feature-flags.ts:16-25`, `src/backend/src/app.ts:52-57`). |
35. | NFR-7 | Retain audit records for 24 months; mandatory escalation delivery rules must be testable and documented; compliance review must show effective preference state including defaults. | `specs/non-functional-requirements.md:101-110` | Audit repository is append-only, which aligns with retention expectations, but the effective-default/read-only reviewer view still needs design and implementation (`src/backend/src/models/audit-repository.ts:1-9`, `src/backend/src/routes/audit.ts:17-34`). |
36. 
37. ## 3. Open questions with file references
38. 
39. 1. **Should compliance reviewers access audit history from the same settings page or a separate audit viewer?** The product spec leaves this open, while the codebase already has a separate audit route that could be linked instead of embedded.  
40.    Sources: `specs/product-spec-notification-preferences.md:187-193`, `src/backend/src/routes/audit.ts:17-34`.
41. 
42. 2. **Should mixed-portfolio restrictions render as a summary banner, per-row indicators, or both?** The product spec explicitly asks this, and the current frontend has no portfolio-aware model yet.  
43.    Sources: `specs/product-spec-notification-preferences.md:166-170`, `:187-193`, `src/frontend/src/pages/preferences.ts:19-36`.
44. 
45. 3. **What is the authoritative read-scope rule for non-delegated underwriters and analyst managers?** The product spec clearly defines self-edit and delegated inspection, but the current GET endpoint accepts any `userId` for any allowed role.  
46.    Sources: `specs/product-spec-notification-preferences.md:48-62`, `:153-160`, `src/backend/src/routes/notifications.ts:33-43`.
47. 
48. 4. **How should loan context reach the preference API for FR-4/SC-3 validation?** The current save payload contains only `userId`, `event`, `channel`, and `enabled`, yet the California rule depends on `loanState`, and the bug report already calls out this gap as a likely root cause.  
49.    Sources: `src/backend/src/routes/notifications.ts:49-54`, `:75-100`, `src/frontend/src/api/client.ts:87-97`, `specs/bug-report.md:49-56`, `:60-63`.
50. 
51. 5. **How should fail-closed auditability work when `queueAudit` is enabled?** The NFR requires rejecting the save before success is reported, but the current queue model emits after persistence and does not roll the write back on handler failure.  
52.    Sources: `specs/non-functional-requirements.md:23-34`, `src/backend/src/services/audit-service.ts:34-45`, `src/backend/src/queue/handlers/audit-handler.ts:8-13`.
53. 
54. ## 4. Inferred implementation choices (not confirmed requirements)
55. 
56. These are recommended plan assumptions based on source structure and architecture rules, but they are **not** directly mandated by the specs.
57. 
58. 1. **Add a dedicated pilot flag for notification preferences** instead of overloading unrelated flags like `smsFallback` or `californiaRules`, because NFR-6 requires release gating and the current feature-flag surface does not model it (`specs/non-functional-requirements.md:84-95`, `src/backend/src/config/feature-flags.ts:16-25`).
59. 
60. 2. **Move preference validation into a dedicated rules/service layer** so routes remain orchestration-only, matching the architecture rule that business rules live under `src/backend/src/rules/` and services handle orchestration/I/O (`docs/architecture.md:22-25`, `specs/feature-request.md:31-34`).
61. 
62. 3. **Return an "effective preferences" response model** that includes synthesized defaults, disabled reasons, mandatory-event metadata, delegated-session mode, and contextual restriction explanations. This best fits FR-3, FR-4, SC-2, SC-3, and NFR-4 without forcing the frontend to reconstruct business rules (`specs/product-spec-notification-preferences.md:94-119`, `:153-180`).
63. 
64. 4. **Use a central client store for the preference matrix and save lifecycle** rather than direct DOM mutation, to comply with ADR-003 and support rollback, ARIA status, and contextual banners (`docs/adr/ADR-003-frontend-state.md:16-31`, `src/frontend/src/components/notification-toggle.ts:18-44`).
65. 
66. 5. **Prefer a transactional or preflight audit-write strategy for preference saves** so the main write cannot succeed unless auditability is guaranteed. This is the clearest way to satisfy NFR-2 given the current asynchronous audit path. (`specs/non-functional-requirements.md:23-34`, `src/backend/src/services/audit-service.ts:18-45`).
67. 
68. ## 5. Constraints and special conditions
69. 
70. - **Delegated sessions are read-only for writes**: delegated users may inspect but not save another user's preferences, and the UI must make that mode obvious (`specs/product-spec-notification-preferences.md:153-160`, `src/backend/src/middleware/auth.ts:63-72`).
71. 
72. - **`LEGAL-218` applies to California decline SMS, not manual-review escalation SMS**: use `loanState` as the jurisdiction source, show persistent explanation text, and present multi-state restrictions conditionally rather than globally (`specs/product-spec-notification-preferences.md:105-119`, `:166-170`).
73. 
74. - **Mandatory-event delivery must stay intact**: manual-review escalation may not be reduced to zero channels, and existing workflow-triggered mandatory-event emission in `loan-service.ts` / `mandatory-events.ts` must continue to produce deliverable events (`specs/product-spec-notification-preferences.md:81-92`, `src/backend/src/rules/mandatory-events.ts:17-37`, `src/backend/src/services/loan-service.ts:100-117`).
75. 
76. - **Audit must fail closed for writes**: do not treat audit as fire-and-forget for preference saves. A read succeeding during audit trouble is a **false positive** and not a bug; a successful-looking write without an audit trail is a **hard negative** and a real bug (`specs/non-functional-requirements.md:23-34`).
77. 
78. - **Degraded-mode fallback is runtime delivery logic, not preference mutation**: receiving email during SMS outage is a **false positive** for "bad preferences" if stored SMS is still enabled; metrics must capture fallback separately (`specs/product-spec-notification-preferences.md:120-130`, `src/backend/src/queue/handlers/notification-handler.ts:62-76`).
79. 
80. - **Pilot gating must hide the feature with 404 for non-pilot users**: returning 403 would leak feature existence and is a **hard negative** against NFR-6 (`specs/non-functional-requirements.md:84-95`).
81. 
82. - **Accessibility constraints are explicit**: disabled controls need persistent helper text, not just a tooltip, and save outcomes need ARIA live messaging (`specs/non-functional-requirements.md:50-60`, `specs/product-spec-notification-preferences.md:176-180`).
83. 
84. - **Queued-notification caveat for finalized applications**: preference changes remain global, but the UI must say they do not affect notifications already queued for that finalized application (`specs/product-spec-notification-preferences.md:147-152`).
85. 
86. ## 6. Numbered tasks with acceptance criteria and source references
87. 
88. 1. **Define and gate the feature entry points**
89.    - Scope: introduce a notification-preferences pilot flag, guard backend endpoints and frontend navigation/page loading, and return 404 for non-pilot users.
90.    - Acceptance criteria:
91.      - Non-pilot users receive 404, not 403, for notification-preference routes/pages.
92.      - Pilot users see the feature without changing unrelated app behavior.
93.      - Rollout notes include observability and fallback expectations.
94.    - Sources: NFR-6 (`specs/non-functional-requirements.md:84-97`), architecture rule on pilot-gated features (`docs/architecture.md:43-47`), current flag surface (`src/backend/src/config/feature-flags.ts:16-25`).
95. 
96. 2. **Introduce backend preference-domain logic for effective defaults and validation**
97.    - Scope: add/centralize rules for role-based defaults, mandatory-event zero-channel protection, California decline SMS restriction, delegated-session/owner checks, and compliance reviewer read-only semantics.
98.    - Acceptance criteria:
99.      - First access returns effective defaults without requiring seeded rows or migration.
100.      - Disabling both channels for `manual-review-escalation` is rejected in both granular and bulk-save flows.
101.      - Decline SMS rejects for California context with an explicit reason tied to `loanState`.
102.      - Delegated sessions and compliance reviewers cannot write preferences.
103.    - Sources: FR-2/3/4 (`specs/product-spec-notification-preferences.md:81-119`), SC-2 (`:153-165`), NFR-6 (`specs/non-functional-requirements.md:86-97`), current route gaps (`src/backend/src/routes/notifications.ts:45-271`).
104. 
105. 3. **Refactor notification preference API routes/services around the rules layer**
106.    - Scope: keep routes thin, return effective preferences plus disabled/helper metadata, and ensure GET/PUT semantics reflect the agreed read/write scope.
107.    - Acceptance criteria:
108.      - GET returns effective preference state, including defaults and restriction explanations.
109.      - PUT rejects invalid saves before persistence and returns enough structured error information for UI rollback.
110.      - API surfaces identify delegated-session mode and restriction reasons without exposing sensitive phone data.
111.    - Sources: architecture layering (`docs/architecture.md:22-25`, `:53-58`), ADR-003 (`docs/adr/ADR-003-frontend-state.md:24-31`), NFR-3 (`specs/non-functional-requirements.md:38-47`), current route/client shape (`src/backend/src/routes/notifications.ts:33-271`, `src/frontend/src/api/client.ts:83-97`).
112. 
113. 4. **Make preference saves fail closed on auditability**
114.    - Scope: redesign preference-save flow so audit failure prevents a successful mutation response; ensure audit entries capture actor, delegated-for, previous/new values, source, and timestamp.
115.    - Acceptance criteria:
116.      - A preference save cannot return success if the audit path is unavailable.
117.      - Audit records contain actor, delegated-for, previous/new values, source, and timestamp for every successful save.
118.      - Validation failures remain 4xx and audit/provider failures are distinguishable for logging/metrics.
119.    - Sources: FR-6 (`specs/product-spec-notification-preferences.md:132-142`), NFR-2/NFR-5/NFR-7 (`specs/non-functional-requirements.md:21-34`, `:63-80`, `:101-107`), current conflicting audit path (`src/backend/src/services/audit-service.ts:18-45`, `src/backend/src/queue/handlers/audit-handler.ts:8-13`, `src/backend/src/middleware/audit-logger.ts:37-65`).
120. 
121. 5. **Preserve mandatory-event delivery and degraded-mode fallback behavior**
122.    - Scope: ensure preference validation and delivery logic work together so mandatory escalation remains deliverable and SMS outages fall back to email without rewriting stored preferences.

[Output truncated. Use view_range=[123, ...] to continue reading.]
```

</details>


---

<sub>⏱️ 3m 30s</sub>

### ✅ `view`

**view the file at C:\Users\nilay\.copilot\session-state\cd551e9d-6f2a-4c2f-8cac-4ad81ea916f4\plan.md.**

C:\Users\nilay\.copilot\session-state\cd551e9d-6f2a-4c2f-8cac-4ad81ea916f4\plan.md (lines 1-80)

```
1. 1. Read architecture, ADR, product, NFR, feature request, bug report, and relevant source surfaces for notification preferences.
2. 2. Synthesize confirmed requirements, conflicts, open questions, inferred choices, tasks, validation, and risks.
3. 3. Write the implementation plan to docs/notification-preferences-plan.md.
```


---

<sub>⏱️ 3m 35s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\notification-preferences-plan.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\notification-preferences-plan.md (lines 121-260)

<details>
<summary>89 lines</summary>

```
121. 5. **Preserve mandatory-event delivery and degraded-mode fallback behavior**
122.    - Scope: ensure preference validation and delivery logic work together so mandatory escalation remains deliverable and SMS outages fall back to email without rewriting stored preferences.
123.    - Acceptance criteria:
124.      - Workflow transitions that require `manual-review-escalation` continue to emit the event.
125.      - Preference state never mutates because of runtime SMS fallback.
126.      - Fallback invocations emit a dedicated metric and are distinguishable from preference-save errors.
127.    - Sources: FR-2/FR-5 (`specs/product-spec-notification-preferences.md:81-92`, `:120-130`), NFR-5 (`specs/non-functional-requirements.md:63-80`), current mandatory/fallback surfaces (`src/backend/src/rules/mandatory-events.ts:17-37`, `src/backend/src/services/loan-service.ts:100-117`, `src/backend/src/queue/handlers/notification-handler.ts:33-77`).
128. 
129. 6. **Rebuild the frontend preferences experience around central state and explicit UX constraints**
130.    - Scope: replace direct-toggle local mutation with a store-backed matrix page that supports optimistic rollback, delegated banners, persistent helper text, finalized-state messaging, and ARIA live announcements.
131.    - Acceptance criteria:
132.      - Persisted preference state lives in the central client store, not component-local state.
133.      - Delegated mode is visually obvious and save actions are disabled or blocked before request.
134.      - Mandatory/legal restriction explanations are persistently visible.
135.      - Save success/failure is announced accessibly, and optimistic changes roll back correctly on server rejection.
136.      - Finalized application context warns that queued notifications are unaffected.
137.    - Sources: ADR-003 (`docs/adr/ADR-003-frontend-state.md:16-31`), SC-1/SC-2/SC-3 (`specs/product-spec-notification-preferences.md:147-180`), NFR-4 (`specs/non-functional-requirements.md:50-60`), current simplistic UI (`src/frontend/src/pages/preferences.ts:10-39`, `src/frontend/src/components/notification-toggle.ts:18-44`).
138. 
139. 7. **Add compliance/audit viewing behavior for effective preferences**
140.    - Scope: expose read-only effective preferences for compliance reviewers and resolve whether audit history is embedded or linked.
141.    - Acceptance criteria:
142.      - Compliance reviewers can inspect effective preferences including defaults but cannot modify operational settings.
143.      - The chosen audit-view pattern is documented and consistent with existing audit routes.
144.      - Audit retention assumptions remain compatible with the append-only repository.
145.    - Sources: product roles + open question (`specs/product-spec-notification-preferences.md:59-63`, `:187-193`), NFR-7 (`specs/non-functional-requirements.md:101-107`), current audit route/repository (`src/backend/src/routes/audit.ts:17-34`, `src/backend/src/models/audit-repository.ts:1-9`).
146. 
147. 8. **Close the testing and observability gaps**
148.    - Scope: add backend/frontend tests and telemetry for validation, audit failure, rollout gating, delegated behavior, fallback, and accessibility.
149.    - Acceptance criteria:
150.      - Unit/integration coverage exists for all hard negatives and false positives listed below.
151.      - Metrics exist for read/save failure, audit write failure, fallback, and save latency.
152.      - Logs distinguish validation issues from downstream failures without leaking sensitive SMS destination data.
153.    - Sources: NFR-3/NFR-5 (`specs/non-functional-requirements.md:38-47`, `:63-80`), lesson expectations (`docs/planning-workflow-example.md:33-39`, `:55-60`), current sparse tests (`src/backend/tests/unit/notification-service.test.ts:10-15`, `src/backend/tests/integration/decisions.test.ts:7-14`).
154. 
155. ## 7. Validation steps
156. 
157. 1. **Defaults and first access**
158.    - Verify a pilot underwriter with no stored rows receives FR-3 defaults on first load without migration.
159.    - Confirm compliance reviewer sees effective read-only state, including defaults.  
160.    Sources: FR-3, NFR-6, NFR-7 (`specs/product-spec-notification-preferences.md:94-104`, `specs/non-functional-requirements.md:86-107`).
161. 
162. 2. **Mandatory-event hard negative / false positive**
163.    - Hard negative: attempt to disable both channels for `manual-review-escalation`; API and UI must reject it.
164.    - False positive: disable only SMS while email remains enabled; this must succeed.  
165.    Sources: FR-2 (`specs/product-spec-notification-preferences.md:81-92`).
166. 
167. 3. **Delegated-session hard negative**
168.    - In delegated mode, verify preferences are viewable but save is blocked and no success toast/state commit survives.
169.    - Confirm audit records include both actor and delegated-for for allowed reads/surfaced operations.  
170.    Sources: SC-2, ADR-003, bug report (`specs/product-spec-notification-preferences.md:153-165`, `docs/adr/ADR-003-frontend-state.md:24-31`, `specs/bug-report.md:20-27`).
171. 
172. 4. **California restriction / LEGAL-218**
173.    - Hard negative: attempt to enable decline SMS for a California loan context; control must be disabled or save rejected with persistent explanation.
174.    - Confirm the rule keys off `loanState`, not borrower address.
175.    - In mixed-portfolio context, verify restrictions render conditionally rather than blanket-disabling all SMS.  
176.    Sources: FR-4, SC-3 (`specs/product-spec-notification-preferences.md:105-119`, `:166-170`).
177. 
178. 5. **Fail-closed audit behavior**
179.    - Hard negative: simulate audit unavailability and confirm preference save fails without persisting the new preference.
180.    - False positive: reads should still succeed during the same outage.  
181.    Sources: NFR-2 (`specs/non-functional-requirements.md:21-34`).
182. 
183. 6. **Degraded-mode fallback**
184.    - False positive: simulate SMS outage with email enabled and confirm delivery falls back to email without mutating stored preferences.
185.    - Verify `notification.sms.fallback` metric increments separately.  
186.    Sources: FR-5, NFR-5 (`specs/product-spec-notification-preferences.md:120-130`, `specs/non-functional-requirements.md:65-74`).
187. 
188. 7. **Pilot gating**
189.    - Hard negative: a non-pilot user must see 404, not 403, for backend endpoints and the UI entry point.  
190.    Sources: NFR-6 (`specs/non-functional-requirements.md:86-95`).
191. 
192. 8. **Accessibility and finalized-state messaging**
193.    - Validate keyboard navigation, screen-reader labels, persistent helper text, and ARIA live status updates.
194.    - In finalized context, confirm the UI warns that already queued notifications are unaffected.  
195.    Sources: SC-1, NFR-4 (`specs/product-spec-notification-preferences.md:147-180`, `specs/non-functional-requirements.md:50-60`).
196. 
197. ## 8. Risks and dependencies
198. 
199. - **Audit architecture risk**: the current queue-based audit flow is fundamentally at odds with fail-closed preference saves. Resolving this may require a synchronous write path, a transactional outbox, or another design that guarantees auditability before success is returned (`src/backend/src/services/audit-service.ts:18-45`, `src/backend/src/queue/handlers/audit-handler.ts:8-13`).
200. 
201. - **Frontend state dependency**: the current preferences UI is not built on a central store, so ADR-003 compliance is a non-trivial refactor rather than a small toggle patch (`src/frontend/src/components/notification-toggle.ts:18-44`, `docs/adr/ADR-003-frontend-state.md:16-31`).
202. 
203. - **API contract dependency**: FR-4 and SC-3 need contextual restriction data, but current client/server payloads do not carry loan or portfolio context (`src/frontend/src/api/client.ts:83-97`, `src/backend/src/routes/notifications.ts:49-54`).
204. 
205. - **Telemetry gap**: NFR-5 calls for metrics, but no metrics layer appears in the current source. Implementation may need a new observability abstraction or integration point.
206. 
207. - **Read-scope ambiguity**: the desired read behavior for non-delegated internal roles is not fully specified and should be resolved before implementation to avoid shipping an over-broad read surface.
208. 
209. - **Bug-report wording conflict**: if the team uses the bug title instead of FR-4/body details, they could incorrectly apply `LEGAL-218` to manual-review escalation SMS instead of decline SMS. The plan should keep FR-4 as canonical.
```

</details>


---

<sub>⏱️ 3m 40s</sub>

### 💬 Copilot

Done — I inspected the architecture, ADR, product spec, NFRs, bug report, feature request, and current notification/auth/audit/frontend surfaces, then saved a structured plan to `docs/notification-preferences-plan.md`.

The plan includes confirmed requirements with FR/SC/ADR/NFR references, open questions with file refs, inferred choices separated from requirements, constraints/special conditions, numbered tasks with acceptance criteria, validation steps, and risks/dependencies.

It explicitly calls out delegated sessions, `LEGAL-218`, mandatory-event delivery, fail-closed audit behavior, degraded-mode fallback, a false positive, a hard negative, and the canonical-source hierarchy for resolving overlaps/conflicts.

---

<sub>Generated by [GitHub Copilot CLI](https://github.com/features/copilot/cli)</sub>
