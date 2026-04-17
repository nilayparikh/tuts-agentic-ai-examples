# Loan Workbench Context Map

This project demonstrates context engineering for GitHub Copilot using a
TypeScript + Express commercial loan application.

## Context Files

| Path                                            | Purpose                       | Lesson  |
| ----------------------------------------------- | ----------------------------- | ------- |
| `.github/copilot-instructions.md`               | Project-wide conventions      | L02–L03 |
| `.github/instructions/api.instructions.md`      | Backend API patterns          | L03     |
| `.github/instructions/frontend.instructions.md` | Frontend SPA patterns         | L03     |
| `docs/architecture.md`                          | System architecture reference | L02     |
| `docs/VOCAB.md`                                 | Domain vocabulary             | L02     |
| `docs/capstone-example.md`                      | Capstone exercise constraints | L09     |

## Agent Files (Exercise 3)

These files are created by the learner during Exercise 3:

| Path                              | Role                 | Boundary                  |
| --------------------------------- | -------------------- | ------------------------- |
| `.github/agents/planner.agent.md` | Read-only planning   | No code output            |
| `.github/agents/tester.agent.md`  | Test-first authoring | No production file access |

## Hook Configs (Exercise 4)

These files are created by the learner during Exercise 4:

| Path                               | Purpose                      | Trigger    |
| ---------------------------------- | ---------------------------- | ---------- |
| `.github/hooks/audit-check.json`   | Block unaudited route writes | Pre-commit |
| `.github/hooks/test-coverage.json` | Require tests for rule files | Pre-commit |
