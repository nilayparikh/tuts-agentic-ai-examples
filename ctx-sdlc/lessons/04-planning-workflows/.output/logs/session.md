# 🤖 Copilot CLI Session

> [!NOTE]
> - **Session ID:** `2c17a379-e5f1-4f63-a9fb-416037cc22d3`  
> - **Started:** 13/03/2026, 22:32:32  
> - **Duration:** 1m 14s  
> - **Exported:** 13/03/2026, 22:33:46  

---

<sub>⏱️ 6s</sub>

### 👤 User

Read docs/architecture.md, docs/adr/ADR-003-frontend-state.md, specs/product-spec-notification-preferences.md, specs/non-functional-requirements.md, and specs/feature-request.md. Produce a read-only implementation plan for notification preferences. Separate confirmed product requirements from inferred implementation choices. Return: summary, open questions with source references, constraints and special conditions, numbered tasks with acceptance criteria and source refs, validation steps, and risks/dependencies. Explicitly call out delegated sessions, LEGAL-218, mandatory-event delivery, fail-closed audit behavior, degraded-mode fallback, at least one false positive, and at least one hard negative. Do not modify files and do not run shell commands. Inspect and read only.

---

<sub>⏱️ 17s</sub>

### 💬 Copilot

I’m reading the requested docs and turning them into a read-only implementation plan, with product facts separated from implementation inferences.

---

<sub>⏱️ 17s</sub>

### ✅ `sql`

**Create planning todos**

<details>
<summary>Arguments</summary>

```json
{
  "description": "Create planning todos",
  "query": "INSERT INTO todos (id, title, description, status) VALUES\n  ('read-source-docs', 'Read source docs', 'Inspect architecture, ADR, product spec, NFR, and feature request for notification preferences planning.', 'in_progress'),\n  ('draft-plan', 'Draft implementation plan', 'Produce a read-only implementation plan separating confirmed requirements from inferred implementation choices.', 'pending');"
}
```

</details>

```
2 row(s) inserted. Last inserted row ID: 2.
```


---

<sub>⏱️ 17s</sub>

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

<sub>⏱️ 17s</sub>

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

<sub>⏱️ 17s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md

<details>
<summary>194 lines</summary>

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
194.
```

</details>


---

<sub>⏱️ 17s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\04-planning-workflows\specs\non-functional-requirements.md

<details>
<summary>111 lines</summary>

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
111.
```

</details>


---

<sub>⏱️ 17s</sub>

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

<sub>⏱️ 29s</sub>

### 💬 Copilot

I’ve got the core sources. There are a couple of meaningful ambiguities in the docs, so I’m capturing those as open questions rather than silently assuming implementation details.

---

<sub>⏱️ 29s</sub>

### ✅ `sql`

**Complete planning todos**

<details>
<summary>Arguments</summary>

```json
{
  "description": "Complete planning todos",
  "query": "UPDATE todos SET status = 'done' WHERE id = 'read-source-docs';\nUPDATE todos SET status = 'in_progress' WHERE id = 'draft-plan';"
}
```

</details>

<details>
<summary>5 lines</summary>

```
Executed 2 statement(s):

1. UPDATE
   1 row(s) updated.

2. UPDATE
   1 row(s) updated.
```

</details>


---

<sub>⏱️ 34s</sub>

### ✅ `sql`

**Mark planning complete**

<details>
<summary>Arguments</summary>

```json
{
  "description": "Mark planning complete",
  "query": "UPDATE todos SET status = 'done' WHERE id = 'draft-plan';"
}
```

</details>

```
1 row(s) updated.
```


---

<sub>⏱️ 1m 14s</sub>

### 💬 Copilot

Here’s a **read-only implementation plan** for notification preferences.

**Summary**

**Confirmed product requirements:** per-event email/SMS preferences for `approval`, `decline`, `document-request`, and `manual-review-escalation`; persistence across sessions/devices; role-based defaults on first access; delegated sessions are view-only for the delegate’s settings; compliance reviewers are read-only; manual-review escalation must always remain deliverable via at least one enabled channel; California decline SMS is blocked by `LEGAL-218`; SMS outages may fall back to email without mutating stored preferences; every write must be audited; pilot gating must hide the feature from non-pilot users with `404` (`specs/product-spec-notification-preferences.md:68-142`, `145-180`; `specs/non-functional-requirements.md:21-35`, `63-107`; `specs/feature-request.md:7-26`).

**Inferred implementation choices:** central frontend store ownership rather than component-local state; optimistic save only with rollback; backend changes likely span route, rule, service, persistence, audit, queue/metrics, and typed API surfaces; effective-preference reads should synthesize defaults on first access without requiring migration; state/jurisdiction evaluation likely needs contextual read models rather than a flat static toggle matrix (`docs/adr/ADR-003-frontend-state.md:16-37`; `docs/architecture.md:41-58`).

**Open questions**

1. **Actual code surface naming is inconsistent.** Product spec says `apps/web/` and `services/api/`, while architecture says `src/frontend/src/` and `src/backend/src/` and the feature request says backend routes live under `src/backend/src/routes/`. Plan should align on the real target paths before implementation (`specs/product-spec-notification-preferences.md:30-31`; `docs/architecture.md:10-33`; `specs/feature-request.md:30-33`).

2. **What exactly is “active loan context” on a global settings page?** FR-4 makes California restrictions depend on active loan context / portfolio context, but preferences are described as global user settings. The team needs a clear rule for when contextual restrictions are shown, computed, and enforced server-side (`specs/product-spec-notification-preferences.md:105-119`, `166-170`).

3. **“Finalized” vs state machine terminology is inconsistent.** The product spec references `finalized`, but architecture defines terminal states as `funded` and `closed`. Clarify whether `finalized` is an umbrella UX term or a real domain state (`specs/product-spec-notification-preferences.md:147-151`; `docs/architecture.md:60-69`).

4. **Audit history placement for compliance reviewers is unresolved.** The spec leaves open whether audit history is on the settings page or a separate viewer (`specs/product-spec-notification-preferences.md:187-193`).

5. **Portfolio-view UX choice is unresolved.** The spec asks whether mixed-state restrictions use a summary banner or per-row indicators; implementation can proceed only after a UX decision, though the rule must remain conditional rather than blanket-disabled (`specs/product-spec-notification-preferences.md:114-116`, `166-170`, `193-194`).

**Constraints and special conditions**

- **Delegated sessions:** analyst managers may inspect but not edit another user’s preferences; UI must indicate delegated mode; audit must include actor and delegated-for user (`specs/product-spec-notification-preferences.md:153-165`; `specs/non-functional-requirements.md:40-44`).

- **LEGAL-218:** decline SMS must remain disabled for California loans, based on `loanState`, not borrower address; mixed portfolio context must show conditional rules, not blanket-disable all SMS (`specs/product-spec-notification-preferences.md:105-119`, `166-170`; `specs/feature-request.md:21-25`).

- **Mandatory-event delivery:** manual-review escalation is mandatory; at least one channel must remain enabled; both UI and API must enforce this (`specs/product-spec-notification-preferences.md:81-92`; `specs/feature-request.md:10-11`, `24`).

- **Fail-closed audit behavior:** writes must abort if audit logging is unavailable; reads may still succeed during audit outage (`specs/non-functional-requirements.md:23-35`).

- **Degraded-mode fallback:** SMS provider outage may fall back to email if email is enabled, but stored preferences must remain unchanged and fallback must emit a separate metric (`specs/product-spec-notification-preferences.md:120-130`; `specs/non-functional-requirements.md:65-73`).

- **Pilot gating / hard negative:** non-pilot users must receive `404`, not `403`, so the feature is hidden rather than disclosed (`specs/non-functional-requirements.md:84-97`; `docs/architecture.md:43-47`).

- **Accessibility:** helper text for disabled controls must be persistent, keyboard/screen-reader support is required, and save outcomes must announce via ARIA live regions (`specs/product-spec-notification-preferences.md:174-180`; `specs/non-functional-requirements.md:50-60`).

- **Performance:** initial load adds at most `150 ms p95`; save completes within `400 ms p95` (`specs/non-functional-requirements.md:9-18`).

- **Retention/compliance:** audit records for preference changes must be retained for 24 months; compliance reviewer view must show effective state including defaults (`specs/non-functional-requirements.md:101-110`).

- **Explicit false positive:** disabling escalation SMS while escalation email stays enabled is **not** a violation; email fallback during SMS outage is **not** a preference bug (`specs/product-spec-notification-preferences.md:90-92`, `128-130`; `specs/non-functional-requirements.md:33-35`, `96-97`).

- **Explicit hard negatives:** allowing all channels off for mandatory escalation; allowing delegated-session writes that optimistically “succeed” then revert; swallowing audit failures; returning `403` instead of `404`; enabling decline SMS on California loans (`specs/product-spec-notification-preferences.md:86-88`, `117-118`, `162-165`; `specs/non-functional-requirements.md:28-31`, `92-94`).

**Numbered tasks**

1. **Define the domain model and effective-preference rules.**  
Acceptance criteria: documented matrix of events/channels; explicit rule that effective preferences may come from stored values or role-based defaults on first access; mandatory-event rule and California contextual restriction are represented separately from raw stored values.  
Sources: `specs/product-spec-notification-preferences.md:68-119`, `94-104`; `specs/non-functional-requirements.md:84-97`; `docs/adr/ADR-003-frontend-state.md:16-31`.

2. **Design the read API for effective preferences plus context metadata.**  
Acceptance criteria: response shape distinguishes stored values vs applied defaults/effective values; includes enough context for delegated-session banner, read-only status, mandatory-event explanation, California conditional restriction, and mixed-portfolio explanation.  
Sources: `specs/product-spec-notification-preferences.md:94-104`, `105-119`, `153-170`, `174-180`; `specs/non-functional-requirements.md:101-107`.

3. **Design the write API and server-side validation rules.**  
Acceptance criteria: server rejects delegated-session writes, compliance-reviewer writes, zero-channel mandatory escalation state, California decline-SMS enablement in CA context, and non-pilot access; response semantics differentiate validation errors from downstream failures.  
Sources: `specs/product-spec-notification-preferences.md:81-92`, `105-119`, `153-165`; `specs/non-functional-requirements.md:21-35`, `63-80`, `84-97`; `specs/feature-request.md:17-18`, `21-25`.

4. **Specify audit behavior for all writes.**  
Acceptance criteria: audit payload captures actor, timestamp, previous/new values, source channel, and delegated-for user; save path is fail-closed if audit write cannot be recorded; retention expectation is preserved.  
Sources: `specs/product-spec-notification-preferences.md:132-142`, `160`; `specs/non-functional-requirements.md:25-35`, `101-110`; `docs/architecture.md:41-47`.

5. **Plan frontend state ownership and rollback semantics.**  
Acceptance criteria: notification preferences live in the central client store, not local component state; optimistic updates are allowed only with rollback on API rejection; delegated-mode rejections cannot leave stale “saved” UI state.  
Sources: `docs/adr/ADR-003-frontend-state.md:16-37`; `specs/product-spec-notification-preferences.md:162-165`, `174-180`.

6. **Plan UI/UX behavior for the settings matrix.**  
Acceptance criteria: matrix grid by event/channel; mandatory event marked inline; disabled controls show persistent helper text; delegated-session visual indicator exists; mixed-portfolio California messaging is conditional rather than blanket-disable; finalized/queued-notification clarification is present once terminology is resolved.  
Sources: `specs/product-spec-notification-preferences.md:147-180`, `166-170`; `specs/non-functional-requirements.md:50-60`; `specs/feature-request.md:7-12`, `19-26`.

7. **Plan degraded-mode and observability behavior.**  
Acceptance criteria: provider outage does not block reads; fallback sends email only when allowed by preferences; stored preferences stay unchanged; metrics/logs distinguish validation failures, provider failures, audit failures, save latency, and SMS fallback counts.  
Sources: `specs/product-spec-notification-preferences.md:120-130`; `specs/non-functional-requirements.md:21-35`, `63-80`.

8. **Plan rollout and change safety.**  
Acceptance criteria: release-flag design hides feature from non-pilot users with `404`; no behavior change for non-pilot users; defaults appear for existing users on first access without migration/backfill.  
Sources: `specs/non-functional-requirements.md:84-97`; `docs/architecture.md:43-47`; `specs/feature-request.md:17-18`, `26`.

9. **Plan test coverage and release validation.**  
Acceptance criteria: test matrix covers role defaults, delegated read-only mode, mandatory-event enforcement, California restriction, fallback behavior, audit fail-closed behavior, `404` flag behavior, accessibility affordances, and metrics/logging classification.  
Sources: `specs/product-spec-notification-preferences.md:81-92`, `105-130`, `153-180`; `specs/non-functional-requirements.md:50-60`, `63-107`; `docs/architecture.md:43-58`.

**Validation steps**

1. Review the planned API contract against the product matrix and verify every event/channel pair is represented, including mandatory escalation semantics and contextual California restrictions.

2. Validate hard negatives: zero-channel escalation save is rejected; delegated-session save is rejected without stale optimistic state; audit outage aborts save; non-pilot access returns `404`; CA decline SMS cannot be enabled in CA context.

3. Validate false positives: escalation SMS off + email on is accepted; email delivery during SMS outage does not imply a stored-preference defect; first-access defaults for existing users are accepted behavior.

4. Validate observability: each failure path maps to the correct metric/log category; fallback increments `notification.sms.fallback`; audit write rejection increments `audit.write.failure`.

5. Validate UX/accessibility: keyboard navigation, screen-reader labels, persistent explanatory text for disabled controls, ARIA announcements for save success/failure, and delegated-mode indicator.

**Risks and dependencies**

- **Primary dependency:** unresolved UX/product decisions on audit-history placement and mixed-portfolio restriction presentation (`specs/product-spec-notification-preferences.md:187-194`).

- **Domain-model risk:** global preferences plus loan-context restrictions can produce confusing “effective vs stored” behavior unless the API clearly separates them (`specs/product-spec-notification-preferences.md:105-119`, `120-126`).

- **State-management risk:** violating ADR-003 by using local state or missing rollback will recreate the known delegated-session false success bug (`docs/adr/ADR-003-frontend-state.md:16-31`; `specs/product-spec-notification-preferences.md:162-165`).

- **Operational risk:** fail-closed audit behavior protects compliance but can raise save failure rates during audit outages; rollout needs monitoring and support guidance (`specs/non-functional-requirements.md:23-35`, `63-80`).

- **Terminology risk:** `finalized` vs `funded/closed` ambiguity could lead to incorrect UI messaging or guard logic unless clarified before implementation (`specs/product-spec-notification-preferences.md:147-151`; `docs/architecture.md:62-69`).

No files were modified, and no shell commands were run.

---

<sub>Generated by [GitHub Copilot CLI](https://github.com/features/copilot/cli)</sub>
