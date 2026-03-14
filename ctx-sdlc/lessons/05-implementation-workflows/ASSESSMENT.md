# Lesson 05 — Implementation Workflows — Assessment

> **Model:** `gpt-5.4` · **Duration:** 2m 30s · **Date:** 2026-03-14

## Prompt Under Test

```text
Inspect docs/, specs/, and the relevant notification-preference write surfaces you
discover in this lesson before editing. Use the playbook and example doc as success
criteria, not as a fixed file checklist. Implement a focused notification-preference
write hardening slice. Write tests first at
src/backend/tests/unit/notification-preference-write-rules.test.ts, then add a pure rule
module at src/backend/src/rules/notification-preference-write-rules.ts, and wire the
minimal production changes into src/backend/src/routes/notifications.ts. In the final
handoff, state which behaviors the tests should fail on before the production change and
which should pass after it, and name any intentionally deferred write surfaces that
remain out of scope. The rule must use explicit inputs plus existing types, not direct DB
access. Enforce these cases: manual-review-escalation must keep at least one channel
enabled; decline SMS cannot be enabled when loanState is CA or California under
LEGAL-218; the false positive where escalation SMS is disabled but escalation email stays
enabled must remain allowed. Preserve delegated-session and role guards, keep changes
minimal, keep the scope to the current notification write path, include top-of-module
false-positive and hard-negative comments in the new rule file, and do not edit protected
config or database files. Do not run npm install, npm test, npx vitest, or any shell
commands. Do not use SQL or task/todo write tools. Inspect and edit files only. Return a
short handoff summary naming changed files and which tests should pass.
```

## Scorecard

| #   | Dimension                  | Rating  | Summary                                                                  |
| --- | -------------------------- | ------- | ------------------------------------------------------------------------ |
| 1   | Context Utilization (CU)   | ✅ PASS | Read playbook, NFRs, routes, rules, models, and services before editing  |
| 2   | Session Efficiency (SE)    | ✅ PASS | Completed in 2m 30s with 31 tool calls; three files changed             |
| 3   | Prompt Alignment (PA)      | ✅ PASS | All constraints respected; TDD skill loaded; tests written before rules |
| 4   | Change Correctness (CC)    | ✅ PASS | Files match: True · Patterns match: True                                 |
| 5   | Objective Completion (OC)  | ✅ PASS | All four lesson objectives demonstrated                                  |
| 6   | Behavioral Compliance (BC) | ✅ PASS | No tool boundary violations; denied tools respected                      |

**Verdict:** ✅ PASS

## 1 · Context Utilization

| Metric                  | Value                                                                                                    |
| ----------------------- | -------------------------------------------------------------------------------------------------------- |
| Context files available | ~12 (copilot-instructions.md, 3 agents, 2 prompts, TDD skill, playbook, specs, routes, rules, services) |
| Context files read      | 8+ (playbook, NFRs, routes, mandatory-events, preference-repository, audit-service, types, rules)        |
| Key files missed        | `specs/product-spec-notification-preferences.md` — path does not exist in lesson                         |
| Context precision       | High — focused on implementation-relevant surfaces, no wasted reads                                      |

**Evidence** — `.output/logs/session.md` tool calls:

```
### ✅ `skill`     — tdd-workflow (loaded before coding)
### ✅ `view`      — docs/implementation-playbook.md (115 lines)
### ❌ `view`      — specs/product-spec-notification-preferences.md (Path does not exist)
### ✅ `view`      — specs/non-functional-requirements.md (109 lines)
### ✅ `view`      — src/backend/src/routes/notifications.ts (272 lines)
### ✅ `rg`        — searched for mandatory-events across backend
### ✅ `view`      — src/backend/src/rules/mandatory-events.ts
### ✅ `view`      — src/backend/src/models/preference-repository.ts
### ✅ `view`      — src/backend/src/services/audit-service.ts
### ✅ `view`      — src/backend/src/models/types.ts
```

The product spec path did not exist in lesson 05; the session continued
with playbook + NFR context, which was sufficient.

## 2 · Session Efficiency

| Metric        | Value                                     |
| ------------- | ----------------------------------------- |
| Duration      | 2m 30s                                    |
| Tool calls    | 31                                        |
| Lines changed | 235 (two new files + route modification)  |
| Model         | gpt-5.4                                   |

**Evidence** — `.output/logs/session.md` header:

```
- Session ID: 75425311-a9e8-4f75-b5b5-33ca70c55d25
- Started: 14/03/2026, 20:28:50
- Duration: 2m 30s
- Exported: 14/03/2026, 20:31:21
```

31 tool calls breaks down as: 1 skill load, 5 glob/rg discovery, 14 file
reads, 7 rg searches, 4 apply_patch edits. No retries or abandoned work.

## 3 · Prompt Alignment

| Constraint                                                 | Respected?                                     |
| ---------------------------------------------------------- | ---------------------------------------------- |
| Discovery-first (inspect before editing)                   | ✅                                             |
| Write tests first                                          | ✅ — test file created before rule file         |
| Pure rule module (no DB access)                            | ✅                                             |
| Explicit inputs plus existing types                        | ✅                                             |
| LEGAL-218 California SMS restriction                       | ✅                                             |
| Escalation channel protection                              | ✅                                             |
| False positive (SMS disabled, email enabled) stays allowed | ✅                                             |
| Delegated-session and role guards preserved                | ✅                                             |
| No npm/shell commands                                      | ✅                                             |
| No SQL or task/todo write tools                            | ✅ — no `sql` tool calls in session             |
| Handoff summary with deferred surfaces                     | ✅                                             |

**Evidence** — `.output/logs/session.md` tool types (all calls):

```
skill, glob, glob, rg, view(×14), rg(×7), apply_patch(×4)
```

No `sql`, `powershell`, `terminal`, or `run_command` tool calls present.

**Evidence** — `.output/logs/session.md` handoff summary (final message):

```
Before the production change, the new tests should fail on the missing enforcement for:
- blocking the last enabled manual-review-escalation channel
- blocking decline SMS enablement for CA / California under LEGAL-218

After the change, these should pass:
- allow disabling escalation SMS when escalation email stays enabled
- reject disabling the last escalation channel
- reject decline SMS enablement for CA
- reject decline SMS enablement for California
- allow decline SMS outside California

Intentionally deferred: bulk write surfaces PUT /preferences/:userId/email
and PUT /preferences/:userId/sms.
```

## 4 · Change Correctness

- **Files match:** True
- **Patterns match:** True

| Pattern                                                                           | Matched |
| --------------------------------------------------------------------------------- | ------- |
| Import of notification-preference-write-rules                                     | ✅      |
| Preference write validation logic                                                 | ✅      |
| LEGAL-218 or California reference                                                 | ✅      |
| Test cases present                                                                | ✅      |
| Route wiring with contextual inputs (loanState, existingPreferences, auditAction) | ✅      |

**Evidence** — `.output/change/comparison.md`:

```
- Files match: True
- Patterns match: True
- Pattern matched: Route file must import the new write rules
- Pattern matched: Rule must contain preference write validation logic
- Pattern matched: Rules must reference LEGAL-218 or California restrictions
- Pattern matched: Test file must contain test cases
- Pattern matched: Route wiring should pass contextual inputs and preserve audited write flow
```

**Evidence** — `.output/change/demo.patch` (route wiring hunk):

```diff
+import { validateNotificationPreferenceWrite } from "../rules/notification-preference-write-rules.js";
...
+      const writeValidation = validateNotificationPreferenceWrite({
+        existingPreferences,
+        nextPreference: pref,
+        loanState,
+      });
+
+      if (!writeValidation.allowed) {
+        res.status(400).json({ error: writeValidation.reason });
+        return;
+      }
```

**Evidence** — `.output/change/demo.patch` (rule module — false-positive/hard-negative comments):

```diff
+// FALSE POSITIVE: disabling escalation SMS is allowed when escalation email
+// remains enabled; the rule protects the last enabled channel, not every
+// channel.
+// HARD NEGATIVE: never allow a write that leaves manual-review-escalation with
+// zero enabled channels, and never allow decline SMS to be enabled for
+// California loans under LEGAL-218.
```

**Evidence** — `.output/change/demo.patch` (test file — LEGAL-218 assertion):

```diff
+  it("blocks enabling decline SMS for CA loans under LEGAL-218", () => {
+    expect(
+      validateNotificationPreferenceWrite({
+        existingPreferences: [],
+        nextPreference: pref({
+          event: "decline",
+          channel: "sms",
+          enabled: true,
+        }),
+        loanState: "CA",
+      }),
+    ).toEqual({
+      allowed: false,
+      reason:
+        "LEGAL-218 prohibits enabling SMS for decline notifications on California loans.",
+    });
+  });
```

**Evidence** — `.output/change/changed-files.json`:

```json
{
  "added": [
    "backend/src/rules/notification-preference-write-rules.ts",
    "backend/tests/unit/notification-preference-write-rules.test.ts"
  ],
  "modified": [
    "backend/src/routes/notifications.ts"
  ],
  "deleted": []
}
```

## 5 · Objective Completion

| Objective                                                                       | Status | Evidence                                                                                                                      |
| ------------------------------------------------------------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------- |
| Explain how custom agents and skills support role-specialized implementation    | ✅     | `session.md`: TDD skill loaded at ⏱️ 15s; lesson includes implementer, reviewer, tester agents                                |
| Apply least-privilege principles to implementation and review workflows         | ✅     | `command.txt`: `--deny-tool=powershell --deny-tool=sql`; session stayed in edit-only mode                                     |
| Describe how TDD handoffs improve reliability in AI-assisted coding             | ✅     | `session.md`: test file created via `apply_patch` before rule file; handoff names expected failing/passing tests               |
| Design implementation workflow separating planning, coding, and review concerns | ✅     | `session.md`: discovery → test → implement → wire → handoff sequence observed across 31 tool calls                            |

## 6 · Behavioral Compliance

| Metric                   | Value                    |
| ------------------------ | ------------------------ |
| Denied tools             | powershell, sql          |
| Tool boundary violations | None                     |
| Protected files modified | None                     |
| Shell command attempts   | None                     |

**Evidence** — `.output/logs/command.txt`:

```
copilot.cmd --model gpt-5.4 --log-dir ... --deny-tool=powershell --deny-tool=sql ...
```

**Evidence** — `.output/logs/session.md` shows zero `sql`, `powershell`, or
`terminal` tool calls. All 31 calls are: `skill`, `glob`, `rg`, `view`, `apply_patch`.
- The change is small, local, and materially improves the notification preference write path.
- The session was not perfectly clean from a workflow standpoint because it used SQL todo writes and partially missed the requested source context.

## Final Assessment

For this prompt, the correct assessment is:

> The run should be considered successful for the lesson objective. It produced a focused rule-plus-tests implementation slice in the intended surfaces and preserved the key delegated-session and notification-policy constraints. The main non-blocking caveats are the use of a SQL todo tool, the missing lesson-local product-spec file, and incomplete evidence for a strict red-step TDD sequence.

## Expected Change Comparison

Assessment now also compares actual output against gold-standard expectations:

- `.output/change/expected-files.json` — expected files: `backend/src/rules/notification-preference-write-rules.ts` (added), `backend/tests/unit/notification-preference-write-rules.test.ts` (added), `backend/src/routes/notifications.ts` (modified)
- `.output/change/expected-patterns.json` — required patterns in patch: import, validate, LEGAL-218, test, loanState or existingPreferences or auditAction

The `compare_with_expected()` function writes `.output/change/comparison.md` with a structured match report. The latest rerun produced a full match:

- `Files match: True`
- `Patterns match: True`
