# Lesson 01 — Why Context Engineering Matters — Assessment

> **Model:** claude-haiku-4.5 · **Format:** with-context vs without-context · **Date:** 2025-03-15
> **CLI:** GitHub Copilot CLI 1.0.5 · **Prompt mode:** `--no-ask-user --deny-tool=powershell`

## Prompt Under Test

```text
Implement the manual review escalation workflow for this repository.
Follow existing repo conventions and architecture.
Return the exact files you would change and the code for each change.
Apply the change directly in code instead of only describing it.
Do not run npm install, npm test, or any shell commands. Inspect and edit files only.
```

Same prompt run in two workspace conditions: `with-context/` (curated `.github/`
and `docs/`) vs `without-context/` (bare workspace with only `src/`).

## Scorecard

| # | Dimension | Rating | Summary |
|---|-----------|--------|---------|
| 1 | Context Utilization (CU) | ✅ PASS | With-context read all 3 context docs in first 15s; without-context had none to discover |
| 2 | Session Efficiency (SE) | ✅ PASS | With-context: 25 tool calls, 1m 24s, 3 edits. Without-context: ~40 tool calls, >180s timeout, 11 edits |
| 3 | Prompt Alignment (PA) | ✅ PASS | Same short prompt in both conditions; no constraints violated |
| 4 | Change Correctness (CC) | ✅ PASS | With-context scored 14/14 on rubric; without-context scored 4.5/14 |
| 5 | Objective Completion (OC) | ✅ PASS | All four lesson objectives demonstrated through comparative gap |
| 6 | Behavioral Compliance (BC) | — | Not applicable for manual comparison |

**Verdict:** ✅ PASS

## 1 · Context Utilization

The with-context workspace provides three curated files:

- `.github/copilot-instructions.md` — behavioral guidance
- `docs/architecture.md` — system design and service boundaries
- `docs/manual-review-escalation.md` — workflow-specific hidden spec

The with-context run discovered and read all three docs within the first 15
seconds. Its plan explicitly listed all 14 rubric requirements before writing any
code. The final output reflects route design, service-layer orchestration,
delegated-session rules, queue contract reuse, audit behavior, the California
notification prefix, and the correct response payload shape.

The without-context run had no context to discover. It explored the app source
code extensively (19 file reads, 5 glob searches) and built a plausible but
repo-wrong implementation: new escalation service, new repository, new DB table,
new route file, new lifecycle states. It got some patterns right by reading
existing code (delegated-session checks, audit calls) but missed all
repo-specific requirements that lived only in hidden context.

## 2 · Session Efficiency

| Metric | With Context | Without Context |
|---|---|---|
| Duration | 1m 24s | >3m 00s (timeout) |
| Tool calls (total) | 25 | ~40 |
| Successful calls | 23 | ~34 |
| Failed/denied calls | 2 | ~6 |
| Files read | 20 views | 19 reads + 4 list + 5 glob |
| Files edited | 2 (modified) | 3 modified + 5 created |
| Session exported | ✅ Yes | ❌ No (process killed at timeout) |

The with-context run was 2× faster and made targeted, precise changes. The
without-context run spent more time exploring but produced more — and wrong — code.

## 3 · Prompt Alignment

The prompt is deliberately short and realistic — two sentences of intent plus two
operational constraints (edit files only, no shell commands). This design is
intentional: the lesson demonstrates that **context surfaces hidden rules without
restating them in the prompt**. Both runs received the identical prompt.

## 4 · Change Correctness

Scored against the 14-point rubric in `with-context/docs/experiment.md`:

| # | Requirement | With Context | Without Context | Notes |
|---|---|---|---|---|
| 1 | `POST /api/applications/:id/manual-review` | ✅ | ❌ | Without: `POST /api/escalations` |
| 2 | Route in `routes/applications.ts` | ✅ | ❌ | Without: created `routes/escalations.ts` |
| 3 | Orchestration in `services/loan-service.ts` | ✅ | ❌ | Without: created `services/escalation-service.ts` |
| 4 | Thin route, logic in service layer | ✅ | ❌ | Without: has a service layer but wrong module |
| 5 | Role gate: `analyst-manager` | ✅ | ⚠️ | Without: also expanded to `compliance-reviewer` |
| 6 | Delegated sessions blocked | ✅ | ✅ | Both discovered delegation check from existing code |
| 7 | No loan status transition | ✅ | ❌ | Without: invented pending/approved/rejected/completed states |
| 8 | Reuses `notification.requested` | ✅ | ✅ | Both emitted existing notification event |
| 9 | Event: `manual-review-escalation` | ✅ | ✅ | Both used correct event name |
| 10 | No new queue contract type | ✅ | ❌ | Without: added new escalation queue contracts |
| 11 | Audit the operation | ✅ | ✅ | Both called `auditAction()` |
| 12 | Action: `loan.manual-review-requested` | ✅ | ❌ | Without: used different action name |
| 13 | `[CA-HighRisk]` subject prefix | ✅ | ❌ | Without: no California rule at all |
| 14 | Response: `{ ok, applicationId, notificationEventId }` | ✅ | ❌ | Without: different response shape |

- **With context:** 14/14
- **Without context:** 4.5/14 (counting partial credit for #5)

### Changed Files Summary

| | With Context | Without Context |
|---|---|---|
| Modified | `routes/applications.ts`, `services/loan-service.ts` | `app.ts`, `seed.ts`, `types.ts` |
| Added | — | `escalation-repository.ts`, `escalation-service.ts`, `escalations.ts`, `escalations.test.ts`, `ESCALATION_WORKFLOW.md` |
| Patch size | 3.1 KB | 34.8 KB |

## 5 · Objective Completion

| Objective | Status | Evidence |
|---|---|---|
| Explain why AI-assisted engineering fails without durable project context | ✅ | Without-context run is plausible but wrong in 9.5/14 repo-specific ways |
| Distinguish prompt engineering from durable repository-level context engineering | ✅ | Same prompt, 14/14 vs 4.5/14 based solely on workspace context |
| Describe why context should be treated as engineering infrastructure | ✅ | Three small files drove route design, permissions, audit, queue reuse, and regulatory compliance |
| Position context engineering as foundation for planning, implementation, review, and maintenance | ✅ | Gap spans design (route location), permissions (role gate), audit (action name), queue contracts, state machine, and regulatory nuance (CA prefix) |

## 6 · Behavioral Compliance

Not applicable. Lesson 01 is a comparative experiment, not a single CLI demo.

## Artifacts

| Path | Generated By |
|---|---|
| `with-context/.output/logs/session.md` | Copilot CLI `--share` export |
| `with-context/.output/logs/copilot.log` | Copilot CLI `--log-dir` |
| `with-context/.output/change/demo.patch` | util.py before/after diff |
| `with-context/.output/change/changed-files.json` | util.py file manifest |
| `without-context/.output/logs/copilot.log` | Copilot CLI `--log-dir` |
| `without-context/.output/change/demo.patch` | util.py before/after diff |
| `without-context/.output/change/changed-files.json` | util.py file manifest |

## Caveats & Follow-Ups

- **Without-context scored higher than previous estimate (4.5 vs 2–3).** The
  model discovered some patterns by reading existing code — delegated-session
  checks, audit calls, and the notification.requested event type. This actually
  strengthens the lesson: the gap is not about obvious failures but about
  **repo-specific requirements invisible without context**.
- **With-context scored 14/14** (up from previous estimate of 13/14). It
  correctly returns `notificationEventId` in the response payload.
- **Without-context run timed out** at 180s without exporting `session.md`. Only
  `copilot.log` (runner output) is available for that run.
- Future improvement: create `expected-files.json` and `expected-patterns.json`
  for both scenarios to automate rubric scoring.
