# Lesson 01 Experiment — Gemini Flash Comparison

This experiment is designed for fast models such as Gemini Flash, where simple
prompts often produce similar-looking answers.

## Same Prompt, Two Context Conditions

Use this exact prompt in both runs:

```text
Implement the manual review escalation workflow for this repository.
Follow existing repo conventions and architecture.
Return the exact files you would change and the code for each change.
```

## Run A — Without Context

Use one of these setups:

- blank chat with no workspace files attached
- workspace opened at `src/` only
- a copy of the app without lesson guidance

Expected result: the answer looks plausible but drifts from repo rules.

## Run B — With Context

Open the lesson workspace with both of these folders visible:

- `src/`
- `with-context/`

Expected result: the answer follows the hidden workflow spec.

## Scoring Rubric

Give 1 point for each requirement the model gets right without being told in the
prompt.

1. Correct route path: `POST /api/applications/:id/manual-review`
2. Correct route file: `routes/applications.ts`
3. Correct orchestration file: `services/loan-service.ts`
4. Thin route handler, logic in service layer
5. Correct role gate: `analyst-manager`
6. Delegated sessions blocked
7. No loan status transition
8. Reuses `notification.requested`
9. Uses event `manual-review-escalation`
10. No new queue contract type
11. Audits the operation
12. Uses action `loan.manual-review-requested`
13. Adds `[CA-HighRisk]` subject prefix for qualifying California loans
14. Returns the expected payload shape

## Interpreting Results

- `0-4`: mostly generic output
- `5-9`: partial repo awareness
- `10-14`: strong context utilization

A useful lesson result is not that the without-context answer is nonsense.
It is that it is **confidently plausible but wrong in repo-specific ways**.
