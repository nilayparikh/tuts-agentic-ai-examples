# Lesson 05 — Implementation Workflows — Run Analysis

> **Session ID:** `adab9e81-5445-4abe-9a55-f384b52cdd8c`
> **Model:** `claude-haiku-4.5`
> **Duration:** 2m 38s
> **Started:** 2026-04-16 11:31:53 · **Ended:** 2026-04-16 11:34:31

---

## Summary

The April 16 utility-driven run completed the scripted Copilot demo and produced the
expected three-file change shape. The automated patch comparison reported a clean match.

The important result came from the next gate: `python util.py --test` exposed that the
raw demo output drifted away from the intended route contract. Instead of keeping
`loanState` as the direct request input, the generated route added an optional `loanId`
lookup path and only applied the write rule when that lookup was supplied.

That meant the generated code looked structurally correct but failed the actual behavior
the lesson is meant to enforce.

## Utility Results

| Step    | Command                 | Result |
| ------- | ----------------------- | ------ |
| Demo    | `python util.py --demo` | PASS   |
| Compare | `.output/change/*`      | PASS   |
| Test    | `python util.py --test` | FAIL   |

## What Passed

- The session discovered lesson docs, specs, and the notification surfaces before editing.
- The change set stayed within the intended three files.
- The model wrote tests plus a pure rule module and updated the route.
- The patch still satisfied the current expected-files and expected-pattern checks.

## What Failed

`python util.py --test` failed three Playwright API checks:

1. blocking the last enabled `manual-review-escalation` channel
2. blocking decline SMS for `loanState: "CA"`
3. blocking decline SMS for `loanState: "California"`

Those failures happened because the generated route validated writes only when `loanId`
was provided. The test harness, product spec, and prompt all expect the route to honor
direct `loanState` input.

## Root Cause

The old patch-shape checks were too permissive. They confirmed that some form of
validation was added, but they did not prove that the route preserved the intended
request contract.

This is why the lesson now treats `python util.py --test` as the decisive gate and why
the prompt plus expected-pattern checks were tightened to insist on direct `loanState`
flow.

## Current Repository State

After the failing raw demo run, the checked-in `src/` workspace was restored to the
intended implementation slice:

- direct `loanState` input in `PUT /api/notifications/preferences`
- explicit-input rule evaluation via `evaluateNotificationPreferenceWrite(...)`
- no new loan lookup contract added to the lesson slice

That restored workspace is the version that should be used for local exploration and
validation.
