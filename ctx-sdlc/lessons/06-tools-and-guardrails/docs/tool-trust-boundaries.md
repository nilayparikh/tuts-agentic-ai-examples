# Tool Trust Boundaries

This document defines the trust model for external tool access in the Loan
Workbench project. Every MCP server and external integration must be classified
before it is added to `.github/mcp.json`.

## Trust Classification

| Level | Label                  | Description                                       | Example                                                       |
| ----- | ---------------------- | ------------------------------------------------- | ------------------------------------------------------------- |
| 1     | **Read-only internal** | Can read project files and data. No mutations.    | Filesystem MCP (scoped to `backend/src/`, `tests/`, `docs/`)  |
| 2     | **Read-only external** | Can query external systems. No mutations.         | SQLite MCP (read-only connection to `data/loan-workbench.db`) |
| 3     | **Write internal**     | Can modify project files within scope.            | Filesystem MCP with write access (rarely justified)           |
| 4     | **Write external**     | Can mutate external systems.                      | API MCP with POST/PUT/DELETE access                           |
| 5     | **Privileged**         | Can execute arbitrary commands or access secrets. | Shell MCP, deployment tools                                   |

## Current MCP Server Inventory

| Server       | Trust Level            | Scope                                                      | Justification                                                                                                               |
| ------------ | ---------------------- | ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `sqlite`     | 2 — Read-only external | `data/loan-workbench.db`                                   | Query application state and audit logs for debugging and analysis. Write operations go through API routes with audit trail. |
| `filesystem` | 1 — Read-only internal | `backend/src/`, `backend/tests/`, `frontend/src/`, `docs/` | Allows the assistant to read source code and documentation. Excludes `.env`, `node_modules`, and config secrets.            |

## Agent × Tool Access Matrix

| Agent       | `sqlite` | `filesystem` | Terminal           | File Writes                        |
| ----------- | -------- | ------------ | ------------------ | ---------------------------------- |
| Implementer | ❌       | ✅ Read      | ✅ Build/lint only | ✅ `backend/src/`, `frontend/src/` |
| Tester      | ✅ Read  | ✅ Read      | ✅ Build/test      | ✅ `backend/tests/` only           |
| Reviewer    | ✅ Read  | ✅ Read      | ❌                 | ❌                                 |

## Adding a New MCP Server

Before adding a server to `.github/mcp.json`:

1. **Classify**: Assign a trust level from the table above.
2. **Scope**: Define the minimum access scope needed. Prefer read-only.
3. **Document**: Add an entry to the inventory table in this file.
4. **Agent mapping**: Update the access matrix to show which agents can use it.
5. **Review**: Have the security policy owner approve the addition.

### Questions to Answer

- What data does this server access?
- Can it mutate anything? If so, what?
- Which agents need it? Can access be restricted to a subset?
- What happens if this server is compromised or returns bad data?
- Is there a read-only alternative that satisfies the use case?

## Principles

1. **Least privilege**: Start with read-only. Justify every write capability.
2. **Scope narrowly**: MCP filesystem access should list specific directories,
   not the entire workspace.
3. **No secret exposure**: MCP servers must not have access to `.env` files,
   API keys, or credentials beyond their connection string.
4. **Defense in depth**: MCP scoping + hook enforcement + instruction guidance.
   No single layer is sufficient alone.
5. **Audit trail**: Write-capable MCP servers should have their operations
   logged, just like API mutations.
