# 🤖 Copilot CLI Session

> [!NOTE]
> - **Session ID:** `0c677d7d-f914-4b4d-9899-d12183ee6fa8`  
> - **Started:** 15/04/2026, 16:48:10  
> - **Duration:** 2m 53s  
> - **Exported:** 15/04/2026, 16:51:03  

---

<sub>⏱️ 5s</sub>

### 👤 User

Inspect the relevant docs/, specs/, and existing source surfaces for notification preferences in this lesson before answering. Discover the architecture, ADR, product, and NFR context you need rather than assuming a fixed file list. Produce a structured implementation plan and save it to docs/notification-preferences-plan.md. The plan must include: summary, source-backed confirmed requirements with references to FR/SC/ADR/NFR identifiers, open questions with file references, inferred implementation choices separated from confirmed requirements, constraints and special conditions, numbered tasks with acceptance criteria and source references, validation steps, and risks/dependencies. Explicitly call out delegated sessions, LEGAL-218, mandatory-event delivery, fail-closed audit behavior, degraded-mode fallback, at least one false positive, and at least one hard negative. If the sources overlap or conflict, identify the canonical source for the plan and explain why. Do not run shell commands and do not use SQL.

---

<sub>⏱️ 10s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows

<details>
<summary>10 lines</summary>

```
.github
.output
ASSESSMENT.md
README.md
RUN.md
__pycache__
docs
specs
src
util.py
```

</details>


---

<sub>⏱️ 10s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples**

"**/{docs,specs}/**/*.md" in Y:\.sources\localm-tuts\courses\_examples

<details>
<summary>29 matches</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\09-ai-assisted-sdlc-capstone\docs\capstone-example.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\09-ai-assisted-sdlc-capstone\docs\architecture.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\specs\non-functional-requirements.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\specs\feature-request.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\specs\bug-report.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\docs\planning-workflow-example.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\docs\architecture.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\docs\adr\ADR-003-frontend-state.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\01-why-context-engineering\with-context\docs\manual-review-escalation.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\01-why-context-engineering\with-context\docs\experiment.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\01-why-context-engineering\with-context\docs\architecture.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\03-instruction-architecture\docs\instruction-layering-example.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\03-instruction-architecture\docs\architecture.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\02-curate-project-context\docs\preference-management-example.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\02-curate-project-context\docs\architecture.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\02-curate-project-context\docs\api-conventions.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\06-tools-and-guardrails\docs\tool-trust-boundaries.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\06-tools-and-guardrails\docs\security-policy.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\06-tools-and-guardrails\docs\guardrail-audit-example.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\07-surface-strategy\docs\surface-strategy-example.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\07-surface-strategy\docs\surface-portability-notes.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\07-surface-strategy\docs\portability-matrix.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\07-surface-strategy\docs\cli-guide.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\08-operating-model\docs\operating-model-example.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\08-operating-model\docs\maintenance-schedule.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-workflow-example.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-playbook.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\non-functional-requirements.md
```

</details>


---

<sub>⏱️ 13s</sub>

### 💬 Copilot

Now let me read the key specs and docs from lesson 04:

---

<sub>⏱️ 13s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\specs\product-spec-notification-preferences.md

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

<sub>⏱️ 13s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\specs\non-functional-requirements.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\specs\non-functional-requirements.md

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

<sub>⏱️ 13s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\docs\architecture.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\docs\architecture.md

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

<sub>⏱️ 16s</sub>

### 💬 Copilot

Now let me check for ADR files and related source code references:

---

<sub>⏱️ 16s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\docs\adr.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\docs\adr

```
ADR-003-frontend-state.md
```


---

<sub>⏱️ 16s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\specs.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\specs

```
bug-report.md
feature-request.md
non-functional-requirements.md
product-spec-notification-preferences.md
```


---

<sub>⏱️ 18s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\docs\adr\ADR-003-frontend-state.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\docs\adr\ADR-003-frontend-state.md

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

<sub>⏱️ 18s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\specs\feature-request.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\specs\feature-request.md

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

<sub>⏱️ 18s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\specs\bug-report.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\specs\bug-report.md

<details>
<summary>65 lines</summary>

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
65.
```

</details>


---

<sub>⏱️ 22s</sub>

### 💬 Copilot

Now let me check the source code structure to understand existing patterns:

---

<sub>⏱️ 22s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src

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

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src**

"**/*.ts" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src

<details>
<summary>6 matches</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\frontend\vite.config.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\tests\unit\state-machine.test.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\tests\unit\notification-service.test.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\tests\unit\business-rules.test.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\tests\integration\decisions.test.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\tests\integration\applications.test.ts
```

</details>


---

<sub>⏱️ 25s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend

```
dist
src
tests
tsconfig.json
```


---

<sub>⏱️ 27s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src

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

<sub>⏱️ 29s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src**

"**/*.ts" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src

<details>
<summary>32 matches</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\app.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\services\notification-service.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\services\loan-service.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\services\decision-service.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\services\audit-service.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\rules\state-machine.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\rules\role-permissions.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\rules\mandatory-events.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\rules\business-rules.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\routes\queue-status.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\routes\notifications.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\routes\decisions.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\routes\audit.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\routes\applications.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\queue\handlers\notification-handler.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\queue\handlers\audit-handler.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\queue\contracts.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\queue\broker.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\models\user-repository.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\models\types.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\models\preference-repository.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\models\loan-repository.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\models\audit-repository.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\config\feature-flags.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\config\env.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\middleware\request-validator.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\middleware\rate-limiter.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\middleware\error-handler.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\middleware\auth.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\middleware\audit-logger.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\db\connection.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\db\seed.ts
```

</details>


---

<sub>⏱️ 32s</sub>

### 💬 Copilot

Let me examine key source files to understand existing patterns:

---

<sub>⏱️ 32s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\models\types.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\models\types.ts

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

<sub>⏱️ 32s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\models\preference-repository.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\models\preference-repository.ts

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

<sub>⏱️ 32s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\rules\mandatory-events.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\rules\mandatory-events.ts

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

<sub>⏱️ 35s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\rules\business-rules.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\rules\business-rules.ts

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

<sub>⏱️ 35s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\rules\role-permissions.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\rules\role-permissions.ts

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

<sub>⏱️ 39s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\middleware\auth.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\middleware\auth.ts

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

<sub>⏱️ 39s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\queue\contracts.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\queue\contracts.ts

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

<sub>⏱️ 42s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\routes\notifications.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\routes\notifications.ts

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

<sub>⏱️ 42s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\services\audit-service.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\services\audit-service.ts

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

<sub>⏱️ 46s</sub>

### 💬 Copilot

Let me check the config and feature flags:

---

<sub>⏱️ 46s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\config\feature-flags.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\config\feature-flags.ts

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

<sub>⏱️ 46s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\queue\broker.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\src\backend\src\queue\broker.ts

<details>
<summary>108 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // In-Process Event Broker
3. // ---------------------------------------------------------------------------
4. // A lightweight pub/sub broker for decoupling producers from consumers.
5. // Events are processed asynchronously but in-process (no external MQ).
6. //
7. // IMPORTANT — ORDERING:
8. //   Events are delivered in FIFO order per event type.  Handlers for the
9. //   same event type run sequentially; handlers for different types run
10. //   concurrently.  Do NOT rely on cross-type ordering.
11. //
12. // IMPORTANT — ERROR HANDLING:
13. //   If a handler throws, the error is logged but does NOT prevent other
14. //   handlers from running.  For critical operations (like audit writes),
15. //   the handler must implement its own retry logic.
16. // ---------------------------------------------------------------------------
17. 
18. import type { BrokerEvent, EventType } from "./contracts.js";
19. 
20. type EventHandler<T extends BrokerEvent = BrokerEvent> = (
21.   event: T,
22. ) => Promise<void>;
23. 
24. class EventBroker {
25.   private handlers = new Map<EventType, EventHandler[]>();
26.   private pendingCount = 0;
27.   private eventHistory: Array<{ event: BrokerEvent; processedAt: string }> = [];
28.   private readonly maxHistory = 200;
29. 
30.   /**
31.    * Register a handler for a specific event type.
32.    * Handlers are called in registration order.
33.    */
34.   on<T extends BrokerEvent>(type: T["type"], handler: EventHandler<T>): void {
35.     const existing = this.handlers.get(type) ?? [];
36.     existing.push(handler as EventHandler);
37.     this.handlers.set(type, existing);
38.   }
39. 
40.   /**
41.    * Emit an event.  All registered handlers are invoked asynchronously.
42.    * Returns immediately — use `flush()` in tests to await completion.
43.    */
44.   emit(event: BrokerEvent): void {
45.     const handlers = this.handlers.get(event.type) ?? [];
46.     if (handlers.length === 0) {
47.       console.warn(
48.         `[broker] No handlers registered for event type: ${event.type}`,
49.       );
50.       return;
51.     }
52. 
53.     this.pendingCount++;
54.     this.eventHistory.push({ event, processedAt: new Date().toISOString() });
55.     if (this.eventHistory.length > this.maxHistory) {
56.       this.eventHistory.shift();
57.     }
58.     this.processHandlers(event, handlers).finally(() => {
59.       this.pendingCount--;
60.     });
61.   }
62. 
63.   /**
64.    * Wait for all pending event processing to complete.
65.    * Used in tests to ensure deterministic assertions.
66.    */
67.   async flush(): Promise<void> {
68.     // Spin-wait with setImmediate until all handlers finish
69.     while (this.pendingCount > 0) {
70.       await new Promise((resolve) => setImmediate(resolve));
71.     }
72.   }
73. 
74.   private async processHandlers(
75.     event: BrokerEvent,
76.     handlers: EventHandler[],
77.   ): Promise<void> {
78.     for (const handler of handlers) {
79.       try {
80.         await handler(event);
81.       } catch (err) {
82.         console.error(`[broker] Handler error for ${event.type}:`, err);
83.       }
84.     }
85.   }
86. 
87.   /** Return the list of registered event types and handler counts. */
88.   getSubscriptions(): Array<{ type: string; handlerCount: number }> {
89.     return Array.from(this.handlers.entries()).map(([type, handlers]) => ({
90.       type,
91.       handlerCount: handlers.length,
92.     }));
93.   }
94. 
95.   /** Return recent event history. */
96.   getHistory(limit = 50): Array<{ event: BrokerEvent; processedAt: string }> {
97.     return this.eventHistory.slice(-limit).reverse();
98.   }
99. 
100.   /** Return pending event count. */
101.   getPendingCount(): number {
102.     return this.pendingCount;
103.   }
104. }
105. 
106. /** Singleton broker instance — import this in producers and consumers. */
107. export const broker = new EventBroker();
108.
```

</details>


---

<sub>⏱️ 49s</sub>

### 💬 Copilot

Now let me check the planning workflow example and other test patterns to understand the expected structure:

---

<sub>⏱️ 49s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\docs\planning-workflow-example.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\docs\planning-workflow-example.md

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

<sub>⏱️ 2m 35s</sub>

### 💬 Copilot

Perfect! Now I have all the context I need. Let me create a comprehensive implementation plan based on the product spec, NFRs, ADRs, and existing codebase patterns. I'll save this to docs/notification-preferences-plan.md:

---

<sub>⏱️ 2m 35s</sub>

### ✅ `create`

**create a new file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\docs\notification-preferences-plan.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\docs\notification-preferences-plan.md

```
Created file Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\docs\notification-preferences-plan.md with 40105 characters
```


---

<sub>⏱️ 2m 39s</sub>

### 💬 Copilot

Perfect! I've created a comprehensive implementation plan for the notification preferences feature. Let me verify the file was created and provide a summary:

---

<sub>⏱️ 2m 39s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\docs\notification-preferences-plan.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\04-planning-workflows\docs\notification-preferences-plan.md (lines 1-50)

<details>
<summary>50 lines</summary>

```
1. # Notification Preferences Implementation Plan
2. 
3. ## Document Summary
4. 
5. This plan outlines the implementation of per-user notification preferences for the Loan Workbench. The feature allows underwriters and analyst managers to configure email and SMS delivery for four event types (approval, decline, document-request, manual-review-escalation) subject to regulatory restrictions, role-based access controls, delegated-session read-only semantics, and fail-closed audit behavior.
6. 
7. **Canonical Source**: `specs/product-spec-notification-preferences.md` (PROJ-412, Q2 2026 pilot) is the authoritative product specification. `specs/non-functional-requirements.md` refines constraints on audit, performance, security, and observability. `docs/adr/ADR-003-frontend-state.md` governs frontend state ownership. `specs/bug-report.md` demonstrates overlapping rule layers that commonly cause AI-generated code to fail.
8. 
9. ---
10. 
11. ## Confirmed Requirements (Source-Backed)
12. 
13. ### Functional Requirements
14. 
15. | Requirement | Identifier | Description |
16. |---|---|---|
17. | Preference matrix | FR-1 | Users configure email and SMS independently for approval, decline, document-request, manual-review-escalation. |
18. | Mandatory escalation | FR-2 | Manual-review-escalation must have at least one enabled channel; users cannot disable all channels. |
19. | Role-based defaults | FR-3 | New users without saved preferences receive underwriter/analyst-manager defaults on first access without migration. |
20. | California SMS restriction | FR-4 / LEGAL-218 | SMS for decline decisions must remain disabled for CA loans until legal review completes. Restriction is loan-state based (not borrower-state). UI must show conditional explanation. |
21. | Degraded SMS fallback | FR-5 | If SMS provider unavailable, delivery falls back to email when enabled. **Stored preferences must NOT change.** Fallback must be logged separately. |
22. | Auditability | FR-6 | Every preference change records actor, timestamp, previous value, new value, source channel, and delegated-for user. |
23. 
24. ### Special Conditions
25. 
26. | Condition | Identifier | Description |
27. |---|---|---|
28. | Locked applications | SC-1 | Settings screen allows preference changes globally; clarify that changes don't affect notifications already queued for a finalized application. |
29. | Delegated sessions | SC-2 | Analyst managers in delegated mode may **view** delegate's preferences but **cannot modify**. UI must indicate delegated-session mode. Audit entries must record both actor and delegated-for user. |
30. | Mixed portfolio | SC-3 | When settings opened from multi-state portfolio, show state-specific restrictions as conditional rules rather than blanket-disabling controls. |
31. 
32. ### Non-Functional Requirements
33. 
34. | Requirement | Identifier | Key Constraint |
35. |---|---|---|
36. | Performance | NFR-1 | Settings load ≤150ms p95 over baseline; save ≤400ms p95. |
37. | Availability | NFR-2 | **FAIL-CLOSED**: If audit logging unavailable, writes ABORT (not silent save without trail). Reads tolerate provider degradation. |
38. | Security | NFR-3 | SMS destination values (phone numbers) are sensitive; exclude from client logs/analytics. Delegated sessions explicitly identified in audit. |
39. | Accessibility | NFR-4 | Keyboard-reachable controls, screen-reader labeled, persistent explanatory text for disabled mandatory events (not tooltips), ARIA live regions for save status. |
40. | Observability | NFR-5 | Emit counters: `preference.read.failure`, `preference.save.failure`, `audit.write.failure`, `notification.sms.fallback`; histogram `preference.save.latency`. Distinguish validation (4xx) from provider failures (5xx). |
41. | Change safety | NFR-6 | Feature shipped behind **release flag** (`notificationPreferences`). Non-pilot users see 404 (not 403) to hide feature existence. Role-based defaults on first access (no pre-migration required). |
42. | Compliance | NFR-7 | Audit records retained 24 months. Mandatory escalation delivery testable and in release checklist. Compliance reviewer's read-only view shows effective preference state including applied defaults. |
43. 
44. ### Architecture & Patterns
45. 
46. | Pattern | Identifier | Implication |
47. |---|---|---|
48. | Central client store | ADR-003 | Frontend notification preferences must use central store (not component-local state). Optimistic updates must support rollback on API rejection. |
49. | Message contracts | Design rule | Changes to `src/backend/src/queue/contracts.ts` are breaking changes; all producers and consumers must be updated. |
50. | Pure business rules | Design pattern | Rule modules in `src/backend/src/rules/` accept parameters (not internal imports); return structured results with `allowed` + `reason` (not bare booleans). |
```

</details>


---

<sub>⏱️ 2m 53s</sub>

### 💬 Copilot

Excellent! The plan has been successfully created. Here's a summary of what I've delivered:

## Summary

I've created a **comprehensive, source-backed implementation plan** for the Notification Preferences feature and saved it to `docs/notification-preferences-plan.md`. The plan includes:

### ✅ Core Sections Delivered

1. **Document Summary** — Identifies canonical sources (product spec, NFR, ADR, bug report)

2. **Confirmed Requirements** — Source-backed tables with FR, SC, NFR, and architecture pattern identifiers

3. **Open Questions & Assumptions** — Documents ambiguities (compliance reviewer audit access, portfolio view display, default generation timing) with resolutions

4. **Inferred Implementation Choices** — Separates specs from codebase design (schema, rule modules, service patterns, frontend store, observability metrics)

5. **Constraints & Special Conditions** — Highlights:
   - LEGAL-218 (California decline SMS restriction)
   - Mandatory escalation hard requirement
   - Delegated sessions (read-only)
   - Fail-closed audit semantics
   - Feature flag rollout strategy
   - No migration required

6. **False Positive & Hard Negative Patterns**:
   - ✅ **False positive example**: Disabling SMS for escalation while email enabled (correctly allowed)
   - ✅ **Hard negative example**: Disabling both SMS and email for escalation (must reject)

7. **12 Numbered Implementation Tasks** with:
   - Specific acceptance criteria
   - Source references (FR/SC/NFR/ADR)
   - Affected files

8. **Validation Steps** — Functional, performance, security, and rollout validation

9. **Risks & Dependencies** — 8 identified risks with mitigations, 5 dependencies

10. **Summary Table** — What changes where (Rules, Services, Routes, Config, Store, Components, Tests)

### ✅ Explicit Callouts Required

All required special cases explicitly addressed:
- ✅ Delegated sessions (SC-2, read-only enforcement, audit records)
- ✅ LEGAL-218 (California SMS restriction, loan-state contextual)
- ✅ Mandatory-event delivery (FR-2, at least one channel required)
- ✅ Fail-closed audit behavior (NFR-2, write rejects if audit unavailable)
- ✅ Degraded-mode fallback (FR-5, SMS→email, preferences unchanged, separate metric)
- ✅ False positive (escalation SMS disabled, email enabled = allowed)
- ✅ Hard negative (all escalation channels disabled = must reject)

The plan is **read-only** (no shell commands, no SQL) and ready for implementation.

---

<sub>Generated by [GitHub Copilot CLI](https://github.com/features/copilot/cli)</sub>
