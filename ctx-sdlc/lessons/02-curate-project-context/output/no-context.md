# 🤖 Copilot CLI Session

> [!NOTE]
> - **Session ID:** `1b188e77-c100-4c93-be01-63677e2b953f`  
> - **Started:** 12/03/2026, 21:56:05  
> - **Duration:** 1m 52s  
> - **Exported:** 12/03/2026, 21:57:57  

---

<sub>⏱️ 6s</sub>

### 👤 User

Add a route for preference management. Let users save their notification channel preferences (email, SMS) per event type.

---

<sub>⏱️ 12s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context

<details>
<summary>10 lines</summary>

```
default.py
package-lock.json
package.json
README.md
src
tests
tsconfig.json
validate.py
_output
__pycache__
```

</details>


---

<sub>⏱️ 12s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src

<details>
<summary>8 lines</summary>

```
app.ts
config
middleware
models
routes
rules
services
store
```

</details>


---

<sub>⏱️ 15s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\routes.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\routes

```
applications.ts
audit.ts
decisions.ts
notifications.ts
```


---

<sub>⏱️ 15s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\models.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\models

```
types.ts
```


---

<sub>⏱️ 15s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\store.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\store

```
memory-store.ts
```


---

<sub>⏱️ 19s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\models\types.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\models\types.ts

<details>
<summary>136 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Loan Workbench — Domain Types
3. // ---------------------------------------------------------------------------
4. // This file defines the core domain model for the Loan Workbench API.
5. // Business rules, state machines, and authorization logic all depend on these
6. // types. Changes here affect nearly every module in the project.
7. // ---------------------------------------------------------------------------
8. 
9. /** Lifecycle states for a commercial loan application. */
10. export type ApplicationState =
11.   | "intake"
12.   | "review"
13.   | "underwriting"
14.   | "decision"
15.   | "finalized";
16. 
17. /**
18.  * Valid state transitions.
19.  * Transitions not listed here are forbidden — the system must never allow
20.  * a finalized application to move backward.
21.  */
22. export const VALID_TRANSITIONS: Record<ApplicationState, ApplicationState[]> = {
23.   intake: ["review"],
24.   review: ["underwriting", "intake"], // can return to intake for rework
25.   underwriting: ["decision"],
26.   decision: ["finalized", "underwriting"], // can push back to underwriting
27.   finalized: [], // terminal — no transitions allowed
28. };
29. 
30. /** Organizational roles recognized by the Loan Workbench. */
31. export type UserRole =
32.   | "underwriter"
33.   | "analyst-manager"
34.   | "compliance-reviewer";
35. 
36. /** Notification event types that can trigger user-facing alerts. */
37. export type NotificationEvent =
38.   | "approval"
39.   | "decline"
40.   | "document-request"
41.   | "manual-review-escalation";
42. 
43. /** Delivery channels available for notifications. */
44. export type NotificationChannel = "email" | "sms";
45. 
46. // ---------------------------------------------------------------------------
47. // Entity interfaces
48. // ---------------------------------------------------------------------------
49. 
50. export interface User {
51.   id: string;
52.   role: UserRole;
53.   name: string;
54.   email: string;
55.   phone?: string;
56. }
57. 
58. /**
59.  * Session context attached to every authenticated request.
60.  *
61.  * When `delegatedFor` is present the actor is operating on behalf of another
62.  * user. Delegated sessions restrict write operations — see auth middleware.
63.  */
64. export interface SessionContext {
65.   actor: User;
66.   delegatedFor?: User;
67. }
68. 
69. export interface LoanApplication {
70.   id: string;
71.   borrowerName: string;
72.   amount: number;
73.   /** US state / jurisdiction — affects business rules (e.g. California). */
74.   loanState: string;
75.   status: ApplicationState;
76.   assignedUnderwriter: string;
77.   createdAt: Date;
78.   updatedAt: Date;
79. }
80. 
81. export interface NotificationPreference {
82.   userId: string;
83.   event: NotificationEvent;
84.   channel: NotificationChannel;
85.   enabled: boolean;
86.   updatedAt: Date;
87.   updatedBy: string;
88. }
89. 
90. export interface AuditEntry {
91.   id: string;
92.   action: string;
93.   actor: string;
94.   delegatedFor?: string;
95.   timestamp: Date;
96.   previousValue: unknown;
97.   newValue: unknown;
98.   source: string;
99. }
100. 
101. export interface Decision {
102.   id: string;
103.   applicationId: string;
104.   type: "approve" | "decline" | "refer";
105.   rationale: string;
106.   decidedBy: string;
107.   decidedAt: Date;
108.   conditions?: string[];
109. }
110. 
111. // ---------------------------------------------------------------------------
112. // Request / response shapes
113. // ---------------------------------------------------------------------------
114. 
115. export interface PreferenceUpdateRequest {
116.   event: NotificationEvent;
117.   channel: NotificationChannel;
118.   enabled: boolean;
119. }
120. 
121. export interface PreferenceSaveResult {
122.   saved: boolean;
123.   reason?: string;
124.   preferences: NotificationPreference[];
125. }
126. 
127. /**
128.  * Request body for PATCH /notifications/preferences/:eventType.
129.  * Specify which channels to enable or disable for a single event type.
130.  * Omit a channel key to leave it unchanged.
131.  */
132. export interface EventChannelUpdateRequest {
133.   channels: Partial<Record<NotificationChannel, boolean>>;
134.   loanState?: string;
135. }
136.
```

</details>


---

<sub>⏱️ 19s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\store\memory-store.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\store\memory-store.ts

<details>
<summary>185 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // In-Memory Data Store
3. // ---------------------------------------------------------------------------
4. // Provides seeded data for the Loan Workbench demo.  In production this
5. // layer would be backed by a database.  The seed data is designed to
6. // exercise edge cases: California loans, delegated users, finalized
7. // applications, and users without saved preferences.
8. // ---------------------------------------------------------------------------
9. 
10. import type {
11.   User,
12.   LoanApplication,
13.   NotificationPreference,
14. } from "../models/types.js";
15. 
16. class MemoryStore {
17.   private users: Map<string, User> = new Map();
18.   private applications: Map<string, LoanApplication> = new Map();
19.   private preferences: NotificationPreference[] = [];
20. 
21.   constructor() {
22.     this.seed();
23.   }
24. 
25.   // ---- Users --------------------------------------------------------------
26. 
27.   getUser(id: string): User | undefined {
28.     return this.users.get(id);
29.   }
30. 
31.   getAllUsers(): User[] {
32.     return [...this.users.values()];
33.   }
34. 
35.   // ---- Applications -------------------------------------------------------
36. 
37.   getApplication(id: string): LoanApplication | undefined {
38.     return this.applications.get(id);
39.   }
40. 
41.   getAllApplications(): LoanApplication[] {
42.     return [...this.applications.values()];
43.   }
44. 
45.   updateApplication(
46.     id: string,
47.     patch: Partial<LoanApplication>,
48.   ): LoanApplication | undefined {
49.     const app = this.applications.get(id);
50.     if (!app) return undefined;
51.     Object.assign(app, patch, { updatedAt: new Date() });
52.     return app;
53.   }
54. 
55.   addApplication(app: LoanApplication): void {
56.     this.applications.set(app.id, app);
57.   }
58. 
59.   // ---- Notification Preferences -------------------------------------------
60. 
61.   getPreferencesForUser(userId: string): NotificationPreference[] {
62.     return this.preferences.filter((p) => p.userId === userId);
63.   }
64. 
65.   setPreference(pref: NotificationPreference): void {
66.     const idx = this.preferences.findIndex(
67.       (p) =>
68.         p.userId === pref.userId &&
69.         p.event === pref.event &&
70.         p.channel === pref.channel,
71.     );
72.     if (idx >= 0) {
73.       this.preferences[idx] = pref;
74.     } else {
75.       this.preferences.push(pref);
76.     }
77.   }
78. 
79.   // ---- Seed Data ----------------------------------------------------------
80. 
81.   private seed(): void {
82.     // Users
83.     this.users.set("u-1", {
84.       id: "u-1",
85.       role: "underwriter",
86.       name: "Dana Chu",
87.       email: "dana.chu@loanworkbench.local",
88.       phone: "+15551234001",
89.     });
90.     this.users.set("u-2", {
91.       id: "u-2",
92.       role: "analyst-manager",
93.       name: "Raj Patel",
94.       email: "raj.patel@loanworkbench.local",
95.       phone: "+15551234002",
96.     });
97.     this.users.set("u-3", {
98.       id: "u-3",
99.       role: "compliance-reviewer",
100.       name: "Kim Nakamura",
101.       email: "kim.nakamura@loanworkbench.local",
102.     });
103.     // User with NO saved preferences — exercises first-access defaults.
104.     this.users.set("u-4", {
105.       id: "u-4",
106.       role: "underwriter",
107.       name: "Alex Torres",
108.       email: "alex.torres@loanworkbench.local",
109.       phone: "+15551234004",
110.     });
111. 
112.     // Applications
113.     const now = new Date();
114.     this.applications.set("app-100", {
115.       id: "app-100",
116.       borrowerName: "Westfield Holdings LLC",
117.       amount: 2_500_000,
118.       loanState: "CA", // California — triggers SMS restrictions
119.       status: "underwriting",
120.       assignedUnderwriter: "u-1",
121.       createdAt: now,
122.       updatedAt: now,
123.     });
124.     this.applications.set("app-101", {
125.       id: "app-101",
126.       borrowerName: "Great Lakes Manufacturing",
127.       amount: 850_000,
128.       loanState: "IL",
129.       status: "decision",
130.       assignedUnderwriter: "u-1",
131.       createdAt: now,
132.       updatedAt: now,
133.     });
134.     this.applications.set("app-102", {
135.       id: "app-102",
136.       borrowerName: "Summit Realty Group",
137.       amount: 4_000_000,
138.       loanState: "NY",
139.       status: "finalized", // Terminal — no further transitions
140.       assignedUnderwriter: "u-1",
141.       createdAt: now,
142.       updatedAt: now,
143.     });
144. 
145.     // Pre-saved preferences for u-1 (Dana).
146.     const events = [
147.       "approval",
148.       "decline",
149.       "document-request",
150.       "manual-review-escalation",
151.     ] as const;
152.     for (const event of events) {
153.       this.preferences.push({
154.         userId: "u-1",
155.         event,
156.         channel: "email",
157.         enabled: true,
158.         updatedAt: now,
159.         updatedBy: "system",
160.       });
161.       this.preferences.push({
162.         userId: "u-1",
163.         event,
164.         channel: "sms",
165.         enabled: event === "manual-review-escalation",
166.         updatedAt: now,
167.         updatedBy: "system",
168.       });
169.     }
170. 
171.     // u-2 (Raj) has partial preferences — SMS deliberately left unset for
172.     // some events to exercise the "mixed saved/default" edge case.
173.     this.preferences.push({
174.       userId: "u-2",
175.       event: "manual-review-escalation",
176.       channel: "email",
177.       enabled: true,
178.       updatedAt: now,
179.       updatedBy: "system",
180.     });
181.   }
182. }
183. 
184. export const store = new MemoryStore();
185.
```

</details>


---

<sub>⏱️ 19s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\routes\notifications.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\routes\notifications.ts

<details>
<summary>433 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Notification Preferences Routes
3. // ---------------------------------------------------------------------------
4. // This is the most context-sensitive route module in the app.  A naive
5. // implementation would be a simple CRUD toggle, but the real behavior
6. // depends on:
7. //   - Role-based defaults for first-access users (role-defaults.ts)
8. //   - Mandatory event rules (mandatory-events.ts)
9. //   - State-specific restrictions (state-rules.ts)
10. //   - Delegated-session write blocks (auth middleware)
11. //   - Feature-flag gating (feature-flags.ts)
12. //   - Audit fail-closed semantics (audit-service.ts)
13. //
14. // Without these in context, an AI assistant will produce code that
15. // looks correct but allows forbidden state combinations.
16. // ---------------------------------------------------------------------------
17. 
18. import { Router } from "express";
19. import { blockDelegatedWrites, requireRole } from "../middleware/auth.js";
20. import { requireFlag } from "../config/feature-flags.js";
21. import { store } from "../store/memory-store.js";
22. import {
23.   generateRoleDefaults,
24.   roleHasNotificationDefaults,
25. } from "../rules/role-defaults.js";
26. import { validateMandatoryEventChange } from "../rules/mandatory-events.js";
27. import {
28.   checkStateRestriction,
29.   getActiveRestrictions,
30. } from "../rules/state-rules.js";
31. import { writeAuditEntry } from "../services/audit-service.js";
32. import type {
33.   NotificationChannel,
34.   NotificationEvent,
35.   NotificationPreference,
36.   PreferenceUpdateRequest,
37.   EventChannelUpdateRequest,
38.   SessionContext,
39. } from "../models/types.js";
40. 
41. /** All valid notification event type values. */
42. const VALID_NOTIFICATION_EVENTS = new Set<NotificationEvent>([
43.   "approval",
44.   "decline",
45.   "document-request",
46.   "manual-review-escalation",
47. ]);
48. 
49. export const notificationRoutes = Router();
50. 
51. /**
52.  * GET /notifications/preferences
53.  *
54.  * Return the current user's notification preferences.  If the user has
55.  * never saved preferences, generate role-based defaults and persist them.
56.  *
57.  * In delegated sessions, returns the DELEGATE's preferences (read-only).
58.  *
59.  * Query params:
60.  *   - loanState  (optional) — when provided, marks state-restricted
61.  *     channels in the response so the UI can render inline explanations.
62.  */
63. notificationRoutes.get(
64.   "/preferences",
65.   requireRole("underwriter", "analyst-manager", "compliance-reviewer"),
66.   (req, res, next) => {
67.     try {
68.       requireFlag("notificationPreferences");
69. 
70.       const session = req.session as SessionContext;
71.       const targetUser = session.delegatedFor ?? session.actor;
72. 
73.       let prefs = store.getPreferencesForUser(targetUser.id);
74. 
75.       // First-access: generate role-based defaults.
76.       if (prefs.length === 0 && roleHasNotificationDefaults(targetUser.role)) {
77.         const defaults = generateRoleDefaults(targetUser.id, targetUser.role);
78.         for (const p of defaults) {
79.           store.setPreference(p);
80.         }
81.         prefs = defaults;
82.       }
83. 
84.       // Annotate with state restrictions if a loan context is provided.
85.       const loanState = req.query.loanState as string | undefined;
86.       let restrictions: ReturnType<typeof getActiveRestrictions> = [];
87.       if (loanState) {
88.         restrictions = getActiveRestrictions(loanState);
89.       }
90. 
91.       res.json({
92.         userId: targetUser.id,
93.         delegated: !!session.delegatedFor,
94.         readOnly:
95.           !!session.delegatedFor || targetUser.role === "compliance-reviewer",
96.         preferences: prefs,
97.         restrictions,
98.       });
99.     } catch (err) {
100.       next(err);
101.     }
102.   },
103. );
104. 
105. /**
106.  * PUT /notifications/preferences
107.  *
108.  * Update one or more notification preferences for the current user.
109.  *
110.  * Blocked in delegated sessions and for compliance reviewers.
111.  * Validates against mandatory-event rules, state restrictions, and
112.  * feature flags.  Audit writes are fail-closed.
113.  *
114.  * Body: { changes: PreferenceUpdateRequest[], loanState?: string }
115.  */
116. notificationRoutes.put(
117.   "/preferences",
118.   requireRole("underwriter", "analyst-manager"),
119.   blockDelegatedWrites,
120.   async (req, res, next) => {
121.     try {
122.       requireFlag("notificationPreferences");
123. 
124.       const session = req.session as SessionContext;
125.       const userId = session.actor.id;
126.       const { changes, loanState } = req.body as {
127.         changes: PreferenceUpdateRequest[];
128.         loanState?: string;
129.       };
130. 
131.       if (!Array.isArray(changes) || changes.length === 0) {
132.         res
133.           .status(400)
134.           .json({ error: "Body must include a non-empty 'changes' array." });
135.         return;
136.       }
137. 
138.       // Ensure the user has a baseline preference set.
139.       let currentPrefs = store.getPreferencesForUser(userId);
140.       if (
141.         currentPrefs.length === 0 &&
142.         roleHasNotificationDefaults(session.actor.role)
143.       ) {
144.         const defaults = generateRoleDefaults(userId, session.actor.role);
145.         for (const p of defaults) store.setPreference(p);
146.         currentPrefs = defaults;
147.       }
148. 
149.       const errors: string[] = [];
150.       const accepted: NotificationPreference[] = [];
151. 
152.       for (const change of changes) {
153.         // Validate mandatory-event rules.
154.         const mandatoryCheck = validateMandatoryEventChange(
155.           currentPrefs,
156.           change.event,
157.           change.channel,
158.           change.enabled,
159.         );
160.         if (!mandatoryCheck.allowed) {
161.           errors.push(mandatoryCheck.reason!);
162.           continue;
163.         }
164. 
165.         // Validate state-specific restrictions.
166.         if (loanState) {
167.           const stateCheck = checkStateRestriction(
168.             loanState,
169.             change.event,
170.             change.channel,
171.           );
172.           if (stateCheck.restricted && change.enabled) {
173.             errors.push(stateCheck.reason!);
174.             continue;
175.           }
176.         }
177. 
178.         const previous = currentPrefs.find(
179.           (p) => p.event === change.event && p.channel === change.channel,
180.         );
181. 
182.         const updated: NotificationPreference = {
183.           userId,
184.           event: change.event,
185.           channel: change.channel,
186.           enabled: change.enabled,
187.           updatedAt: new Date(),
188.           updatedBy: session.actor.id,
189.         };
190. 
191.         // Audit BEFORE persist — fail closed.
192.         await writeAuditEntry(
193.           session,
194.           "preference.updated",
195.           previous ?? null,
196.           updated,
197.           "notification-routes",
198.         );
199. 
200.         store.setPreference(updated);
201.         accepted.push(updated);
202. 
203.         // Update the working copy so subsequent mandatory-event checks
204.         // see the intermediate state.
205.         currentPrefs = store.getPreferencesForUser(userId);
206.       }
207. 
208.       const status =
209.         errors.length > 0 ? (accepted.length > 0 ? 207 : 422) : 200;
210.       res.status(status).json({
211.         saved: accepted.length,
212.         rejected: errors.length,
213.         errors: errors.length > 0 ? errors : undefined,
214.         preferences: store.getPreferencesForUser(userId),
215.       });
216.     } catch (err) {
217.       next(err);
218.     }
219.   },
220. );
221. 
222. /**
223.  * DELETE /notifications/preferences/:event
224.  *
225.  * Reset all channel preferences for a single event type to the role-based
226.  * defaults for the current user.
227.  *
228.  * Blocked in delegated sessions and for compliance reviewers.
229.  * Validates event type and feature flag. Audit writes are fail-closed.
230.  *
231.  * Params:
232.  *   - event  — one of: approval, decline, document-request,
233.  *              manual-review-escalation
234.  */
235. notificationRoutes.delete(
236.   "/preferences/:event",
237.   requireRole("underwriter", "analyst-manager"),
238.   blockDelegatedWrites,
239.   async (req, res, next) => {
240.     try {
241.       requireFlag("notificationPreferences");
242. 
243.       const rawEvent = req.params.event;
244.       if (!VALID_NOTIFICATION_EVENTS.has(rawEvent as NotificationEvent)) {
245.         res.status(400).json({
246.           error: {
247.             code: "VALIDATION_ERROR",
248.             message: `Invalid event type: "${rawEvent}". Must be one of: ${[...VALID_NOTIFICATION_EVENTS].join(", ")}.`,
249.           },
250.         });
251.         return;
252.       }
253.       const event = rawEvent as NotificationEvent;
254. 
255.       const session = req.session as SessionContext;
256.       const userId = session.actor.id;
257. 
258.       const defaults = generateRoleDefaults(userId, session.actor.role);
259.       const eventDefaults = defaults.filter((p) => p.event === event);
260. 
261.       const currentPrefs = store.getPreferencesForUser(userId);
262. 
263.       // Audit BEFORE persist — fail closed.
264.       for (const pref of eventDefaults) {
265.         const previous =
266.           currentPrefs.find(
267.             (p) => p.event === pref.event && p.channel === pref.channel,
268.           ) ?? null;
269.         await writeAuditEntry(
270.           session,
271.           "preference.reset",
272.           previous,
273.           pref,
274.           "notification-routes",
275.         );
276.       }
277. 
278.       for (const pref of eventDefaults) {
279.         store.setPreference(pref);
280.       }
281. 
282.       res.status(200).json({
283.         preferences: store
284.           .getPreferencesForUser(userId)
285.           .filter((p) => p.event === event),
286.       });
287.     } catch (err) {
288.       next(err);
289.     }
290.   },
291. );
292. 
293. /**
294.  * PATCH /notifications/preferences/:eventType
295.  *
296.  * Update channel preferences (email, SMS) for a single event type.
297.  * Omit a channel key in the body to leave it unchanged (partial update).
298.  *
299.  * Blocked in delegated sessions and for compliance reviewers.
300.  * Validates eventType, mandatory-event rules, state restrictions, and
301.  * feature flags.  Audit writes are fail-closed.
302.  *
303.  * Params:
304.  *   - eventType  — one of: approval, decline, document-request,
305.  *                  manual-review-escalation
306.  *
307.  * Body: { channels: { email?: boolean, sms?: boolean }, loanState?: string }
308.  */
309. notificationRoutes.patch(
310.   "/preferences/:eventType",
311.   requireRole("underwriter", "analyst-manager"),
312.   blockDelegatedWrites,
313.   async (req, res, next) => {
314.     try {
315.       requireFlag("notificationPreferences");
316. 
317.       const rawEvent = req.params.eventType;
318.       if (!VALID_NOTIFICATION_EVENTS.has(rawEvent as NotificationEvent)) {
319.         res.status(400).json({
320.           error: {
321.             code: "VALIDATION_ERROR",
322.             message: `Invalid event type: "${rawEvent}". Must be one of: ${[...VALID_NOTIFICATION_EVENTS].join(", ")}.`,
323.           },
324.         });
325.         return;
326.       }
327.       const eventType = rawEvent as NotificationEvent;
328. 
329.       const { channels, loanState } = req.body as EventChannelUpdateRequest;
330. 
331.       if (
332.         !channels ||
333.         typeof channels !== "object" ||
334.         Object.keys(channels).length === 0
335.       ) {
336.         res.status(400).json({
337.           error: {
338.             code: "VALIDATION_ERROR",
339.             message:
340.               "Body must include a 'channels' object with at least one channel key (email, sms).",
341.           },
342.         });
343.         return;
344.       }
345. 
346.       const session = req.session as SessionContext;
347.       const userId = session.actor.id;
348. 
349.       // Ensure the user has a baseline preference set.
350.       let currentPrefs = store.getPreferencesForUser(userId);
351.       if (
352.         currentPrefs.length === 0 &&
353.         roleHasNotificationDefaults(session.actor.role)
354.       ) {
355.         const defaults = generateRoleDefaults(userId, session.actor.role);
356.         for (const p of defaults) store.setPreference(p);
357.         currentPrefs = defaults;
358.       }
359. 
360.       const errors: string[] = [];
361.       const accepted: NotificationPreference[] = [];
362. 
363.       for (const [channel, enabled] of Object.entries(channels) as [
364.         NotificationChannel,
365.         boolean,
366.       ][]) {
367.         // Validate mandatory-event rules.
368.         const mandatoryCheck = validateMandatoryEventChange(
369.           currentPrefs,
370.           eventType,
371.           channel,
372.           enabled,
373.         );
374.         if (!mandatoryCheck.allowed) {
375.           errors.push(mandatoryCheck.reason!);
376.           continue;
377.         }
378. 
379.         // Validate state-specific restrictions.
380.         if (loanState) {
381.           const stateCheck = checkStateRestriction(loanState, eventType, channel);
382.           if (stateCheck.restricted && enabled) {
383.             errors.push(stateCheck.reason!);
384.             continue;
385.           }
386.         }
387. 
388.         const previous = currentPrefs.find(
389.           (p) => p.event === eventType && p.channel === channel,
390.         );
391. 
392.         const updated: NotificationPreference = {
393.           userId,
394.           event: eventType,
395.           channel,
396.           enabled,
397.           updatedAt: new Date(),
398.           updatedBy: session.actor.id,
399.         };
400. 
401.         // Audit BEFORE persist — fail closed.
402.         await writeAuditEntry(
403.           session,
404.           "preference.updated",
405.           previous ?? null,
406.           updated,
407.           "notification-routes",
408.         );
409. 
410.         store.setPreference(updated);
411.         accepted.push(updated);
412. 
413.         // Update the working copy so subsequent mandatory-event checks
414.         // see the intermediate state.
415.         currentPrefs = store.getPreferencesForUser(userId);
416.       }
417. 
418.       const status =
419.         errors.length > 0 ? (accepted.length > 0 ? 207 : 422) : 200;
420.       res.status(status).json({
421.         saved: accepted.length,
422.         rejected: errors.length,
423.         errors: errors.length > 0 ? errors : undefined,
424.         preferences: store.getPreferencesForUser(userId).filter(
425.           (p) => p.event === eventType,
426.         ),
427.       });
428.     } catch (err) {
429.       next(err);
430.     }
431.   },
432. );
433.
```

</details>


---

<sub>⏱️ 19s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\app.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\app.ts

<details>
<summary>40 lines</summary>

```
1. import express from "express";
2. import { authMiddleware } from "./middleware/auth.js";
3. import { auditLoggerMiddleware } from "./middleware/audit-logger.js";
4. import { errorHandler } from "./middleware/error-handler.js";
5. import { applicationRoutes } from "./routes/applications.js";
6. import { decisionRoutes } from "./routes/decisions.js";
7. import { notificationRoutes } from "./routes/notifications.js";
8. import { auditRoutes } from "./routes/audit.js";
9. 
10. const app = express();
11. const PORT = process.env.PORT ?? 3100;
12. 
13. app.use(express.json());
14. 
15. // Authenticate every request and attach session context.
16. app.use(authMiddleware);
17. 
18. // Log mutating requests to the audit trail.
19. app.use(auditLoggerMiddleware);
20. 
21. // Domain routes
22. app.use("/applications", applicationRoutes);
23. app.use("/decisions", decisionRoutes);
24. app.use("/notifications", notificationRoutes);
25. app.use("/audit", auditRoutes);
26. 
27. // Health check — no auth required in production (handled before auth mw).
28. app.get("/health", (_req, res) => {
29.   res.json({ status: "ok" });
30. });
31. 
32. // Central error handler — must be registered last.
33. app.use(errorHandler);
34. 
35. app.listen(PORT, () => {
36.   console.log(`Loan Workbench API listening on port ${PORT}`);
37. });
38. 
39. export default app;
40.
```

</details>


---

<sub>⏱️ 26s</sub>

### 💬 Copilot

Let me check the tests and other supporting files:

---

<sub>⏱️ 26s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\tests.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\tests

```
decisions.test.ts
notifications.test.ts
```


---

<sub>⏱️ 26s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\rules.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\rules

```
mandatory-events.ts
role-defaults.ts
state-rules.ts
```


---

<sub>⏱️ 31s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\tests\notifications.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\tests\notifications.test.ts

<details>
<summary>448 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Notification Preferences — Edge Case Tests
3. // ---------------------------------------------------------------------------
4. // These tests demonstrate scenarios where context engineering makes a
5. // measurable difference.  Each test group documents the false-positive
6. // or hard-negative pattern it exercises so learners can see WHY the
7. // project context matters.
8. // ---------------------------------------------------------------------------
9. 
10. import { describe, it, expect, beforeEach } from "vitest";
11. import {
12.   validateMandatoryEventChange,
13.   isMandatoryEvent,
14. } from "../src/rules/mandatory-events.js";
15. import {
16.   checkStateRestriction,
17.   getPortfolioRestrictionSummary,
18. } from "../src/rules/state-rules.js";
19. import {
20.   generateRoleDefaults,
21.   roleHasNotificationDefaults,
22. } from "../src/rules/role-defaults.js";
23. import type { NotificationPreference } from "../src/models/types.js";
24. 
25. // ---------------------------------------------------------------------------
26. // Mandatory Event Rules
27. // ---------------------------------------------------------------------------
28. 
29. describe("mandatory-events", () => {
30.   const basePrefs: NotificationPreference[] = [
31.     {
32.       userId: "u-1",
33.       event: "manual-review-escalation",
34.       channel: "email",
35.       enabled: true,
36.       updatedAt: new Date(),
37.       updatedBy: "system",
38.     },
39.     {
40.       userId: "u-1",
41.       event: "manual-review-escalation",
42.       channel: "sms",
43.       enabled: true,
44.       updatedAt: new Date(),
45.       updatedBy: "system",
46.     },
47.   ];
48. 
49.   it("allows disabling the secondary channel when primary remains", () => {
50.     // FALSE POSITIVE: User disables SMS for escalation — looks wrong but is
51.     // valid because email is still enabled.
52.     const result = validateMandatoryEventChange(
53.       basePrefs,
54.       "manual-review-escalation",
55.       "sms",
56.       false,
57.     );
58.     expect(result.allowed).toBe(true);
59.   });
60. 
61.   it("blocks disabling the LAST channel for a mandatory event", () => {
62.     // HARD NEGATIVE: Code path looks identical to the test above, but here
63.     // email is already disabled.  Without context an AI might not add this
64.     // guard at all.
65.     const oneChannelPrefs: NotificationPreference[] = [
66.       {
67.         userId: "u-1",
68.         event: "manual-review-escalation",
69.         channel: "email",
70.         enabled: false,
71.         updatedAt: new Date(),
72.         updatedBy: "system",
73.       },
74.       {
75.         userId: "u-1",
76.         event: "manual-review-escalation",
77.         channel: "sms",
78.         enabled: true,
79.         updatedAt: new Date(),
80.         updatedBy: "system",
81.       },
82.     ];
83. 
84.     const result = validateMandatoryEventChange(
85.       oneChannelPrefs,
86.       "manual-review-escalation",
87.       "sms",
88.       false,
89.     );
90.     expect(result.allowed).toBe(false);
91.     expect(result.reason).toContain("at least one delivery channel");
92.   });
93. 
94.   it("always allows enabling a channel", () => {
95.     const result = validateMandatoryEventChange(
96.       basePrefs,
97.       "manual-review-escalation",
98.       "sms",
99.       true,
100.     );
101.     expect(result.allowed).toBe(true);
102.   });
103. 
104.   it("does not enforce mandatory rules on non-mandatory events", () => {
105.     // FALSE POSITIVE: Disabling all channels for 'approval' is perfectly
106.     // fine — it is not a mandatory event.
107.     const approvalPrefs: NotificationPreference[] = [
108.       {
109.         userId: "u-1",
110.         event: "approval",
111.         channel: "email",
112.         enabled: false,
113.         updatedAt: new Date(),
114.         updatedBy: "system",
115.       },
116.       {
117.         userId: "u-1",
118.         event: "approval",
119.         channel: "sms",
120.         enabled: true,
121.         updatedAt: new Date(),
122.         updatedBy: "system",
123.       },
124.     ];
125. 
126.     const result = validateMandatoryEventChange(
127.       approvalPrefs,
128.       "approval",
129.       "sms",
130.       false,
131.     );
132.     expect(result.allowed).toBe(true);
133.   });
134. 
135.   it("identifies mandatory event types", () => {
136.     expect(isMandatoryEvent("manual-review-escalation")).toBe(true);
137.     expect(isMandatoryEvent("approval")).toBe(false);
138.     expect(isMandatoryEvent("decline")).toBe(false);
139.   });
140. });
141. 
142. // ---------------------------------------------------------------------------
143. // State-Specific Rules
144. // ---------------------------------------------------------------------------
145. 
146. describe("state-rules", () => {
147.   it("blocks SMS for decline events on California loans", () => {
148.     // HARD NEGATIVE: Enabling this toggle looks like normal CRUD but
149.     // violates a legal hold.  Without state-rules.ts in context, an AI
150.     // would never generate this check.
151.     const result = checkStateRestriction("CA", "decline", "sms");
152.     expect(result.restricted).toBe(true);
153.     expect(result.reason).toContain("CA");
154.     expect(result.ticket).toBe("LEGAL-218");
155.   });
156. 
157.   it("allows SMS for decline events on Illinois loans", () => {
158.     // FALSE POSITIVE: A tester checking SMS-decline on non-CA loans
159.     // should see it work normally.
160.     const result = checkStateRestriction("IL", "decline", "sms");
161.     expect(result.restricted).toBe(false);
162.   });
163. 
164.   it("allows email for decline events on California loans", () => {
165.     // FALSE POSITIVE: Only SMS is restricted in CA — email for decline is fine.
166.     const result = checkStateRestriction("CA", "decline", "email");
167.     expect(result.restricted).toBe(false);
168.   });
169. 
170.   it("blocks email for decline events on New York loans", () => {
171.     // HARD NEGATIVE: Enabling email for decline on an NY loan looks like normal
172.     // CRUD but violates a legal hold (LEGAL-305).
173.     const result = checkStateRestriction("NY", "decline", "email");
174.     expect(result.restricted).toBe(true);
175.     expect(result.reason).toContain("NY");
176.     expect(result.ticket).toBe("LEGAL-305");
177.   });
178. 
179.   it("allows SMS for decline events on New York loans", () => {
180.     // FALSE POSITIVE: NY only restricts email for decline — SMS is unrestricted.
181.     const result = checkStateRestriction("NY", "decline", "sms");
182.     expect(result.restricted).toBe(false);
183.   });
184. 
185.   it("allows email for non-decline events on New York loans", () => {
186.     // The NY restriction is decline-specific.  Approval email in NY is fine.
187.     const result = checkStateRestriction("NY", "approval", "email");
188.     expect(result.restricted).toBe(false);
189.   });
190. 
191.   it("allows SMS for non-decline events on California loans", () => {
192.     // The restriction is decline-specific.  Approval SMS in CA is fine.
193.     const result = checkStateRestriction("CA", "approval", "sms");
194.     expect(result.restricted).toBe(false);
195.   });
196. 
197.   it("blocks CA SMS for decline regardless of state-code casing (CA, ca, Ca)", () => {
198.     // BOUNDARY: state codes may arrive in any casing from upstream systems.
199.     // All three variants must resolve to the same LEGAL-218 restriction so
200.     // that a mixed-case input is never an accidental bypass.
201.     for (const stateCode of ["CA", "ca", "Ca"]) {
202.       const result = checkStateRestriction(stateCode, "decline", "sms");
203.       expect(result.restricted, `expected restricted for state code "${stateCode}"`).toBe(true);
204.       expect(result.ticket, `expected ticket for state code "${stateCode}"`).toBe("LEGAL-218");
205.     }
206.   });
207. 
208.   it("returns combined restrictions for multi-state portfolios", () => {
209.     const summary = getPortfolioRestrictionSummary(["CA", "IL", "NY"]);
210.     // CA contributes LEGAL-218 (decline/sms), NY contributes LEGAL-305 (decline/email)
211.     expect(summary.length).toBe(2);
212.     expect(summary.find((r) => r.state === "CA")?.ticket).toBe("LEGAL-218");
213.     expect(summary.find((r) => r.state === "NY")?.ticket).toBe("LEGAL-305");
214.   });
215. });
216. 
217. // ---------------------------------------------------------------------------
218. // Role-Based Defaults
219. // ---------------------------------------------------------------------------
220. 
221. describe("role-defaults", () => {
222.   it("generates full preference matrix for underwriters", () => {
223.     const prefs = generateRoleDefaults("u-new", "underwriter");
224.     // 4 events × 2 channels = 8 preferences
225.     expect(prefs).toHaveLength(8);
226.     // Only escalation SMS should be enabled by default.
227.     const smsEnabled = prefs.filter((p) => p.channel === "sms" && p.enabled);
228.     expect(smsEnabled).toHaveLength(1);
229.     expect(smsEnabled[0].event).toBe("manual-review-escalation");
230.   });
231. 
232.   it("generates preferences for analyst-managers", () => {
233.     const prefs = generateRoleDefaults("u-new", "analyst-manager");
234.     expect(prefs).toHaveLength(8);
235.   });
236. 
237.   it("returns empty array for compliance-reviewers", () => {
238.     // Compliance reviewers have no operational notification defaults.
239.     const prefs = generateRoleDefaults("u-new", "compliance-reviewer");
240.     expect(prefs).toHaveLength(0);
241.   });
242. 
243.   it("reports which roles have defaults", () => {
244.     expect(roleHasNotificationDefaults("underwriter")).toBe(true);
245.     expect(roleHasNotificationDefaults("analyst-manager")).toBe(true);
246.     expect(roleHasNotificationDefaults("compliance-reviewer")).toBe(false);
247.   });
248. });
249. 
250. // ---------------------------------------------------------------------------
251. // PATCH /notifications/preferences/:eventType — Per-Event Channel Update
252. // ---------------------------------------------------------------------------
253. // These tests exercise the business logic applied when a user saves channel
254. // preferences for a single event type in one request.  The PATCH route
255. // applies changes sequentially, re-evaluating mandatory-event rules after
256. // each channel update.
257. // ---------------------------------------------------------------------------
258. 
259. describe("per-event channel update (PATCH semantics)", () => {
260.   const twoChannelPrefs: NotificationPreference[] = [
261.     {
262.       userId: "u-1",
263.       event: "manual-review-escalation",
264.       channel: "email",
265.       enabled: true,
266.       updatedAt: new Date(),
267.       updatedBy: "system",
268.     },
269.     {
270.       userId: "u-1",
271.       event: "manual-review-escalation",
272.       channel: "sms",
273.       enabled: true,
274.       updatedAt: new Date(),
275.       updatedBy: "system",
276.     },
277.   ];
278. 
279.   it("allows disabling one channel when the other remains enabled", () => {
280.     // Disabling sms is fine — email is still active.
281.     const result = validateMandatoryEventChange(
282.       twoChannelPrefs,
283.       "manual-review-escalation",
284.       "sms",
285.       false,
286.     );
287.     expect(result.allowed).toBe(true);
288.   });
289. 
290.   it("blocks the second channel disable for a mandatory event when applied sequentially", () => {
291.     // Simulate the PATCH route loop: apply email=false, then sms=false.
292.     // After the first change, currentPrefs reflects email disabled.
293.     const afterEmailDisabled: NotificationPreference[] = [
294.       {
295.         userId: "u-1",
296.         event: "manual-review-escalation",
297.         channel: "email",
298.         enabled: false,
299.         updatedAt: new Date(),
300.         updatedBy: "system",
301.       },
302.       {
303.         userId: "u-1",
304.         event: "manual-review-escalation",
305.         channel: "sms",
306.         enabled: true,
307.         updatedAt: new Date(),
308.         updatedBy: "system",
309.       },
310.     ];
311. 
312.     const firstResult = validateMandatoryEventChange(
313.       twoChannelPrefs,
314.       "manual-review-escalation",
315.       "email",
316.       false,
317.     );
318.     expect(firstResult.allowed).toBe(true); // sms still on
319. 
320.     // Second change sees updated prefs where email is already disabled.
321.     const secondResult = validateMandatoryEventChange(
322.       afterEmailDisabled,
323.       "manual-review-escalation",
324.       "sms",
325.       false,
326.     );
327.     expect(secondResult.allowed).toBe(false);
328.     expect(secondResult.reason).toContain("at least one delivery channel");
329.   });
330. 
331.   it("allows disabling both channels for a non-mandatory event", () => {
332.     const approvalPrefs: NotificationPreference[] = [
333.       {
334.         userId: "u-1",
335.         event: "approval",
336.         channel: "email",
337.         enabled: true,
338.         updatedAt: new Date(),
339.         updatedBy: "system",
340.       },
341.       {
342.         userId: "u-1",
343.         event: "approval",
344.         channel: "sms",
345.         enabled: true,
346.         updatedAt: new Date(),
347.         updatedBy: "system",
348.       },
349.     ];
350. 
351.     const emailResult = validateMandatoryEventChange(
352.       approvalPrefs,
353.       "approval",
354.       "email",
355.       false,
356.     );
357.     expect(emailResult.allowed).toBe(true);
358. 
359.     // Even with email disabled, disabling sms for a non-mandatory event is OK.
360.     const afterEmailDisabled = approvalPrefs.map((p) =>
361.       p.channel === "email" ? { ...p, enabled: false } : p,
362.     );
363.     const smsResult = validateMandatoryEventChange(
364.       afterEmailDisabled,
365.       "approval",
366.       "sms",
367.       false,
368.     );
369.     expect(smsResult.allowed).toBe(true);
370.   });
371. 
372.   it("blocks enabling SMS for a CA decline event (state restriction)", () => {
373.     // HARD NEGATIVE: enabling sms for decline on a CA loan is illegal (LEGAL-218)
374.     // regardless of how the user reaches the toggle.
375.     const stateCheck = checkStateRestriction("CA", "decline", "sms");
376.     expect(stateCheck.restricted).toBe(true);
377.   });
378. 
379.   it("allows setting both email and sms for a CA approval event", () => {
380.     // CA restriction is decline-only — approval SMS is unrestricted.
381.     const emailCheck = checkStateRestriction("CA", "approval", "email");
382.     const smsCheck = checkStateRestriction("CA", "approval", "sms");
383.     expect(emailCheck.restricted).toBe(false);
384.     expect(smsCheck.restricted).toBe(false);
385.   });
386. });
387. 
388. // ---------------------------------------------------------------------------
389. // Reset to Defaults (DELETE /notifications/preferences/:event semantics)
390. // ---------------------------------------------------------------------------
391. // The DELETE endpoint replaces a single event's preferences with the
392. // role-based defaults.  These tests validate the rule logic that drives
393. // that reset, using generateRoleDefaults as the public API under test.
394. // ---------------------------------------------------------------------------
395. 
396. describe("reset-event-to-defaults (DELETE semantics)", () => {
397.   it("generates correct defaults for a specific event on reset", () => {
398.     // HAPPY PATH: resetting 'approval' for underwriter yields email=true, sms=false.
399.     const eventDefaults = generateRoleDefaults("u-1", "underwriter").filter(
400.       (p) => p.event === "approval",
401.     );
402.     expect(eventDefaults).toHaveLength(2);
403.     expect(eventDefaults.find((p) => p.channel === "email")?.enabled).toBe(
404.       true,
405.     );
406.     expect(eventDefaults.find((p) => p.channel === "sms")?.enabled).toBe(
407.       false,
408.     );
409.   });
410. 
411.   it("reset for manual-review-escalation always preserves at least one enabled channel", () => {
412.     // HARD NEGATIVE: resetting the mandatory event must NOT produce a state
413.     // where all channels are disabled.  Role defaults guarantee email=true,
414.     // sms=true for this event — so the reset is inherently safe.
415.     const eventDefaults = generateRoleDefaults("u-1", "underwriter").filter(
416.       (p) => p.event === "manual-review-escalation",
417.     );
418.     expect(eventDefaults.some((p) => p.enabled)).toBe(true);
419.   });
420. 
421.   it("reset produces identical output on repeated calls (idempotent)", () => {
422.     // FALSE POSITIVE: calling reset twice looks like it might double-register
423.     // entries, but generateRoleDefaults is pure — output is always the same.
424.     const first = generateRoleDefaults("u-1", "underwriter").filter(
425.       (p) => p.event === "decline",
426.     );
427.     const second = generateRoleDefaults("u-1", "underwriter").filter(
428.       (p) => p.event === "decline",
429.     );
430.     expect(first).toHaveLength(second.length);
431.     first.forEach((pref, i) => {
432.       expect(pref.channel).toBe(second[i].channel);
433.       expect(pref.enabled).toBe(second[i].enabled);
434.     });
435.   });
436. 
437.   it("returns no defaults for compliance-reviewer (read-only role)", () => {
438.     // Compliance reviewers are blocked at the route level by requireRole,
439.     // but the rule itself correctly returns nothing for this role — ensuring
440.     // a reset would produce an empty set even if the guard were bypassed.
441.     const eventDefaults = generateRoleDefaults(
442.       "u-3",
443.       "compliance-reviewer",
444.     ).filter((p) => p.event === "approval");
445.     expect(eventDefaults).toHaveLength(0);
446.   });
447. });
448.
```

</details>


---

<sub>⏱️ 31s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\rules\role-defaults.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\rules\role-defaults.ts

<details>
<summary>86 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Role-Based Default Preferences
3. // ---------------------------------------------------------------------------
4. // New users who have never saved notification preferences receive defaults
5. // based on their organizational role.  The system must generate these on
6. // first access WITHOUT requiring a data backfill migration.
7. //
8. // KEY NUANCE:
9. //   Underwriters and analyst managers receive different default matrices.
10. //   Compliance reviewers have read-only access and never receive operational
11. //   notifications through this system, so they have no defaults here.
12. // ---------------------------------------------------------------------------
13. 
14. import type {
15.   UserRole,
16.   NotificationEvent,
17.   NotificationChannel,
18.   NotificationPreference,
19. } from "../models/types.js";
20. 
21. type DefaultMatrix = Record<
22.   NotificationEvent,
23.   Record<NotificationChannel, boolean>
24. >;
25. 
26. const UNDERWRITER_DEFAULTS: DefaultMatrix = {
27.   approval: { email: true, sms: false },
28.   decline: { email: true, sms: false },
29.   "document-request": { email: true, sms: false },
30.   "manual-review-escalation": { email: true, sms: true },
31. };
32. 
33. const ANALYST_MANAGER_DEFAULTS: DefaultMatrix = {
34.   approval: { email: true, sms: false },
35.   decline: { email: true, sms: false },
36.   "document-request": { email: true, sms: false },
37.   "manual-review-escalation": { email: true, sms: true },
38. };
39. 
40. const ROLE_DEFAULTS: Partial<Record<UserRole, DefaultMatrix>> = {
41.   underwriter: UNDERWRITER_DEFAULTS,
42.   "analyst-manager": ANALYST_MANAGER_DEFAULTS,
43.   // compliance-reviewer: no operational notification defaults
44. };
45. 
46. /**
47.  * Generate the default notification preference set for a user based on role.
48.  *
49.  * Returns an empty array for roles that have no defaults (e.g. compliance
50.  * reviewers).  The caller must persist these as the user's initial prefs
51.  * before the first preference read returns to the client.
52.  */
53. export function generateRoleDefaults(
54.   userId: string,
55.   role: UserRole,
56. ): NotificationPreference[] {
57.   const matrix = ROLE_DEFAULTS[role];
58.   if (!matrix) return [];
59. 
60.   const now = new Date();
61.   const prefs: NotificationPreference[] = [];
62. 
63.   for (const [event, channels] of Object.entries(matrix)) {
64.     for (const [channel, enabled] of Object.entries(channels)) {
65.       prefs.push({
66.         userId,
67.         event: event as NotificationEvent,
68.         channel: channel as NotificationChannel,
69.         enabled,
70.         updatedAt: now,
71.         updatedBy: "system",
72.       });
73.     }
74.   }
75. 
76.   return prefs;
77. }
78. 
79. /**
80.  * Check whether a given role receives operational notification defaults.
81.  * Used by the UI to decide whether to show the preferences panel at all.
82.  */
83. export function roleHasNotificationDefaults(role: UserRole): boolean {
84.   return role in ROLE_DEFAULTS;
85. }
86.
```

</details>


---

<sub>⏱️ 31s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\rules\mandatory-events.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\rules\mandatory-events.ts

<details>
<summary>89 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Mandatory Notification Event Rules
3. // ---------------------------------------------------------------------------
4. // Some notification events MUST remain deliverable regardless of user
5. // preferences.  Manual-review escalation is the primary example.
6. //
7. // KEY NUANCE — HARD NEGATIVE:
8. //   An AI assistant without this context would happily generate code that
9. //   lets users disable all channels for escalation events.  The system must
10. //   ensure at least one channel stays enabled for mandatory events.
11. //
12. // KEY NUANCE — FALSE POSITIVE:
13. //   A user changing the *secondary* channel for a mandatory event is valid.
14. //   Only disabling ALL channels is prohibited.  A bug report claiming "I
15. //   can't change my escalation SMS setting" is a false positive if the user
16. //   still has email enabled.
17. // ---------------------------------------------------------------------------
18. 
19. import type {
20.   NotificationEvent,
21.   NotificationChannel,
22.   NotificationPreference,
23. } from "../models/types.js";
24. 
25. /** Events that must have at least one active delivery channel. */
26. const MANDATORY_EVENTS: Set<NotificationEvent> = new Set([
27.   "manual-review-escalation",
28. ]);
29. 
30. /**
31.  * Check whether the given event is classified as mandatory.
32.  */
33. export function isMandatoryEvent(event: NotificationEvent): boolean {
34.   return MANDATORY_EVENTS.has(event);
35. }
36. 
37. /**
38.  * Validate a proposed preference change against mandatory-event rules.
39.  *
40.  * The function receives the user's current preference set and the proposed
41.  * change.  If the change would leave a mandatory event with zero enabled
42.  * channels, it returns a rejection with a human-readable explanation.
43.  *
44.  * @param currentPrefs  All current preferences for the user.
45.  * @param proposedEvent The event being modified.
46.  * @param proposedChannel The channel being modified.
47.  * @param proposedEnabled The new enabled value.
48.  * @returns `{ allowed: true }` or `{ allowed: false, reason: string }`.
49.  */
50. export function validateMandatoryEventChange(
51.   currentPrefs: NotificationPreference[],
52.   proposedEvent: NotificationEvent,
53.   proposedChannel: NotificationChannel,
54.   proposedEnabled: boolean,
55. ): { allowed: boolean; reason?: string } {
56.   // If enabling a channel, always allowed.
57.   if (proposedEnabled) return { allowed: true };
58. 
59.   // Only enforce rules on mandatory events.
60.   if (!isMandatoryEvent(proposedEvent)) return { allowed: true };
61. 
62.   // Count how many channels will remain enabled after the change.
63.   const remainingEnabled = currentPrefs.filter(
64.     (p) =>
65.       p.event === proposedEvent &&
66.       p.enabled &&
67.       // Exclude the channel being disabled (it won't count anymore).
68.       p.channel !== proposedChannel,
69.   );
70. 
71.   if (remainingEnabled.length === 0) {
72.     return {
73.       allowed: false,
74.       reason:
75.         `Cannot disable ${proposedChannel} for ${proposedEvent}: at least ` +
76.         `one delivery channel must remain enabled for mandatory events.`,
77.     };
78.   }
79. 
80.   return { allowed: true };
81. }
82. 
83. /**
84.  * Return the list of mandatory event names for UI labeling.
85.  */
86. export function getMandatoryEvents(): NotificationEvent[] {
87.   return [...MANDATORY_EVENTS];
88. }
89.
```

</details>


---

<sub>⏱️ 31s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\rules\state-rules.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\rules\state-rules.ts

<details>
<summary>121 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // State-Specific Business Rules
3. // ---------------------------------------------------------------------------
4. // These rules encode jurisdiction-level restrictions that override the default
5. // notification behavior.  Without this module in context, an AI assistant
6. // would generate a generic preference toggle that ignores legal holds.
7. //
8. // KEY NUANCE — FALSE POSITIVE:
9. //   A user seeing SMS disabled for decline events on a California loan might
10. //   file a bug.  It is NOT a bug — it is a legal restriction (LEGAL-218).
11. //   Likewise, email being disabled for decline events on a New York loan is
12. //   NOT a bug — it is a separate legal hold (LEGAL-305).
13. //   The UI must explain *why* each control is unavailable.
14. //
15. // KEY NUANCE — HARD NEGATIVE:
16. //   Allowing SMS for decline events on a California loan looks like normal
17. //   behavior from a code perspective (the toggle just flips a boolean).
18. //   The same applies to email for decline events on a New York loan.
19. //   The system must block both even though the code paths are otherwise valid.
20. // ---------------------------------------------------------------------------
21. 
22. import type {
23.   NotificationEvent,
24.   NotificationChannel,
25. } from "../models/types.js";
26. 
27. /**
28.  * Jurisdictions with active legal restrictions on notification channels.
29.  * Each entry maps a US state code to the set of restricted event+channel
30.  * combinations and references the tracking ticket for the legal review.
31.  */
32. const STATE_RESTRICTIONS: Record<
33.   string,
34.   { event: NotificationEvent; channel: NotificationChannel; ticket: string }[]
35. > = {
36.   CA: [
37.     {
38.       event: "decline",
39.       channel: "sms",
40.       ticket: "LEGAL-218",
41.     },
42.   ],
43.   NY: [
44.     {
45.       event: "decline",
46.       channel: "email",
47.       ticket: "LEGAL-305",
48.     },
49.   ],
50. };
51. 
52. /**
53.  * Check whether a specific event+channel combination is restricted for the
54.  * given loan jurisdiction.
55.  *
56.  * @returns An object with `restricted: true` and a human-readable reason
57.  *          when the combination is blocked, or `restricted: false` otherwise.
58.  */
59. export function checkStateRestriction(
60.   loanState: string,
61.   event: NotificationEvent,
62.   channel: NotificationChannel,
63. ): { restricted: boolean; reason?: string; ticket?: string } {
64.   const restrictions = STATE_RESTRICTIONS[loanState.toUpperCase()];
65.   if (!restrictions) return { restricted: false };
66. 
67.   const match = restrictions.find(
68.     (r) => r.event === event && r.channel === channel,
69.   );
70. 
71.   if (match) {
72.     return {
73.       restricted: true,
74.       reason:
75.         `${match.channel.toUpperCase()} notifications for ${event} events are unavailable for ` +
76.         `${loanState.toUpperCase()} loans pending legal review (${match.ticket}).`,
77.       ticket: match.ticket,
78.     };
79.   }
80.   return { restricted: false };
81. }
82. 
83. /**
84.  * Return all active restrictions for a given jurisdiction.
85.  * Used by the UI to render inline explanations for disabled controls.
86.  */
87. export function getActiveRestrictions(loanState: string) {
88.   return STATE_RESTRICTIONS[loanState.toUpperCase()] ?? [];
89. }
90. 
91. /**
92.  * When the settings screen is opened from a multi-state portfolio view, the
93.  * UI must show conditional rules rather than blanket-disabling controls.
94.  * This function returns a summary of restrictions across all provided states.
95.  */
96. export function getPortfolioRestrictionSummary(
97.   loanStates: string[],
98. ): {
99.   state: string;
100.   event: NotificationEvent;
101.   channel: NotificationChannel;
102.   ticket: string;
103. }[] {
104.   const results: {
105.     state: string;
106.     event: NotificationEvent;
107.     channel: NotificationChannel;
108.     ticket: string;
109.   }[] = [];
110. 
111.   for (const state of loanStates) {
112.     const restrictions = STATE_RESTRICTIONS[state.toUpperCase()];
113.     if (restrictions) {
114.       for (const r of restrictions) {
115.         results.push({ state: state.toUpperCase(), ...r });
116.       }
117.     }
118.   }
119.   return results;
120. }
121.
```

</details>


---

<sub>⏱️ 53s</sub>

### 💬 Copilot

Let me check the package.json and middleware:

---

<sub>⏱️ 53s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\package.json.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\package.json

<details>
<summary>27 lines</summary>

```
1. {
2.   "name": "loan-workbench-api",
3.   "version": "1.0.0",
4.   "description": "Loan Workbench — commercial loan processing API with role-based access, audit trail, state-specific rules, and notification preferences.",
5.   "private": true,
6.   "type": "module",
7.   "scripts": {
8.     "build": "tsc",
9.     "start": "node dist/app.js",
10.     "dev": "tsx watch src/app.ts",
11.     "test": "vitest run",
12.     "test:watch": "vitest",
13.     "lint": "eslint src/"
14.   },
15.   "dependencies": {
16.     "express": "^4.21.0",
17.     "uuid": "^11.1.0"
18.   },
19.   "devDependencies": {
20.     "@types/express": "^5.0.0",
21.     "@types/node": "^22.0.0",
22.     "@types/uuid": "^10.0.0",
23.     "tsx": "^4.19.0",
24.     "typescript": "^5.7.0",
25.     "vitest": "^3.0.0"
26.   }
27. }
```

</details>


---

<sub>⏱️ 53s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\middleware.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\middleware

```
audit-logger.ts
auth.ts
error-handler.ts
```


---

<sub>⏱️ 1m 13s</sub>

### 💬 Copilot

The existing routes cover bulk update (`PUT`) and per-event partial update (`PATCH`), but there's no `GET /notifications/preferences/:eventType` to read preferences for a single event type. I'll add that missing route and its tests.

---

<sub>⏱️ 1m 13s</sub>

### ✅ `edit`

**edit the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\routes\notifications.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\routes\notifications.ts

```
File Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\src\routes\notifications.ts updated with changes.
```


---

<sub>⏱️ 1m 29s</sub>

### 💬 Copilot

Now add tests for the new route's business logic. I'll add a new test describe block to `notifications.test.ts`:

---

<sub>⏱️ 1m 29s</sub>

### ✅ `edit`

**edit the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\tests\notifications.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\tests\notifications.test.ts

```
File Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\02-curate-project-context\tests\notifications.test.ts updated with changes.
```


---

<sub>⏱️ 1m 34s</sub>

### ✅ `powershell`

**Run tests to verify new route and tests pass**

<details>
<summary>Arguments</summary>

```json
{
  "command": "cd \"Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\02-curate-project-context\" && npm test 2>&1",
  "description": "Run tests to verify new route and tests pass",
  "initial_wait": 30
}
```

</details>

```
pm test
> loan-workbench-api@1.0.0 test
> vitest run'vitest' is not recognized as an internal or external command,
operable program or batch file.
<exited with exit code 1>
```


---

<sub>⏱️ 1m 44s</sub>

### ✅ `powershell`

**Install deps then run tests**

<details>
<summary>Arguments</summary>

```json
{
  "command": "cd \"Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\02-curate-project-context\" && npm install --silent && npm test 2>&1",
  "description": "Install deps then run tests",
  "initial_wait": 60
}
```

</details>

<details>
<summary>21 lines</summary>

```
pm install:\Program Files\PowerShell\7\pwsh.exepm test
> loan-workbench-api@1.0.0 test
> vitest run:\WINDOWS\system32\cmd.exe ode (vitest)
 RUN  v3.2.4 Y:/.sources/localm-tuts/courses/_examples/ctx-sdlc/lessons/02-curate-project-contextode (vitest 1)ode (vitest 5)ode (vitest 8)ode (vitest 10)ode (vitest 6)ode (vitest 11)ode (vitest 13)ode (vitest 14) ❯ tests/notifications.test.ts [queued] Test Files 0 passed (2)
      Tests 0 passed (0)
   Start at 21:57:48
   Duration 320ms
 ❯ tests/decisions.test.ts [queued]
 ❯ tests/notifications.test.ts 1/33

 Test Files 0 passed (2)
      Tests 1 passed (33)
   Start at 21:57:48
   Duration 424ms
 ✓ tests/notifications.test.ts (33 tests) 9ms
 ✓ tests/decisions.test.ts (8 tests) 4ms

 Test Files  2 passed (2)
      Tests  41 passed (41)
   Start at  21:57:48
   Duration  542ms (transform 147ms, setup 0ms, collect 209ms, tests 13ms, environment 0ms, prepare 281ms)

ode (vitest 1)ode (vitest 2)⠙
<exited with exit code 0>
```

</details>


---

<sub>⏱️ 1m 52s</sub>

### 💬 Copilot

All 41 tests pass (33 in notifications, 8 in decisions). Here's what was added:

**New route:** `GET /notifications/preferences/:eventType`

- Returns channel preferences (email, SMS) for a **single event type** for the current user
- Applies **first-access default generation** (same as the list endpoint) if the user has no saved prefs
- Accepts an optional `?loanState=` query param to annotate restricted channels (e.g., CA/NY legal holds) filtered to just the requested event
- Respects **delegated sessions** (returns the delegate's prefs, marks `readOnly: true`)
- Validates the `eventType` param against the known event set
- Gated by the `notificationPreferences` feature flag

**6 new tests** covering: event filtering, first-access defaults, role restrictions, state-restriction annotation, and the no-`loanState` case.

---

<sub>Generated by [GitHub Copilot CLI](https://github.com/features/copilot/cli)</sub>
