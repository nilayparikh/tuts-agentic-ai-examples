# 🤖 Copilot CLI Session

> [!NOTE]
> - **Session ID:** `cf510843-0806-43e9-b2ab-e76e4afaad6d`  
> - **Started:** 14/03/2026, 19:37:41  
> - **Duration:** 3m 1s  
> - **Exported:** 14/03/2026, 19:40:43  

---

<sub>⏱️ 5s</sub>

### 👤 User

Inspect docs/, specs/, and the relevant notification-preference write surfaces you discover in this lesson before editing. Use the playbook and example doc as success criteria, not as a fixed file checklist. Implement a focused notification-preference write hardening slice. Write tests first at src/backend/tests/unit/notification-preference-write-rules.test.ts, then add a pure rule module at src/backend/src/rules/notification-preference-write-rules.ts, and wire the minimal production changes into src/backend/src/routes/notifications.ts. In the final handoff, state which behaviors the tests should fail on before the production change and which should pass after it, and name any intentionally deferred write surfaces that remain out of scope. The rule must use explicit inputs plus existing types, not direct DB access. Enforce these cases: manual-review-escalation must keep at least one channel enabled; decline SMS cannot be enabled when loanState is CA or California under LEGAL-218; the false positive where escalation SMS is disabled but escalation email stays enabled must remain allowed. Preserve delegated-session and role guards, keep changes minimal, keep the scope to the current notification write path, include top-of-module false-positive and hard-negative comments in the new rule file, and do not edit protected config or database files. Do not run npm install, npm test, npx vitest, or any shell commands. Do not use SQL or task/todo write tools. Inspect and edit files only. Return a short handoff summary naming changed files and which tests should pass.

---

<sub>⏱️ 15s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\docs.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\docs

```
implementation-playbook.md
implementation-workflow-example.md
```


---

<sub>⏱️ 15s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\specs.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\specs

```
non-functional-requirements.md
```


---

<sub>⏱️ 15s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "notification|preference|notifications",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\05-implementation-workflows\\src\\backend",
  "output_mode": "content",
  "glob": "**/*.{ts,tsx}",
  "-n": true,
  "head_limit": 200
}
```

</details>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\notification-service.test.ts:7:// These tests verify the notification routing logic at the service level.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\notification-service.test.ts:11:  it("placeholder — notification service emits queue events", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\notification-service.test.ts:12:    // Integration tests for notification delivery live in the queue handler tests.
```


---

<sub>⏱️ 22s</sub>

### 💬 Copilot

I’m reading the lesson guidance and the current backend surfaces first so the hardening stays aligned with the lesson’s intended slice.

---

<sub>⏱️ 22s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\docs\implementation-playbook.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\docs\implementation-playbook.md

<details>
<summary>115 lines</summary>

````
1. # Implementation Playbook
2. 
3. This document defines role boundaries, coding conventions, and handoff protocols
4. for the Loan Workbench implementation workflow.
5. 
6. ## Role Boundaries
7. 
8. | Role        | Can Read                | Can Write                                   | Can Execute            |
9. | ----------- | ----------------------- | ------------------------------------------- | ---------------------- |
10. | Implementer | All source, specs, docs | `src/backend/src/**`, `src/frontend/src/**` | Terminal (build, lint) |
11. | Tester      | All source, specs, docs | `src/backend/tests/**` only                 | Terminal + test runner |
12. | Reviewer    | All source, specs, docs | Nothing                                     | Nothing                |
13. 
14. ### Why These Boundaries Exist
15. 
16. - **Implementer cannot run tests**: Forces explicit handoff to the tester.
17.   Prevents "I'll just fix the test to match my code" shortcuts.
18. - **Reviewer cannot write**: Maintains independence. A reviewer who can "just
19.   fix it" is no longer reviewing — they're co-implementing.
20. - **Tester owns the test runner**: Only the tester decides when tests pass.
21.   The implementer provides code; the tester validates it.
22. 
23. ## Coding Conventions
24. 
25. ### Route Handlers (`src/backend/src/routes/`)
26. 
27. 1. Extract business logic to `src/backend/src/rules/` or `src/backend/src/services/` — routes should
28.    orchestrate, not decide.
29. 2. Use `requireRole()` middleware for role checks.
30. 3. Use `blockDelegatedWrites` middleware for mutation endpoints.
31. 4. Audit events via the queue broker or direct DB write before persisting changes.
32. 
33. ### Business Rules (`src/backend/src/rules/`)
34. 
35. 1. Pure functions that take data and return decisions.
36. 2. No side effects (no I/O, no audit writes, no HTTP responses).
37. 3. Document the legal or business source in a comment (e.g., `// LEGAL-218`).
38. 4. Annotate edge cases with `// FALSE POSITIVE` or `// HARD NEGATIVE`.
39. 
40. ### Services (`src/backend/src/services/`)
41. 
42. 1. Handle I/O and external integrations.
43. 2. Fail-closed for security-critical operations (audit).
44. 3. Degrade gracefully for non-critical operations (notification delivery).
45. 4. Never modify stored user preferences as a side effect of delivery.
46. 
47. ### Middleware (`src/backend/src/middleware/`)
48. 
49. 1. Thin and composable — one concern per middleware.
50. 2. Auth middleware sets `req.session`, nothing else.
51. 3. Guard middleware (like `blockDelegatedWrites`) returns 403 on violation.
52. 4. Error handler masks internal details — no stack traces in production.
53. 
54. ### Tests (`src/backend/tests/`)
55. 
56. 1. Use `describe`/`it` with behavior-focused names.
57. 2. One assertion per `it()` block.
58. 3. Test through route handlers using supertest-style requests.
59. 4. Annotate false-positive and hard-negative tests with comments.
60. 5. Do not mock business rule functions — test them through real call paths.
61. 
62. ## Handoff Protocols
63. 
64. ### Tester → Implementer
65. 
66. ```
67. Failing tests:
68.   - test name: "expected behavior description"
69.   - file: src/backend/tests/unit/xxx.test.ts
70. 
71. Files that need changes:
72.   - src/backend/src/rules/xxx.ts — add/modify rule
73.   - src/backend/src/routes/xxx.ts — wire in rule check
74. 
75. Relevant specs:
76.   - NFR-X: requirement summary
77.   - FR-X: functional requirement
78. ```
79. 
80. ### Implementer → Reviewer
81. 
82. ```
83. Changed files:
84.   - src/backend/src/rules/xxx.ts — what changed
85.   - src/backend/src/routes/xxx.ts — what changed
86. 
87. Tests that should pass:
88.   - "test name" in src/backend/tests/unit/xxx.test.ts
89. 
90. NFRs touched:
91.   - NFR-X: how it's addressed
92. ```
93. 
94. ### Reviewer → Team
95. 
96. ```
97. Review Summary:
98.   Verdict: APPROVE | REQUEST_CHANGES
99.   Files: list
100.   Issues: count
101. 
102. Issues (if any):
103.   1. [SEVERITY] description — file — spec reference
104. ```
105. 
106. ## Anti-Patterns
107. 
108. | Anti-Pattern               | Why It's Wrong                                   | Correct Approach                  |
109. | -------------------------- | ------------------------------------------------ | --------------------------------- |
110. | One agent does everything  | No independent validation                        | Three-agent role separation       |
111. | Implementer runs own tests | "Tests pass" because they were adjusted to match | Tester owns execution             |
112. | Reviewer pushes fixes      | No independent review trail                      | Reviewer flags, implementer fixes |
113. | Skipping the red step      | No proof the test catches the defect             | Always start with a failing test  |
114. | Batching unrelated changes | Review scope explosion                           | One feature per TDD cycle         |
115.
````

</details>


---

<sub>⏱️ 22s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\docs\implementation-workflow-example.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\docs\implementation-workflow-example.md

<details>
<summary>54 lines</summary>

```
1. # Lesson 05 — Implementation Workflow Example
2. 
3. This document defines the concrete example used in Lesson 05.
4. 
5. ## Objective
6. 
7. Show that a constrained implementation workflow can make a focused production change with matching tests instead of attempting the entire notification-preferences feature at once.
8. 
9. ## Expected Change Shape
10. 
11. The preferred output for this lesson is a small change set with:
12. 
13. 1. One new pure rule module under `src/backend/src/rules/`
14. 2. One matching unit test file under `src/backend/tests/unit/`
15. 3. One targeted wiring change to `src/backend/src/routes/notifications.ts`
16. 4. No edits to protected config or database files
17. 
18. ## Required Constraints
19. 
20. 1. The workflow must implement code, not only describe it.
21. 2. The new rule must use explicit inputs and existing domain types instead of direct database access.
22. 3. The change must preserve delegated-session and role guards already present in the route.
23. 4. The implementation must cover a mandatory-event rule and the California `LEGAL-218` restriction.
24. 5. The implementation must call out at least one false positive and one hard negative in the new rule module comments.
25. 6. The run must not execute shell commands.
26. 7. The run must not edit protected files such as feature flags, schema, or seed data.
27. 8. The run must not use SQL or task/todo write tools.
28. 9. The final handoff should explain the expected red/green test behavior and name any deferred follow-up surfaces that remain intentionally out of scope.
29. 10. The workflow should discover the current notification-preference write surfaces before editing and make the chosen slice boundary explicit.
30. 
31. ## Concrete Scenario
32. 
33. Harden notification preference writes so the existing route cannot:
34. 
35. - disable the last available channel for `manual-review-escalation`
36. - enable decline SMS for California loan context
37. 
38. Good output should keep the change local and avoid sprawling refactors.
39. 
40. It should also make the intentional scope boundary visible: this lesson is about hardening the current notification write path, not implementing every preference mutation surface in the repository at once.
41. 
42. Good output should explicitly name the deferred write surfaces in the handoff instead of silently implying that the whole notification-preferences domain is now complete.
43. 
44. ## What Good Output Looks Like
45. 
46. Good output will usually:
47. 
48. - create a pure rule file and a matching unit test file
49. - wire the route to call the rule rather than embedding the full policy inline
50. - preserve existing delegated-session and permission checks
51. - cite or encode the false-positive case where escalation SMS is disabled but escalation email remains enabled
52. - encode the hard-negative case where all escalation channels end up disabled
53. - explain which test cases would fail before the production change and which should pass after it
54.
```

</details>


---

<sub>⏱️ 22s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\specs\non-functional-requirements.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\specs\non-functional-requirements.md

<details>
<summary>109 lines</summary>

```
1. # Non-Functional Requirements — Implementation Workflows
2. 
3. These NFRs apply during implementation. Each includes the **AI mistake without
4. context** annotation showing what goes wrong when the AI doesn't have this NFR.
5. 
6. ---
7. 
8. ## NFR-1: Audit Trail Integrity (Fail-Closed)
9. 
10. **Requirement**: Every mutation that changes user data must write an audit entry
11. BEFORE persisting the change. If the audit write fails, the mutation MUST fail
12. with a 503 error. No silent fallback.
13. 
14. **AI mistake without context**: AI implements try-catch around the audit write
15. and proceeds with the mutation anyway. "Best-effort logging" sounds reasonable
16. but violates a compliance requirement.
17. 
18. > **HARD NEGATIVE**: The AI generates code that catches audit failures and logs
19. > a warning instead of aborting. This passes basic tests but fails compliance.
20. 
21. **Test signal**: Any test that mocks audit failure should assert the mutation
22. did NOT persist AND the response is 503.
23. 
24. ---
25. 
26. ## NFR-2: Degraded Mode for Non-Critical Services
27. 
28. **Requirement**: Notification delivery failures must fall back to email when SMS
29. is unavailable. The fallback must NOT modify stored user preferences.
30. 
31. **AI mistake without context**: AI implements the fallback but also updates the
32. user's stored channel preference from SMS to email "for consistency."
33. 
34. > **FALSE POSITIVE**: AI flags the inconsistency between stored preference (SMS)
35. > and actual delivery (email) as a bug. It's intentional — delivery degrades
36. > but preferences don't change.
37. 
38. **Test signal**: After a degraded delivery, GET /preferences should still show
39. the original SMS preference.
40. 
41. ---
42. 
43. ## NFR-3: Request Latency Budget
44. 
45. **Requirement**: Preference save operations must complete in <200ms under normal
46. conditions. Sequential I/O should be minimized.
47. 
48. **AI mistake without context**: AI adds synchronous delivery confirmation after
49. every preference save, doubling latency. Delivery is async by design.
50. 
51. > **FALSE POSITIVE**: AI suggests adding `await deliverNotification()` to the
52. > save handler for "consistency." Delivery is fire-and-forget by design.
53. 
54. ---
55. 
56. ## NFR-4: Role-Scoped Data Access
57. 
58. **Requirement**: Underwriters can only see their own audit entries. Analyst-managers
59. see entries for their team. Compliance reviewers see all entries.
60. 
61. **AI mistake without context**: AI implements a single `/audit` endpoint that
62. returns all entries regardless of role, adding a client-side filter. Server-side
63. scoping is the requirement.
64. 
65. > **HARD NEGATIVE**: The AI returns all audit data and filters in the response
66. > mapper. This "works" for underwriters viewing their own data but leaks
67. > everyone else's data in the response payload.
68. 
69. ---
70. 
71. ## NFR-5: Feature Flag Behavior (404 Not 403)
72. 
73. **Requirement**: Non-pilot users hitting gated endpoints must receive 404 (Not
74. Found), not 403 (Forbidden). This prevents information leakage about unreleased
75. features.
76. 
77. **AI mistake without context**: AI uses 403 because "the user isn't authorized
78. for this feature." The distinction matters — 403 confirms the endpoint exists.
79. 
80. > **HARD NEGATIVE**: AI returns 403 for non-pilot users. Security scanners and
81. > curious users now know the feature endpoint exists and is gated.
82. 
83. ---
84. 
85. ## NFR-6: Schema Backward Compatibility
86. 
87. **Requirement**: API schema changes must be additive. Existing clients must not
88. break when new fields are added. Removed fields must be deprecated with a
89. minimum two-release notice.
90. 
91. **AI mistake without context**: AI renames a response field from `channels` to
92. `notificationChannels` for "clarity." All existing clients break.
93. 
94. > **HARD NEGATIVE**: The AI improves naming but breaks every consumer. Additive
95. > changes (adding `notificationChannels` alongside `channels`) are safe.
96. 
97. ---
98. 
99. ## NFR-7: Structured Logging and Observability
100. 
101. **Requirement**: All log entries must be structured JSON with `correlationId`,
102. `userId`, `action`, and `timestamp`. No `console.log()` with string concatenation.
103. 
104. **AI mistake without context**: AI uses `console.log(\`User ${userId} saved preferences\`)`
105. which is unstructured and not machine-parseable.
106. 
107. > **FALSE POSITIVE**: AI flags existing structured logging as "verbose" and
108. > simplifies to `console.log()`. The structured format is a requirement.
109.
```

</details>


---

<sub>⏱️ 22s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows**

"**/notifications.ts" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows

```
No files matched the pattern.
```


---

<sub>⏱️ 22s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows**

"**/*notification*write*rules*.ts" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows

```
No files matched the pattern.
```


---

<sub>⏱️ 22s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend**

"**/*notification*.ts" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\notification-service.test.ts
```


---

<sub>⏱️ 33s</sub>

### 💬 Copilot

I found the lesson docs, but the backend search didn’t surface the route yet, so I’m widening the file inspection inside this lesson only and creating a quick plan artifact before editing.

---

<sub>⏱️ 33s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src

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

<sub>⏱️ 33s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend

```
dist
src
tests
tsconfig.json
```


---

<sub>⏱️ 33s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src

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

<sub>⏱️ 33s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests

```
integration
unit
```


---

<sub>⏱️ 33s</sub>

### ❌ `view`

**view the file at C:\Users\nilay\.copilot\session-state\cf510843-0806-43e9-b2ab-e76e4afaad6d\plan.md.**

C:\Users\nilay\.copilot\session-state\cf510843-0806-43e9-b2ab-e76e4afaad6d\plan.md

```
Path does not exist
```


---

<sub>⏱️ 41s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes**

"**/notifications.ts" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts
```


---

<sub>⏱️ 41s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "manual-review-escalation|decline|loanState|LEGAL-218|preferences",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\05-implementation-workflows\\src\\backend\\src",
  "output_mode": "content",
  "glob": "**/*.ts",
  "-n": true,
  "head_limit": 300
}
```

</details>

<details>
<summary>56 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\types.ts:40:  | "decline"
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\types.ts:42:  | "manual-review-escalation";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\types.ts:75:  loanState: string;
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\types.ts:86:  type: "approved" | "declined" | "conditional";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:4:// Database operations for notification preferences.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:37:      `SELECT ${PREFERENCE_COLUMNS} FROM notification_preferences WHERE user_id = ?`,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:55:      `SELECT ${PREFERENCE_COLUMNS} FROM notification_preferences WHERE user_id = ? AND event = ? AND channel = ?`,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:67:    `INSERT OR REPLACE INTO notification_preferences (user_id, event, channel, enabled, updated_at, updated_by)
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:82:    .prepare("DELETE FROM notification_preferences WHERE user_id = ?")
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\loan-repository.ts:19:  loan_state AS loanState,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\loan-repository.ts:66:  loanState: string;
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\loan-repository.ts:80:    data.loanState.toUpperCase(),
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:6://   All roles can READ preferences (for display purposes).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:7://   Only underwriters and analyst-managers can WRITE preferences.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:8://   Compliance reviewers are READ-ONLY for notification preferences.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:12://   preferences but CANNOT modify them.  The route handler must check
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:33:/** GET /api/notifications/preferences/:userId — get preferences for a user. */
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:35:  "/preferences/:userId",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:45:/** PUT /api/notifications/preferences — set a notification preference. */
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:47:  "/preferences",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:62:          error: "Delegated sessions cannot modify notification preferences.",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:70:          error: `Role '${session.actor.role}' cannot modify notification preferences.`,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:108: * PUT /api/notifications/preferences/:userId/email — set email notification preferences for all events.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:110: * Only the owner can modify their own preferences. Delegated sessions are blocked.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:113:  "/preferences/:userId/email",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:126:          error: "FORBIDDEN: Delegated sessions cannot modify notification preferences.",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:134:          error: `FORBIDDEN: Users can only modify their own notification preferences.`,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:142:          error: `FORBIDDEN: Role '${session.actor.role}' cannot modify notification preferences.`,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:149:      const events: Array<"approval" | "decline" | "document-request" | "manual-review-escalation"> = [
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:151:        "decline",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:153:        "manual-review-escalation",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:191: * PUT /api/notifications/preferences/:userId/sms — set SMS notification preferences for all events.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:193: * Only the owner can modify their own preferences. Delegated sessions are blocked.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:196:  "/preferences/:userId/sms",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:209:          error: "FORBIDDEN: Delegated sessions cannot modify notification preferences.",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:217:          error: `FORBIDDEN: Users can only modify their own notification preferences.`,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:225:          error: `FORBIDDEN: Role '${session.actor.role}' cannot modify notification preferences.`,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:232:      const events: Array<"approval" | "decline" | "document-request" | "manual-review-escalation"> = [
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:234:        "decline",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:236:        "manual-review-escalation",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\applications.ts:56:    { field: "loanState", type: "string", required: true },
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\middleware\auth.ts:12://   Compliance reviewers can view notification preferences and audit logs
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\rules\role-permissions.ts:10://   They CANNOT modify notification preferences, even though they can view
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\rules\mandatory-events.ts:24:  "underwriting->decision": ["manual-review-escalation"],
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\rules\business-rules.ts:46:  if (featureFlags.californiaRules && loan.loanState === "CA") {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\db\seed.ts:6:// finalized applications, and users without saved preferences.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\db\seed.ts:26:    `INSERT OR IGNORE INTO notification_preferences (user_id, event, channel, enabled, updated_at, updated_by)
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\db\seed.ts:114:    insertPref.run("u-1", "decline", "email", 1, now, "u-1");
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\db\seed.ts:116:    insertPref.run("u-2", "manual-review-escalation", "sms", 1, now, "u-2");
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\db\seed.ts:117:    // u-3 intentionally has NO preferences → tests default behavior
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\services\decision-service.ts:120:      event: type === "declined" ? "decline" : "approval",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\services\loan-service.ts:31:  data: { borrowerName: string; amount: number; loanState: string },
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\services\loan-service.ts:40:    loanState: data.loanState.toUpperCase(),
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\services\loan-service.ts:52:    loanState: data.loanState,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\services\notification-service.ts:11://   user's stored preferences — it is a runtime delivery decision only.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\queue\handlers\notification-handler.ts:10://   event.  The fallback does NOT change stored preferences — it is a
```

</details>


---

<sub>⏱️ 41s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models**

"**/*notification*.ts" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models

```
No files matched the pattern.
```


---

<sub>⏱️ 41s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\rules**

"**/*notification*.ts" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\rules

```
No files matched the pattern.
```


---

<sub>⏱️ 41s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\middleware**

"**/*session*.ts" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\middleware

```
No files matched the pattern.
```


---

<sub>⏱️ 47s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts

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

<sub>⏱️ 47s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\types.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\types.ts

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

<sub>⏱️ 47s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts

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

<sub>⏱️ 47s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\rules\role-permissions.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\rules\role-permissions.ts

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

<sub>⏱️ 47s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\rules\mandatory-events.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\rules\mandatory-events.ts

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

<sub>⏱️ 56s</sub>

### 💬 Copilot

I’ve identified the lesson’s three write surfaces. I’m now checking the existing test style and app wiring so I can add the pure rule tests first and keep the route change as small as possible.

---

<sub>⏱️ 56s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\notification-service.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\notification-service.test.ts

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

<sub>⏱️ 56s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "describe\\(|it\\(|expect\\(",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\05-implementation-workflows\\src\\backend\\tests",
  "output_mode": "content",
  "glob": "**/*.test.ts",
  "-n": true,
  "head_limit": 200
}
```

</details>

<details>
<summary>53 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts:12:describe("State Machine", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts:13:  it("allows intake → review", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts:14:    expect(canTransition("intake", "review")).toBe(true);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts:17:  it("allows review → underwriting", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts:18:    expect(canTransition("review", "underwriting")).toBe(true);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts:21:  it("allows review → intake (rework)", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts:22:    expect(canTransition("review", "intake")).toBe(true);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts:25:  it("blocks intake → decision (skip)", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts:26:    expect(canTransition("intake", "decision")).toBe(false);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts:29:  it("blocks finalized → any state", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts:30:    expect(canTransition("finalized", "intake")).toBe(false);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts:31:    expect(canTransition("finalized", "review")).toBe(false);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts:32:    expect(canTransition("finalized", "underwriting")).toBe(false);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts:33:    expect(canTransition("finalized", "decision")).toBe(false);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts:36:  it("returns valid next states", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts:37:    expect(validNextStates("decision")).toEqual(["finalized", "underwriting"]);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts:38:    expect(validNextStates("finalized")).toEqual([]);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts:41:  it("assertTransition throws for invalid transitions", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts:42:    expect(() => assertTransition("intake", "finalized")).toThrow(
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\notification-service.test.ts:10:describe("Notification Service", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\notification-service.test.ts:11:  it("placeholder — notification service emits queue events", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\notification-service.test.ts:14:    expect(true).toBe(true);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts:25:describe("Business Rules", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts:26:  it("passes for a valid standard loan", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts:27:    expect(validateLoanRules(baseLoan)).toEqual([]);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts:30:  it("rejects zero amount", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts:32:    expect(violations).toHaveLength(1);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts:33:    expect(violations[0].rule).toBe("positive-amount");
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts:36:  it("rejects California loan below minimum", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts:42:    expect(violations.some((v) => v.rule === "ca-min-amount")).toBe(true);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts:45:  it("rejects California loan above maximum", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts:51:    expect(violations.some((v) => v.rule === "ca-max-amount")).toBe(true);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts:55:describe("Approval Roles", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts:56:  it("underwriter can approve loans up to $1M", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts:57:    expect(canApprove("underwriter", 500000)).toBe(true);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts:60:  it("underwriter cannot approve loans over $1M", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts:61:    expect(canApprove("underwriter", 1_500_000)).toBe(false);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts:64:  it("analyst-manager required for loans over $1M", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts:65:    expect(requiredApprovalRoles(1_500_000)).toContain("analyst-manager");
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts:68:  it("compliance-reviewer required for loans over $2.5M", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts:69:    expect(requiredApprovalRoles(3_000_000)).toContain("compliance-reviewer");
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\integration\decisions.test.ts:7:describe("Decision Routes (integration)", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\integration\decisions.test.ts:8:  it("placeholder — POST /api/decisions requires decision state", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\integration\decisions.test.ts:9:    expect(true).toBe(true);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\integration\decisions.test.ts:12:  it("placeholder — delegated sessions cannot record decisions", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\integration\decisions.test.ts:13:    expect(true).toBe(true);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\integration\applications.test.ts:10:describe("Application Routes (integration)", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\integration\applications.test.ts:11:  it("placeholder — GET /api/applications returns 200", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\integration\applications.test.ts:13:    expect(true).toBe(true);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\integration\applications.test.ts:16:  it("placeholder — POST /api/applications validates required fields", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\integration\applications.test.ts:17:    expect(true).toBe(true);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\integration\applications.test.ts:20:  it("placeholder — PATCH /api/applications/:id/status enforces state machine", () => {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\integration\applications.test.ts:21:    expect(true).toBe(true);
```

</details>


---

<sub>⏱️ 56s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\app.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\app.ts

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

<sub>⏱️ 56s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\package.json.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\package.json

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

<sub>⏱️ 56s</sub>

### ❌ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\package.json.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\package.json

```
Path does not exist
```


---

<sub>⏱️ 1m 6s</sub>

### 💬 Copilot

I’ve got the likely slice boundary: the single `PUT /preferences` write path is the cleanest place to harden now, while the bulk `/email` and `/sms` writes look intentionally separate and likely deferred. I’m checking callers and validation context before I patch the tests and rule.

---

<sub>⏱️ 1m 6s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "\\/api\\/notifications\\/preferences|setPreference\\(|preferences\\b",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\05-implementation-workflows\\src",
  "output_mode": "content",
  "glob": "**/*.{ts,tsx}",
  "-n": true,
  "head_limit": 300
}
```

</details>

```
No matches found.
```


---

<sub>⏱️ 1m 6s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\middleware\request-validator.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\middleware\request-validator.ts

<details>
<summary>51 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Request Validator Middleware
3. // ---------------------------------------------------------------------------
4. // Validates request bodies against expected shapes before they reach
5. // route handlers.  Returns 400 with descriptive errors on failure.
6. //
7. // This is intentionally simple — no JSON Schema library dependency.
8. // For production, consider ajv or zod.
9. // ---------------------------------------------------------------------------
10. 
11. import type { Request, Response, NextFunction } from "express";
12. 
13. export type ValidationRule = {
14.   field: string;
15.   type: "string" | "number" | "boolean";
16.   required?: boolean;
17. };
18. 
19. /**
20.  * Factory that returns middleware validating req.body against the given rules.
21.  */
22. export function validateBody(rules: ValidationRule[]) {
23.   return (req: Request, res: Response, next: NextFunction): void => {
24.     const errors: string[] = [];
25. 
26.     for (const rule of rules) {
27.       const value = req.body?.[rule.field];
28. 
29.       if (value === undefined || value === null) {
30.         if (rule.required) {
31.           errors.push(`Missing required field: '${rule.field}'`);
32.         }
33.         continue;
34.       }
35. 
36.       if (typeof value !== rule.type) {
37.         errors.push(
38.           `Field '${rule.field}' must be ${rule.type}, got ${typeof value}`,
39.         );
40.       }
41.     }
42. 
43.     if (errors.length > 0) {
44.       res.status(400).json({ error: "Validation failed.", details: errors });
45.       return;
46.     }
47. 
48.     next();
49.   };
50. }
51.
```

</details>


---

<sub>⏱️ 1m 6s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\middleware\error-handler.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\middleware\error-handler.ts

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

<sub>⏱️ 1m 6s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\loan-repository.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\loan-repository.ts

<details>
<summary>122 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Loan Application Repository
3. // ---------------------------------------------------------------------------
4. // Database operations for loan applications.  All SQL lives here — services
5. // and routes interact with loans only through this module.
6. //
7. // IMPORTANT: The `loan_state` column stores the US state/jurisdiction, NOT
8. // the application lifecycle state.  The lifecycle is in `status`.
9. // ---------------------------------------------------------------------------
10. 
11. import { v4 as uuid } from "uuid";
12. import { getDb } from "../db/connection.js";
13. import type { LoanApplication, ApplicationState } from "./types.js";
14. 
15. const LOAN_COLUMNS = `
16.   id,
17.   borrower_name AS borrowerName,
18.   amount,
19.   loan_state AS loanState,
20.   status,
21.   assigned_underwriter AS assignedUnderwriter,
22.   risk_score AS riskScore,
23.   created_at AS createdAt,
24.   updated_at AS updatedAt
25. `;
26. 
27. export function findAllLoans(): LoanApplication[] {
28.   const db = getDb();
29.   return db
30.     .prepare(
31.       `SELECT ${LOAN_COLUMNS} FROM loan_applications ORDER BY created_at DESC`,
32.     )
33.     .all() as LoanApplication[];
34. }
35. 
36. export function findLoanById(id: string): LoanApplication | undefined {
37.   const db = getDb();
38.   return db.prepare(`SELECT ${LOAN_COLUMNS} FROM loan_applications WHERE id = ?`).get(id) as
39.     | LoanApplication
40.     | undefined;
41. }
42. 
43. export function findLoansByStatus(status: ApplicationState): LoanApplication[] {
44.   const db = getDb();
45.   return db
46.     .prepare(
47.       `SELECT ${LOAN_COLUMNS} FROM loan_applications WHERE status = ? ORDER BY created_at DESC`,
48.     )
49.     .all(status) as LoanApplication[];
50. }
51. 
52. export function findLoansByUnderwriter(
53.   underwriterId: string,
54. ): LoanApplication[] {
55.   const db = getDb();
56.   return db
57.     .prepare(
58.       `SELECT ${LOAN_COLUMNS} FROM loan_applications WHERE assigned_underwriter = ? ORDER BY created_at DESC`,
59.     )
60.     .all(underwriterId) as LoanApplication[];
61. }
62. 
63. export function createLoan(data: {
64.   borrowerName: string;
65.   amount: number;
66.   loanState: string;
67.   assignedUnderwriter: string;
68. }): LoanApplication {
69.   const db = getDb();
70.   const id = uuid();
71.   const now = new Date().toISOString();
72. 
73.   db.prepare(
74.     `INSERT INTO loan_applications (id, borrower_name, amount, loan_state, status, assigned_underwriter, created_at, updated_at)
75.      VALUES (?, ?, ?, ?, 'intake', ?, ?, ?)`,
76.   ).run(
77.     id,
78.     data.borrowerName,
79.     data.amount,
80.     data.loanState.toUpperCase(),
81.     data.assignedUnderwriter,
82.     now,
83.     now,
84.   );
85. 
86.   return findLoanById(id)!;
87. }
88. 
89. export function updateLoanStatus(
90.   id: string,
91.   status: ApplicationState,
92. ): LoanApplication | undefined {
93.   const db = getDb();
94.   const now = new Date().toISOString();
95. 
96.   const result = db
97.     .prepare(
98.       "UPDATE loan_applications SET status = ?, updated_at = ? WHERE id = ?",
99.     )
100.     .run(status, now, id);
101. 
102.   if (result.changes === 0) return undefined;
103.   return findLoanById(id);
104. }
105. 
106. export function updateLoanRiskScore(
107.   id: string,
108.   riskScore: number,
109. ): LoanApplication | undefined {
110.   const db = getDb();
111.   const now = new Date().toISOString();
112. 
113.   const result = db
114.     .prepare(
115.       "UPDATE loan_applications SET risk_score = ?, updated_at = ? WHERE id = ?",
116.     )
117.     .run(riskScore, now, id);
118. 
119.   if (result.changes === 0) return undefined;
120.   return findLoanById(id);
121. }
122.
```

</details>


---

<sub>⏱️ 1m 13s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\rules\business-rules.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\rules\business-rules.ts

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

<sub>⏱️ 1m 13s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts

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

<sub>⏱️ 1m 13s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts

<details>
<summary>47 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // State Machine Tests
3. // ---------------------------------------------------------------------------
4. 
5. import { describe, it, expect } from "vitest";
6. import {
7.   canTransition,
8.   validNextStates,
9.   assertTransition,
10. } from "../../src/rules/state-machine.js";
11. 
12. describe("State Machine", () => {
13.   it("allows intake → review", () => {
14.     expect(canTransition("intake", "review")).toBe(true);
15.   });
16. 
17.   it("allows review → underwriting", () => {
18.     expect(canTransition("review", "underwriting")).toBe(true);
19.   });
20. 
21.   it("allows review → intake (rework)", () => {
22.     expect(canTransition("review", "intake")).toBe(true);
23.   });
24. 
25.   it("blocks intake → decision (skip)", () => {
26.     expect(canTransition("intake", "decision")).toBe(false);
27.   });
28. 
29.   it("blocks finalized → any state", () => {
30.     expect(canTransition("finalized", "intake")).toBe(false);
31.     expect(canTransition("finalized", "review")).toBe(false);
32.     expect(canTransition("finalized", "underwriting")).toBe(false);
33.     expect(canTransition("finalized", "decision")).toBe(false);
34.   });
35. 
36.   it("returns valid next states", () => {
37.     expect(validNextStates("decision")).toEqual(["finalized", "underwriting"]);
38.     expect(validNextStates("finalized")).toEqual([]);
39.   });
40. 
41.   it("assertTransition throws for invalid transitions", () => {
42.     expect(() => assertTransition("intake", "finalized")).toThrow(
43.       "INVALID_STATE",
44.     );
45.   });
46. });
47.
```

</details>


---

<sub>⏱️ 1m 22s</sub>

### ✅ `skill`

**tdd-workflow**

<details>
<summary>Arguments</summary>

```json
{
  "skill": "tdd-workflow"
}
```

</details>

```
Skill "tdd-workflow" loaded successfully. Follow the instructions in the skill context.
```


---

<sub>⏱️ 1m 28s</sub>

### 💬 Copilot

I’ve now got the lesson docs plus the route surface. I’m doing one more spec read, then I’ll write the red tests first and follow with the minimal rule/route wiring.

---

<sub>⏱️ 1m 28s</sub>

### ❌ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\specs\product-spec-notification-preferences.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\specs\product-spec-notification-preferences.md

```
Path does not exist
```


---

<sub>⏱️ 1m 28s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows**

"**/product-spec-notification-preferences.md" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows

```
No files matched the pattern.
```


---

<sub>⏱️ 1m 42s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\frontend**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "setPreference\\(|/api/notifications/preferences|loanState",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\05-implementation-workflows\\src\\frontend",
  "output_mode": "content",
  "glob": "**/*.{ts,tsx}",
  "-n": true,
  "head_limit": 200
}
```

</details>

```
No matches found.
```


---

<sub>⏱️ 1m 42s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\frontend.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\frontend

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

<sub>⏱️ 1m 42s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\frontend**

"**/*notification*.ts*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\frontend

```
No files matched the pattern.
```


---

<sub>⏱️ 1m 48s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Add File: C:\\Users\\nilay\\.copilot\\session-state\\cf510843-0806-43e9-b2ab-e76e4afaad6d\\plan.md\n+1. Inspect lesson docs, specs, and current notification preference write surfaces.\n+2. Add red unit tests for the focused notification preference write hardening slice.\n+3. Implement a pure notification preference write rule module with explicit inputs.\n+4. Wire the minimal production change into the current PUT /preferences route only.\n+5. Review changed files and hand off expected red/green behavior plus deferred surfaces.\n*** End Patch\n"
```

</details>

```
Added 1 file(s): C:\Users\nilay\.copilot\session-state\cf510843-0806-43e9-b2ab-e76e4afaad6d\plan.md
```


---

<sub>⏱️ 2m 17s</sub>

### 💬 Copilot

I’ve settled the slice: harden only `PUT /api/notifications/preferences` for now, and leave the bulk `/email` and `/sms` write routes explicitly deferred. I’m adding the red unit tests for the pure rule first.

---

<sub>⏱️ 2m 17s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Add File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\05-implementation-workflows\\src\\backend\\tests\\unit\\notification-preference-write-rules.test.ts\n+import { describe, expect, it } from \"vitest\";\n+import {\n+  evaluateNotificationPreferenceWrite,\n+} from \"../../src/rules/notification-preference-write-rules.js\";\n+import type { NotificationPreference } from \"../../src/models/types.js\";\n+\n+function buildPreference(\n+  overrides: Partial<NotificationPreference>,\n+): NotificationPreference {\n+  return {\n+    userId: \"u-1\",\n+    event: \"manual-review-escalation\",\n+    channel: \"email\",\n+    enabled: true,\n+    updatedAt: \"2026-03-14T00:00:00.000Z\",\n+    updatedBy: \"u-1\",\n+    ...overrides,\n+  };\n+}\n+\n+describe(\"evaluateNotificationPreferenceWrite\", () => {\n+  it(\"allows disabling escalation SMS when escalation email stays enabled\", () => {\n+    // FALSE POSITIVE: disabling one escalation channel is still valid\n+    // when the mandatory event keeps another enabled channel.\n+    const result = evaluateNotificationPreferenceWrite({\n+      existingPreferences: [\n+        buildPreference({ channel: \"email\", enabled: true }),\n+        buildPreference({ channel: \"sms\", enabled: true }),\n+      ],\n+      nextPreference: buildPreference({ channel: \"sms\", enabled: false }),\n+    });\n+\n+    expect(result).toEqual({ allowed: true });\n+  });\n+\n+  it(\"blocks disabling the last enabled channel for manual-review-escalation\", () => {\n+    // HARD NEGATIVE: the mandatory escalation event cannot end up with\n+    // every delivery channel disabled.\n+    const result = evaluateNotificationPreferenceWrite({\n+      existingPreferences: [\n+        buildPreference({ channel: \"email\", enabled: true }),\n+        buildPreference({ channel: \"sms\", enabled: false }),\n+      ],\n+      nextPreference: buildPreference({ channel: \"email\", enabled: false }),\n+    });\n+\n+    expect(result).toEqual({\n+      allowed: false,\n+      reason:\n+        \"manual-review-escalation must keep at least one notification channel enabled.\",\n+    });\n+  });\n+\n+  it(\"blocks enabling decline SMS for California loan state abbreviations\", () => {\n+    const result = evaluateNotificationPreferenceWrite({\n+      existingPreferences: [\n+        buildPreference({\n+          event: \"decline\",\n+          channel: \"email\",\n+          enabled: true,\n+        }),\n+      ],\n+      nextPreference: buildPreference({\n+        event: \"decline\",\n+        channel: \"sms\",\n+        enabled: true,\n+      }),\n+      loanState: \"CA\",\n+    });\n+\n+    expect(result).toEqual({\n+      allowed: false,\n+      reason:\n+        \"LEGAL-218: decline SMS cannot be enabled for California loans.\",\n+    });\n+  });\n+\n+  it(\"blocks enabling decline SMS for California loan state names\", () => {\n+    const result = evaluateNotificationPreferenceWrite({\n+      existingPreferences: [],\n+      nextPreference: buildPreference({\n+        event: \"decline\",\n+        channel: \"sms\",\n+        enabled: true,\n+      }),\n+      loanState: \"California\",\n+    });\n+\n+    expect(result).toEqual({\n+      allowed: false,\n+      reason:\n+        \"LEGAL-218: decline SMS cannot be enabled for California loans.\",\n+    });\n+  });\n+\n+  it(\"allows non-California decline SMS writes\", () => {\n+    const result = evaluateNotificationPreferenceWrite({\n+      existingPreferences: [],\n+      nextPreference: buildPreference({\n+        event: \"decline\",\n+        channel: \"sms\",\n+        enabled: true,\n+      }),\n+      loanState: \"NY\",\n+    });\n+\n+    expect(result).toEqual({ allowed: true });\n+  });\n+});\n*** End Patch\n"
```

</details>

```
Added 1 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts
```


---

<sub>⏱️ 2m 33s</sub>

### 💬 Copilot

The tests are in place. I’m adding the pure rule module now, keeping it explicit-input only and reusing the existing mandatory-event definition instead of duplicating it.

---

<sub>⏱️ 2m 33s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Add File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\05-implementation-workflows\\src\\backend\\src\\rules\\notification-preference-write-rules.ts\n+// ---------------------------------------------------------------------------\n+// Notification Preference Write Rules\n+// ---------------------------------------------------------------------------\n+// FALSE POSITIVE:\n+//   Disabling manual-review-escalation SMS is still valid when escalation email\n+//   remains enabled. The write should not be rejected just because one channel\n+//   turns off.\n+//\n+// HARD NEGATIVE:\n+//   manual-review-escalation is a mandatory notification event for the\n+//   underwriting -> decision flow. A write must never leave that event with all\n+//   delivery channels disabled.\n+// ---------------------------------------------------------------------------\n+\n+import type { LoanApplication, NotificationPreference } from \"../models/types.js\";\n+import { getMandatoryEvents } from \"./mandatory-events.js\";\n+\n+export interface NotificationPreferenceWriteInput {\n+  existingPreferences: NotificationPreference[];\n+  nextPreference: NotificationPreference;\n+  loanState?: LoanApplication[\"loanState\"];\n+}\n+\n+export type NotificationPreferenceWriteDecision =\n+  | { allowed: true }\n+  | { allowed: false; reason: string };\n+\n+const MANDATORY_WRITE_EVENTS = new Set(\n+  getMandatoryEvents(\"underwriting\", \"decision\"),\n+);\n+\n+export function evaluateNotificationPreferenceWrite(\n+  input: NotificationPreferenceWriteInput,\n+): NotificationPreferenceWriteDecision {\n+  if (blocksCaliforniaDeclineSms(input)) {\n+    return {\n+      allowed: false,\n+      reason: \"LEGAL-218: decline SMS cannot be enabled for California loans.\",\n+    };\n+  }\n+\n+  if (blocksMandatoryEventChannelRemoval(input)) {\n+    return {\n+      allowed: false,\n+      reason:\n+        \"manual-review-escalation must keep at least one notification channel enabled.\",\n+    };\n+  }\n+\n+  return { allowed: true };\n+}\n+\n+function blocksCaliforniaDeclineSms({\n+  nextPreference,\n+  loanState,\n+}: NotificationPreferenceWriteInput): boolean {\n+  return (\n+    nextPreference.event === \"decline\" &&\n+    nextPreference.channel === \"sms\" &&\n+    nextPreference.enabled &&\n+    isCaliforniaLoanState(loanState)\n+  );\n+}\n+\n+function blocksMandatoryEventChannelRemoval({\n+  existingPreferences,\n+  nextPreference,\n+}: NotificationPreferenceWriteInput): boolean {\n+  if (\n+    !MANDATORY_WRITE_EVENTS.has(nextPreference.event) ||\n+    nextPreference.enabled\n+  ) {\n+    return false;\n+  }\n+\n+  const nextEventPreferences = mergeNextPreference(existingPreferences, nextPreference)\n+    .filter((preference) => preference.event === nextPreference.event);\n+\n+  return !nextEventPreferences.some((preference) => preference.enabled);\n+}\n+\n+function mergeNextPreference(\n+  existingPreferences: NotificationPreference[],\n+  nextPreference: NotificationPreference,\n+): NotificationPreference[] {\n+  const withoutCurrentChannel = existingPreferences.filter(\n+    (preference) =>\n+      !(\n+        preference.event === nextPreference.event &&\n+        preference.channel === nextPreference.channel\n+      ),\n+  );\n+\n+  return [...withoutCurrentChannel, nextPreference];\n+}\n+\n+function isCaliforniaLoanState(loanState?: LoanApplication[\"loanState\"]): boolean {\n+  if (!loanState) {\n+    return false;\n+  }\n+\n+  const normalized = loanState.trim().toUpperCase();\n+  return normalized === \"CA\" || normalized === \"CALIFORNIA\";\n+}\n*** End Patch\n"
```

</details>

```
Added 1 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\rules\notification-preference-write-rules.ts
```


---

<sub>⏱️ 2m 42s</sub>

### 💬 Copilot

I’ve added the pure rule. Last step is the minimal route wiring in the current single-write path, while leaving the delegated-session and role guards untouched.

---

<sub>⏱️ 2m 42s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Update File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\05-implementation-workflows\\src\\backend\\src\\routes\\notifications.ts\n@@\n import { validateBody } from \"../middleware/request-validator.js\";\n import { hasPermission } from \"../rules/role-permissions.js\";\n+import { evaluateNotificationPreferenceWrite } from \"../rules/notification-preference-write-rules.js\";\n import { auditAction } from \"../services/audit-service.js\";\n import * as prefRepo from \"../models/preference-repository.js\";\n@@\n   validateBody([\n     { field: \"userId\", type: \"string\", required: true },\n     { field: \"event\", type: \"string\", required: true },\n     { field: \"channel\", type: \"string\", required: true },\n     { field: \"enabled\", type: \"boolean\", required: true },\n+    { field: \"loanState\", type: \"string\" },\n   ]),\n   (req, res, next) => {\n@@\n-      const { userId, event, channel, enabled } = req.body;\n+      const { userId, event, channel, enabled, loanState } = req.body;\n       const now = new Date().toISOString();\n+      const existingPreferences = prefRepo.findPreferencesForUser(userId);\n \n       const previous = prefRepo.findPreference(userId, event, channel);\n \n       const pref: NotificationPreference = {\n@@\n         updatedBy: session.actor.id,\n       };\n+\n+      const writeDecision = evaluateNotificationPreferenceWrite({\n+        existingPreferences,\n+        nextPreference: pref,\n+        loanState,\n+      });\n+\n+      if (!writeDecision.allowed) {\n+        next(new Error(`VALIDATION: ${writeDecision.reason}`));\n+        return;\n+      }\n \n       prefRepo.setPreference(pref);\n*** End Patch\n"
```

</details>

```
Modified 1 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts
```


---

<sub>⏱️ 2m 47s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\rules\notification-preference-write-rules.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\rules\notification-preference-write-rules.ts

<details>
<summary>105 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Notification Preference Write Rules
3. // ---------------------------------------------------------------------------
4. // FALSE POSITIVE:
5. //   Disabling manual-review-escalation SMS is still valid when escalation email
6. //   remains enabled. The write should not be rejected just because one channel
7. //   turns off.
8. //
9. // HARD NEGATIVE:
10. //   manual-review-escalation is a mandatory notification event for the
11. //   underwriting -> decision flow. A write must never leave that event with all
12. //   delivery channels disabled.
13. // ---------------------------------------------------------------------------
14. 
15. import type { LoanApplication, NotificationPreference } from "../models/types.js";
16. import { getMandatoryEvents } from "./mandatory-events.js";
17. 
18. export interface NotificationPreferenceWriteInput {
19.   existingPreferences: NotificationPreference[];
20.   nextPreference: NotificationPreference;
21.   loanState?: LoanApplication["loanState"];
22. }
23. 
24. export type NotificationPreferenceWriteDecision =
25.   | { allowed: true }
26.   | { allowed: false; reason: string };
27. 
28. const MANDATORY_WRITE_EVENTS = new Set(
29.   getMandatoryEvents("underwriting", "decision"),
30. );
31. 
32. export function evaluateNotificationPreferenceWrite(
33.   input: NotificationPreferenceWriteInput,
34. ): NotificationPreferenceWriteDecision {
35.   if (blocksCaliforniaDeclineSms(input)) {
36.     return {
37.       allowed: false,
38.       reason: "LEGAL-218: decline SMS cannot be enabled for California loans.",
39.     };
40.   }
41. 
42.   if (blocksMandatoryEventChannelRemoval(input)) {
43.     return {
44.       allowed: false,
45.       reason:
46.         "manual-review-escalation must keep at least one notification channel enabled.",
47.     };
48.   }
49. 
50.   return { allowed: true };
51. }
52. 
53. function blocksCaliforniaDeclineSms({
54.   nextPreference,
55.   loanState,
56. }: NotificationPreferenceWriteInput): boolean {
57.   return (
58.     nextPreference.event === "decline" &&
59.     nextPreference.channel === "sms" &&
60.     nextPreference.enabled &&
61.     isCaliforniaLoanState(loanState)
62.   );
63. }
64. 
65. function blocksMandatoryEventChannelRemoval({
66.   existingPreferences,
67.   nextPreference,
68. }: NotificationPreferenceWriteInput): boolean {
69.   if (
70.     !MANDATORY_WRITE_EVENTS.has(nextPreference.event) ||
71.     nextPreference.enabled
72.   ) {
73.     return false;
74.   }
75. 
76.   const nextEventPreferences = mergeNextPreference(existingPreferences, nextPreference)
77.     .filter((preference) => preference.event === nextPreference.event);
78. 
79.   return !nextEventPreferences.some((preference) => preference.enabled);
80. }
81. 
82. function mergeNextPreference(
83.   existingPreferences: NotificationPreference[],
84.   nextPreference: NotificationPreference,
85. ): NotificationPreference[] {
86.   const withoutCurrentChannel = existingPreferences.filter(
87.     (preference) =>
88.       !(
89.         preference.event === nextPreference.event &&
90.         preference.channel === nextPreference.channel
91.       ),
92.   );
93. 
94.   return [...withoutCurrentChannel, nextPreference];
95. }
96. 
97. function isCaliforniaLoanState(loanState?: LoanApplication["loanState"]): boolean {
98.   if (!loanState) {
99.     return false;
100.   }
101. 
102.   const normalized = loanState.trim().toUpperCase();
103.   return normalized === "CA" || normalized === "CALIFORNIA";
104. }
105.
```

</details>


---

<sub>⏱️ 2m 47s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts (lines 16-120)

<details>
<summary>105 lines</summary>

```
16. import { Router } from "express";
17. import { requireRole } from "../middleware/auth.js";
18. import { validateBody } from "../middleware/request-validator.js";
19. import { hasPermission } from "../rules/role-permissions.js";
20. import { evaluateNotificationPreferenceWrite } from "../rules/notification-preference-write-rules.js";
21. import { auditAction } from "../services/audit-service.js";
22. import * as prefRepo from "../models/preference-repository.js";
23. import type {
24.   SessionContext,
25.   NotificationPreference,
26. } from "../models/types.js";
27. 
28. export const notificationRoutes = Router();
29. 
30. function firstParam(value: string | string[]): string {
31.   return Array.isArray(value) ? value[0] : value;
32. }
33. 
34. /** GET /api/notifications/preferences/:userId — get preferences for a user. */
35. notificationRoutes.get(
36.   "/preferences/:userId",
37.   requireRole("underwriter", "analyst-manager", "compliance-reviewer"),
38.   (req, res) => {
39.     const prefs = prefRepo.findPreferencesForUser(
40.       firstParam(req.params.userId),
41.     );
42.     res.json(prefs);
43.   },
44. );
45. 
46. /** PUT /api/notifications/preferences — set a notification preference. */
47. notificationRoutes.put(
48.   "/preferences",
49.   requireRole("underwriter", "analyst-manager"),
50.   validateBody([
51.     { field: "userId", type: "string", required: true },
52.     { field: "event", type: "string", required: true },
53.     { field: "channel", type: "string", required: true },
54.     { field: "enabled", type: "boolean", required: true },
55.     { field: "loanState", type: "string" },
56.   ]),
57.   (req, res, next) => {
58.     try {
59.       const session = req.session as SessionContext;
60. 
61.       // Block writes in delegated sessions
62.       if (session.delegatedFor) {
63.         res.status(403).json({
64.           error: "Delegated sessions cannot modify notification preferences.",
65.         });
66.         return;
67.       }
68. 
69.       // Additional permission check
70.       if (!hasPermission(session.actor.role, "notification-pref:write")) {
71.         res.status(403).json({
72.           error: `Role '${session.actor.role}' cannot modify notification preferences.`,
73.         });
74.         return;
75.       }
76. 
77.       const { userId, event, channel, enabled, loanState } = req.body;
78.       const now = new Date().toISOString();
79.       const existingPreferences = prefRepo.findPreferencesForUser(userId);
80. 
81.       const previous = prefRepo.findPreference(userId, event, channel);
82. 
83.       const pref: NotificationPreference = {
84.         userId,
85.         event,
86.         channel,
87.         enabled,
88.         updatedAt: now,
89.         updatedBy: session.actor.id,
90.       };
91. 
92.       const writeDecision = evaluateNotificationPreferenceWrite({
93.         existingPreferences,
94.         nextPreference: pref,
95.         loanState,
96.       });
97. 
98.       if (!writeDecision.allowed) {
99.         next(new Error(`VALIDATION: ${writeDecision.reason}`));
100.         return;
101.       }
102. 
103.       prefRepo.setPreference(pref);
104. 
105.       // Audit the preference change
106.       auditAction(
107.         session,
108.         "preference.updated",
109.         previous ?? null,
110.         pref,
111.         "notification-routes",
112.       );
113. 
114.       res.json(pref);
115.     } catch (err) {
116.       next(err);
117.     }
118.   },
119. );
120.
```

</details>


---

<sub>⏱️ 2m 47s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts

<details>
<summary>110 lines</summary>

```
1. import { describe, expect, it } from "vitest";
2. import {
3.   evaluateNotificationPreferenceWrite,
4. } from "../../src/rules/notification-preference-write-rules.js";
5. import type { NotificationPreference } from "../../src/models/types.js";
6. 
7. function buildPreference(
8.   overrides: Partial<NotificationPreference>,
9. ): NotificationPreference {
10.   return {
11.     userId: "u-1",
12.     event: "manual-review-escalation",
13.     channel: "email",
14.     enabled: true,
15.     updatedAt: "2026-03-14T00:00:00.000Z",
16.     updatedBy: "u-1",
17.     ...overrides,
18.   };
19. }
20. 
21. describe("evaluateNotificationPreferenceWrite", () => {
22.   it("allows disabling escalation SMS when escalation email stays enabled", () => {
23.     // FALSE POSITIVE: disabling one escalation channel is still valid
24.     // when the mandatory event keeps another enabled channel.
25.     const result = evaluateNotificationPreferenceWrite({
26.       existingPreferences: [
27.         buildPreference({ channel: "email", enabled: true }),
28.         buildPreference({ channel: "sms", enabled: true }),
29.       ],
30.       nextPreference: buildPreference({ channel: "sms", enabled: false }),
31.     });
32. 
33.     expect(result).toEqual({ allowed: true });
34.   });
35. 
36.   it("blocks disabling the last enabled channel for manual-review-escalation", () => {
37.     // HARD NEGATIVE: the mandatory escalation event cannot end up with
38.     // every delivery channel disabled.
39.     const result = evaluateNotificationPreferenceWrite({
40.       existingPreferences: [
41.         buildPreference({ channel: "email", enabled: true }),
42.         buildPreference({ channel: "sms", enabled: false }),
43.       ],
44.       nextPreference: buildPreference({ channel: "email", enabled: false }),
45.     });
46. 
47.     expect(result).toEqual({
48.       allowed: false,
49.       reason:
50.         "manual-review-escalation must keep at least one notification channel enabled.",
51.     });
52.   });
53. 
54.   it("blocks enabling decline SMS for California loan state abbreviations", () => {
55.     const result = evaluateNotificationPreferenceWrite({
56.       existingPreferences: [
57.         buildPreference({
58.           event: "decline",
59.           channel: "email",
60.           enabled: true,
61.         }),
62.       ],
63.       nextPreference: buildPreference({
64.         event: "decline",
65.         channel: "sms",
66.         enabled: true,
67.       }),
68.       loanState: "CA",
69.     });
70. 
71.     expect(result).toEqual({
72.       allowed: false,
73.       reason:
74.         "LEGAL-218: decline SMS cannot be enabled for California loans.",
75.     });
76.   });
77. 
78.   it("blocks enabling decline SMS for California loan state names", () => {
79.     const result = evaluateNotificationPreferenceWrite({
80.       existingPreferences: [],
81.       nextPreference: buildPreference({
82.         event: "decline",
83.         channel: "sms",
84.         enabled: true,
85.       }),
86.       loanState: "California",
87.     });
88. 
89.     expect(result).toEqual({
90.       allowed: false,
91.       reason:
92.         "LEGAL-218: decline SMS cannot be enabled for California loans.",
93.     });
94.   });
95. 
96.   it("allows non-California decline SMS writes", () => {
97.     const result = evaluateNotificationPreferenceWrite({
98.       existingPreferences: [],
99.       nextPreference: buildPreference({
100.         event: "decline",
101.         channel: "sms",
102.         enabled: true,
103.       }),
104.       loanState: "NY",
105.     });
106. 
107.     expect(result).toEqual({ allowed: true });
108.   });
109. });
110.
```

</details>


---

<sub>⏱️ 3m 1s</sub>

### 💬 Copilot

Implemented the focused hardening slice in:

`src/backend/tests/unit/notification-preference-write-rules.test.ts`

`src/backend/src/rules/notification-preference-write-rules.ts`

`src/backend/src/routes/notifications.ts`

Before the production change, the new tests should fail on: allowing the last `manual-review-escalation` channel to be disabled, and allowing `decline` SMS to be enabled for `CA`/`California`. After the change, these should pass, along with the false-positive case that disabling escalation SMS while escalation email stays enabled remains allowed, plus the non-California decline SMS allow case.

Intentionally deferred write surfaces: `PUT /preferences/:userId/email` and `PUT /preferences/:userId/sms`.

---

<sub>Generated by [GitHub Copilot CLI](https://github.com/features/copilot/cli)</sub>
