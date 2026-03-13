---
name: tdd-workflow
description: Structured red-green-refactor workflow for TaskFlow implementation tasks
---

# TDD Workflow Skill

> Guides test-driven development for TaskFlow features.

## When to Use

Use this skill when implementing any new feature or fixing a bug.
The TDD cycle applies to all three packages: web, api, and shared.

## The TDD Cycle for TaskFlow

### Step 1 — Write the Failing Test

**API tests** (`packages/api/tests/`):

```typescript
import { describe, it, expect } from "vitest";
import request from "supertest";
import { app } from "../src/app.js";

describe("POST /api/v1/tasks", () => {
  it("should create a task with valid data", async () => {
    const res = await request(app)
      .post("/api/v1/tasks")
      .set("Authorization", `Bearer ${testToken}`)
      .send({ title: "New task", projectId: testProjectId });

    expect(res.status).toBe(201);
    expect(res.body.data).toHaveProperty("id");
    expect(res.body.data.title).toBe("New task");
  });

  it("should reject invalid data", async () => {
    const res = await request(app)
      .post("/api/v1/tasks")
      .set("Authorization", `Bearer ${testToken}`)
      .send({});

    expect(res.status).toBe(400);
    expect(res.body.code).toBe("VALIDATION_ERROR");
  });
});
```

**Frontend tests** (`packages/web/tests/`):

```typescript
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { TaskCard } from '../src/components/TaskCard.js';

describe('TaskCard', () => {
  it('should display task title and status', () => {
    render(<TaskCard task={mockTask} />);
    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('TODO')).toBeInTheDocument();
  });
});
```

### Step 2 — Run and Confirm Failure

```bash
npx vitest run --reporter=verbose
```

The test should FAIL for the right reason (missing feature, not syntax error).

### Step 3 — Implement the Minimum Code

Write just enough code to make the failing test pass.

### Step 4 — Verify Green

```bash
npx vitest run --reporter=verbose
```

All tests should pass.

### Step 5 — Refactor

Clean up the implementation while keeping tests green.
