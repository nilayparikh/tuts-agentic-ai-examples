# Exercise 2 — Planning Workflow

> **Lessons Applied:** L04 (Planning Workflows) + L03 (Instruction Architecture)
> **Estimated Time:** 30–45 minutes
> **Difficulty:** Intermediate

## Objective

Create a reusable prompt file that forces the AI agent to produce a structured
implementation plan — discovering relevant files from the codebase — without
writing any code.

## Background

In Lesson 4 you learned that the best AI-assisted workflows read before they
write. A planning phase prevents the agent from making changes based on
assumptions instead of evidence.

The problem: when you give an agent a feature description, it jumps straight
to code. It skips the discovery step. It doesn't check which existing patterns
to follow. The result is code that compiles but doesn't fit the codebase.

A well-crafted prompt file fixes this by constraining the output format.

## Tasks

### Task 1: Create the Prompt File

Create `.github/prompts/feature-plan.prompt.md` with this structure:

```markdown
---
mode: agent
description: "Produce a structured implementation plan for a new feature"
---

# Feature Planning Prompt

## Input

{{feature_description}}

## Instructions

1. **Discovery phase** — read the project's architecture doc, relevant
   instruction files, and source files before planning. List every file
   you read.

2. **Identify constraints** — from the instruction files and architecture
   doc, list every rule, convention, or pattern that applies to this feature.

3. **Map affected surfaces** — identify which backend routes, rules,
   services, models, and frontend pages this feature touches.

4. **Produce the plan** — output a structured implementation plan with:
   - Files to create (with purpose)
   - Files to modify (with specific changes)
   - Testing requirements (which test files, which cases)
   - Risks and open questions

## Constraints

- Do NOT write any code. Output only the plan.
- Do NOT assume file paths — discover them from the codebase.
- Reference specific files by their actual path.
- Follow the three-layer separation (Route → Rule → Service).
```

Adapt the template above to match your style. The key constraints are:
no code output, discovery-first, and structured format.

### Task 2: Test the Prompt — Rate-Limit Feature

Use your prompt file to plan this feature:

> "Add a rate limit for notification preference write operations. Users should
> be limited to 10 preference changes per minute. The rate limit should use
> the existing rate-limiter middleware pattern. Violations should return 429
> with a structured error response."

Evaluate the plan against these checkpoints:

- [ ] Did the agent read `backend/src/middleware/rate-limiter.ts`?
- [ ] Did the agent read `backend/src/routes/notifications.ts`?
- [ ] Did the agent identify the existing middleware chain pattern?
- [ ] Does the plan reference the three-layer separation?
- [ ] Did the agent discover the error response format from `api.instructions.md`?
- [ ] Is the plan code-free — no TypeScript, no implementation snippets?

### Task 3: Iterate on the Prompt

If the agent produced code, add stronger constraints. Common fixes:

- Add: "If you catch yourself writing TypeScript, stop and describe the change in words instead."
- Add: "Your output format is markdown only — no code fences except for file paths."
- Add: "End with a section titled 'Ready for Implementation' that lists prerequisites."

Re-run until the agent consistently produces plans, not code.

### Task 4: Test the Prompt — Second Feature

Use your prompt file to plan a different feature:

> "Add a notification delivery receipt tracking system. When a notification is
> sent via email or SMS, record the delivery status (sent, delivered, bounced,
> failed) in a new receipts table. The notification service should update
> receipt status on provider callbacks."

This tests whether your prompt generalizes beyond the first feature. Check:

- [ ] The agent discovered new surfaces (queue contracts, notification service)
- [ ] The plan identifies a new model/table requirement
- [ ] The plan follows the same three-layer separation
- [ ] Still no code output

## Success Criteria

1. `.github/prompts/feature-plan.prompt.md` exists and is well-structured
2. The prompt produces a discovery-first plan for at least two different features
3. All file references in the plan are real files discovered from the codebase
4. No code appears in any plan output
5. The plan identifies applicable patterns from instruction files

## Hints

- The rate-limiter middleware is at `backend/src/middleware/rate-limiter.ts` —
  but don't hardcode this in your prompt. Let the agent find it.
- The notification route already has a middleware chain (authenticate → authorize →
  validateBody). Your plan should describe inserting the rate limiter into this chain.
- Check how error responses are structured in `api.instructions.md` — the plan
  should reference this convention.

## What You're Practicing

- **L04 pattern:** Read-only planning that prevents premature implementation
- **L03 pattern:** Prompt files as reusable workflow templates
- **Core skill:** Constraining AI output format to get planning artifacts, not code
