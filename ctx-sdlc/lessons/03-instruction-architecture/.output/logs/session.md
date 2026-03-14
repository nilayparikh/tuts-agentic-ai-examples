# 🤖 Copilot CLI Session

> [!NOTE]
> - **Session ID:** `1f3eda36-a79d-4c3e-99f8-897f393d9dbd`  
> - **Started:** 14/03/2026, 17:37:43  
> - **Duration:** 2m 41s  
> - **Exported:** 14/03/2026, 17:40:24  

---

<sub>⏱️ 5s</sub>

### 👤 User

Create a pure business-rule module at src/backend/src/rules/notification-channel-rules.ts and matching tests at src/backend/tests/unit/notification-channel-rules.test.ts. First inspect the existing backend rule and test surfaces to discover the current notification-channel conventions and the existing mandatory-event source of truth. The rule should validate when disabling a notification channel is allowed for mandatory events, including the California decline LEGAL-218 restriction. Follow the repository conventions you discover. Reuse the discovered mandatory-event source or explicit function inputs; do not assume its file path and do not create a second hardcoded mandatory-events list or helper. Return structured results with human-readable reasons, include top-of-module false-positive and hard-negative comments, and add tests for happy path, boundary, false positive, and hard negative scenarios. Apply the change directly in code instead of only describing it. Do not run npm install, npm test, or any shell commands. Inspect and edit files only.

---

<sub>⏱️ 19s</sub>

### ✅ `sql`

**Seed work todos**

<details>
<summary>Arguments</summary>

```json
{
  "description": "Seed work todos",
  "query": "INSERT INTO todos (id, title, description, status) VALUES\n  ('inspect-rule-surfaces', 'Inspect rule surfaces', 'Read architecture docs plus existing backend rule and test files to discover notification-channel conventions and the mandatory-event source of truth.', 'in_progress'),\n  ('implement-channel-rules', 'Implement channel rules', 'Create the pure notification-channel-rules business module following discovered conventions and reuse the existing mandatory-event source of truth.', 'pending'),\n  ('add-rule-tests', 'Add rule tests', 'Create matching unit tests covering happy path, boundary, false positive, and hard negative scenarios for notification channel disable validation.', 'pending'),\n  ('verify-edits', 'Verify edits', 'Review the final code and tests for consistency with repository conventions without running shell commands.', 'pending');"
}
```

</details>

```
4 row(s) inserted. Last inserted row ID: 4.
```


---

<sub>⏱️ 19s</sub>

### ✅ `glob`

**src/backend/src/rules/**/*.ts**

"src/backend/src/rules/**/*.ts"

```
No files matched the pattern.
```


---

<sub>⏱️ 19s</sub>

### ✅ `glob`

**src/backend/tests/**/*.test.ts**

"src/backend/tests/**/*.test.ts"

```
No files matched the pattern.
```


---

<sub>⏱️ 19s</sub>

### ✅ `glob`

**docs/*.md**

"docs/*.md"

```
.\docs\architecture.md
.\docs\instruction-layering-example.md
```


---

<sub>⏱️ 19s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "mandatory-events|notification-channel|LEGAL-218|decline",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\03-instruction-architecture",
  "output_mode": "content",
  "glob": "src/backend/src/**/*.ts",
  "-n": true,
  "head_limit": 200
}
```

</details>

```
No matches found.
```


---

<sub>⏱️ 25s</sub>

### 💬 Copilot

I’m mapping the backend layout first so the new rule matches the project’s actual patterns instead of guessing paths or conventions.

---

<sub>⏱️ 25s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture (lines 1-200)

<details>
<summary>8 lines</summary>

```
.github
.output
ASSESSMENT.md
docs
README.md
src
util.py
__pycache__
```

</details>


---

<sub>⏱️ 25s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src (lines 1-200)

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

<sub>⏱️ 25s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\docs\architecture.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\docs\architecture.md (lines 1-250)

<details>
<summary>60 lines</summary>

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
19.       models/               ← Domain types + DB repository classes
20.       routes/               ← HTTP route handlers
21.       rules/                ← State machine, business rules, role permissions
22.       services/             ← Business logic orchestration
23.     tests/
24.       unit/                 ← Pure function and rule tests
25.       integration/          ← Route + service tests
26.   frontend/
27.     src/
28.       api/                  ← Typed HTTP client
29.       pages/                ← Dashboard, detail, preferences
30.       components/           ← UI building blocks
31.     styles/
32. ```
33. 
34. ## Instruction Scoping
35. 
36. Instructions are scoped to match the source structure:
37. 
38. | Instruction File                 | `applyTo`                       | Covers                     |
39. | -------------------------------- | ------------------------------- | -------------------------- |
40. | `copilot-instructions.md`        | all files                       | Global conventions         |
41. | `backend.instructions.md`        | `src/backend/src/**/*.ts`       | Route and service patterns |
42. | `business-rules.instructions.md` | `src/backend/src/rules/**`      | Rule authoring standards   |
43. | `security.instructions.md`       | `src/backend/src/middleware/**` | Auth and security patterns |
44. | `testing.instructions.md`        | `src/backend/tests/**`          | Test conventions           |
45. 
46. This layering means editing a file in `src/backend/src/rules/` activates three
47. instruction files simultaneously: global, backend, and business-rules.
48. 
49. ## Lesson 03 Example Target
50. 
51. The lesson demo should deliberately cross instruction boundaries.
52. 
53. The preferred change is:
54. 
55. - add a pure rule module in `src/backend/src/rules/notification-channel-rules.ts`
56. - add matching tests in `src/backend/tests/unit/notification-channel-rules.test.ts`
57. - keep the rule pure and side-effect free
58. - keep the tests explicit and behavior-oriented
59. 
60. That combination lets the model pick up repository-wide rules, backend conventions, business-rule conventions, and test conventions in one task.
````

</details>


---

<sub>⏱️ 25s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\docs\instruction-layering-example.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\docs\instruction-layering-example.md (lines 1-250)

<details>
<summary>59 lines</summary>

```
1. # Lesson 03 — Instruction Layering Example
2. 
3. This document defines the concrete example used in Lesson 03.
4. 
5. ## Objective
6. 
7. Show that layered instruction files improve both where GitHub Copilot CLI edits and how it structures the generated code.
8. 
9. The example should touch two scoped surfaces:
10. 
11. - `src/backend/src/rules/notification-channel-rules.ts`
12. - `src/backend/tests/unit/notification-channel-rules.test.ts`
13. 
14. ## Expected Change Shape
15. 
16. The preferred implementation for this lesson is:
17. 
18. - create a new pure business-rule module for notification channel changes
19. - create matching unit tests that mirror the source path
20. - keep the change local to the rule and its tests
21. 
22. ## Required Constraints
23. 
24. These constraints are part of the example and must be preserved by the generated code:
25. 
26. 1. The rule module must stay pure: no Express imports, no database access, no audit writes, no queue usage.
27. 2. The rule module must return structured results rather than a bare boolean.
28. 3. California-specific restriction text must include `LEGAL-218` in both the rule metadata and the human-readable reason.
29. 4. The module header comments must document one false positive and one hard negative scenario.
30. 5. The tests must cover happy path, boundary case, false positive, and hard negative scenarios.
31. 6. The tests must use explicit assertions rather than snapshots.
32. 7. Do not modify `src/backend/src/models/types.ts` for this lesson.
33. 8. Do not run shell commands during the assessment run.
34. 9. Discover and reuse the existing mandatory-event source of truth instead of creating a new hardcoded mandatory-events list or helper.
35. 10. Do not assume a fixed source file path for that mandatory-event knowledge; discover the current source-of-truth location from the lesson surfaces.
36. 
37. ## Concrete Scenario
38. 
39. For this lesson, the rule should validate notification channel changes for mandatory events.
40. 
41. The intended hard case is:
42. 
43. - on California loans, decline notifications must not end up with every channel disabled
44. - disabling SMS is acceptable when email remains enabled
45. - disabling the last enabled channel for a California decline notification should fail with a structured `LEGAL-218` reason
46. 
47. Good output usually introduces a function like `validateNotificationChannelChange(...)` with a narrow input shape and a structured result object.
48. 
49. The preferred implementation should reuse the discovered mandatory-event source of truth rather than introducing a second source of truth or assuming a fixed file path for it.
50. 
51. ## What Good Output Looks Like
52. 
53. Good output will usually:
54. 
55. - add one rule file and one matching test file
56. - keep all business logic inside the rule module
57. - keep tests close to the instruction language: false positive, hard negative, and boundary cases should be visible in test names or comments
58. - avoid inventing services, repositories, or new global domain types
59. - avoid duplicating mandatory-event definitions inside the new rule module
```

</details>


---

<sub>⏱️ 29s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture**

"src/backend/src/**/*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture

```
No files matched the pattern.
```


---

<sub>⏱️ 29s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture**

"src/backend/tests/**/*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture

```
No files matched the pattern.
```


---

<sub>⏱️ 29s</sub>

### ✅ `sql`

**Track inspection todo**

<details>
<summary>Arguments</summary>

```json
{
  "description": "Track inspection todo",
  "query": "UPDATE todos SET status = 'in_progress' WHERE id = 'inspect-rule-surfaces';"
}
```

</details>

```
1 row(s) updated.
```


---

<sub>⏱️ 36s</sub>

### 💬 Copilot

I found the lesson docs, but the glob patterns aren’t resolving under this workspace the way I expected, so I’m switching to direct directory reads to discover the actual backend files safely.

---

<sub>⏱️ 36s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend (lines 1-250)

```
dist
src
tests
tsconfig.json
```


---

<sub>⏱️ 36s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src (lines 1-250)

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

<sub>⏱️ 36s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\tests.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\tests (lines 1-250)

```
integration
unit
```


---

<sub>⏱️ 42s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\rules.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\rules (lines 1-250)

```
business-rules.ts
mandatory-events.ts
role-permissions.ts
state-machine.ts
```


---

<sub>⏱️ 42s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\tests\unit.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\tests\unit (lines 1-250)

```
business-rules.test.ts
notification-service.test.ts
state-machine.test.ts
```


---

<sub>⏱️ 42s</sub>

### ✅ `sql`

**Mark implementation ready**

<details>
<summary>Arguments</summary>

```json
{
  "description": "Mark implementation ready",
  "query": "UPDATE todos SET status = 'pending' WHERE id = 'implement-channel-rules'; UPDATE todos SET status = 'pending' WHERE id = 'add-rule-tests';"
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

<sub>⏱️ 46s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Add File: C:/Users/nilay/.copilot/session-state/1f3eda36-a79d-4c3e-99f8-897f393d9dbd/plan.md\n+1. Inspect backend rule and test surfaces, including the mandatory-event source of truth.\n+2. Implement a pure notification channel rule module that reuses the discovered mandatory-event source and returns structured results with human-readable reasons.\n+3. Add unit tests covering happy path, boundary, false positive, and hard negative scenarios.\n+4. Review the edited files for consistency with repository conventions.\n*** End Patch\n"
```

</details>

```
Added 1 file(s): C:\Users\nilay\.copilot\session-state\1f3eda36-a79d-4c3e-99f8-897f393d9dbd\plan.md
```


---

<sub>⏱️ 57s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\rules\mandatory-events.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\rules\mandatory-events.ts (lines 1-250)

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

<sub>⏱️ 57s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\rules\business-rules.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\rules\business-rules.ts (lines 1-250)

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

<sub>⏱️ 57s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\rules\state-machine.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\rules\state-machine.ts (lines 1-250)

<details>
<summary>43 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // State Machine Rules
3. // ---------------------------------------------------------------------------
4. // Enforces the loan application lifecycle.  Valid transitions are defined
5. // in models/types.ts (VALID_TRANSITIONS).
6. //
7. // IMPORTANT: Finalized applications can NEVER transition to any other state.
8. // This is a hard business rule — there is no admin override.
9. // ---------------------------------------------------------------------------
10. 
11. import { VALID_TRANSITIONS, type ApplicationState } from "../models/types.js";
12. 
13. /**
14.  * Check whether a state transition is legal.
15.  */
16. export function canTransition(
17.   from: ApplicationState,
18.   to: ApplicationState,
19. ): boolean {
20.   return VALID_TRANSITIONS[from]?.includes(to) ?? false;
21. }
22. 
23. /**
24.  * Get the list of valid next states from the current state.
25.  */
26. export function validNextStates(from: ApplicationState): ApplicationState[] {
27.   return VALID_TRANSITIONS[from] ?? [];
28. }
29. 
30. /**
31.  * Guard function — throws if the transition is not allowed.
32.  */
33. export function assertTransition(
34.   from: ApplicationState,
35.   to: ApplicationState,
36. ): void {
37.   if (!canTransition(from, to)) {
38.     throw new Error(
39.       `INVALID_STATE: Cannot transition from '${from}' to '${to}'. ` +
40.         `Valid transitions from '${from}': [${validNextStates(from).join(", ")}]`,
41.     );
42.   }
43. }
```

</details>


---

<sub>⏱️ 57s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\rules\role-permissions.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\rules\role-permissions.ts (lines 1-250)

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

<sub>⏱️ 57s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\tests\unit\business-rules.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\tests\unit\business-rules.test.ts (lines 1-300)

<details>
<summary>71 lines</summary>

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
```

</details>


---

<sub>⏱️ 57s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\tests\unit\state-machine.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\tests\unit\state-machine.test.ts (lines 1-300)

<details>
<summary>46 lines</summary>

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
```

</details>


---

<sub>⏱️ 57s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\models\types.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\models\types.ts (lines 1-250)

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

<sub>⏱️ 1m 3s</sub>

### 💬 Copilot

I found the mandatory-event source of truth in `src/backend/src/rules/mandatory-events.ts`. Next I’m checking the notification-related backend surfaces so the new rule API and test names align with existing terminology.

---

<sub>⏱️ 1m 3s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "NotificationPreference|notification|mandatory",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\03-instruction-architecture\\src\\backend\\src",
  "output_mode": "files_with_matches",
  "glob": "**/*.ts",
  "head_limit": 200
}
```

</details>

<details>
<summary>14 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\services\notification-service.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\services\loan-service.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\services\decision-service.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\config\feature-flags.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\app.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\models\preference-repository.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\models\types.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\middleware\auth.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\routes\notifications.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\db\seed.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\rules\mandatory-events.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\queue\contracts.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\rules\role-permissions.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\queue\handlers\notification-handler.ts
```

</details>


---

<sub>⏱️ 1m 3s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\tests\unit\notification-service.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\tests\unit\notification-service.test.ts (lines 1-320)

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

<sub>⏱️ 1m 3s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\services.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\services (lines 1-250)

```
audit-service.ts
decision-service.ts
loan-service.ts
notification-service.ts
```


---

<sub>⏱️ 1m 3s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\routes.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\routes (lines 1-250)

```
applications.ts
audit.ts
decisions.ts
notifications.ts
queue-status.ts
```


---

<sub>⏱️ 1m 9s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\routes\notifications.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\routes\notifications.ts (lines 1-320)

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

<sub>⏱️ 1m 9s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\models\preference-repository.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\models\preference-repository.ts (lines 1-320)

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

<sub>⏱️ 1m 9s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\services\notification-service.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\services\notification-service.ts (lines 1-320)

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

<sub>⏱️ 1m 9s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\db\seed.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\db\seed.ts (lines 1-320)

<details>
<summary>170 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Database Seed Script
3. // ---------------------------------------------------------------------------
4. // Populates the database with demo data for development and testing.
5. // The seed data exercises edge cases: California loans, delegated users,
6. // finalized applications, and users without saved preferences.
7. //
8. // Run: npm run db:seed
9. // ---------------------------------------------------------------------------
10. 
11. import { getDb, closeDb } from "./connection.js";
12. 
13. export function seedDatabase(): void {
14.   const db = getDb();
15. 
16.   const insertUser = db.prepare(
17.     `INSERT OR IGNORE INTO users (id, role, name, email, phone) VALUES (?, ?, ?, ?, ?)`,
18.   );
19. 
20.   const insertApp = db.prepare(
21.     `INSERT OR IGNORE INTO loan_applications (id, borrower_name, amount, loan_state, status, assigned_underwriter, risk_score, created_at, updated_at)
22.      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
23.   );
24. 
25.   const insertPref = db.prepare(
26.     `INSERT OR IGNORE INTO notification_preferences (user_id, event, channel, enabled, updated_at, updated_by)
27.      VALUES (?, ?, ?, ?, ?, ?)`,
28.   );
29. 
30.   const insertDecision = db.prepare(
31.     `INSERT OR IGNORE INTO decisions (id, application_id, type, rationale, decided_by, decided_at, conditions)
32.      VALUES (?, ?, ?, ?, ?, ?, ?)`,
33.   );
34. 
35.   const insertAudit = db.prepare(
36.     `INSERT OR IGNORE INTO audit_entries (id, action, actor, delegated_for, timestamp, previous_value, new_value, source)
37.      VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
38.   );
39. 
40.   const seedAll = db.transaction(() => {
41.     // ── Users ──
42.     insertUser.run(
43.       "u-1",
44.       "underwriter",
45.       "Dana Chu",
46.       "dana.chu@loanworkbench.local",
47.       "+15551234001",
48.     );
49.     insertUser.run(
50.       "u-2",
51.       "analyst-manager",
52.       "Raj Patel",
53.       "raj.patel@loanworkbench.local",
54.       "+15551234002",
55.     );
56.     insertUser.run(
57.       "u-3",
58.       "compliance-reviewer",
59.       "Kim Nakamura",
60.       "kim.nakamura@loanworkbench.local",
61.       null,
62.     );
63. 
64.     // ── Loan Applications ──
65.     const now = new Date().toISOString();
66.     insertApp.run(
67.       "app-1",
68.       "Acme Corp",
69.       500000,
70.       "CA",
71.       "underwriting",
72.       "u-1",
73.       72.5,
74.       now,
75.       now,
76.     );
77.     insertApp.run(
78.       "app-2",
79.       "Beta LLC",
80.       150000,
81.       "NY",
82.       "intake",
83.       "u-1",
84.       null,
85.       now,
86.       now,
87.     );
88.     insertApp.run(
89.       "app-3",
90.       "Gamma Inc",
91.       2000000,
92.       "CA",
93.       "decision",
94.       "u-2",
95.       85.0,
96.       now,
97.       now,
98.     );
99.     insertApp.run(
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
151.       "aud-2",
152.       "decision.recorded",
153.       "u-2",
154.       null,
155.       now,
156.       null,
157.       JSON.stringify({ applicationId: "app-4", type: "approved" }),
158.       "seed-script",
159.     );
160.   });
161. 
162.   seedAll();
163.   console.log("✓ Database seeded with demo data.");
164. }
165. 
166. // Run directly: tsx backend/src/db/seed.ts
167. if (process.argv[1]?.endsWith("seed.ts")) {
168.   seedDatabase();
169.   closeDb();
170. }
```

</details>


---

<sub>⏱️ 1m 48s</sub>

### 💬 Copilot

I’ve got the conventions now: pure rule modules in `src/backend/src/rules`, structured outputs, and explicit Vitest cases in `tests/unit`. I’m wiring the new rule to the existing `getMandatoryEvents()` source of truth rather than inventing another mandatory-event list.

---

<sub>⏱️ 1m 48s</sub>

### ✅ `sql`

**Update todo statuses**

<details>
<summary>Arguments</summary>

```json
{
  "description": "Update todo statuses",
  "query": "UPDATE todos SET status = 'done' WHERE id = 'inspect-rule-surfaces'; UPDATE todos SET status = 'in_progress' WHERE id = 'implement-channel-rules'; UPDATE todos SET status = 'in_progress' WHERE id = 'add-rule-tests';"
}
```

</details>

<details>
<summary>7 lines</summary>

```
Executed 3 statement(s):

1. UPDATE
   1 row(s) updated.

2. UPDATE
   1 row(s) updated.

3. UPDATE
   1 row(s) updated.
```

</details>


---

<sub>⏱️ 1m 49s</sub>

### ✅ `store_memory`

<details>
<summary>Arguments</summary>

```json
{
  "subject": "mandatory events",
  "fact": "Mandatory notification events are defined in src/backend/src/rules/mandatory-events.ts via transition-keyed MANDATORY_EVENTS and getMandatoryEvents(from,to).",
  "citations": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\03-instruction-architecture\\src\\backend\\src\\rules\\mandatory-events.ts:12-36",
  "reason": "This is the source of truth future rule and service changes should reuse instead of creating duplicate mandatory-event lists. Remembering it helps prevent divergence across business rules, route validation, and tests.",
  "category": "general"
}
```

</details>

```
Memory stored successfully.
```


---

<sub>⏱️ 2m 12s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Add File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\03-instruction-architecture\\src\\backend\\src\\rules\\notification-channel-rules.ts\n+// ---------------------------------------------------------------------------\n+// Notification Channel Rules\n+// ---------------------------------------------------------------------------\n+// False positive:\n+//   Disabling SMS for a mandatory event is valid when another channel remains\n+//   enabled after the change. Mandatory delivery requires coverage, not every\n+//   channel to stay on.\n+//\n+// Hard negative:\n+//   Disabling the final enabled channel for a mandatory event looks like a\n+//   normal preference toggle, but it is forbidden because the event would lose\n+//   all delivery coverage. California decline SMS changes have an additional\n+//   LEGAL-218 fallback requirement.\n+// ---------------------------------------------------------------------------\n+\n+import {\n+  getMandatoryEvents,\n+  type MANDATORY_EVENTS,\n+} from \"./mandatory-events.js\";\n+import type {\n+  ApplicationState,\n+  NotificationChannel,\n+  NotificationEvent,\n+} from \"../models/types.js\";\n+\n+type RuleName = \"allowed\" | \"mandatory-event-coverage\" | \"ca-decline-sms-fallback\";\n+\n+export interface NotificationChannelPreferenceLike {\n+  channel: NotificationChannel;\n+  enabled: boolean;\n+}\n+\n+export interface ValidateNotificationChannelChangeInput {\n+  event: NotificationEvent;\n+  channel: NotificationChannel;\n+  enabled: boolean;\n+  currentPreferences: ReadonlyArray<NotificationChannelPreferenceLike>;\n+  loanState?: string;\n+  fromState?: ApplicationState;\n+  toState?: ApplicationState;\n+  mandatoryEvents?: ReadonlyArray<NotificationEvent>;\n+}\n+\n+export interface ChannelDisableResult {\n+  allowed: boolean;\n+  rule: RuleName;\n+  reason: string;\n+  ticket?: string;\n+}\n+\n+const CALIFORNIA_DECLINE_SMS_RESTRICTION = {\n+  rule: \"ca-decline-sms-fallback\",\n+  ticket: \"LEGAL-218\",\n+  reason:\n+    \"LEGAL-218: California decline notifications may disable SMS only when email remains enabled as a fallback.\",\n+} as const;\n+\n+function resolveMandatoryEvents(\n+  input: ValidateNotificationChannelChangeInput,\n+): ReadonlyArray<NotificationEvent> {\n+  if (input.mandatoryEvents) {\n+    return input.mandatoryEvents;\n+  }\n+\n+  if (input.fromState && input.toState) {\n+    return getMandatoryEvents(input.fromState, input.toState);\n+  }\n+\n+  return [];\n+}\n+\n+function buildPreferenceMap(\n+  currentPreferences: ReadonlyArray<NotificationChannelPreferenceLike>,\n+  channel: NotificationChannel,\n+  enabled: boolean,\n+): Record<NotificationChannel, boolean> {\n+  const nextState: Record<NotificationChannel, boolean> = {\n+    email: false,\n+    sms: false,\n+  };\n+\n+  for (const preference of currentPreferences) {\n+    nextState[preference.channel] = preference.enabled;\n+  }\n+\n+  nextState[channel] = enabled;\n+  return nextState;\n+}\n+\n+export function validateNotificationChannelChange(\n+  input: ValidateNotificationChannelChangeInput,\n+): ChannelDisableResult {\n+  if (input.enabled) {\n+    return {\n+      allowed: true,\n+      rule: \"allowed\",\n+      reason: \"Enabling a notification channel is always allowed.\",\n+    };\n+  }\n+\n+  const nextPreferences = buildPreferenceMap(\n+    input.currentPreferences,\n+    input.channel,\n+    input.enabled,\n+  );\n+  const mandatoryEvents = resolveMandatoryEvents(input);\n+  const eventIsMandatory = mandatoryEvents.includes(input.event);\n+  const normalizedLoanState = input.loanState?.toUpperCase();\n+\n+  if (\n+    normalizedLoanState === \"CA\" &&\n+    input.event === \"decline\" &&\n+    input.channel === \"sms\" &&\n+    !nextPreferences.email\n+  ) {\n+    return {\n+      allowed: false,\n+      rule: CALIFORNIA_DECLINE_SMS_RESTRICTION.rule,\n+      reason: CALIFORNIA_DECLINE_SMS_RESTRICTION.reason,\n+      ticket: CALIFORNIA_DECLINE_SMS_RESTRICTION.ticket,\n+    };\n+  }\n+\n+  if (eventIsMandatory && !nextPreferences.email && !nextPreferences.sms) {\n+    return {\n+      allowed: false,\n+      rule: \"mandatory-event-coverage\",\n+      reason: `Mandatory event '${input.event}' must keep at least one notification channel enabled.`,\n+    };\n+  }\n+\n+  return {\n+    allowed: true,\n+    rule: \"allowed\",\n+    reason: `Channel change allowed for '${input.event}'.`,\n+  };\n+}\n*** Add File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\03-instruction-architecture\\src\\backend\\tests\\unit\\notification-channel-rules.test.ts\n+import { describe, expect, it } from \"vitest\";\n+import type { NotificationChannel } from \"../../src/models/types.js\";\n+import { validateNotificationChannelChange } from \"../../src/rules/notification-channel-rules.js\";\n+\n+function preference(channel: NotificationChannel, enabled: boolean) {\n+  return { channel, enabled };\n+}\n+\n+describe(\"notification channel rules\", () => {\n+  it(\"allows enabling a channel for a mandatory event\", () => {\n+    // Happy path: turning a channel on is always safe, even for mandatory events.\n+    const result = validateNotificationChannelChange({\n+      event: \"approval\",\n+      channel: \"sms\",\n+      enabled: true,\n+      currentPreferences: [preference(\"email\", false), preference(\"sms\", false)],\n+      fromState: \"decision\",\n+      toState: \"finalized\",\n+    });\n+\n+    expect(result).toEqual({\n+      allowed: true,\n+      rule: \"allowed\",\n+      reason: \"Enabling a notification channel is always allowed.\",\n+    });\n+  });\n+\n+  it(\"blocks disabling the last enabled channel for a mandatory event\", () => {\n+    // Boundary case: this change removes the exact last remaining delivery path.\n+    const result = validateNotificationChannelChange({\n+      event: \"approval\",\n+      channel: \"email\",\n+      enabled: false,\n+      currentPreferences: [preference(\"email\", true), preference(\"sms\", false)],\n+      fromState: \"decision\",\n+      toState: \"finalized\",\n+    });\n+\n+    expect(result.allowed).toBe(false);\n+    expect(result.rule).toBe(\"mandatory-event-coverage\");\n+    expect(result.reason).toBe(\n+      \"Mandatory event 'approval' must keep at least one notification channel enabled.\",\n+    );\n+  });\n+\n+  it(\"allows disabling sms for a mandatory event when email remains enabled\", () => {\n+    // False positive: disabling one channel still preserves mandatory coverage.\n+    const result = validateNotificationChannelChange({\n+      event: \"approval\",\n+      channel: \"sms\",\n+      enabled: false,\n+      currentPreferences: [preference(\"email\", true), preference(\"sms\", true)],\n+      fromState: \"decision\",\n+      toState: \"finalized\",\n+    });\n+\n+    expect(result).toEqual({\n+      allowed: true,\n+      rule: \"allowed\",\n+      reason: \"Channel change allowed for 'approval'.\",\n+    });\n+  });\n+\n+  it(\"blocks disabling sms for california decline notifications without email fallback\", () => {\n+    // Hard negative: it looks like a normal SMS toggle, but LEGAL-218 forbids it.\n+    const result = validateNotificationChannelChange({\n+      event: \"decline\",\n+      channel: \"sms\",\n+      enabled: false,\n+      currentPreferences: [preference(\"email\", false), preference(\"sms\", true)],\n+      loanState: \"ca\",\n+    });\n+\n+    expect(result.allowed).toBe(false);\n+    expect(result.rule).toBe(\"ca-decline-sms-fallback\");\n+    expect(result.ticket).toBe(\"LEGAL-218\");\n+    expect(result.reason).toBe(\n+      \"LEGAL-218: California decline notifications may disable SMS only when email remains enabled as a fallback.\",\n+    );\n+  });\n+});\n*** End Patch\n"
```

</details>

```
Added 2 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\rules\notification-channel-rules.ts, Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\tests\unit\notification-channel-rules.test.ts
```


---

<sub>⏱️ 2m 17s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\rules\notification-channel-rules.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\rules\notification-channel-rules.ts (lines 1-260)

<details>
<summary>137 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Notification Channel Rules
3. // ---------------------------------------------------------------------------
4. // False positive:
5. //   Disabling SMS for a mandatory event is valid when another channel remains
6. //   enabled after the change. Mandatory delivery requires coverage, not every
7. //   channel to stay on.
8. //
9. // Hard negative:
10. //   Disabling the final enabled channel for a mandatory event looks like a
11. //   normal preference toggle, but it is forbidden because the event would lose
12. //   all delivery coverage. California decline SMS changes have an additional
13. //   LEGAL-218 fallback requirement.
14. // ---------------------------------------------------------------------------
15. 
16. import {
17.   getMandatoryEvents,
18.   type MANDATORY_EVENTS,
19. } from "./mandatory-events.js";
20. import type {
21.   ApplicationState,
22.   NotificationChannel,
23.   NotificationEvent,
24. } from "../models/types.js";
25. 
26. type RuleName = "allowed" | "mandatory-event-coverage" | "ca-decline-sms-fallback";
27. 
28. export interface NotificationChannelPreferenceLike {
29.   channel: NotificationChannel;
30.   enabled: boolean;
31. }
32. 
33. export interface ValidateNotificationChannelChangeInput {
34.   event: NotificationEvent;
35.   channel: NotificationChannel;
36.   enabled: boolean;
37.   currentPreferences: ReadonlyArray<NotificationChannelPreferenceLike>;
38.   loanState?: string;
39.   fromState?: ApplicationState;
40.   toState?: ApplicationState;
41.   mandatoryEvents?: ReadonlyArray<NotificationEvent>;
42. }
43. 
44. export interface ChannelDisableResult {
45.   allowed: boolean;
46.   rule: RuleName;
47.   reason: string;
48.   ticket?: string;
49. }
50. 
51. const CALIFORNIA_DECLINE_SMS_RESTRICTION = {
52.   rule: "ca-decline-sms-fallback",
53.   ticket: "LEGAL-218",
54.   reason:
55.     "LEGAL-218: California decline notifications may disable SMS only when email remains enabled as a fallback.",
56. } as const;
57. 
58. function resolveMandatoryEvents(
59.   input: ValidateNotificationChannelChangeInput,
60. ): ReadonlyArray<NotificationEvent> {
61.   if (input.mandatoryEvents) {
62.     return input.mandatoryEvents;
63.   }
64. 
65.   if (input.fromState && input.toState) {
66.     return getMandatoryEvents(input.fromState, input.toState);
67.   }
68. 
69.   return [];
70. }
71. 
72. function buildPreferenceMap(
73.   currentPreferences: ReadonlyArray<NotificationChannelPreferenceLike>,
74.   channel: NotificationChannel,
75.   enabled: boolean,
76. ): Record<NotificationChannel, boolean> {
77.   const nextState: Record<NotificationChannel, boolean> = {
78.     email: false,
79.     sms: false,
80.   };
81. 
82.   for (const preference of currentPreferences) {
83.     nextState[preference.channel] = preference.enabled;
84.   }
85. 
86.   nextState[channel] = enabled;
87.   return nextState;
88. }
89. 
90. export function validateNotificationChannelChange(
91.   input: ValidateNotificationChannelChangeInput,
92. ): ChannelDisableResult {
93.   if (input.enabled) {
94.     return {
95.       allowed: true,
96.       rule: "allowed",
97.       reason: "Enabling a notification channel is always allowed.",
98.     };
99.   }
100. 
101.   const nextPreferences = buildPreferenceMap(
102.     input.currentPreferences,
103.     input.channel,
104.     input.enabled,
105.   );
106.   const mandatoryEvents = resolveMandatoryEvents(input);
107.   const eventIsMandatory = mandatoryEvents.includes(input.event);
108.   const normalizedLoanState = input.loanState?.toUpperCase();
109. 
110.   if (
111.     normalizedLoanState === "CA" &&
112.     input.event === "decline" &&
113.     input.channel === "sms" &&
114.     !nextPreferences.email
115.   ) {
116.     return {
117.       allowed: false,
118.       rule: CALIFORNIA_DECLINE_SMS_RESTRICTION.rule,
119.       reason: CALIFORNIA_DECLINE_SMS_RESTRICTION.reason,
120.       ticket: CALIFORNIA_DECLINE_SMS_RESTRICTION.ticket,
121.     };
122.   }
123. 
124.   if (eventIsMandatory && !nextPreferences.email && !nextPreferences.sms) {
125.     return {
126.       allowed: false,
127.       rule: "mandatory-event-coverage",
128.       reason: `Mandatory event '${input.event}' must keep at least one notification channel enabled.`,
129.     };
130.   }
131. 
132.   return {
133.     allowed: true,
134.     rule: "allowed",
135.     reason: `Channel change allowed for '${input.event}'.`,
136.   };
137. }
```

</details>


---

<sub>⏱️ 2m 17s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\tests\unit\notification-channel-rules.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\tests\unit\notification-channel-rules.test.ts (lines 1-260)

<details>
<summary>81 lines</summary>

```
1. import { describe, expect, it } from "vitest";
2. import type { NotificationChannel } from "../../src/models/types.js";
3. import { validateNotificationChannelChange } from "../../src/rules/notification-channel-rules.js";
4. 
5. function preference(channel: NotificationChannel, enabled: boolean) {
6.   return { channel, enabled };
7. }
8. 
9. describe("notification channel rules", () => {
10.   it("allows enabling a channel for a mandatory event", () => {
11.     // Happy path: turning a channel on is always safe, even for mandatory events.
12.     const result = validateNotificationChannelChange({
13.       event: "approval",
14.       channel: "sms",
15.       enabled: true,
16.       currentPreferences: [preference("email", false), preference("sms", false)],
17.       fromState: "decision",
18.       toState: "finalized",
19.     });
20. 
21.     expect(result).toEqual({
22.       allowed: true,
23.       rule: "allowed",
24.       reason: "Enabling a notification channel is always allowed.",
25.     });
26.   });
27. 
28.   it("blocks disabling the last enabled channel for a mandatory event", () => {
29.     // Boundary case: this change removes the exact last remaining delivery path.
30.     const result = validateNotificationChannelChange({
31.       event: "approval",
32.       channel: "email",
33.       enabled: false,
34.       currentPreferences: [preference("email", true), preference("sms", false)],
35.       fromState: "decision",
36.       toState: "finalized",
37.     });
38. 
39.     expect(result.allowed).toBe(false);
40.     expect(result.rule).toBe("mandatory-event-coverage");
41.     expect(result.reason).toBe(
42.       "Mandatory event 'approval' must keep at least one notification channel enabled.",
43.     );
44.   });
45. 
46.   it("allows disabling sms for a mandatory event when email remains enabled", () => {
47.     // False positive: disabling one channel still preserves mandatory coverage.
48.     const result = validateNotificationChannelChange({
49.       event: "approval",
50.       channel: "sms",
51.       enabled: false,
52.       currentPreferences: [preference("email", true), preference("sms", true)],
53.       fromState: "decision",
54.       toState: "finalized",
55.     });
56. 
57.     expect(result).toEqual({
58.       allowed: true,
59.       rule: "allowed",
60.       reason: "Channel change allowed for 'approval'.",
61.     });
62.   });
63. 
64.   it("blocks disabling sms for california decline notifications without email fallback", () => {
65.     // Hard negative: it looks like a normal SMS toggle, but LEGAL-218 forbids it.
66.     const result = validateNotificationChannelChange({
67.       event: "decline",
68.       channel: "sms",
69.       enabled: false,
70.       currentPreferences: [preference("email", false), preference("sms", true)],
71.       loanState: "ca",
72.     });
73. 
74.     expect(result.allowed).toBe(false);
75.     expect(result.rule).toBe("ca-decline-sms-fallback");
76.     expect(result.ticket).toBe("LEGAL-218");
77.     expect(result.reason).toBe(
78.       "LEGAL-218: California decline notifications may disable SMS only when email remains enabled as a fallback.",
79.     );
80.   });
81. });
```

</details>


---

<sub>⏱️ 2m 28s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Update File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\03-instruction-architecture\\src\\backend\\src\\rules\\notification-channel-rules.ts\n@@\n-import {\n-  getMandatoryEvents,\n-  type MANDATORY_EVENTS,\n-} from \"./mandatory-events.js\";\n+import { getMandatoryEvents } from \"./mandatory-events.js\";\n@@\n-type RuleName = \"allowed\" | \"mandatory-event-coverage\" | \"ca-decline-sms-fallback\";\n+type RuleName =\n+  | \"allowed\"\n+  | \"mandatory-event-coverage\"\n+  | \"ca-decline-sms-fallback\";\n*** End Patch\n"
```

</details>

```
Modified 1 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\rules\notification-channel-rules.ts
```


---

<sub>⏱️ 2m 33s</sub>

### 💬 Copilot

The core logic is in place now. I’m doing a final file-level review for type-safety and convention alignment since I’m not allowed to run the test suite or shell commands here.

---

<sub>⏱️ 2m 33s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\rules\notification-channel-rules.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\src\rules\notification-channel-rules.ts (lines 1-260)

<details>
<summary>137 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Notification Channel Rules
3. // ---------------------------------------------------------------------------
4. // False positive:
5. //   Disabling SMS for a mandatory event is valid when another channel remains
6. //   enabled after the change. Mandatory delivery requires coverage, not every
7. //   channel to stay on.
8. //
9. // Hard negative:
10. //   Disabling the final enabled channel for a mandatory event looks like a
11. //   normal preference toggle, but it is forbidden because the event would lose
12. //   all delivery coverage. California decline SMS changes have an additional
13. //   LEGAL-218 fallback requirement.
14. // ---------------------------------------------------------------------------
15. 
16. import { getMandatoryEvents } from "./mandatory-events.js";
17. import type {
18.   ApplicationState,
19.   NotificationChannel,
20.   NotificationEvent,
21. } from "../models/types.js";
22. 
23. type RuleName =
24.   | "allowed"
25.   | "mandatory-event-coverage"
26.   | "ca-decline-sms-fallback";
27. 
28. export interface NotificationChannelPreferenceLike {
29.   channel: NotificationChannel;
30.   enabled: boolean;
31. }
32. 
33. export interface ValidateNotificationChannelChangeInput {
34.   event: NotificationEvent;
35.   channel: NotificationChannel;
36.   enabled: boolean;
37.   currentPreferences: ReadonlyArray<NotificationChannelPreferenceLike>;
38.   loanState?: string;
39.   fromState?: ApplicationState;
40.   toState?: ApplicationState;
41.   mandatoryEvents?: ReadonlyArray<NotificationEvent>;
42. }
43. 
44. export interface ChannelDisableResult {
45.   allowed: boolean;
46.   rule: RuleName;
47.   reason: string;
48.   ticket?: string;
49. }
50. 
51. const CALIFORNIA_DECLINE_SMS_RESTRICTION = {
52.   rule: "ca-decline-sms-fallback",
53.   ticket: "LEGAL-218",
54.   reason:
55.     "LEGAL-218: California decline notifications may disable SMS only when email remains enabled as a fallback.",
56. } as const;
57. 
58. function resolveMandatoryEvents(
59.   input: ValidateNotificationChannelChangeInput,
60. ): ReadonlyArray<NotificationEvent> {
61.   if (input.mandatoryEvents) {
62.     return input.mandatoryEvents;
63.   }
64. 
65.   if (input.fromState && input.toState) {
66.     return getMandatoryEvents(input.fromState, input.toState);
67.   }
68. 
69.   return [];
70. }
71. 
72. function buildPreferenceMap(
73.   currentPreferences: ReadonlyArray<NotificationChannelPreferenceLike>,
74.   channel: NotificationChannel,
75.   enabled: boolean,
76. ): Record<NotificationChannel, boolean> {
77.   const nextState: Record<NotificationChannel, boolean> = {
78.     email: false,
79.     sms: false,
80.   };
81. 
82.   for (const preference of currentPreferences) {
83.     nextState[preference.channel] = preference.enabled;
84.   }
85. 
86.   nextState[channel] = enabled;
87.   return nextState;
88. }
89. 
90. export function validateNotificationChannelChange(
91.   input: ValidateNotificationChannelChangeInput,
92. ): ChannelDisableResult {
93.   if (input.enabled) {
94.     return {
95.       allowed: true,
96.       rule: "allowed",
97.       reason: "Enabling a notification channel is always allowed.",
98.     };
99.   }
100. 
101.   const nextPreferences = buildPreferenceMap(
102.     input.currentPreferences,
103.     input.channel,
104.     input.enabled,
105.   );
106.   const mandatoryEvents = resolveMandatoryEvents(input);
107.   const eventIsMandatory = mandatoryEvents.includes(input.event);
108.   const normalizedLoanState = input.loanState?.toUpperCase();
109. 
110.   if (
111.     normalizedLoanState === "CA" &&
112.     input.event === "decline" &&
113.     input.channel === "sms" &&
114.     !nextPreferences.email
115.   ) {
116.     return {
117.       allowed: false,
118.       rule: CALIFORNIA_DECLINE_SMS_RESTRICTION.rule,
119.       reason: CALIFORNIA_DECLINE_SMS_RESTRICTION.reason,
120.       ticket: CALIFORNIA_DECLINE_SMS_RESTRICTION.ticket,
121.     };
122.   }
123. 
124.   if (eventIsMandatory && !nextPreferences.email && !nextPreferences.sms) {
125.     return {
126.       allowed: false,
127.       rule: "mandatory-event-coverage",
128.       reason: `Mandatory event '${input.event}' must keep at least one notification channel enabled.`,
129.     };
130.   }
131. 
132.   return {
133.     allowed: true,
134.     rule: "allowed",
135.     reason: `Channel change allowed for '${input.event}'.`,
136.   };
137. }
```

</details>


---

<sub>⏱️ 2m 33s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\tests\unit\notification-channel-rules.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\src\backend\tests\unit\notification-channel-rules.test.ts (lines 1-260)

<details>
<summary>81 lines</summary>

```
1. import { describe, expect, it } from "vitest";
2. import type { NotificationChannel } from "../../src/models/types.js";
3. import { validateNotificationChannelChange } from "../../src/rules/notification-channel-rules.js";
4. 
5. function preference(channel: NotificationChannel, enabled: boolean) {
6.   return { channel, enabled };
7. }
8. 
9. describe("notification channel rules", () => {
10.   it("allows enabling a channel for a mandatory event", () => {
11.     // Happy path: turning a channel on is always safe, even for mandatory events.
12.     const result = validateNotificationChannelChange({
13.       event: "approval",
14.       channel: "sms",
15.       enabled: true,
16.       currentPreferences: [preference("email", false), preference("sms", false)],
17.       fromState: "decision",
18.       toState: "finalized",
19.     });
20. 
21.     expect(result).toEqual({
22.       allowed: true,
23.       rule: "allowed",
24.       reason: "Enabling a notification channel is always allowed.",
25.     });
26.   });
27. 
28.   it("blocks disabling the last enabled channel for a mandatory event", () => {
29.     // Boundary case: this change removes the exact last remaining delivery path.
30.     const result = validateNotificationChannelChange({
31.       event: "approval",
32.       channel: "email",
33.       enabled: false,
34.       currentPreferences: [preference("email", true), preference("sms", false)],
35.       fromState: "decision",
36.       toState: "finalized",
37.     });
38. 
39.     expect(result.allowed).toBe(false);
40.     expect(result.rule).toBe("mandatory-event-coverage");
41.     expect(result.reason).toBe(
42.       "Mandatory event 'approval' must keep at least one notification channel enabled.",
43.     );
44.   });
45. 
46.   it("allows disabling sms for a mandatory event when email remains enabled", () => {
47.     // False positive: disabling one channel still preserves mandatory coverage.
48.     const result = validateNotificationChannelChange({
49.       event: "approval",
50.       channel: "sms",
51.       enabled: false,
52.       currentPreferences: [preference("email", true), preference("sms", true)],
53.       fromState: "decision",
54.       toState: "finalized",
55.     });
56. 
57.     expect(result).toEqual({
58.       allowed: true,
59.       rule: "allowed",
60.       reason: "Channel change allowed for 'approval'.",
61.     });
62.   });
63. 
64.   it("blocks disabling sms for california decline notifications without email fallback", () => {
65.     // Hard negative: it looks like a normal SMS toggle, but LEGAL-218 forbids it.
66.     const result = validateNotificationChannelChange({
67.       event: "decline",
68.       channel: "sms",
69.       enabled: false,
70.       currentPreferences: [preference("email", false), preference("sms", true)],
71.       loanState: "ca",
72.     });
73. 
74.     expect(result.allowed).toBe(false);
75.     expect(result.rule).toBe("ca-decline-sms-fallback");
76.     expect(result.ticket).toBe("LEGAL-218");
77.     expect(result.reason).toBe(
78.       "LEGAL-218: California decline notifications may disable SMS only when email remains enabled as a fallback.",
79.     );
80.   });
81. });
```

</details>


---

<sub>⏱️ 2m 33s</sub>

### ✅ `sql`

**Complete todos**

<details>
<summary>Arguments</summary>

```json
{
  "description": "Complete todos",
  "query": "UPDATE todos SET status = 'done' WHERE id = 'implement-channel-rules'; UPDATE todos SET status = 'done' WHERE id = 'add-rule-tests'; UPDATE todos SET status = 'done' WHERE id = 'verify-edits'; SELECT id, status FROM todos ORDER BY id;"
}
```

</details>

<details>
<summary>15 lines</summary>

```
Executed 4 statement(s):

1. UPDATE
   1 row(s) updated.

2. UPDATE
   1 row(s) updated.

3. UPDATE
   1 row(s) updated.

4. SELECT
   4 row(s) returned:
   
   | id | status |
   | --- | --- |
   | add-rule-tests | done |
   | implement-channel-rules | done |
   | inspect-rule-surfaces | done |
   | verify-edits | done |
```

</details>


---

<sub>⏱️ 2m 41s</sub>

### 💬 Copilot

Added the new pure rule module at `src/backend/src/rules/notification-channel-rules.ts` and matching tests at `src/backend/tests/unit/notification-channel-rules.test.ts`.

The rule reuses the discovered mandatory-event source of truth via `getMandatoryEvents()` from `mandatory-events.ts`, returns structured results with human-readable reasons, documents false-positive and hard-negative cases at the top of the module, blocks disabling the last channel for mandatory events, and enforces the California decline SMS fallback rule with `LEGAL-218` in both metadata and reason text.

Tests cover happy path, boundary, false positive, and hard negative cases.

I did not run shell commands, per your instruction.

---

<sub>Generated by [GitHub Copilot CLI](https://github.com/features/copilot/cli)</sub>
