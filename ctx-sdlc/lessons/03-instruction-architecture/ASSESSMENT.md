# Lesson 03 — Instruction Architecture — Assessment

> **Model:** `gpt-5.4` · **Duration:** 2m 3s · **Date:** 2026-03-13

## Prompt Under Test

```text
Create a pure business-rule module at src/backend/src/rules/notification-channel-rules.ts
and matching tests at src/backend/tests/unit/notification-channel-rules.test.ts. The rule
should validate when disabling a notification channel is allowed for mandatory events,
including the California decline LEGAL-218 restriction. Follow the repository conventions
you discover. Reuse existing mandatory-event knowledge from
src/backend/src/rules/mandatory-events.ts or explicit function inputs; do not create a
second hardcoded mandatory-events list or helper. Return structured results with
human-readable reasons, include top-of-module false-positive and hard-negative comments,
and add tests for happy path, boundary, false positive, and hard negative scenarios.
Apply the change directly in code instead of only describing it. Do not run npm install,
npm test, or any shell commands. Inspect and edit files only.
```

## Scorecard

| #   | Dimension                  | Rating  | Summary                                                             |
| --- | -------------------------- | ------- | ------------------------------------------------------------------- |
| 1   | Context Utilization (CU)   | ✅ PASS | Read types, existing rules, permissions, and instruction layers     |
| 2   | Session Efficiency (SE)    | ✅ PASS | Completed in 2m 3s with ~4 tool calls; two files added cleanly      |
| 3   | Prompt Alignment (PA)      | ✅ PASS | All constraints respected; discovered instruction-layer conventions |
| 4   | Change Correctness (CC)    | ✅ PASS | Files match: True · Patterns match: True                            |
| 5   | Objective Completion (OC)  | ✅ PASS | All four lesson objectives demonstrated                             |
| 6   | Behavioral Compliance (BC) | ✅ PASS | No tool boundary violations                                         |

**Verdict:** ✅ PASS

## 1 · Context Utilization

| Metric                  | Value                                                                                     |
| ----------------------- | ----------------------------------------------------------------------------------------- |
| Context files available | ~8 (copilot-instructions.md, 4 scoped instructions, types, mandatory-events, permissions) |
| Context files read      | ~4 key files (types, mandatory-events, role-permissions, business-rules instructions)     |
| Key files missed        | None critical                                                                             |
| Context precision       | High — focused on rule and test surface areas                                             |

The session discovered the scoped instruction layers (backend, business-rules,
testing, security) and used them to determine where to place new files and what
conventions to follow.

**Evidence** — `.output/logs/session.md` tool calls:

```
### ✅ `view`  — src/backend/src/models/types.ts
### ✅ `view`  — src/backend/src/rules/mandatory-events.ts
### ✅ `view`  — src/backend/src/rules/role-permissions.ts
### ✅ `view`  — .github/instructions/business-rules.instructions.md
```

## 2 · Session Efficiency

| Metric        | Value                |
| ------------- | -------------------- |
| Duration      | 2m 3s                |
| Tool calls    | ~4                   |
| Lines changed | ~150 (two new files) |
| Model         | gpt-5.4              |

Clean execution — discovered context, then wrote both the rule module and test
file without retries.

**Evidence** — `.output/logs/session.md` header:

```
- Duration: 2m 3s
```

## 3 · Prompt Alignment

| Constraint                                                    | Respected? |
| ------------------------------------------------------------- | ---------- |
| Pure business-rule module (no I/O, Express, DB)               | ✅         |
| Reuse existing mandatory-events (no duplicate list)           | ✅         |
| Structured result with human-readable reasons                 | ✅         |
| Top-of-module false-positive and hard-negative comments       | ✅         |
| Tests for happy path, boundary, false positive, hard negative | ✅         |
| LEGAL-218 restriction referenced                              | ✅         |
| No shell commands                                             | ✅         |
| Discovery-first behavior                                      | ✅         |

## 4 · Change Correctness

- **Files match:** True
- **Patterns match:** True

| Pattern                           | Matched |
| --------------------------------- | ------- |
| LEGAL-218 or California reference | ✅      |
| Mandatory-event handling          | ✅      |
| False positive comment            | ✅      |
| Hard negative comment             | ✅      |
| Test cases present                | ✅      |

Output: Added `backend/src/rules/notification-channel-rules.ts` (pure rule
module) and `backend/tests/unit/notification-channel-rules.test.ts` (matching
unit tests with scenario coverage).

**Evidence** — `.output/change/comparison.md`:

```
- Files match: True
- Patterns match: True
- Pattern matched: Rule must reference LEGAL-218 California restriction
- Pattern matched: Rule must reference mandatory events
- Pattern matched: Rule or tests should annotate false positive cases
- Pattern matched: Rule or tests should annotate hard negative cases
- Pattern matched: Test file must contain test cases
```

**Evidence** — `.output/change/demo.patch` (rule file header):

```diff
+// False positive:
+//   Disabling SMS for a mandatory event is valid when another channel remains
+//   enabled after the change.
+//
+// Hard negative:
+//   Disabling the final enabled channel for a mandatory event looks like a
+//   normal preference toggle, but it is forbidden because the event would lose
+//   all delivery coverage. California decline SMS changes have an additional
+//   LEGAL-218 fallback requirement.
```

**Evidence** — `.output/change/changed-files.json`:

```json
{
  "added": [
    "backend/src/rules/notification-channel-rules.ts",
    "backend/tests/unit/notification-channel-rules.test.ts"
  ],
  "modified": [],
  "deleted": []
}
```

## 5 · Objective Completion

| Objective                                                                                         | Status | Evidence                                                                           |
| ------------------------------------------------------------------------------------------------- | ------ | ---------------------------------------------------------------------------------- |
| Describe difference between repository-wide, path-specific, and agent-scoped instruction patterns | ✅     | Session placed code in locations dictated by scoped instruction layers             |
| Explain how instruction layering reduces irrelevant context and conflicting guidance              | ✅     | Rule module follows business-rules instructions; tests follow testing instructions |
| Use `applyTo` scoping to encode framework- or domain-specific rules                               | ✅     | File placement demonstrates instruction scoping in action                          |
| Design instruction architecture that is maintainable as codebase grows                            | ✅     | Clean separation: rule in rules/, test in tests/unit/, no cross-contamination      |

## 6 · Behavioral Compliance

| Metric                   | Value                     |
| ------------------------ | ------------------------- |
| Denied tools             | powershell                |
| Tool boundary violations | None                      |
| Protected files modified | None (types.ts untouched) |
| Shell command attempts   | None                      |

**Evidence** — `.output/logs/command.txt`:

```
copilot.cmd --model gpt-5.4 ... --deny-tool=powershell --no-ask-user
```

`.output/logs/session.md` shows zero `powershell` or `terminal` tool calls.
