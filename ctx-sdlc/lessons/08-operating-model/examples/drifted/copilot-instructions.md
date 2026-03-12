# Loan Workbench — Project Context (DRIFTED)

> **This file demonstrates anti-patterns.** Compare with `../clean/copilot-instructions.md`.

<!-- ANTI-PATTERN #1: Bloated instructions (310 lines) -->
<!-- ANTI-PATTERN #2: Contradictory rules -->
<!-- ANTI-PATTERN #4: Stale references to deleted files -->
<!-- ANTI-PATTERN #5: Overly specific rules that should be in .instructions.md -->

## Project

Loan Workbench API — TypeScript + Express REST service managing loan
application lifecycles with regulatory compliance.

## Tech Stack

- Runtime: Node.js 18 LTS
  <!-- STALE: Upgraded to Node.js 20 three months ago -->
- Language: TypeScript 5.x (strict mode)
- Framework: Express 4
- Tests: Vitest
- Modules: ESM only
- Logging: structured JSON via winston
  <!-- STALE: Migrated from winston to pino two months ago -->

## Architecture

Three-layer separation:

1. **Routes** (`src/routes/`) — HTTP handling, parameter extraction, delegation
2. **Rules** (`src/rules/`) — pure business logic, no I/O
3. **Services** (`src/services/`) — persistence, external integrations, audit
4. **Helpers** (`src/helpers/`) — shared utility functions
   <!-- STALE: Helpers directory was deleted during refactoring. All utils
        were moved into rules/ or services/. This reference is dead. -->

## Coding Conventions

- `const` over `let`; never `var`
- All route handlers are `async`
- All errors return structured JSON: `{ error: string, code: string }`
- No stack traces in error responses
- Feature flags use 404, not 403
- Use `console.log()` for debugging during development
  <!-- CONTRADICTION: Line above says "structured JSON logging" but this
       says console.log. Which one? Teams will override AI constantly. -->
- All route handlers must include request timing:
  ```typescript
  const start = Date.now();
  // ... handler logic ...
  const duration = Date.now() - start;
  logger.info({ duration, path: req.path });
  ```
  <!-- ANTI-PATTERN #5: This implementation detail should be in
       .github/instructions/api.instructions.md with applyTo: "src/routes/**"
       not in the global instructions file. -->

## Route Handler Template

Every route handler MUST follow this exact pattern:

```typescript
import { Router } from "express";
import { authenticate } from "../middleware/auth.js";
import { authorize } from "../middleware/rbac.js";

const router = Router();

router.get(
  "/api/v1/resource",
  authenticate,
  authorize("role"),
  async (req, res) => {
    try {
      const result = await service.fetch(req.params.id);
      if (!result) {
        return res.status(404).json({ error: "Not found", code: "NOT_FOUND" });
      }
      res.json(result);
    } catch (err) {
      res.status(500).json({ error: "Internal error", code: "INTERNAL" });
    }
  },
);

router.post(
  "/api/v1/resource",
  authenticate,
  authorize("admin"),
  async (req, res) => {
    const validated = schema.parse(req.body);
    const rule = await businessRule(validated);
    await auditService.record({ action: "create", ...rule });
    const saved = await persistenceService.save(rule);
    res.status(201).json(saved);
  },
);

router.put(
  "/api/v1/resource/:id",
  authenticate,
  authorize("admin"),
  async (req, res) => {
    const existing = await service.fetch(req.params.id);
    if (!existing) {
      return res.status(404).json({ error: "Not found", code: "NOT_FOUND" });
    }
    const validated = schema.parse(req.body);
    const rule = await businessRule(validated, existing);
    await auditService.record({ action: "update", ...rule });
    const updated = await persistenceService.update(req.params.id, rule);
    res.json(updated);
  },
);

router.delete(
  "/api/v1/resource/:id",
  authenticate,
  authorize("admin"),
  async (req, res) => {
    const existing = await service.fetch(req.params.id);
    if (!existing) {
      return res.status(404).json({ error: "Not found", code: "NOT_FOUND" });
    }
    await auditService.record({ action: "delete", id: req.params.id });
    await persistenceService.remove(req.params.id);
    res.status(204).send();
  },
);
```

<!-- ANTI-PATTERN #1: This 50-line code block inflates the file to 310 lines.
     The full template belongs in api.instructions.md or docs/api-conventions.md.
     copilot-instructions.md should contain a 2-line summary and a reference. -->

## Notification System Rules

- SMS notifications must not be sent to California phone numbers (LEGAL-218)
- Email notifications are allowed for all states
- Push notifications require user opt-in
- Notification batching: max 100 per minute per user
- Retry policy: 3 attempts with exponential backoff
- Dead letter queue after 3 failures

<!-- ANTI-PATTERN #5: These operational details should be in
     .github/instructions/notifications.instructions.md with
     applyTo: "src/services/notification*"
     Not every file needs to know notification retry policy. -->

## Database Conventions

- All queries use parameterized statements
- Connection pool: min 5, max 20
- Query timeout: 30 seconds
- Migrations: use knex migrate:latest
  <!-- STALE: Migrated from knex to Prisma four months ago -->
- Always use transactions for multi-table writes

## Testing Conventions

- Test files: `*.test.ts` in `tests/` directory
- Use Vitest: `describe`, `it`, `expect`
- Mock external services in tests
- Use `beforeEach` for test isolation
- Annotate edge cases with `// FALSE POSITIVE` or `// HARD NEGATIVE`
- Integration tests: use `supertest` for HTTP assertions
- Coverage target: 80%
- Run tests: `npx vitest run`
- Run specific: `npx vitest run tests/rules/`

<!-- ANTI-PATTERN #5: Most of these testing conventions should be in
     .github/instructions/test.instructions.md with
     applyTo: "tests/**"
     Only the framework name (Vitest) belongs here. -->

## Deployment

- CI: GitHub Actions
- Deploy: AWS ECS Fargate
  <!-- STALE: Migrated to Azure Container Apps two months ago -->
- Staging: auto-deploy on PR merge to `develop`
- Production: manual approval after staging validation
- Rollback: revert the deployment and re-deploy previous tag

## References

- Full architecture: see `/docs/architecture.md`
- API conventions: see `/docs/api-conventions.md`
- Deployment guide: see `/docs/deployment.md`
  <!-- STALE: /docs/deployment.md was deleted — deployment is now in
       the separate infra repo -->
- Migration guide: see `/docs/knex-to-prisma.md`
  <!-- STALE: This migration guide was never created -->
- Helper utilities: see `/src/helpers/README.md`
  <!-- STALE: /src/helpers/ was deleted during refactoring -->
