# Lesson 03 — VS Code Copilot Chat Guide

## Steps

### 1. Set up the workspace

```bash
python util.py --setup
cd src && npm install
```

### 2. Routes layer — backend.instructions.md activates

Open `src/backend/src/routes/notifications.ts` and ask:

```
Add a DELETE /notifications/preferences/:event endpoint that resets to defaults for the current user.
```

**Observe:** Code uses `Router.delete()` with `requireRole()` middleware, calls `writeAuditEntry()` before deleting, returns 204/404. The route orchestrates — no inline business logic.

### 3. Rules layer — business-rules.instructions.md activates

Open `src/backend/src/rules/state-rules.ts` and ask:

```
Add a rule that validates notification preferences. Users cannot subscribe to channels their role does not permit.
```

**Observe:** Code returns `{ valid, violations }` — pure functions with no side effects. Business rules validate, routes orchestrate.

### 4. Security layer — security.instructions.md activates

Open `src/backend/src/middleware/auth.ts` and ask:

```
Add rate-limiting middleware for the notification preferences endpoint.
```

**Observe:** Security-specific patterns activate (fail-closed, structured logging, no business logic in middleware).

### 5. Test layer — testing.instructions.md activates

Open `src/backend/tests/` and ask:

```
Write tests for the notification preference reset endpoint.
```

**Observe:** Test conventions activate (no mocking of audit service, use factory helpers, arrange-act-assert).

### 6. Cleanup

```bash
python util.py --clean
```
