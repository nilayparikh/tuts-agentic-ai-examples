# 🤖 Copilot CLI Session

> [!NOTE]
> - **Session ID:** `0b1cb144-3c12-4347-909a-85fc85baa317`  
> - **Started:** 14/03/2026, 17:17:58  
> - **Duration:** 3m 57s  
> - **Exported:** 14/03/2026, 17:21:56  

---

<sub>⏱️ 5s</sub>

### 👤 User

Inspect the relevant docs/, specs/, and existing source surfaces for notification preferences in this lesson before answering. Discover the architecture, ADR, product, and NFR context you need rather than assuming a fixed file list. Produce a structured implementation plan and save it to docs/notification-preferences-plan.md. The plan must include: summary, source-backed confirmed requirements with references to FR/SC/ADR/NFR identifiers, open questions with file references, inferred implementation choices separated from confirmed requirements, constraints and special conditions, numbered tasks with acceptance criteria and source references, validation steps, and risks/dependencies. Explicitly call out delegated sessions, LEGAL-218, mandatory-event delivery, fail-closed audit behavior, degraded-mode fallback, at least one false positive, and at least one hard negative. If the sources overlap or conflict, identify the canonical source for the plan and explain why. Do not run shell commands and do not use SQL.

---

<sub>⏱️ 17s</sub>

### 💬 Copilot

I’m gathering the authoritative sources first so the plan is anchored in the lesson’s actual docs, ADRs, specs, and current notification-preference code paths.

---

<sub>⏱️ 18s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows**

"docs\**\*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows

```
No files matched the pattern.
```


---

<sub>⏱️ 18s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows**

"specs\**\*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows

```
No files matched the pattern.
```


---

<sub>⏱️ 18s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "notification|preference|LEGAL-218|delegated|audit|degraded|mandatory|fallback|fail-closed",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\04-planning-workflows",
  "output_mode": "content",
  "glob": "docs/**",
  "-n": true,
  "head_limit": 200
}
```

</details>

<details>
<summary>19 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\planning-workflow-example.md:7:Show that a planning workflow can turn a visible feature request into a grounded, written implementation plan. The CLI writes the plan to `docs/notification-preferences-plan.md` so the output is assessable as a code change.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\planning-workflow-example.md:11:The demo must produce a new file `docs/notification-preferences-plan.md` containing:
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\planning-workflow-example.md:31:1. The plan must be written to `docs/notification-preferences-plan.md` as a real file change.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\planning-workflow-example.md:34:4. The plan must explicitly call out delegated-session behavior, LEGAL-218, mandatory-event delivery, fail-closed audit semantics, and degraded-mode fallback.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\planning-workflow-example.md:43:Use the notification preferences feature request and supporting docs to produce a plan that is deeper than "add a settings page and API route".
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\planning-workflow-example.md:47:- delegated sessions
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\planning-workflow-example.md:50:- audit fail-closed semantics
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\planning-workflow-example.md:58:- identify affected route, rule, service, UI, state, and audit surfaces
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\adr\ADR-003-frontend-state.md:10:application lists, decision forms, notification settings, and audit viewers.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\adr\ADR-003-frontend-state.md:21:- Persisted user preferences
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\adr\ADR-003-frontend-state.md:35:An AI assistant generating a notification-preferences UI will default to
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\architecture.md:17:      middleware/           ← Auth, audit logger, error handler, rate limiter
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\architecture.md:21:        handlers/           ← Notification + audit event consumers
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\architecture.md:30:      pages/                ← Dashboard, application detail, preferences
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\architecture.md:42:2. Underwriting decisions require API support and audit coverage.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\architecture.md:44:4. Pilot-gated features must call out rollout, observability, and fallback behavior.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\architecture.md:45:5. Product rules may vary by role, loan jurisdiction, and delegated-session mode.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\architecture.md:46:6. Audit is mandatory for all writes — via queue broker or direct DB write.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\architecture.md:57:- identify the frontend, route, rule, service, audit, and observability surfaces that would likely change
```

</details>


---

<sub>⏱️ 18s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "notification|preference|LEGAL-218|delegated|audit|degraded|mandatory|fallback|fail-closed",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\04-planning-workflows",
  "output_mode": "content",
  "glob": "specs/**",
  "-n": true,
  "head_limit": 200
}
```

</details>

<details>
<summary>84 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:15:notifications. The current Loan Workbench sends a fixed set of email alerts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:16:with no user-level preferences. Teams report alert fatigue for routine document
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:17:requests and missed high-severity escalation events when all notifications are
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:22:Allow authorized users to configure notification preferences by channel and
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:23:event type without breaking auditability, workflow SLAs, or regulatory
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:30:- Settings UI for notification preferences in `apps/web/`
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:31:- API support in `services/api/` for reading and updating preferences
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:34:- Event-specific preferences for: approval, decline, document-request,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:40:- Push notifications
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:41:- Per-loan notification overrides
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:50:- Can edit their own notification preferences
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:51:- **Cannot suppress mandatory manual-review-escalation notifications**
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:55:- Can edit their own notification preferences
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:56:- Receives additional portfolio-level digest notifications (later release)
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:57:- Can operate in **delegated mode** on behalf of another user
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:61:- **Read-only** access to effective preference configuration for audit review
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:62:- Cannot change operational preferences from the UI
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:83:Manual-review escalation is a **mandatory notification**. Users may change the
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:86:> **HARD NEGATIVE pattern:** Without this rule, an AI generating the preference
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:102:New users without saved preferences must receive these defaults on first access
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:108:the legal review tracked in `LEGAL-218` is complete.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:125:2. **Stored preferences must NOT be modified by the fallback.**
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:129:> an outage is NOT a preference bug. Support agents must check delivery logs,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:130:> not the preference store, to diagnose delivery complaints.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:134:Every preference change must record:
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:150:preferences globally, but the settings screen must clarify that changes **do not
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:151:affect notifications already queued** for that application.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:155:If an analyst manager is operating in delegated mode:
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:157:- They may **view** the delegate's notification preferences.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:158:- They may **not modify** the delegate's preferences.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:159:- The UI must visually indicate delegated-session mode.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:160:- Audit entries must record both the actor and the delegated-for user.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:162:> **HARD NEGATIVE pattern:** A delegated save that shows a "success" toast but
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:184:- < 1% failed preference saves during pilot
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:185:- Zero Sev2 incidents caused by suppressed mandatory escalation alerts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:189:1. Should compliance reviewers access audit history from the same settings page
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md:190:   or a separate audit viewer?
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:3:These NFRs constrain the notification preferences feature. Each requirement
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:15:> **AI mistake without context:** An assistant might generate a preference save
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:23:- Preference reads must tolerate notification-provider degradation (the provider
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:24:  is not the source of truth for preferences).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:25:- **If audit logging is unavailable, writes must FAIL CLOSED** rather than
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:26:  silently saving preferences without an audit trail.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:29:> will generate `try { auditLog(...) } catch { /* ignore */ }` unless the NFR
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:33:> **FALSE POSITIVE:** Preference reads succeeding during an audit-service
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:34:> outage is NOT a bug — only writes require audit availability.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:40:- Only authenticated internal users can access the preferences endpoint.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:43:- Delegated sessions must be explicitly identified in audit logs.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:45:> **AI mistake without context:** An assistant might log the full preference
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:53:- Disabled mandatory-event controls must have **persistent explanatory text**,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:69:| `preference.read.failure`   | Counter   | Store read errors                             |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:70:| `preference.save.failure`   | Counter   | Distinguishes validation from provider errors |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:71:| `audit.write.failure`       | Counter   | Tracks fail-closed rejections                 |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:72:| `notification.sms.fallback` | Counter   | SMS→email fallback invocations                |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:73:| `preference.save.latency`   | Histogram | p50/p95/p99 save duration                     |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:89:- Existing users without saved preferences must receive role-based defaults
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:103:- Audit records for preference changes must be **retained for 24 months**.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:106:- The compliance reviewer's read-only view must show the effective preference
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md:110:> job to audit records without checking the retention policy.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\feature-request.md:3:Add notification preferences to the Loan Workbench settings area.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\feature-request.md:7:- Underwriters can control email and SMS notifications per event type.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\feature-request.md:11:- The plan must account for delegated sessions, audit logging, and state-based restrictions.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\feature-request.md:15:- Full product specification: `specs/product-spec-notification-preferences.md`
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\feature-request.md:21:- **California loans** cannot enable SMS for decline decisions (LEGAL-218).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\feature-request.md:22:- **Delegated sessions**: analyst managers may inspect but not edit another user's preferences.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\feature-request.md:23:- **SMS degraded mode**: email fallback must preserve the stored preference model.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\feature-request.md:24:- **Mandatory escalation events** must remain deliverable even when users change preferences.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\feature-request.md:25:- **Audit writes** must fail closed — no silent saves without an audit trail.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\feature-request.md:26:- **Existing users** may not have stored preferences and need role-based defaults on first access.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\feature-request.md:30:- Current settings screens do not expose notification preferences.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:6:delegated sessions; save succeeds visually but reverts on refresh.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:10:An analyst manager opened notification settings while acting on behalf of an
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:11:underwriter (`x-delegated-for: u-1`) for a California loan (`app-100`). They
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:14:1. The SMS toggle for decline notifications was **enabled and editable** even
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:15:   though California loans restrict decline SMS (LEGAL-218).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:22:- **Delegated sessions should be read-only** for another user's preferences (SC-2).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:43:| Business rule | CA decline SMS is restricted                              | FR-4 / LEGAL-218 |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:45:| Audit         | If audit write failed, the save should have been rejected | NFR-2            |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:49:1. **Delegated-session write guard** is not applied to the preference save route.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:60:- Compare UI behavior against `specs/product-spec-notification-preferences.md` sections SC-2 and FR-4.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:61:- Check `src/backend/src/routes/notifications.ts` for the `blockDelegatedWrites` middleware attachment.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:62:- Check whether the preference save sends `loanState` to the API.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:63:- Verify that the audit service was healthy at the time of the report.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\bug-report.md:64:- Check `src/backend/src/middleware/auth.ts` for delegated-session detection logic.
```

</details>


---

<sub>⏱️ 18s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "notification|preference|LEGAL-218|delegated|audit|degraded|mandatory|fallback|fail-closed",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\04-planning-workflows",
  "output_mode": "content",
  "glob": "src/**",
  "-n": true,
  "head_limit": 300
}
```

</details>

```
No matches found.
```


---

<sub>⏱️ 29s</sub>

### 💬 Copilot

I found the main requirement sources and now I’m reading the concrete architecture/ADR/spec/code files to ground the plan and spot any conflicts or gaps.

---

<sub>⏱️ 29s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs

```
adr
architecture.md
planning-workflow-example.md
```


---

<sub>⏱️ 29s</sub>

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

<sub>⏱️ 29s</sub>

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

<sub>⏱️ 29s</sub>

### ❌ `view`

**view the file at C:\Users\nilay\.copilot\session-state\0b1cb144-3c12-4347-909a-85fc85baa317\plan.md.**

C:\Users\nilay\.copilot\session-state\0b1cb144-3c12-4347-909a-85fc85baa317\plan.md

```
Path does not exist
```


---

<sub>⏱️ 29s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows**

"src\**\*notification*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows

```
No files matched the pattern.
```


---

<sub>⏱️ 29s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows**

"src\**\*preference*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows

```
No files matched the pattern.
```


---

<sub>⏱️ 40s</sub>

### 💬 Copilot

The source tree is smaller than expected, so I’m enumerating the exact backend/frontend notification surfaces next and then I’ll draft the plan file from those references.

---

<sub>⏱️ 40s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend

```
dist
src
tests
tsconfig.json
```


---

<sub>⏱️ 40s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend

<details>
<summary>6 lines</summary>

```
index.html
public
src
styles
tsconfig.json
vite.config.ts
```

</details>


---

<sub>⏱️ 40s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "notification|preference|delegated|LEGAL-218|audit|fallback|mandatory",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\04-planning-workflows\\src\\backend",
  "output_mode": "files_with_matches",
  "head_limit": 100
}
```

</details>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\unit\notification-service.test.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\integration\decisions.test.ts
```


---

<sub>⏱️ 40s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "notification|preference|delegated|LEGAL-218|audit|fallback|mandatory",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\04-planning-workflows\\src\\frontend",
  "output_mode": "files_with_matches",
  "head_limit": 100
}
```

</details>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\styles\main.css
```


---

<sub>⏱️ 40s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\architecture.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\architecture.md

<details>
<summary>70 lines</summary>

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
70.
````

</details>


---

<sub>⏱️ 40s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\adr\ADR-003-frontend-state.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\adr\ADR-003-frontend-state.md

<details>
<summary>38 lines</summary>

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
38.
```

</details>


---

<sub>⏱️ 40s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\feature-request.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\feature-request.md

<details>
<summary>41 lines</summary>

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
41.
```

</details>


---

<sub>⏱️ 40s</sub>

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

<sub>⏱️ 40s</sub>

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

<sub>⏱️ 40s</sub>

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

<sub>⏱️ 46s</sub>

### 💬 Copilot

I’ve got the core spec/NFR material. Next I’m reading the backend/frontend code paths that already touch notifications, audit, auth, flags, and store behavior so the task list maps to real files.

---

<sub>⏱️ 46s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src

<details>
<summary>9 lines</summary>

```
app.ts
config
db
middleware
models
queue
routes
rules
services
```

</details>


---

<sub>⏱️ 46s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src

```
api
components
main.ts
pages
```


---

<sub>⏱️ 46s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "blockDelegatedWrites|delegated|audit|feature flag|404|notification|preference|store|useState|optimistic|rollback|loanState",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\04-planning-workflows\\src",
  "output_mode": "content",
  "-n": true,
  "head_limit": 300
}
```

</details>

<details>
<summary>9 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\styles\main.css:452:.notification-toggle {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\styles\main.css:462:.notification-toggle:hover {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\integration\decisions.test.ts:12:  it("placeholder — delegated sessions cannot record decisions", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\unit\business-rules.test.ts:17:  loanState: "NY",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\unit\business-rules.test.ts:39:      loanState: "CA",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\unit\business-rules.test.ts:48:      loanState: "CA",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\unit\notification-service.test.ts:7:// These tests verify the notification routing logic at the service level.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\unit\notification-service.test.ts:11:  it("placeholder — notification service emits queue events", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\unit\notification-service.test.ts:12:    // Integration tests for notification delivery live in the queue handler tests.
```

</details>


---

<sub>⏱️ 46s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\unit\notification-service.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\unit\notification-service.test.ts

<details>
<summary>17 lines</summary>

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
17.
```

</details>


---

<sub>⏱️ 46s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\integration\decisions.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\integration\decisions.test.ts

<details>
<summary>16 lines</summary>

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
16.
```

</details>


---

<sub>⏱️ 55s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes

```
applications.ts
audit.ts
decisions.ts
notifications.ts
queue-status.ts
```


---

<sub>⏱️ 55s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware

```
audit-logger.ts
auth.ts
error-handler.ts
rate-limiter.ts
request-validator.ts
```


---

<sub>⏱️ 55s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules

```
business-rules.ts
mandatory-events.ts
role-permissions.ts
state-machine.ts
```


---

<sub>⏱️ 55s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services

```
audit-service.ts
decision-service.ts
loan-service.ts
notification-service.ts
```


---

<sub>⏱️ 55s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\pages.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\pages

```
api-explorer.ts
application-detail.ts
dashboard.ts
preferences.ts
queue-monitor.ts
```


---

<sub>⏱️ 55s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\api.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\api

```
client.ts
types.ts
```


---

<sub>⏱️ 55s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\components.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\components

```
app-shell.ts
loan-table.ts
notification-toggle.ts
status-badge.ts
```


---

<sub>⏱️ 55s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\unit\business-rules.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\tests\unit\business-rules.test.ts

<details>
<summary>72 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Business Rules Tests
3. // ---------------------------------------------------------------------------
4. 
5. import { describe, it, expect } from "vitest";
6. import {
7.   validateLoanRules,
8.   requiredApprovalRoles,
9.   canApprove,
10. } from "../../src/rules/business-rules.js";
11. import type { LoanApplication } from "../../src/models/types.js";
12. 
13. const baseLoan: LoanApplication = {
14.   id: "test-1",
15.   borrowerName: "Test Corp",
16.   amount: 100000,
17.   loanState: "NY",
18.   status: "intake",
19.   assignedUnderwriter: "u-1",
20.   riskScore: null,
21.   createdAt: new Date().toISOString(),
22.   updatedAt: new Date().toISOString(),
23. };
24. 
25. describe("Business Rules", () => {
26.   it("passes for a valid standard loan", () => {
27.     expect(validateLoanRules(baseLoan)).toEqual([]);
28.   });
29. 
30.   it("rejects zero amount", () => {
31.     const violations = validateLoanRules({ ...baseLoan, amount: 0 });
32.     expect(violations).toHaveLength(1);
33.     expect(violations[0].rule).toBe("positive-amount");
34.   });
35. 
36.   it("rejects California loan below minimum", () => {
37.     const violations = validateLoanRules({
38.       ...baseLoan,
39.       loanState: "CA",
40.       amount: 10000,
41.     });
42.     expect(violations.some((v) => v.rule === "ca-min-amount")).toBe(true);
43.   });
44. 
45.   it("rejects California loan above maximum", () => {
46.     const violations = validateLoanRules({
47.       ...baseLoan,
48.       loanState: "CA",
49.       amount: 6_000_000,
50.     });
51.     expect(violations.some((v) => v.rule === "ca-max-amount")).toBe(true);
52.   });
53. });
54. 
55. describe("Approval Roles", () => {
56.   it("underwriter can approve loans up to $1M", () => {
57.     expect(canApprove("underwriter", 500000)).toBe(true);
58.   });
59. 
60.   it("underwriter cannot approve loans over $1M", () => {
61.     expect(canApprove("underwriter", 1_500_000)).toBe(false);
62.   });
63. 
64.   it("analyst-manager required for loans over $1M", () => {
65.     expect(requiredApprovalRoles(1_500_000)).toContain("analyst-manager");
66.   });
67. 
68.   it("compliance-reviewer required for loans over $2.5M", () => {
69.     expect(requiredApprovalRoles(3_000_000)).toContain("compliance-reviewer");
70.   });
71. });
72.
```

</details>


---

<sub>⏱️ 1m 5s</sub>

### 💬 Copilot

I’ve identified the concrete files. I’m reading the route, middleware, service, UI, and queue contract surfaces now so the plan can name exact change points and validation targets.

---

<sub>⏱️ 1m 5s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\notifications.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\notifications.ts

<details>
<summary>272 lines</summary>

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
272.
```

</details>


---

<sub>⏱️ 1m 5s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\auth.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\auth.ts

<details>
<summary>98 lines</summary>

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
98.
```

</details>


---

<sub>⏱️ 1m 5s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\notification-service.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\notification-service.ts

<details>
<summary>48 lines</summary>

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
48.
```

</details>


---

<sub>⏱️ 1m 5s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\audit-service.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\audit-service.ts

<details>
<summary>47 lines</summary>

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
47.
```

</details>


---

<sub>⏱️ 1m 5s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\mandatory-events.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\mandatory-events.ts

<details>
<summary>38 lines</summary>

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
38.
```

</details>


---

<sub>⏱️ 1m 5s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\role-permissions.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\role-permissions.ts

<details>
<summary>64 lines</summary>

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
64.
```

</details>


---

<sub>⏱️ 1m 5s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\contracts.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\contracts.ts

<details>
<summary>73 lines</summary>

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
73.
```

</details>


---

<sub>⏱️ 1m 5s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\api\client.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\api\client.ts

<details>
<summary>104 lines</summary>

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
104.
```

</details>


---

<sub>⏱️ 1m 5s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\api\types.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\api\types.ts

<details>
<summary>47 lines</summary>

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
47.
```

</details>


---

<sub>⏱️ 1m 5s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\pages\preferences.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\pages\preferences.ts

<details>
<summary>41 lines</summary>

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
41.
```

</details>


---

<sub>⏱️ 1m 5s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\components\notification-toggle.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\components\notification-toggle.ts

<details>
<summary>46 lines</summary>

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
46.
```

</details>


---

<sub>⏱️ 1m 14s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\models\types.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\models\types.ts

<details>
<summary>112 lines</summary>

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
112.
```

</details>


---

<sub>⏱️ 1m 14s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\models\preference-repository.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\models\preference-repository.ts

<details>
<summary>86 lines</summary>

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
86.
```

</details>


---

<sub>⏱️ 1m 14s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\config\feature-flags.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\config\feature-flags.ts

<details>
<summary>28 lines</summary>

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
28.
```

</details>


---

<sub>⏱️ 1m 14s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue

```
broker.ts
contracts.ts
handlers
```


---

<sub>⏱️ 1m 14s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\main.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\main.ts

<details>
<summary>59 lines</summary>

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
59.
```

</details>


---

<sub>⏱️ 1m 14s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\components\app-shell.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\components\app-shell.ts

<details>
<summary>59 lines</summary>

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
59.
```

</details>


---

<sub>⏱️ 1m 14s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\app.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\app.ts

<details>
<summary>82 lines</summary>

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
82.
```

</details>


---

<sub>⏱️ 1m 14s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\adr.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\adr

```
ADR-003-frontend-state.md
```


---

<sub>⏱️ 1m 24s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "preference\\.read\\.failure|preference\\.save\\.failure|audit\\.write\\.failure|notification\\.sms\\.fallback|preference\\.save\\.latency|metric|telemetry|observability",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\04-planning-workflows\\src",
  "output_mode": "content",
  "-n": true,
  "head_limit": 200
}
```

</details>

```
No matches found.
```


---

<sub>⏱️ 1m 24s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers

```
audit-handler.ts
notification-handler.ts
```


---

<sub>⏱️ 1m 24s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers\notification-handler.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers\notification-handler.ts

<details>
<summary>87 lines</summary>

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
87.
```

</details>


---

<sub>⏱️ 1m 24s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers\audit-handler.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers\audit-handler.ts

<details>
<summary>60 lines</summary>

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
60.
```

</details>


---

<sub>⏱️ 1m 24s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\error-handler.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\error-handler.ts

<details>
<summary>37 lines</summary>

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
37.
```

</details>


---

<sub>⏱️ 1m 24s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\audit.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\audit.ts

<details>
<summary>36 lines</summary>

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
36.
```

</details>


---

<sub>⏱️ 1m 32s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\pages\dashboard.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\pages\dashboard.ts

<details>
<summary>59 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Dashboard Page
3. // ---------------------------------------------------------------------------
4. // Shows all loan applications in a table with branded summary stats.
5. // ---------------------------------------------------------------------------
6. 
7. import { getApplications } from "../api/client.js";
8. import { renderLoanTable } from "../components/loan-table.js";
9. 
10. export async function renderDashboard(container: HTMLElement): Promise<void> {
11.   container.innerHTML = `<p class="loading">Loading applications\u2026</p>`;
12. 
13.   try {
14.     const loans = await getApplications();
15. 
16.     const stats = {
17.       total: loans.length,
18.       intake: loans.filter((l) => l.status === "intake").length,
19.       underwriting: loans.filter((l) => l.status === "underwriting").length,
20.       finalized: loans.filter((l) => l.status === "finalized").length,
21.     };
22. 
23.     container.innerHTML = `
24.       <section class="dashboard">
25.         <div class="page-header">
26.           <h2>Loan Applications</h2>
27.           <p>Overview of all applications and their current status.</p>
28.         </div>
29.         <div class="stats-bar">
30.           <div class="stat">
31.             <span class="stat-value">${stats.total}</span>
32.             <span class="stat-label">Total</span>
33.           </div>
34.           <div class="stat">
35.             <span class="stat-value">${stats.intake}</span>
36.             <span class="stat-label">Intake</span>
37.           </div>
38.           <div class="stat">
39.             <span class="stat-value">${stats.underwriting}</span>
40.             <span class="stat-label">Underwriting</span>
41.           </div>
42.           <div class="stat">
43.             <span class="stat-value">${stats.finalized}</span>
44.             <span class="stat-label">Finalized</span>
45.           </div>
46.         </div>
47.         <div id="loan-table-container"></div>
48.       </section>
49.     `;
50. 
51.     const tableContainer = container.querySelector<HTMLElement>(
52.       "#loan-table-container",
53.     )!;
54.     renderLoanTable(tableContainer, loans);
55.   } catch (err) {
56.     container.innerHTML = `<p class="error">Failed to load applications: ${(err as Error).message}</p>`;
57.   }
58. }
59.
```

</details>


---

<sub>⏱️ 1m 32s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\pages\application-detail.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src\pages\application-detail.ts

<details>
<summary>117 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Application Detail Page
3. // ---------------------------------------------------------------------------
4. // Shows a single loan application with its decisions and transition buttons.
5. // ---------------------------------------------------------------------------
6. 
7. import {
8.   getApplication,
9.   getDecisions,
10.   transitionApplication,
11. } from "../api/client.js";
12. import { renderStatusBadge } from "../components/status-badge.js";
13. 
14. const NEXT_STATES: Record<string, string[]> = {
15.   intake: ["review"],
16.   review: ["underwriting", "intake"],
17.   underwriting: ["decision"],
18.   decision: ["finalized", "underwriting"],
19.   finalized: [],
20. };
21. 
22. export async function renderApplicationDetail(
23.   container: HTMLElement,
24. ): Promise<void> {
25.   const params = new URLSearchParams(window.location.hash.split("?")[1] ?? "");
26.   const id = params.get("id");
27. 
28.   if (!id) {
29.     container.innerHTML = `<p class="error">No application ID specified.</p>`;
30.     return;
31.   }
32. 
33.   container.innerHTML = `<p class="loading">Loading application...</p>`;
34. 
35.   try {
36.     const [loan, decisions] = await Promise.all([
37.       getApplication(id),
38.       getDecisions(id),
39.     ]);
40.     const nextStates = NEXT_STATES[loan.status] ?? [];
41. 
42.     container.innerHTML = `
43.       <section class="application-detail">
44.         <div class="page-header">
45.           <h2>${loan.borrowerName}</h2>
46.           <p>${loan.id} · ${loan.loanState} · Assigned to ${loan.assignedUnderwriter}</p>
47.         </div>
48.         <div class="detail-grid">
49.           <div class="detail-field"><span class="field-label">ID</span><span class="field-value">${loan.id}</span></div>
50.           <div class="detail-field"><span class="field-label">Amount</span><span class="field-value">$${loan.amount.toLocaleString()}</span></div>
51.           <div class="detail-field"><span class="field-label">State</span><span class="field-value">${loan.loanState}</span></div>
52.           <div class="detail-field"><span class="field-label">Status</span><span class="field-value">${renderStatusBadge(loan.status)}</span></div>
53.           <div class="detail-field"><span class="field-label">Risk Score</span><span class="field-value">${loan.riskScore ?? "—"}</span></div>
54.           <div class="detail-field"><span class="field-label">Created</span><span class="field-value">${new Date(loan.createdAt).toLocaleDateString()}</span></div>
55.         </div>
56. 
57.         <div class="actions">
58.           ${
59.             nextStates.length === 0
60.               ? `<p class="subtitle">This application is finalized. No further transitions are available.</p>`
61.               : nextStates
62.                   .map(
63.                     (state) => `<button class="btn btn-primary transition-btn" data-next-state="${state}">Move to ${state}</button>`,
64.                   )
65.                   .join("")
66.           }
67.         </div>
68. 
69.         <h3>Decisions (${decisions.length})</h3>
70.         ${
71.           decisions.length === 0
72.             ? `<p class="empty-state">No decisions recorded.</p>`
73.             : decisions
74.                 .map(
75.                   (d) => `
76.             <div class="decision-card">
77.               <strong>${d.type}</strong> by ${d.decidedBy} on ${new Date(d.decidedAt).toLocaleDateString()}
78.               <p>${d.rationale}</p>
79.             </div>
80.           `,
81.                 )
82.                 .join("")
83.         }
84. 
85.         <div id="transition-actions" class="actions"></div>
86.       </section>
87.     `;
88. 
89.     container
90.       .querySelectorAll<HTMLButtonElement>(".transition-btn")
91.       .forEach((button) => {
92.         button.addEventListener("click", async () => {
93.           const nextState = button.dataset.nextState;
94.           if (!nextState) {
95.             return;
96.           }
97. 
98.           button.disabled = true;
99.           try {
100.             await transitionApplication(id, nextState);
101.             await renderApplicationDetail(container);
102.           } catch (err) {
103.             button.disabled = false;
104.             container
105.               .querySelector(".actions")
106.               ?.insertAdjacentHTML(
107.                 "beforeend",
108.                 `<p class="error">Failed to transition application: ${(err as Error).message}</p>`,
109.               );
110.           }
111.         });
112.       });
113.   } catch (err) {
114.     container.innerHTML = `<p class="error">Failed to load application: ${(err as Error).message}</p>`;
115.   }
116. }
117.
```

</details>


---

<sub>⏱️ 1m 32s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\loan-service.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\loan-service.ts

<details>
<summary>121 lines</summary>

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
121.
```

</details>


---

<sub>⏱️ 1m 32s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\applications.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\applications.ts

<details>
<summary>94 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Loan Application Routes
3. // ---------------------------------------------------------------------------
4. 
5. import { Router } from "express";
6. import { requireRole } from "../middleware/auth.js";
7. import { validateBody } from "../middleware/request-validator.js";
8. import { auditAction } from "../services/audit-service.js";
9. import * as loanService from "../services/loan-service.js";
10. import * as loanRepo from "../models/loan-repository.js";
11. import type { SessionContext, ApplicationState } from "../models/types.js";
12. 
13. export const applicationRoutes = Router();
14. 
15. function firstParam(value: string | string[]): string {
16.   return Array.isArray(value) ? value[0] : value;
17. }
18. 
19. /** GET /api/applications — list all applications. */
20. applicationRoutes.get(
21.   "/",
22.   requireRole("underwriter", "analyst-manager", "compliance-reviewer"),
23.   (req, res) => {
24.     const { status, underwriter } = req.query;
25.     if (status) {
26.       res.json(loanRepo.findLoansByStatus(status as ApplicationState));
27.     } else if (underwriter) {
28.       res.json(loanRepo.findLoansByUnderwriter(underwriter as string));
29.     } else {
30.       res.json(loanRepo.findAllLoans());
31.     }
32.   },
33. );
34. 
35. /** GET /api/applications/:id — get a single application. */
36. applicationRoutes.get(
37.   "/:id",
38.   requireRole("underwriter", "analyst-manager", "compliance-reviewer"),
39.   (req, res) => {
40.     const app = loanRepo.findLoanById(firstParam(req.params.id));
41.     if (!app) {
42.       res.status(404).json({ error: "Application not found." });
43.       return;
44.     }
45.     res.json(app);
46.   },
47. );
48. 
49. /** POST /api/applications — create a new loan application. */
50. applicationRoutes.post(
51.   "/",
52.   requireRole("underwriter", "analyst-manager"),
53.   validateBody([
54.     { field: "borrowerName", type: "string", required: true },
55.     { field: "amount", type: "number", required: true },
56.     { field: "loanState", type: "string", required: true },
57.   ]),
58.   (req, res, next) => {
59.     try {
60.       const session = req.session as SessionContext;
61.       const loan = loanService.createLoan(session, req.body);
62.       res.status(201).json(loan);
63.     } catch (err) {
64.       next(err);
65.     }
66.   },
67. );
68. 
69. /**
70.  * PATCH /api/applications/:id/status — transition application state.
71.  *
72.  * The request body must include `{ status: ApplicationState }`.
73.  * Only legal transitions (per VALID_TRANSITIONS) are allowed.
74.  * Finalized applications cannot be transitioned at all.
75.  */
76. applicationRoutes.patch(
77.   "/:id/status",
78.   requireRole("underwriter", "analyst-manager"),
79.   validateBody([{ field: "status", type: "string", required: true }]),
80.   (req, res, next) => {
81.     try {
82.       const session = req.session as SessionContext;
83.       const updated = loanService.transitionLoan(
84.         session,
85.         firstParam(req.params.id),
86.         req.body.status,
87.       );
88.       res.json(updated);
89.     } catch (err) {
90.       next(err);
91.     }
92.   },
93. );
94.
```

</details>


---

<sub>⏱️ 1m 32s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\decisions.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\decisions.ts

<details>
<summary>55 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Decision Routes
3. // ---------------------------------------------------------------------------
4. 
5. import { Router } from "express";
6. import { requireRole } from "../middleware/auth.js";
7. import { validateBody } from "../middleware/request-validator.js";
8. import * as decisionService from "../services/decision-service.js";
9. import type { SessionContext } from "../models/types.js";
10. 
11. export const decisionRoutes = Router();
12. 
13. function firstParam(value: string | string[]): string {
14.   return Array.isArray(value) ? value[0] : value;
15. }
16. 
17. /** GET /api/decisions/:applicationId — get decisions for an application. */
18. decisionRoutes.get(
19.   "/:applicationId",
20.   requireRole("underwriter", "analyst-manager", "compliance-reviewer"),
21.   (req, res) => {
22.     const decisions = decisionService.getDecisionsForApplication(
23.       firstParam(req.params.applicationId),
24.     );
25.     res.json(decisions);
26.   },
27. );
28. 
29. /** POST /api/decisions — record a new decision. */
30. decisionRoutes.post(
31.   "/",
32.   requireRole("underwriter", "analyst-manager"),
33.   validateBody([
34.     { field: "applicationId", type: "string", required: true },
35.     { field: "type", type: "string", required: true },
36.     { field: "rationale", type: "string", required: true },
37.   ]),
38.   (req, res, next) => {
39.     try {
40.       const session = req.session as SessionContext;
41.       const { applicationId, type, rationale, conditions } = req.body;
42.       const decision = decisionService.recordDecision(
43.         session,
44.         applicationId,
45.         type,
46.         rationale,
47.         conditions,
48.       );
49.       res.status(201).json(decision);
50.     } catch (err) {
51.       next(err);
52.     }
53.   },
54. );
55.
```

</details>


---

<sub>⏱️ 1m 40s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\planning-workflow-example.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\planning-workflow-example.md

<details>
<summary>61 lines</summary>

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
61.
```

</details>


---

<sub>⏱️ 1m 40s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "404|pilot|release flag|feature flag",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\04-planning-workflows\\src\\backend\\src",
  "output_mode": "content",
  "-n": true,
  "head_limit": 100
}
```

</details>

<details>
<summary>6 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\services\audit-service.ts:5:// to the message queue (or write directly depending on feature flags).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\business-rules.ts:14://   These rules are gated behind the `californiaRules` feature flag.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\config\feature-flags.ts:4:// Runtime feature flags that control business behavior.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\middleware\error-handler.ts:26:    res.status(404).json({ error: err.message });
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\routes\applications.ts:42:      res.status(404).json({ error: "Application not found." });
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\queue\handlers\notification-handler.ts:8://   When the SMS provider is unavailable and the feature flag is enabled,
```

</details>


---

<sub>⏱️ 1m 40s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\frontend\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "404|pilot|release flag|feature flag",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\04-planning-workflows\\src\\frontend\\src",
  "output_mode": "content",
  "-n": true,
  "head_limit": 100
}
```

</details>

```
No matches found.
```


---

<sub>⏱️ 1m 40s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\db**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "audit|preference|notification_preferences|audit_entries|retention",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\04-planning-workflows\\src\\backend\\src\\db",
  "output_mode": "content",
  "-n": true,
  "head_limit": 200
}
```

</details>

<details>
<summary>9 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\db\seed.ts:6:// finalized applications, and users without saved preferences.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\db\seed.ts:26:    `INSERT OR IGNORE INTO notification_preferences (user_id, event, channel, enabled, updated_at, updated_by)
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\db\seed.ts:36:    `INSERT OR IGNORE INTO audit_entries (id, action, actor, delegated_for, timestamp, previous_value, new_value, source)
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\db\seed.ts:117:    // u-3 intentionally has NO preferences → tests default behavior
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\db\schema.sql:44:CREATE TABLE IF NOT EXISTS notification_preferences (
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\db\schema.sql:54:CREATE TABLE IF NOT EXISTS audit_entries (
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\db\schema.sql:69:CREATE INDEX IF NOT EXISTS idx_preferences_user ON notification_preferences(user_id);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\db\schema.sql:70:CREATE INDEX IF NOT EXISTS idx_audit_actor ON audit_entries(actor);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\db\schema.sql:71:CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_entries(timestamp);
```

</details>


---

<sub>⏱️ 1m 40s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\db\schema.sql.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\db\schema.sql

<details>
<summary>72 lines</summary>

```
1. -- ---------------------------------------------------------------------------
2. -- Loan Workbench — Database Schema
3. -- ---------------------------------------------------------------------------
4. -- SQLite DDL for the Loan Workbench platform.
5. -- Run via: npm run db:seed (which executes seed.ts → creates tables + data)
6. --
7. -- IMPORTANT: When adding columns, create a new migration file in
8. -- db/migrations/ and update the seed.ts to apply it.  Never modify this
9. -- file directly for incremental changes — it represents the CURRENT schema.
10. -- ---------------------------------------------------------------------------
11. 
12. CREATE TABLE IF NOT EXISTS users (
13.     id          TEXT PRIMARY KEY,
14.     role        TEXT NOT NULL CHECK (role IN ('underwriter', 'analyst-manager', 'compliance-reviewer')),
15.     name        TEXT NOT NULL,
16.     email       TEXT NOT NULL UNIQUE,
17.     phone       TEXT,
18.     created_at  TEXT NOT NULL DEFAULT (datetime('now'))
19. );
20. 
21. CREATE TABLE IF NOT EXISTS loan_applications (
22.     id                    TEXT PRIMARY KEY,
23.     borrower_name         TEXT NOT NULL,
24.     amount                REAL NOT NULL CHECK (amount > 0),
25.     loan_state            TEXT NOT NULL,
26.     status                TEXT NOT NULL DEFAULT 'intake'
27.                           CHECK (status IN ('intake', 'review', 'underwriting', 'decision', 'finalized')),
28.     assigned_underwriter  TEXT NOT NULL REFERENCES users(id),
29.     risk_score            REAL,
30.     created_at            TEXT NOT NULL DEFAULT (datetime('now')),
31.     updated_at            TEXT NOT NULL DEFAULT (datetime('now'))
32. );
33. 
34. CREATE TABLE IF NOT EXISTS decisions (
35.     id              TEXT PRIMARY KEY,
36.     application_id  TEXT NOT NULL REFERENCES loan_applications(id),
37.     type            TEXT NOT NULL CHECK (type IN ('approved', 'declined', 'conditional')),
38.     rationale       TEXT NOT NULL,
39.     decided_by      TEXT NOT NULL REFERENCES users(id),
40.     decided_at      TEXT NOT NULL DEFAULT (datetime('now')),
41.     conditions      TEXT  -- JSON array, nullable
42. );
43. 
44. CREATE TABLE IF NOT EXISTS notification_preferences (
45.     user_id     TEXT NOT NULL REFERENCES users(id),
46.     event       TEXT NOT NULL CHECK (event IN ('approval', 'decline', 'document-request', 'manual-review-escalation')),
47.     channel     TEXT NOT NULL CHECK (channel IN ('email', 'sms')),
48.     enabled     INTEGER NOT NULL DEFAULT 1,
49.     updated_at  TEXT NOT NULL DEFAULT (datetime('now')),
50.     updated_by  TEXT NOT NULL,
51.     PRIMARY KEY (user_id, event, channel)
52. );
53. 
54. CREATE TABLE IF NOT EXISTS audit_entries (
55.     id              TEXT PRIMARY KEY,
56.     action          TEXT NOT NULL,
57.     actor           TEXT NOT NULL,
58.     delegated_for   TEXT,
59.     timestamp       TEXT NOT NULL DEFAULT (datetime('now')),
60.     previous_value  TEXT,  -- JSON
61.     new_value       TEXT,  -- JSON
62.     source          TEXT NOT NULL
63. );
64. 
65. -- Indexes for common queries
66. CREATE INDEX IF NOT EXISTS idx_applications_status ON loan_applications(status);
67. CREATE INDEX IF NOT EXISTS idx_applications_underwriter ON loan_applications(assigned_underwriter);
68. CREATE INDEX IF NOT EXISTS idx_decisions_application ON decisions(application_id);
69. CREATE INDEX IF NOT EXISTS idx_preferences_user ON notification_preferences(user_id);
70. CREATE INDEX IF NOT EXISTS idx_audit_actor ON audit_entries(actor);
71. CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_entries(timestamp);
72.
```

</details>


---

<sub>⏱️ 1m 45s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\business-rules.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\rules\business-rules.ts

<details>
<summary>84 lines</summary>

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
84.
```

</details>


---

<sub>⏱️ 1m 45s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\db\seed.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\db\seed.ts (lines 100-150)

<details>
<summary>51 lines</summary>

```
100.       "app-4",
101.       "Delta Co",
102.       75000,
103.       "TX",
104.       "finalized",
105.       "u-1",
106.       91.2,
107.       now,
108.       now,
109.     );
110. 
111.     // ── Notification Preferences ──
112.     insertPref.run("u-1", "approval", "email", 1, now, "u-1");
113.     insertPref.run("u-1", "approval", "sms", 1, now, "u-1");
114.     insertPref.run("u-1", "decline", "email", 1, now, "u-1");
115.     insertPref.run("u-2", "approval", "email", 1, now, "u-2");
116.     insertPref.run("u-2", "manual-review-escalation", "sms", 1, now, "u-2");
117.     // u-3 intentionally has NO preferences → tests default behavior
118. 
119.     // ── Decisions ──
120.     insertDecision.run(
121.       "dec-1",
122.       "app-3",
123.       "conditional",
124.       "High loan amount requires additional collateral verification.",
125.       "u-2",
126.       now,
127.       JSON.stringify(["Collateral appraisal", "Updated revenue statements"]),
128.     );
129.     insertDecision.run(
130.       "dec-2",
131.       "app-4",
132.       "approved",
133.       "Loan meets policy thresholds and required documentation is complete.",
134.       "u-2",
135.       now,
136.       null,
137.     );
138. 
139.     // ── Audit Trail ──
140.     insertAudit.run(
141.       "aud-1",
142.       "application.created",
143.       "u-1",
144.       null,
145.       now,
146.       null,
147.       JSON.stringify({ applicationId: "app-1", status: "underwriting" }),
148.       "seed-script",
149.     );
150.     insertAudit.run(
```

</details>


---

<sub>⏱️ 1m 45s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\models\audit-repository.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\src\models\audit-repository.ts

<details>
<summary>95 lines</summary>

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
95.
```

</details>


---

<sub>⏱️ 1m 45s</sub>

### ❌ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\package.json.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\backend\package.json

```
Path does not exist
```


---

<sub>⏱️ 1m 45s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\package.json.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\src\package.json

<details>
<summary>34 lines</summary>

```
1. {
2.   "name": "loan-workbench",
3.   "version": "1.0.0",
4.   "description": "Loan Workbench — commercial loan processing platform with backend API, embedded message queue, SQLite database, and web frontend.",
5.   "private": true,
6.   "type": "module",
7.   "scripts": {
8.     "dev": "concurrently -n api,web -c blue,green \"npm:dev:backend\" \"npm:dev:frontend\"",
9.     "dev:backend": "tsx watch backend/src/app.ts",
10.     "dev:frontend": "vite frontend --port 5173",
11.     "start": "node backend/dist/app.js",
12.     "build": "tsc -p tsconfig.json",
13.     "test": "vitest run",
14.     "test:watch": "vitest",
15.     "db:seed": "tsx backend/src/db/seed.ts",
16.     "lint": "eslint backend/src/ frontend/src/"
17.   },
18.   "dependencies": {
19.     "better-sqlite3": "^11.0.0",
20.     "express": "^4.21.0",
21.     "uuid": "^11.1.0"
22.   },
23.   "devDependencies": {
24.     "@types/better-sqlite3": "^7.6.0",
25.     "@types/express": "^5.0.0",
26.     "@types/node": "^22.0.0",
27.     "@types/uuid": "^10.0.0",
28.     "concurrently": "^9.0.0",
29.     "tsx": "^4.19.0",
30.     "typescript": "^5.7.0",
31.     "vite": "^6.0.0",
32.     "vitest": "^3.0.0"
33.   }
34. }
```

</details>


---

<sub>⏱️ 3m 41s</sub>

### 💬 Copilot

I’ve got enough source context now. I’m writing the plan file with explicit source citations, canonical-source notes, task sequencing, and the required edge-case callouts.

---

<sub>⏱️ 3m 41s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Add File: C:\\Users\\nilay\\.copilot\\session-state\\0b1cb144-3c12-4347-909a-85fc85baa317\\plan.md\n+# Session Plan\n+\n+1. Read lesson docs, ADR, specs, and current notification-related source surfaces.\n+2. Reconcile overlaps/conflicts and identify canonical sources for planning.\n+3. Draft `docs/notification-preferences-plan.md` with confirmed requirements, open questions, inferred choices, tasks, validation, and risks.\n+4. Save the plan without changing implementation code or using shell/SQL.\n*** Add File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\04-planning-workflows\\docs\\notification-preferences-plan.md\n+# Notification Preferences Implementation Plan\n+\n+## Summary\n+\n+This plan covers a pilot-gated notification-preferences feature for Loan Workbench that spans backend routes, rules, services, audit behavior, queue delivery, frontend state, and UX. The implementation must preserve mandatory-event delivery, block delegated-session writes, enforce the California decline-SMS restriction tracked in `LEGAL-218`, fail closed when audit logging is unavailable, preserve stored preferences during degraded-mode SMS-to-email fallback, and honor ADR-003 by using central store state for persisted preferences instead of component-local state.\n+\n+## Canonical sources and conflict handling\n+\n+### Canonical sources for this plan\n+\n+- **Behavioral requirements:** `specs/product-spec-notification-preferences.md` and `specs/non-functional-requirements.md` are canonical because they define the normalized `FR-*`, `SC-*`, and `NFR-*` requirements that this plan must trace.\n+- **Architecture and implementation constraints:** `docs/architecture.md` and `docs/adr/ADR-003-frontend-state.md` are canonical for lesson-specific structure, cross-layer responsibilities, and frontend state ownership.\n+- **Actual impact surfaces:** the current `src/**` code is canonical for file paths and current behavior because the product spec uses placeholder paths (`apps/web/`, `services/api/`) that do not match this lesson repo.\n+\n+### Overlaps and conflicts\n+\n+- `specs/feature-request.md` overlaps with the product spec but is a summary input, not the normative source, because it lacks the full FR/SC detail and open-question resolution.\n+- `specs/bug-report.md` is evidence of likely failure modes and missing guards, not a normative source of desired behavior.\n+- The product spec mentions `apps/web/` and `services/api/` (`specs/product-spec-notification-preferences.md:30-31`), but `docs/architecture.md:10-33` and the repository structure under `src/frontend/src/` and `src/backend/src/` are the canonical lesson paths.\n+\n+## Source-backed confirmed requirements\n+\n+### Confirmed product and UX requirements\n+\n+1. **Per-event, per-channel matrix is required.** Users configure `email` and `sms` independently for `approval`, `decline`, `document-request`, and `manual-review-escalation` (`FR-1`, `specs/product-spec-notification-preferences.md:68-80`).\n+2. **Mandatory-event delivery rule:** `manual-review-escalation` must always remain deliverable, meaning at least one channel stays enabled; disabling both channels is a hard negative and both UI and API must enforce it (`FR-2`, `specs/product-spec-notification-preferences.md:81-92`).\n+3. **Role-based defaults on first access:** underwriters and analyst managers default to all email events enabled plus SMS for escalation only, without a backfill migration; compliance reviewers are read-only and have no operational defaults (`FR-3`, `specs/product-spec-notification-preferences.md:94-104`; `NFR-6`, `specs/non-functional-requirements.md:84-97`).\n+4. **LEGAL-218 restriction:** decline SMS must remain unavailable for California loans; the rule is based on `loanState`, not borrower address, and mixed portfolio contexts must show conditional messaging instead of blanket disabling (`FR-4`, `specs/product-spec-notification-preferences.md:105-119`; `SC-3`, `specs/product-spec-notification-preferences.md:166-170`).\n+5. **Degraded-mode fallback:** when SMS is unavailable, delivery may fall back to email only if email is enabled; stored preferences must not change, and fallback needs a separate metric (`FR-5`, `specs/product-spec-notification-preferences.md:120-130`).\n+6. **Auditability:** each preference change must record actor, timestamp, previous value, new value, source channel, and delegated-for user when applicable (`FR-6`, `specs/product-spec-notification-preferences.md:132-142`).\n+7. **Delegated sessions are view-only:** an analyst manager acting for another user may view but not modify that user’s preferences; the UI must visibly indicate delegated mode and audit must capture both actor and delegated-for user (`SC-2`, `specs/product-spec-notification-preferences.md:153-165`).\n+8. **Finalized application nuance:** preference updates remain global, but the UI must explain that changes do not affect already queued notifications for finalized applications (`SC-1`, `specs/product-spec-notification-preferences.md:147-151`).\n+9. **Accessibility and feedback:** disabled controls need persistent helper text, not just tooltips, and save success/failure must be announced via ARIA live regions (`NFR-4`, `specs/non-functional-requirements.md:50-60`).\n+\n+### Confirmed architecture and implementation constraints\n+\n+10. **Typed client + route/rule/service split:** routes orchestrate, rules hold business logic, and services handle orchestration/I/O; plans must identify frontend, route, rule, service, audit, and observability surfaces (`docs/architecture.md:41-58`).\n+11. **Audit is mandatory for all writes** and may flow through queue broker or direct DB write, so preference writes cannot bypass audit coverage (`docs/architecture.md:41-47`).\n+12. **ADR-003 applies:** persisted user preferences must live in a central client store, and optimistic updates require rollback if the API rejects the write (`docs/adr/ADR-003-frontend-state.md:16-37`).\n+13. **Pilot rollout must hide the feature for non-pilot users with `404`, not `403`** (`NFR-6`, `specs/non-functional-requirements.md:84-95`).\n+14. **Reads tolerate downstream degradation, but writes fail closed when audit is unavailable** (`NFR-2`, `specs/non-functional-requirements.md:21-34`).\n+15. **Observability requirements are explicit:** emit `preference.read.failure`, `preference.save.failure`, `audit.write.failure`, `notification.sms.fallback`, and `preference.save.latency`, and distinguish validation failures from infrastructure failures in logs (`NFR-5`, `specs/non-functional-requirements.md:63-80`).\n+16. **Security/privacy constraints:** only authenticated internal users can access the endpoints, delegated sessions must be identified in audit logs, and sensitive SMS destination data must not appear in client logs or analytics (`NFR-3`, `specs/non-functional-requirements.md:38-47`).\n+17. **Compliance constraints:** audit retention is 24 months, mandatory escalation rules must be testable and documented, and compliance read-only views must show effective preferences including applied defaults (`NFR-7`, `specs/non-functional-requirements.md:101-110`).\n+\n+### Confirmed current implementation surfaces\n+\n+18. **Backend notification routes already exist** at `src/backend/src/routes/notifications.ts`, including GET and PUT endpoints plus bulk email/SMS endpoints (`src/backend/src/routes/notifications.ts:33-271`).\n+19. **Delegated-session detection already exists** in auth middleware via `x-delegated-for` and `SessionContext.delegatedFor` (`src/backend/src/middleware/auth.ts:61-75`; `src/backend/src/models/types.ts:59-68`).\n+20. **The notification delivery path already has a degraded-mode concept** in both the notification service and queue handler, including the requirement to preserve stored preferences during fallback (`src/backend/src/services/notification-service.ts:8-17`; `src/backend/src/queue/handlers/notification-handler.ts:7-12`).\n+21. **Mandatory events already exist for workflow transitions** through `getMandatoryEvents(...)`, which means the preference work must not accidentally suppress those deliveries (`src/backend/src/rules/mandatory-events.ts:16-37`; `src/backend/src/services/loan-service.ts:100-117`).\n+22. **The frontend currently renders direct toggle controls and calls the API client directly** from the component (`src/frontend/src/pages/preferences.ts:16-36`; `src/frontend/src/components/notification-toggle.ts:29-41`; `src/frontend/src/api/client.ts:83-97`).\n+\n+## Open questions with file references\n+\n+1. **Where should compliance reviewers see audit history?** The product spec leaves open whether this belongs on the same settings page or in a separate audit viewer (`specs/product-spec-notification-preferences.md:187-193`). The repo already has a separate audit route and queue/audit pages, which suggests an existing split (`src/backend/src/routes/audit.ts:17-35`; `docs/architecture.md:21,29-31`).\n+2. **How should loan context reach the preferences screen?** `FR-4` and `SC-3` require loan-state-aware restrictions and mixed-portfolio messaging, but the current preferences page only derives a `userId` from `#user-select` and has no application or portfolio context (`specs/product-spec-notification-preferences.md:105-119,166-170`; `src/frontend/src/pages/preferences.ts:13-18`; `src/frontend/src/components/app-shell.ts:26-31`).\n+3. **How should fail-closed audit semantics work when `queueAudit` is enabled?** Current queued audit handling explicitly does not roll back the original operation after audit failure, which conflicts with `NFR-2` for preference writes (`src/backend/src/services/audit-service.ts:18-45`; `src/backend/src/queue/handlers/audit-handler.ts:8-13`; `specs/non-functional-requirements.md:21-34`).\n+4. **Should the bulk `/preferences/:userId/email` and `/sms` endpoints remain part of the pilot scope?** The product spec requires a matrix and per-event/per-channel rules, but it does not require channel-wide bulk toggles; bulk writes may complicate FR-2 and FR-4 enforcement (`specs/product-spec-notification-preferences.md:68-92,105-119`; `src/backend/src/routes/notifications.ts:107-271`).\n+5. **What is the pilot gating surface?** `NFR-6` requires a release flag and `404` for non-pilot users, but the current feature flag set does not include a notification-preferences pilot flag (`specs/non-functional-requirements.md:84-95`; `src/backend/src/config/feature-flags.ts:16-25`).\n+\n+## Inferred implementation choices\n+\n+The items below are planning recommendations, not confirmed requirements.\n+\n+1. **Add a dedicated notification-preferences release flag** in backend config and apply it at both route and frontend-navigation entry points, returning `404` from API endpoints and hiding the navigation affordance for non-pilot users. This is inferred from `NFR-6` and the existing feature-flag pattern in `src/backend/src/config/feature-flags.ts`.\n+2. **Introduce a frontend preference store module** under `src/frontend/src/` and move read/update state out of `renderNotificationToggle(...)` so the page follows ADR-003 instead of component-local state.\n+3. **Treat the general `PUT /api/notifications/preferences` endpoint as the canonical write path** for the matrix UI and either remove, hide, or narrowly constrain the bulk email/SMS endpoints during pilot to reduce rule-bypass risk.\n+4. **Add backend rule helpers for preference validation** rather than embedding FR-2 and FR-4 checks in routes, because `docs/architecture.md` says business rules belong in `src/backend/src/rules/`.\n+5. **Materialize effective preferences at read time** by combining stored rows with role defaults when no explicit record exists, instead of backfilling all missing rows. This matches `FR-3` and `NFR-6`.\n+6. **Make preference writes synchronously audit-safe** either by forcing direct audit writes for this feature or by changing the queued audit path to provide write-time durability/acknowledgement before the preference save is committed. This is inferred to satisfy `NFR-2`.\n+7. **Represent UI restrictions as metadata from the API or store selectors** so the frontend can render persistent helper text for delegated mode, mandatory-event rules, and `LEGAL-218` without duplicating backend logic.\n+\n+## Constraints and special conditions\n+\n+- **Delegated sessions:** view-only in delegated mode; no success-shaped fallback or optimistic success toast on rejected writes (`SC-2`, `specs/product-spec-notification-preferences.md:153-165`; bug example in `specs/bug-report.md:20-27,47-56`).\n+- **LEGAL-218:** decline SMS is unavailable for California loans and must be explained inline; the rule keys off `loanState` (`FR-4`, `specs/product-spec-notification-preferences.md:105-119`).\n+- **Mandatory-event delivery:** preference changes must not suppress `manual-review-escalation` below one enabled channel, and transition-driven mandatory events must still emit from the loan workflow (`FR-2`, `specs/product-spec-notification-preferences.md:81-92`; `src/backend/src/rules/mandatory-events.ts:16-37`; `src/backend/src/services/loan-service.ts:100-117`).\n+- **Fail-closed audit behavior:** preference writes must be rejected if audit cannot be recorded; current async queue-audit behavior is not sufficient for this feature (`NFR-2`, `specs/non-functional-requirements.md:21-34`; `src/backend/src/queue/handlers/audit-handler.ts:8-13`).\n+- **Degraded-mode fallback:** SMS outage may deliver by email when allowed, but the stored preference model must remain unchanged and fallback must be separately observable (`FR-5`, `specs/product-spec-notification-preferences.md:120-130`; `src/backend/src/queue/handlers/notification-handler.ts:62-71`).\n+- **Pilot hiding:** non-pilot users must see no change; API should return `404`, not `403` (`NFR-6`, `specs/non-functional-requirements.md:84-95`).\n+- **Accessibility:** disabled controls need persistent explanatory text and save outcomes need ARIA announcements (`NFR-4`, `specs/non-functional-requirements.md:50-60`).\n+- **Finalized applications:** preferences stay global, but the UI must clarify that queued notifications for finalized applications are unaffected (`SC-1`, `specs/product-spec-notification-preferences.md:147-151`).\n+- **Security/privacy:** avoid client-side logging of sensitive operational data; the current toggle component’s `console.error(...)` should not evolve into logging full preference or phone metadata (`NFR-3`, `specs/non-functional-requirements.md:38-47`; `src/frontend/src/components/notification-toggle.ts:37-40`).\n+\n+## False positives and hard negatives to protect against\n+\n+### False positives\n+\n+- **False positive:** disabling escalation SMS while escalation email remains enabled is valid and must not be treated as a violation (`FR-2`, `specs/product-spec-notification-preferences.md:90-92`).\n+- **False positive:** preference reads succeeding during an audit-service outage are not a bug; only writes require audit availability (`NFR-2`, `specs/non-functional-requirements.md:33-34`).\n+- **False positive:** a user receiving email instead of SMS during an SMS outage is not a preference-store bug if fallback rules triggered (`FR-5`, `specs/product-spec-notification-preferences.md:128-130`).\n+\n+### Hard negatives\n+\n+- **Hard negative:** allowing both escalation channels to be disabled (`FR-2`, `specs/product-spec-notification-preferences.md:86-88`).\n+- **Hard negative:** enabling decline SMS for a California loan despite `LEGAL-218` (`FR-4`, `specs/product-spec-notification-preferences.md:117-118`).\n+- **Hard negative:** using `403` instead of `404` for hidden non-pilot endpoints (`NFR-6`, `specs/non-functional-requirements.md:92-95`).\n+- **Hard negative:** swallowing audit failure and persisting the preference anyway (`NFR-2`, `specs/non-functional-requirements.md:28-31`).\n+- **Hard negative:** delegated save appears successful in the UI but reverts on refresh (`SC-2`, `specs/product-spec-notification-preferences.md:162-164`; `specs/bug-report.md:14-18,49-56`).\n+\n+## Numbered tasks with acceptance criteria and source references\n+\n+1. **Define the pilot-gated backend contract and route guards.**\n+   - Acceptance criteria:\n+     - Notification-preferences endpoints are guarded by a dedicated release flag.\n+     - Non-pilot users receive `404`, not `403`.\n+     - Authenticated underwriters, analyst managers, and compliance reviewers can read when in pilot; only allowed write actors can proceed to validation.\n+   - Source references: `NFR-6` (`specs/non-functional-requirements.md:84-95`), `docs/architecture.md:41-47`, `src/backend/src/routes/notifications.ts:33-271`, `src/backend/src/config/feature-flags.ts:16-25`, `src/backend/src/middleware/auth.ts:78-97`.\n+\n+2. **Refactor backend preference validation into rule-layer functions.**\n+   - Acceptance criteria:\n+     - Backend rules enforce mandatory-event minimum-channel behavior for `manual-review-escalation`.\n+     - Backend rules enforce `LEGAL-218` based on `loanState`.\n+     - Validation logic is reusable by both single-cell and any retained bulk update path.\n+   - Source references: `FR-2` (`specs/product-spec-notification-preferences.md:81-92`), `FR-4` (`specs/product-spec-notification-preferences.md:105-119`), `docs/architecture.md:53-58`, `src/backend/src/routes/notifications.ts:45-105,107-271`.\n+\n+3. **Correct authorization semantics for ownership, delegated sessions, and compliance access.**\n+   - Acceptance criteria:\n+     - Delegated sessions can read but cannot write another user’s preferences.\n+     - Compliance reviewers remain read-only.\n+     - Write paths consistently reject non-owner preference changes unless the product later explicitly broadens scope.\n+     - Errors align with central error handling conventions.\n+   - Source references: `SC-2` (`specs/product-spec-notification-preferences.md:153-165`), `FR-6` (`specs/product-spec-notification-preferences.md:132-142`), `src/backend/src/middleware/auth.ts:61-75`, `src/backend/src/rules/role-permissions.ts:27-59`, `src/backend/src/routes/notifications.ts:55-73,123-145,206-228`, `src/backend/src/middleware/error-handler.ts:16-35`.\n+\n+4. **Implement effective-default reads without migration backfill.**\n+   - Acceptance criteria:\n+     - Users with no stored preferences receive role-based effective defaults on first read.\n+     - Compliance reviewers see effective read-only state including defaults.\n+     - No pre-backfill or migration is required to make the feature usable for existing users.\n+   - Source references: `FR-3` (`specs/product-spec-notification-preferences.md:94-104`), `NFR-6` (`specs/non-functional-requirements.md:89-97`), `NFR-7` (`specs/non-functional-requirements.md:103-107`), `src/backend/src/models/preference-repository.ts:31-77`, `src/backend/src/db/seed.ts:111-117`.\n+\n+5. **Make preference writes fail closed on audit unavailability.**\n+   - Acceptance criteria:\n+     - A preference write does not persist unless its audit record is durably accepted.\n+     - `audit.write.failure` is emitted/logged distinctly from validation failures.\n+     - Preference reads continue to work during audit outages.\n+   - Source references: `NFR-2` (`specs/non-functional-requirements.md:21-34`), `NFR-5` (`specs/non-functional-requirements.md:65-80`), `FR-6` (`specs/product-spec-notification-preferences.md:132-142`), `src/backend/src/services/audit-service.ts:18-45`, `src/backend/src/queue/handlers/audit-handler.ts:8-13`.\n+\n+6. **Preserve degraded-mode delivery semantics and observability.**\n+   - Acceptance criteria:\n+     - SMS outage triggers email fallback only when allowed by effective preferences.\n+     - Stored preference rows remain unchanged by fallback behavior.\n+     - `notification.sms.fallback` is emitted, and operational logs distinguish provider problems from user validation errors.\n+   - Source references: `FR-5` (`specs/product-spec-notification-preferences.md:120-130`), `NFR-5` (`specs/non-functional-requirements.md:65-80`), `src/backend/src/services/notification-service.ts:8-17`, `src/backend/src/queue/handlers/notification-handler.ts:56-76`.\n+\n+7. **Design the frontend state model and data flow around ADR-003.**\n+   - Acceptance criteria:\n+     - Persisted preference data is owned by a central client store, not individual toggle components.\n+     - Optimistic UI is allowed only with rollback support and explicit server-error handling.\n+     - The store tracks effective preferences, saving state, and delegated/read-only mode.\n+   - Source references: `ADR-003` (`docs/adr/ADR-003-frontend-state.md:16-37`), `specs/product-spec-notification-preferences.md:176-180`, `src/frontend/src/pages/preferences.ts:16-36`, `src/frontend/src/components/notification-toggle.ts:29-41`.\n+\n+8. **Redesign the preferences UI to match matrix, restriction, and accessibility requirements.**\n+   - Acceptance criteria:\n+     - The page renders a matrix by event and channel.\n+     - Mandatory events are visually marked with persistent explanatory text.\n+     - Delegated-session mode is visibly indicated and disables writes.\n+     - California decline SMS shows inline explanation tied to current loan context.\n+     - Success/failure feedback uses screen-reader-announced status messaging.\n+   - Source references: `FR-1` (`specs/product-spec-notification-preferences.md:68-80`), `FR-2` (`specs/product-spec-notification-preferences.md:81-92`), `FR-4` (`specs/product-spec-notification-preferences.md:105-119`), `SC-2` (`specs/product-spec-notification-preferences.md:153-165`), `NFR-4` (`specs/non-functional-requirements.md:50-60`), `src/frontend/src/pages/preferences.ts:19-35`, `src/frontend/src/components/app-shell.ts:20-31`.\n+\n+9. **Add loan-context and mixed-portfolio restriction handling to the UI/API boundary.**\n+   - Acceptance criteria:\n+     - The frontend can display conditional restrictions for California and mixed-state portfolio contexts without turning the global preference model into per-loan overrides.\n+     - The save request includes enough context for backend validation when a state-dependent rule applies, or the backend can resolve it from authoritative state.\n+     - Finalized-application messaging clarifies queued-notification behavior.\n+   - Source references: `FR-4` (`specs/product-spec-notification-preferences.md:110-115`), `SC-1` (`specs/product-spec-notification-preferences.md:147-151`), `SC-3` (`specs/product-spec-notification-preferences.md:166-170`), `specs/bug-report.md:60-63`, `src/frontend/src/pages/application-detail.ts:35-53`, `src/frontend/src/pages/preferences.ts:13-18`, `src/frontend/src/api/client.ts:87-97`.\n+\n+10. **Add automated coverage for rules, routes, delivery, and UX failure handling.**\n+    - Acceptance criteria:\n+      - Tests cover delegated read-only behavior, mandatory-event enforcement, California decline SMS restriction, effective defaults, fail-closed audit rejection, fallback-without-mutation, pilot `404` hiding, and optimistic rollback.\n+      - Release validation explicitly includes false-positive and hard-negative scenarios from the specs.\n+    - Source references: `docs/planning-workflow-example.md:53-60`, `FR-2` (`specs/product-spec-notification-preferences.md:86-92`), `FR-4` (`specs/product-spec-notification-preferences.md:117-118`), `FR-5` (`specs/product-spec-notification-preferences.md:128-130`), `SC-2` (`specs/product-spec-notification-preferences.md:162-164`), `NFR-2` (`specs/non-functional-requirements.md:28-34`), `NFR-6` (`specs/non-functional-requirements.md:92-97`), `src/backend/tests/unit/notification-service.test.ts:10-15`, `src/backend/tests/integration/decisions.test.ts:7-14`.\n+\n+## Validation steps\n+\n+1. **Backend rule tests**\n+   - Verify `manual-review-escalation` rejects zero enabled channels but accepts email-only and sms-only valid states.\n+   - Verify California decline SMS is rejected when `loanState === \"CA\"` and not rejected solely because borrower data differs.\n+\n+2. **Authorization and delegated-session tests**\n+   - Verify delegated sessions can fetch the delegate’s effective preferences but receive a write rejection.\n+   - Verify compliance reviewers can read but not write.\n+   - Verify non-owner direct writes are rejected if owner-only semantics are retained.\n+\n+3. **Pilot gating tests**\n+   - Verify non-pilot API reads/writes return `404`.\n+   - Verify pilot users with no stored rows still see effective defaults on first load.\n+\n+4. **Audit fail-closed tests**\n+   - Simulate audit unavailability and verify preference writes are rejected and not persisted.\n+   - Verify preference reads still succeed during the same outage.\n+   - Verify `audit.write.failure` and `preference.save.failure` are distinguishable.\n+\n+5. **Delivery fallback tests**\n+   - Simulate unhealthy SMS provider with email enabled and confirm fallback delivery occurs without mutating stored preferences.\n+   - Simulate unhealthy SMS provider with email disabled and confirm no silent preference mutation or misleading UX.\n+\n+6. **Frontend state and UX tests**\n+   - Verify the page renders a matrix, mandatory inline helper text, delegated-session banner, and ARIA-announced save status.\n+   - Verify optimistic rollback occurs on rejected saves and no false success toast/state persists.\n+   - Verify mixed-portfolio messaging is conditional, not blanket-disabled.\n+\n+7. **Regression checks against known nuanced cases**\n+   - **False positive check:** escalation SMS off + escalation email on remains valid.\n+   - **False positive check:** email delivery during SMS outage is not surfaced as a preference corruption bug.\n+   - **Hard negative check:** delegated save must never look successful.\n+   - **Hard negative check:** non-pilot hidden route must not leak via `403`.\n+\n+## Risks and dependencies\n+\n+### Risks\n+\n+- **Audit architecture mismatch:** current queued audit flow does not satisfy fail-closed semantics for preference writes; this is the largest implementation risk because it crosses service, queue, and persistence boundaries (`src/backend/src/services/audit-service.ts:18-45`; `src/backend/src/queue/handlers/audit-handler.ts:8-13`).\n+- **State/context mismatch in the UI:** current preferences page has no loan or portfolio context, but FR-4/SC-3 require conditional restriction messaging. Without a clear context source, the UI may either over-disable or under-enforce.\n+- **ADR-003 gap:** the current direct-toggle pattern bypasses a central store, increasing risk of repeated delegated-session false successes and inconsistent rollback behavior.\n+- **Bulk endpoint complexity:** channel-wide bulk updates can easily violate FR-2 or FR-4 unless rule evaluation is centralized and context-aware.\n+- **Observability gap:** no metrics surface is currently present in source for the required counters/histograms, so telemetry work may require introducing a common instrumentation surface.\n+\n+### Dependencies\n+\n+- Product decision on compliance-view placement (`specs/product-spec-notification-preferences.md:187-193`).\n+- Product/engineering decision on how the preferences page receives active application or mixed-portfolio context.\n+- Engineering decision on synchronous audit durability strategy when `queueAudit` is enabled.\n+- Release-management support for pilot flag rollout and checklist updates required by `NFR-7`.\n*** End Patch\n"
```

</details>

```
Added 2 file(s): C:\Users\nilay\.copilot\session-state\0b1cb144-3c12-4347-909a-85fc85baa317\plan.md, Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\notification-preferences-plan.md
```


---

<sub>⏱️ 3m 47s</sub>

### 💬 Copilot

The plan file is written. I’m doing a quick source-level sanity pass on the saved markdown to make sure the required sections and callouts are present.

---

<sub>⏱️ 3m 47s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\notification-preferences-plan.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\notification-preferences-plan.md (lines 1-260)

<details>
<summary>159 lines</summary>

```
1. # Notification Preferences Implementation Plan
2. 
3. ## Summary
4. 
5. This plan covers a pilot-gated notification-preferences feature for Loan Workbench that spans backend routes, rules, services, audit behavior, queue delivery, frontend state, and UX. The implementation must preserve mandatory-event delivery, block delegated-session writes, enforce the California decline-SMS restriction tracked in `LEGAL-218`, fail closed when audit logging is unavailable, preserve stored preferences during degraded-mode SMS-to-email fallback, and honor ADR-003 by using central store state for persisted preferences instead of component-local state.
6. 
7. ## Canonical sources and conflict handling
8. 
9. ### Canonical sources for this plan
10. 
11. - **Behavioral requirements:** `specs/product-spec-notification-preferences.md` and `specs/non-functional-requirements.md` are canonical because they define the normalized `FR-*`, `SC-*`, and `NFR-*` requirements that this plan must trace.
12. - **Architecture and implementation constraints:** `docs/architecture.md` and `docs/adr/ADR-003-frontend-state.md` are canonical for lesson-specific structure, cross-layer responsibilities, and frontend state ownership.
13. - **Actual impact surfaces:** the current `src/**` code is canonical for file paths and current behavior because the product spec uses placeholder paths (`apps/web/`, `services/api/`) that do not match this lesson repo.
14. 
15. ### Overlaps and conflicts
16. 
17. - `specs/feature-request.md` overlaps with the product spec but is a summary input, not the normative source, because it lacks the full FR/SC detail and open-question resolution.
18. - `specs/bug-report.md` is evidence of likely failure modes and missing guards, not a normative source of desired behavior.
19. - The product spec mentions `apps/web/` and `services/api/` (`specs/product-spec-notification-preferences.md:30-31`), but `docs/architecture.md:10-33` and the repository structure under `src/frontend/src/` and `src/backend/src/` are the canonical lesson paths.
20. 
21. ## Source-backed confirmed requirements
22. 
23. ### Confirmed product and UX requirements
24. 
25. 1. **Per-event, per-channel matrix is required.** Users configure `email` and `sms` independently for `approval`, `decline`, `document-request`, and `manual-review-escalation` (`FR-1`, `specs/product-spec-notification-preferences.md:68-80`).
26. 2. **Mandatory-event delivery rule:** `manual-review-escalation` must always remain deliverable, meaning at least one channel stays enabled; disabling both channels is a hard negative and both UI and API must enforce it (`FR-2`, `specs/product-spec-notification-preferences.md:81-92`).
27. 3. **Role-based defaults on first access:** underwriters and analyst managers default to all email events enabled plus SMS for escalation only, without a backfill migration; compliance reviewers are read-only and have no operational defaults (`FR-3`, `specs/product-spec-notification-preferences.md:94-104`; `NFR-6`, `specs/non-functional-requirements.md:84-97`).
28. 4. **LEGAL-218 restriction:** decline SMS must remain unavailable for California loans; the rule is based on `loanState`, not borrower address, and mixed portfolio contexts must show conditional messaging instead of blanket disabling (`FR-4`, `specs/product-spec-notification-preferences.md:105-119`; `SC-3`, `specs/product-spec-notification-preferences.md:166-170`).
29. 5. **Degraded-mode fallback:** when SMS is unavailable, delivery may fall back to email only if email is enabled; stored preferences must not change, and fallback needs a separate metric (`FR-5`, `specs/product-spec-notification-preferences.md:120-130`).
30. 6. **Auditability:** each preference change must record actor, timestamp, previous value, new value, source channel, and delegated-for user when applicable (`FR-6`, `specs/product-spec-notification-preferences.md:132-142`).
31. 7. **Delegated sessions are view-only:** an analyst manager acting for another user may view but not modify that user’s preferences; the UI must visibly indicate delegated mode and audit must capture both actor and delegated-for user (`SC-2`, `specs/product-spec-notification-preferences.md:153-165`).
32. 8. **Finalized application nuance:** preference updates remain global, but the UI must explain that changes do not affect already queued notifications for finalized applications (`SC-1`, `specs/product-spec-notification-preferences.md:147-151`).
33. 9. **Accessibility and feedback:** disabled controls need persistent helper text, not just tooltips, and save success/failure must be announced via ARIA live regions (`NFR-4`, `specs/non-functional-requirements.md:50-60`).
34. 
35. ### Confirmed architecture and implementation constraints
36. 
37. 10. **Typed client + route/rule/service split:** routes orchestrate, rules hold business logic, and services handle orchestration/I/O; plans must identify frontend, route, rule, service, audit, and observability surfaces (`docs/architecture.md:41-58`).
38. 11. **Audit is mandatory for all writes** and may flow through queue broker or direct DB write, so preference writes cannot bypass audit coverage (`docs/architecture.md:41-47`).
39. 12. **ADR-003 applies:** persisted user preferences must live in a central client store, and optimistic updates require rollback if the API rejects the write (`docs/adr/ADR-003-frontend-state.md:16-37`).
40. 13. **Pilot rollout must hide the feature for non-pilot users with `404`, not `403`** (`NFR-6`, `specs/non-functional-requirements.md:84-95`).
41. 14. **Reads tolerate downstream degradation, but writes fail closed when audit is unavailable** (`NFR-2`, `specs/non-functional-requirements.md:21-34`).
42. 15. **Observability requirements are explicit:** emit `preference.read.failure`, `preference.save.failure`, `audit.write.failure`, `notification.sms.fallback`, and `preference.save.latency`, and distinguish validation failures from infrastructure failures in logs (`NFR-5`, `specs/non-functional-requirements.md:63-80`).
43. 16. **Security/privacy constraints:** only authenticated internal users can access the endpoints, delegated sessions must be identified in audit logs, and sensitive SMS destination data must not appear in client logs or analytics (`NFR-3`, `specs/non-functional-requirements.md:38-47`).
44. 17. **Compliance constraints:** audit retention is 24 months, mandatory escalation rules must be testable and documented, and compliance read-only views must show effective preferences including applied defaults (`NFR-7`, `specs/non-functional-requirements.md:101-110`).
45. 
46. ### Confirmed current implementation surfaces
47. 
48. 18. **Backend notification routes already exist** at `src/backend/src/routes/notifications.ts`, including GET and PUT endpoints plus bulk email/SMS endpoints (`src/backend/src/routes/notifications.ts:33-271`).
49. 19. **Delegated-session detection already exists** in auth middleware via `x-delegated-for` and `SessionContext.delegatedFor` (`src/backend/src/middleware/auth.ts:61-75`; `src/backend/src/models/types.ts:59-68`).
50. 20. **The notification delivery path already has a degraded-mode concept** in both the notification service and queue handler, including the requirement to preserve stored preferences during fallback (`src/backend/src/services/notification-service.ts:8-17`; `src/backend/src/queue/handlers/notification-handler.ts:7-12`).
51. 21. **Mandatory events already exist for workflow transitions** through `getMandatoryEvents(...)`, which means the preference work must not accidentally suppress those deliveries (`src/backend/src/rules/mandatory-events.ts:16-37`; `src/backend/src/services/loan-service.ts:100-117`).
52. 22. **The frontend currently renders direct toggle controls and calls the API client directly** from the component (`src/frontend/src/pages/preferences.ts:16-36`; `src/frontend/src/components/notification-toggle.ts:29-41`; `src/frontend/src/api/client.ts:83-97`).
53. 
54. ## Open questions with file references
55. 
56. 1. **Where should compliance reviewers see audit history?** The product spec leaves open whether this belongs on the same settings page or in a separate audit viewer (`specs/product-spec-notification-preferences.md:187-193`). The repo already has a separate audit route and queue/audit pages, which suggests an existing split (`src/backend/src/routes/audit.ts:17-35`; `docs/architecture.md:21,29-31`).
57. 2. **How should loan context reach the preferences screen?** `FR-4` and `SC-3` require loan-state-aware restrictions and mixed-portfolio messaging, but the current preferences page only derives a `userId` from `#user-select` and has no application or portfolio context (`specs/product-spec-notification-preferences.md:105-119,166-170`; `src/frontend/src/pages/preferences.ts:13-18`; `src/frontend/src/components/app-shell.ts:26-31`).
58. 3. **How should fail-closed audit semantics work when `queueAudit` is enabled?** Current queued audit handling explicitly does not roll back the original operation after audit failure, which conflicts with `NFR-2` for preference writes (`src/backend/src/services/audit-service.ts:18-45`; `src/backend/src/queue/handlers/audit-handler.ts:8-13`; `specs/non-functional-requirements.md:21-34`).
59. 4. **Should the bulk `/preferences/:userId/email` and `/sms` endpoints remain part of the pilot scope?** The product spec requires a matrix and per-event/per-channel rules, but it does not require channel-wide bulk toggles; bulk writes may complicate FR-2 and FR-4 enforcement (`specs/product-spec-notification-preferences.md:68-92,105-119`; `src/backend/src/routes/notifications.ts:107-271`).
60. 5. **What is the pilot gating surface?** `NFR-6` requires a release flag and `404` for non-pilot users, but the current feature flag set does not include a notification-preferences pilot flag (`specs/non-functional-requirements.md:84-95`; `src/backend/src/config/feature-flags.ts:16-25`).
61. 
62. ## Inferred implementation choices
63. 
64. The items below are planning recommendations, not confirmed requirements.
65. 
66. 1. **Add a dedicated notification-preferences release flag** in backend config and apply it at both route and frontend-navigation entry points, returning `404` from API endpoints and hiding the navigation affordance for non-pilot users. This is inferred from `NFR-6` and the existing feature-flag pattern in `src/backend/src/config/feature-flags.ts`.
67. 2. **Introduce a frontend preference store module** under `src/frontend/src/` and move read/update state out of `renderNotificationToggle(...)` so the page follows ADR-003 instead of component-local state.
68. 3. **Treat the general `PUT /api/notifications/preferences` endpoint as the canonical write path** for the matrix UI and either remove, hide, or narrowly constrain the bulk email/SMS endpoints during pilot to reduce rule-bypass risk.
69. 4. **Add backend rule helpers for preference validation** rather than embedding FR-2 and FR-4 checks in routes, because `docs/architecture.md` says business rules belong in `src/backend/src/rules/`.
70. 5. **Materialize effective preferences at read time** by combining stored rows with role defaults when no explicit record exists, instead of backfilling all missing rows. This matches `FR-3` and `NFR-6`.
71. 6. **Make preference writes synchronously audit-safe** either by forcing direct audit writes for this feature or by changing the queued audit path to provide write-time durability/acknowledgement before the preference save is committed. This is inferred to satisfy `NFR-2`.
72. 7. **Represent UI restrictions as metadata from the API or store selectors** so the frontend can render persistent helper text for delegated mode, mandatory-event rules, and `LEGAL-218` without duplicating backend logic.
73. 
74. ## Constraints and special conditions
75. 
76. - **Delegated sessions:** view-only in delegated mode; no success-shaped fallback or optimistic success toast on rejected writes (`SC-2`, `specs/product-spec-notification-preferences.md:153-165`; bug example in `specs/bug-report.md:20-27,47-56`).
77. - **LEGAL-218:** decline SMS is unavailable for California loans and must be explained inline; the rule keys off `loanState` (`FR-4`, `specs/product-spec-notification-preferences.md:105-119`).
78. - **Mandatory-event delivery:** preference changes must not suppress `manual-review-escalation` below one enabled channel, and transition-driven mandatory events must still emit from the loan workflow (`FR-2`, `specs/product-spec-notification-preferences.md:81-92`; `src/backend/src/rules/mandatory-events.ts:16-37`; `src/backend/src/services/loan-service.ts:100-117`).
79. - **Fail-closed audit behavior:** preference writes must be rejected if audit cannot be recorded; current async queue-audit behavior is not sufficient for this feature (`NFR-2`, `specs/non-functional-requirements.md:21-34`; `src/backend/src/queue/handlers/audit-handler.ts:8-13`).
80. - **Degraded-mode fallback:** SMS outage may deliver by email when allowed, but the stored preference model must remain unchanged and fallback must be separately observable (`FR-5`, `specs/product-spec-notification-preferences.md:120-130`; `src/backend/src/queue/handlers/notification-handler.ts:62-71`).
81. - **Pilot hiding:** non-pilot users must see no change; API should return `404`, not `403` (`NFR-6`, `specs/non-functional-requirements.md:84-95`).
82. - **Accessibility:** disabled controls need persistent explanatory text and save outcomes need ARIA announcements (`NFR-4`, `specs/non-functional-requirements.md:50-60`).
83. - **Finalized applications:** preferences stay global, but the UI must clarify that queued notifications for finalized applications are unaffected (`SC-1`, `specs/product-spec-notification-preferences.md:147-151`).
84. - **Security/privacy:** avoid client-side logging of sensitive operational data; the current toggle component’s `console.error(...)` should not evolve into logging full preference or phone metadata (`NFR-3`, `specs/non-functional-requirements.md:38-47`; `src/frontend/src/components/notification-toggle.ts:37-40`).
85. 
86. ## False positives and hard negatives to protect against
87. 
88. ### False positives
89. 
90. - **False positive:** disabling escalation SMS while escalation email remains enabled is valid and must not be treated as a violation (`FR-2`, `specs/product-spec-notification-preferences.md:90-92`).
91. - **False positive:** preference reads succeeding during an audit-service outage are not a bug; only writes require audit availability (`NFR-2`, `specs/non-functional-requirements.md:33-34`).
92. - **False positive:** a user receiving email instead of SMS during an SMS outage is not a preference-store bug if fallback rules triggered (`FR-5`, `specs/product-spec-notification-preferences.md:128-130`).
93. 
94. ### Hard negatives
95. 
96. - **Hard negative:** allowing both escalation channels to be disabled (`FR-2`, `specs/product-spec-notification-preferences.md:86-88`).
97. - **Hard negative:** enabling decline SMS for a California loan despite `LEGAL-218` (`FR-4`, `specs/product-spec-notification-preferences.md:117-118`).
98. - **Hard negative:** using `403` instead of `404` for hidden non-pilot endpoints (`NFR-6`, `specs/non-functional-requirements.md:92-95`).
99. - **Hard negative:** swallowing audit failure and persisting the preference anyway (`NFR-2`, `specs/non-functional-requirements.md:28-31`).
100. - **Hard negative:** delegated save appears successful in the UI but reverts on refresh (`SC-2`, `specs/product-spec-notification-preferences.md:162-164`; `specs/bug-report.md:14-18,49-56`).
101. 
102. ## Numbered tasks with acceptance criteria and source references
103. 
104. 1. **Define the pilot-gated backend contract and route guards.**
105.    - Acceptance criteria:
106.      - Notification-preferences endpoints are guarded by a dedicated release flag.
107.      - Non-pilot users receive `404`, not `403`.
108.      - Authenticated underwriters, analyst managers, and compliance reviewers can read when in pilot; only allowed write actors can proceed to validation.
109.    - Source references: `NFR-6` (`specs/non-functional-requirements.md:84-95`), `docs/architecture.md:41-47`, `src/backend/src/routes/notifications.ts:33-271`, `src/backend/src/config/feature-flags.ts:16-25`, `src/backend/src/middleware/auth.ts:78-97`.
110. 
111. 2. **Refactor backend preference validation into rule-layer functions.**
112.    - Acceptance criteria:
113.      - Backend rules enforce mandatory-event minimum-channel behavior for `manual-review-escalation`.
114.      - Backend rules enforce `LEGAL-218` based on `loanState`.
115.      - Validation logic is reusable by both single-cell and any retained bulk update path.
116.    - Source references: `FR-2` (`specs/product-spec-notification-preferences.md:81-92`), `FR-4` (`specs/product-spec-notification-preferences.md:105-119`), `docs/architecture.md:53-58`, `src/backend/src/routes/notifications.ts:45-105,107-271`.
117. 
118. 3. **Correct authorization semantics for ownership, delegated sessions, and compliance access.**
119.    - Acceptance criteria:
120.      - Delegated sessions can read but cannot write another user’s preferences.
121.      - Compliance reviewers remain read-only.
122.      - Write paths consistently reject non-owner preference changes unless the product later explicitly broadens scope.
123.      - Errors align with central error handling conventions.
124.    - Source references: `SC-2` (`specs/product-spec-notification-preferences.md:153-165`), `FR-6` (`specs/product-spec-notification-preferences.md:132-142`), `src/backend/src/middleware/auth.ts:61-75`, `src/backend/src/rules/role-permissions.ts:27-59`, `src/backend/src/routes/notifications.ts:55-73,123-145,206-228`, `src/backend/src/middleware/error-handler.ts:16-35`.
125. 
126. 4. **Implement effective-default reads without migration backfill.**
127.    - Acceptance criteria:
128.      - Users with no stored preferences receive role-based effective defaults on first read.
129.      - Compliance reviewers see effective read-only state including defaults.
130.      - No pre-backfill or migration is required to make the feature usable for existing users.
131.    - Source references: `FR-3` (`specs/product-spec-notification-preferences.md:94-104`), `NFR-6` (`specs/non-functional-requirements.md:89-97`), `NFR-7` (`specs/non-functional-requirements.md:103-107`), `src/backend/src/models/preference-repository.ts:31-77`, `src/backend/src/db/seed.ts:111-117`.
132. 
133. 5. **Make preference writes fail closed on audit unavailability.**
134.    - Acceptance criteria:
135.      - A preference write does not persist unless its audit record is durably accepted.
136.      - `audit.write.failure` is emitted/logged distinctly from validation failures.
137.      - Preference reads continue to work during audit outages.
138.    - Source references: `NFR-2` (`specs/non-functional-requirements.md:21-34`), `NFR-5` (`specs/non-functional-requirements.md:65-80`), `FR-6` (`specs/product-spec-notification-preferences.md:132-142`), `src/backend/src/services/audit-service.ts:18-45`, `src/backend/src/queue/handlers/audit-handler.ts:8-13`.
139. 
140. 6. **Preserve degraded-mode delivery semantics and observability.**
141.    - Acceptance criteria:
142.      - SMS outage triggers email fallback only when allowed by effective preferences.
143.      - Stored preference rows remain unchanged by fallback behavior.
144.      - `notification.sms.fallback` is emitted, and operational logs distinguish provider problems from user validation errors.
145.    - Source references: `FR-5` (`specs/product-spec-notification-preferences.md:120-130`), `NFR-5` (`specs/non-functional-requirements.md:65-80`), `src/backend/src/services/notification-service.ts:8-17`, `src/backend/src/queue/handlers/notification-handler.ts:56-76`.
146. 
147. 7. **Design the frontend state model and data flow around ADR-003.**
148.    - Acceptance criteria:
149.      - Persisted preference data is owned by a central client store, not individual toggle components.
150.      - Optimistic UI is allowed only with rollback support and explicit server-error handling.
151.      - The store tracks effective preferences, saving state, and delegated/read-only mode.
152.    - Source references: `ADR-003` (`docs/adr/ADR-003-frontend-state.md:16-37`), `specs/product-spec-notification-preferences.md:176-180`, `src/frontend/src/pages/preferences.ts:16-36`, `src/frontend/src/components/notification-toggle.ts:29-41`.
153. 
154. 8. **Redesign the preferences UI to match matrix, restriction, and accessibility requirements.**
155.    - Acceptance criteria:
156.      - The page renders a matrix by event and channel.
157.      - Mandatory events are visually marked with persistent explanatory text.
158.      - Delegated-session mode is visibly indicated and disables writes.

[Output truncated. Use view_range=[159, ...] to continue reading.]
```

</details>


---

<sub>⏱️ 3m 47s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\notification-preferences-plan.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\notification-preferences-plan.md (lines 261-520)

<details>
<summary>5 lines</summary>

```diff

diff --git a/Y:/.sources/localm-tuts/courses/_examples/ctx-sdlc/lessons/04-planning-workflows/docs/notification-preferences-plan.md b/Y:/.sources/localm-tuts/courses/_examples/ctx-sdlc/lessons/04-planning-workflows/docs/notification-preferences-plan.md
index 0000000..0000000 100644
--- a/Y:/.sources/localm-tuts/courses/_examples/ctx-sdlc/lessons/04-planning-workflows/docs/notification-preferences-plan.md
+++ b/Y:/.sources/localm-tuts/courses/_examples/ctx-sdlc/lessons/04-planning-workflows/docs/notification-preferences-plan.md
@@ -261,260 +261,260 @@
```

</details>


---

<sub>⏱️ 3m 52s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\notification-preferences-plan.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\docs\notification-preferences-plan.md (lines 159-260)

<details>
<summary>68 lines</summary>

```
159.      - California decline SMS shows inline explanation tied to current loan context.
160.      - Success/failure feedback uses screen-reader-announced status messaging.
161.    - Source references: `FR-1` (`specs/product-spec-notification-preferences.md:68-80`), `FR-2` (`specs/product-spec-notification-preferences.md:81-92`), `FR-4` (`specs/product-spec-notification-preferences.md:105-119`), `SC-2` (`specs/product-spec-notification-preferences.md:153-165`), `NFR-4` (`specs/non-functional-requirements.md:50-60`), `src/frontend/src/pages/preferences.ts:19-35`, `src/frontend/src/components/app-shell.ts:20-31`.
162. 
163. 9. **Add loan-context and mixed-portfolio restriction handling to the UI/API boundary.**
164.    - Acceptance criteria:
165.      - The frontend can display conditional restrictions for California and mixed-state portfolio contexts without turning the global preference model into per-loan overrides.
166.      - The save request includes enough context for backend validation when a state-dependent rule applies, or the backend can resolve it from authoritative state.
167.      - Finalized-application messaging clarifies queued-notification behavior.
168.    - Source references: `FR-4` (`specs/product-spec-notification-preferences.md:110-115`), `SC-1` (`specs/product-spec-notification-preferences.md:147-151`), `SC-3` (`specs/product-spec-notification-preferences.md:166-170`), `specs/bug-report.md:60-63`, `src/frontend/src/pages/application-detail.ts:35-53`, `src/frontend/src/pages/preferences.ts:13-18`, `src/frontend/src/api/client.ts:87-97`.
169. 
170. 10. **Add automated coverage for rules, routes, delivery, and UX failure handling.**
171.     - Acceptance criteria:
172.       - Tests cover delegated read-only behavior, mandatory-event enforcement, California decline SMS restriction, effective defaults, fail-closed audit rejection, fallback-without-mutation, pilot `404` hiding, and optimistic rollback.
173.       - Release validation explicitly includes false-positive and hard-negative scenarios from the specs.
174.     - Source references: `docs/planning-workflow-example.md:53-60`, `FR-2` (`specs/product-spec-notification-preferences.md:86-92`), `FR-4` (`specs/product-spec-notification-preferences.md:117-118`), `FR-5` (`specs/product-spec-notification-preferences.md:128-130`), `SC-2` (`specs/product-spec-notification-preferences.md:162-164`), `NFR-2` (`specs/non-functional-requirements.md:28-34`), `NFR-6` (`specs/non-functional-requirements.md:92-97`), `src/backend/tests/unit/notification-service.test.ts:10-15`, `src/backend/tests/integration/decisions.test.ts:7-14`.
175. 
176. ## Validation steps
177. 
178. 1. **Backend rule tests**
179.    - Verify `manual-review-escalation` rejects zero enabled channels but accepts email-only and sms-only valid states.
180.    - Verify California decline SMS is rejected when `loanState === "CA"` and not rejected solely because borrower data differs.
181. 
182. 2. **Authorization and delegated-session tests**
183.    - Verify delegated sessions can fetch the delegate’s effective preferences but receive a write rejection.
184.    - Verify compliance reviewers can read but not write.
185.    - Verify non-owner direct writes are rejected if owner-only semantics are retained.
186. 
187. 3. **Pilot gating tests**
188.    - Verify non-pilot API reads/writes return `404`.
189.    - Verify pilot users with no stored rows still see effective defaults on first load.
190. 
191. 4. **Audit fail-closed tests**
192.    - Simulate audit unavailability and verify preference writes are rejected and not persisted.
193.    - Verify preference reads still succeed during the same outage.
194.    - Verify `audit.write.failure` and `preference.save.failure` are distinguishable.
195. 
196. 5. **Delivery fallback tests**
197.    - Simulate unhealthy SMS provider with email enabled and confirm fallback delivery occurs without mutating stored preferences.
198.    - Simulate unhealthy SMS provider with email disabled and confirm no silent preference mutation or misleading UX.
199. 
200. 6. **Frontend state and UX tests**
201.    - Verify the page renders a matrix, mandatory inline helper text, delegated-session banner, and ARIA-announced save status.
202.    - Verify optimistic rollback occurs on rejected saves and no false success toast/state persists.
203.    - Verify mixed-portfolio messaging is conditional, not blanket-disabled.
204. 
205. 7. **Regression checks against known nuanced cases**
206.    - **False positive check:** escalation SMS off + escalation email on remains valid.
207.    - **False positive check:** email delivery during SMS outage is not surfaced as a preference corruption bug.
208.    - **Hard negative check:** delegated save must never look successful.
209.    - **Hard negative check:** non-pilot hidden route must not leak via `403`.
210. 
211. ## Risks and dependencies
212. 
213. ### Risks
214. 
215. - **Audit architecture mismatch:** current queued audit flow does not satisfy fail-closed semantics for preference writes; this is the largest implementation risk because it crosses service, queue, and persistence boundaries (`src/backend/src/services/audit-service.ts:18-45`; `src/backend/src/queue/handlers/audit-handler.ts:8-13`).
216. - **State/context mismatch in the UI:** current preferences page has no loan or portfolio context, but FR-4/SC-3 require conditional restriction messaging. Without a clear context source, the UI may either over-disable or under-enforce.
217. - **ADR-003 gap:** the current direct-toggle pattern bypasses a central store, increasing risk of repeated delegated-session false successes and inconsistent rollback behavior.
218. - **Bulk endpoint complexity:** channel-wide bulk updates can easily violate FR-2 or FR-4 unless rule evaluation is centralized and context-aware.
219. - **Observability gap:** no metrics surface is currently present in source for the required counters/histograms, so telemetry work may require introducing a common instrumentation surface.
220. 
221. ### Dependencies
222. 
223. - Product decision on compliance-view placement (`specs/product-spec-notification-preferences.md:187-193`).
224. - Product/engineering decision on how the preferences page receives active application or mixed-portfolio context.
225. - Engineering decision on synchronous audit durability strategy when `queueAudit` is enabled.
226. - Release-management support for pilot flag rollout and checklist updates required by `NFR-7`.
```

</details>


---

<sub>⏱️ 3m 57s</sub>

### 💬 Copilot

Done — I inspected the lesson docs, ADR, specs, and current notification-related source surfaces, then wrote a structured plan to `docs/notification-preferences-plan.md`.

The plan includes the required summary, canonical-source/conflict handling, confirmed FR/SC/ADR/NFR-backed requirements, open questions with file refs, inferred choices separated from requirements, constraints, numbered tasks with acceptance criteria, validation steps, and risks/dependencies. It explicitly calls out delegated sessions, `LEGAL-218`, mandatory-event delivery, fail-closed audit behavior, degraded-mode fallback, false positives, and hard negatives.

---

<sub>Generated by [GitHub Copilot CLI](https://github.com/features/copilot/cli)</sub>
