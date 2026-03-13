---
agent: Plan
description: "Plan a new feature for TaskFlow following the architecture and conventions."
---

# Add Feature — Planning Prompt

You are a senior developer planning a new feature for TaskFlow.

## Context

#file:../../../../docs/architecture.md
#file:../../../../.github/copilot-instructions.md

## Feature Request

**Feature**: {{ feature_description }}

## Output Required

Produce a plan with these sections:

### 1. Scope

- What packages are affected? (`web`, `api`, `shared`)
- What existing files need modification?
- What new files need creation?

### 2. Data Model Changes

- New Prisma models or fields needed
- Migration steps

### 3. API Changes

- New routes (method, path, request/response)
- New middleware needed
- WebSocket events

### 4. Frontend Changes

- New components
- New/modified Zustand stores
- New/modified hooks
- New routes

### 5. Testing Plan

- Key test cases for each layer
- Edge cases to cover
