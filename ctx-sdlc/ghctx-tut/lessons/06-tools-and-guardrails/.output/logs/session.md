# 🤖 Copilot CLI Session

> [!NOTE]
> - **Session ID:** `ca2dc2b2-3dc8-45bf-abad-3e17ac710e34`  
> - **Started:** 14/03/2026, 19:33:56  
> - **Duration:** 3m 21s  
> - **Exported:** 14/03/2026, 19:37:17  

---

<sub>⏱️ 5s</sub>

### 👤 User

Inspect the lesson's guardrail-related instructions, hook configs, scripts, MCP config, and policy docs before answering. Discover the relevant files rather than assuming a fixed list. Then implement a new import-validation guardrail that enforces the project's barrel-file import convention during pre-commit. Create the hook config in .github/hooks/import-validation.json following the pattern of the existing hook configs. Create the validation script in .github/scripts/validate_imports.py following the pattern of the existing guardrail scripts. The hook must use PreToolUse event type and invoke the Python validation script. The validation script must be a complete Python file, not a placeholder, and the run is only complete when both files exist. The validation script must read hook JSON from stdin when present, inspect changed .ts/.tsx files, and deny imports that bypass a sibling index.ts barrel and reach into internal module paths. Apply the changes directly in files. Do not run shell commands and do not use SQL.

---

<sub>⏱️ 17s</sub>

### ✅ `glob`

**.github\**\*.json**

".github\**\*.json"

```
No files matched the pattern.
```


---

<sub>⏱️ 17s</sub>

### ✅ `glob`

**.github\**\*.py**

".github\**\*.py"

```
No files matched the pattern.
```


---

<sub>⏱️ 17s</sub>

### ✅ `glob`

**docs\**\*.md**

"docs\**\*.md"

```
No files matched the pattern.
```


---

<sub>⏱️ 17s</sub>

### ✅ `rg`

**.**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "guardrail|hook|MCP|policy|security|trust|import-validation|barrel|index\\.ts",
  "path": ".",
  "output_mode": "content",
  "glob": "*.{md,json,py,ts,tsx}",
  "-n": true,
  "head_limit": 200
}
```

</details>

<details>
<summary>103 lines</summary>

```
.\util.py:8:  python util.py --demo     Run a Copilot CLI guardrail-audit demo and capture artifacts
.\util.py:32:GENERATED_HOOK_PATH = LESSON / ".github" / "hooks" / "import-validation.json"
.\util.py:137:    "Inspect the lesson's guardrail-related instructions, hook configs, scripts, MCP config, and policy docs before answering. "
.\util.py:139:    "Then implement a new import-validation guardrail that enforces the project's barrel-file import convention during pre-commit. "
.\util.py:140:    "Create the hook config in .github/hooks/import-validation.json following the pattern of the existing hook configs. "
.\util.py:141:    "Create the validation script in .github/scripts/validate_imports.py following the pattern of the existing guardrail scripts. "
.\util.py:142:    "The hook must use PreToolUse event type and invoke the Python validation script. "
.\util.py:144:    "The validation script must read hook JSON from stdin when present, inspect changed .ts/.tsx files, and deny imports that bypass a sibling index.ts barrel and reach into internal module paths. "
.\util.py:423:        "Run a Copilot CLI guardrail-audit demo and capture logs plus a git-style diff",
.\README.md:4:> **Topic:** Hooks, MCP configuration, and runtime scripts that guard against unsafe operations.
.\README.md:15:Hooks intercept Copilot tool calls at runtime to enforce guardrails.
.\README.md:23:This lesson also includes MCP configuration for extending tool capabilities.
.\README.md:27:This lesson should demonstrate guardrail implementation, not just analysis.
.\README.md:31:- inspect the hook, MCP, and policy files to discover existing guardrail patterns
.\README.md:32:- create a new import-validation guardrail (hook config + validation script) that follows those patterns
.\README.md:33:- the new guardrail must enforce barrel-file import conventions for TypeScript files
.\README.md:40:| `.github/hooks/file-protection.json`       | PreToolUse hook                                           |
.\README.md:41:| `.github/hooks/post-save-format.json`      | PostToolUse hook                                          |
.\README.md:42:| `.github/hooks/pre-commit-validate.json`   | PreToolUse hook                                           |
.\README.md:46:| `.github/mcp.json`                         | MCP server configuration                                  |
.\README.md:47:| `docs/security-policy.md`                  | Security policy                                           |
.\README.md:48:| `docs/tool-trust-boundaries.md`            | Tool trust boundaries                                     |
.\README.md:49:| `docs/guardrail-audit-example.md`          | Concrete lesson-06 demo target and assessment constraints |
.\README.md:53:Create a new guardrail:
.\README.md:56:copilot -p "Inspect the lesson's guardrail-related instructions, hook configs, scripts, MCP config, and policy docs before answering. Discover the relevant files rather than assuming a fixed list. Then implement a new import-validation guardrail that enforces the project's barrel-file import convention during pre-commit. Create the hook config in .github/hooks/import-validation.json following the pattern of the existing hook configs. Create the validation script in .github/scripts/validate_imports.py following the pattern of the existing guardrail scripts. The hook must use PreToolUse event type and invoke the Python validation script. The validation script must check that TypeScript files import from barrel files (index.ts) rather than reaching into internal module paths. Apply the changes directly in files. Do not run shell commands and do not use SQL." --allow-all-tools --deny-tool=powershell --deny-tool=sql
.\README.md:61:- the CLI creates `.github/hooks/import-validation.json` and `.github/scripts/validate_imports.py`
.\README.md:62:- the hook config uses `PreToolUse` event type following existing patterns
.\README.md:63:- the validation script enforces barrel-file imports
.\README.md:69:Ask Copilot to perform edits that should trigger hooks.
.\README.md:75:- inspect the GitHub Copilot output logs to confirm hook execution
.\README.md:77:Expected result: you can see the operational difference between static instructions and runtime guardrails.
.\docs\tool-trust-boundaries.md:3:This document defines the trust model for external tool access in the Loan
.\docs\tool-trust-boundaries.md:4:Workbench project. Every MCP server and external integration must be classified
.\docs\tool-trust-boundaries.md:11:| 1     | **Read-only internal** | Can read project files and data. No mutations.    | Filesystem MCP (scoped to `src/backend/src/`, `src/backend/tests/`, `docs/`) |
.\docs\tool-trust-boundaries.md:12:| 2     | **Read-only external** | Can query external systems. No mutations.         | SQLite MCP (read-only connection to `data/loan-workbench.db`)                |
.\docs\tool-trust-boundaries.md:13:| 3     | **Write internal**     | Can modify project files within scope.            | Filesystem MCP with write access (rarely justified)                          |
.\docs\tool-trust-boundaries.md:14:| 4     | **Write external**     | Can mutate external systems.                      | API MCP with POST/PUT/DELETE access                                          |
.\docs\tool-trust-boundaries.md:15:| 5     | **Privileged**         | Can execute arbitrary commands or access secrets. | Shell MCP, deployment tools                                                  |
.\docs\tool-trust-boundaries.md:17:## Current MCP Server Inventory
.\docs\tool-trust-boundaries.md:32:## Adding a New MCP Server
.\docs\tool-trust-boundaries.md:36:1. **Classify**: Assign a trust level from the table above.
.\docs\tool-trust-boundaries.md:40:5. **Review**: Have the security policy owner approve the addition.
.\docs\tool-trust-boundaries.md:53:2. **Scope narrowly**: MCP filesystem access should list specific directories,
.\docs\tool-trust-boundaries.md:55:3. **No secret exposure**: MCP servers must not have access to `.env` files,
.\docs\tool-trust-boundaries.md:57:4. **Defense in depth**: MCP scoping + hook enforcement + instruction guidance.
.\docs\tool-trust-boundaries.md:59:5. **Audit trail**: Write-capable MCP servers should have their operations
.\docs\guardrail-audit-example.md:7:Show that the CLI can discover existing guardrail patterns and create a new import-validation guardrail that follows the same conventions — producing assessable file changes.
.\docs\guardrail-audit-example.md:13:1. `.github/hooks/import-validation.json` — PreToolUse hook config matching existing hook patterns
.\docs\guardrail-audit-example.md:14:2. `.github/scripts/validate_imports.py` — validation script enforcing barrel-file import convention
.\docs\guardrail-audit-example.md:25:1. The hook config must use `PreToolUse` event type following existing hook file patterns.
.\docs\guardrail-audit-example.md:26:2. The validation script must check that TypeScript files import from barrel files (index.ts) rather than reaching into internal module paths.
.\docs\guardrail-audit-example.md:27:3. The implementation must follow the discovered conventions from existing hook configs and scripts.
.\docs\guardrail-audit-example.md:28:4. The change must stay scoped to `.github/hooks/` and `.github/scripts/`.
.\docs\guardrail-audit-example.md:34:Use the lesson's existing hook configs (file-protection, pre-commit-validate, post-save-format) and their scripts as pattern references to create a new import-validation guardrail.
.\docs\guardrail-audit-example.md:36:Good output should produce a hook + script pair that is consistent with the existing guardrail style.
.\docs\guardrail-audit-example.md:42:- create a hook JSON config with `PreToolUse` event type and a reference to `validate_imports.py`
.\docs\guardrail-audit-example.md:44:- follow the same structure and conventions as the existing hook + script pairs
.\docs\guardrail-audit-example.md:45:- keep the change scoped to the `.github/` guardrail surface
.\docs\security-policy.md:3:This document defines the security controls enforced by hooks and instructions.
.\docs\security-policy.md:8:The following files are protected by the file-protection hook and cannot be
.\docs\security-policy.md:27:database schema without a migration. The file-protection hook prevents this.
.\docs\security-policy.md:71:security model.
.\docs\security-policy.md:89:If a security control is bypassed:
.\docs\security-policy.md:92:2. Verify hook configurations have not been modified.
.\docs\security-policy.md:93:3. Review MCP server access logs (if write-capable servers are configured).
.\docs\security-policy.md:94:4. Document the incident and update this policy if needed.
.\ASSESSMENT.md:12:Inspect the lesson's guardrail-related instructions, hook configs, scripts, MCP config, and policy docs before answering. Discover the relevant files rather than assuming a fixed list. Then implement a new import-validation guardrail that enforces the project's barrel-file import convention during pre-commit. Create the hook config in .github/hooks/import-validation.json following the pattern of the existing hook configs. Create the validation script in .github/scripts/validate_imports.py following the pattern of the existing guardrail scripts. The hook must use PreToolUse event type and invoke the Python validation script. The validation script must check that TypeScript files import from barrel files (index.ts) rather than reaching into internal module paths. Apply the changes directly in files. Do not run shell commands and do not use SQL.
.\ASSESSMENT.md:21:> Did the produced code changes implement the prompt in a way that follows the repository's standards, constraints, and discovered guardrail patterns?
.\ASSESSMENT.md:27:- `.output/change/expected-files.json` — expected files: `.github/hooks/import-validation.json` (added), `.github/scripts/validate_imports.py` (added)
.\ASSESSMENT.md:28:- `.output/change/expected-patterns.json` — required patterns in patch: PreToolUse, validate_imports.py, import, barrel/index.ts
.\ASSESSMENT.md:44:- added `.github/hooks/import-validation.json`
.\ASSESSMENT.md:46:The generated hook file used the correct `PreToolUse` event type and referenced `python .github/scripts/validate_imports.py`, but the run did **not** create the expected `.github/scripts/validate_imports.py` file.
.\ASSESSMENT.md:55:- expected added files: `.github/hooks/import-validation.json`, `.github/scripts/validate_imports.py`
.\ASSESSMENT.md:56:- actual added files: `.github/hooks/import-validation.json`
.\ASSESSMENT.md:57:- missing expected pattern: barrel-file or `index.ts` import convention
.\ASSESSMENT.md:69:- The rerun discovered the right hook surface and created a correctly-shaped hook config.
.\ASSESSMENT.md:71:- The most important repository-specific rule, the barrel-file import convention, was not actually implemented.
.\ASSESSMENT.md:77:> The run should not be considered fully successful. It produced a plausible hook config, but it failed to create the companion validation script and did not demonstrate the required barrel-file import enforcement logic.
.\.github\copilot-instructions.md:6:for loan application workflow management. This workspace uses MCP servers and
.\.github\copilot-instructions.md:7:hooks for capability expansion and enforcement.
.\.github\copilot-instructions.md:11:### MCP Servers
.\.github\copilot-instructions.md:13:This project configures MCP servers in `.github/mcp.json`. Follow these rules:
.\.github\copilot-instructions.md:16:   MCP. All mutations go through the Express API routes with audit trail.
.\.github\copilot-instructions.md:17:2. **Filesystem access is scoped.** The MCP filesystem server can only read
.\.github\copilot-instructions.md:20:3. **Do not add MCP servers** without updating `docs/tool-trust-boundaries.md`
.\.github\copilot-instructions.md:21:   with the new server's trust classification.
.\.github\copilot-instructions.md:25:Hooks in `.github/hooks/` enforce deterministic rules. Do not try to bypass them:
.\.github\copilot-instructions.md:28:   If they fail, the commit is blocked. Fix the issues — do not disable the hook.
.\.github\copilot-instructions.md:32:   by AI assistance. See `docs/security-policy.md` for the approval process.
.\.github\hooks\file-protection.json:2:  "hooks": {
.\.github\scripts\check_protected_files.py:2:"""PreToolUse hook: block edits to protected files.
.\.github\scripts\check_protected_files.py:4:Reads JSON from stdin (VS Code hook input) and checks if the tool is
.\.github\scripts\check_protected_files.py:47:                "hookSpecificOutput": {
.\.github\scripts\check_protected_files.py:48:                    "hookEventName": "PreToolUse",
.\.github\scripts\check_protected_files.py:51:                        f"Edit blocked: '{fp}' is protected by security policy. "
.\.github\scripts\check_protected_files.py:52:                        "See docs/security-policy.md for the change approval process."
.\.github\scripts\format_file.py:4:Called by the post-save hook to auto-format TypeScript files.
.\.github\hooks\post-save-format.json:2:  "hooks": {
.\.github\hooks\pre-commit-validate.json:2:  "hooks": {
.\.github\scripts\validate_commit.py:4:Called by the pre-commit hook to ensure code quality before committing.
.\.output\change\expected-patterns.json:15:    "pattern": "barrel|index\\.ts|internal module path",
.\.output\change\expected-patterns.json:16:    "description": "Validation script should reference barrel-file or index.ts convention"
.\.output\change\expected-files.json:3:    ".github/hooks/import-validation.json",
```

</details>


---

<sub>⏱️ 31s</sub>

### 💬 Copilot

I’ve found the guardrail surface and I’m reading the existing configs, scripts, MCP file, and policy docs now so the new hook matches local conventions instead of guessing.

---

<sub>⏱️ 31s</sub>

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

<sub>⏱️ 31s</sub>

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

<sub>⏱️ 31s</sub>

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

<sub>⏱️ 31s</sub>

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

<sub>⏱️ 31s</sub>

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

<sub>⏱️ 31s</sub>

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

<sub>⏱️ 31s</sub>

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

<sub>⏱️ 31s</sub>

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

<sub>⏱️ 31s</sub>

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

<sub>⏱️ 31s</sub>

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

<sub>⏱️ 31s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "^export |^import .*from |index\\.ts$",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\06-tools-and-guardrails\\src",
  "output_mode": "content",
  "glob": "*.{ts,tsx}",
  "-n": true,
  "head_limit": 200
}
```

</details>

<details>
<summary>8 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\frontend\vite.config.ts:1:import { defineConfig } from "vite";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\frontend\vite.config.ts:3:export default defineConfig({
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\unit\state-machine.test.ts:5:import { describe, it, expect } from "vitest";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\unit\notification-service.test.ts:5:import { describe, it, expect, vi, beforeEach } from "vitest";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\unit\business-rules.test.ts:5:import { describe, it, expect } from "vitest";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\unit\business-rules.test.ts:11:import type { LoanApplication } from "../../src/models/types.js";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\integration\decisions.test.ts:5:import { describe, it, expect } from "vitest";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\integration\applications.test.ts:5:import { describe, it, expect } from "vitest";
```

</details>


---

<sub>⏱️ 31s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails**

"src\**\index.ts" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails

```
No files matched the pattern.
```


---

<sub>⏱️ 43s</sub>

### 💬 Copilot

I’ve confirmed the local patterns: hook JSON is a tiny `hooks -\> event -\> command` map, and the Python guardrail scripts are small standalone files that either emit a deny payload or exit cleanly. I’m checking the TypeScript layout now so the import rule matches the lesson’s actual barrel structure.

---

<sub>⏱️ 43s</sub>

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

<sub>⏱️ 43s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src**

"**\index.ts" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src

```
No files matched the pattern.
```


---

<sub>⏱️ 43s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "from\\s+[\"'][.]{1,2}\\/.*[\"']",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\06-tools-and-guardrails\\src",
  "output_mode": "content",
  "glob": "*.{ts,tsx}",
  "-n": true,
  "head_limit": 200
}
```

</details>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\unit\business-rules.test.ts:10:} from "../../src/rules/business-rules.js";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\unit\business-rules.test.ts:11:import type { LoanApplication } from "../../src/models/types.js";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\tests\unit\state-machine.test.ts:10:} from "../../src/rules/state-machine.js";
```


---

<sub>⏱️ 43s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "export\\s+\\*|export\\s+\\{",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\06-tools-and-guardrails\\src",
  "output_mode": "content",
  "glob": "index.ts",
  "-n": true,
  "head_limit": 200
}
```

</details>

```
No matches found.
```


---

<sub>⏱️ 50s</sub>

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

<sub>⏱️ 50s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src**

"**\*.ts" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src

<details>
<summary>32 matches</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\services\notification-service.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\services\loan-service.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\services\decision-service.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\services\audit-service.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\rules\state-machine.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\rules\role-permissions.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\rules\mandatory-events.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\rules\business-rules.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\routes\queue-status.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\routes\notifications.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\routes\decisions.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\routes\audit.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\routes\applications.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\queue\handlers\notification-handler.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\queue\handlers\audit-handler.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\queue\contracts.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\queue\broker.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\models\user-repository.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\models\types.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\models\preference-repository.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\models\loan-repository.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\models\audit-repository.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\middleware\request-validator.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\middleware\rate-limiter.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\middleware\error-handler.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\middleware\auth.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\middleware\audit-logger.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\db\seed.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\db\connection.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\config\feature-flags.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\config\env.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\backend\src\app.ts
```

</details>


---

<sub>⏱️ 50s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\frontend\src**

"**\*.tsx" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\src\frontend\src

```
No files matched the pattern.
```


---

<sub>⏱️ 50s</sub>

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

<sub>⏱️ 50s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\README.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\README.md (lines 1-120)

<details>
<summary>85 lines</summary>

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
````

</details>


---

<sub>⏱️ 1m 23s</sub>

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

<sub>⏱️ 1m 23s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.output\change\expected-patterns.json.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.output\change\expected-patterns.json

<details>
<summary>19 lines</summary>

```
1. [
2.   {
3.     "pattern": "PreToolUse",
4.     "description": "Hook config must use PreToolUse event type"
5.   },
6.   {
7.     "pattern": "validate_imports\\.py",
8.     "description": "Hook or script must reference validate_imports.py"
9.   },
10.   {
11.     "pattern": "import",
12.     "description": "Validation script must contain import-related logic"
13.   },
14.   {
15.     "pattern": "barrel|index\\.ts|internal module path",
16.     "description": "Validation script should reference barrel-file or index.ts convention"
17.   }
18. ]
19.
```

</details>


---

<sub>⏱️ 1m 23s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.output\change\expected-files.json.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.output\change\expected-files.json

<details>
<summary>9 lines</summary>

```
1. {
2.   "added": [
3.     ".github/hooks/import-validation.json",
4.     ".github/scripts/validate_imports.py"
5.   ],
6.   "modified": [],
7.   "deleted": []
8. }
9.
```

</details>


---

<sub>⏱️ 2m 4s</sub>

### 💬 Copilot

I’ve got enough context to implement this cleanly: I’m adding only the two guardrail files the lesson expects, plus a small session plan outside the repo so the work stays organized.

---

<sub>⏱️ 2m 4s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Add File: C:\\Users\\nilay\\.copilot\\session-state\\ca2dc2b2-3dc8-45bf-abad-3e17ac710e34\\plan.md\n+## Plan\n+\n+1. Review the lesson's guardrail instructions, hook configs, scripts, MCP config, and policy docs to match existing conventions.\n+2. Add `.github/hooks/import-validation.json` using the same `hooks -> PreToolUse -> command` structure as the existing hook files.\n+3. Add `.github/scripts/validate_imports.py` as a standalone Python guardrail that reads hook JSON from stdin when present, inspects changed `.ts`/`.tsx` files, and denies barrel-bypassing imports.\n+4. Verify both new files exist and the implementation stays scoped to `.github/hooks/` and `.github/scripts/`.\n*** End Patch\n"
```

</details>

```
Added 1 file(s): C:\Users\nilay\.copilot\session-state\ca2dc2b2-3dc8-45bf-abad-3e17ac710e34\plan.md
```


---

<sub>⏱️ 2m 33s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Add File: .github/hooks/import-validation.json\n+{\n+  \"hooks\": {\n+    \"PreToolUse\": [\n+      {\n+        \"type\": \"command\",\n+        \"command\": \"python .github/scripts/validate_imports.py\",\n+        \"timeout\": 10\n+      }\n+    ]\n+  }\n+}\n*** Add File: .github/scripts/validate_imports.py\n+#!/usr/bin/env python3\n+\"\"\"PreToolUse hook: enforce barrel-file imports for TypeScript files.\n+\n+Reads hook JSON from stdin when present, inspects changed .ts/.tsx files, and\n+denies imports that bypass a sibling index.ts barrel to reach into an internal\n+module path.\n+\"\"\"\n+from __future__ import annotations\n+\n+import json\n+import re\n+import sys\n+from pathlib import Path, PurePosixPath\n+from typing import Iterable\n+\n+IMPORT_PATTERN = re.compile(\n+    r\"\"\"\n+    (?:\n+        import\\s+(?:type\\s+)?(?:[\\w*\\s{},]+\\s+from\\s+)? |\n+        export\\s+(?:type\\s+)?(?:[\\w*\\s{},]+\\s+from\\s+) |\n+        import\\s*\\(\n+    )\n+    [\"'](?P<specifier>[^\"']+)[\"']\n+    \"\"\",\n+    re.VERBOSE,\n+)\n+PATH_TOKEN_PATTERN = re.compile(\n+    r\"(?P<path>(?:[A-Za-z]:)?[\\\\/][^\\s\\\"']+\\.(?:ts|tsx)|[A-Za-z0-9_.\\\\/-]+\\.(?:ts|tsx))\"\n+)\n+TS_FILE_SUFFIXES = {\".ts\", \".tsx\"}\n+SOURCE_SUFFIXES = (\".ts\", \".tsx\", \".js\", \".jsx\", \".mts\", \".cts\", \".mjs\", \".cjs\")\n+BARREL_NAMES = (\"index.ts\", \"index.tsx\")\n+IGNORED_DIRECTORIES = {\"node_modules\", \"dist\", \".git\"}\n+REPO_ROOT = Path(__file__).resolve().parents[2]\n+\n+\n+def load_hook_payload() -> dict | None:\n+    \"\"\"Read hook JSON from stdin when available.\"\"\"\n+    try:\n+        raw = sys.stdin.read()\n+    except OSError:\n+        return None\n+\n+    if not raw.strip():\n+        return None\n+\n+    try:\n+        data = json.loads(raw)\n+    except json.JSONDecodeError:\n+        return None\n+\n+    return data if isinstance(data, dict) else None\n+\n+\n+def is_typescript_file(path: Path) -> bool:\n+    return path.suffix in TS_FILE_SUFFIXES and path.is_file()\n+\n+\n+def normalize_candidate(raw_path: str) -> Path | None:\n+    raw_path = raw_path.strip().strip(\"\\\"'\")\n+    if not raw_path:\n+        return None\n+\n+    normalized = raw_path.replace(\"/\", \"\\\\\")\n+    path = Path(normalized)\n+    if not path.is_absolute():\n+        path = REPO_ROOT / path\n+\n+    try:\n+        resolved = path.resolve(strict=False)\n+    except OSError:\n+        return None\n+\n+    try:\n+        resolved.relative_to(REPO_ROOT)\n+    except ValueError:\n+        return None\n+\n+    return resolved if is_typescript_file(resolved) else None\n+\n+\n+def extract_typescript_paths(value: object) -> set[Path]:\n+    \"\"\"Recursively collect .ts/.tsx paths from hook JSON.\"\"\"\n+    matches: set[Path] = set()\n+\n+    if isinstance(value, str):\n+        for token in PATH_TOKEN_PATTERN.findall(value):\n+            candidate = normalize_candidate(token)\n+            if candidate is not None:\n+                matches.add(candidate)\n+        return matches\n+\n+    if isinstance(value, dict):\n+        for nested in value.values():\n+            matches.update(extract_typescript_paths(nested))\n+        return matches\n+\n+    if isinstance(value, list):\n+        for nested in value:\n+            matches.update(extract_typescript_paths(nested))\n+\n+    return matches\n+\n+\n+def discover_files(payload: dict | None) -> list[Path]:\n+    \"\"\"Prefer changed files from hook JSON; otherwise scan the workspace.\"\"\"\n+    if payload is not None:\n+        payload_files = sorted(extract_typescript_paths(payload))\n+        if payload_files:\n+            return payload_files\n+\n+    files: list[Path] = []\n+    for extension in (\"*.ts\", \"*.tsx\"):\n+        for path in REPO_ROOT.rglob(extension):\n+            if any(part in IGNORED_DIRECTORIES for part in path.parts):\n+                continue\n+            if path.is_file():\n+                files.append(path)\n+    return sorted(set(files))\n+\n+\n+def find_barrel(directory: Path) -> Path | None:\n+    for barrel_name in BARREL_NAMES:\n+        barrel = directory / barrel_name\n+        if barrel.is_file():\n+            return barrel\n+    return None\n+\n+\n+def is_within(path: Path, directory: Path) -> bool:\n+    try:\n+        path.relative_to(directory)\n+        return True\n+    except ValueError:\n+        return False\n+\n+\n+def candidate_targets(base_path: Path, specifier: str) -> Iterable[Path]:\n+    suffix = PurePosixPath(specifier).suffix\n+\n+    if suffix in SOURCE_SUFFIXES:\n+        if suffix == \".ts\" or suffix == \".tsx\":\n+            yield base_path\n+            return\n+\n+        stem = base_path.with_suffix(\"\")\n+        for target_suffix in TS_FILE_SUFFIXES:\n+            yield stem.with_suffix(target_suffix)\n+        return\n+\n+    yield base_path.with_suffix(\".ts\")\n+    yield base_path.with_suffix(\".tsx\")\n+    yield base_path / \"index.ts\"\n+    yield base_path / \"index.tsx\"\n+\n+\n+def resolve_import(importer: Path, specifier: str) -> Path | None:\n+    if not specifier.startswith(\".\"):\n+        return None\n+\n+    specifier_path = PurePosixPath(specifier)\n+    base_path = (importer.parent / Path(*specifier_path.parts)).resolve(strict=False)\n+\n+    for candidate in candidate_targets(base_path, specifier):\n+        if candidate.is_file():\n+            return candidate\n+\n+    return None\n+\n+\n+def format_relative_import(importer: Path, barrel: Path) -> str:\n+    relative = PurePosixPath(\n+        Path(\n+            PurePosixPath(\n+                Path(barrel.parent).relative_to(REPO_ROOT)\n+            )\n+        )\n+    )\n+    from_importer = PurePosixPath(\n+        Path(\n+            PurePosixPath(\n+                Path(importer.parent).relative_to(REPO_ROOT)\n+            )\n+        )\n+    )\n+    rel_path = PurePosixPath(\n+        Path(\n+            Path(\n+                REPO_ROOT / relative\n+            ).relative_to(REPO_ROOT)\n+        )\n+    )\n+    importer_dir = REPO_ROOT / from_importer\n+    suggestion = PurePosixPath(\n+        Path(\n+            barrel.parent.relative_to(importer_dir)\n+        )\n+    )\n+    text = str(suggestion).replace(\"\\\\\", \"/\")\n+    if not text.startswith(\".\"):\n+        text = f\"./{text}\"\n+    return text\n+\n+\n+def find_barrel_violation(importer: Path, specifier: str) -> tuple[Path, Path] | None:\n+    target = resolve_import(importer, specifier)\n+    if target is None or target.name.startswith(\"index.\"):\n+        return None\n+\n+    for directory in [target.parent, *target.parent.parents]:\n+        if not is_within(directory, REPO_ROOT):\n+            continue\n+\n+        barrel = find_barrel(directory)\n+        if barrel is None:\n+            continue\n+\n+        if is_within(importer.parent, directory):\n+            continue\n+\n+        return target, barrel\n+\n+    return None\n+\n+\n+def collect_violations(path: Path) -> list[str]:\n+    try:\n+        content = path.read_text(encoding=\"utf-8\")\n+    except OSError:\n+        return []\n+\n+    violations: list[str] = []\n+    for match in IMPORT_PATTERN.finditer(content):\n+        specifier = match.group(\"specifier\")\n+        violation = find_barrel_violation(path, specifier)\n+        if violation is None:\n+            continue\n+\n+        target, barrel = violation\n+        suggested_import = format_relative_import(path, barrel)\n+        violations.append(\n+            (\n+                f\"{path.relative_to(REPO_ROOT)} imports '{specifier}', which bypasses \"\n+                f\"the barrel '{barrel.relative_to(REPO_ROOT)}' and reaches an internal \"\n+                f\"module path '{target.relative_to(REPO_ROOT)}'. Import from \"\n+                f\"'{suggested_import}' instead.\"\n+            )\n+        )\n+\n+    return violations\n+\n+\n+def emit_deny(violations: list[str]) -> None:\n+    reason = \"Import validation failed:\\n- \" + \"\\n- \".join(violations[:10])\n+    if len(violations) > 10:\n+        reason += f\"\\n- ...and {len(violations) - 10} more violation(s).\"\n+\n+    result = {\n+        \"hookSpecificOutput\": {\n+            \"hookEventName\": \"PreToolUse\",\n+            \"permissionDecision\": \"deny\",\n+            \"permissionDecisionReason\": reason,\n+        }\n+    }\n+    json.dump(result, sys.stdout)\n+\n+\n+def main() -> None:\n+    payload = load_hook_payload()\n+    files = discover_files(payload)\n+\n+    violations: list[str] = []\n+    for path in files:\n+        violations.extend(collect_violations(path))\n+\n+    if violations:\n+        emit_deny(violations)\n+\n+\n+if __name__ == \"__main__\":\n+    main()\n*** End Patch\n"
```

</details>

```
Added 2 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\hooks\import-validation.json, Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\validate_imports.py
```


---

<sub>⏱️ 2m 42s</sub>

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
7.         "timeout": 10
8.       }
9.     ]
10.   }
11. }
12.
```

</details>


---

<sub>⏱️ 2m 42s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\validate_imports.py.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\validate_imports.py

<details>
<summary>282 lines</summary>

```
1. #!/usr/bin/env python3
2. """PreToolUse hook: enforce barrel-file imports for TypeScript files.
3. 
4. Reads hook JSON from stdin when present, inspects changed .ts/.tsx files, and
5. denies imports that bypass a sibling index.ts barrel to reach into an internal
6. module path.
7. """
8. from __future__ import annotations
9. 
10. import json
11. import re
12. import sys
13. from pathlib import Path, PurePosixPath
14. from typing import Iterable
15. 
16. IMPORT_PATTERN = re.compile(
17.     r"""
18.     (?:
19.         import\s+(?:type\s+)?(?:[\w*\s{},]+\s+from\s+)? |
20.         export\s+(?:type\s+)?(?:[\w*\s{},]+\s+from\s+) |
21.         import\s*\(
22.     )
23.     ["'](?P<specifier>[^"']+)["']
24.     """,
25.     re.VERBOSE,
26. )
27. PATH_TOKEN_PATTERN = re.compile(
28.     r"(?P<path>(?:[A-Za-z]:)?[\\/][^\s\"']+\.(?:ts|tsx)|[A-Za-z0-9_.\\/-]+\.(?:ts|tsx))"
29. )
30. TS_FILE_SUFFIXES = {".ts", ".tsx"}
31. SOURCE_SUFFIXES = (".ts", ".tsx", ".js", ".jsx", ".mts", ".cts", ".mjs", ".cjs")
32. BARREL_NAMES = ("index.ts", "index.tsx")
33. IGNORED_DIRECTORIES = {"node_modules", "dist", ".git"}
34. REPO_ROOT = Path(__file__).resolve().parents[2]
35. 
36. 
37. def load_hook_payload() -> dict | None:
38.     """Read hook JSON from stdin when available."""
39.     try:
40.         raw = sys.stdin.read()
41.     except OSError:
42.         return None
43. 
44.     if not raw.strip():
45.         return None
46. 
47.     try:
48.         data = json.loads(raw)
49.     except json.JSONDecodeError:
50.         return None
51. 
52.     return data if isinstance(data, dict) else None
53. 
54. 
55. def is_typescript_file(path: Path) -> bool:
56.     return path.suffix in TS_FILE_SUFFIXES and path.is_file()
57. 
58. 
59. def normalize_candidate(raw_path: str) -> Path | None:
60.     raw_path = raw_path.strip().strip("\"'")
61.     if not raw_path:
62.         return None
63. 
64.     normalized = raw_path.replace("/", "\\")
65.     path = Path(normalized)
66.     if not path.is_absolute():
67.         path = REPO_ROOT / path
68. 
69.     try:
70.         resolved = path.resolve(strict=False)
71.     except OSError:
72.         return None
73. 
74.     try:
75.         resolved.relative_to(REPO_ROOT)
76.     except ValueError:
77.         return None
78. 
79.     return resolved if is_typescript_file(resolved) else None
80. 
81. 
82. def extract_typescript_paths(value: object) -> set[Path]:
83.     """Recursively collect .ts/.tsx paths from hook JSON."""
84.     matches: set[Path] = set()
85. 
86.     if isinstance(value, str):
87.         for token in PATH_TOKEN_PATTERN.findall(value):
88.             candidate = normalize_candidate(token)
89.             if candidate is not None:
90.                 matches.add(candidate)
91.         return matches
92. 
93.     if isinstance(value, dict):
94.         for nested in value.values():
95.             matches.update(extract_typescript_paths(nested))
96.         return matches
97. 
98.     if isinstance(value, list):
99.         for nested in value:
100.             matches.update(extract_typescript_paths(nested))
101. 
102.     return matches
103. 
104. 
105. def discover_files(payload: dict | None) -> list[Path]:
106.     """Prefer changed files from hook JSON; otherwise scan the workspace."""
107.     if payload is not None:
108.         payload_files = sorted(extract_typescript_paths(payload))
109.         if payload_files:
110.             return payload_files
111. 
112.     files: list[Path] = []
113.     for extension in ("*.ts", "*.tsx"):
114.         for path in REPO_ROOT.rglob(extension):
115.             if any(part in IGNORED_DIRECTORIES for part in path.parts):
116.                 continue
117.             if path.is_file():
118.                 files.append(path)
119.     return sorted(set(files))
120. 
121. 
122. def find_barrel(directory: Path) -> Path | None:
123.     for barrel_name in BARREL_NAMES:
124.         barrel = directory / barrel_name
125.         if barrel.is_file():
126.             return barrel
127.     return None
128. 
129. 
130. def is_within(path: Path, directory: Path) -> bool:
131.     try:
132.         path.relative_to(directory)
133.         return True
134.     except ValueError:
135.         return False
136. 
137. 
138. def candidate_targets(base_path: Path, specifier: str) -> Iterable[Path]:
139.     suffix = PurePosixPath(specifier).suffix
140. 
141.     if suffix in SOURCE_SUFFIXES:
142.         if suffix == ".ts" or suffix == ".tsx":
143.             yield base_path
144.             return
145. 
146.         stem = base_path.with_suffix("")
147.         for target_suffix in TS_FILE_SUFFIXES:
148.             yield stem.with_suffix(target_suffix)
149.         return
150. 
151.     yield base_path.with_suffix(".ts")
152.     yield base_path.with_suffix(".tsx")
153.     yield base_path / "index.ts"
154.     yield base_path / "index.tsx"
155. 
156. 
157. def resolve_import(importer: Path, specifier: str) -> Path | None:
158.     if not specifier.startswith("."):
159.         return None
160. 
161.     specifier_path = PurePosixPath(specifier)
162.     base_path = (importer.parent / Path(*specifier_path.parts)).resolve(strict=False)
163. 
164.     for candidate in candidate_targets(base_path, specifier):
165.         if candidate.is_file():
166.             return candidate
167. 
168.     return None
169. 
170. 
171. def format_relative_import(importer: Path, barrel: Path) -> str:
172.     relative = PurePosixPath(
173.         Path(
174.             PurePosixPath(
175.                 Path(barrel.parent).relative_to(REPO_ROOT)
176.             )
177.         )
178.     )
179.     from_importer = PurePosixPath(
180.         Path(
181.             PurePosixPath(
182.                 Path(importer.parent).relative_to(REPO_ROOT)
183.             )
184.         )
185.     )
186.     rel_path = PurePosixPath(
187.         Path(
188.             Path(
189.                 REPO_ROOT / relative
190.             ).relative_to(REPO_ROOT)
191.         )
192.     )
193.     importer_dir = REPO_ROOT / from_importer
194.     suggestion = PurePosixPath(
195.         Path(
196.             barrel.parent.relative_to(importer_dir)
197.         )
198.     )
199.     text = str(suggestion).replace("\\", "/")
200.     if not text.startswith("."):
201.         text = f"./{text}"
202.     return text
203. 
204. 
205. def find_barrel_violation(importer: Path, specifier: str) -> tuple[Path, Path] | None:
206.     target = resolve_import(importer, specifier)
207.     if target is None or target.name.startswith("index."):
208.         return None
209. 
210.     for directory in [target.parent, *target.parent.parents]:
211.         if not is_within(directory, REPO_ROOT):
212.             continue
213. 
214.         barrel = find_barrel(directory)
215.         if barrel is None:
216.             continue
217. 
218.         if is_within(importer.parent, directory):
219.             continue
220. 
221.         return target, barrel
222. 
223.     return None
224. 
225. 
226. def collect_violations(path: Path) -> list[str]:
227.     try:
228.         content = path.read_text(encoding="utf-8")
229.     except OSError:
230.         return []
231. 
232.     violations: list[str] = []
233.     for match in IMPORT_PATTERN.finditer(content):
234.         specifier = match.group("specifier")
235.         violation = find_barrel_violation(path, specifier)
236.         if violation is None:
237.             continue
238. 
239.         target, barrel = violation
240.         suggested_import = format_relative_import(path, barrel)
241.         violations.append(
242.             (
243.                 f"{path.relative_to(REPO_ROOT)} imports '{specifier}', which bypasses "
244.                 f"the barrel '{barrel.relative_to(REPO_ROOT)}' and reaches an internal "
245.                 f"module path '{target.relative_to(REPO_ROOT)}'. Import from "
246.                 f"'{suggested_import}' instead."
247.             )
248.         )
249. 
250.     return violations
251. 
252. 
253. def emit_deny(violations: list[str]) -> None:
254.     reason = "Import validation failed:\n- " + "\n- ".join(violations[:10])
255.     if len(violations) > 10:
256.         reason += f"\n- ...and {len(violations) - 10} more violation(s)."
257. 
258.     result = {
259.         "hookSpecificOutput": {
260.             "hookEventName": "PreToolUse",
261.             "permissionDecision": "deny",
262.             "permissionDecisionReason": reason,
263.         }
264.     }
265.     json.dump(result, sys.stdout)
266. 
267. 
268. def main() -> None:
269.     payload = load_hook_payload()
270.     files = discover_files(payload)
271. 
272.     violations: list[str] = []
273.     for path in files:
274.         violations.extend(collect_violations(path))
275. 
276.     if violations:
277.         emit_deny(violations)
278. 
279. 
280. if __name__ == "__main__":
281.     main()
282.
```

</details>


---

<sub>⏱️ 2m 55s</sub>

### 💬 Copilot

I found one rough edge in the first pass: the import suggestion builder was more complex than it needed to be. I’m tightening that now so the deny message reliably suggests the correct barrel path.

---

<sub>⏱️ 2m 55s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Update File: .github/scripts/validate_imports.py\n@@\n import json\n+import os\n import re\n import sys\n@@\n def format_relative_import(importer: Path, barrel: Path) -> str:\n-    relative = PurePosixPath(\n-        Path(\n-            PurePosixPath(\n-                Path(barrel.parent).relative_to(REPO_ROOT)\n-            )\n-        )\n-    )\n-    from_importer = PurePosixPath(\n-        Path(\n-            PurePosixPath(\n-                Path(importer.parent).relative_to(REPO_ROOT)\n-            )\n-        )\n-    )\n-    rel_path = PurePosixPath(\n-        Path(\n-            Path(\n-                REPO_ROOT / relative\n-            ).relative_to(REPO_ROOT)\n-        )\n-    )\n-    importer_dir = REPO_ROOT / from_importer\n-    suggestion = PurePosixPath(\n-        Path(\n-            barrel.parent.relative_to(importer_dir)\n-        )\n-    )\n-    text = str(suggestion).replace(\"\\\\\", \"/\")\n+    text = Path(os.path.relpath(barrel.parent, importer.parent)).as_posix()\n     if not text.startswith(\".\"):\n         text = f\"./{text}\"\n     return text\n*** End Patch\n"
```

</details>

```
Modified 1 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\validate_imports.py
```


---

<sub>⏱️ 3m 11s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\validate_imports.py.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\06-tools-and-guardrails\.github\scripts\validate_imports.py (lines 1-260)

<details>
<summary>255 lines</summary>

```
1. #!/usr/bin/env python3
2. """PreToolUse hook: enforce barrel-file imports for TypeScript files.
3. 
4. Reads hook JSON from stdin when present, inspects changed .ts/.tsx files, and
5. denies imports that bypass a sibling index.ts barrel to reach into an internal
6. module path.
7. """
8. from __future__ import annotations
9. 
10. import json
11. import os
12. import re
13. import sys
14. from pathlib import Path, PurePosixPath
15. from typing import Iterable
16. 
17. IMPORT_PATTERN = re.compile(
18.     r"""
19.     (?:
20.         import\s+(?:type\s+)?(?:[\w*\s{},]+\s+from\s+)? |
21.         export\s+(?:type\s+)?(?:[\w*\s{},]+\s+from\s+) |
22.         import\s*\(
23.     )
24.     ["'](?P<specifier>[^"']+)["']
25.     """,
26.     re.VERBOSE,
27. )
28. PATH_TOKEN_PATTERN = re.compile(
29.     r"(?P<path>(?:[A-Za-z]:)?[\\/][^\s\"']+\.(?:ts|tsx)|[A-Za-z0-9_.\\/-]+\.(?:ts|tsx))"
30. )
31. TS_FILE_SUFFIXES = {".ts", ".tsx"}
32. SOURCE_SUFFIXES = (".ts", ".tsx", ".js", ".jsx", ".mts", ".cts", ".mjs", ".cjs")
33. BARREL_NAMES = ("index.ts", "index.tsx")
34. IGNORED_DIRECTORIES = {"node_modules", "dist", ".git"}
35. REPO_ROOT = Path(__file__).resolve().parents[2]
36. 
37. 
38. def load_hook_payload() -> dict | None:
39.     """Read hook JSON from stdin when available."""
40.     try:
41.         raw = sys.stdin.read()
42.     except OSError:
43.         return None
44. 
45.     if not raw.strip():
46.         return None
47. 
48.     try:
49.         data = json.loads(raw)
50.     except json.JSONDecodeError:
51.         return None
52. 
53.     return data if isinstance(data, dict) else None
54. 
55. 
56. def is_typescript_file(path: Path) -> bool:
57.     return path.suffix in TS_FILE_SUFFIXES and path.is_file()
58. 
59. 
60. def normalize_candidate(raw_path: str) -> Path | None:
61.     raw_path = raw_path.strip().strip("\"'")
62.     if not raw_path:
63.         return None
64. 
65.     normalized = raw_path.replace("/", "\\")
66.     path = Path(normalized)
67.     if not path.is_absolute():
68.         path = REPO_ROOT / path
69. 
70.     try:
71.         resolved = path.resolve(strict=False)
72.     except OSError:
73.         return None
74. 
75.     try:
76.         resolved.relative_to(REPO_ROOT)
77.     except ValueError:
78.         return None
79. 
80.     return resolved if is_typescript_file(resolved) else None
81. 
82. 
83. def extract_typescript_paths(value: object) -> set[Path]:
84.     """Recursively collect .ts/.tsx paths from hook JSON."""
85.     matches: set[Path] = set()
86. 
87.     if isinstance(value, str):
88.         for token in PATH_TOKEN_PATTERN.findall(value):
89.             candidate = normalize_candidate(token)
90.             if candidate is not None:
91.                 matches.add(candidate)
92.         return matches
93. 
94.     if isinstance(value, dict):
95.         for nested in value.values():
96.             matches.update(extract_typescript_paths(nested))
97.         return matches
98. 
99.     if isinstance(value, list):
100.         for nested in value:
101.             matches.update(extract_typescript_paths(nested))
102. 
103.     return matches
104. 
105. 
106. def discover_files(payload: dict | None) -> list[Path]:
107.     """Prefer changed files from hook JSON; otherwise scan the workspace."""
108.     if payload is not None:
109.         payload_files = sorted(extract_typescript_paths(payload))
110.         if payload_files:
111.             return payload_files
112. 
113.     files: list[Path] = []
114.     for extension in ("*.ts", "*.tsx"):
115.         for path in REPO_ROOT.rglob(extension):
116.             if any(part in IGNORED_DIRECTORIES for part in path.parts):
117.                 continue
118.             if path.is_file():
119.                 files.append(path)
120.     return sorted(set(files))
121. 
122. 
123. def find_barrel(directory: Path) -> Path | None:
124.     for barrel_name in BARREL_NAMES:
125.         barrel = directory / barrel_name
126.         if barrel.is_file():
127.             return barrel
128.     return None
129. 
130. 
131. def is_within(path: Path, directory: Path) -> bool:
132.     try:
133.         path.relative_to(directory)
134.         return True
135.     except ValueError:
136.         return False
137. 
138. 
139. def candidate_targets(base_path: Path, specifier: str) -> Iterable[Path]:
140.     suffix = PurePosixPath(specifier).suffix
141. 
142.     if suffix in SOURCE_SUFFIXES:
143.         if suffix == ".ts" or suffix == ".tsx":
144.             yield base_path
145.             return
146. 
147.         stem = base_path.with_suffix("")
148.         for target_suffix in TS_FILE_SUFFIXES:
149.             yield stem.with_suffix(target_suffix)
150.         return
151. 
152.     yield base_path.with_suffix(".ts")
153.     yield base_path.with_suffix(".tsx")
154.     yield base_path / "index.ts"
155.     yield base_path / "index.tsx"
156. 
157. 
158. def resolve_import(importer: Path, specifier: str) -> Path | None:
159.     if not specifier.startswith("."):
160.         return None
161. 
162.     specifier_path = PurePosixPath(specifier)
163.     base_path = (importer.parent / Path(*specifier_path.parts)).resolve(strict=False)
164. 
165.     for candidate in candidate_targets(base_path, specifier):
166.         if candidate.is_file():
167.             return candidate
168. 
169.     return None
170. 
171. 
172. def format_relative_import(importer: Path, barrel: Path) -> str:
173.     text = Path(os.path.relpath(barrel.parent, importer.parent)).as_posix()
174.     if not text.startswith("."):
175.         text = f"./{text}"
176.     return text
177. 
178. 
179. def find_barrel_violation(importer: Path, specifier: str) -> tuple[Path, Path] | None:
180.     target = resolve_import(importer, specifier)
181.     if target is None or target.name.startswith("index."):
182.         return None
183. 
184.     for directory in [target.parent, *target.parent.parents]:
185.         if not is_within(directory, REPO_ROOT):
186.             continue
187. 
188.         barrel = find_barrel(directory)
189.         if barrel is None:
190.             continue
191. 
192.         if is_within(importer.parent, directory):
193.             continue
194. 
195.         return target, barrel
196. 
197.     return None
198. 
199. 
200. def collect_violations(path: Path) -> list[str]:
201.     try:
202.         content = path.read_text(encoding="utf-8")
203.     except OSError:
204.         return []
205. 
206.     violations: list[str] = []
207.     for match in IMPORT_PATTERN.finditer(content):
208.         specifier = match.group("specifier")
209.         violation = find_barrel_violation(path, specifier)
210.         if violation is None:
211.             continue
212. 
213.         target, barrel = violation
214.         suggested_import = format_relative_import(path, barrel)
215.         violations.append(
216.             (
217.                 f"{path.relative_to(REPO_ROOT)} imports '{specifier}', which bypasses "
218.                 f"the barrel '{barrel.relative_to(REPO_ROOT)}' and reaches an internal "
219.                 f"module path '{target.relative_to(REPO_ROOT)}'. Import from "
220.                 f"'{suggested_import}' instead."
221.             )
222.         )
223. 
224.     return violations
225. 
226. 
227. def emit_deny(violations: list[str]) -> None:
228.     reason = "Import validation failed:\n- " + "\n- ".join(violations[:10])
229.     if len(violations) > 10:
230.         reason += f"\n- ...and {len(violations) - 10} more violation(s)."
231. 
232.     result = {
233.         "hookSpecificOutput": {
234.             "hookEventName": "PreToolUse",
235.             "permissionDecision": "deny",
236.             "permissionDecisionReason": reason,
237.         }
238.     }
239.     json.dump(result, sys.stdout)
240. 
241. 
242. def main() -> None:
243.     payload = load_hook_payload()
244.     files = discover_files(payload)
245. 
246.     violations: list[str] = []
247.     for path in files:
248.         violations.extend(collect_violations(path))
249. 
250.     if violations:
251.         emit_deny(violations)
252. 
253. 
254. if __name__ == "__main__":
255.     main()
```

</details>


---

<sub>⏱️ 3m 11s</sub>

### ✅ `store_memory`

<details>
<summary>Arguments</summary>

```json
{
  "subject": "guardrails",
  "fact": "Lesson 06 guardrail hooks use JSON with hooks[event] command entries that invoke Python scripts from .github/scripts/.",
  "citations": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\06-tools-and-guardrails\\.github\\hooks\\file-protection.json:1-11; Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\06-tools-and-guardrails\\.github\\hooks\\pre-commit-validate.json:1-11; Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\06-tools-and-guardrails\\.github\\scripts\\check_protected_files.py:1-63",
  "reason": "This hook/config pattern is a stable repository convention that future code-generation or review tasks need to preserve when adding or modifying guardrails. Remembering that lesson 06 guardrails are wired through small JSON hook configs that invoke Python scripts will help keep future changes consistent with the existing runtime enforcement surface.",
  "category": "general"
}
```

</details>

```
Memory stored successfully.
```


---

<sub>⏱️ 3m 21s</sub>

### 💬 Copilot

Implemented the new guardrail in the lesson’s existing pattern.

I first inspected `.github/copilot-instructions.md`, `.github/mcp.json`, the existing hook configs, the Python guardrail scripts, and the policy docs before editing.

Added:

- `.github/hooks/import-validation.json` with a `PreToolUse` command hook invoking `python .github/scripts/validate_imports.py`
- `.github/scripts/validate_imports.py`, a complete standalone guardrail that reads hook JSON from `stdin` when present, finds changed `.ts`/`.tsx` files, resolves relative imports, and denies imports that bypass an `index.ts`/`index.tsx` barrel to reach internal module paths

No shell commands or SQL were used.

---

<sub>Generated by [GitHub Copilot CLI](https://github.com/features/copilot/cli)</sub>
