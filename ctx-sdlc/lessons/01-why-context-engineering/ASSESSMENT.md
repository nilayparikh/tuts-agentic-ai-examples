# Lesson 01 — Why Context Engineering Matters — Assessment

> **Model:** comparative (no single model) · **Format:** with-context vs without-context · **Date:** 2026-03-13

## Prompt Under Test

```text
Implement the manual review escalation workflow for this repository.
Follow existing repo conventions and architecture.
Return the exact files you would change and the code for each change.
```

Same prompt run in two workspace conditions: `with-context/` (curated `.github/`
and `docs/`) vs `without-context/` (bare workspace).

## Scorecard

| # | Dimension | Rating | Summary |
|---|-----------|--------|---------|
| 1 | Context Utilization (CU) | ✅ PASS | With-context run discovered hidden repo rules; without-context had none to discover |
| 2 | Session Efficiency (SE) | — | Not applicable for comparative format |
| 3 | Prompt Alignment (PA) | ✅ PASS | Same short prompt in both conditions; no constraints violated |
| 4 | Change Correctness (CC) | ✅ PASS | With-context scored 13/14 on rubric; without-context scored 2–3/14 |
| 5 | Objective Completion (OC) | ✅ PASS | All four lesson objectives demonstrated through comparative gap |
| 6 | Behavioral Compliance (BC) | — | Not applicable for manual comparison |

**Verdict:** ✅ PASS

## 1 · Context Utilization

The with-context workspace provides three curated files:

- `.github/copilot-instructions.md` — behavioral guidance
- `docs/architecture.md` — system design and service boundaries
- `docs/manual-review-escalation.md` — workflow-specific hidden spec

The with-context run consumed all three and produced code that reflects route
design, service-layer orchestration, delegated-session rules, queue contract
reuse, audit behavior, and California-specific notification rules. The
without-context run had no context to discover and defaulted to plausible but
repo-wrong design (new lifecycle state, schema changes, wrong permissions).

## 2 · Session Efficiency

Not applicable. Lesson 01 uses a comparative format, not the standardized
`.output/` bundle. No session duration or tool call data available.

## 3 · Prompt Alignment

The prompt is deliberately short and realistic — three sentences with no
explicit constraints. This design is intentional: the lesson demonstrates that
**context surfaces hidden rules without restating them in the prompt**. Both
runs received the identical prompt.

## 4 · Change Correctness

Scored against the 14-point rubric in `with-context/docs/experiment.md`:

| Requirement | With Context | Without Context |
|---|---|---|
| Correct route path (`POST /api/applications/:id/manual-review`) | ✅ | ❌ |
| Correct route file (`routes/applications.ts`) | ✅ | ⚠️ |
| Correct orchestration file (`services/loan-service.ts`) | ✅ | ❌ |
| Thin route handler, logic in service layer | ✅ | ❌ |
| Correct role gate (`analyst-manager`) | ✅ | ❌ |
| Delegated sessions blocked | ✅ | ❌ |
| No loan status transition | ✅ | ❌ |
| Reuses `notification.requested` | ✅ | ❌ |
| Uses event `manual-review-escalation` | ✅ | ✅ |
| No new queue contract type | ✅ | ✅ |
| Audits the operation | ✅ | ❌ |
| Uses action `loan.manual-review-requested` | ✅ | ❌ |
| Adds `[CA-HighRisk]` subject prefix | ✅ | ❌ |
| Returns expected payload shape | ⚠️ | ❌ |

- **With context:** 13/14
- **Without context:** 2–3/14

## 5 · Objective Completion

| Objective | Status | Evidence |
|---|---|---|
| Explain why AI-assisted engineering fails without durable project context | ✅ | Without-context run is plausible but wrong in 11+ repo-specific ways |
| Distinguish prompt engineering from durable repository-level context engineering | ✅ | Same prompt, dramatically different outcomes based on workspace context |
| Describe why context should be treated as engineering infrastructure | ✅ | Three small files changed architecture, permissions, audit, and regulatory compliance |
| Position context engineering as foundation for planning, implementation, review, and maintenance | ✅ | Gap spans design, permissions, audit, queue usage, and regulatory nuance |

## 6 · Behavioral Compliance

Not applicable. Lesson 01 is a manual comparison, not a CLI-driven demo.

## Caveats & Follow-Ups

- With-context run missed `notificationEventId` in response payload (1/14
  partial). This is a useful teaching point: context improves output
  substantially but does not guarantee perfection.
- Lesson 01 does not yet use the standardized `.output/` artifact bundle.
  Future improvement: capture both runs under consistent artifact layout for
  mechanical comparison.
