# Lesson 05 — Implementation Workflows — Run Analysis

> **Session ID:** `377dfefc-8ead-414c-bf9d-13331963e788`
> **Model:** `gpt-5.4`
> **Duration:** `5m 58s`
> **Started:** `2026-04-16 13:56:09` · **Ended:** `2026-04-16 14:02:08`

---

## Summary

The April 16 utility-driven run completed the scripted Copilot demo and produced the
expected three-file implementation slice for the lesson.

The captured patch added one pure rule module, one matching unit-test file, and one
focused route edit. The automated comparison under `.output/change/` reported a clean
match for both file shape and required patterns.

The current checked-in workspace also passes the full validator. That means the lesson is
now aligned across all three signals that matter here: prompt intent, patch comparison,
and end-to-end validation.

## Utility Results

| Step    | Command                                 | Result |
| ------- | --------------------------------------- | ------ |
| Demo    | `python util.py --demo --model gpt-5.4` | PASS   |
| Compare | `.output/change/comparison.md`          | PASS   |
| Test    | `python util.py --test`                 | PASS   |

## What the Captured Demo Produced

- `backend/src/rules/notification-preference-write-rules.ts` added
- `backend/tests/unit/notification-preference-write-rules.test.ts` added
- `backend/src/routes/notifications.ts` modified

The route wiring keeps `loanState` as direct request input, uses existing preferences as
explicit rule input, and preserves the existing audit flow after successful writes.

## Comparison Report

The generated comparison file reports:

- `Files match: True`
- `Patterns match: True`

Required patterns verified by the lesson harness:

1. import of the new write-rule module
2. explicit-input write validation using existing preferences
3. LEGAL-218 or California restriction coverage
4. presence of real test cases
5. route wiring that preserves direct `loanState` flow and audited persistence

## Current Validation Result

The checked-in example passes the full validation suite:

- 6 vitest files passed
- 29 backend tests passed
- 13 Playwright UI tests passed

The validation gate specifically proves the business-rule behaviors this lesson cares
about:

1. blocking the last enabled `manual-review-escalation` channel
2. blocking decline SMS for `loanState: "CA"`
3. blocking decline SMS for `loanState: "California"`
4. allowing the false-positive case where escalation SMS is disabled but escalation email stays enabled

## Why This Run Matters

This lesson is about workflow discipline, not about a large feature branch. The useful
result is a small, inspectable change set that survives the real validator after the code
is in place.

That is the implementation pattern the lesson is meant to teach:

- keep the slice small
- keep roles separate
- keep the rules pure
- trust the validation gate, not just the diff
