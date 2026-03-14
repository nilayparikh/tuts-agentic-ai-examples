# 🤖 Copilot CLI Session

> [!NOTE]
> - **Session ID:** `75425311-a9e8-4f75-b5b5-33ca70c55d25`  
> - **Started:** 14/03/2026, 20:28:50  
> - **Duration:** 2m 30s  
> - **Exported:** 14/03/2026, 20:31:21  

---

<sub>⏱️ 6s</sub>

### 👤 User

Inspect docs/, specs/, and the relevant notification-preference write surfaces you discover in this lesson before editing. Use the playbook and example doc as success criteria, not as a fixed file checklist. Implement a focused notification-preference write hardening slice. Write tests first at src/backend/tests/unit/notification-preference-write-rules.test.ts, then add a pure rule module at src/backend/src/rules/notification-preference-write-rules.ts, and wire the minimal production changes into src/backend/src/routes/notifications.ts. In the final handoff, state which behaviors the tests should fail on before the production change and which should pass after it, and name any intentionally deferred write surfaces that remain out of scope. The rule must use explicit inputs plus existing types, not direct DB access. Enforce these cases: manual-review-escalation must keep at least one channel enabled; decline SMS cannot be enabled when loanState is CA or California under LEGAL-218; the false positive where escalation SMS is disabled but escalation email stays enabled must remain allowed. Preserve delegated-session and role guards, keep changes minimal, keep the scope to the current notification write path, include top-of-module false-positive and hard-negative comments in the new rule file, and do not edit protected config or database files. Do not run npm install, npm test, npx vitest, or any shell commands. Do not use SQL or task/todo write tools. Inspect and edit files only. Return a short handoff summary naming changed files and which tests should pass.

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

<sub>⏱️ 20s</sub>

### 💬 Copilot

I’m tracing the lesson docs/specs and current notification write path first, then I’ll do the TDD slice with minimal route wiring.

---

<sub>⏱️ 20s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows**

"docs\**\*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows

```
No files matched the pattern.
```


---

<sub>⏱️ 20s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows**

"specs\**\*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows

```
No files matched the pattern.
```


---

<sub>⏱️ 20s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "notification",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\05-implementation-workflows\\src",
  "glob": "**/*.{ts,tsx,md}",
  "output_mode": "files_with_matches",
  "head_limit": 50
}
```

</details>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\notification-service.test.ts
```


---

<sub>⏱️ 20s</sub>

### ❌ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\specs\product-spec-notification-preferences.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\specs\product-spec-notification-preferences.md

```
Path does not exist
```


---

<sub>⏱️ 20s</sub>

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

<sub>⏱️ 29s</sub>

### 💬 Copilot

The lesson’s spec file name differs from the playbook example, so I’m locating the actual docs and current route/types before drafting the failing tests.

---

<sub>⏱️ 29s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\docs.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\docs

```
implementation-playbook.md
implementation-workflow-example.md
```


---

<sub>⏱️ 29s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\specs.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\specs

```
non-functional-requirements.md
```


---

<sub>⏱️ 29s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\docs**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "notification|preference|LEGAL-218|manual-review-escalation|decline",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\05-implementation-workflows\\docs",
  "glob": "**/*.md",
  "output_mode": "content",
  "-n": true,
  "head_limit": 200
}
```

</details>

<details>
<summary>12 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\docs\implementation-workflow-example.md:7:Show that a constrained implementation workflow can make a focused production change with matching tests instead of attempting the entire notification-preferences feature at once.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\docs\implementation-workflow-example.md:15:3. One targeted wiring change to `src/backend/src/routes/notifications.ts`
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\docs\implementation-workflow-example.md:23:4. The implementation must cover a mandatory-event rule and the California `LEGAL-218` restriction.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\docs\implementation-workflow-example.md:29:10. The workflow should discover the current notification-preference write surfaces before editing and make the chosen slice boundary explicit.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\docs\implementation-workflow-example.md:33:Harden notification preference writes so the existing route cannot:
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\docs\implementation-workflow-example.md:35:- disable the last available channel for `manual-review-escalation`
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\docs\implementation-workflow-example.md:36:- enable decline SMS for California loan context
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\docs\implementation-workflow-example.md:40:It should also make the intentional scope boundary visible: this lesson is about hardening the current notification write path, not implementing every preference mutation surface in the repository at once.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\docs\implementation-workflow-example.md:42:Good output should explicitly name the deferred write surfaces in the handoff instead of silently implying that the whole notification-preferences domain is now complete.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\docs\implementation-playbook.md:37:3. Document the legal or business source in a comment (e.g., `// LEGAL-218`).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\docs\implementation-playbook.md:44:3. Degrade gracefully for non-critical operations (notification delivery).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\docs\implementation-playbook.md:45:4. Never modify stored user preferences as a side effect of delivery.
```

</details>


---

<sub>⏱️ 29s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\specs**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "notification|preference|LEGAL-218|manual-review-escalation|decline",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\05-implementation-workflows\\specs",
  "glob": "**/*.md",
  "output_mode": "content",
  "-n": true,
  "head_limit": 200
}
```

</details>

<details>
<summary>10 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\specs\non-functional-requirements.md:29:is unavailable. The fallback must NOT modify stored user preferences.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\specs\non-functional-requirements.md:32:user's stored channel preference from SMS to email "for consistency."
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\specs\non-functional-requirements.md:34:> **FALSE POSITIVE**: AI flags the inconsistency between stored preference (SMS)
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\specs\non-functional-requirements.md:36:> but preferences don't change.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\specs\non-functional-requirements.md:38:**Test signal**: After a degraded delivery, GET /preferences should still show
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\specs\non-functional-requirements.md:39:the original SMS preference.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\specs\non-functional-requirements.md:49:every preference save, doubling latency. Delivery is async by design.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\specs\non-functional-requirements.md:92:`notificationChannels` for "clarity." All existing clients break.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\specs\non-functional-requirements.md:95:> changes (adding `notificationChannels` alongside `channels`) are safe.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\specs\non-functional-requirements.md:104:**AI mistake without context**: AI uses `console.log(\`User ${userId} saved preferences\`)`
```

</details>


---

<sub>⏱️ 29s</sub>

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

<sub>⏱️ 29s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "type Notification|interface Notification|loanState|NotificationPreference|NotificationEvent|NotificationChannel|Preference",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\05-implementation-workflows\\src\\backend\\src",
  "glob": "**/*.ts",
  "output_mode": "content",
  "-n": true,
  "head_limit": 200
}
```

</details>

<details>
<summary>60 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\db\seed.ts:111:    // ── Notification Preferences ──
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\services\notification-service.ts:24:  NotificationEvent,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\services\notification-service.ts:25:  NotificationChannel,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\services\notification-service.ts:34:  event: NotificationEvent,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\services\notification-service.ts:37:  preferredChannel: NotificationChannel = "email",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\services\loan-service.ts:31:  data: { borrowerName: string; amount: number; loanState: string },
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\services\loan-service.ts:40:    loanState: data.loanState.toUpperCase(),
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\services\loan-service.ts:52:    loanState: data.loanState,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\queue\handlers\notification-handler.ts:16:import { findPreferencesForUser } from "../../models/preference-repository.js";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\queue\handlers\notification-handler.ts:44:  const prefs = findPreferencesForUser(userId);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\queue\contracts.ts:19:  NotificationEvent,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\queue\contracts.ts:20:  NotificationChannel,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\queue\contracts.ts:31:export interface NotificationRequestedEvent extends BaseEvent {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\queue\contracts.ts:35:    event: NotificationEvent;
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\queue\contracts.ts:38:    preferredChannel: NotificationChannel;
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\rules\mandatory-events.ts:12:import type { ApplicationState, NotificationEvent } from "../models/types.js";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\rules\mandatory-events.ts:21:  Record<TransitionKey, NotificationEvent[]>
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\rules\mandatory-events.ts:34:): NotificationEvent[] {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\loan-repository.ts:19:  loan_state AS loanState,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\loan-repository.ts:66:  loanState: string;
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\loan-repository.ts:80:    data.loanState.toUpperCase(),
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\rules\business-rules.ts:46:  if (featureFlags.californiaRules && loan.loanState === "CA") {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\types.ts:38:export type NotificationEvent =
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\types.ts:45:export type NotificationChannel = "email" | "sms";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\types.ts:75:  loanState: string;
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\types.ts:93:export interface NotificationPreference {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\types.ts:95:  event: NotificationEvent;
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\types.ts:96:  channel: NotificationChannel;
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:2:// Notification Preference Repository
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:7://   The `setPreference` function uses INSERT OR REPLACE on the composite
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:15:  NotificationPreference,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:16:  NotificationEvent,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:17:  NotificationChannel,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:29:type PreferenceRow = NotificationPreference & { enabled: number | boolean };
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:31:export function findPreferencesForUser(
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:33:): NotificationPreference[] {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:40:    .map((pref) => pref as PreferenceRow)
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:44:    })) as NotificationPreference[];
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:47:export function findPreference(
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:49:  event: NotificationEvent,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:50:  channel: NotificationChannel,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:51:): NotificationPreference | undefined {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:58:    | (NotificationPreference & { enabled: number | boolean })
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:64:export function setPreference(pref: NotificationPreference): void {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:79:export function deletePreferencesForUser(userId: string): number {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\applications.ts:56:    { field: "loanState", type: "string", required: true },
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:2:// Notification Preference Routes
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:24:  NotificationPreference,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:38:    const prefs = prefRepo.findPreferencesForUser(
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:78:      const previous = prefRepo.findPreference(userId, event, channel);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:80:      const pref: NotificationPreference = {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:89:      prefRepo.setPreference(pref);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:156:      const updates: NotificationPreference[] = [];
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:159:        const previous = prefRepo.findPreference(targetUserId, event, "email");
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:161:        const pref: NotificationPreference = {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:170:        prefRepo.setPreference(pref);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:239:      const updates: NotificationPreference[] = [];
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:242:        const previous = prefRepo.findPreference(targetUserId, event, "sms");
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:244:        const pref: NotificationPreference = {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:253:        prefRepo.setPreference(pref);
```

</details>


---

<sub>⏱️ 42s</sub>

### 💬 Copilot

I’ve found the current write surfaces: the single-route write plus bulk email/sms routes. I’m keeping this slice scoped to the single `PUT /preferences` path and reading the local example/playbook plus test conventions before writing the red tests.

---

<sub>⏱️ 42s</sub>

### ❌ `view`

**view the file at C:\Users\nilay\.copilot\session-state\75425311-a9e8-4f75-b5b5-33ca70c55d25\plan.md.**

C:\Users\nilay\.copilot\session-state\75425311-a9e8-4f75-b5b5-33ca70c55d25\plan.md

```
Path does not exist
```


---

<sub>⏱️ 42s</sub>

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

<sub>⏱️ 42s</sub>

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

<sub>⏱️ 42s</sub>

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

<sub>⏱️ 42s</sub>

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

<sub>⏱️ 42s</sub>

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

<sub>⏱️ 42s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "describe\\(|it\\(",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\05-implementation-workflows\\src\\backend\\tests\\unit",
  "glob": "**/*.test.ts",
  "output_mode": "files_with_matches",
  "head_limit": 50
}
```

</details>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\notification-service.test.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts
```


---

<sub>⏱️ 48s</sub>

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

<sub>⏱️ 48s</sub>

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

<sub>⏱️ 48s</sub>

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

<sub>⏱️ 1m 11s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Add File: C:\\Users\\nilay\\.copilot\\session-state\\75425311-a9e8-4f75-b5b5-33ca70c55d25\\plan.md\n+# Plan\n+\n+1. Inspect lesson docs, specs, current notification-preference write surfaces, and domain types.\n+2. Add failing unit tests for the focused notification-preference write hardening slice.\n+3. Implement a pure notification-preference write rule module with explicit inputs and annotated edge-case comments.\n+4. Wire the current `PUT /api/notifications/preferences` route to the new rule with minimal production changes.\n+5. Review the changed files against the documented scope boundary and hand off expected red/green behavior.\n*** End Patch\n"
```

</details>

```
Added 1 file(s): C:\Users\nilay\.copilot\session-state\75425311-a9e8-4f75-b5b5-33ca70c55d25\plan.md
```


---

<sub>⏱️ 1m 34s</sub>

### 💬 Copilot

I’ve got the rule shape pinned down, so I’m laying down the red tests against a pure evaluator before touching production code.

---

<sub>⏱️ 1m 34s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Add File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\05-implementation-workflows\\src\\backend\\tests\\unit\\notification-preference-write-rules.test.ts\n+import { describe, expect, it } from \"vitest\";\n+\n+import type { NotificationPreference } from \"../../src/models/types.js\";\n+import { evaluateNotificationPreferenceWrite } from \"../../src/rules/notification-preference-write-rules.js\";\n+\n+const basePreference: NotificationPreference = {\n+  userId: \"uw-1\",\n+  event: \"approval\",\n+  channel: \"email\",\n+  enabled: true,\n+  updatedAt: \"2026-03-14T00:00:00.000Z\",\n+  updatedBy: \"uw-1\",\n+};\n+\n+function makePreference(\n+  overrides: Partial<NotificationPreference>,\n+): NotificationPreference {\n+  return {\n+    ...basePreference,\n+    ...overrides,\n+  };\n+}\n+\n+describe(\"Notification Preference Write Rules\", () => {\n+  it(\"allows disabling escalation SMS when escalation email remains enabled\", () => {\n+    // FALSE POSITIVE: disabling one channel is allowed when the other channel stays enabled.\n+    expect(\n+      evaluateNotificationPreferenceWrite({\n+        existingPreferences: [\n+          makePreference({\n+            event: \"manual-review-escalation\",\n+            channel: \"email\",\n+            enabled: true,\n+          }),\n+          makePreference({\n+            event: \"manual-review-escalation\",\n+            channel: \"sms\",\n+            enabled: true,\n+          }),\n+        ],\n+        nextPreference: makePreference({\n+          event: \"manual-review-escalation\",\n+          channel: \"sms\",\n+          enabled: false,\n+        }),\n+      }),\n+    ).toEqual({ allowed: true });\n+  });\n+\n+  it(\"rejects disabling the last enabled escalation channel\", () => {\n+    // HARD NEGATIVE: a mandatory escalation event cannot end up with no enabled channels.\n+    expect(\n+      evaluateNotificationPreferenceWrite({\n+        existingPreferences: [\n+          makePreference({\n+            event: \"manual-review-escalation\",\n+            channel: \"email\",\n+            enabled: true,\n+          }),\n+          makePreference({\n+            event: \"manual-review-escalation\",\n+            channel: \"sms\",\n+            enabled: false,\n+          }),\n+        ],\n+        nextPreference: makePreference({\n+          event: \"manual-review-escalation\",\n+          channel: \"email\",\n+          enabled: false,\n+        }),\n+      }),\n+    ).toEqual({\n+      allowed: false,\n+      reason:\n+        \"manual-review-escalation must keep at least one notification channel enabled.\",\n+    });\n+  });\n+\n+  it(\"rejects enabling decline SMS for CA loans\", () => {\n+    expect(\n+      evaluateNotificationPreferenceWrite({\n+        existingPreferences: [],\n+        nextPreference: makePreference({\n+          event: \"decline\",\n+          channel: \"sms\",\n+          enabled: true,\n+        }),\n+        loanState: \"CA\",\n+      }),\n+    ).toEqual({\n+      allowed: false,\n+      reason:\n+        \"LEGAL-218: decline SMS cannot be enabled for California loans.\",\n+    });\n+  });\n+\n+  it(\"rejects enabling decline SMS for California loans spelled out\", () => {\n+    expect(\n+      evaluateNotificationPreferenceWrite({\n+        existingPreferences: [],\n+        nextPreference: makePreference({\n+          event: \"decline\",\n+          channel: \"sms\",\n+          enabled: true,\n+        }),\n+        loanState: \"California\",\n+      }),\n+    ).toEqual({\n+      allowed: false,\n+      reason:\n+        \"LEGAL-218: decline SMS cannot be enabled for California loans.\",\n+    });\n+  });\n+\n+  it(\"allows decline SMS outside California\", () => {\n+    expect(\n+      evaluateNotificationPreferenceWrite({\n+        existingPreferences: [],\n+        nextPreference: makePreference({\n+          event: \"decline\",\n+          channel: \"sms\",\n+          enabled: true,\n+        }),\n+        loanState: \"NY\",\n+      }),\n+    ).toEqual({ allowed: true });\n+  });\n+});\n*** End Patch\n"
```

</details>

```
Added 1 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts
```


---

<sub>⏱️ 1m 46s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Add File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\05-implementation-workflows\\src\\backend\\src\\rules\\notification-preference-write-rules.ts\n+import type {\n+  NotificationEvent,\n+  NotificationPreference,\n+} from \"../models/types.js\";\n+import { getMandatoryEvents } from \"./mandatory-events.js\";\n+\n+// FALSE POSITIVE: disabling escalation SMS is still allowed when escalation email\n+// remains enabled. The write is only invalid when the event would lose every channel.\n+// HARD NEGATIVE: manual-review-escalation is a mandatory event, so writes must fail\n+// closed if they would leave that event with no enabled delivery channel at all.\n+\n+export interface NotificationPreferenceWriteInput {\n+  existingPreferences: NotificationPreference[];\n+  nextPreference: NotificationPreference;\n+  loanState?: string;\n+}\n+\n+export type NotificationPreferenceWriteDecision =\n+  | { allowed: true }\n+  | { allowed: false; reason: string };\n+\n+const MANDATORY_WRITE_GUARDED_EVENTS = new Set<NotificationEvent>(\n+  getMandatoryEvents(\"underwriting\", \"decision\"),\n+);\n+\n+function preferenceKey(pref: NotificationPreference): string {\n+  return `${pref.event}:${pref.channel}`;\n+}\n+\n+function mergePreference(\n+  existingPreferences: NotificationPreference[],\n+  nextPreference: NotificationPreference,\n+): NotificationPreference[] {\n+  const preferencesByKey = new Map<string, NotificationPreference>();\n+\n+  for (const pref of existingPreferences) {\n+    preferencesByKey.set(preferenceKey(pref), pref);\n+  }\n+\n+  preferencesByKey.set(preferenceKey(nextPreference), nextPreference);\n+\n+  return [...preferencesByKey.values()];\n+}\n+\n+function normalizeLoanState(loanState?: string): string | undefined {\n+  return loanState?.trim().toUpperCase();\n+}\n+\n+function keepsMandatoryEventDeliverable(\n+  preferences: NotificationPreference[],\n+  event: NotificationEvent,\n+): boolean {\n+  return preferences.some((pref) => pref.event === event && pref.enabled);\n+}\n+\n+export function evaluateNotificationPreferenceWrite(\n+  input: NotificationPreferenceWriteInput,\n+): NotificationPreferenceWriteDecision {\n+  const { existingPreferences, nextPreference, loanState } = input;\n+  const effectivePreferences = mergePreference(existingPreferences, nextPreference);\n+\n+  if (\n+    MANDATORY_WRITE_GUARDED_EVENTS.has(nextPreference.event) &&\n+    !keepsMandatoryEventDeliverable(effectivePreferences, nextPreference.event)\n+  ) {\n+    return {\n+      allowed: false,\n+      reason:\n+        \"manual-review-escalation must keep at least one notification channel enabled.\",\n+    };\n+  }\n+\n+  const normalizedLoanState = normalizeLoanState(loanState);\n+\n+  if (\n+    nextPreference.event === \"decline\" &&\n+    nextPreference.channel === \"sms\" &&\n+    nextPreference.enabled &&\n+    (normalizedLoanState === \"CA\" || normalizedLoanState === \"CALIFORNIA\")\n+  ) {\n+    return {\n+      allowed: false,\n+      // LEGAL-218: California decline notices cannot enable SMS delivery.\n+      reason: \"LEGAL-218: decline SMS cannot be enabled for California loans.\",\n+    };\n+  }\n+\n+  return { allowed: true };\n+}\n*** End Patch\n"
```

</details>

```
Added 1 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\rules\notification-preference-write-rules.ts
```


---

<sub>⏱️ 2m 0s</sub>

### 💬 Copilot

The pure rule is in place; I’m doing the minimal route wire-up now and deciding how to pass explicit `loanState` context without expanding scope into the bulk write endpoints.

---

<sub>⏱️ 2m 0s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "PUT /api/notifications/preferences|setPreference\\(|loanState",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\05-implementation-workflows\\src",
  "glob": "**/*.{ts,tsx}",
  "output_mode": "content",
  "-n": true,
  "head_limit": 200
}
```

</details>

<details>
<summary>6 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts:88:        loanState: "CA",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts:106:        loanState: "California",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts:124:        loanState: "NY",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts:17:  loanState: "NY",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts:39:      loanState: "CA",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts:48:      loanState: "CA",
```

</details>


---

<sub>⏱️ 2m 0s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\frontend**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "preferences\"|/preferences",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\05-implementation-workflows\\src\\frontend",
  "glob": "**/*.{ts,tsx}",
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

<sub>⏱️ 2m 9s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Update File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\05-implementation-workflows\\src\\backend\\src\\routes\\notifications.ts\n@@\n import { validateBody } from \"../middleware/request-validator.js\";\n import { hasPermission } from \"../rules/role-permissions.js\";\n+import { evaluateNotificationPreferenceWrite } from \"../rules/notification-preference-write-rules.js\";\n import { auditAction } from \"../services/audit-service.js\";\n import * as prefRepo from \"../models/preference-repository.js\";\n@@\n   validateBody([\n     { field: \"userId\", type: \"string\", required: true },\n     { field: \"event\", type: \"string\", required: true },\n     { field: \"channel\", type: \"string\", required: true },\n     { field: \"enabled\", type: \"boolean\", required: true },\n+    { field: \"loanState\", type: \"string\" },\n   ]),\n   (req, res, next) => {\n@@\n-      const { userId, event, channel, enabled } = req.body;\n+      const { userId, event, channel, enabled, loanState } = req.body;\n       const now = new Date().toISOString();\n \n       const previous = prefRepo.findPreference(userId, event, channel);\n+      const existingPreferences = prefRepo.findPreferencesForUser(userId);\n \n       const pref: NotificationPreference = {\n         userId,\n@@\n         updatedBy: session.actor.id,\n       };\n \n+      const writeDecision = evaluateNotificationPreferenceWrite({\n+        existingPreferences,\n+        nextPreference: pref,\n+        loanState,\n+      });\n+\n+      if (!writeDecision.allowed) {\n+        res.status(400).json({ error: writeDecision.reason });\n+        return;\n+      }\n+\n       prefRepo.setPreference(pref);\n*** End Patch\n"
```

</details>

```
Modified 1 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts
```


---

<sub>⏱️ 2m 15s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts

<details>
<summary>129 lines</summary>

```
1. import { describe, expect, it } from "vitest";
2. 
3. import type { NotificationPreference } from "../../src/models/types.js";
4. import { evaluateNotificationPreferenceWrite } from "../../src/rules/notification-preference-write-rules.js";
5. 
6. const basePreference: NotificationPreference = {
7.   userId: "uw-1",
8.   event: "approval",
9.   channel: "email",
10.   enabled: true,
11.   updatedAt: "2026-03-14T00:00:00.000Z",
12.   updatedBy: "uw-1",
13. };
14. 
15. function makePreference(
16.   overrides: Partial<NotificationPreference>,
17. ): NotificationPreference {
18.   return {
19.     ...basePreference,
20.     ...overrides,
21.   };
22. }
23. 
24. describe("Notification Preference Write Rules", () => {
25.   it("allows disabling escalation SMS when escalation email remains enabled", () => {
26.     // FALSE POSITIVE: disabling one channel is allowed when the other channel stays enabled.
27.     expect(
28.       evaluateNotificationPreferenceWrite({
29.         existingPreferences: [
30.           makePreference({
31.             event: "manual-review-escalation",
32.             channel: "email",
33.             enabled: true,
34.           }),
35.           makePreference({
36.             event: "manual-review-escalation",
37.             channel: "sms",
38.             enabled: true,
39.           }),
40.         ],
41.         nextPreference: makePreference({
42.           event: "manual-review-escalation",
43.           channel: "sms",
44.           enabled: false,
45.         }),
46.       }),
47.     ).toEqual({ allowed: true });
48.   });
49. 
50.   it("rejects disabling the last enabled escalation channel", () => {
51.     // HARD NEGATIVE: a mandatory escalation event cannot end up with no enabled channels.
52.     expect(
53.       evaluateNotificationPreferenceWrite({
54.         existingPreferences: [
55.           makePreference({
56.             event: "manual-review-escalation",
57.             channel: "email",
58.             enabled: true,
59.           }),
60.           makePreference({
61.             event: "manual-review-escalation",
62.             channel: "sms",
63.             enabled: false,
64.           }),
65.         ],
66.         nextPreference: makePreference({
67.           event: "manual-review-escalation",
68.           channel: "email",
69.           enabled: false,
70.         }),
71.       }),
72.     ).toEqual({
73.       allowed: false,
74.       reason:
75.         "manual-review-escalation must keep at least one notification channel enabled.",
76.     });
77.   });
78. 
79.   it("rejects enabling decline SMS for CA loans", () => {
80.     expect(
81.       evaluateNotificationPreferenceWrite({
82.         existingPreferences: [],
83.         nextPreference: makePreference({
84.           event: "decline",
85.           channel: "sms",
86.           enabled: true,
87.         }),
88.         loanState: "CA",
89.       }),
90.     ).toEqual({
91.       allowed: false,
92.       reason:
93.         "LEGAL-218: decline SMS cannot be enabled for California loans.",
94.     });
95.   });
96. 
97.   it("rejects enabling decline SMS for California loans spelled out", () => {
98.     expect(
99.       evaluateNotificationPreferenceWrite({
100.         existingPreferences: [],
101.         nextPreference: makePreference({
102.           event: "decline",
103.           channel: "sms",
104.           enabled: true,
105.         }),
106.         loanState: "California",
107.       }),
108.     ).toEqual({
109.       allowed: false,
110.       reason:
111.         "LEGAL-218: decline SMS cannot be enabled for California loans.",
112.     });
113.   });
114. 
115.   it("allows decline SMS outside California", () => {
116.     expect(
117.       evaluateNotificationPreferenceWrite({
118.         existingPreferences: [],
119.         nextPreference: makePreference({
120.           event: "decline",
121.           channel: "sms",
122.           enabled: true,
123.         }),
124.         loanState: "NY",
125.       }),
126.     ).toEqual({ allowed: true });
127.   });
128. });
129.
```

</details>


---

<sub>⏱️ 2m 15s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\rules\notification-preference-write-rules.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\rules\notification-preference-write-rules.ts

<details>
<summary>90 lines</summary>

```
1. import type {
2.   NotificationEvent,
3.   NotificationPreference,
4. } from "../models/types.js";
5. import { getMandatoryEvents } from "./mandatory-events.js";
6. 
7. // FALSE POSITIVE: disabling escalation SMS is still allowed when escalation email
8. // remains enabled. The write is only invalid when the event would lose every channel.
9. // HARD NEGATIVE: manual-review-escalation is a mandatory event, so writes must fail
10. // closed if they would leave that event with no enabled delivery channel at all.
11. 
12. export interface NotificationPreferenceWriteInput {
13.   existingPreferences: NotificationPreference[];
14.   nextPreference: NotificationPreference;
15.   loanState?: string;
16. }
17. 
18. export type NotificationPreferenceWriteDecision =
19.   | { allowed: true }
20.   | { allowed: false; reason: string };
21. 
22. const MANDATORY_WRITE_GUARDED_EVENTS = new Set<NotificationEvent>(
23.   getMandatoryEvents("underwriting", "decision"),
24. );
25. 
26. function preferenceKey(pref: NotificationPreference): string {
27.   return `${pref.event}:${pref.channel}`;
28. }
29. 
30. function mergePreference(
31.   existingPreferences: NotificationPreference[],
32.   nextPreference: NotificationPreference,
33. ): NotificationPreference[] {
34.   const preferencesByKey = new Map<string, NotificationPreference>();
35. 
36.   for (const pref of existingPreferences) {
37.     preferencesByKey.set(preferenceKey(pref), pref);
38.   }
39. 
40.   preferencesByKey.set(preferenceKey(nextPreference), nextPreference);
41. 
42.   return [...preferencesByKey.values()];
43. }
44. 
45. function normalizeLoanState(loanState?: string): string | undefined {
46.   return loanState?.trim().toUpperCase();
47. }
48. 
49. function keepsMandatoryEventDeliverable(
50.   preferences: NotificationPreference[],
51.   event: NotificationEvent,
52. ): boolean {
53.   return preferences.some((pref) => pref.event === event && pref.enabled);
54. }
55. 
56. export function evaluateNotificationPreferenceWrite(
57.   input: NotificationPreferenceWriteInput,
58. ): NotificationPreferenceWriteDecision {
59.   const { existingPreferences, nextPreference, loanState } = input;
60.   const effectivePreferences = mergePreference(existingPreferences, nextPreference);
61. 
62.   if (
63.     MANDATORY_WRITE_GUARDED_EVENTS.has(nextPreference.event) &&
64.     !keepsMandatoryEventDeliverable(effectivePreferences, nextPreference.event)
65.   ) {
66.     return {
67.       allowed: false,
68.       reason:
69.         "manual-review-escalation must keep at least one notification channel enabled.",
70.     };
71.   }
72. 
73.   const normalizedLoanState = normalizeLoanState(loanState);
74. 
75.   if (
76.     nextPreference.event === "decline" &&
77.     nextPreference.channel === "sms" &&
78.     nextPreference.enabled &&
79.     (normalizedLoanState === "CA" || normalizedLoanState === "CALIFORNIA")
80.   ) {
81.     return {
82.       allowed: false,
83.       // LEGAL-218: California decline notices cannot enable SMS delivery.
84.       reason: "LEGAL-218: decline SMS cannot be enabled for California loans.",
85.     };
86.   }
87. 
88.   return { allowed: true };
89. }
90.
```

</details>


---

<sub>⏱️ 2m 15s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts (lines 45-120)

<details>
<summary>76 lines</summary>

```
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
79. 
80.       const previous = prefRepo.findPreference(userId, event, channel);
81.       const existingPreferences = prefRepo.findPreferencesForUser(userId);
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
99.         res.status(400).json({ error: writeDecision.reason });
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

<sub>⏱️ 2m 30s</sub>

### 💬 Copilot

Implemented the focused hardening slice in:

- `src/backend/tests/unit/notification-preference-write-rules.test.ts`
- `src/backend/src/rules/notification-preference-write-rules.ts`
- `src/backend/src/routes/notifications.ts`

Before the production change, the new tests should fail on the missing enforcement for:
- blocking the last enabled `manual-review-escalation` channel
- blocking decline SMS enablement for `CA` / `California` under `LEGAL-218`

After the change, these should pass:
- allow disabling escalation SMS when escalation email stays enabled
- reject disabling the last escalation channel
- reject decline SMS enablement for `CA`
- reject decline SMS enablement for `California`
- allow decline SMS outside California

Intentionally deferred: bulk write surfaces `PUT /preferences/:userId/email` and `PUT /preferences/:userId/sms`.

---

<sub>Generated by [GitHub Copilot CLI](https://github.com/features/copilot/cli)</sub>
