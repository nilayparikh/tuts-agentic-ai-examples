---
applyTo: "app/backend/src/**"
---

# API Instructions — Express 4 + SQLite

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

Apply in this order:

1. `authenticate` — validates session token
2. `authorize(role)` — checks role-based access
3. Handler body — validates, delegates, responds

## Error Handling

| Status | Code                 | When                          |
| ------ | -------------------- | ----------------------------- |
| 400    | `VALIDATION_ERROR`   | Request body fails validation |
| 401    | `AUTH_REQUIRED`      | Missing or invalid session    |
| 403    | `FORBIDDEN`          | Insufficient role             |
| 404    | `NOT_FOUND`          | Resource or disabled feature  |
| 422    | `INVALID_TRANSITION` | State machine violation       |
| 500    | `INTERNAL_ERROR`     | Unexpected server error       |

## Database

- All queries through better-sqlite3 wrapper
- Domain types from `app/backend/src/models/types.ts`
- Use transactions for multi-table writes

## Real-time

- WebSocket events emitted after successful writes
- Event format: `{ type: string, payload: object }`
- Never emit before the database write succeeds
