# Lesson 04 — Planning Workflows — Assessment

> **Model:** `gpt-5.4` · **Duration:** 1m 14s · **Date:** 2026-03-13

## Prompt Under Test

```text
Inspect the relevant docs/, specs/, and existing source surfaces for notification
preferences in this lesson before answering. Discover the architecture, ADR, product,
and NFR context you need rather than assuming a fixed file list. Produce a structured
implementation plan and save it to docs/notification-preferences-plan.md. The plan must
include: summary, source-backed confirmed requirements with references to FR/SC/ADR/NFR
identifiers, open questions with file references, inferred implementation choices
separated from confirmed requirements, constraints and special conditions, numbered
tasks with acceptance criteria and source references, validation steps, and
risks/dependencies. Explicitly call out delegated sessions, LEGAL-218, mandatory-event
delivery, fail-closed audit behavior, degraded-mode fallback, at least one false
positive, and at least one hard negative. If the sources overlap or conflict, identify
the canonical source for the plan and explain why. Do not run shell commands and do not
use SQL.
```

## Scorecard

| #   | Dimension                  | Rating  | Summary                                                               |
| --- | -------------------------- | ------- | --------------------------------------------------------------------- |
| 1   | Context Utilization (CU)   | ✅ PASS | Discovered architecture, ADR, product spec, and NFR docs autonomously |
| 2   | Session Efficiency (SE)    | ✅ PASS | Completed in 1m 14s with ~5 tool calls; single plan artifact produced |
| 3   | Prompt Alignment (PA)      | ✅ PASS | All plan sections present; discovery-first behavior observed          |
| 4   | Change Correctness (CC)    | ✅ PASS | Files match: True · Patterns match: True                              |
| 5   | Objective Completion (OC)  | ✅ PASS | All four lesson objectives demonstrated                               |
| 6   | Behavioral Compliance (BC) | ✅ PASS | No tool boundary violations; read-only discovery phase                |

**Verdict:** ✅ PASS

## 1 · Context Utilization

| Metric                  | Value                                                                          |
| ----------------------- | ------------------------------------------------------------------------------ |
| Context files available | ~10 (copilot-instructions.md, planner agent, 2 prompt files, specs, docs, ADR) |
| Context files read      | ~4 key docs (architecture.md, ADR, product-spec, NFR)                          |
| Key files missed        | None critical                                                                  |
| Context precision       | High — focused on planning inputs, not implementation surfaces                 |

The session performed discovery across `docs/`, `specs/`, and `docs/adr/`
before writing the plan. This mirrors the lesson's emphasis on read-only
planning agents that discover context before proposing actions.

**Evidence** — `.output/logs/session.md` tool calls:

```
### ✅ `view`  — docs/architecture.md
### ✅ `view`  — docs/adr/ADR-001-express-over-fastify.md
### ✅ `view`  — specs/product-spec-notification-preferences.md
### ✅ `view`  — specs/non-functional-requirements.md
```

## 2 · Session Efficiency

| Metric        | Value                        |
| ------------- | ---------------------------- |
| Duration      | 1m 14s                       |
| Tool calls    | ~5                           |
| Lines changed | ~200+ (single plan document) |
| Model         | gpt-5.4                      |

Fast execution for a planning task — produced a comprehensive 200+ line
structured plan document in a single pass.

**Evidence** — `.output/logs/session.md` header:

```
- Duration: 1m 14s
```

## 3 · Prompt Alignment

| Constraint                                              | Respected? |
| ------------------------------------------------------- | ---------- |
| Discover context rather than assume fixed file list     | ✅         |
| Save to docs/notification-preferences-plan.md           | ✅         |
| Include all required plan sections                      | ✅         |
| Call out delegated sessions, LEGAL-218, mandatory-event | ✅         |
| Call out fail-closed audit, degraded-mode fallback      | ✅         |
| Include false positive and hard negative                | ✅         |
| Identify canonical source when overlap/conflict         | ✅         |
| No shell commands or SQL                                | ✅         |

## 4 · Change Correctness

- **Files match:** True
- **Patterns match:** True

| Pattern                      | Matched |
| ---------------------------- | ------- |
| Delegated-session handling   | ✅      |
| LEGAL-218 reference          | ✅      |
| Mandatory-event delivery     | ✅      |
| Fail-closed audit behavior   | ✅      |
| False positive scenario      | ✅      |
| Hard negative scenario       | ✅      |
| Acceptance criteria in tasks | ✅      |

Output: Added `docs/notification-preferences-plan.md` — 22 source-backed
requirements, 5 open questions, 7 inferred choices, 10 numbered tasks with
acceptance criteria and source references.

**Evidence** — `.output/change/comparison.md`:

```
- Files match: True
- Patterns match: True
- Pattern matched: Plan must call out delegated-session behavior
- Pattern matched: Plan must reference LEGAL-218
- Pattern matched: Plan must cover mandatory-event delivery
- Pattern matched: Plan must call out fail-closed audit behavior
- Pattern matched: Plan must identify a false positive
- Pattern matched: Plan must identify a hard negative
- Pattern matched: Plan must include tasks and acceptance criteria
```

**Evidence** — `.output/change/demo.patch` (plan summary section):

```diff
+# Notification Preferences Implementation Plan
+
+## 1. Summary
+
+Implement notification preferences as a pilot-gated, source-of-truth-backed feature
+spanning backend rules/services/routes, frontend state/UI, audit, and observability.
+The feature must let authorized users manage email/SMS per event type while preserving
+mandatory escalation delivery, delegated-session read-only behavior, California decline
+SMS restrictions (`LEGAL-218`), degraded-mode delivery fallback, and fail-closed audit
+semantics.
```

**Evidence** — `.output/change/changed-files.json`:

```json
{ "added": ["docs/notification-preferences-plan.md"], "modified": [], "deleted": [] }
```

## 5 · Objective Completion

| Objective                                                                | Status | Evidence                                                                               |
| ------------------------------------------------------------------------ | ------ | -------------------------------------------------------------------------------------- |
| Explain why AI-assisted planning should be separated from implementation | ✅     | Session was read-only; produced plan document, not code changes                        |
| Use prompt files to standardize recurring planning activities            | ✅     | Lesson includes `plan-feature.prompt.md` and `investigate-bug.prompt.md` templates     |
| Describe how read-only planning agents improve decomposition             | ✅     | Planner agent discovered context and decomposed into 10 tasks with acceptance criteria |
| Design planning workflow that turns vague requests into actionable tasks | ✅     | Plan output includes numbered tasks, source references, open questions, and validation |

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
