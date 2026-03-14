# 🤖 Copilot CLI Session

> [!NOTE]
> - **Session ID:** `682d6a41-1c8b-4392-b048-8beaa543212f`  
> - **Started:** 13/03/2026, 23:27:55  
> - **Duration:** 42s  
> - **Exported:** 13/03/2026, 23:28:37  

---

<sub>⏱️ 5s</sub>

### 👤 User

Read .github/copilot-instructions.md, .github/mcp.json, docs/tool-trust-boundaries.md, docs/security-policy.md, .github/hooks/file-protection.json, .github/hooks/pre-commit-validate.json, .github/hooks/post-save-format.json, .github/scripts/check_protected_files.py, and .github/scripts/validate_commit.py. Produce a read-only guardrail audit for this lesson. Return: summary, confirmed controls, inconsistencies with file references, false positives, hard negatives, prioritized fixes, and residual risks. Explicitly call out whether protected-file policy matches hook enforcement, whether filesystem scope matches the documented trust boundaries, whether fail-closed audit and 404-not-403 rules are represented consistently, and what the CLI cannot demonstrate because VS Code hooks do not run here. Do not modify files, do not run shell commands, and do not use SQL or any other write-capable tools. Inspect and read only.

---

<sub>⏱️ 15s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\copilot-instructions.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\copilot-instructions.md

<details>
<summary>50 lines</summary>

```
1. # Loan Workbench — Copilot Instructions (Guardrails Focus)
2. 
3. ## Project
4. 
5. TypeScript Express API with embedded message broker and SQLite persistence
6. for loan application workflow management. This workspace uses MCP servers and
7. hooks for capability expansion and enforcement.
8. 
9. ## Tool Policy
10. 
11. ### MCP Servers
12. 
13. This project configures MCP servers in `.github/mcp.json`. Follow these rules:
14. 
15. 1. **Database access is read-only.** Never attempt to write to the database via
16.    MCP. All mutations go through the Express API routes with audit trail.
17. 2. **Filesystem access is scoped.** The MCP filesystem server can only read
18.    `src/backend/src/`, `src/backend/tests/`, and `docs/`. It cannot access
19.    `.env`, `node_modules`, or config files with secrets.
20. 3. **Do not add MCP servers** without updating `docs/tool-trust-boundaries.md`
21.    with the new server's trust classification.
22. 
23. ### Hooks
24. 
25. Hooks in `.github/hooks/` enforce deterministic rules. Do not try to bypass them:
26. 
27. 1. **Pre-commit validation** (`pre-commit-validate.json`): Runs lint and tests.
28.    If they fail, the commit is blocked. Fix the issues — do not disable the hook.
29. 2. **Post-save formatting** (`post-save-format.json`): Prettier runs after every
30.    `.ts` file save. Do not add manual formatting code.
31. 3. **File protection** (`file-protection.json`): Certain files cannot be edited
32.    by AI assistance. See `docs/security-policy.md` for the approval process.
33. 
34. ## Security Rules
35. 
36. - Audit events must succeed before mutations persist (fail-closed).
37. - Error responses must not leak internal state or stack traces.
38. - Delegated sessions cannot perform write operations.
39. - Feature flags use 404 (not 403) for non-pilot users.
40. - Protected files require manual approval for changes.
41. 
42. ## Code Conventions
43. 
44. - TypeScript strict mode, ESM imports.
45. - Business rules in `src/backend/src/rules/` — pure functions, no side effects.
46. - Services in `src/backend/src/services/` — I/O and external integrations.
47. - Routes in `src/backend/src/routes/` — orchestration only, delegate to rules and services.
48. - Queue broker in `src/backend/src/queue/` — async event handling (notifications, audit).
49. - All tests in `src/backend/tests/` using Vitest.
50.
```

</details>


---

<sub>⏱️ 15s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\mcp.json.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\mcp.json

<details>
<summary>33 lines</summary>

```
1. {
2.   "servers": {
3.     "sqlite": {
4.       "command": "npx",
5.       "args": [
6.         "-y",
7.         "@anthropic-ai/mcp-server-sqlite",
8.         "${workspaceFolder}/src/data/loan-workbench.db"
9.       ],
10.       "description": "Read-only access to the Loan Workbench SQLite database for querying application state, audit logs, and notification preferences.",
11.       "permissions": {
12.         "read": true,
13.         "write": false
14.       }
15.     },
16.     "filesystem": {
17.       "command": "npx",
18.       "args": [
19.         "-y",
20.         "@modelcontextprotocol/server-filesystem",
21.         "${workspaceFolder}/src/backend/src",
22.         "${workspaceFolder}/src/backend/tests",
23.         "${workspaceFolder}/src/frontend/src",
24.         "${workspaceFolder}/docs"
25.       ],
26.       "description": "Scoped filesystem access for reading source code, tests, and documentation. Excludes .env, node_modules, and config secrets.",
27.       "permissions": {
28.         "read": true,
29.         "write": false
30.       }
31.     }
32.   }
33. }
```

</details>


---

<sub>⏱️ 15s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\docs\tool-trust-boundaries.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\docs\tool-trust-boundaries.md

<details>
<summary>61 lines</summary>

```
1. # Tool Trust Boundaries
2. 
3. This document defines the trust model for external tool access in the Loan
4. Workbench project. Every MCP server and external integration must be classified
5. before it is added to `.github/mcp.json`.
6. 
7. ## Trust Classification
8. 
9. | Level | Label                  | Description                                       | Example                                                                      |
10. | ----- | ---------------------- | ------------------------------------------------- | ---------------------------------------------------------------------------- |
11. | 1     | **Read-only internal** | Can read project files and data. No mutations.    | Filesystem MCP (scoped to `src/backend/src/`, `src/backend/tests/`, `docs/`) |
12. | 2     | **Read-only external** | Can query external systems. No mutations.         | SQLite MCP (read-only connection to `data/loan-workbench.db`)                |
13. | 3     | **Write internal**     | Can modify project files within scope.            | Filesystem MCP with write access (rarely justified)                          |
14. | 4     | **Write external**     | Can mutate external systems.                      | API MCP with POST/PUT/DELETE access                                          |
15. | 5     | **Privileged**         | Can execute arbitrary commands or access secrets. | Shell MCP, deployment tools                                                  |
16. 
17. ## Current MCP Server Inventory
18. 
19. | Server       | Trust Level            | Scope                                                                  | Justification                                                                                                               |
20. | ------------ | ---------------------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
21. | `sqlite`     | 2 — Read-only external | `data/loan-workbench.db`                                               | Query application state and audit logs for debugging and analysis. Write operations go through API routes with audit trail. |
22. | `filesystem` | 1 — Read-only internal | `src/backend/src/`, `src/backend/tests/`, `src/frontend/src/`, `docs/` | Allows the assistant to read source code and documentation. Excludes `.env`, `node_modules`, and config secrets.            |
23. 
24. ## Agent × Tool Access Matrix
25. 
26. | Agent       | `sqlite` | `filesystem` | Terminal           | File Writes                                |
27. | ----------- | -------- | ------------ | ------------------ | ------------------------------------------ |
28. | Implementer | ❌       | ✅ Read      | ✅ Build/lint only | ✅ `src/backend/src/`, `src/frontend/src/` |
29. | Tester      | ✅ Read  | ✅ Read      | ✅ Build/test      | ✅ `backend/tests/` only                   |
30. | Reviewer    | ✅ Read  | ✅ Read      | ❌                 | ❌                                         |
31. 
32. ## Adding a New MCP Server
33. 
34. Before adding a server to `.github/mcp.json`:
35. 
36. 1. **Classify**: Assign a trust level from the table above.
37. 2. **Scope**: Define the minimum access scope needed. Prefer read-only.
38. 3. **Document**: Add an entry to the inventory table in this file.
39. 4. **Agent mapping**: Update the access matrix to show which agents can use it.
40. 5. **Review**: Have the security policy owner approve the addition.
41. 
42. ### Questions to Answer
43. 
44. - What data does this server access?
45. - Can it mutate anything? If so, what?
46. - Which agents need it? Can access be restricted to a subset?
47. - What happens if this server is compromised or returns bad data?
48. - Is there a read-only alternative that satisfies the use case?
49. 
50. ## Principles
51. 
52. 1. **Least privilege**: Start with read-only. Justify every write capability.
53. 2. **Scope narrowly**: MCP filesystem access should list specific directories,
54.    not the entire workspace.
55. 3. **No secret exposure**: MCP servers must not have access to `.env` files,
56.    API keys, or credentials beyond their connection string.
57. 4. **Defense in depth**: MCP scoping + hook enforcement + instruction guidance.
58.    No single layer is sufficient alone.
59. 5. **Audit trail**: Write-capable MCP servers should have their operations
60.    logged, just like API mutations.
61.
```

</details>


---

<sub>⏱️ 15s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\docs\security-policy.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\docs\security-policy.md

<details>
<summary>95 lines</summary>

```
1. # Security Policy — Loan Workbench
2. 
3. This document defines the security controls enforced by hooks and instructions.
4. It is the source of truth for what is allowed and what is blocked.
5. 
6. ## Protected Files
7. 
8. The following files are protected by the file-protection hook and cannot be
9. edited by AI assistance:
10. 
11. | File                                      | Reason                                                                  | Change Process                                         |
12. | ----------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------ |
13. | `.env` / `.env.*`                         | Contains database paths, API keys, feature flag overrides               | Manual edit by an authorized engineer. Reviewed in PR. |
14. | `src/backend/src/config/feature-flags.ts` | Controls pilot gating. Incorrect changes expose unreleased features.    | Product owner approval + manual edit.                  |
15. | `src/backend/src/db/schema.sql`           | Database DDL. Modifications can break migrations and the test baseline. | Coordinated change with migration update.              |
16. | `src/backend/src/db/seed.ts`              | Contains seeded test data. Modifications can break the test baseline.   | Coordinated change with test update.                   |
17. 
18. ### Why AI Cannot Edit These Files
19. 
20. These files are not dangerous because of what they contain syntactically — they
21. are dangerous because of the **decisions** they encode. Feature flags determine
22. who sees unreleased features. Environment variables contain secrets. Test data
23. establishes the baseline that all tests rely on.
24. 
25. An AI assistant might "helpfully" add a feature flag for a feature it's building,
26. or seed test data that makes its tests pass but breaks others, or modify the
27. database schema without a migration. The file-protection hook prevents this.
28. 
29. ## Audit Requirements
30. 
31. ### Fail-Closed Semantics
32. 
33. All data mutations must write an audit entry BEFORE persisting the change.
34. If the audit service is unavailable, the mutation MUST fail with HTTP 503.
35. 
36. This is enforced by:
37. 
38. 1. **Code design**: Audit events are emitted via the queue broker (or direct DB
39.    write) before persisting in every route handler.
40. 2. **Tests**: Edge-case tests verify that audit failure blocks persistence.
41. 3. **Hooks**: Pre-commit validation ensures tests pass before code is committed.
42. 
43. ### What Gets Audited
44. 
45. | Action                       | Audit Fields                               | Retention |
46. | ---------------------------- | ------------------------------------------ | --------- |
47. | Preference save              | userId, changes, timestamp, sessionType    | 90 days   |
48. | Application state transition | applicationId, fromState, toState, userId  | Permanent |
49. | Decision recording           | applicationId, decision, userId, timestamp | Permanent |
50. | Failed mutation              | userId, action, reason, timestamp          | 30 days   |
51. 
52. ## Session Security
53. 
54. ### Delegated Sessions
55. 
56. A delegated session is when user A acts on behalf of user B. The `x-delegated-for`
57. header indicates delegation.
58. 
59. **Rule**: Delegated sessions are read-only for sensitive operations. The
60. `blockDelegatedWrites` middleware enforces this on:
61. 
62. - `PUT /notifications/preferences`
63. - `POST /decisions`
64. - `PATCH /applications/:id/status`
65. 
66. ### Why This Matters for AI
67. 
68. An AI assistant might not distinguish between "I'm helping user A" and "user A
69. is acting as user B." Without the delegated session context, the AI would
70. happily mutate data on behalf of a delegated principal — which violates the
71. security model.
72. 
73. ## Error Response Safety
74. 
75. Error responses must not leak:
76. 
77. - Stack traces
78. - Internal file paths
79. - Database connection strings
80. - User IDs of other users
81. - Feature flag names or values
82. 
83. The central error handler in `src/backend/src/middleware/error-handler.ts` enforces this.
84. For 4xx errors, a brief message is returned. For 5xx errors, only a generic
85. "Internal server error" with a correlation ID is returned.
86. 
87. ## Incident Response
88. 
89. If a security control is bypassed:
90. 
91. 1. Check the audit log for the affected time period.
92. 2. Verify hook configurations have not been modified.
93. 3. Review MCP server access logs (if write-capable servers are configured).
94. 4. Document the incident and update this policy if needed.
95.
```

</details>


---

<sub>⏱️ 15s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\hooks\file-protection.json.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\hooks\file-protection.json

<details>
<summary>11 lines</summary>

```
1. {
2.   "hooks": {
3.     "PreToolUse": [
4.       {
5.         "type": "command",
6.         "command": "python .github/scripts/check_protected_files.py",
7.         "timeout": 10
8.       }
9.     ]
10.   }
11. }
```

</details>


---

<sub>⏱️ 15s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\hooks\pre-commit-validate.json.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\hooks\pre-commit-validate.json

<details>
<summary>11 lines</summary>

```
1. {
2.   "hooks": {
3.     "PreToolUse": [
4.       {
5.         "type": "command",
6.         "command": "python .github/scripts/validate_commit.py",
7.         "timeout": 60
8.       }
9.     ]
10.   }
11. }
```

</details>


---

<sub>⏱️ 15s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\hooks\post-save-format.json.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\hooks\post-save-format.json

<details>
<summary>11 lines</summary>

```
1. {
2.   "hooks": {
3.     "PostToolUse": [
4.       {
5.         "type": "command",
6.         "command": "npx prettier --write \"$TOOL_INPUT_FILE_PATH\"",
7.         "timeout": 15
8.       }
9.     ]
10.   }
11. }
```

</details>


---

<sub>⏱️ 15s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\check_protected_files.py.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\check_protected_files.py

<details>
<summary>64 lines</summary>

```
1. #!/usr/bin/env python3
2. """PreToolUse hook: block edits to protected files.
3. 
4. Reads JSON from stdin (VS Code hook input) and checks if the tool is
5. attempting to edit a protected file. Returns a deny decision if so.
6. 
7. Protected files:
8.   - .env, .env.*
9.     - src/backend/src/config/feature-flags.ts
10.     - src/backend/src/db/connection.ts
11. """
12. import json
13. import sys
14. from pathlib import PurePosixPath
15. 
16. PROTECTED_PATTERNS = [
17.     ".env",
18.     "src/backend/src/config/feature-flags.ts",
19.     "src/backend/src/db/connection.ts",
20. ]
21. 
22. 
23. def is_protected(filepath: str) -> bool:
24.     p = PurePosixPath(filepath)
25.     for pattern in PROTECTED_PATTERNS:
26.         if p.name.startswith(".env") or str(p) == pattern:
27.             return True
28.     return False
29. 
30. 
31. def main() -> None:
32.     data = json.load(sys.stdin)
33.     tool_name = data.get("tool_name", "")
34.     tool_input = data.get("tool_input", {})
35. 
36.     # Only check file-editing tools
37.     if tool_name not in ("editFiles", "createFile"):
38.         sys.exit(0)
39. 
40.     files = tool_input.get("files", [])
41.     file_path = tool_input.get("filePath", "")
42.     paths_to_check = files if files else ([file_path] if file_path else [])
43. 
44.     for fp in paths_to_check:
45.         if is_protected(fp):
46.             result = {
47.                 "hookSpecificOutput": {
48.                     "hookEventName": "PreToolUse",
49.                     "permissionDecision": "deny",
50.                     "permissionDecisionReason": (
51.                         f"Edit blocked: '{fp}' is protected by security policy. "
52.                         "See docs/security-policy.md for the change approval process."
53.                     ),
54.                 }
55.             }
56.             json.dump(result, sys.stdout)
57.             sys.exit(0)
58. 
59.     sys.exit(0)
60. 
61. 
62. if __name__ == "__main__":
63.     main()
64.
```

</details>


---

<sub>⏱️ 15s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\validate_commit.py.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\validate_commit.py

<details>
<summary>52 lines</summary>

```
1. #!/usr/bin/env python3
2. """Pre-commit validation script (Python replacement for validate-commit.sh).
3. 
4. Called by the pre-commit hook to ensure code quality before committing.
5. Usage: python validate_commit.py
6. """
7. import subprocess
8. import sys
9. from pathlib import Path
10. 
11. 
12. def run_step(name: str, cmd: list[str]) -> bool:
13.     """Run a validation step and return True if it passed."""
14.     print(f"  {name}...")
15.     result = subprocess.run(cmd, capture_output=True, text=True)
16.     if result.returncode != 0:
17.         print(f"  FAIL: {name}")
18.         if result.stdout:
19.             print(result.stdout[:500])
20.         if result.stderr:
21.             print(result.stderr[:500])
22.         return False
23.     print(f"  OK")
24.     return True
25. 
26. 
27. def main() -> None:
28.     print("=== Pre-commit validation ===")
29. 
30.     steps = [
31.         ("[1/3] TypeScript compilation", ["npx", "tsc", "--noEmit"]),
32.     ]
33. 
34.     # Only run eslint if config exists
35.     if Path(".eslintrc.json").exists() or Path("eslint.config.js").exists():
36.         steps.append(("[2/3] Lint", ["npx", "eslint", "src/", "tests/", "--max-warnings", "0"]))
37.     else:
38.         print("  [2/3] Lint skipped (no eslint config found)")
39. 
40.     steps.append(("[3/3] Tests", ["npx", "vitest", "run", "--reporter=verbose"]))
41. 
42.     for name, cmd in steps:
43.         if not run_step(name, cmd):
44.             print(f"\nFAIL: {name} failed. Fix issues before committing.")
45.             sys.exit(1)
46. 
47.     print("\n=== All checks passed ===")
48. 
49. 
50. if __name__ == "__main__":
51.     main()
52.
```

</details>


---

<sub>⏱️ 42s</sub>

### 💬 Copilot

## Summary

This lesson’s guardrails are **partially aligned but not internally consistent**. The strongest controls are the read-only MCP permissions and the documented fail-closed audit requirement. The weakest area is hook-policy parity: the protected-file policy in `docs/security-policy.md` does **not** match what `.github/scripts/check_protected_files.py` actually blocks, and the “pre-commit” hook is modeled as a generic `PreToolUse` command rather than an actual commit-time gate.

## Confirmed controls

- **SQLite MCP is read-only** in `.github/mcp.json:3-15`, and that matches both `.github/copilot-instructions.md:15-16` and `docs/tool-trust-boundaries.md:21`.
- **Filesystem MCP is read-only** in `.github/mcp.json:16-31`.
- **Filesystem scope matches the documented trust boundaries**: both `.github/mcp.json:21-24` and `docs/tool-trust-boundaries.md:22` include:
  - `src/backend/src`
  - `src/backend/tests`
  - `src/frontend/src`
  - `docs`
- **Protected-file enforcement exists** via `.github/hooks/file-protection.json:1-10` calling `.github/scripts/check_protected_files.py`.
- **Validation enforcement exists** via `.github/hooks/pre-commit-validate.json:1-10` calling `.github/scripts/validate_commit.py`.
- **Validation script actually runs compile/tests**, and lint conditionally, in `.github/scripts/validate_commit.py:30-40`.
- **Formatting enforcement exists** via `.github/hooks/post-save-format.json:1-10`, which invokes Prettier.

## Inconsistencies with file references

### 1. Protected-file policy does not match hook enforcement
- Policy says protected files are:
  - `.env` / `.env.*`
  - `src/backend/src/config/feature-flags.ts`
  - `src/backend/src/db/schema.sql`
  - `src/backend/src/db/seed.ts`
  - `docs/security-policy.md:11-16`
- Hook script protects:
  - `.env`
  - `src/backend/src/config/feature-flags.ts`
  - `src/backend/src/db/connection.ts`
  - `.github/scripts/check_protected_files.py:16-20`

**Conclusion:** protected-file policy and hook enforcement **do not match**.

### 2. Filesystem scope conflicts between instructions and trust-boundary docs
- `.github/copilot-instructions.md:17-19` says filesystem access is limited to `src/backend/src/`, `src/backend/tests/`, and `docs/`.
- `.github/mcp.json:21-24` and `docs/tool-trust-boundaries.md:22` also allow `src/frontend/src/`.

**Conclusion:** the filesystem scope **matches the documented trust boundaries**, but **not** the Copilot instructions.

### 3. “Pre-commit” hook is described as commit-time, but configured as `PreToolUse`
- Docs describe a **pre-commit validation** hook: `.github/copilot-instructions.md:27-28`.
- Actual hook file uses `"PreToolUse"`: `.github/hooks/pre-commit-validate.json:2-9`.

**Conclusion:** naming and runtime semantics are inconsistent. This looks more like “run validation before tool use” than “run on git commit.”

### 4. “Post-save formatting” is described narrowly, but hook file is broad
- Docs say Prettier runs after every `.ts` file save: `.github/copilot-instructions.md:29-30`.
- Hook config simply runs `npx prettier --write "$TOOL_INPUT_FILE_PATH"` on `PostToolUse`: `.github/hooks/post-save-format.json:2-8`.

**Conclusion:** no `.ts` scoping is visible in the hook file itself.

### 5. Fail-closed audit rule is documented, but not represented in hooks/scripts here
- `.github/copilot-instructions.md:36`
- `docs/security-policy.md:33-41`

Both document fail-closed behavior, but the inspected hooks/scripts do not verify route ordering, 503 behavior, or audit-before-persist semantics.

### 6. 404-not-403 rule is not represented consistently
- Present in `.github/copilot-instructions.md:39`
- Not present in `docs/security-policy.md`
- Not represented in the inspected hooks/scripts

**Conclusion:** the **404-not-403 rule is not consistently represented** across the lesson artifacts.

## False positives

These are cases where enforcement appears stricter than the documented policy:

- `src/backend/src/db/connection.ts` is blocked by hook script but is **not** listed as protected in `docs/security-policy.md:11-16`.
  - Source: `.github/scripts/check_protected_files.py:18-20`

- The formatting hook may apply beyond `.ts` saves because `.github/hooks/post-save-format.json:2-8` does not show any extension filter, despite docs saying `.ts` only.

## Hard negatives

These are documented protections that are **not actually enforced** by the inspected hook script:

- `src/backend/src/db/schema.sql` is documented protected but absent from `.github/scripts/check_protected_files.py:16-20`.
- `src/backend/src/db/seed.ts` is documented protected but absent from `.github/scripts/check_protected_files.py:16-20`.

These are the highest-confidence enforcement gaps in the lesson.

## Prioritized fixes

1. **Align protected-file policy and hook enforcement first.**
   - Update `.github/scripts/check_protected_files.py` or `docs/security-policy.md` so both list the same protected files.
   - At minimum, reconcile `schema.sql`, `seed.ts`, and `db/connection.ts`.

2. **Resolve filesystem-scope drift.**
   - Either add `src/frontend/src/` to `.github/copilot-instructions.md`, or remove it from `.github/mcp.json` and `docs/tool-trust-boundaries.md`.

3. **Clarify hook semantics.**
   - If validation is truly pre-commit, the configuration/documentation should reflect commit-time execution rather than generic `PreToolUse`.
   - If the platform only supports tool hooks, rename the control to avoid overclaiming.

4. **Document or enforce the 404-not-403 rule uniformly.**
   - Add it to `docs/security-policy.md` and back it with tests or a validation check.

5. **Narrow formatting-hook scope explicitly.**
   - Ensure the post-save formatter is limited to `.ts` files if that is the intended policy.

## Residual risks

- **Policy drift risk:** multiple sources of truth disagree (`copilot-instructions`, trust-boundary doc, security policy, hook script).
- **Overclaimed enforcement risk:** docs imply stronger guarantees than the hook files demonstrate.
- **Coverage gap risk:** fail-closed audit and 404-not-403 are documented rules, but nothing in the inspected hook layer proves they are enforced.
- **Tool-name dependency risk:** `.github/scripts/check_protected_files.py:37-38` only checks `editFiles` and `createFile`; if other editing tool names exist in the runtime, protection may be bypassed.

## What the CLI cannot demonstrate here

Because **VS Code hooks do not run in this CLI session**, I can only audit the static hook/config files. I **cannot demonstrate**:
- that `PreToolUse` / `PostToolUse` actually fire,
- that `$TOOL_INPUT_FILE_PATH` is populated correctly,
- that file-protection blocks real edits in the editor,
- that formatting runs on save,
- or that validation truly blocks commits in practice.

So this is a **read-only design/config audit**, not a live enforcement test.

---

<sub>Generated by [GitHub Copilot CLI](https://github.com/features/copilot/cli)</sub>
