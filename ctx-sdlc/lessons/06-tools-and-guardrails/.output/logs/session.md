# 🤖 Copilot CLI Session

> [!NOTE]
> - **Session ID:** `40c75b31-2f1d-4e6a-818e-77eed151539f`  
> - **Started:** 14/03/2026, 01:51:45  
> - **Duration:** 3m 13s  
> - **Exported:** 14/03/2026, 01:54:59  

---

<sub>⏱️ 5s</sub>

### 👤 User

Inspect the lesson's guardrail-related instructions, hook configs, scripts, MCP config, and policy docs before answering. Discover the relevant files rather than assuming a fixed list. Then implement a new import-validation guardrail that enforces the project's barrel-file import convention during pre-commit. Create the hook config in .github/hooks/import-validation.json following the pattern of the existing hook configs. Create the validation script in .github/scripts/validate_imports.py following the pattern of the existing guardrail scripts. The hook must use PreToolUse event type and invoke the Python validation script. The validation script must check that TypeScript files import from barrel files (index.ts) rather than reaching into internal module paths. Apply the changes directly in files. Do not run shell commands and do not use SQL.

---

<sub>⏱️ 15s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails**

"**/.github/**/*.json" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\mcp.json
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\hooks\pre-commit-validate.json
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\hooks\post-save-format.json
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\hooks\file-protection.json
```


---

<sub>⏱️ 15s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails**

"**/.github/**/*.py" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\validate_commit.py
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\format_file.py
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\check_protected_files.py
```


---

<sub>⏱️ 15s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails**

"**/docs/**/*.md" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\docs\tool-trust-boundaries.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\docs\security-policy.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\docs\guardrail-audit-example.md
```


---

<sub>⏱️ 15s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "guardrail|hook|PreToolUse|mcp|policy|barrel|index\\.ts|import",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\06-tools-and-guardrails",
  "output_mode": "files_with_matches",
  "glob": "*.{md,json,py,ts}",
  "-i": true,
  "head_limit": 200
}
```

</details>

<details>
<summary>14 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\util.py
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\README.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\ASSESSMENT.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\docs\tool-trust-boundaries.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\docs\security-policy.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\docs\guardrail-audit-example.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\copilot-instructions.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\mcp.json
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\hooks\pre-commit-validate.json
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\hooks\file-protection.json
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\hooks\post-save-format.json
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\check_protected_files.py
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\format_file.py
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\validate_commit.py
```

</details>


---

<sub>⏱️ 20s</sub>

### 💬 Copilot

I found the lesson’s actual guardrail surfaces. Next I’m reading the existing configs/scripts and the TypeScript layout so the new guardrail matches the lesson’s patterns instead of inventing one.

---

<sub>⏱️ 20s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Add File: C:/Users/nilay/.copilot/session-state/40c75b31-2f1d-4e6a-818e-77eed151539f/plan.md\n+## Plan\n+\n+1. Inspect existing Copilot instructions, hook configs, guardrail scripts, MCP config, and policy docs.\n+2. Inspect TypeScript source layout to confirm the barrel-file import convention and identify representative imports.\n+3. Add `.github/hooks/import-validation.json` matching existing hook config structure and using `PreToolUse`.\n+4. Add `.github/scripts/validate_imports.py` matching existing script conventions and enforcing barrel-file imports.\n+5. Review affected files to verify consistency with project patterns.\n*** End Patch\n"
```

</details>

```
Added 1 file(s): C:\Users\nilay\.copilot\session-state\40c75b31-2f1d-4e6a-818e-77eed151539f\plan.md
```


---

<sub>⏱️ 28s</sub>

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

<sub>⏱️ 28s</sub>

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

<sub>⏱️ 28s</sub>

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

<sub>⏱️ 28s</sub>

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

<sub>⏱️ 28s</sub>

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

<sub>⏱️ 28s</sub>

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

<sub>⏱️ 28s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\format_file.py.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\format_file.py

<details>
<summary>24 lines</summary>

```
1. #!/usr/bin/env python3
2. """Post-save formatting script (Python replacement for format-file.sh).
3. 
4. Called by the post-save hook to auto-format TypeScript files.
5. Usage: python format_file.py <filepath>
6. """
7. import subprocess
8. import sys
9. from pathlib import Path
10. 
11. 
12. def main() -> None:
13.     if len(sys.argv) < 2:
14.         print("Usage: python format_file.py <filepath>", file=sys.stderr)
15.         sys.exit(1)
16. 
17.     filepath = Path(sys.argv[1])
18.     if filepath.suffix in (".ts", ".tsx"):
19.         subprocess.run(["npx", "prettier", "--write", str(filepath)], check=True)
20. 
21. 
22. if __name__ == "__main__":
23.     main()
24.
```

</details>


---

<sub>⏱️ 28s</sub>

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

<sub>⏱️ 28s</sub>

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

<sub>⏱️ 28s</sub>

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

<sub>⏱️ 28s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\docs\guardrail-audit-example.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\docs\guardrail-audit-example.md

<details>
<summary>46 lines</summary>

```
1. # Lesson 06 — Guardrail Implementation Example
2. 
3. This document defines the concrete example used in Lesson 06.
4. 
5. ## Objective
6. 
7. Show that the CLI can discover existing guardrail patterns and create a new import-validation guardrail that follows the same conventions — producing assessable file changes.
8. 
9. ## Expected Output Shape
10. 
11. The demo must produce two new files:
12. 
13. 1. `.github/hooks/import-validation.json` — PreToolUse hook config matching existing hook patterns
14. 2. `.github/scripts/validate_imports.py` — validation script enforcing barrel-file import convention
15. 
16. ## Expected Change Artifacts
17. 
18. Assessment compares the actual `demo.patch` and `changed-files.json` against:
19. 
20. - `.output/change/expected-files.json` — expected added/modified/deleted files
21. - `.output/change/expected-patterns.json` — regex patterns that must appear in the patch
22. 
23. ## Required Constraints
24. 
25. 1. The hook config must use `PreToolUse` event type following existing hook file patterns.
26. 2. The validation script must check that TypeScript files import from barrel files (index.ts) rather than reaching into internal module paths.
27. 3. The implementation must follow the discovered conventions from existing hook configs and scripts.
28. 4. The change must stay scoped to `.github/hooks/` and `.github/scripts/`.
29. 5. Do not run shell commands during the assessment run.
30. 6. Do not use SQL during the assessment run.
31. 
32. ## Concrete Scenario
33. 
34. Use the lesson's existing hook configs (file-protection, pre-commit-validate, post-save-format) and their scripts as pattern references to create a new import-validation guardrail.
35. 
36. Good output should produce a hook + script pair that is consistent with the existing guardrail style.
37. 
38. ## What Good Output Looks Like
39. 
40. Good output will usually:
41. 
42. - create a hook JSON config with `PreToolUse` event type and a reference to `validate_imports.py`
43. - create a Python validation script that checks import paths
44. - follow the same structure and conventions as the existing hook + script pairs
45. - keep the change scoped to the `.github/` guardrail surface
46.
```

</details>


---

<sub>⏱️ 28s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails**

"src/**/*.ts" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails

```
No files matched the pattern.
```


---

<sub>⏱️ 28s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails**

"src/**/index.ts" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails

```
No files matched the pattern.
```


---

<sub>⏱️ 28s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "from ['\\\"][^'\\\"]+['\\\"]",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\06-tools-and-guardrails\\src",
  "output_mode": "content",
  "glob": "*.ts",
  "-n": true,
  "head_limit": 200
}
```

</details>

<details>
<summary>9 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\frontend\vite.config.ts:1:import { defineConfig } from "vite";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\unit\state-machine.test.ts:5:import { describe, it, expect } from "vitest";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\unit\state-machine.test.ts:10:} from "../../src/rules/state-machine.js";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\integration\decisions.test.ts:5:import { describe, it, expect } from "vitest";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\integration\applications.test.ts:5:import { describe, it, expect } from "vitest";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\unit\notification-service.test.ts:5:import { describe, it, expect, vi, beforeEach } from "vitest";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\unit\business-rules.test.ts:5:import { describe, it, expect } from "vitest";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\unit\business-rules.test.ts:10:} from "../../src/rules/business-rules.js";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\unit\business-rules.test.ts:11:import type { LoanApplication } from "../../src/models/types.js";
```

</details>


---

<sub>⏱️ 40s</sub>

### 💬 Copilot

I’ve confirmed the lesson explicitly expects this exact hook/script pair. I’m now checking the source layout to make the validator enforce the real import convention instead of a guessed regex.

---

<sub>⏱️ 40s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src

<details>
<summary>6 lines</summary>

```
.env.example
backend
frontend
package-lock.json
package.json
tsconfig.json
```

</details>


---

<sub>⏱️ 40s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src

<details>
<summary>9 lines</summary>

```
app.ts
config
db
middleware
models
queue
routes
rules
services
```

</details>


---

<sub>⏱️ 40s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests

```
integration
unit
```


---

<sub>⏱️ 40s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "^export\\s+(\\*|\\{)|^export\\s+type",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\06-tools-and-guardrails\\src",
  "output_mode": "content",
  "glob": "*.ts",
  "-n": true,
  "head_limit": 200
}
```

</details>

```
No matches found.
```


---

<sub>⏱️ 40s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "index\\.ts",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\06-tools-and-guardrails\\src",
  "output_mode": "files_with_matches",
  "glob": "*.ts",
  "head_limit": 200
}
```

</details>

```
No matches found.
```


---

<sub>⏱️ 40s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "from ['\\\"](\\.{1,2}/[^'\\\"]+)['\\\"]",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\06-tools-and-guardrails\\src\\backend",
  "output_mode": "content",
  "glob": "*.ts",
  "-n": true,
  "head_limit": 200
}
```

</details>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\unit\state-machine.test.ts:10:} from "../../src/rules/state-machine.js";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\unit\business-rules.test.ts:10:} from "../../src/rules/business-rules.js";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\unit\business-rules.test.ts:11:import type { LoanApplication } from "../../src/models/types.js";
```


---

<sub>⏱️ 47s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "tool_input|TOOL_INPUT|filePath|oldString|newString|content",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\06-tools-and-guardrails",
  "output_mode": "content",
  "glob": "*.{md,json,py}",
  "-n": true,
  "head_limit": 200
}
```

</details>

<details>
<summary>6 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\util.py:153:def _write_text_atomic(path: Path, content: str) -> None:
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\util.py:163:    handle.write(content)
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\check_protected_files.py:34:    tool_input = data.get("tool_input", {})
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\check_protected_files.py:40:    files = tool_input.get("files", [])
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\check_protected_files.py:41:    file_path = tool_input.get("filePath", "")
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\hooks\post-save-format.json:6:        "command": "npx prettier --write \"$TOOL_INPUT_FILE_PATH\"",
```

</details>


---

<sub>⏱️ 47s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\docs**

"**/*hook*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\docs

```
No files matched the pattern.
```


---

<sub>⏱️ 47s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\README.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\README.md

<details>
<summary>86 lines</summary>

````
1. # Lesson 06 — Tools and Guardrails
2. 
3. > **App:** Loan Workbench (TypeScript Express API + SQLite)
4. > **Topic:** Hooks, MCP configuration, and runtime scripts that guard against unsafe operations.
5. 
6. ## Setup
7. 
8. ```bash
9. python util.py --setup
10. python util.py --run
11. ```
12. 
13. ## What This Demonstrates
14. 
15. Hooks intercept Copilot tool calls at runtime to enforce guardrails.
16. 
17. | Hook File                  | Event       | Purpose                                    |
18. | -------------------------- | ----------- | ------------------------------------------ |
19. | `file-protection.json`     | PreToolUse  | Blocks edits to protected files            |
20. | `post-save-format.json`    | PostToolUse | Auto-formats files after writes            |
21. | `pre-commit-validate.json` | PreToolUse  | Validates changes before commit operations |
22. 
23. This lesson also includes MCP configuration for extending tool capabilities.
24. 
25. ## Example Goal
26. 
27. This lesson should demonstrate guardrail implementation, not just analysis.
28. 
29. For this example, the intended outcome is:
30. 
31. - inspect the hook, MCP, and policy files to discover existing guardrail patterns
32. - create a new import-validation guardrail (hook config + validation script) that follows those patterns
33. - the new guardrail must enforce barrel-file import conventions for TypeScript files
34. - the change is assessable via actual vs expected file and pattern comparison
35. 
36. ## Context Files
37. 
38. | Path                                       | Purpose                                                   |
39. | ------------------------------------------ | --------------------------------------------------------- |
40. | `.github/hooks/file-protection.json`       | PreToolUse hook                                           |
41. | `.github/hooks/post-save-format.json`      | PostToolUse hook                                          |
42. | `.github/hooks/pre-commit-validate.json`   | PreToolUse hook                                           |
43. | `.github/scripts/check_protected_files.py` | File protection script                                    |
44. | `.github/scripts/format_file.py`           | Formatter script                                          |
45. | `.github/scripts/validate_commit.py`       | Commit validation script                                  |
46. | `.github/mcp.json`                         | MCP server configuration                                  |
47. | `docs/security-policy.md`                  | Security policy                                           |
48. | `docs/tool-trust-boundaries.md`            | Tool trust boundaries                                     |
49. | `docs/guardrail-audit-example.md`          | Concrete lesson-06 demo target and assessment constraints |
50. 
51. ## Copilot CLI Workflow
52. 
53. Create a new guardrail:
54. 
55. ```bash
56. copilot -p "Inspect the lesson's guardrail-related instructions, hook configs, scripts, MCP config, and policy docs before answering. Discover the relevant files rather than assuming a fixed list. Then implement a new import-validation guardrail that enforces the project's barrel-file import convention during pre-commit. Create the hook config in .github/hooks/import-validation.json following the pattern of the existing hook configs. Create the validation script in .github/scripts/validate_imports.py following the pattern of the existing guardrail scripts. The hook must use PreToolUse event type and invoke the Python validation script. The validation script must check that TypeScript files import from barrel files (index.ts) rather than reaching into internal module paths. Apply the changes directly in files. Do not run shell commands and do not use SQL." --allow-all-tools --deny-tool=powershell --deny-tool=sql
57. ```
58. 
59. Expected outcome:
60. 
61. - the CLI creates `.github/hooks/import-validation.json` and `.github/scripts/validate_imports.py`
62. - the hook config uses `PreToolUse` event type following existing patterns
63. - the validation script enforces barrel-file imports
64. - `.output/change/demo.patch` contains the new files
65. - `.output/change/comparison.md` shows actual vs expected file and pattern match results
66. 
67. ## VS Code Chat Workflow
68. 
69. Ask Copilot to perform edits that should trigger hooks.
70. 
71. Examples:
72. 
73. - ask it to edit a protected file and observe the block
74. - ask it to create or update a normal source file and observe post-save formatting
75. - inspect the GitHub Copilot output logs to confirm hook execution
76. 
77. Expected result: you can see the operational difference between static instructions and runtime guardrails.
78. 
79. For the captured demo run, use `python util.py --demo --model gpt-5.4`.
80. 
81. ## Cleanup
82. 
83. ```bash
84. python util.py --clean
85. ```
86.
````

</details>


---

<sub>⏱️ 47s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\ASSESSMENT.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\ASSESSMENT.md

<details>
<summary>52 lines</summary>

````
1. # Lesson 06 CLI Prompt Assessment
2. 
3. This assessment is intentionally narrow.
4. 
5. It evaluates only whether the code changes produced by the lesson's GitHub Copilot CLI prompt respected the required standards, constraints, and repository context for that prompt.
6. 
7. It does not assess the lesson overall.
8. 
9. ## Prompt Under Test
10. 
11. ```text
12. Inspect the lesson's guardrail-related instructions, hook configs, scripts, MCP config, and policy docs before answering. Discover the relevant files rather than assuming a fixed list. Then implement a new import-validation guardrail that enforces the project's barrel-file import convention during pre-commit. Create the hook config in .github/hooks/import-validation.json following the pattern of the existing hook configs. Create the validation script in .github/scripts/validate_imports.py following the pattern of the existing guardrail scripts. The hook must use PreToolUse event type and invoke the Python validation script. The validation script must check that TypeScript files import from barrel files (index.ts) rather than reaching into internal module paths. Apply the changes directly in files. Do not run shell commands and do not use SQL.
13. ```
14. 
15. The assessment run uses the model from `lessons/_common/assessment-config.json`.
16. 
17. ## Assessment Scope
18. 
19. The only question being evaluated is:
20. 
21. > Did the produced code changes implement the prompt in a way that follows the repository's standards, constraints, and discovered guardrail patterns?
22. 
23. ## Expected Change Artifacts
24. 
25. Assessment compares actual output against gold-standard expectations:
26. 
27. - `.output/change/expected-files.json` — expected files: `.github/hooks/import-validation.json` (added), `.github/scripts/validate_imports.py` (added)
28. - `.output/change/expected-patterns.json` — required patterns in patch: PreToolUse, validate_imports.py, import, barrel/index.ts
29. 
30. The `compare_with_expected()` function writes `.output/change/comparison.md` with a structured match report.
31. 
32. ## Assessment Criteria
33. 
34. | Criterion | Source |
35. | --- | --- |
36. | Hook config created at `.github/hooks/import-validation.json` | `expected-files.json` |
37. | Validation script created at `.github/scripts/validate_imports.py` | `expected-files.json` |
38. | Hook uses `PreToolUse` event type | `expected-patterns.json` |
39. | Hook references `validate_imports.py` | `expected-patterns.json` |
40. | Script checks import paths | `expected-patterns.json` |
41. | Script enforces barrel-file (index.ts) convention | `expected-patterns.json` |
42. | No shell commands executed | Prompt constraint |
43. | No SQL tools used | Prompt constraint |
44. 
45. ## Captured Result
46. 
47. Pending re-run with the updated implementation-oriented prompt. Previous assessment was for a read-only guardrail audit demo that has been replaced.
48. 
49. ## Verdict
50. 
51. Pending re-run.
52.
````

</details>


---

<sub>⏱️ 52s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\util.py**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "editFiles|createFile|tool_name|tool_input",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\06-tools-and-guardrails\\util.py",
  "output_mode": "content",
  "-n": true,
  "head_limit": 100
}
```

</details>

```
No matches found.
```


---

<sub>⏱️ 52s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\util.py.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\util.py (lines 1-260)

<details>
<summary>260 lines</summary>

```
1. #!/usr/bin/env python3
2. """Lesson 06 — Tools And Guardrails workspace utility.
3. 
4. Usage:
5.   python util.py --setup    Copy app source into src/, create .env interactively
6.   python util.py --run      Install deps + start backend & frontend dev servers
7.   python util.py --clean    Remove copied src/ and build artifacts
8.   python util.py --demo     Run a Copilot CLI guardrail-audit demo and capture artifacts
9. """
10. 
11. from __future__ import annotations
12. 
13. import difflib
14. import json
15. import os
16. import shutil
17. import subprocess
18. import sys
19. import tempfile
20. import time
21. from pathlib import Path
22. 
23. MODEL_OVERRIDE_FLAG = "--model"
24. LESSON = Path(__file__).resolve().parent
25. APP_SOURCE = LESSON.parent.parent / "app"
26. CONFIG_PATH = LESSON.parent / "_common" / "assessment-config.json"
27. OUTPUT_DIR = LESSON / ".output"
28. LOG_DIR = OUTPUT_DIR / "logs"
29. CHANGE_DIR = OUTPUT_DIR / "change"
30. KEPT_LOG_FILES = {"command.txt", "prompt.txt", "session.md", "copilot.log"}
31. RUNNER_LOG_PATH = LOG_DIR / "runner.log"
32. TEXT_EXTENSIONS = {
33.   ".css",
34.   ".html",
35.   ".js",
36.   ".json",
37.   ".md",
38.   ".mjs",
39.   ".ts",
40.   ".tsx",
41.   ".txt",
42.   ".yaml",
43.   ".yml",
44. }
45. 
46. sys.path.insert(0, str(LESSON.parent / "_common"))
47. from util_base import clean, compare_with_expected, main  # noqa: E402
48. 
49. 
50. def _extract_model_override(argv: list[str]) -> tuple[list[str], str | None]:
51.   if MODEL_OVERRIDE_FLAG not in argv:
52.     return argv, None
53. 
54.   index = argv.index(MODEL_OVERRIDE_FLAG)
55.   if index + 1 >= len(argv):
56.     raise SystemExit("ERROR: --model requires a value.")
57. 
58.   model_name = argv[index + 1]
59.   trimmed = argv[:index] + argv[index + 2 :]
60.   return trimmed, model_name
61. 
62. 
63. sys.argv, _MODEL_OVERRIDE = _extract_model_override(sys.argv)
64. if _MODEL_OVERRIDE:
65.   os.environ["CTX_SDLC_COPILOT_MODEL"] = _MODEL_OVERRIDE
66. 
67. 
68. def _load_assessment_config() -> dict[str, object]:
69.   if not CONFIG_PATH.exists():
70.     return {}
71.   return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
72. 
73. 
74. ASSESSMENT_CONFIG = _load_assessment_config()
75. DEMO_TIMEOUT_SECONDS = int(
76.   os.environ.get(
77.     "CTX_SDLC_DEMO_TIMEOUT",
78.     str(ASSESSMENT_CONFIG.get("defaultDemoTimeoutSeconds", 180)),
79.   )
80. )
81. DEMO_MODEL = os.environ.get(
82.   "CTX_SDLC_COPILOT_MODEL",
83.   str(ASSESSMENT_CONFIG.get("defaultAssessmentModel", "claude-haiku-4.5")),
84. )
85. 
86. 
87. def _is_text_file(path: Path) -> bool:
88.   return path.suffix.lower() in TEXT_EXTENSIONS
89. 
90. 
91. def _snapshot_tree(root: Path) -> dict[str, str]:
92.   snapshot: dict[str, str] = {}
93.   if not root.exists():
94.     return snapshot
95. 
96.   for path in sorted(root.rglob("*")):
97.     if not path.is_file() or not _is_text_file(path):
98.       continue
99.     if any(part in {"node_modules", "dist", "data", ".git", ".output"} for part in path.parts):
100.       continue
101.     snapshot[path.relative_to(root).as_posix()] = path.read_text(encoding="utf-8")
102.   return snapshot
103. 
104. 
105. def _reset_output_dirs() -> None:
106.   for directory in (LOG_DIR, CHANGE_DIR):
107.     if directory.exists():
108.       shutil.rmtree(directory)
109.     directory.mkdir(parents=True, exist_ok=True)
110. 
111. 
112. def _reset_demo_workspace() -> Path:
113.   clean(LESSON)
114.   src_dir = LESSON / "src"
115.   shutil.copytree(
116.     APP_SOURCE,
117.     src_dir,
118.     ignore=shutil.ignore_patterns("node_modules", ".env", "*.db", "data"),
119.   )
120.   return src_dir
121. 
122. 
123. def _demo_prompt() -> str:
124.   return (
125.     "Inspect the lesson's guardrail-related instructions, hook configs, scripts, MCP config, and policy docs before answering. "
126.     "Discover the relevant files rather than assuming a fixed list. "
127.     "Then implement a new import-validation guardrail that enforces the project's barrel-file import convention during pre-commit. "
128.     "Create the hook config in .github/hooks/import-validation.json following the pattern of the existing hook configs. "
129.     "Create the validation script in .github/scripts/validate_imports.py following the pattern of the existing guardrail scripts. "
130.     "The hook must use PreToolUse event type and invoke the Python validation script. "
131.     "The validation script must check that TypeScript files import from barrel files (index.ts) rather than reaching into internal module paths. "
132.     "Apply the changes directly in files. Do not run shell commands and do not use SQL."
133.   )
134. 
135. 
136. def _resolve_copilot_executable() -> str:
137.   copilot_executable = (
138.     shutil.which("copilot.cmd")
139.     or shutil.which("copilot.bat")
140.     or shutil.which("copilot")
141.   )
142.   if copilot_executable is None:
143.     raise FileNotFoundError("Could not resolve the Copilot CLI executable on PATH.")
144.   return copilot_executable
145. 
146. 
147. def _validate_demo_model() -> str:
148.   if not DEMO_MODEL.strip():
149.     raise RuntimeError("Assessment model configuration is empty.")
150.   return DEMO_MODEL
151. 
152. 
153. def _write_text_atomic(path: Path, content: str) -> None:
154.   path.parent.mkdir(parents=True, exist_ok=True)
155.   with tempfile.NamedTemporaryFile(
156.     "w",
157.     encoding="utf-8",
158.     delete=False,
159.     dir=path.parent,
160.     prefix=f".{path.name}.",
161.     suffix=".tmp",
162.   ) as handle:
163.     handle.write(content)
164.     temp_path = Path(handle.name)
165.   temp_path.replace(path)
166. 
167. 
168. def _write_json(path: Path, payload: object) -> None:
169.   _write_text_atomic(path, json.dumps(payload, indent=2) + "\n")
170. 
171. 
172. def _write_diff(before: dict[str, str], after: dict[str, str]) -> dict[str, list[str]]:
173.   keys = sorted(set(before) | set(after))
174.   patch_chunks: list[str] = []
175.   changed = {"added": [], "modified": [], "deleted": []}
176. 
177.   for key in keys:
178.     old_text = before.get(key)
179.     new_text = after.get(key)
180.     if old_text == new_text:
181.       continue
182. 
183.     if old_text is None:
184.       changed["added"].append(key)
185.     elif new_text is None:
186.       changed["deleted"].append(key)
187.     else:
188.       changed["modified"].append(key)
189. 
190.     diff = difflib.unified_diff(
191.       (old_text or "").splitlines(keepends=True),
192.       (new_text or "").splitlines(keepends=True),
193.       fromfile=f"a/{key}",
194.       tofile=f"b/{key}",
195.       n=3,
196.     )
197.     patch_chunks.append("".join(diff))
198. 
199.   _write_text_atomic(CHANGE_DIR / "demo.patch", "\n".join(chunk for chunk in patch_chunks if chunk))
200.   _write_json(CHANGE_DIR / "changed-files.json", changed)
201.   return changed
202. 
203. 
204. def _wait_for_fresh_artifacts(run_started_at: float) -> None:
205.   required_paths = [
206.     LOG_DIR / "command.txt",
207.     LOG_DIR / "prompt.txt",
208.     LOG_DIR / "session.md",
209.     LOG_DIR / "copilot.log",
210.     CHANGE_DIR / "demo.patch",
211.     CHANGE_DIR / "changed-files.json",
212.   ]
213.   stable_hits = 0
214.   previous_state: tuple[tuple[str, int, int], ...] | None = None
215.   deadline = time.time() + 15
216. 
217.   while time.time() < deadline:
218.     if not all(path.exists() for path in required_paths):
219.       time.sleep(0.5)
220.       continue
221. 
222.     current_state = tuple(
223.       (str(path), path.stat().st_size, int(path.stat().st_mtime_ns))
224.       for path in required_paths
225.     )
226.     if any(state[2] < int(run_started_at * 1_000_000_000) for state in current_state):
227.       time.sleep(0.5)
228.       previous_state = current_state
229.       stable_hits = 0
230.       continue
231. 
232.     if current_state == previous_state:
233.       stable_hits += 1
234.     else:
235.       stable_hits = 0
236.       previous_state = current_state
237. 
238.     if stable_hits >= 2:
239.       return
240. 
241.     time.sleep(0.5)
242. 
243. 
244. def _kill_process_tree(pid: int) -> None:
245.   if os.name == "nt":
246.     subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True, check=False, shell=False)
247.     return
248.   try:
249.     os.kill(pid, 9)
250.   except ProcessLookupError:
251.     return
252. 
253. 
254. def _finalize_log_dir() -> None:
255.   process_logs = sorted(LOG_DIR.glob("process-*.log"), key=lambda path: path.stat().st_mtime, reverse=True)
256.   target_log = LOG_DIR / "copilot.log"
257.   if target_log.exists():
258.     target_log.unlink()
259.   if process_logs:
260.     process_logs[0].replace(target_log)
```

</details>


---

<sub>⏱️ 52s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails**

"src/backend/src/**/*.ts" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails

```
No files matched the pattern.
```


---

<sub>⏱️ 52s</sub>

### ❌ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\package.json.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\package.json

```
Path does not exist
```


---

<sub>⏱️ 57s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src**

"**/package.json" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\package.json
```


---

<sub>⏱️ 57s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src**

"**/tsconfig*.json" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\tsconfig.json
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\frontend\tsconfig.json
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tsconfig.json
```


---

<sub>⏱️ 57s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "from ['\\\"]\\.\\.?/.+/.+['\\\"]",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\06-tools-and-guardrails\\src",
  "output_mode": "content",
  "glob": "*.ts",
  "-n": true,
  "head_limit": 200
}
```

</details>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\unit\state-machine.test.ts:10:} from "../../src/rules/state-machine.js";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\unit\business-rules.test.ts:10:} from "../../src/rules/business-rules.js";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\unit\business-rules.test.ts:11:import type { LoanApplication } from "../../src/models/types.js";
```


---

<sub>⏱️ 57s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "from ['\\\"][^'\\\"]+index\\.js['\\\"]|from ['\\\"][^'\\\"]+/index['\\\"]",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\06-tools-and-guardrails\\src",
  "output_mode": "content",
  "glob": "*.ts",
  "-n": true,
  "head_limit": 100
}
```

</details>

```
No matches found.
```


---

<sub>⏱️ 1m 2s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\package.json.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\package.json

<details>
<summary>34 lines</summary>

```
1. {
2.   "name": "loan-workbench",
3.   "version": "1.0.0",
4.   "description": "Loan Workbench — commercial loan processing platform with backend API, embedded message queue, SQLite database, and web frontend.",
5.   "private": true,
6.   "type": "module",
7.   "scripts": {
8.     "dev": "concurrently -n api,web -c blue,green \"npm:dev:backend\" \"npm:dev:frontend\"",
9.     "dev:backend": "tsx watch backend/src/app.ts",
10.     "dev:frontend": "vite frontend --port 5173",
11.     "start": "node backend/dist/app.js",
12.     "build": "tsc -p tsconfig.json",
13.     "test": "vitest run",
14.     "test:watch": "vitest",
15.     "db:seed": "tsx backend/src/db/seed.ts",
16.     "lint": "eslint backend/src/ frontend/src/"
17.   },
18.   "dependencies": {
19.     "better-sqlite3": "^11.0.0",
20.     "express": "^4.21.0",
21.     "uuid": "^11.1.0"
22.   },
23.   "devDependencies": {
24.     "@types/better-sqlite3": "^7.6.0",
25.     "@types/express": "^5.0.0",
26.     "@types/node": "^22.0.0",
27.     "@types/uuid": "^10.0.0",
28.     "concurrently": "^9.0.0",
29.     "tsx": "^4.19.0",
30.     "typescript": "^5.7.0",
31.     "vite": "^6.0.0",
32.     "vitest": "^3.0.0"
33.   }
34. }
```

</details>


---

<sub>⏱️ 1m 2s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tsconfig.json.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tsconfig.json

<details>
<summary>26 lines</summary>

```
1. {
2.   "compilerOptions": {
3.     "target": "ES2022",
4.     "module": "NodeNext",
5.     "moduleResolution": "NodeNext",
6.     "outDir": "../dist",
7.     "rootDir": "..",
8.     "strict": true,
9.     "esModuleInterop": true,
10.     "skipLibCheck": true,
11.     "forceConsistentCasingInFileNames": true,
12.     "resolveJsonModule": true,
13.     "types": [
14.       "node",
15.       "vitest/globals"
16.     ]
17.   },
18.   "include": [
19.     "src/**/*.ts",
20.     "tests/**/*.ts"
21.   ],
22.   "exclude": [
23.     "../node_modules",
24.     "../backend/dist"
25.   ]
26. }
```

</details>


---

<sub>⏱️ 1m 2s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\unit\business-rules.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\unit\business-rules.test.ts

<details>
<summary>72 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Business Rules Tests
3. // ---------------------------------------------------------------------------
4. 
5. import { describe, it, expect } from "vitest";
6. import {
7.   validateLoanRules,
8.   requiredApprovalRoles,
9.   canApprove,
10. } from "../../src/rules/business-rules.js";
11. import type { LoanApplication } from "../../src/models/types.js";
12. 
13. const baseLoan: LoanApplication = {
14.   id: "test-1",
15.   borrowerName: "Test Corp",
16.   amount: 100000,
17.   loanState: "NY",
18.   status: "intake",
19.   assignedUnderwriter: "u-1",
20.   riskScore: null,
21.   createdAt: new Date().toISOString(),
22.   updatedAt: new Date().toISOString(),
23. };
24. 
25. describe("Business Rules", () => {
26.   it("passes for a valid standard loan", () => {
27.     expect(validateLoanRules(baseLoan)).toEqual([]);
28.   });
29. 
30.   it("rejects zero amount", () => {
31.     const violations = validateLoanRules({ ...baseLoan, amount: 0 });
32.     expect(violations).toHaveLength(1);
33.     expect(violations[0].rule).toBe("positive-amount");
34.   });
35. 
36.   it("rejects California loan below minimum", () => {
37.     const violations = validateLoanRules({
38.       ...baseLoan,
39.       loanState: "CA",
40.       amount: 10000,
41.     });
42.     expect(violations.some((v) => v.rule === "ca-min-amount")).toBe(true);
43.   });
44. 
45.   it("rejects California loan above maximum", () => {
46.     const violations = validateLoanRules({
47.       ...baseLoan,
48.       loanState: "CA",
49.       amount: 6_000_000,
50.     });
51.     expect(violations.some((v) => v.rule === "ca-max-amount")).toBe(true);
52.   });
53. });
54. 
55. describe("Approval Roles", () => {
56.   it("underwriter can approve loans up to $1M", () => {
57.     expect(canApprove("underwriter", 500000)).toBe(true);
58.   });
59. 
60.   it("underwriter cannot approve loans over $1M", () => {
61.     expect(canApprove("underwriter", 1_500_000)).toBe(false);
62.   });
63. 
64.   it("analyst-manager required for loans over $1M", () => {
65.     expect(requiredApprovalRoles(1_500_000)).toContain("analyst-manager");
66.   });
67. 
68.   it("compliance-reviewer required for loans over $2.5M", () => {
69.     expect(requiredApprovalRoles(3_000_000)).toContain("compliance-reviewer");
70.   });
71. });
72.
```

</details>


---

<sub>⏱️ 1m 2s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\unit\state-machine.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\unit\state-machine.test.ts

<details>
<summary>47 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // State Machine Tests
3. // ---------------------------------------------------------------------------
4. 
5. import { describe, it, expect } from "vitest";
6. import {
7.   canTransition,
8.   validNextStates,
9.   assertTransition,
10. } from "../../src/rules/state-machine.js";
11. 
12. describe("State Machine", () => {
13.   it("allows intake → review", () => {
14.     expect(canTransition("intake", "review")).toBe(true);
15.   });
16. 
17.   it("allows review → underwriting", () => {
18.     expect(canTransition("review", "underwriting")).toBe(true);
19.   });
20. 
21.   it("allows review → intake (rework)", () => {
22.     expect(canTransition("review", "intake")).toBe(true);
23.   });
24. 
25.   it("blocks intake → decision (skip)", () => {
26.     expect(canTransition("intake", "decision")).toBe(false);
27.   });
28. 
29.   it("blocks finalized → any state", () => {
30.     expect(canTransition("finalized", "intake")).toBe(false);
31.     expect(canTransition("finalized", "review")).toBe(false);
32.     expect(canTransition("finalized", "underwriting")).toBe(false);
33.     expect(canTransition("finalized", "decision")).toBe(false);
34.   });
35. 
36.   it("returns valid next states", () => {
37.     expect(validNextStates("decision")).toEqual(["finalized", "underwriting"]);
38.     expect(validNextStates("finalized")).toEqual([]);
39.   });
40. 
41.   it("assertTransition throws for invalid transitions", () => {
42.     expect(() => assertTransition("intake", "finalized")).toThrow(
43.       "INVALID_STATE",
44.     );
45.   });
46. });
47.
```

</details>


---

<sub>⏱️ 1m 2s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails**

"src/backend/src/{rules,models,services,routes,queue}/**/*.ts" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails

```
No files matched the pattern.
```


---

<sub>⏱️ 1m 2s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\rules\business-rules.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\rules\business-rules.ts

<details>
<summary>84 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Business Rules
3. // ---------------------------------------------------------------------------
4. // Domain-specific validation rules.  These are checked by services BEFORE
5. // persisting changes.
6. //
7. // CALIFORNIA RULES — REGULATORY REQUIREMENT:
8. //   Loans in California (loan_state = "CA") have additional requirements:
9. //   - Minimum loan amount: $50,000
10. //   - Maximum loan amount: $5,000,000
11. //   - Mandatory 3-day cooling-off period between "review" → "underwriting"
12. //   - Additional disclosure document required before finalization
13. //
14. //   These rules are gated behind the `californiaRules` feature flag.
15. //   When disabled, California loans follow standard rules.
16. //
17. // AMOUNT THRESHOLDS:
18. //   - Loans over $1,000,000 require analyst-manager approval (not just underwriter)
19. //   - Loans over $2,500,000 require compliance-reviewer sign-off
20. // ---------------------------------------------------------------------------
21. 
22. import { featureFlags } from "../config/feature-flags.js";
23. import type { LoanApplication, UserRole } from "../models/types.js";
24. 
25. export interface RuleViolation {
26.   rule: string;
27.   message: string;
28. }
29. 
30. /**
31.  * Validate a loan application against all business rules.
32.  * Returns an empty array if all rules pass.
33.  */
34. export function validateLoanRules(loan: LoanApplication): RuleViolation[] {
35.   const violations: RuleViolation[] = [];
36. 
37.   // Standard rules
38.   if (loan.amount <= 0) {
39.     violations.push({
40.       rule: "positive-amount",
41.       message: "Loan amount must be positive.",
42.     });
43.   }
44. 
45.   // California-specific rules
46.   if (featureFlags.californiaRules && loan.loanState === "CA") {
47.     if (loan.amount < 50_000) {
48.       violations.push({
49.         rule: "ca-min-amount",
50.         message: "California loans must be at least $50,000.",
51.       });
52.     }
53.     if (loan.amount > 5_000_000) {
54.       violations.push({
55.         rule: "ca-max-amount",
56.         message: "California loans cannot exceed $5,000,000.",
57.       });
58.     }
59.   }
60. 
61.   return violations;
62. }
63. 
64. /**
65.  * Determine which roles are required to approve a loan at the given amount.
66.  */
67. export function requiredApprovalRoles(amount: number): UserRole[] {
68.   if (amount > 2_500_000) {
69.     return ["analyst-manager", "compliance-reviewer"];
70.   }
71.   if (amount > 1_000_000) {
72.     return ["analyst-manager"];
73.   }
74.   return ["underwriter"];
75. }
76. 
77. /**
78.  * Check if a role is authorized to approve a loan of the given amount.
79.  */
80. export function canApprove(role: UserRole, amount: number): boolean {
81.   const required = requiredApprovalRoles(amount);
82.   return required.includes(role);
83. }
84.
```

</details>


---

<sub>⏱️ 1m 2s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\models\types.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\models\types.ts

<details>
<summary>112 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Loan Workbench — Domain Types
3. // ---------------------------------------------------------------------------
4. // This file defines the core domain model for the Loan Workbench platform.
5. // Business rules, state machines, authorization logic, queue contracts, and
6. // database schema all depend on these types.  Changes here affect nearly
7. // every module in the project.
8. // ---------------------------------------------------------------------------
9. 
10. /** Lifecycle states for a commercial loan application. */
11. export type ApplicationState =
12.   | "intake"
13.   | "review"
14.   | "underwriting"
15.   | "decision"
16.   | "finalized";
17. 
18. /**
19.  * Valid state transitions.
20.  * Transitions not listed here are forbidden — the system must never allow
21.  * a finalized application to move backward.
22.  */
23. export const VALID_TRANSITIONS: Record<ApplicationState, ApplicationState[]> = {
24.   intake: ["review"],
25.   review: ["underwriting", "intake"], // can return to intake for rework
26.   underwriting: ["decision"],
27.   decision: ["finalized", "underwriting"], // can push back to underwriting
28.   finalized: [], // terminal — no transitions allowed
29. };
30. 
31. /** Organizational roles recognized by the Loan Workbench. */
32. export type UserRole =
33.   | "underwriter"
34.   | "analyst-manager"
35.   | "compliance-reviewer";
36. 
37. /** Notification event types that can trigger user-facing alerts. */
38. export type NotificationEvent =
39.   | "approval"
40.   | "decline"
41.   | "document-request"
42.   | "manual-review-escalation";
43. 
44. /** Delivery channels available for notifications. */
45. export type NotificationChannel = "email" | "sms";
46. 
47. // ---------------------------------------------------------------------------
48. // Entity interfaces
49. // ---------------------------------------------------------------------------
50. 
51. export interface User {
52.   id: string;
53.   role: UserRole;
54.   name: string;
55.   email: string;
56.   phone?: string;
57. }
58. 
59. /**
60.  * Session context attached to every authenticated request.
61.  *
62.  * When `delegatedFor` is present the actor is operating on behalf of another
63.  * user.  Delegated sessions restrict write operations — see auth middleware.
64.  */
65. export interface SessionContext {
66.   actor: User;
67.   delegatedFor?: User;
68. }
69. 
70. export interface LoanApplication {
71.   id: string;
72.   borrowerName: string;
73.   amount: number;
74.   /** US state / jurisdiction — affects business rules (e.g. California). */
75.   loanState: string;
76.   status: ApplicationState;
77.   assignedUnderwriter: string;
78.   riskScore: number | null;
79.   createdAt: string;
80.   updatedAt: string;
81. }
82. 
83. export interface Decision {
84.   id: string;
85.   applicationId: string;
86.   type: "approved" | "declined" | "conditional";
87.   rationale: string;
88.   decidedBy: string;
89.   decidedAt: string;
90.   conditions?: string[];
91. }
92. 
93. export interface NotificationPreference {
94.   userId: string;
95.   event: NotificationEvent;
96.   channel: NotificationChannel;
97.   enabled: boolean;
98.   updatedAt: string;
99.   updatedBy: string;
100. }
101. 
102. export interface AuditEntry {
103.   id: string;
104.   action: string;
105.   actor: string;
106.   delegatedFor: string | null;
107.   timestamp: string;
108.   previousValue: string | null;
109.   newValue: string | null;
110.   source: string;
111. }
112.
```

</details>


---

<sub>⏱️ 1m 58s</sub>

### 💬 Copilot

I’ve got the main pattern now: hook JSONs are tiny, while the Python scripts either read `PreToolUse` JSON from `stdin` or run a standalone validation flow. I’m implementing the new guardrail as a small hook plus a Python validator that understands TypeScript import paths and exempts barrel files themselves.

---

<sub>⏱️ 1m 58s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "barrel|index\\.ts|internal module",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\06-tools-and-guardrails",
  "output_mode": "content",
  "glob": "*.{md,py,json,ts}",
  "-n": true,
  "head_limit": 200
}
```

</details>

<details>
<summary>10 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\util.py:127:    "Then implement a new import-validation guardrail that enforces the project's barrel-file import convention during pre-commit. "
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\util.py:131:    "The validation script must check that TypeScript files import from barrel files (index.ts) rather than reaching into internal module paths. "
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\README.md:33:- the new guardrail must enforce barrel-file import conventions for TypeScript files
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\README.md:56:copilot -p "Inspect the lesson's guardrail-related instructions, hook configs, scripts, MCP config, and policy docs before answering. Discover the relevant files rather than assuming a fixed list. Then implement a new import-validation guardrail that enforces the project's barrel-file import convention during pre-commit. Create the hook config in .github/hooks/import-validation.json following the pattern of the existing hook configs. Create the validation script in .github/scripts/validate_imports.py following the pattern of the existing guardrail scripts. The hook must use PreToolUse event type and invoke the Python validation script. The validation script must check that TypeScript files import from barrel files (index.ts) rather than reaching into internal module paths. Apply the changes directly in files. Do not run shell commands and do not use SQL." --allow-all-tools --deny-tool=powershell --deny-tool=sql
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\README.md:63:- the validation script enforces barrel-file imports
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\docs\guardrail-audit-example.md:14:2. `.github/scripts/validate_imports.py` — validation script enforcing barrel-file import convention
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\docs\guardrail-audit-example.md:26:2. The validation script must check that TypeScript files import from barrel files (index.ts) rather than reaching into internal module paths.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\ASSESSMENT.md:12:Inspect the lesson's guardrail-related instructions, hook configs, scripts, MCP config, and policy docs before answering. Discover the relevant files rather than assuming a fixed list. Then implement a new import-validation guardrail that enforces the project's barrel-file import convention during pre-commit. Create the hook config in .github/hooks/import-validation.json following the pattern of the existing hook configs. Create the validation script in .github/scripts/validate_imports.py following the pattern of the existing guardrail scripts. The hook must use PreToolUse event type and invoke the Python validation script. The validation script must check that TypeScript files import from barrel files (index.ts) rather than reaching into internal module paths. Apply the changes directly in files. Do not run shell commands and do not use SQL.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\ASSESSMENT.md:28:- `.output/change/expected-patterns.json` — required patterns in patch: PreToolUse, validate_imports.py, import, barrel/index.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\ASSESSMENT.md:41:| Script enforces barrel-file (index.ts) convention | `expected-patterns.json` |
```

</details>


---

<sub>⏱️ 1m 58s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\app.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\app.ts (lines 1-120)

<details>
<summary>81 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Loan Workbench — Application Entry Point
3. // ---------------------------------------------------------------------------
4. // Express server with middleware chain, route mounting, database init,
5. // and message queue handler registration.
6. //
7. // MIDDLEWARE ORDER (matters!):
8. //   1. express.json()          — Parse JSON bodies
9. //   2. rateLimiterMiddleware   — Rate limit before auth (prevent brute force)
10. //   3. authMiddleware          — Authenticate & attach session context
11. //   4. auditLoggerMiddleware   — Log mutating requests (needs session)
12. //   5. Routes                  — Business logic
13. //   6. errorHandler            — Catch-all error handler (MUST be last)
14. // ---------------------------------------------------------------------------
15. 
16. import express from "express";
17. import path from "path";
18. import { fileURLToPath } from "url";
19. import { config } from "./config/env.js";
20. import { getDb } from "./db/connection.js";
21. import { seedDatabase } from "./db/seed.js";
22. import { authMiddleware } from "./middleware/auth.js";
23. import { auditLoggerMiddleware } from "./middleware/audit-logger.js";
24. import { rateLimiterMiddleware } from "./middleware/rate-limiter.js";
25. import { errorHandler } from "./middleware/error-handler.js";
26. import { applicationRoutes } from "./routes/applications.js";
27. import { decisionRoutes } from "./routes/decisions.js";
28. import { notificationRoutes } from "./routes/notifications.js";
29. import { auditRoutes } from "./routes/audit.js";
30. import { queueStatusRoutes } from "./routes/queue-status.js";
31. import { registerNotificationHandler } from "./queue/handlers/notification-handler.js";
32. import { registerAuditHandler } from "./queue/handlers/audit-handler.js";
33. 
34. const __dirname = path.dirname(fileURLToPath(import.meta.url));
35. 
36. const app = express();
37. 
38. // ── Initialize database ──
39. getDb();
40. seedDatabase();
41. 
42. // ── Register queue handlers ──
43. registerNotificationHandler();
44. registerAuditHandler();
45. 
46. // ── Middleware chain (ORDER MATTERS) ──
47. app.use(express.json());
48. app.use(rateLimiterMiddleware);
49. app.use(authMiddleware);
50. app.use(auditLoggerMiddleware);
51. 
52. // ── API Routes ──
53. app.use("/api/applications", applicationRoutes);
54. app.use("/api/decisions", decisionRoutes);
55. app.use("/api/notifications", notificationRoutes);
56. app.use("/api/audit", auditRoutes);
57. app.use("/api/queue", queueStatusRoutes);
58. 
59. // ── Health check (no auth required — placed before auth middleware in request flow) ──
60. app.get("/health", (_req, res) => {
61.   res.json({ status: "ok", timestamp: new Date().toISOString() });
62. });
63. 
64. // ── Serve frontend static files ──
65. const frontendDir = path.resolve(__dirname, "../../frontend");
66. app.use(express.static(frontendDir));
67. 
68. // ── SPA fallback — serve index.html for non-API routes ──
69. app.get("*", (_req, res) => {
70.   res.sendFile(path.join(frontendDir, "index.html"));
71. });
72. 
73. // ── Error handler (MUST be last) ──
74. app.use(errorHandler);
75. 
76. app.listen(config.port, () => {
77.   console.log(`Loan Workbench API listening on port ${config.port}`);
78.   console.log(`Database: ${config.dbPath}`);
79. });
80. 
81. export default app;
```

</details>


---

<sub>⏱️ 1m 58s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\frontend\vite.config.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\frontend\vite.config.ts (lines 1-80)

<details>
<summary>10 lines</summary>

```
1. import { defineConfig } from "vite";
2. 
3. export default defineConfig({
4.   server: {
5.     proxy: {
6.       "/api": "http://localhost:3100",
7.       "/health": "http://localhost:3100",
8.     },
9.   },
10. });
```

</details>


---

<sub>⏱️ 2m 46s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Add File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\06-tools-and-guardrails\\.github\\hooks\\import-validation.json\n+{\n+  \"hooks\": {\n+    \"PreToolUse\": [\n+      {\n+        \"type\": \"command\",\n+        \"command\": \"python .github/scripts/validate_imports.py\",\n+        \"timeout\": 20\n+      }\n+    ]\n+  }\n+}\n*** Add File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\06-tools-and-guardrails\\.github\\scripts\\validate_imports.py\n+#!/usr/bin/env python3\n+\"\"\"PreToolUse hook: enforce barrel-file imports for TypeScript modules.\n+\n+This validator blocks imports that reach through another module's internal file\n+path when the import should go through that module's `index.ts` barrel instead.\n+Barrel files themselves are exempt because they aggregate those internal files.\n+\"\"\"\n+import json\n+import re\n+import sys\n+from pathlib import Path, PurePosixPath\n+\n+PROJECT_ROOT = Path(__file__).resolve().parents[2]\n+SOURCE_ROOT = PROJECT_ROOT / \"src\"\n+TS_EXTENSIONS = {\".ts\", \".tsx\", \".mts\", \".cts\"}\n+JS_TO_TS_EXTENSIONS = {\n+    \".js\": [\".ts\", \".tsx\"],\n+    \".jsx\": [\".tsx\", \".ts\"],\n+    \".mjs\": [\".mts\", \".ts\"],\n+    \".cjs\": [\".cts\", \".ts\"],\n+}\n+EDIT_TOOLS = {\"editFiles\", \"createFile\"}\n+IMPORT_RE = re.compile(\n+    r\"\"\"\n+    ^\\s*\n+    (?:\n+      import\n+      (?:\n+        \\s+(?:type\\s+)?[\\s\\S]*?\\s+from\n+      )?\n+      |\n+      export\n+      \\s+(?:type\\s+)?\n+      [\\s\\S]*?\\s+from\n+    )\n+    \\s*[\"'](?P<specifier>[^\"']+)[\"']\n+    \"\"\",\n+    re.MULTILINE | re.VERBOSE,\n+)\n+\n+\n+def is_typescript_file(path: Path) -> bool:\n+    return path.suffix in TS_EXTENSIONS\n+\n+\n+def is_barrel_file(path: Path) -> bool:\n+    return path.name.startswith(\"index.\") and is_typescript_file(path)\n+\n+\n+def normalize_path(raw_path: str) -> Path:\n+    path = Path(raw_path)\n+    if path.is_absolute():\n+        return path\n+    posix_path = PurePosixPath(raw_path.replace(\"\\\\\", \"/\"))\n+    return PROJECT_ROOT.joinpath(*posix_path.parts)\n+\n+\n+def relative_path(path: Path) -> str:\n+    try:\n+        return path.relative_to(PROJECT_ROOT).as_posix()\n+    except ValueError:\n+        return path.as_posix()\n+\n+\n+def strip_relative_segments(specifier: str) -> list[str]:\n+    parts = PurePosixPath(specifier).parts\n+    return [part for part in parts if part not in (\".\", \"..\")]\n+\n+\n+def resolve_base_target(source_path: Path, specifier: str) -> Path:\n+    specifier_path = PurePosixPath(specifier)\n+    return source_path.parent.joinpath(*specifier_path.parts).resolve(strict=False)\n+\n+\n+def has_barrel_file(directory: Path) -> bool:\n+    return any((directory / f\"index{extension}\").exists() for extension in TS_EXTENSIONS)\n+\n+\n+def is_barrel_import(source_path: Path, specifier: str) -> bool:\n+    base_target = resolve_base_target(source_path, specifier)\n+\n+    if base_target.is_dir():\n+        return has_barrel_file(base_target)\n+\n+    if base_target.exists() and base_target.stem == \"index\":\n+        return True\n+\n+    if base_target.suffix in JS_TO_TS_EXTENSIONS:\n+        for extension in JS_TO_TS_EXTENSIONS[base_target.suffix]:\n+            if base_target.with_suffix(extension).exists() and base_target.stem == \"index\":\n+                return True\n+\n+    if not base_target.suffix and has_barrel_file(base_target):\n+        return True\n+\n+    return False\n+\n+\n+def is_deep_relative_import(source_path: Path, specifier: str) -> bool:\n+    if not specifier.startswith(\".\"):\n+        return False\n+\n+    if is_barrel_import(source_path, specifier):\n+        return False\n+\n+    path_parts = strip_relative_segments(specifier)\n+    if len(path_parts) <= 1:\n+        return False\n+\n+    if PurePosixPath(path_parts[-1]).stem == \"index\":\n+        return False\n+\n+    return True\n+\n+\n+def suggested_barrel(specifier: str) -> str:\n+    path = PurePosixPath(specifier)\n+    parent = path.parent\n+    if str(parent) == \".\":\n+        return \"./index.ts\"\n+    return f\"{parent.as_posix()}/index.ts\"\n+\n+\n+def collect_violations(source_path: Path, content: str) -> list[str]:\n+    if is_barrel_file(source_path):\n+        return []\n+\n+    violations: list[str] = []\n+    for match in IMPORT_RE.finditer(content):\n+        specifier = match.group(\"specifier\")\n+        if is_deep_relative_import(source_path, specifier):\n+            violations.append(\n+                f\"{relative_path(source_path)} imports '{specifier}'. \"\n+                f\"Use the barrel file '{suggested_barrel(specifier)}' \"\n+                \"instead of an internal module path.\"\n+            )\n+    return violations\n+\n+\n+def collect_repository_violations() -> list[str]:\n+    violations: list[str] = []\n+    if not SOURCE_ROOT.exists():\n+        return violations\n+\n+    for path in sorted(SOURCE_ROOT.rglob(\"*\")):\n+        if not path.is_file() or not is_typescript_file(path):\n+            continue\n+        if any(part in {\"node_modules\", \"dist\"} for part in path.parts):\n+            continue\n+        violations.extend(collect_violations(path, path.read_text(encoding=\"utf-8\")))\n+    return violations\n+\n+\n+def read_hook_payload() -> dict | None:\n+    if sys.stdin.isatty():\n+        return None\n+\n+    raw = sys.stdin.read().strip()\n+    if not raw:\n+        return None\n+\n+    try:\n+        return json.loads(raw)\n+    except json.JSONDecodeError:\n+        return None\n+\n+\n+def collect_hook_violations(payload: dict) -> list[str]:\n+    tool_name = payload.get(\"tool_name\", \"\")\n+    tool_input = payload.get(\"tool_input\", {})\n+\n+    if tool_name not in EDIT_TOOLS:\n+        return []\n+\n+    file_path = tool_input.get(\"filePath\")\n+    files = tool_input.get(\"files\", [])\n+    paths_to_check = files if files else ([file_path] if file_path else [])\n+\n+    content = (\n+        tool_input.get(\"content\")\n+        or tool_input.get(\"newContent\")\n+        or tool_input.get(\"newString\")\n+        or \"\"\n+    )\n+\n+    violations: list[str] = []\n+    for raw_path in paths_to_check:\n+        path = normalize_path(raw_path)\n+        if not is_typescript_file(path):\n+            continue\n+\n+        if content:\n+            violations.extend(collect_violations(path, content))\n+            continue\n+\n+        if path.exists():\n+            violations.extend(collect_violations(path, path.read_text(encoding=\"utf-8\")))\n+\n+    return violations\n+\n+\n+def emit_deny(violations: list[str]) -> None:\n+    result = {\n+        \"hookSpecificOutput\": {\n+            \"hookEventName\": \"PreToolUse\",\n+            \"permissionDecision\": \"deny\",\n+            \"permissionDecisionReason\": (\n+                \"Import validation failed. \"\n+                + \" \".join(violations[:3])\n+            ),\n+        }\n+    }\n+    json.dump(result, sys.stdout)\n+\n+\n+def main() -> None:\n+    payload = read_hook_payload()\n+    if payload is not None:\n+        violations = collect_hook_violations(payload)\n+        if violations:\n+            emit_deny(violations)\n+        return\n+\n+    print(\"=== Import validation ===\")\n+    violations = collect_repository_violations()\n+    if violations:\n+        print(\"FAIL: TypeScript imports must use barrel files (index.ts).\")\n+        for violation in violations[:20]:\n+            print(f\"  - {violation}\")\n+        sys.exit(1)\n+\n+    print(\"OK\")\n+\n+\n+if __name__ == \"__main__\":\n+    main()\n*** End Patch\n"
```

</details>

```
Added 2 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\hooks\import-validation.json, Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\validate_imports.py
```


---

<sub>⏱️ 2m 59s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Update File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\06-tools-and-guardrails\\.github\\scripts\\validate_imports.py\n@@\n EDIT_TOOLS = {\"editFiles\", \"createFile\"}\n@@\n def read_hook_payload() -> dict | None:\n@@\n     except json.JSONDecodeError:\n         return None\n \n \n+def is_commit_operation(payload: dict) -> bool:\n+    tool_name = payload.get(\"tool_name\", \"\")\n+    tool_input = payload.get(\"tool_input\", {})\n+\n+    if tool_name in {\"runTerminalCommand\", \"powershell\", \"bash\"}:\n+        command = \" \".join(\n+            str(part)\n+            for part in (\n+                tool_input.get(\"command\"),\n+                tool_input.get(\"input\"),\n+                tool_input.get(\"args\"),\n+            )\n+            if part\n+        )\n+        return \"git commit\" in command\n+\n+    return False\n+\n+\n def collect_hook_violations(payload: dict) -> list[str]:\n     tool_name = payload.get(\"tool_name\", \"\")\n     tool_input = payload.get(\"tool_input\", {})\n \n+    if is_commit_operation(payload):\n+        return collect_repository_violations()\n+\n     if tool_name not in EDIT_TOOLS:\n         return []\n*** End Patch\n"
```

</details>

```
Modified 1 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\validate_imports.py
```


---

<sub>⏱️ 3m 4s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\hooks\import-validation.json.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\hooks\import-validation.json

<details>
<summary>12 lines</summary>

```
1. {
2.   "hooks": {
3.     "PreToolUse": [
4.       {
5.         "type": "command",
6.         "command": "python .github/scripts/validate_imports.py",
7.         "timeout": 20
8.       }
9.     ]
10.   }
11. }
12.
```

</details>


---

<sub>⏱️ 3m 4s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\validate_imports.py.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\validate_imports.py

<details>
<summary>259 lines</summary>

```
1. #!/usr/bin/env python3
2. """PreToolUse hook: enforce barrel-file imports for TypeScript modules.
3. 
4. This validator blocks imports that reach through another module's internal file
5. path when the import should go through that module's `index.ts` barrel instead.
6. Barrel files themselves are exempt because they aggregate those internal files.
7. """
8. import json
9. import re
10. import sys
11. from pathlib import Path, PurePosixPath
12. 
13. PROJECT_ROOT = Path(__file__).resolve().parents[2]
14. SOURCE_ROOT = PROJECT_ROOT / "src"
15. TS_EXTENSIONS = {".ts", ".tsx", ".mts", ".cts"}
16. JS_TO_TS_EXTENSIONS = {
17.     ".js": [".ts", ".tsx"],
18.     ".jsx": [".tsx", ".ts"],
19.     ".mjs": [".mts", ".ts"],
20.     ".cjs": [".cts", ".ts"],
21. }
22. EDIT_TOOLS = {"editFiles", "createFile"}
23. IMPORT_RE = re.compile(
24.     r"""
25.     ^\s*
26.     (?:
27.       import
28.       (?:
29.         \s+(?:type\s+)?[\s\S]*?\s+from
30.       )?
31.       |
32.       export
33.       \s+(?:type\s+)?
34.       [\s\S]*?\s+from
35.     )
36.     \s*["'](?P<specifier>[^"']+)["']
37.     """,
38.     re.MULTILINE | re.VERBOSE,
39. )
40. 
41. 
42. def is_typescript_file(path: Path) -> bool:
43.     return path.suffix in TS_EXTENSIONS
44. 
45. 
46. def is_barrel_file(path: Path) -> bool:
47.     return path.name.startswith("index.") and is_typescript_file(path)
48. 
49. 
50. def normalize_path(raw_path: str) -> Path:
51.     path = Path(raw_path)
52.     if path.is_absolute():
53.         return path
54.     posix_path = PurePosixPath(raw_path.replace("\\", "/"))
55.     return PROJECT_ROOT.joinpath(*posix_path.parts)
56. 
57. 
58. def relative_path(path: Path) -> str:
59.     try:
60.         return path.relative_to(PROJECT_ROOT).as_posix()
61.     except ValueError:
62.         return path.as_posix()
63. 
64. 
65. def strip_relative_segments(specifier: str) -> list[str]:
66.     parts = PurePosixPath(specifier).parts
67.     return [part for part in parts if part not in (".", "..")]
68. 
69. 
70. def resolve_base_target(source_path: Path, specifier: str) -> Path:
71.     specifier_path = PurePosixPath(specifier)
72.     return source_path.parent.joinpath(*specifier_path.parts).resolve(strict=False)
73. 
74. 
75. def has_barrel_file(directory: Path) -> bool:
76.     return any((directory / f"index{extension}").exists() for extension in TS_EXTENSIONS)
77. 
78. 
79. def is_barrel_import(source_path: Path, specifier: str) -> bool:
80.     base_target = resolve_base_target(source_path, specifier)
81. 
82.     if base_target.is_dir():
83.         return has_barrel_file(base_target)
84. 
85.     if base_target.exists() and base_target.stem == "index":
86.         return True
87. 
88.     if base_target.suffix in JS_TO_TS_EXTENSIONS:
89.         for extension in JS_TO_TS_EXTENSIONS[base_target.suffix]:
90.             if base_target.with_suffix(extension).exists() and base_target.stem == "index":
91.                 return True
92. 
93.     if not base_target.suffix and has_barrel_file(base_target):
94.         return True
95. 
96.     return False
97. 
98. 
99. def is_deep_relative_import(source_path: Path, specifier: str) -> bool:
100.     if not specifier.startswith("."):
101.         return False
102. 
103.     if is_barrel_import(source_path, specifier):
104.         return False
105. 
106.     path_parts = strip_relative_segments(specifier)
107.     if len(path_parts) <= 1:
108.         return False
109. 
110.     if PurePosixPath(path_parts[-1]).stem == "index":
111.         return False
112. 
113.     return True
114. 
115. 
116. def suggested_barrel(specifier: str) -> str:
117.     path = PurePosixPath(specifier)
118.     parent = path.parent
119.     if str(parent) == ".":
120.         return "./index.ts"
121.     return f"{parent.as_posix()}/index.ts"
122. 
123. 
124. def collect_violations(source_path: Path, content: str) -> list[str]:
125.     if is_barrel_file(source_path):
126.         return []
127. 
128.     violations: list[str] = []
129.     for match in IMPORT_RE.finditer(content):
130.         specifier = match.group("specifier")
131.         if is_deep_relative_import(source_path, specifier):
132.             violations.append(
133.                 f"{relative_path(source_path)} imports '{specifier}'. "
134.                 f"Use the barrel file '{suggested_barrel(specifier)}' "
135.                 "instead of an internal module path."
136.             )
137.     return violations
138. 
139. 
140. def collect_repository_violations() -> list[str]:
141.     violations: list[str] = []
142.     if not SOURCE_ROOT.exists():
143.         return violations
144. 
145.     for path in sorted(SOURCE_ROOT.rglob("*")):
146.         if not path.is_file() or not is_typescript_file(path):
147.             continue
148.         if any(part in {"node_modules", "dist"} for part in path.parts):
149.             continue
150.         violations.extend(collect_violations(path, path.read_text(encoding="utf-8")))
151.     return violations
152. 
153. 
154. def read_hook_payload() -> dict | None:
155.     if sys.stdin.isatty():
156.         return None
157. 
158.     raw = sys.stdin.read().strip()
159.     if not raw:
160.         return None
161. 
162.     try:
163.         return json.loads(raw)
164.     except json.JSONDecodeError:
165.         return None
166. 
167. 
168. def is_commit_operation(payload: dict) -> bool:
169.     tool_name = payload.get("tool_name", "")
170.     tool_input = payload.get("tool_input", {})
171. 
172.     if tool_name in {"runTerminalCommand", "powershell", "bash"}:
173.         command = " ".join(
174.             str(part)
175.             for part in (
176.                 tool_input.get("command"),
177.                 tool_input.get("input"),
178.                 tool_input.get("args"),
179.             )
180.             if part
181.         )
182.         return "git commit" in command
183. 
184.     return False
185. 
186. 
187. def collect_hook_violations(payload: dict) -> list[str]:
188.     tool_name = payload.get("tool_name", "")
189.     tool_input = payload.get("tool_input", {})
190. 
191.     if is_commit_operation(payload):
192.         return collect_repository_violations()
193. 
194.     if tool_name not in EDIT_TOOLS:
195.         return []
196. 
197.     file_path = tool_input.get("filePath")
198.     files = tool_input.get("files", [])
199.     paths_to_check = files if files else ([file_path] if file_path else [])
200. 
201.     content = (
202.         tool_input.get("content")
203.         or tool_input.get("newContent")
204.         or tool_input.get("newString")
205.         or ""
206.     )
207. 
208.     violations: list[str] = []
209.     for raw_path in paths_to_check:
210.         path = normalize_path(raw_path)
211.         if not is_typescript_file(path):
212.             continue
213. 
214.         if content:
215.             violations.extend(collect_violations(path, content))
216.             continue
217. 
218.         if path.exists():
219.             violations.extend(collect_violations(path, path.read_text(encoding="utf-8")))
220. 
221.     return violations
222. 
223. 
224. def emit_deny(violations: list[str]) -> None:
225.     result = {
226.         "hookSpecificOutput": {
227.             "hookEventName": "PreToolUse",
228.             "permissionDecision": "deny",
229.             "permissionDecisionReason": (
230.                 "Import validation failed. "
231.                 + " ".join(violations[:3])
232.             ),
233.         }
234.     }
235.     json.dump(result, sys.stdout)
236. 
237. 
238. def main() -> None:
239.     payload = read_hook_payload()
240.     if payload is not None:
241.         violations = collect_hook_violations(payload)
242.         if violations:
243.             emit_deny(violations)
244.         return
245. 
246.     print("=== Import validation ===")
247.     violations = collect_repository_violations()
248.     if violations:
249.         print("FAIL: TypeScript imports must use barrel files (index.ts).")
250.         for violation in violations[:20]:
251.             print(f"  - {violation}")
252.         sys.exit(1)
253. 
254.     print("OK")
255. 
256. 
257. if __name__ == "__main__":
258.     main()
259.
```

</details>


---

<sub>⏱️ 3m 13s</sub>

### 💬 Copilot

Implemented the new guardrail in the requested surfaces:

- Added `.github/hooks/import-validation.json` with a `PreToolUse` command hook that runs `python .github/scripts/validate_imports.py`.
- Added `.github/scripts/validate_imports.py` following the existing script patterns.

The validator:
- reads `PreToolUse` payloads like the file-protection guardrail,
- checks TypeScript imports for deep relative/internal module paths,
- allows barrel imports via `index.ts`,
- skips barrel files themselves,
- can also scan the repo when triggered for commit-like operations or standalone.

I inspected the lesson instructions, hook configs, scripts, MCP config, and policy docs first. No shell commands or SQL were used.

---

<sub>Generated by [GitHub Copilot CLI](https://github.com/features/copilot/cli)</sub>
