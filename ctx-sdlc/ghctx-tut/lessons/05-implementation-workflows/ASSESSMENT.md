# Lesson 05 — Implementation Workflows — Assessment

> **Model:** `claude-haiku-4.5` · **Duration:** 2m 38s · **Date:** 2026-04-16

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

| #   | Dimension                  | Rating     | Summary                                                              |
| --- | -------------------------- | ---------- | -------------------------------------------------------------------- |
| 1   | Context Utilization (CU)   | ✅ PASS    | Read the lesson docs, specs, and write surfaces before editing       |
| 2   | Session Efficiency (SE)    | ✅ PASS    | Completed in 2m 38s with a focused three-file change set             |
| 3   | Prompt Alignment (PA)      | ⚠️ PARTIAL | Followed TDD and scope, but changed the route contract to `loanId`   |
| 4   | Change Correctness (CC)    | ❌ FAIL    | Patch matched expectations, but end-to-end validation failed         |
| 5   | Objective Completion (OC)  | ⚠️ PARTIAL | Demonstrated the workflow shape, but not a working end-to-end slice  |
| 6   | Behavioral Compliance (BC) | ✅ PASS    | No tool boundary violations; denied tools respected                  |
| 7   | Context Validation (CV)    | ✅ PASS    | Discovery happened before writes and stayed on lesson-local surfaces |

**Verdict:** ❌ FAIL

## 1 · Context Utilization

| Metric                  | Value                                                                 |
| ----------------------- | --------------------------------------------------------------------- |
| Context files available | Lesson docs, specs, prompts, agents, TDD skill, and notification code |
| Context files read      | Docs, specs, route file, rules, repository, types, and service code   |
| Key files missed        | None material to the narrow implementation slice                      |
| Context precision       | High — reads stayed on the notification write path                    |

**Evidence** — `.output/logs/session.md` tool calls:

```
### ✅ `glob`      — docs/**/*.md
### ✅ `glob`      — specs/**/*.md
### ✅ `view`      — docs/implementation-workflow-example.md
### ✅ `view`      — docs/architecture.md
### ✅ `view`      — specs/product-spec-notification-preferences.md
### ✅ `view`      — src/backend/src/routes/notifications.ts
### ✅ `view`      — src/backend/src/models/preference-repository.ts
### ✅ `view`      — src/backend/src/models/types.ts
```

The session did the required discovery work before editing and stayed close to the
requested notification-preference surfaces.

## 2 · Session Efficiency

| Metric        | Value                                            |
| ------------- | ------------------------------------------------ |
| Duration      | 2m 38s                                           |
| Tool calls    | Focused session with discovery, reads, and edits |
| Lines changed | Three-file implementation slice                  |
| Model         | claude-haiku-4.5                                 |

**Evidence** — `.output/logs/session.md` header:

```
- Session ID: adab9e81-5445-4abe-9a55-f384b52cdd8c
- Started: 16/04/2026, 11:31:53
- Duration: 2m 38s
- Exported: 16/04/2026, 11:34:31
```

The session stayed efficient, but efficiency does not offset behavioral drift that was
only caught by the end-to-end test gate.

## 3 · Prompt Alignment

| Constraint                                                 | Respected?                                   |
| ---------------------------------------------------------- | -------------------------------------------- |
| Discovery-first (inspect before editing)                   | ✅                                           |
| Write tests first                                          | ✅                                           |
| Pure rule module (no DB access)                            | ✅                                           |
| Explicit inputs plus existing types                        | ✅ in the rule module                        |
| Direct `loanState` request input                           | ❌ route changed to optional `loanId` lookup |
| LEGAL-218 California SMS restriction                       | ⚠️ implemented behind the wrong route gate   |
| Escalation channel protection                              | ⚠️ implemented behind the wrong route gate   |
| False positive (SMS disabled, email enabled) stays allowed | ✅                                           |
| Delegated-session and role guards preserved                | ✅                                           |
| No npm/shell commands                                      | ✅                                           |
| No SQL or task/todo write tools                            | ✅                                           |
| Handoff summary with deferred surfaces                     | ✅                                           |

**Evidence** — `.output/logs/command.txt` and post-run validation:

```
C:\Users\nilay\AppData\Roaming\npm\copilot.cmd --model claude-haiku-4.5 ... --deny-tool=powershell --deny-tool=sql ...
```

The prompt-level constraints were mostly respected, but the raw output still violated the
intended request contract by introducing `loanId` lookup semantics.

**Evidence** — `python util.py --test` output after the demo run:

```
FAILED tests\test_ui.py::TestWriteRuleEnforcement::test_mandatory_event_last_channel_blocked
FAILED tests\test_ui.py::TestWriteRuleEnforcement::test_legal_218_ca_decline_sms_blocked
FAILED tests\test_ui.py::TestWriteRuleEnforcement::test_legal_218_california_spelled_out
```

## 4 · Change Correctness

- **Files match:** True
- **Patterns match:** True
- **End-to-end validation after demo:** Failed

| Pattern                                                                       | Matched |
| ----------------------------------------------------------------------------- | ------- |
| Import of notification-preference-write-rules                                 | ✅      |
| Explicit-input preference write validation logic                              | ✅      |
| LEGAL-218 or California reference                                             | ✅      |
| Test cases present                                                            | ✅      |
| Route wiring with direct `loanState` context, explicit inputs, and audit flow | ✅ weak |

**Evidence** — `.output/change/comparison.md`:

```
- Files match: True
- Patterns match: True
- Pattern matched: Route file must import the new write rules
- Pattern matched: Rule must expose explicit-input write validation using existing preferences
- Pattern matched: Rules must reference LEGAL-218 or California restrictions
- Pattern matched: Test file must contain test cases
- Pattern matched: Route wiring should pass direct loanState context, explicit write inputs, and preserve audited flow
```

Automated pattern checks alone were insufficient here. The route patch still passed the
regex checks while changing the write contract in a way that broke the UI-level validation.

**Evidence** — `.output/change/changed-files.json`:

```json
{
  "added": [
    "backend/src/rules/notification-preference-write-rules.ts",
    "backend/tests/unit/notification-preference-write-rules.test.ts"
  ],
  "modified": ["backend/src/routes/notifications.ts"],
  "deleted": []
}
```

Because the raw demo output failed end-to-end behavior checks, this dimension is a fail
despite the manifest and pattern match passing.

## 5 · Objective Completion

| Objective                                                                       | Status | Evidence                                                                         |
| ------------------------------------------------------------------------------- | ------ | -------------------------------------------------------------------------------- |
| Explain how custom agents and skills support role-specialized implementation    | ✅     | Session still followed a discovery → test → implement sequence                   |
| Apply least-privilege principles to implementation and review workflows         | ✅     | Denied tools were respected                                                      |
| Describe how TDD handoffs improve reliability in AI-assisted coding             | ⚠️     | The tester gate mattered, but the raw demo output still failed the behavior gate |
| Design implementation workflow separating planning, coding, and review concerns | ⚠️     | The workflow shape appeared, but the raw output was not end-to-end correct       |

## 6 · Behavioral Compliance

| Metric                   | Value           |
| ------------------------ | --------------- |
| Denied tools             | powershell, sql |
| Tool boundary violations | None            |
| Protected files modified | None            |
| Shell command attempts   | None            |

**Evidence** — `.output/logs/command.txt`:

```
copilot.cmd --model claude-haiku-4.5 --log-dir ... --deny-tool=powershell --deny-tool=sql ...
```

No boundary violations were observed. The failure was semantic, not procedural.

The session read lesson-local context before writing, and the edits stayed confined to the
expected notification preference surfaces.

## Final Assessment

For this prompt, the correct assessment is:

> The raw prompt-driven run should be considered a failure for the end-to-end lesson gate. It produced the expected file shape and stayed within the correct surfaces, but it changed the route contract from direct `loanState` input to optional `loanId` lookup semantics. That drift was not caught by the original patch-shape checks and was only exposed by `python util.py --test`, which failed three rule-enforcement checks.

## Expected Change Comparison

Assessment now also compares actual output against gold-standard expectations:

- `.output/change/expected-files.json` — expected files: `backend/src/rules/notification-preference-write-rules.ts` (added), `backend/tests/unit/notification-preference-write-rules.test.ts` (added), `backend/src/routes/notifications.ts` (modified)
- `.output/change/expected-patterns.json` — required patterns in patch: import, explicit-input validation, LEGAL-218, test coverage, and direct `loanState` flow

The `compare_with_expected()` function writes `.output/change/comparison.md` with a structured match report. The latest rerun produced a full match:

- `Files match: True`
- `Patterns match: True`

## 7 · Context Validation

> When and how was non-system context accessed during the session?

| Metric                          | Value                                                                                                                                                                           |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| First codebase discovery        | Before any code edits                                                                                                                                                           |
| Read pattern                    | Docs and specs first, then route, types, rules, repository, and tests                                                                                                           |
| Files written                   | `src/backend/tests/unit/notification-preference-write-rules.test.ts`, `src/backend/src/rules/notification-preference-write-rules.ts`, `src/backend/src/routes/notifications.ts` |
| Discovery-before-write behavior | Present                                                                                                                                                                         |
| Scope drift                     | Semantic drift at the route contract, not at file-selection level                                                                                                               |

**Validation summary:** The model accessed the right lesson-local context before editing and kept the file selection disciplined. The failure came later, when the route contract drifted from direct `loanState` input to optional `loanId` lookup semantics. That means context access was acceptable, but context application was incomplete.
