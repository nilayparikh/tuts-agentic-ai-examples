# Lesson 05 — Implementation Workflows — Assessment

> **Model:** `gpt-5.4` · **Duration:** `5m 58s` · **Date:** `2026-04-16`

## Prompt Under Test

```text
Inspect docs/, specs/, and the relevant notification-preference write surfaces you discover in this lesson before editing. Use the playbook and example doc as success criteria, not as a fixed file checklist. Implement a focused notification-preference write hardening slice. Write tests first at src/backend/tests/unit/notification-preference-write-rules.test.ts, then add a pure rule module at src/backend/src/rules/notification-preference-write-rules.ts, and wire the minimal production changes into src/backend/src/routes/notifications.ts. In the final handoff, state which behaviors the tests should fail on before the production change and which should pass after it, and name any intentionally deferred write surfaces that remain out of scope. The rule must use explicit inputs plus existing types, not direct DB access. Enforce these cases: manual-review-escalation must keep at least one channel enabled; decline SMS cannot be enabled when loanState is CA or California under LEGAL-218; treat loanState as the direct request input for this route instead of introducing a new loanId lookup or any repository fetch; the false positive where escalation SMS is disabled but escalation email stays enabled must remain allowed. When tests assert business-rule rejections, prefer semantic checks over brittle exact wording, and preserve the current route rejection style when practical; if the route returns 400 or 422 for these rule violations, the payload must still clearly express the business invariant. Preserve delegated-session and role guards, keep changes minimal, keep the scope to the current notification write path, include top-of-module false-positive and hard-negative comments in the new rule file, and do not edit protected config or database files. Do not run npm install, npm test, npx vitest, or any shell commands. Do not use SQL or task/todo write tools. Inspect and edit files only. Return a short handoff summary naming changed files and which tests should pass.
```

## Scorecard

| #   | Dimension                  | Rating  | Summary                                                                        |
| --- | -------------------------- | ------- | ------------------------------------------------------------------------------ |
| 1   | Context Utilization (CU)   | ✅ PASS | Read lesson docs, specs, and implementation surfaces before editing            |
| 2   | Session Efficiency (SE)    | ✅ PASS | Completed in 5m 58s with a focused three-file change set                       |
| 3   | Prompt Alignment (PA)      | ✅ PASS | The generated patch respected the requested direct `loanState` contract        |
| 4   | Change Correctness (CC)    | ✅ PASS | Files match: True · Patterns match: True                                       |
| 5   | Objective Completion (OC)  | ✅ PASS | The prompt-driven output demonstrates the intended narrow implementation slice |
| 6   | Behavioral Compliance (BC) | ✅ PASS | No tool boundary violations; denied tools respected                            |
| 7   | Context Validation (CV)    | ✅ PASS | Discovery happened before writes and stayed on lesson-local surfaces           |

**Verdict:** ✅ PASS

## 1 · Context Utilization

| Metric                  | Value                                                                 |
| ----------------------- | --------------------------------------------------------------------- |
| Context files available | Lesson docs, specs, prompts, agents, TDD skill, and notification code |
| Context files read      | Docs, specs, route file, repository/types surfaces, and tests         |
| Key files missed        | None material to the narrow implementation slice                      |
| Context precision       | High — reads stayed on the notification write path                    |

**Evidence** — `.output/logs/session.md` shows discovery over `docs/`, `specs/`, and the
route and model surfaces before edits were made.

The session did the required discovery work before editing and stayed close to the
requested notification-preference surfaces.

## 2 · Session Efficiency

| Metric        | Value                                            |
| ------------- | ------------------------------------------------ |
| Duration      | 5m 58s                                           |
| Tool calls    | Focused session with discovery, reads, and edits |
| Lines changed | Three-file implementation slice                  |
| Model         | gpt-5.4                                          |

**Evidence** — `.output/logs/session.md` header:

```text
- Session ID: 377dfefc-8ead-414c-bf9d-13331963e788
- Started: 16/04/2026, 13:56:09
- Duration: 5m 58s
- Exported: 16/04/2026, 14:02:08
```

The run remained narrow and produced only the files the lesson expected.

## 3 · Prompt Alignment

| Constraint                                                 | Respected? |
| ---------------------------------------------------------- | ---------- |
| Discovery-first (inspect before editing)                   | ✅         |
| Write tests first                                          | ✅         |
| Pure rule module (no DB access)                            | ✅         |
| Explicit inputs plus existing types                        | ✅         |
| Direct `loanState` request input                           | ✅         |
| LEGAL-218 California SMS restriction                       | ✅         |
| Escalation channel protection                              | ✅         |
| False positive (SMS disabled, email enabled) stays allowed | ✅         |
| Delegated-session and role guards preserved                | ✅         |
| No npm/shell commands                                      | ✅         |
| No SQL or task/todo write tools                            | ✅         |
| Handoff summary with deferred surfaces                     | ✅         |

**Evidence** — `.output/logs/command.txt` shows `--deny-tool=powershell` and
`--deny-tool=sql`, while the captured patch keeps `loanState` in direct route input and
does not introduce a repository lookup contract.

## 4 · Change Correctness

- **Files match:** True
- **Patterns match:** True

| Pattern                                                                       | Matched |
| ----------------------------------------------------------------------------- | ------- |
| Import of notification-preference-write-rules                                 | ✅      |
| Explicit-input preference write validation logic                              | ✅      |
| LEGAL-218 or California reference                                             | ✅      |
| Test cases present                                                            | ✅      |
| Route wiring with direct `loanState` context, explicit inputs, and audit flow | ✅      |

**Evidence** — `.output/change/comparison.md`:

```text
- Files match: True
- Patterns match: True
- Pattern matched: Route file must import the new write rules
- Pattern matched: Rule must expose explicit-input write validation using existing preferences
- Pattern matched: Rules must reference LEGAL-218 or California restrictions
- Pattern matched: Test file must contain test cases
- Pattern matched: Route wiring should pass direct loanState context, explicit write inputs, and preserve audited flow
```

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

On the narrow assessment scope for prompt-driven changes, the patch satisfies the lesson's
required standards, constraints, and expected output shape.

## 5 · Objective Completion

| Objective                                                                       | Status | Evidence                                                                  |
| ------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------------- |
| Explain how custom agents and skills support role-specialized implementation    | ✅     | The run follows the expected test, implement, and handoff shape           |
| Apply least-privilege principles to implementation and review workflows         | ✅     | Denied tools were respected                                               |
| Describe how TDD handoffs improve reliability in AI-assisted coding             | ✅     | The generated tests, rule file, and handoff all encode red/green behavior |
| Design implementation workflow separating planning, coding, and review concerns | ✅     | The output stays within a narrow three-file implementation slice          |

## 6 · Behavioral Compliance

| Metric                   | Value           |
| ------------------------ | --------------- |
| Denied tools             | powershell, sql |
| Tool boundary violations | None            |
| Protected files modified | None            |
| Shell command attempts   | None            |

**Evidence** — `.output/logs/command.txt`:

```text
copilot.cmd --model gpt-5.4 ... --deny-tool=powershell --deny-tool=sql ...
```

No boundary violations were observed. The session stayed within the allowed file-editing
workflow.

## Final Assessment

For this prompt, the correct assessment is:

> The prompt-driven run should be considered successful. It discovered the right lesson-local context, produced the expected three-file implementation slice, preserved the direct `loanState` request contract, and satisfied the lesson's required file and pattern checks without violating tool boundaries.

## Expected Change Comparison

Assessment compares actual output against the lesson's gold-standard expectations:

- `.output/change/expected-files.json` — expected files for the narrow implementation slice
- `.output/change/expected-patterns.json` — required patterns for import, explicit-input validation, LEGAL-218 coverage, tests, and direct route wiring

The `compare_with_expected()` function writes `.output/change/comparison.md` with a
structured match report. The latest captured run produced a full match:

- `Files match: True`
- `Patterns match: True`

## 7 · Context Validation

> When and how was non-system context accessed during the session?

| Metric                          | Value                                                                                                                                                                           |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| First codebase discovery        | Before any code edits                                                                                                                                                           |
| Read pattern                    | Docs and specs first, then route and supporting backend surfaces                                                                                                                |
| Files written                   | `src/backend/tests/unit/notification-preference-write-rules.test.ts`, `src/backend/src/rules/notification-preference-write-rules.ts`, `src/backend/src/routes/notifications.ts` |
| Discovery-before-write behavior | Present                                                                                                                                                                         |
| Scope drift                     | None material to the requested lesson slice                                                                                                                                     |

**Validation summary:** The model accessed the right lesson-local context before editing, kept the file selection disciplined, and produced a patch that aligns with the lesson's required standards and scope.
