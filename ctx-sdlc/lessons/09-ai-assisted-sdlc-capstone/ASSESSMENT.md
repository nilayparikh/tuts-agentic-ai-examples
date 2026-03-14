# Lesson 09 — AI-Assisted SDLC Capstone — Assessment

> **Model:** `gpt-5.4` · **Duration:** 3m 57s · **Date:** 2026-03-14

## Prompt Under Test

```text
Inspect the capstone lesson's project instructions, backend and frontend scoped
instructions, architecture doc, and the relevant backend/frontend notification-preference
surfaces you discover before answering. Do not assume a fixed file list beyond those
starting points. Then implement a notification preference event-channel validator as a
cross-stack hardening slice: 1. Create a pure validation rule module at
backend/src/rules/preference-event-channel-validator.ts that validates event-channel
combinations are allowed, enforcing that mandatory events cannot have all channels
disabled, and respecting LEGAL-218 California SMS restrictions from existing rules.
2. Create unit tests at
backend/tests/unit/preference-event-channel-validator.test.ts covering valid
combinations, mandatory-event violations, and LEGAL-218 false positive and hard negative
cases. 3. Wire the validator import into the existing notification preference write route
in backend/src/routes/notifications.ts. Follow the repository conventions you discover.
Apply the changes directly in code. Do not run npm install, npm test, or any shell
commands. Do not use SQL.
```

## Scorecard

| #   | Dimension                  | Rating  | Summary                                                                           |
| --- | -------------------------- | ------- | --------------------------------------------------------------------------------- |
| 1   | Context Utilization (CU)   | ✅ PASS | Discovered instructions, architecture, and backend/frontend surfaces autonomously |
| 2   | Session Efficiency (SE)    | ✅ PASS | Completed in 3m 57s with ~11 tool calls; three files changed                      |
| 3   | Prompt Alignment (PA)      | ✅ PASS | Discovery-first behavior; all three implementation steps completed                |
| 4   | Change Correctness (CC)    | ✅ PASS | Files match: True · Patterns match: True                                          |
| 5   | Objective Completion (OC)  | ✅ PASS | All five capstone objectives demonstrated                                         |
| 6   | Behavioral Compliance (BC) | ✅ PASS | No tool boundary violations                                                       |

**Verdict:** ✅ PASS

## 1 · Context Utilization

| Metric                  | Value                                                                                                    |
| ----------------------- | -------------------------------------------------------------------------------------------------------- |
| Context files available | ~8 (copilot-instructions.md, api + frontend instructions, architecture, routes, rules, models, services) |
| Context files read      | 6+ (instructions, architecture, backend routes/rules/models, services)                                   |
| Key files missed        | None                                                                                                     |
| Context precision       | High — broad discovery across backend and frontend surfaces                                              |

The capstone session performed the most thorough discovery of any lesson: it
read scoped backend/frontend instructions, architecture docs, existing rules,
models, and services before implementing. This demonstrates the full
curate → plan → build loop.

**Evidence** — `.output/logs/session.md` tool calls:

```
### ✅ `view`  — .github/instructions/copilot-instructions.md
### ✅ `view`  — .github/instructions/backend.instructions.md
### ✅ `view`  — .github/instructions/frontend.instructions.md
### ✅ `view`  — docs/architecture.md
### ✅ `view`  — backend/src/routes/notifications.ts
### ✅ `view`  — backend/src/rules/mandatory-events.ts
### ✅ `view`  — backend/src/models/types.ts
### ✅ `view`  — backend/src/services/audit-service.ts
```

## 2 · Session Efficiency

| Metric        | Value                                     |
| ------------- | ----------------------------------------- |
| Duration      | 3m 57s                                    |
| Tool calls    | ~11                                       |
| Lines changed | ~250 (two new files + route modification) |
| Model         | gpt-5.4                                   |

Longest session in the course, reflecting the capstone's synthesis of all prior
lessons. The higher tool call count shows thorough discovery across multiple
surfaces, which is the intended capstone behavior.

**Evidence** — `.output/logs/session.md` header:

```
- Duration: 3m 57s
```

## 3 · Prompt Alignment

| Constraint                                             | Respected? |
| ------------------------------------------------------ | ---------- |
| Discovery-first (not fixed file list)                  | ✅         |
| Pure validation rule module                            | ✅         |
| Mandatory-event channel enforcement                    | ✅         |
| LEGAL-218 California SMS restriction                   | ✅         |
| Unit tests with false positive and hard negative cases | ✅         |
| Wire validator into existing route                     | ✅         |
| Follow discovered conventions                          | ✅         |
| No shell commands or SQL                               | ✅         |

## 4 · Change Correctness

- **Files match:** True
- **Patterns match:** True

| Pattern                               | Matched |
| ------------------------------------- | ------- |
| Event-channel validation logic        | ✅      |
| Mandatory-event enforcement           | ✅      |
| LEGAL-218 reference                   | ✅      |
| Validator import in route             | ✅      |
| Test cases present                    | ✅      |
| False positive/hard negative handling | ✅      |

Output:

- Added `backend/src/rules/preference-event-channel-validator.ts` — pure rule module
- Added `backend/tests/unit/preference-event-channel-validator.test.ts` — scenario coverage with FP/HN
- Modified `backend/src/routes/notifications.ts` — wired validator import

**Evidence** — `.output/change/comparison.md`:

```
- Files match: True
- Patterns match: True
- Pattern matched: Implementation should add event-channel validation
- Pattern matched: Implementation should enforce mandatory-event constraints
- Pattern matched: Implementation should reference LEGAL-218
- Pattern matched: Route and tests should reference the validator
- Pattern matched: Implementation should add unit tests
- Pattern matched: Tests should annotate false positive and hard negative cases
```

**Evidence** — `.output/change/demo.patch` (route wiring):

```diff
+import { assertPreferenceEventChannelAllowed } from "../rules/preference-event-channel-validator.js";
...
+      assertPreferenceEventChannelAllowed({
+        event,
+        channel,
+        enabled,
+        existingPreferences,
+      });
```

**Evidence** — `.output/change/changed-files.json`:

```json
{
  "added": [
    "backend/src/rules/preference-event-channel-validator.ts",
    "backend/tests/unit/preference-event-channel-validator.test.ts"
  ],
  "modified": [
    "backend/src/routes/notifications.ts"
  ],
  "deleted": []
}
```

## 5 · Objective Completion

| Objective                                                                      | Status | Evidence                                                                                                            |
| ------------------------------------------------------------------------------ | ------ | ------------------------------------------------------------------------------------------------------------------- |
| Synthesize all course layers into single curate → plan → build → validate loop | ✅     | Session discovered context (curate), analyzed surfaces (plan), implemented code (build), and wired tests (validate) |
| Map each customization surface to corresponding SDLC phase                     | ✅     | Instructions/docs = curate; discovery = plan; rule/test/route = build                                               |
| Design minimum viable context stack for teams starting from scratch            | ✅     | Lesson uses minimal .github/ + docs/ + scoped instructions — starter stack                                          |
| Apply progressive complexity principle to sequence team adoption               | ✅     | Capstone builds on all 8 prior lessons, demonstrating progressive layering                                          |
| Evaluate readiness at each adoption stage using quality indicators             | ✅     | File match + pattern match + behavioral compliance serve as quality indicators                                      |

## 6 · Behavioral Compliance

| Metric                   | Value           |
| ------------------------ | --------------- |
| Denied tools             | powershell, sql |
| Tool boundary violations | None            |
| Protected files modified | None            |
| Shell command attempts   | None            |

**Evidence** — `.output/logs/command.txt`:

```
copilot.cmd --model gpt-5.4 ... --deny-tool=powershell --deny-tool=sql --no-ask-user
```

`.output/logs/session.md` shows zero `sql`, `powershell`, or `terminal` tool calls.

## Verdict

Assessment result for this prompt:

- Standards followed: Yes
- Constraints followed: Yes
- Required context applied: Yes

Overall judgment:

- The rerun produced the intended rule-plus-tests-plus-route shape for the capstone.
- The generated change matched both the expected file manifest and the expected behavioral patterns.
- This run is a complete success for the updated lesson objective.

## Final Assessment

For this prompt, the correct assessment is:

> The run should be considered fully successful. It produced the expected cross-stack backend hardening slice, matched the expected file manifest exactly, and covered the required validator, rule, and test behaviors.
