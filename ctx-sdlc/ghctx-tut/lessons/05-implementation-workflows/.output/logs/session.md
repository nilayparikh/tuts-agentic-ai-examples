# 🤖 Copilot CLI Session

> [!NOTE]
> - **Session ID:** `7858bbe2-fd0b-4e1c-9839-68962fc30407`  
> - **Started:** 16/04/2026, 12:53:58  
> - **Duration:** 6m 4s  
> - **Exported:** 16/04/2026, 13:00:03  

---

<sub>⏱️ 5s</sub>

### 👤 User

Inspect docs/, specs/, and the relevant notification-preference write surfaces you discover in this lesson before editing. Use the playbook and example doc as success criteria, not as a fixed file checklist. Implement a focused notification-preference write hardening slice. Write tests first at src/backend/tests/unit/notification-preference-write-rules.test.ts, then add a pure rule module at src/backend/src/rules/notification-preference-write-rules.ts, and wire the minimal production changes into src/backend/src/routes/notifications.ts. In the final handoff, state which behaviors the tests should fail on before the production change and which should pass after it, and name any intentionally deferred write surfaces that remain out of scope. The rule must use explicit inputs plus existing types, not direct DB access. Enforce these cases: manual-review-escalation must keep at least one channel enabled; decline SMS cannot be enabled when loanState is CA or California under LEGAL-218; treat loanState as the direct request input for this route instead of introducing a new loanId lookup or any repository fetch; the false positive where escalation SMS is disabled but escalation email stays enabled must remain allowed. When tests assert business-rule rejections, prefer semantic checks over brittle exact wording, and preserve the current route rejection style when practical; if the route returns 400 or 422 for these rule violations, the payload must still clearly express the business invariant. Preserve delegated-session and role guards, keep changes minimal, keep the scope to the current notification write path, include top-of-module false-positive and hard-negative comments in the new rule file, and do not edit protected config or database files. Do not run npm install, npm test, npx vitest, or any shell commands. Do not use SQL or task/todo write tools. Inspect and edit files only. Return a short handoff summary naming changed files and which tests should pass.

---

<sub>⏱️ 12s</sub>

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

<sub>⏱️ 30s</sub>

### 💬 Copilot

I’m inspecting the lesson docs/specs and the current notification write path first so the tests match the intended invariants before I wire the minimal route change.

---

<sub>⏱️ 30s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows**

"docs\**\*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows

```
No files matched the pattern.
```


---

<sub>⏱️ 30s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows**

"specs\**\*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows

```
No files matched the pattern.
```


---

<sub>⏱️ 30s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "notification-preference|notification preference|LEGAL-218|manual-review-escalation|playbook|example",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows",
  "output_mode": "files_with_matches",
  "head_limit": 100
}
```

</details>

<details>
<summary>25 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\.github\skills\tdd-workflow\SKILL.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-playbook.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\.github\agents\implementer.agent.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\.github\prompts\implement-feature.prompt.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\ASSESSMENT.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\.github\prompts\review-changes.prompt.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\architecture.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\.github\agents\tester.agent.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-workflow-example.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\.output\change\expected-files.json
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\.output\change\expected-patterns.json
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\.github\agents\reviewer.agent.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\.output\logs\command.txt
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\HANDOFF.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\.output\logs\process-1776340437106-22152.log
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\util.py
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\HANDOFF_IMPLEMENTATION.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\RUN.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\product-spec-notification-preferences.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\tests\test_ui.py
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\README.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\.output\logs\prompt.txt
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\VERIFICATION.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\.output\logs\runner.log
```

</details>


---

<sub>⏱️ 30s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\product-spec-notification-preferences.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\product-spec-notification-preferences.md

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

<sub>⏱️ 30s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\non-functional-requirements.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\non-functional-requirements.md

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

<sub>⏱️ 30s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts

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

<sub>⏱️ 30s</sub>

### ❌ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts

```
Path does not exist
```


---

<sub>⏱️ 30s</sub>

### ❌ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\notification-channel-rules.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\notification-channel-rules.ts

```
Path does not exist
```


---

<sub>⏱️ 30s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\mandatory-events.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\mandatory-events.ts

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

<sub>⏱️ 44s</sub>

### 💬 Copilot

I found the playbook/example docs and the current route surface. Next I’m reading the lesson guidance plus nearby tests/types so the new rule module matches existing patterns and keeps scope to the single write path.

---

<sub>⏱️ 44s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-playbook.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-playbook.md

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

<sub>⏱️ 44s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-workflow-example.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-workflow-example.md

<details>
<summary>100 lines</summary>

```
1. # Lesson 05 — Implementation Workflow Example
2. 
3. This document defines the concrete example used in Lesson 05.
4. 
5. ## Prerequisite Context
6. 
7. This lesson consumes `docs/notification-preferences-plan.md`, the structured
8. implementation plan produced by the Lesson 04 planning workflow. The plan maps
9. out all backend, frontend, audit, and observability surfaces for the full
10. notification-preferences feature. Lesson 05 implements only **one focused slice**
11. of that plan — hardening the notification-preference write path.
12. 
13. ## Objective
14. 
15. Show that a constrained implementation workflow can make a focused production change with matching tests instead of attempting the entire notification-preferences feature at once.
16. 
17. ## Expected Change Shape
18. 
19. The preferred output for this lesson is a small change set with:
20. 
21. 1. One new pure rule module under `src/backend/src/rules/`
22. 2. One matching unit test file under `src/backend/tests/unit/`
23. 3. One targeted wiring change to `src/backend/src/routes/notifications.ts`
24. 4. No edits to protected config or database files
25. 
26. ## Required Constraints
27. 
28. 1. The workflow must implement code, not only describe it.
29. 2. The new rule must use explicit inputs and existing domain types instead of direct database access.
30. 3. The change must preserve delegated-session and role guards already present in the route.
31. 4. The implementation must cover a mandatory-event rule and the California `LEGAL-218` restriction.
32. 5. The implementation must call out at least one false positive and one hard negative in the new rule module comments.
33. 6. The run must not execute shell commands.
34. 7. The run must not edit protected files such as feature flags, schema, or seed data.
35. 8. The run must not use SQL or task/todo write tools.
36. 9. The final handoff should explain the expected red/green test behavior and name any deferred follow-up surfaces that remain intentionally out of scope.
37. 10. The workflow should discover the current notification-preference write surfaces before editing and make the chosen slice boundary explicit.
38. 11. The write path must keep `loanState` as the direct request input for this route. Do not replace it with a new `loanId` lookup contract.
39. 12. The lesson is not complete until `python util.py --test` passes after the demo or manual implementation.
40. 
41. ## Concrete Scenario
42. 
43. Harden notification preference writes so the existing route cannot:
44. 
45. - disable the last available channel for `manual-review-escalation`
46. - enable decline SMS for California loan context
47. 
48. Good output should keep the change local and avoid sprawling refactors.
49. 
50. It should also make the intentional scope boundary visible: this lesson is about hardening the current notification write path, not implementing every preference mutation surface in the repository at once.
51. 
52. Good output should explicitly name the deferred write surfaces in the handoff instead of silently implying that the whole notification-preferences domain is now complete.
53. 
54. ## What Good Output Looks Like
55. 
56. Good output will usually:
57. 
58. - create a pure rule file and a matching unit test file
59. - wire the route to call the rule rather than embedding the full policy inline
60. - preserve existing delegated-session and permission checks
61. - keep the route contract direct and explicit by passing `loanState` into the rule instead of adding loan repository lookups
62. - cite or encode the false-positive case where escalation SMS is disabled but escalation email remains enabled
63. - encode the hard-negative case where all escalation channels end up disabled
64. - explain which test cases would fail before the production change and which should pass after it
65. - survive the end-to-end `python util.py --test` gate after the code change is produced
66. 
67. ## Test Authoring Quality Bar
68. 
69. Generated tests must be durable across semantically equivalent implementations.
70. That matters in this lesson because `python util.py --demo` recreates `src/` from
71. the app baseline before each run, so any test fix that lives only in generated
72. source will be lost on the next demo.
73. 
74. When a rule returns a human-readable reason string:
75. 
76. - assert the invariant, not one exact sentence or capitalization pattern
77. - normalize text before matching, such as lowercasing the reason
78. - prefer checking stable business terms like `manual-review-escalation`,
79.   `at least one`, or `LEGAL-218`
80. - avoid brittle exact-string checks for explanatory prose unless the exact text
81.   is part of the contract
82. 
83. For this lesson, the mandatory-event tests should prove that the rejection
84. mentions the escalation invariant and the "at least one channel" rule, even if
85. the final sentence shape differs.
86. 
87. The `LEGAL-218` checks may assert the literal token `LEGAL-218`, because that
88. identifier is a stable contract signal rather than free-form wording.
89. 
90. When the current route rejects a business-rule violation, stable semantics matter
91. more than one exact HTTP code. In this lesson, a semantically equivalent
92. implementation may surface the rejection as `400` or `422` while still returning
93. the correct business explanation. Unless the lesson is explicitly about HTTP
94. status design, tests should accept either status for these rule rejections and
95. assert the business invariant from the payload.
96. 
97. If the implementation can preserve the route's existing rejection style without
98. extra complexity, prefer `400` for this lesson so the API remains aligned with
99. the rest of the simple validation surfaces.
100.
```

</details>


---

<sub>⏱️ 44s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md

```
File too large to read at once (40.3 KB). Consider using the grep tool to search within the file, or view with view_range to read specific sections.
```


---

<sub>⏱️ 44s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\types.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\types.ts

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

<sub>⏱️ 44s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts

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

<sub>⏱️ 44s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "describe\\(|LEGAL-218|manual-review-escalation|notificationRoutes|preference.updated|canDisableChannel|RuleViolation|allowed: false|reason:",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows\\src\\backend",
  "output_mode": "files_with_matches",
  "glob": "**/*.{ts,tsx}",
  "head_limit": 200
}
```

</details>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\notification-service.test.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\integration\decisions.test.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\integration\applications.test.ts
```


---

<sub>⏱️ 44s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows**

"src\backend\tests\unit\*.ts" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows

```
No files matched the pattern.
```


---

<sub>⏱️ 44s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\business-rules.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\business-rules.ts

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

<sub>⏱️ 53s</sub>

### 💬 Copilot

The repo doesn’t already have a notification-preference unit test file, so I’m reading the nearby test style and app wiring before I add the red tests.

---

<sub>⏱️ 53s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts

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

<sub>⏱️ 53s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\notification-service.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\notification-service.test.ts

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

<sub>⏱️ 53s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\integration\applications.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\integration\applications.test.ts

<details>
<summary>24 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Application Routes Integration Tests
3. // ---------------------------------------------------------------------------
4. 
5. import { describe, it, expect } from "vitest";
6. 
7. // Integration tests require a running database and Express app.
8. // These serve as contract documentation for the API.
9. 
10. describe("Application Routes (integration)", () => {
11.   it("placeholder — GET /api/applications returns 200", () => {
12.     // To run: set up test DB, import app, use supertest
13.     expect(true).toBe(true);
14.   });
15. 
16.   it("placeholder — POST /api/applications validates required fields", () => {
17.     expect(true).toBe(true);
18.   });
19. 
20.   it("placeholder — PATCH /api/applications/:id/status enforces state machine", () => {
21.     expect(true).toBe(true);
22.   });
23. });
24.
```

</details>


---

<sub>⏱️ 53s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "notificationRoutes|express\\(|supertest|request\\(|app =|export const app|createApp|routes",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows\\src\\backend",
  "output_mode": "content",
  "glob": "**/*.{ts,tsx}",
  "-n": true,
  "head_limit": 200
}
```

</details>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\integration\applications.test.ts:12:    // To run: set up test DB, import app, use supertest
```


---

<sub>⏱️ 53s</sub>

### ❌ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\package.json.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\package.json

```
Path does not exist
```


---

<sub>⏱️ 1m 8s</sub>

### 💬 Copilot

I’ve confirmed the existing tests are lightweight unit-style files, so I’m reading the notification middleware/route dependencies now to decide the smallest durable route-level assertions to include in the new test file.

---

<sub>⏱️ 1m 8s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\middleware\auth.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\middleware\auth.ts

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

<sub>⏱️ 1m 8s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\middleware\request-validator.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\middleware\request-validator.ts

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

<sub>⏱️ 1m 8s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\role-permissions.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\role-permissions.ts

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

<sub>⏱️ 1m 8s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "auditAction\\(|export function auditAction|export const auditAction|findPreference\\(|setPreference\\(|findPreferencesForUser\\(",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows\\src\\backend\\src",
  "output_mode": "files_with_matches",
  "glob": "**/*.ts",
  "head_limit": 50
}
```

</details>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\services\audit-service.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\queue\handlers\notification-handler.ts
```


---

<sub>⏱️ 1m 8s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\services\audit-service.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\services\audit-service.ts

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

<sub>⏱️ 1m 16s</sub>

### 💬 Copilot

I’ve got enough of the coding conventions now; I’m checking the plan for the intended slice boundary so the handoff can explicitly name which other preference-write surfaces stay deferred.

---

<sub>⏱️ 1m 16s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "notification preferences|write path|preferences/:userId/email|preferences/:userId/sms|surface|route|manual-review-escalation|LEGAL-218|loanState",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows\\docs\\notification-preferences-plan.md",
  "output_mode": "content",
  "-n": true,
  "head_limit": 200
}
```

</details>

<details>
<summary>43 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:12:This plan outlines the implementation of user-configurable notification preferences for the Loan Workbench platform. The feature addresses alert fatigue by allowing underwriters and analyst managers to control which notifications they receive (approval, decline, document-request, manual-review-escalation) across email and SMS channels.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:15:- Mandatory notification events (manual-review-escalation) must always have at least one enabled channel.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:16:- California loans have a temporary SMS restriction for decline notifications (LEGAL-218).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:33:| FR2 | Mandatory event rule: ≥1 channel for manual-review-escalation | product-spec-notification-preferences.md § FR-2 (explicit hard negative pattern) |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:35:| FR4 | California SMS restriction for decline (LEGAL-218)          | product-spec-notification-preferences.md § FR-4 (explicit: loan_state based) |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:67:| AR5 | Message contracts in queue/contracts.ts are breaking-change surface | docs/architecture.md § Key Architectural Rules § #7 |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:76:   - **Implication for Plan**: Affects frontend routing and component composition. Current routes/audit.ts exists but may need expansion.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:100:   - **Choice**: Implement `canDisableChannel(loanState, event, channel, userId) => ChannelDisableRule` as pure function in `src/backend/src/rules/notification-channel-rules.ts`.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:104:   - **Inference**: SC-2 delegated read-only pattern + existing route structure (notifications.ts).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:109:   - **Inference**: FR-3 "no migration required" + architecture rule (AR3 "routes orchestrate").
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:119:   - **Inference**: NFR-5 observability requirement + route error handling.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:135:   - Users may not disable all channels for `manual-review-escalation`.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:140:2. **California SMS Restriction (LEGAL-218)**  
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:141:   - SMS for `decline` notifications must remain unavailable when `loanState = "CA"`.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:171:   - User disables SMS for `manual-review-escalation` while email is enabled.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:194:  - Function accepts `(loanState, event, channel, mandatoryEvents)` as parameters (no internal imports of loan/user data).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:197:  - Rejects SMS disable for decline on CA loans (if `loanState = "CA"` and `event = "decline"` and `channel = "sms"`).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:198:  - Exports function for route and test use.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:221:- **Description**: Modify `src/backend/src/routes/notifications.ts` PUT handlers to call `canDisableChannel()` before persisting.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:250:- **Description**: Add feature flag `notificationPreferences` to `src/backend/src/config/feature-flags.ts` and guard routes.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:254:  - Wrap notification preference routes with flag check that returns 404 (not 403) for non-pilot users.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:269:  - Audit entry includes: action ("preference.updated"), actor ID, delegated-for ID (if applicable), previous preference state, new preference state, source ("notification-routes"), timestamp.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:320:  - Render matrix: rows = events (approval, decline, document-request, manual-review-escalation), columns = channels (email, sms).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:322:  - Mandatory events (manual-review-escalation) have **persistent helper text** (not tooltip): "At least one channel must be enabled for escalation notifications."
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:323:  - CA decline SMS disabled control with explanation: "SMS for decline notifications is unavailable for California loans (legal review LEGAL-218 in progress)."
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:375:  - Parameter-driven tests for all event/channel/loanState combinations.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:416:  - **Hard Negative 1**: Attempt to disable all channels for manual-review-escalation → fails with 400, preference unchanged.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:437:   - [ ] CA LEGAL-218 restriction verified with legal team.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:452:   - [ ] Delegated session mode toggle prevents writes at store and route level.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:498:| **Delegated Session Authorization Bypass** (SC-2 hard negative) | High     | Test delegated-session blocks at both route layer (task 1.3) and store layer (task 3.1); add audit entry validation to catch attempts. |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:499:| **California LEGAL-218 Regulatory Compliance** (FR-4, LEGAL-218) | Critical | Coordinate with legal team before pilot rollout; document LEGAL-218 case number in code and audit trail. Update feature-flag documentation with compliance expiration date (when LEGAL-218 resolves). |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:512:1. **Legal Review LEGAL-218 Completion**: California decline SMS restriction tied to external legal milestone. Plan CA restriction removal as separate rollout once LEGAL-218 resolves.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:523:| **Mandatory Event Rule (FR-2)**         | Confirmed  | ≥1 channel for manual-review-escalation; hard negatives explicit. |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:525:| **CA SMS Restriction (FR-4, LEGAL-218)** | Confirmed  | loan_state-based, explicit hard negative.                       |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:533:| **Delegated Session Guard at Route**    | Inferred   | Derived from SC-2 + existing route pattern.                     |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:534:| **Lazy Defaults (No Upfront Migration)** | Inferred   | Derived from FR-3 "no migration required" + route-level orchestration (AR3). |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:536:| **Metric Distinction (Validation vs Provider)** | Inferred | Derived from NFR-5 observability + route error handling.       |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:557:- Confirms system shape, rule placement (rules/), and route orchestration (AR3).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:563:- Existing `src/backend/src/routes/notifications.ts` (already partially implemented) shows route-layer delegation blocking and audit calls.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:570:- **LEGAL-218**: Legal review tracking regulatory compliance for decline SMS in California; temporary restriction applies to loans with `loanState = "CA"`.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:585:- [ ] All preference routes wrapped with flag check (404 for non-pilot).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:589:- [ ] Delegated-session authorization verified at route and store layers (task 4.1, 3.1).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:590:- [ ] CA LEGAL-218 restriction confirmed with legal team.
```

</details>


---

<sub>⏱️ 1m 16s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md (lines 1-220)

<details>
<summary>220 lines</summary>

```
1. # Notification Preferences Implementation Plan
2. 
3. **Status:** Planning Phase  
4. **Owner:** Lending Platform Product (PROJ-412)  
5. **Target:** 2026 Q2 Pilot  
6. **Last Updated:** 2026-04-15
7. 
8. ---
9. 
10. ## Executive Summary
11. 
12. This plan outlines the implementation of user-configurable notification preferences for the Loan Workbench platform. The feature addresses alert fatigue by allowing underwriters and analyst managers to control which notifications they receive (approval, decline, document-request, manual-review-escalation) across email and SMS channels.
13. 
14. **Key Constraints:**
15. - Mandatory notification events (manual-review-escalation) must always have at least one enabled channel.
16. - California loans have a temporary SMS restriction for decline notifications (LEGAL-218).
17. - Delegated analyst-manager sessions are read-only.
18. - Audit logging must fail-closed (abort saves if audit unavailable).
19. - Compliance reviewers have read-only access.
20. - SMS provider failures fall back to email without modifying stored preferences.
21. 
22. **Canonical Source:** Product Specification (specs/product-spec-notification-preferences.md) is the primary authority. NFRs provide constraints and safety rails. Architecture and ADRs guide implementation pattern choices.
23. 
24. ---
25. 
26. ## Confirmed Requirements with Source References
27. 
28. ### Functional Requirements (FR)
29. 
30. | ID  | Requirement                                                  | Source Reference                                            |
31. | --- | ------------------------------------------------------------ | ----------------------------------------------------------- |
32. | FR1 | Preference matrix: email/SMS independent per event type      | product-spec-notification-preferences.md § Functional Requirements § FR-1 |
33. | FR2 | Mandatory event rule: ≥1 channel for manual-review-escalation | product-spec-notification-preferences.md § FR-2 (explicit hard negative pattern) |
34. | FR3 | Role-based defaults on first access (no migration required)   | product-spec-notification-preferences.md § FR-3 § User-based defaults table |
35. | FR4 | California SMS restriction for decline (LEGAL-218)          | product-spec-notification-preferences.md § FR-4 (explicit: loan_state based) |
36. | FR5 | Degraded delivery fallback: SMS→email, no pref modification  | product-spec-notification-preferences.md § FR-5 (explicit false positive pattern) |
37. | FR6 | Audit all preference changes (actor, timestamp, old/new values) | product-spec-notification-preferences.md § FR-6 (complete audit trail) |
38. 
39. ### Special Conditions (SC)
40. 
41. | ID   | Condition                                                    | Source Reference                                           |
42. | ---- | ------------------------------------------------------------ | ---------------------------------------------------------- |
43. | SC-1 | Locked applications: prefs change globally, UI clarifies no retroactive effect | product-spec-notification-preferences.md § SC-1 |
44. | SC-2 | Delegated sessions: read-only (no modify), visually indicated | product-spec-notification-preferences.md § SC-2 (explicit hard negative pattern) |
45. | SC-3 | Multi-state portfolio: conditional rules, not blanket disable | product-spec-notification-preferences.md § SC-3 |
46. 
47. ### Non-Functional Requirements (NFR)
48. 
49. | ID   | Requirement                                                  | Source Reference                                                  |
50. | ---- | ------------------------------------------------------------ | ------------------------------------------------------------- |
51. | NFR1 | Performance: ≤150 ms p95 (settings page load), ≤400 ms p95 (save) | non-functional-requirements.md § NFR-1 |
52. | NFR2 | Availability: audit writes fail-closed (abort on audit unavailable) | non-functional-requirements.md § NFR-2 (explicit hard negative) |
53. | NFR3 | Security: no SMS phone numbers in logs/analytics; delegated sessions explicit in audit | non-functional-requirements.md § NFR-3 |
54. | NFR4 | Accessibility: persistent explanatory text for mandatory controls, ARIA live regions | non-functional-requirements.md § NFR-4 |
55. | NFR5 | Observability: distinct metrics for validation vs provider failures, SMS fallback tracking | non-functional-requirements.md § NFR-5 |
56. | NFR6 | Feature flag: 404 for non-pilot users (not 403); role-based defaults without migration | non-functional-requirements.md § NFR-6 |
57. | NFR7 | Compliance: 24-month audit retention; mandatory escalation delivery testable | non-functional-requirements.md § NFR-7 |
58. 
59. ### Architectural Patterns
60. 
61. | ID  | Pattern                                                      | Source Reference                                              |
62. | --- | ------------------------------------------------------------ | ------------------------------------------------------------- |
63. | AR1 | Central client store for persisted user preferences (not component-local state) | docs/adr/ADR-003-frontend-state.md § Decision |
64. | AR2 | Pure business rule functions with structured result objects  | src/backend/src/rules/business-rules.ts, role-permissions.ts |
65. | AR3 | Routes orchestrate; business rules live in src/backend/src/rules/ | docs/architecture.md § System Shape § Key Architectural Rules |
66. | AR4 | Audit via queue broker OR direct DB write (controlled by `queueAudit` flag) | src/backend/src/config/feature-flags.ts, audit-service.ts |
67. | AR5 | Message contracts in queue/contracts.ts are breaking-change surface | docs/architecture.md § Key Architectural Rules § #7 |
68. | AR6 | Feature-flagged endpoints return 404 (not 403) for non-pilot users | non-functional-requirements.md § NFR-6 |
69. 
70. ---
71. 
72. ## Open Questions with File References
73. 
74. 1. **Compliance Reviewer Audit Access**: Should compliance reviewers access preference audit history from the same settings page or a separate audit viewer?
75.    - **Reference**: product-spec-notification-preferences.md § Open Questions #1
76.    - **Implication for Plan**: Affects frontend routing and component composition. Current routes/audit.ts exists but may need expansion.
77. 
78. 2. **Portfolio View Restriction Display**: Should multi-state portfolio views show restriction summary banner or per-row indicators?
79.    - **Reference**: product-spec-notification-preferences.md § Open Questions #3
80.    - **Implication for Plan**: Affects frontend component architecture but does not block core feature (single-state view implementation).
81. 
82. 3. **Audit Service Availability Handling**: Does "fail-closed" mean the save endpoint returns 500, or does it retry with exponential backoff?
83.    - **Reference**: non-functional-requirements.md § NFR-2 (hard negative pattern)
84.    - **Implication for Plan**: Clarify in error-handling strategy before implementing audit integration.
85. 
86. 4. **SMS Fallback Metrics**: Should `notification.sms.fallback` metric increment only on successful email delivery, or on fallback trigger?
87.    - **Reference**: non-functional-requirements.md § NFR-5
88.    - **Implication for Plan**: Affects queue handler implementation in queue/handlers/.
89. 
90. ---
91. 
92. ## Inferred Implementation Choices
93. 
94. ### Separated from Confirmed Requirements
95. 
96. The following choices are derived from architecture and NFR context, **not** explicit in functional requirements:
97. 
98. 1. **Preference Validation as Pure Function**  
99.    - **Inference**: Business rule pattern (AR2) + mandatory event hard negative (FR2).
100.    - **Choice**: Implement `canDisableChannel(loanState, event, channel, userId) => ChannelDisableRule` as pure function in `src/backend/src/rules/notification-channel-rules.ts`.
101.    - **Why**: Enables AI-safety testing for edge cases (e.g., CA decline SMS, zero-channel scenarios).
102. 
103. 2. **Delegated Session Authorization at Route Handler**  
104.    - **Inference**: SC-2 delegated read-only pattern + existing route structure (notifications.ts).
105.    - **Choice**: Route handler checks `session.delegatedFor` and returns 403 before accepting PUT (already implemented in notifications.ts lines 59–65, 124–129, 206–211).
106.    - **Why**: Consistent with existing guard pattern; prevents optimization mistakes.
107. 
108. 3. **Role-Based Default Generation at Route Handler (Lazy)**  
109.    - **Inference**: FR-3 "no migration required" + architecture rule (AR3 "routes orchestrate").
110.    - **Choice**: GET /api/notifications/preferences/:userId returns defaults if no saved preferences exist (not on login/signup).
111.    - **Why**: Avoids upfront migration; accepts trade-off of first-access latency.
112. 
113. 4. **Central Client Store for Preference State**  
114.    - **Inference**: ADR-003 decision (AR1) + persisted user preferences cross-screen scenario.
115.    - **Choice**: Frontend state manager (likely Zustand or simple Redux) stores preference matrix and handles optimistic updates with rollback on API rejection.
116.    - **Why**: Ensures consistency across navigation, page refresh, and delegated-session detection.
117. 
118. 5. **Validation Failure Metric Distinction**  
119.    - **Inference**: NFR-5 observability requirement + route error handling.
120.    - **Choice**: Emit `preference.save.failure` with tag distinguishing `validation_error` (hard 400) vs `provider_error` (soft 500).
121.    - **Why**: Enables alerting on actionable infrastructure failures vs user-input mistakes.
122. 
123. 6. **Audit Logging as Separate Middleware Invocation**  
124.    - **Inference**: NFR-2 fail-closed + audit-service.ts pattern (auditAction queues or writes synchronously).
125.    - **Choice**: Preference save fails (rollback, return 500) if auditAction emits error or fails synchronously.
126.    - **Why**: Prevents silent audit loss; complies with fail-closed requirement.
127. 
128. ---
129. 
130. ## Constraints and Special Conditions
131. 
132. ### Critical Constraints
133. 
134. 1. **Mandatory Event Hard Negative (FR2)**  
135.    - Users may not disable all channels for `manual-review-escalation`.
136.    - **Both UI and API** must enforce this rule.
137.    - **Test Case**: Attempt to disable email while SMS is already disabled → must fail.
138.    - **Source**: product-spec-notification-preferences.md § FR-2 § HARD NEGATIVE pattern.
139. 
140. 2. **California SMS Restriction (LEGAL-218)**  
141.    - SMS for `decline` notifications must remain unavailable when `loanState = "CA"`.
142.    - Applies to **loan jurisdiction**, not borrower address if they differ.
143.    - **UI Impact**: Show persistent helper text (not tooltip) explaining restriction.
144.    - **Source**: product-spec-notification-preferences.md § FR-4; non-functional-requirements.md § NFR-6.
145. 
146. 3. **Fail-Closed Audit (NFR2)**  
147.    - If audit service is unavailable, preference save must **fail** (not silently skip audit).
148.    - **Test Case**: Simulate audit-service outage → API returns 500, preference is NOT saved.
149.    - **Source**: non-functional-requirements.md § NFR-2 § HARD NEGATIVE pattern.
150. 
151. 4. **Delegated Session Read-Only (SC-2)**  
152.    - Analyst managers in delegated mode may **read** but not **modify** delegate preferences.
153.    - UI must indicate delegated-session mode visually.
154.    - **Test Case**: Try to PATCH preferences in delegated session → 403 "Delegated sessions cannot modify...".
155.    - **Source**: product-spec-notification-preferences.md § SC-2 § HARD NEGATIVE pattern (optimistic UI update without server rejection).
156. 
157. 5. **Feature Flag Rollout (NFR6)**  
158.    - Non-pilot users must see **404** (not 403) for feature-flagged endpoints.
159.    - Leaking 403 tells users the feature exists but is restricted.
160.    - **Source**: non-functional-requirements.md § NFR-6.
161. 
162. ### False-Positive Patterns (Not Bugs)
163. 
164. 1. **SMS Fallback to Email During Outage**  
165.    - A user receives email instead of SMS during SMS-provider outage.
166.    - **Not a bug**: Stored preferences are unchanged; delivery logs show fallback.
167.    - Support must check delivery logs, not preference store.
168.    - **Source**: product-spec-notification-preferences.md § FR-5 § FALSE POSITIVE pattern.
169. 
170. 2. **Disabling SMS While Email Remains Enabled**  
171.    - User disables SMS for `manual-review-escalation` while email is enabled.
172.    - **Not a violation**: Constraint is ≥1 channel, not which channel is active.
173.    - **Source**: product-spec-notification-preferences.md § FR-2 § FALSE POSITIVE pattern.
174. 
175. 3. **Role-Based Defaults Without Migration**  
176.    - New/existing users without saved preferences receive defaults on first API access (no upfront migration).
177.    - **Not a data-integrity bug**: Lazy default generation is correct per spec.
178.    - **Source**: non-functional-requirements.md § NFR-6 § FALSE POSITIVE pattern.
179. 
180. 4. **Preference Reads During Audit Outage**  
181.    - User reads preferences while audit service is unavailable.
182.    - **Not a bug**: Only writes require audit availability.
183.    - **Source**: non-functional-requirements.md § NFR-2 § FALSE POSITIVE pattern.
184. 
185. ---
186. 
187. ## Numbered Tasks with Acceptance Criteria and Source References
188. 
189. ### Phase 1: Backend Rules and Persistence (Foundation)
190. 
191. #### Task 1.1: Implement Mandatory Event Validation Rule
192. - **Description**: Create pure function `canDisableChannel()` in `src/backend/src/rules/notification-channel-rules.ts`.
193. - **Acceptance Criteria**:
194.   - Function accepts `(loanState, event, channel, mandatoryEvents)` as parameters (no internal imports of loan/user data).
195.   - Returns `{ allowed: boolean, reason: string }`.
196.   - Rejects any attempt to disable all channels for events in mandatoryEvents.
197.   - Rejects SMS disable for decline on CA loans (if `loanState = "CA"` and `event = "decline"` and `channel = "sms"`).
198.   - Exports function for route and test use.
199. - **Test Coverage**:
200.   - Happy path: disable SMS for approval (email enabled) → allowed.
201.   - Boundary: disable email for escalation when SMS enabled → allowed.
202.   - Hard negative: disable email for escalation when SMS already disabled → rejected.
203.   - Hard negative: disable SMS for decline on CA loan → rejected.
204.   - Hard negative: disable SMS for decline on non-CA loan → allowed.
205. - **Source Reference**: product-spec-notification-preferences.md § FR-2, FR-4; rules/business-rules.ts pattern.
206. 
207. #### Task 1.2: Extend Preference Repository with Bulk Query
208. - **Description**: Add function to `src/backend/src/models/preference-repository.ts` to fetch all preferences for a user with defaults applied.
209. - **Acceptance Criteria**:
210.   - Function: `getEffectivePreferences(userId: string, role: UserRole) => NotificationPreference[]`.
211.   - Returns saved preferences or role-based defaults if no saved preferences exist.
212.   - Defaults match FR-3 table (underwriter/analyst-manager: all events email enabled, escalation-only SMS).
213.   - No database write occurs (read-only).
214. - **Test Coverage**:
215.   - New user (no saved prefs) → returns defaults for role.
216.   - Partially saved user (some prefs exist) → merges saved + defaults.
217.   - Full user (all prefs exist) → returns saved only.
218. - **Source Reference**: product-spec-notification-preferences.md § FR-3; preference-repository.ts pattern.
219. 
220. #### Task 1.3: Extend Notification Routes with Validation Gate
```

</details>


---

<sub>⏱️ 1m 16s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "PUT\\s+\"?/preferences|notificationRoutes\\.put\\(|preferences/:userId/email|preferences/:userId/sms",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows\\src\\backend\\src",
  "output_mode": "content",
  "glob": "**/*.ts",
  "-n": true,
  "head_limit": 200
}
```

</details>

<details>
<summary>7 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:46:notificationRoutes.put(
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:108: * PUT /api/notifications/preferences/:userId/email — set email notification preferences for all events.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:112:notificationRoutes.put(
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:113:  "/preferences/:userId/email",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:191: * PUT /api/notifications/preferences/:userId/sms — set SMS notification preferences for all events.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:195:notificationRoutes.put(
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:196:  "/preferences/:userId/sms",
```

</details>


---

<sub>⏱️ 2m 54s</sub>

### 💬 Copilot

I’m at the point of writing the test file now; I just need the package/module shape so the imports and mocks line up with the repo’s ESM setup.

---

<sub>⏱️ 2m 54s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows**

"**/package.json" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows

```
No files matched the pattern.
```


---

<sub>⏱️ 2m 54s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "\"type\"\\s*:\\s*\"module\"|vitest|supertest",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows",
  "output_mode": "content",
  "glob": "**/package.json",
  "-n": true,
  "head_limit": 50
}
```

</details>

```
No matches found.
```


---

<sub>⏱️ 2m 59s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend

```
dist
src
tests
tsconfig.json
```


---

<sub>⏱️ 2m 59s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows

<details>
<summary>14 lines</summary>

```
.github
.output
ASSESSMENT.md
HANDOFF.md
HANDOFF_IMPLEMENTATION.md
README.md
RUN.md
VERIFICATION.md
__pycache__
docs
specs
src
tests
util.py
```

</details>


---

<sub>⏱️ 4m 3s</sub>

### 💬 Copilot

I’ve got the shape pinned down. I’m adding the red test file now with rule-level coverage plus a couple of route-level assertions for the business rejection payloads and the allowed false-positive case.

---

<sub>⏱️ 4m 3s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Add File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows\\src\\backend\\tests\\unit\\notification-preference-write-rules.test.ts\n+import { beforeAll, beforeEach, describe, expect, it, vi } from \"vitest\";\n+import type { NotificationPreference } from \"../../src/models/types.js\";\n+\n+const preferenceRepoMock = vi.hoisted(() => ({\n+  findPreference: vi.fn(),\n+  findPreferencesForUser: vi.fn(),\n+  setPreference: vi.fn(),\n+}));\n+\n+const auditServiceMock = vi.hoisted(() => ({\n+  auditAction: vi.fn(),\n+}));\n+\n+vi.mock(\"../../src/models/preference-repository.js\", () => preferenceRepoMock);\n+vi.mock(\"../../src/services/audit-service.js\", () => auditServiceMock);\n+\n+let validateNotificationPreferenceWrite: (\n+  input: {\n+    nextPreference: Pick<\n+      NotificationPreference,\n+      \"event\" | \"channel\" | \"enabled\"\n+    >;\n+    existingPreferences: NotificationPreference[];\n+    loanState: string;\n+  },\n+) => { allowed: boolean; reason: string };\n+\n+let notificationRoutes: unknown;\n+\n+function buildPreference(\n+  overrides: Partial<NotificationPreference>,\n+): NotificationPreference {\n+  return {\n+    userId: \"user-1\",\n+    event: \"manual-review-escalation\",\n+    channel: \"email\",\n+    enabled: true,\n+    updatedAt: \"2026-04-16T00:00:00.000Z\",\n+    updatedBy: \"user-1\",\n+    ...overrides,\n+  };\n+}\n+\n+function normalizeText(value: unknown): string {\n+  return String(value).toLowerCase().replace(/\\s+/g, \" \").trim();\n+}\n+\n+function getPutPreferencesHandler(): (\n+  req: Record<string, unknown>,\n+  res: {\n+    status: (code: number) => unknown;\n+    json: (payload: unknown) => unknown;\n+  },\n+  next: (error?: unknown) => void,\n+) => void {\n+  const routeLayer = (notificationRoutes as {\n+    stack: Array<{\n+      route?: {\n+        path: string;\n+        methods: Record<string, boolean>;\n+        stack: Array<{ handle: (...args: unknown[]) => void }>;\n+      };\n+    }>;\n+  }).stack.find(\n+    (layer) => layer.route?.path === \"/preferences\" && layer.route.methods.put,\n+  );\n+\n+  if (!routeLayer?.route) {\n+    throw new Error(\"PUT /preferences route not found.\");\n+  }\n+\n+  return routeLayer.route.stack[routeLayer.route.stack.length - 1]\n+    .handle as typeof getPutPreferencesHandler extends () => infer T ? T : never;\n+}\n+\n+function createResponse() {\n+  return {\n+    statusCode: 200,\n+    body: undefined as unknown,\n+    status(code: number) {\n+      this.statusCode = code;\n+      return this;\n+    },\n+    json(payload: unknown) {\n+      this.body = payload;\n+      return this;\n+    },\n+  };\n+}\n+\n+beforeAll(async () => {\n+  ({ validateNotificationPreferenceWrite } = await import(\n+    \"../../src/rules/notification-preference-write-rules.js\"\n+  ));\n+  ({ notificationRoutes } = await import(\"../../src/routes/notifications.js\"));\n+});\n+\n+beforeEach(() => {\n+  vi.clearAllMocks();\n+});\n+\n+describe(\"validateNotificationPreferenceWrite\", () => {\n+  it(\"allows disabling escalation sms when escalation email remains enabled\", () => {\n+    // FALSE POSITIVE: SMS can be disabled when email still preserves the mandatory event.\n+    const result = validateNotificationPreferenceWrite({\n+      nextPreference: {\n+        event: \"manual-review-escalation\",\n+        channel: \"sms\",\n+        enabled: false,\n+      },\n+      existingPreferences: [\n+        buildPreference({ event: \"manual-review-escalation\", channel: \"email\" }),\n+        buildPreference({\n+          event: \"manual-review-escalation\",\n+          channel: \"sms\",\n+          enabled: true,\n+        }),\n+      ],\n+      loanState: \"NY\",\n+    });\n+\n+    expect(result.allowed).toBe(true);\n+  });\n+\n+  it(\"rejects disabling the last enabled escalation channel\", () => {\n+    // HARD NEGATIVE: manual-review-escalation must never end up with zero enabled channels.\n+    const result = validateNotificationPreferenceWrite({\n+      nextPreference: {\n+        event: \"manual-review-escalation\",\n+        channel: \"email\",\n+        enabled: false,\n+      },\n+      existingPreferences: [\n+        buildPreference({ event: \"manual-review-escalation\", channel: \"email\" }),\n+        buildPreference({\n+          event: \"manual-review-escalation\",\n+          channel: \"sms\",\n+          enabled: false,\n+        }),\n+      ],\n+      loanState: \"NY\",\n+    });\n+\n+    const reason = normalizeText(result.reason);\n+\n+    expect(result.allowed).toBe(false);\n+    expect(reason).toContain(\"manual-review-escalation\");\n+    expect(reason).toContain(\"at least one\");\n+  });\n+\n+  it.each([\"CA\", \"California\"])(\n+    \"rejects enabling decline sms for %s loan state under LEGAL-218\",\n+    (loanState) => {\n+      const result = validateNotificationPreferenceWrite({\n+        nextPreference: {\n+          event: \"decline\",\n+          channel: \"sms\",\n+          enabled: true,\n+        },\n+        existingPreferences: [],\n+        loanState,\n+      });\n+\n+      const reason = normalizeText(result.reason);\n+\n+      expect(result.allowed).toBe(false);\n+      expect(reason).toContain(\"legal-218\");\n+      expect(reason).toContain(\"decline\");\n+      expect(reason).toContain(\"sms\");\n+    },\n+  );\n+\n+  it(\"allows enabling decline sms for non-California loan state\", () => {\n+    const result = validateNotificationPreferenceWrite({\n+      nextPreference: {\n+        event: \"decline\",\n+        channel: \"sms\",\n+        enabled: true,\n+      },\n+      existingPreferences: [],\n+      loanState: \"NV\",\n+    });\n+\n+    expect(result.allowed).toBe(true);\n+  });\n+});\n+\n+describe(\"PUT /preferences route hardening\", () => {\n+  it(\"returns 400 with escalation invariant details when the write would disable the last channel\", () => {\n+    const handler = getPutPreferencesHandler();\n+    const response = createResponse();\n+\n+    preferenceRepoMock.findPreference.mockReturnValue(\n+      buildPreference({ event: \"manual-review-escalation\", channel: \"email\" }),\n+    );\n+    preferenceRepoMock.findPreferencesForUser.mockReturnValue([\n+      buildPreference({ event: \"manual-review-escalation\", channel: \"email\" }),\n+      buildPreference({\n+        event: \"manual-review-escalation\",\n+        channel: \"sms\",\n+        enabled: false,\n+      }),\n+    ]);\n+\n+    handler(\n+      {\n+        body: {\n+          userId: \"user-1\",\n+          event: \"manual-review-escalation\",\n+          channel: \"email\",\n+          enabled: false,\n+          loanState: \"NY\",\n+        },\n+        session: {\n+          actor: {\n+            id: \"user-1\",\n+            role: \"underwriter\",\n+            name: \"User One\",\n+            email: \"user-1@example.com\",\n+          },\n+        },\n+      },\n+      response,\n+      vi.fn(),\n+    );\n+\n+    const payload = response.body as { error?: string; details?: string[] };\n+    const details = normalizeText(payload.details?.join(\" \"));\n+\n+    expect(response.statusCode).toBe(400);\n+    expect(payload.error).toBe(\"Validation failed.\");\n+    expect(details).toContain(\"manual-review-escalation\");\n+    expect(details).toContain(\"at least one\");\n+    expect(preferenceRepoMock.setPreference).not.toHaveBeenCalled();\n+    expect(auditServiceMock.auditAction).not.toHaveBeenCalled();\n+  });\n+\n+  it(\"returns 400 with LEGAL-218 details when California decline sms is enabled\", () => {\n+    const handler = getPutPreferencesHandler();\n+    const response = createResponse();\n+\n+    preferenceRepoMock.findPreference.mockReturnValue(\n+      buildPreference({\n+        event: \"decline\",\n+        channel: \"sms\",\n+        enabled: false,\n+      }),\n+    );\n+    preferenceRepoMock.findPreferencesForUser.mockReturnValue([]);\n+\n+    handler(\n+      {\n+        body: {\n+          userId: \"user-1\",\n+          event: \"decline\",\n+          channel: \"sms\",\n+          enabled: true,\n+          loanState: \"California\",\n+        },\n+        session: {\n+          actor: {\n+            id: \"user-1\",\n+            role: \"underwriter\",\n+            name: \"User One\",\n+            email: \"user-1@example.com\",\n+          },\n+        },\n+      },\n+      response,\n+      vi.fn(),\n+    );\n+\n+    const payload = response.body as { details?: string[] };\n+    const details = normalizeText(payload.details?.join(\" \"));\n+\n+    expect(response.statusCode).toBe(400);\n+    expect(details).toContain(\"legal-218\");\n+    expect(details).toContain(\"decline\");\n+    expect(details).toContain(\"sms\");\n+    expect(preferenceRepoMock.setPreference).not.toHaveBeenCalled();\n+  });\n+\n+  it(\"allows disabling escalation sms when escalation email stays enabled\", () => {\n+    const handler = getPutPreferencesHandler();\n+    const response = createResponse();\n+\n+    preferenceRepoMock.findPreference.mockReturnValue(\n+      buildPreference({\n+        event: \"manual-review-escalation\",\n+        channel: \"sms\",\n+        enabled: true,\n+      }),\n+    );\n+    preferenceRepoMock.findPreferencesForUser.mockReturnValue([\n+      buildPreference({ event: \"manual-review-escalation\", channel: \"email\" }),\n+      buildPreference({\n+        event: \"manual-review-escalation\",\n+        channel: \"sms\",\n+        enabled: true,\n+      }),\n+    ]);\n+\n+    handler(\n+      {\n+        body: {\n+          userId: \"user-1\",\n+          event: \"manual-review-escalation\",\n+          channel: \"sms\",\n+          enabled: false,\n+          loanState: \"NY\",\n+        },\n+        session: {\n+          actor: {\n+            id: \"user-1\",\n+            role: \"underwriter\",\n+            name: \"User One\",\n+            email: \"user-1@example.com\",\n+          },\n+        },\n+      },\n+      response,\n+      vi.fn(),\n+    );\n+\n+    expect(response.statusCode).toBe(200);\n+    expect(preferenceRepoMock.setPreference).toHaveBeenCalledTimes(1);\n+    expect(auditServiceMock.auditAction).toHaveBeenCalledTimes(1);\n+  });\n+});\n*** End Patch\n"
```

</details>

```
Added 1 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts
```


---

<sub>⏱️ 4m 12s</sub>

### 💬 Copilot

The test file is in place. I’m reading it once to catch any brittle import/router-stack issues before I add the rule and route wiring it expects.

---

<sub>⏱️ 4m 12s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts

<details>
<summary>330 lines</summary>

```
1. import { beforeAll, beforeEach, describe, expect, it, vi } from "vitest";
2. import type { NotificationPreference } from "../../src/models/types.js";
3. 
4. const preferenceRepoMock = vi.hoisted(() => ({
5.   findPreference: vi.fn(),
6.   findPreferencesForUser: vi.fn(),
7.   setPreference: vi.fn(),
8. }));
9. 
10. const auditServiceMock = vi.hoisted(() => ({
11.   auditAction: vi.fn(),
12. }));
13. 
14. vi.mock("../../src/models/preference-repository.js", () => preferenceRepoMock);
15. vi.mock("../../src/services/audit-service.js", () => auditServiceMock);
16. 
17. let validateNotificationPreferenceWrite: (
18.   input: {
19.     nextPreference: Pick<
20.       NotificationPreference,
21.       "event" | "channel" | "enabled"
22.     >;
23.     existingPreferences: NotificationPreference[];
24.     loanState: string;
25.   },
26. ) => { allowed: boolean; reason: string };
27. 
28. let notificationRoutes: unknown;
29. 
30. function buildPreference(
31.   overrides: Partial<NotificationPreference>,
32. ): NotificationPreference {
33.   return {
34.     userId: "user-1",
35.     event: "manual-review-escalation",
36.     channel: "email",
37.     enabled: true,
38.     updatedAt: "2026-04-16T00:00:00.000Z",
39.     updatedBy: "user-1",
40.     ...overrides,
41.   };
42. }
43. 
44. function normalizeText(value: unknown): string {
45.   return String(value).toLowerCase().replace(/\s+/g, " ").trim();
46. }
47. 
48. function getPutPreferencesHandler(): (
49.   req: Record<string, unknown>,
50.   res: {
51.     status: (code: number) => unknown;
52.     json: (payload: unknown) => unknown;
53.   },
54.   next: (error?: unknown) => void,
55. ) => void {
56.   const routeLayer = (notificationRoutes as {
57.     stack: Array<{
58.       route?: {
59.         path: string;
60.         methods: Record<string, boolean>;
61.         stack: Array<{ handle: (...args: unknown[]) => void }>;
62.       };
63.     }>;
64.   }).stack.find(
65.     (layer) => layer.route?.path === "/preferences" && layer.route.methods.put,
66.   );
67. 
68.   if (!routeLayer?.route) {
69.     throw new Error("PUT /preferences route not found.");
70.   }
71. 
72.   return routeLayer.route.stack[routeLayer.route.stack.length - 1]
73.     .handle as typeof getPutPreferencesHandler extends () => infer T ? T : never;
74. }
75. 
76. function createResponse() {
77.   return {
78.     statusCode: 200,
79.     body: undefined as unknown,
80.     status(code: number) {
81.       this.statusCode = code;
82.       return this;
83.     },
84.     json(payload: unknown) {
85.       this.body = payload;
86.       return this;
87.     },
88.   };
89. }
90. 
91. beforeAll(async () => {
92.   ({ validateNotificationPreferenceWrite } = await import(
93.     "../../src/rules/notification-preference-write-rules.js"
94.   ));
95.   ({ notificationRoutes } = await import("../../src/routes/notifications.js"));
96. });
97. 
98. beforeEach(() => {
99.   vi.clearAllMocks();
100. });
101. 
102. describe("validateNotificationPreferenceWrite", () => {
103.   it("allows disabling escalation sms when escalation email remains enabled", () => {
104.     // FALSE POSITIVE: SMS can be disabled when email still preserves the mandatory event.
105.     const result = validateNotificationPreferenceWrite({
106.       nextPreference: {
107.         event: "manual-review-escalation",
108.         channel: "sms",
109.         enabled: false,
110.       },
111.       existingPreferences: [
112.         buildPreference({ event: "manual-review-escalation", channel: "email" }),
113.         buildPreference({
114.           event: "manual-review-escalation",
115.           channel: "sms",
116.           enabled: true,
117.         }),
118.       ],
119.       loanState: "NY",
120.     });
121. 
122.     expect(result.allowed).toBe(true);
123.   });
124. 
125.   it("rejects disabling the last enabled escalation channel", () => {
126.     // HARD NEGATIVE: manual-review-escalation must never end up with zero enabled channels.
127.     const result = validateNotificationPreferenceWrite({
128.       nextPreference: {
129.         event: "manual-review-escalation",
130.         channel: "email",
131.         enabled: false,
132.       },
133.       existingPreferences: [
134.         buildPreference({ event: "manual-review-escalation", channel: "email" }),
135.         buildPreference({
136.           event: "manual-review-escalation",
137.           channel: "sms",
138.           enabled: false,
139.         }),
140.       ],
141.       loanState: "NY",
142.     });
143. 
144.     const reason = normalizeText(result.reason);
145. 
146.     expect(result.allowed).toBe(false);
147.     expect(reason).toContain("manual-review-escalation");
148.     expect(reason).toContain("at least one");
149.   });
150. 
151.   it.each(["CA", "California"])(
152.     "rejects enabling decline sms for %s loan state under LEGAL-218",
153.     (loanState) => {
154.       const result = validateNotificationPreferenceWrite({
155.         nextPreference: {
156.           event: "decline",
157.           channel: "sms",
158.           enabled: true,
159.         },
160.         existingPreferences: [],
161.         loanState,
162.       });
163. 
164.       const reason = normalizeText(result.reason);
165. 
166.       expect(result.allowed).toBe(false);
167.       expect(reason).toContain("legal-218");
168.       expect(reason).toContain("decline");
169.       expect(reason).toContain("sms");
170.     },
171.   );
172. 
173.   it("allows enabling decline sms for non-California loan state", () => {
174.     const result = validateNotificationPreferenceWrite({
175.       nextPreference: {
176.         event: "decline",
177.         channel: "sms",
178.         enabled: true,
179.       },
180.       existingPreferences: [],
181.       loanState: "NV",
182.     });
183. 
184.     expect(result.allowed).toBe(true);
185.   });
186. });
187. 
188. describe("PUT /preferences route hardening", () => {
189.   it("returns 400 with escalation invariant details when the write would disable the last channel", () => {
190.     const handler = getPutPreferencesHandler();
191.     const response = createResponse();
192. 
193.     preferenceRepoMock.findPreference.mockReturnValue(
194.       buildPreference({ event: "manual-review-escalation", channel: "email" }),
195.     );
196.     preferenceRepoMock.findPreferencesForUser.mockReturnValue([
197.       buildPreference({ event: "manual-review-escalation", channel: "email" }),
198.       buildPreference({
199.         event: "manual-review-escalation",
200.         channel: "sms",
201.         enabled: false,
202.       }),
203.     ]);
204. 
205.     handler(
206.       {
207.         body: {
208.           userId: "user-1",
209.           event: "manual-review-escalation",
210.           channel: "email",
211.           enabled: false,
212.           loanState: "NY",
213.         },
214.         session: {
215.           actor: {
216.             id: "user-1",
217.             role: "underwriter",
218.             name: "User One",
219.             email: "user-1@example.com",
220.           },
221.         },
222.       },
223.       response,
224.       vi.fn(),
225.     );
226. 
227.     const payload = response.body as { error?: string; details?: string[] };
228.     const details = normalizeText(payload.details?.join(" "));
229. 
230.     expect(response.statusCode).toBe(400);
231.     expect(payload.error).toBe("Validation failed.");
232.     expect(details).toContain("manual-review-escalation");
233.     expect(details).toContain("at least one");
234.     expect(preferenceRepoMock.setPreference).not.toHaveBeenCalled();
235.     expect(auditServiceMock.auditAction).not.toHaveBeenCalled();
236.   });
237. 
238.   it("returns 400 with LEGAL-218 details when California decline sms is enabled", () => {
239.     const handler = getPutPreferencesHandler();
240.     const response = createResponse();
241. 
242.     preferenceRepoMock.findPreference.mockReturnValue(
243.       buildPreference({
244.         event: "decline",
245.         channel: "sms",
246.         enabled: false,
247.       }),
248.     );
249.     preferenceRepoMock.findPreferencesForUser.mockReturnValue([]);
250. 
251.     handler(
252.       {
253.         body: {
254.           userId: "user-1",
255.           event: "decline",
256.           channel: "sms",
257.           enabled: true,
258.           loanState: "California",
259.         },
260.         session: {
261.           actor: {
262.             id: "user-1",
263.             role: "underwriter",
264.             name: "User One",
265.             email: "user-1@example.com",
266.           },
267.         },
268.       },
269.       response,
270.       vi.fn(),
271.     );
272. 
273.     const payload = response.body as { details?: string[] };
274.     const details = normalizeText(payload.details?.join(" "));
275. 
276.     expect(response.statusCode).toBe(400);
277.     expect(details).toContain("legal-218");
278.     expect(details).toContain("decline");
279.     expect(details).toContain("sms");
280.     expect(preferenceRepoMock.setPreference).not.toHaveBeenCalled();
281.   });
282. 
283.   it("allows disabling escalation sms when escalation email stays enabled", () => {
284.     const handler = getPutPreferencesHandler();
285.     const response = createResponse();
286. 
287.     preferenceRepoMock.findPreference.mockReturnValue(
288.       buildPreference({
289.         event: "manual-review-escalation",
290.         channel: "sms",
291.         enabled: true,
292.       }),
293.     );
294.     preferenceRepoMock.findPreferencesForUser.mockReturnValue([
295.       buildPreference({ event: "manual-review-escalation", channel: "email" }),
296.       buildPreference({
297.         event: "manual-review-escalation",
298.         channel: "sms",
299.         enabled: true,
300.       }),
301.     ]);
302. 
303.     handler(
304.       {
305.         body: {
306.           userId: "user-1",
307.           event: "manual-review-escalation",
308.           channel: "sms",
309.           enabled: false,
310.           loanState: "NY",
311.         },
312.         session: {
313.           actor: {
314.             id: "user-1",
315.             role: "underwriter",
316.             name: "User One",
317.             email: "user-1@example.com",
318.           },
319.         },
320.       },
321.       response,
322.       vi.fn(),
323.     );
324. 
325.     expect(response.statusCode).toBe(200);
326.     expect(preferenceRepoMock.setPreference).toHaveBeenCalledTimes(1);
327.     expect(auditServiceMock.auditAction).toHaveBeenCalledTimes(1);
328.   });
329. });
330.
```

</details>


---

<sub>⏱️ 4m 36s</sub>

### 💬 Copilot

The new rule module is next. I’m keeping it pure and explicit — just `nextPreference`, `existingPreferences`, and `loanState` — so the route stays as the orchestrator and the business decisions stay testable.

---

<sub>⏱️ 4m 36s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Add File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows\\src\\backend\\src\\rules\\notification-preference-write-rules.ts\n+// ---------------------------------------------------------------------------\n+// Notification Preference Write Rules\n+// ---------------------------------------------------------------------------\n+// FALSE POSITIVE: disabling manual-review-escalation SMS is allowed when email\n+// remains enabled. The invariant is \"at least one channel\", not \"all channels\".\n+//\n+// HARD NEGATIVE: rejecting only a specific channel toggle is insufficient if\n+// the write would leave manual-review-escalation with zero enabled channels.\n+//\n+// LEGAL-218: decline SMS cannot be enabled for California loan contexts.\n+// ---------------------------------------------------------------------------\n+\n+import type {\n+  NotificationChannel,\n+  NotificationPreference,\n+} from \"../models/types.js\";\n+\n+export interface NotificationPreferenceWriteInput {\n+  nextPreference: Pick<NotificationPreference, \"event\" | \"channel\" | \"enabled\">;\n+  existingPreferences: NotificationPreference[];\n+  loanState: string;\n+}\n+\n+export interface NotificationPreferenceWriteRule {\n+  allowed: boolean;\n+  reason: string;\n+}\n+\n+const ALLOWED_WRITE: NotificationPreferenceWriteRule = {\n+  allowed: true,\n+  reason: \"Notification preference write allowed.\",\n+};\n+\n+export function validateNotificationPreferenceWrite(\n+  input: NotificationPreferenceWriteInput,\n+): NotificationPreferenceWriteRule {\n+  const { nextPreference, existingPreferences, loanState } = input;\n+\n+  if (\n+    nextPreference.event === \"decline\" &&\n+    nextPreference.channel === \"sms\" &&\n+    nextPreference.enabled &&\n+    isCaliforniaLoanState(loanState)\n+  ) {\n+    return {\n+      allowed: false,\n+      reason:\n+        \"LEGAL-218: decline SMS cannot be enabled for California loanState.\",\n+    };\n+  }\n+\n+  if (\n+    nextPreference.event !== \"manual-review-escalation\" ||\n+    nextPreference.enabled\n+  ) {\n+    return ALLOWED_WRITE;\n+  }\n+\n+  const otherChannel = otherNotificationChannel(nextPreference.channel);\n+  const otherPreference = existingPreferences.find(\n+    (preference) =>\n+      preference.event === \"manual-review-escalation\" &&\n+      preference.channel === otherChannel,\n+  );\n+\n+  if (otherPreference?.enabled === false) {\n+    return {\n+      allowed: false,\n+      reason:\n+        \"manual-review-escalation must keep at least one channel enabled.\",\n+    };\n+  }\n+\n+  return ALLOWED_WRITE;\n+}\n+\n+function otherNotificationChannel(\n+  channel: NotificationChannel,\n+): NotificationChannel {\n+  return channel === \"email\" ? \"sms\" : \"email\";\n+}\n+\n+function isCaliforniaLoanState(loanState: string): boolean {\n+  const normalized = loanState.trim().toLowerCase();\n+  return normalized === \"ca\" || normalized === \"california\";\n+}\n*** End Patch\n"
```

</details>

```
Added 1 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\notification-preference-write-rules.ts
```


---

<sub>⏱️ 4m 52s</sub>

### 💬 Copilot

I’ve got the pure rule in place. Now I’m wiring only the single `PUT /preferences` path to call it and return the same simple 400-style validation payload on business-rule rejections.

---

<sub>⏱️ 4m 52s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Update File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows\\src\\backend\\src\\routes\\notifications.ts\n@@\n import { requireRole } from \"../middleware/auth.js\";\n import { validateBody } from \"../middleware/request-validator.js\";\n+import { validateNotificationPreferenceWrite } from \"../rules/notification-preference-write-rules.js\";\n import { hasPermission } from \"../rules/role-permissions.js\";\n import { auditAction } from \"../services/audit-service.js\";\n import * as prefRepo from \"../models/preference-repository.js\";\n@@\n   validateBody([\n     { field: \"userId\", type: \"string\", required: true },\n     { field: \"event\", type: \"string\", required: true },\n     { field: \"channel\", type: \"string\", required: true },\n     { field: \"enabled\", type: \"boolean\", required: true },\n+    { field: \"loanState\", type: \"string\", required: true },\n   ]),\n   (req, res, next) => {\n@@\n-      const { userId, event, channel, enabled } = req.body;\n+      const { userId, event, channel, enabled, loanState } = req.body;\n       const now = new Date().toISOString();\n+      const existingPreferences = prefRepo.findPreferencesForUser(userId);\n+      const writeRule = validateNotificationPreferenceWrite({\n+        nextPreference: { event, channel, enabled },\n+        existingPreferences,\n+        loanState,\n+      });\n+\n+      if (!writeRule.allowed) {\n+        res.status(400).json({\n+          error: \"Validation failed.\",\n+          details: [writeRule.reason],\n+        });\n+        return;\n+      }\n \n       const previous = prefRepo.findPreference(userId, event, channel);\n*** End Patch\n"
```

</details>

```
Modified 1 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts
```


---

<sub>⏱️ 4m 59s</sub>

### 💬 Copilot

The production wiring is in. I’m doing a final read-through of the changed files now to catch any type or scope mismatches since this run is file-only and I’m not using the shell.

---

<sub>⏱️ 4m 59s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\notification-preference-write-rules.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\notification-preference-write-rules.ts

<details>
<summary>87 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Notification Preference Write Rules
3. // ---------------------------------------------------------------------------
4. // FALSE POSITIVE: disabling manual-review-escalation SMS is allowed when email
5. // remains enabled. The invariant is "at least one channel", not "all channels".
6. //
7. // HARD NEGATIVE: rejecting only a specific channel toggle is insufficient if
8. // the write would leave manual-review-escalation with zero enabled channels.
9. //
10. // LEGAL-218: decline SMS cannot be enabled for California loan contexts.
11. // ---------------------------------------------------------------------------
12. 
13. import type {
14.   NotificationChannel,
15.   NotificationPreference,
16. } from "../models/types.js";
17. 
18. export interface NotificationPreferenceWriteInput {
19.   nextPreference: Pick<NotificationPreference, "event" | "channel" | "enabled">;
20.   existingPreferences: NotificationPreference[];
21.   loanState: string;
22. }
23. 
24. export interface NotificationPreferenceWriteRule {
25.   allowed: boolean;
26.   reason: string;
27. }
28. 
29. const ALLOWED_WRITE: NotificationPreferenceWriteRule = {
30.   allowed: true,
31.   reason: "Notification preference write allowed.",
32. };
33. 
34. export function validateNotificationPreferenceWrite(
35.   input: NotificationPreferenceWriteInput,
36. ): NotificationPreferenceWriteRule {
37.   const { nextPreference, existingPreferences, loanState } = input;
38. 
39.   if (
40.     nextPreference.event === "decline" &&
41.     nextPreference.channel === "sms" &&
42.     nextPreference.enabled &&
43.     isCaliforniaLoanState(loanState)
44.   ) {
45.     return {
46.       allowed: false,
47.       reason:
48.         "LEGAL-218: decline SMS cannot be enabled for California loanState.",
49.     };
50.   }
51. 
52.   if (
53.     nextPreference.event !== "manual-review-escalation" ||
54.     nextPreference.enabled
55.   ) {
56.     return ALLOWED_WRITE;
57.   }
58. 
59.   const otherChannel = otherNotificationChannel(nextPreference.channel);
60.   const otherPreference = existingPreferences.find(
61.     (preference) =>
62.       preference.event === "manual-review-escalation" &&
63.       preference.channel === otherChannel,
64.   );
65. 
66.   if (otherPreference?.enabled === false) {
67.     return {
68.       allowed: false,
69.       reason:
70.         "manual-review-escalation must keep at least one channel enabled.",
71.     };
72.   }
73. 
74.   return ALLOWED_WRITE;
75. }
76. 
77. function otherNotificationChannel(
78.   channel: NotificationChannel,
79. ): NotificationChannel {
80.   return channel === "email" ? "sms" : "email";
81. }
82. 
83. function isCaliforniaLoanState(loanState: string): boolean {
84.   const normalized = loanState.trim().toLowerCase();
85.   return normalized === "ca" || normalized === "california";
86. }
87.
```

</details>


---

<sub>⏱️ 4m 59s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts (lines 1-120)

<details>
<summary>120 lines</summary>

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
19. import { validateNotificationPreferenceWrite } from "../rules/notification-preference-write-rules.js";
20. import { hasPermission } from "../rules/role-permissions.js";
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
55.     { field: "loanState", type: "string", required: true },
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
80.       const writeRule = validateNotificationPreferenceWrite({
81.         nextPreference: { event, channel, enabled },
82.         existingPreferences,
83.         loanState,
84.       });
85. 
86.       if (!writeRule.allowed) {
87.         res.status(400).json({
88.           error: "Validation failed.",
89.           details: [writeRule.reason],
90.         });
91.         return;
92.       }
93. 
94.       const previous = prefRepo.findPreference(userId, event, channel);
95. 
96.       const pref: NotificationPreference = {
97.         userId,
98.         event,
99.         channel,
100.         enabled,
101.         updatedAt: now,
102.         updatedBy: session.actor.id,
103.       };
104. 
105.       prefRepo.setPreference(pref);
106. 
107.       // Audit the preference change
108.       auditAction(
109.         session,
110.         "preference.updated",
111.         previous ?? null,
112.         pref,
113.         "notification-routes",
114.       );
115. 
116.       res.json(pref);
117.     } catch (err) {
118.       next(err);
119.     }
120.   },
```

</details>


---

<sub>⏱️ 4m 59s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts (lines 1-330)

<details>
<summary>330 lines</summary>

```
1. import { beforeAll, beforeEach, describe, expect, it, vi } from "vitest";
2. import type { NotificationPreference } from "../../src/models/types.js";
3. 
4. const preferenceRepoMock = vi.hoisted(() => ({
5.   findPreference: vi.fn(),
6.   findPreferencesForUser: vi.fn(),
7.   setPreference: vi.fn(),
8. }));
9. 
10. const auditServiceMock = vi.hoisted(() => ({
11.   auditAction: vi.fn(),
12. }));
13. 
14. vi.mock("../../src/models/preference-repository.js", () => preferenceRepoMock);
15. vi.mock("../../src/services/audit-service.js", () => auditServiceMock);
16. 
17. let validateNotificationPreferenceWrite: (
18.   input: {
19.     nextPreference: Pick<
20.       NotificationPreference,
21.       "event" | "channel" | "enabled"
22.     >;
23.     existingPreferences: NotificationPreference[];
24.     loanState: string;
25.   },
26. ) => { allowed: boolean; reason: string };
27. 
28. let notificationRoutes: unknown;
29. 
30. function buildPreference(
31.   overrides: Partial<NotificationPreference>,
32. ): NotificationPreference {
33.   return {
34.     userId: "user-1",
35.     event: "manual-review-escalation",
36.     channel: "email",
37.     enabled: true,
38.     updatedAt: "2026-04-16T00:00:00.000Z",
39.     updatedBy: "user-1",
40.     ...overrides,
41.   };
42. }
43. 
44. function normalizeText(value: unknown): string {
45.   return String(value).toLowerCase().replace(/\s+/g, " ").trim();
46. }
47. 
48. function getPutPreferencesHandler(): (
49.   req: Record<string, unknown>,
50.   res: {
51.     status: (code: number) => unknown;
52.     json: (payload: unknown) => unknown;
53.   },
54.   next: (error?: unknown) => void,
55. ) => void {
56.   const routeLayer = (notificationRoutes as {
57.     stack: Array<{
58.       route?: {
59.         path: string;
60.         methods: Record<string, boolean>;
61.         stack: Array<{ handle: (...args: unknown[]) => void }>;
62.       };
63.     }>;
64.   }).stack.find(
65.     (layer) => layer.route?.path === "/preferences" && layer.route.methods.put,
66.   );
67. 
68.   if (!routeLayer?.route) {
69.     throw new Error("PUT /preferences route not found.");
70.   }
71. 
72.   return routeLayer.route.stack[routeLayer.route.stack.length - 1]
73.     .handle as typeof getPutPreferencesHandler extends () => infer T ? T : never;
74. }
75. 
76. function createResponse() {
77.   return {
78.     statusCode: 200,
79.     body: undefined as unknown,
80.     status(code: number) {
81.       this.statusCode = code;
82.       return this;
83.     },
84.     json(payload: unknown) {
85.       this.body = payload;
86.       return this;
87.     },
88.   };
89. }
90. 
91. beforeAll(async () => {
92.   ({ validateNotificationPreferenceWrite } = await import(
93.     "../../src/rules/notification-preference-write-rules.js"
94.   ));
95.   ({ notificationRoutes } = await import("../../src/routes/notifications.js"));
96. });
97. 
98. beforeEach(() => {
99.   vi.clearAllMocks();
100. });
101. 
102. describe("validateNotificationPreferenceWrite", () => {
103.   it("allows disabling escalation sms when escalation email remains enabled", () => {
104.     // FALSE POSITIVE: SMS can be disabled when email still preserves the mandatory event.
105.     const result = validateNotificationPreferenceWrite({
106.       nextPreference: {
107.         event: "manual-review-escalation",
108.         channel: "sms",
109.         enabled: false,
110.       },
111.       existingPreferences: [
112.         buildPreference({ event: "manual-review-escalation", channel: "email" }),
113.         buildPreference({
114.           event: "manual-review-escalation",
115.           channel: "sms",
116.           enabled: true,
117.         }),
118.       ],
119.       loanState: "NY",
120.     });
121. 
122.     expect(result.allowed).toBe(true);
123.   });
124. 
125.   it("rejects disabling the last enabled escalation channel", () => {
126.     // HARD NEGATIVE: manual-review-escalation must never end up with zero enabled channels.
127.     const result = validateNotificationPreferenceWrite({
128.       nextPreference: {
129.         event: "manual-review-escalation",
130.         channel: "email",
131.         enabled: false,
132.       },
133.       existingPreferences: [
134.         buildPreference({ event: "manual-review-escalation", channel: "email" }),
135.         buildPreference({
136.           event: "manual-review-escalation",
137.           channel: "sms",
138.           enabled: false,
139.         }),
140.       ],
141.       loanState: "NY",
142.     });
143. 
144.     const reason = normalizeText(result.reason);
145. 
146.     expect(result.allowed).toBe(false);
147.     expect(reason).toContain("manual-review-escalation");
148.     expect(reason).toContain("at least one");
149.   });
150. 
151.   it.each(["CA", "California"])(
152.     "rejects enabling decline sms for %s loan state under LEGAL-218",
153.     (loanState) => {
154.       const result = validateNotificationPreferenceWrite({
155.         nextPreference: {
156.           event: "decline",
157.           channel: "sms",
158.           enabled: true,
159.         },
160.         existingPreferences: [],
161.         loanState,
162.       });
163. 
164.       const reason = normalizeText(result.reason);
165. 
166.       expect(result.allowed).toBe(false);
167.       expect(reason).toContain("legal-218");
168.       expect(reason).toContain("decline");
169.       expect(reason).toContain("sms");
170.     },
171.   );
172. 
173.   it("allows enabling decline sms for non-California loan state", () => {
174.     const result = validateNotificationPreferenceWrite({
175.       nextPreference: {
176.         event: "decline",
177.         channel: "sms",
178.         enabled: true,
179.       },
180.       existingPreferences: [],
181.       loanState: "NV",
182.     });
183. 
184.     expect(result.allowed).toBe(true);
185.   });
186. });
187. 
188. describe("PUT /preferences route hardening", () => {
189.   it("returns 400 with escalation invariant details when the write would disable the last channel", () => {
190.     const handler = getPutPreferencesHandler();
191.     const response = createResponse();
192. 
193.     preferenceRepoMock.findPreference.mockReturnValue(
194.       buildPreference({ event: "manual-review-escalation", channel: "email" }),
195.     );
196.     preferenceRepoMock.findPreferencesForUser.mockReturnValue([
197.       buildPreference({ event: "manual-review-escalation", channel: "email" }),
198.       buildPreference({
199.         event: "manual-review-escalation",
200.         channel: "sms",
201.         enabled: false,
202.       }),
203.     ]);
204. 
205.     handler(
206.       {
207.         body: {
208.           userId: "user-1",
209.           event: "manual-review-escalation",
210.           channel: "email",
211.           enabled: false,
212.           loanState: "NY",
213.         },
214.         session: {
215.           actor: {
216.             id: "user-1",
217.             role: "underwriter",
218.             name: "User One",
219.             email: "user-1@example.com",
220.           },
221.         },
222.       },
223.       response,
224.       vi.fn(),
225.     );
226. 
227.     const payload = response.body as { error?: string; details?: string[] };
228.     const details = normalizeText(payload.details?.join(" "));
229. 
230.     expect(response.statusCode).toBe(400);
231.     expect(payload.error).toBe("Validation failed.");
232.     expect(details).toContain("manual-review-escalation");
233.     expect(details).toContain("at least one");
234.     expect(preferenceRepoMock.setPreference).not.toHaveBeenCalled();
235.     expect(auditServiceMock.auditAction).not.toHaveBeenCalled();
236.   });
237. 
238.   it("returns 400 with LEGAL-218 details when California decline sms is enabled", () => {
239.     const handler = getPutPreferencesHandler();
240.     const response = createResponse();
241. 
242.     preferenceRepoMock.findPreference.mockReturnValue(
243.       buildPreference({
244.         event: "decline",
245.         channel: "sms",
246.         enabled: false,
247.       }),
248.     );
249.     preferenceRepoMock.findPreferencesForUser.mockReturnValue([]);
250. 
251.     handler(
252.       {
253.         body: {
254.           userId: "user-1",
255.           event: "decline",
256.           channel: "sms",
257.           enabled: true,
258.           loanState: "California",
259.         },
260.         session: {
261.           actor: {
262.             id: "user-1",
263.             role: "underwriter",
264.             name: "User One",
265.             email: "user-1@example.com",
266.           },
267.         },
268.       },
269.       response,
270.       vi.fn(),
271.     );
272. 
273.     const payload = response.body as { details?: string[] };
274.     const details = normalizeText(payload.details?.join(" "));
275. 
276.     expect(response.statusCode).toBe(400);
277.     expect(details).toContain("legal-218");
278.     expect(details).toContain("decline");
279.     expect(details).toContain("sms");
280.     expect(preferenceRepoMock.setPreference).not.toHaveBeenCalled();
281.   });
282. 
283.   it("allows disabling escalation sms when escalation email stays enabled", () => {
284.     const handler = getPutPreferencesHandler();
285.     const response = createResponse();
286. 
287.     preferenceRepoMock.findPreference.mockReturnValue(
288.       buildPreference({
289.         event: "manual-review-escalation",
290.         channel: "sms",
291.         enabled: true,
292.       }),
293.     );
294.     preferenceRepoMock.findPreferencesForUser.mockReturnValue([
295.       buildPreference({ event: "manual-review-escalation", channel: "email" }),
296.       buildPreference({
297.         event: "manual-review-escalation",
298.         channel: "sms",
299.         enabled: true,
300.       }),
301.     ]);
302. 
303.     handler(
304.       {
305.         body: {
306.           userId: "user-1",
307.           event: "manual-review-escalation",
308.           channel: "sms",
309.           enabled: false,
310.           loanState: "NY",
311.         },
312.         session: {
313.           actor: {
314.             id: "user-1",
315.             role: "underwriter",
316.             name: "User One",
317.             email: "user-1@example.com",
318.           },
319.         },
320.       },
321.       response,
322.       vi.fn(),
323.     );
324. 
325.     expect(response.statusCode).toBe(200);
326.     expect(preferenceRepoMock.setPreference).toHaveBeenCalledTimes(1);
327.     expect(auditServiceMock.auditAction).toHaveBeenCalledTimes(1);
328.   });
329. });
330.
```

</details>


---

<sub>⏱️ 5m 30s</sub>

### 💬 Copilot

I found one small thing worth tightening before I stop: the test helper can be simpler and less type-fragile without changing behavior, so I’m cleaning that up.

---

<sub>⏱️ 5m 30s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Update File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows\\src\\backend\\tests\\unit\\notification-preference-write-rules.test.ts\n@@\n function normalizeText(value: unknown): string {\n   return String(value).toLowerCase().replace(/\\s+/g, \" \").trim();\n }\n \n-function getPutPreferencesHandler(): (\n+type RouteHandler = (\n   req: Record<string, unknown>,\n   res: {\n     status: (code: number) => unknown;\n     json: (payload: unknown) => unknown;\n   },\n   next: (error?: unknown) => void,\n-) => void {\n+) => void;\n+\n+function getPutPreferencesHandler(): RouteHandler {\n   const routeLayer = (notificationRoutes as {\n     stack: Array<{\n       route?: {\n         path: string;\n         methods: Record<string, boolean>;\n@@\n   if (!routeLayer?.route) {\n     throw new Error(\"PUT /preferences route not found.\");\n   }\n \n-  return routeLayer.route.stack[routeLayer.route.stack.length - 1]\n-    .handle as typeof getPutPreferencesHandler extends () => infer T ? T : never;\n+  return routeLayer.route.stack[routeLayer.route.stack.length - 1]\n+    .handle as RouteHandler;\n }\n*** End Patch\n"
```

</details>

```
Modified 1 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts
```


---

<sub>⏱️ 5m 35s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Update File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows\\src\\backend\\src\\routes\\notifications.ts\n@@\n import { Router } from \"express\";\n import { requireRole } from \"../middleware/auth.js\";\n import { validateBody } from \"../middleware/request-validator.js\";\n-import { validateNotificationPreferenceWrite } from \"../rules/notification-preference-write-rules.js\";\n+import { validateNotificationPreferenceWrite } from \"../rules/notification-preference-write-rules.js\";\n*** End Patch\n"
```

</details>

```
Modified 1 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts
```


---

<sub>⏱️ 5m 44s</sub>

### 💬 Copilot

The slice is implemented. I’m doing one last targeted read of the test helper and rule/route contract together so the handoff reflects the actual changed surface and the intentionally deferred ones.

---

<sub>⏱️ 5m 44s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts (lines 44-120)

<details>
<summary>77 lines</summary>

```
44. function normalizeText(value: unknown): string {
45.   return String(value).toLowerCase().replace(/\s+/g, " ").trim();
46. }
47. 
48. type RouteHandler = (
49.   req: Record<string, unknown>,
50.   res: {
51.     status: (code: number) => unknown;
52.     json: (payload: unknown) => unknown;
53.   },
54.   next: (error?: unknown) => void,
55. ) => void;
56. 
57. function getPutPreferencesHandler(): RouteHandler {
58.   const routeLayer = (notificationRoutes as {
59.     stack: Array<{
60.       route?: {
61.         path: string;
62.         methods: Record<string, boolean>;
63.         stack: Array<{ handle: (...args: unknown[]) => void }>;
64.       };
65.     }>;
66.   }).stack.find(
67.     (layer) => layer.route?.path === "/preferences" && layer.route.methods.put,
68.   );
69. 
70.   if (!routeLayer?.route) {
71.     throw new Error("PUT /preferences route not found.");
72.   }
73. 
74.   return routeLayer.route.stack[routeLayer.route.stack.length - 1]
75.     .handle as RouteHandler;
76. }
77. 
78. function createResponse() {
79.   return {
80.     statusCode: 200,
81.     body: undefined as unknown,
82.     status(code: number) {
83.       this.statusCode = code;
84.       return this;
85.     },
86.     json(payload: unknown) {
87.       this.body = payload;
88.       return this;
89.     },
90.   };
91. }
92. 
93. beforeAll(async () => {
94.   ({ validateNotificationPreferenceWrite } = await import(
95.     "../../src/rules/notification-preference-write-rules.js"
96.   ));
97.   ({ notificationRoutes } = await import("../../src/routes/notifications.js"));
98. });
99. 
100. beforeEach(() => {
101.   vi.clearAllMocks();
102. });
103. 
104. describe("validateNotificationPreferenceWrite", () => {
105.   it("allows disabling escalation sms when escalation email remains enabled", () => {
106.     // FALSE POSITIVE: SMS can be disabled when email still preserves the mandatory event.
107.     const result = validateNotificationPreferenceWrite({
108.       nextPreference: {
109.         event: "manual-review-escalation",
110.         channel: "sms",
111.         enabled: false,
112.       },
113.       existingPreferences: [
114.         buildPreference({ event: "manual-review-escalation", channel: "email" }),
115.         buildPreference({
116.           event: "manual-review-escalation",
117.           channel: "sms",
118.           enabled: true,
119.         }),
120.       ],
```

</details>


---

<sub>⏱️ 5m 44s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts (lines 188-329)

<details>
<summary>142 lines</summary>

```
188. });
189. 
190. describe("PUT /preferences route hardening", () => {
191.   it("returns 400 with escalation invariant details when the write would disable the last channel", () => {
192.     const handler = getPutPreferencesHandler();
193.     const response = createResponse();
194. 
195.     preferenceRepoMock.findPreference.mockReturnValue(
196.       buildPreference({ event: "manual-review-escalation", channel: "email" }),
197.     );
198.     preferenceRepoMock.findPreferencesForUser.mockReturnValue([
199.       buildPreference({ event: "manual-review-escalation", channel: "email" }),
200.       buildPreference({
201.         event: "manual-review-escalation",
202.         channel: "sms",
203.         enabled: false,
204.       }),
205.     ]);
206. 
207.     handler(
208.       {
209.         body: {
210.           userId: "user-1",
211.           event: "manual-review-escalation",
212.           channel: "email",
213.           enabled: false,
214.           loanState: "NY",
215.         },
216.         session: {
217.           actor: {
218.             id: "user-1",
219.             role: "underwriter",
220.             name: "User One",
221.             email: "user-1@example.com",
222.           },
223.         },
224.       },
225.       response,
226.       vi.fn(),
227.     );
228. 
229.     const payload = response.body as { error?: string; details?: string[] };
230.     const details = normalizeText(payload.details?.join(" "));
231. 
232.     expect(response.statusCode).toBe(400);
233.     expect(payload.error).toBe("Validation failed.");
234.     expect(details).toContain("manual-review-escalation");
235.     expect(details).toContain("at least one");
236.     expect(preferenceRepoMock.setPreference).not.toHaveBeenCalled();
237.     expect(auditServiceMock.auditAction).not.toHaveBeenCalled();
238.   });
239. 
240.   it("returns 400 with LEGAL-218 details when California decline sms is enabled", () => {
241.     const handler = getPutPreferencesHandler();
242.     const response = createResponse();
243. 
244.     preferenceRepoMock.findPreference.mockReturnValue(
245.       buildPreference({
246.         event: "decline",
247.         channel: "sms",
248.         enabled: false,
249.       }),
250.     );
251.     preferenceRepoMock.findPreferencesForUser.mockReturnValue([]);
252. 
253.     handler(
254.       {
255.         body: {
256.           userId: "user-1",
257.           event: "decline",
258.           channel: "sms",
259.           enabled: true,
260.           loanState: "California",
261.         },
262.         session: {
263.           actor: {
264.             id: "user-1",
265.             role: "underwriter",
266.             name: "User One",
267.             email: "user-1@example.com",
268.           },
269.         },
270.       },
271.       response,
272.       vi.fn(),
273.     );
274. 
275.     const payload = response.body as { details?: string[] };
276.     const details = normalizeText(payload.details?.join(" "));
277. 
278.     expect(response.statusCode).toBe(400);
279.     expect(details).toContain("legal-218");
280.     expect(details).toContain("decline");
281.     expect(details).toContain("sms");
282.     expect(preferenceRepoMock.setPreference).not.toHaveBeenCalled();
283.   });
284. 
285.   it("allows disabling escalation sms when escalation email stays enabled", () => {
286.     const handler = getPutPreferencesHandler();
287.     const response = createResponse();
288. 
289.     preferenceRepoMock.findPreference.mockReturnValue(
290.       buildPreference({
291.         event: "manual-review-escalation",
292.         channel: "sms",
293.         enabled: true,
294.       }),
295.     );
296.     preferenceRepoMock.findPreferencesForUser.mockReturnValue([
297.       buildPreference({ event: "manual-review-escalation", channel: "email" }),
298.       buildPreference({
299.         event: "manual-review-escalation",
300.         channel: "sms",
301.         enabled: true,
302.       }),
303.     ]);
304. 
305.     handler(
306.       {
307.         body: {
308.           userId: "user-1",
309.           event: "manual-review-escalation",
310.           channel: "sms",
311.           enabled: false,
312.           loanState: "NY",
313.         },
314.         session: {
315.           actor: {
316.             id: "user-1",
317.             role: "underwriter",
318.             name: "User One",
319.             email: "user-1@example.com",
320.           },
321.         },
322.       },
323.       response,
324.       vi.fn(),
325.     );
326. 
327.     expect(response.statusCode).toBe(200);
328.     expect(preferenceRepoMock.setPreference).toHaveBeenCalledTimes(1);
329.     expect(auditServiceMock.auditAction).toHaveBeenCalledTimes(1);
```

</details>


---

<sub>⏱️ 5m 44s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\notification-preference-write-rules.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\notification-preference-write-rules.ts (lines 1-120)

<details>
<summary>87 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Notification Preference Write Rules
3. // ---------------------------------------------------------------------------
4. // FALSE POSITIVE: disabling manual-review-escalation SMS is allowed when email
5. // remains enabled. The invariant is "at least one channel", not "all channels".
6. //
7. // HARD NEGATIVE: rejecting only a specific channel toggle is insufficient if
8. // the write would leave manual-review-escalation with zero enabled channels.
9. //
10. // LEGAL-218: decline SMS cannot be enabled for California loan contexts.
11. // ---------------------------------------------------------------------------
12. 
13. import type {
14.   NotificationChannel,
15.   NotificationPreference,
16. } from "../models/types.js";
17. 
18. export interface NotificationPreferenceWriteInput {
19.   nextPreference: Pick<NotificationPreference, "event" | "channel" | "enabled">;
20.   existingPreferences: NotificationPreference[];
21.   loanState: string;
22. }
23. 
24. export interface NotificationPreferenceWriteRule {
25.   allowed: boolean;
26.   reason: string;
27. }
28. 
29. const ALLOWED_WRITE: NotificationPreferenceWriteRule = {
30.   allowed: true,
31.   reason: "Notification preference write allowed.",
32. };
33. 
34. export function validateNotificationPreferenceWrite(
35.   input: NotificationPreferenceWriteInput,
36. ): NotificationPreferenceWriteRule {
37.   const { nextPreference, existingPreferences, loanState } = input;
38. 
39.   if (
40.     nextPreference.event === "decline" &&
41.     nextPreference.channel === "sms" &&
42.     nextPreference.enabled &&
43.     isCaliforniaLoanState(loanState)
44.   ) {
45.     return {
46.       allowed: false,
47.       reason:
48.         "LEGAL-218: decline SMS cannot be enabled for California loanState.",
49.     };
50.   }
51. 
52.   if (
53.     nextPreference.event !== "manual-review-escalation" ||
54.     nextPreference.enabled
55.   ) {
56.     return ALLOWED_WRITE;
57.   }
58. 
59.   const otherChannel = otherNotificationChannel(nextPreference.channel);
60.   const otherPreference = existingPreferences.find(
61.     (preference) =>
62.       preference.event === "manual-review-escalation" &&
63.       preference.channel === otherChannel,
64.   );
65. 
66.   if (otherPreference?.enabled === false) {
67.     return {
68.       allowed: false,
69.       reason:
70.         "manual-review-escalation must keep at least one channel enabled.",
71.     };
72.   }
73. 
74.   return ALLOWED_WRITE;
75. }
76. 
77. function otherNotificationChannel(
78.   channel: NotificationChannel,
79. ): NotificationChannel {
80.   return channel === "email" ? "sms" : "email";
81. }
82. 
83. function isCaliforniaLoanState(loanState: string): boolean {
84.   const normalized = loanState.trim().toLowerCase();
85.   return normalized === "ca" || normalized === "california";
86. }
87.
```

</details>


---

<sub>⏱️ 5m 44s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts (lines 46-118)

<details>
<summary>73 lines</summary>

```
46. /** PUT /api/notifications/preferences — set a notification preference. */
47. notificationRoutes.put(
48.   "/preferences",
49.   requireRole("underwriter", "analyst-manager"),
50.   validateBody([
51.     { field: "userId", type: "string", required: true },
52.     { field: "event", type: "string", required: true },
53.     { field: "channel", type: "string", required: true },
54.     { field: "enabled", type: "boolean", required: true },
55.     { field: "loanState", type: "string", required: true },
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
80.       const writeRule = validateNotificationPreferenceWrite({
81.         nextPreference: { event, channel, enabled },
82.         existingPreferences,
83.         loanState,
84.       });
85. 
86.       if (!writeRule.allowed) {
87.         res.status(400).json({
88.           error: "Validation failed.",
89.           details: [writeRule.reason],
90.         });
91.         return;
92.       }
93. 
94.       const previous = prefRepo.findPreference(userId, event, channel);
95. 
96.       const pref: NotificationPreference = {
97.         userId,
98.         event,
99.         channel,
100.         enabled,
101.         updatedAt: now,
102.         updatedBy: session.actor.id,
103.       };
104. 
105.       prefRepo.setPreference(pref);
106. 
107.       // Audit the preference change
108.       auditAction(
109.         session,
110.         "preference.updated",
111.         previous ?? null,
112.         pref,
113.         "notification-routes",
114.       );
115. 
116.       res.json(pref);
117.     } catch (err) {
118.       next(err);
```

</details>


---

<sub>⏱️ 6m 4s</sub>

### 💬 Copilot

Implemented the focused hardening slice in `src/backend/tests/unit/notification-preference-write-rules.test.ts`, `src/backend/src/rules/notification-preference-write-rules.ts`, and `src/backend/src/routes/notifications.ts`. `PUT /preferences` now requires direct `loanState` input, runs a pure write-rule check before persisting, rejects invariant violations with the existing simple `400`/`Validation failed.` style plus semantic `details`, and preserves the existing delegated-session and role guards.

Before the production change, the new tests for **rejecting the last enabled `manual-review-escalation` channel** and **rejecting California/`CA` decline SMS enablement under `LEGAL-218`** should fail because the route would accept and persist those writes. After the change, those rejection tests should pass, and the false-positive case **disabling escalation SMS while escalation email stays enabled** should also pass as allowed. Deferred write surfaces still out of scope: `PUT /preferences/:userId/email` and `PUT /preferences/:userId/sms`.

---

<sub>Generated by [GitHub Copilot CLI](https://github.com/features/copilot/cli)</sub>
