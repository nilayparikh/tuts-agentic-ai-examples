# Exercise 4 — Guardrails & Validation

> **Lessons Applied:** L06 (Tools & Guardrails) + L08 (Operating Model)
> **Estimated Time:** 30–45 minutes
> **Difficulty:** Intermediate

## Objective

Create deterministic guardrail hooks that enforce compliance rules the
instruction files can only suggest. Then build a context inventory as
the baseline for your operating model.

## Background

In Lesson 6 you learned the difference between instructions and hooks:

- **Instructions** suggest behavior — the agent can ignore them.
- **Hooks** enforce behavior — the commit fails if rules are violated.

In Lesson 8 you learned that a context system needs measurement. You can't
maintain what you can't count.

This exercise makes both concrete.

## Tasks

### Task 1: Create the Audit-Check Hook

Route handlers that write data must call the audit service. Without a hook,
an agent can skip audit calls and the code still compiles. The hook catches
this before commit.

Create `.github/hooks/audit-check.json`:

```json
{
  "name": "audit-check",
  "description": "Ensure all route handlers that modify data call the audit service",
  "event": "preCommit",
  "steps": [
    {
      "type": "script",
      "command": "node scripts/check-audit-compliance.js",
      "description": "Scan modified route files for audit service calls"
    }
  ]
}
```

Then create the check script at `scripts/check-audit-compliance.js` (or
`.ts`). The script should:

1. Find all files matching `backend/src/routes/*.ts` that were modified
   in the current commit (use `git diff --cached --name-only`)
2. For each modified route file, check that:
   - Every `router.post`, `router.put`, `router.patch`, `router.delete`
     handler body contains a call to `auditAction` or `auditService`
   - Handlers that only read data (`router.get`) are exempt
3. Exit with code 1 and a descriptive error if any write handler is missing
   an audit call

**Test it:** Temporarily remove the `auditAction` call from
`notifications.ts`, stage the file, and run the script. It should fail.
Restore the file afterward.

### Task 2: Create the Test-Coverage Hook

Every rule file in `backend/src/rules/` must have a matching test in
`backend/tests/unit/`. This hook enforces the convention.

Create `.github/hooks/test-coverage.json`:

```json
{
  "name": "test-coverage",
  "description": "Ensure every rule module has a matching unit test file",
  "event": "preCommit",
  "steps": [
    {
      "type": "script",
      "command": "node scripts/check-rule-tests.js",
      "description": "Verify test file exists for each rule module"
    }
  ]
}
```

Then create the check script at `scripts/check-rule-tests.js`. The script
should:

1. List all `.ts` files in `backend/src/rules/` (excluding index files)
2. For each rule file `foo.ts`, check that `backend/tests/unit/foo.test.ts`
   exists
3. Exit with code 1 if any rule file is missing a corresponding test file

**Test it:** Create a dummy file `backend/src/rules/dummy-rule.ts`. Run the
script. It should fail because `backend/tests/unit/dummy-rule.test.ts`
doesn't exist. Delete the dummy file afterward.

### Task 3: Build Your Context Inventory

Create `docs/CONTEXT_INVENTORY.md` — a snapshot of every context artifact
in the project. This is your operating baseline from Lesson 8.

Include these sections:

**Instruction Files:**

| File                                            | Scope             | Last Updated | Rule Count |
| ----------------------------------------------- | ----------------- | ------------ | ---------- |
| `.github/copilot-instructions.md`               | Global            | [date]       | [count]    |
| `.github/instructions/api.instructions.md`      | `backend/src/**`  | [date]       | [count]    |
| `.github/instructions/frontend.instructions.md` | `frontend/src/**` | [date]       | [count]    |

**Documentation Files:**

| File                   | Purpose             | Last Updated | Word Count |
| ---------------------- | ------------------- | ------------ | ---------- |
| `docs/architecture.md` | System architecture | [date]       | [count]    |
| `docs/VOCAB.md`        | Domain vocabulary   | [date]       | [count]    |

**Agent Files:**

| File                              | Role     | Boundary             | Created In |
| --------------------------------- | -------- | -------------------- | ---------- |
| `.github/agents/planner.agent.md` | Planning | No code output       | Exercise 3 |
| `.github/agents/tester.agent.md`  | Testing  | No production access | Exercise 3 |

**Prompt Files:**

| File                                     | Purpose          | Created In |
| ---------------------------------------- | ---------------- | ---------- |
| `.github/prompts/feature-plan.prompt.md` | Feature planning | Exercise 2 |

**Hook Configurations:**

| File                               | Purpose          | Trigger    | Created In |
| ---------------------------------- | ---------------- | ---------- | ---------- |
| `.github/hooks/audit-check.json`   | Audit compliance | Pre-commit | Exercise 4 |
| `.github/hooks/test-coverage.json` | Test parity      | Pre-commit | Exercise 4 |

**Summary Stats:**

- Total instruction files: \_
- Total documentation files: \_
- Total agent files: \_
- Total prompt files: \_
- Total hook configurations: \_
- Total context artifacts: \_

### Task 4: Identify Maintenance Gaps

Review your inventory and answer:

1. Which instruction file has the most rules? Is it too large to maintain?
2. Are there any backend subsystems not covered by a path-scoped instruction?
3. Do all docs reference current source file paths (or are any stale)?
4. Which context artifact would break first if the codebase changes?

Write your answers as a "Maintenance Notes" section at the bottom of the
inventory.

## Success Criteria

1. `.github/hooks/audit-check.json` and `.github/hooks/test-coverage.json` exist
2. Both check scripts work — they fail on violations and pass on compliant code
3. `docs/CONTEXT_INVENTORY.md` exists with all sections filled out
4. The inventory includes maintenance notes identifying at least two risks
5. The hooks are deterministic — same input always produces same result

## Hints

- For the audit check script, `git diff --cached --name-only --diff-filter=AM`
  gives you added and modified files in the staging area
- Regex to find write handlers: `/router\.(post|put|patch|delete)\(/`
- Regex to find audit calls: `/audit(Action|Service)/`
- For the test coverage script, use `fs.readdirSync` to list rule files and
  `fs.existsSync` to check for matching tests
- The context inventory is a living document — plan to update it monthly

## What You're Practicing

- **L06 pattern:** Hooks for deterministic enforcement (vs instruction suggestions)
- **L08 pattern:** Context inventory as an operating baseline
- **Core skill:** Making the wrong thing impossible, then measuring what you built
