# Lesson 01 — Compare Results

This file compares the observed **with-context** and **without-context** runs
for the prompt:

```text
Implement the manual review escalation workflow for this repository.
Follow existing repo conventions and architecture.
Return the exact files you would change and the code for each change.
```

Source of truth for scoring:

- `with-context/docs/experiment.md`
- `with-context/docs/manual-review-escalation.md`

## Verdict

Yes, this example **does win** with context.

The **with-context** run is materially better and clearly more repository-aware.
It follows the intended architecture, keeps the workflow out of the state
machine, reuses the existing queue contract, respects delegated-session rules,
and applies the California high-risk nuance.

The **without-context** run is exactly the kind of failure this lesson is trying
to demonstrate: it is **plausible, confident, and wrong in repo-specific ways**.
It invented a new `escalated` lifecycle state, changed the schema and state
machine, and turned a workflow request into a domain model change.

## Scorecard

Scored against the 14-point rubric in `with-context/docs/experiment.md`.

| Requirement | With Context | Without Context | Notes |
| --- | --- | --- | --- |
| Correct route path: `POST /api/applications/:id/manual-review` | Yes | No | Without-context kept using status transitions instead of a new route. |
| Correct route file: `routes/applications.ts` | Yes | Partial | Without-context changed the correct file, but for the wrong behavior. |
| Correct orchestration file: `services/loan-service.ts` | Yes | No | With-context added service orchestration; without-context did not. |
| Thin route handler, logic in service layer | Yes | No | With-context split route and service correctly. |
| Correct role gate: `analyst-manager` | Yes | No | Without-context expanded permissions toward `compliance-reviewer`. |
| Delegated sessions blocked | Yes | No | With-context explicitly enforced this. |
| No loan status transition | Yes | No | Without-context introduced a new lifecycle state, which is a hard miss. |
| Reuses `notification.requested` | Yes | No | With-context reused the existing event contract. |
| Uses event `manual-review-escalation` | Yes | Yes | Both runs surfaced this event name. |
| No new queue contract type | Yes | Yes | Neither summary indicates a new broker contract was added. |
| Audits the operation | Yes | No | With-context emitted an audit event; without-context summary does not. |
| Uses action `loan.manual-review-requested` | Yes | No | Only the with-context run used the correct action name. |
| Adds `[CA-HighRisk]` subject prefix | Yes | No | This is a strong repo-specific win for with-context. |
| Returns expected payload shape | Partial | No | With-context returned `{ ok, applicationId }` but appears to miss `notificationEventId`. |

## Approximate Scores

- **With context:** 13/14
- **Without context:** 2/14 to 3/14

Why the range for without-context:

- It deserves credit for surfacing `manual-review-escalation`.
- It may deserve partial credit for touching `applications.ts`, but not for the
  correct workflow behavior.
- It should **not** receive credit for architectural correctness, because it
  implemented the wrong concept.

## What The With-Context Run Got Right

The with-context run aligned with the hidden spec in the ways that matter:

1. It added the manual review workflow as a **new endpoint**, not as a state transition.
2. It kept orchestration in `loan-service.ts`, which matches the repo architecture.
3. It respected the delegated-session restriction from auth behavior.
4. It reused the existing `notification.requested` broker contract instead of inventing a new one.
5. It added audit behavior using the repo's existing pattern.
6. It implemented the California-specific `[CA-HighRisk]` subject prefix rule.

This is exactly the kind of outcome the lesson wants to show: the model did not
just produce cleaner code, it discovered **hidden repository rules**.

## What The Without-Context Run Got Wrong

The without-context run drifted into a different design entirely:

1. It introduced a new `escalated` application state.
2. It changed the database schema and lifecycle state machine.
3. It treated escalation as a status transition instead of a side workflow.
4. It widened route permissions in the wrong direction.
5. It missed the delegated-session restriction.
6. It missed the California-specific rule.
7. It did not follow the expected payload shape.

This is a good failure mode for the lesson because it is not random or broken.
It is a **reasonable-sounding implementation that violates repository intent**.

## Is The Example Strong Enough?

Yes. This comparison now demonstrates the difference clearly.

The gap is not cosmetic. The two runs disagree on:

- domain model shape
- route design
- service boundaries
- permission model
- queue usage
- audit behavior
- regulatory nuance

That is a strong context-engineering lesson.

## One Remaining Miss In The With-Context Run

The with-context run appears to miss one detail from the hidden spec:

- expected response payload should include `notificationEventId`

So the contextual run is not perfect, but it is still decisively better than the
baseline. In fact, that imperfection helps the lesson: context improves the
answer substantially, but does not guarantee total correctness.

## Recommended Framing For The Lesson

Use this summary when presenting the result:

> Without context, Gemini Flash produced a plausible implementation by changing
> the application's lifecycle and schema. With context, it discovered that
> manual review escalation is not a new state at all, but a side workflow with
> a specific route, service-layer orchestration, delegated-session restrictions,
> audit behavior, queue contract reuse, and California-specific notification
> rules.

## Recommendation

Keep this example.

If you want to make it even sharper, the next improvement is small:

- update the hidden spec or evaluation notes to call out `notificationEventId`
  more prominently, since that is the one place where the with-context run still
  fell short.
