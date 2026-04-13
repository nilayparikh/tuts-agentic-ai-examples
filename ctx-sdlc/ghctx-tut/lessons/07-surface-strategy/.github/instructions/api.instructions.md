---
applyTo: "app/backend/src/routes/**"
---

# API Route Instructions

These rules apply only when editing files under `app/backend/src/routes/`.

## Route Handler Pattern

Every route handler MUST follow this template:

```typescript
router.post("/path", authenticate, authorize("role"), async (req, res) => {
  const validated = schema.parse(req.body);
  const result = await ruleFunction(validated);
  await auditService.record({ action: "action_name", ...result });
  await persistenceService.save(result);
  res.status(201).json(result);
});
```

## Middleware Chain

Always apply in this order:

1. `authenticate` — validates session token
2. `authorize(role)` — checks role-based access
3. Handler body — validates, delegates, responds

## Error Handling

- Validation errors: 400 with `{ error: string, code: "VALIDATION_ERROR" }`
- Not found: 404 with `{ error: string, code: "NOT_FOUND" }`
- Feature flag disabled: 404 (NOT 403) with `{ error: string, code: "NOT_FOUND" }`
- Unauthorized: 401 with `{ error: "Unauthorized", code: "AUTH_REQUIRED" }`
- Forbidden: 403 with `{ error: string, code: "FORBIDDEN" }`

> **Note**: This file uses `applyTo` scoping — it is only active in VS Code
> and Copilot Coding Agent. It is NOT loaded in GitHub CLI or Code Review.
> The portable equivalent is the pattern documented in
> `.github/copilot-instructions.md` and `/docs/api-conventions.md`.
