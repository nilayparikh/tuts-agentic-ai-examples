---
applyTo: "packages/api/**"
---

# API Instructions — Express 5 + Prisma

## Controller Pattern

Every route handler MUST follow this template:

```typescript
// routes/tasks.ts
router.get("/api/v1/tasks", authenticate, async (req, res) => {
  const tasks = await taskService.listForUser(req.user.id);
  res.json({ data: tasks });
});
```

## Middleware Chain

Apply in this order:

1. `authenticate` — validates JWT, attaches `req.user`
2. `authorize(role)` — checks role-based access (admin, member, viewer)
3. `validate(schema)` — Zod validation of request body
4. Controller body — delegates to service, returns response

## Error Handling

```typescript
// Standard error response format
res.status(code).json({ error: string, code: string });
```

| Status | Code               | When                           |
| ------ | ------------------ | ------------------------------ |
| 400    | `VALIDATION_ERROR` | Request body fails Zod parsing |
| 401    | `AUTH_REQUIRED`    | Missing or invalid JWT         |
| 403    | `FORBIDDEN`        | Insufficient role              |
| 404    | `NOT_FOUND`        | Resource doesn't exist         |
| 409    | `CONFLICT`         | Duplicate or state conflict    |
| 500    | `INTERNAL_ERROR`   | Unexpected server error        |

## Database

- All queries through Prisma Client
- No raw SQL unless solving N+1 with `$queryRaw`
- Use transactions for multi-model writes
- Always use `select` or `include` — no `findMany()` without field selection

## Real-time

- WebSocket events emitted after successful writes
- Event format: `{ type: string, payload: object }`
- Never emit before the database write succeeds
