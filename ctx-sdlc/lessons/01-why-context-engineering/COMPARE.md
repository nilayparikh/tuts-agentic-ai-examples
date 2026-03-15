# Lesson 01 — Compare Results

> **Model:** claude-haiku-4.5 · **CLI:** GitHub Copilot CLI 1.0.5 · **Date:** 2025-03-15

This file compares the observed **with-context** and **without-context** runs
for the prompt:

```text
Implement the manual review escalation workflow for this repository.
Follow existing repo conventions and architecture.
Return the exact files you would change and the code for each change.
Apply the change directly in code instead of only describing it.
Do not run npm install, npm test, or any shell commands. Inspect and edit files only.
```

Source of truth for scoring:

- `with-context/docs/experiment.md`
- `with-context/docs/manual-review-escalation.md`

## Verdict

Yes, this example **does win** with context.

The **with-context** run scored **14/14** — a perfect hit on every rubric item.
It discovered the hidden spec within 15 seconds, planned against all 14
requirements, and surgically modified only the 2 correct files in 1 minute 24
seconds.

The **without-context** run scored **4.5/14** and is exactly the kind of failure
this lesson is designed to demonstrate: **plausible, confident, and wrong in
repo-specific ways**. It created 5 new files and a new escalation subsystem with
its own DB table, lifecycle states, repository, service, and route file — when
the correct answer was to add 27 lines to one route and 65 lines to one service.

## Scorecard

Scored against the 14-point rubric in `with-context/docs/experiment.md`.

| # | Requirement | With Context | Without Context | Notes |
|---|---|---|---|---|
| 1 | `POST /api/applications/:id/manual-review` | ✅ | ❌ | Without: `POST /api/escalations` |
| 2 | Route in `routes/applications.ts` | ✅ | ❌ | Without: created `routes/escalations.ts` |
| 3 | Orchestration in `services/loan-service.ts` | ✅ | ❌ | Without: created `services/escalation-service.ts` |
| 4 | Thin route, logic in service | ✅ | ❌ | Without: has service but wrong module |
| 5 | Role gate: `analyst-manager` | ✅ | ⚠️ | Without: expanded to `compliance-reviewer` too |
| 6 | Delegated sessions blocked | ✅ | ✅ | Both discovered from existing code patterns |
| 7 | No loan status transition | ✅ | ❌ | Without: invented pending/approved/rejected/completed |
| 8 | Reuses `notification.requested` | ✅ | ✅ | Both reused existing event |
| 9 | Event: `manual-review-escalation` | ✅ | ✅ | Both used correct event name |
| 10 | No new queue contract | ✅ | ❌ | Without: added escalation contracts + new DB table |
| 11 | Audit the operation | ✅ | ✅ | Both called `auditAction()` |
| 12 | Action: `loan.manual-review-requested` | ✅ | ❌ | Without: used different action name |
| 13 | `[CA-HighRisk]` subject prefix | ✅ | ❌ | Without: no California rule at all |
| 14 | Response: `{ ok, applicationId, notificationEventId }` | ✅ | ❌ | Without: different response shape |

## Scores

- **With context:** 14/14
- **Without context:** 4.5/14 (partial credit for #5)

The without-context run scored higher than earlier estimates (4.5 vs 2–3) because
it discovered some patterns from existing code: delegated-session checks, the
`notification.requested` event, the `manual-review-escalation` event name, and
`auditAction()` calls. These 4 correct items came from code conventions, not
project context — which actually strengthens the lesson's point: context provides
the **repo-specific** requirements that code-reading alone cannot surface.

## What The With-Context Run Got Right

The with-context run achieved a perfect 14/14:

1. Added manual review as a **new POST endpoint** on `applications.ts`, not a state transition
2. Kept orchestration in `loan-service.ts` matching repo architecture
3. Respected delegated-session restriction from auth behavior
4. Reused existing `notification.requested` broker contract
5. Added audit with correct action name `loan.manual-review-requested`
6. Implemented California `[CA-HighRisk]` prefix with feature flag + state + amount check
7. Returns `{ ok, applicationId, notificationEventId }` — correct payload shape
8. Only modified 2 files (3.1 KB patch) — no new files, no schema changes

The model read the hidden spec at T+15s and planned against all 14 requirements
before writing any code. Session duration: 1 minute 24 seconds.

## What The Without-Context Run Got Wrong

The without-context run built an entirely different system (34.8 KB patch, 5 new files):

1. Created a new `routes/escalations.ts` instead of adding to `applications.ts`
2. Created a new `escalation-service.ts` instead of using `loan-service.ts`
3. Created a new `escalation-repository.ts` with its own SQL table
4. Invented four new lifecycle states: `pending`, `approved`, `rejected`, `completed`
5. Expanded permissions to include `compliance-reviewer`
6. Used a different audit action name
7. Missed the California `[CA-HighRisk]` rule entirely
8. Produced a different response shape

What it got right (by reading existing code): delegated-session blocking,
`notification.requested` event reuse, `manual-review-escalation` event name,
and `auditAction()` calls. These 4 correct items all came from code conventions
visible in the source — not from project context.

## Is The Example Strong Enough?

Yes — stronger than previous estimates.

The gap is not cosmetic. The two runs disagree on:

- **domain model shape** (2 files modified vs 5 files created + 3 modified)
- **route design** (`/:id/manual-review` on applications vs new `/escalations`)
- **service boundaries** (loan-service vs new escalation-service + repository)
- **permission model** (`analyst-manager` only vs `analyst-manager` + `compliance-reviewer`)
- **queue usage** (reuse `notification.requested` vs add new escalation contracts)
- **audit behavior** (correct action name vs different action)
- **regulatory nuance** (`[CA-HighRisk]` prefix vs nothing)
- **state machine** (no status change vs 4 new lifecycle states)

The without-context run is actually **more impressive but more wrong** — it
built a complete escalation subsystem with DB schema, repository, service,
tests, and docs. This makes the lesson point even sharper: raw capability
without context produces confident, well-structured, wrong code.

## One Improvement From The With-Context Run

The with-context run now achieves **14/14** — it correctly returns
`notificationEventId` in the response payload. Previous estimates had this at
13/14 (partial miss). This was achieved by using the curated `docs/` files that
specify the exact response shape.

## Recommended Framing For The Lesson

Use this summary when presenting the result:

> Without context, claude-haiku-4.5 built an impressive new escalation subsystem
> with its own database table, repository, service, route file, and lifecycle
> states — 34.8 KB of confident, well-structured code that violates 9.5 of 14
> repository-specific requirements. With context, the same model read the hidden
> spec in 15 seconds and produced a surgical 3.1 KB patch that modifies only the
> 2 correct files and scores 14/14.

## Recommendation

Keep this example. The contrast is now backed by real CLI session data.

Future improvements:
- Add `expected-files.json` and `expected-patterns.json` to both scenarios for
  automated rubric scoring
- Create `compare_outputs.py` script (referenced in README but not yet built)
