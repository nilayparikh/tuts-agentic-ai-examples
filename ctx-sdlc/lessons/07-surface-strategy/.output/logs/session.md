# 🤖 Copilot CLI Session

> [!NOTE]
> - **Session ID:** `91fc5598-5648-434f-abb8-13ff42b84815`  
> - **Started:** 14/03/2026, 01:55:10  
> - **Duration:** 2m 7s  
> - **Exported:** 14/03/2026, 01:57:17  

---

<sub>⏱️ 5s</sub>

### 👤 User

Inspect the lesson's surface-strategy artifacts before answering. Discover the relevant baseline instructions, scoped instructions, agents, prompts, MCP, hooks, and docs that exist here rather than assuming a fixed file list. Then create two new files based on your analysis: 1. Create .github/instructions/portable-baseline.instructions.md containing the extracted cross-surface-portable subset of the existing instructions that works on CLI, Chat, inline completions, coding agent, and code review surfaces. Use applyTo: '**' scope. 2. Create docs/surface-portability-notes.md documenting which features are portable vs surface-specific, one concrete portability risk, one false positive, one hard negative, and recommendations for where each kind of guidance should live. Follow the discovered instruction architecture conventions. Apply the changes directly in files. Do not run shell commands and do not use SQL.

---

<sub>⏱️ 17s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy**

".github/**/*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.github\copilot-instructions.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.github\instructions\api.instructions.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.github\agents\reviewer.agent.md
```


---

<sub>⏱️ 17s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy**

"docs/**/*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\surface-strategy-example.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\portability-matrix.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\cli-guide.md
```


---

<sub>⏱️ 17s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "applyTo:|Copilot|instruction|Instructions|prompt|agent|hook|MCP|modelcontextprotocol|model context protocol",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\07-surface-strategy",
  "output_mode": "files_with_matches",
  "head_limit": 200
}
```

</details>

<details>
<summary>12 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\util.py
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\ASSESSMENT.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\README.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\surface-strategy-example.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\portability-matrix.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\cli-guide.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.github\copilot-instructions.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.github\instructions\api.instructions.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.github\agents\reviewer.agent.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.output\logs\command.txt
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.output\logs\process-1773453309034-18460.log
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.output\logs\prompt.txt
```

</details>


---

<sub>⏱️ 24s</sub>

### 💬 Copilot

I’m mapping the lesson’s actual instruction architecture first so the new files reflect what’s already here, not a guessed template. Next I’ll extract the portable subset and document the surface-specific gaps clearly.

---

<sub>⏱️ 24s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy**

".*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy

```
No files matched the pattern.
```


---

<sub>⏱️ 24s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy**

"**/*.md" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy

<details>
<summary>8 matches</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\README.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\surface-strategy-example.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\portability-matrix.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\cli-guide.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\ASSESSMENT.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.github\instructions\api.instructions.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.github\copilot-instructions.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.github\agents\reviewer.agent.md
```

</details>


---

<sub>⏱️ 24s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "hook|hooks|MCP|mcp|prompt|prompts|agent|agents|copilot-instructions|applyTo",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\07-surface-strategy",
  "output_mode": "content",
  "-n": true,
  "head_limit": 250
}
```

</details>

```
Output too large to read at once (53.4 KB). Saved to: C:\Users\nilay\AppData\Local\Temp\copilot-tool-output-1773453334816-n5jc18.txt
Consider using tools like grep (for searching), head/tail (for viewing start/end), view with view_range (for specific sections), or jq (for JSON) to examine portions of the output.

Preview (first 500 chars):
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\util.py:30:KEPT_LOG_F
```


---

<sub>⏱️ 24s</sub>

### ❌ `view`

**view the file at C:\Users\nilay\.copilot\session-state\91fc5598-5648-434f-abb8-13ff42b84815\plan.md.**

C:\Users\nilay\.copilot\session-state\91fc5598-5648-434f-abb8-13ff42b84815\plan.md

```
Path does not exist
```


---

<sub>⏱️ 33s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.github\copilot-instructions.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.github\copilot-instructions.md

<details>
<summary>52 lines</summary>

```
1. # Loan Workbench — Project Context
2. 
3. > **Auto-loaded** by all Copilot surfaces that support repository-level instructions.
4. > This is the most portable context artifact — it works in VS Code Chat,
5. > VS Code Inline, GitHub CLI, Copilot Coding Agent, and Code Review suggestions.
6. 
7. ## Project
8. 
9. Loan Workbench API — TypeScript + Express REST service managing loan
10. application lifecycles with regulatory compliance (California SMS restriction),
11. role-based access, and audit-first persistence.
12. 
13. ## Tech Stack
14. 
15. - Runtime: Node.js 20 LTS
16. - Language: TypeScript 5.x (strict mode)
17. - Framework: Express 4, better-sqlite3 for persistence
18. - Queue: In-process event broker for async side-effects
19. - Tests: Vitest (see ADR-002 — do NOT suggest Jest)
20. - Modules: ESM only (see ADR-003 — no CommonJS)
21. - Logging: structured JSON via pino
22. 
23. ## Architecture
24. 
25. Four-layer separation:
26. 
27. 1. **Routes** (`app/backend/src/routes/`) — HTTP handling, parameter extraction, delegation
28. 2. **Rules** (`app/backend/src/rules/`) — pure business logic, no I/O
29. 3. **Services** (`app/backend/src/services/`) — persistence, external integrations, audit
30. 4. **Queue** (`app/backend/src/queue/`) — async event handling (notifications, audit)
31. 
32. Request flow: Route → authenticate → authorize → validate → Rule → Service → respond.
33. 
34. Audit events are emitted BEFORE persistence — if the audit fails, the write
35. does NOT proceed (fail-closed semantics).
36. 
37. ## Coding Conventions
38. 
39. - `const` over `let`; never `var`
40. - All route handlers are `async`
41. - All errors return structured JSON: `{ error: string, code: string }`
42. - No stack traces in error responses (security)
43. - Feature flags use 404 (feature not found), not 403 (forbidden)
44. - Logging: structured JSON, never `console.log()`
45. - Tests annotated with `// FALSE POSITIVE` or `// HARD NEGATIVE` where applicable
46. 
47. ## References
48. 
49. - Full architecture: see `/docs/architecture.md`
50. - API conventions: see `/docs/api-conventions.md`
51. - Technology decisions: see `/docs/adr/`
52.
```

</details>


---

<sub>⏱️ 33s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.github\instructions\api.instructions.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.github\instructions\api.instructions.md

<details>
<summary>43 lines</summary>

````
1. ---
2. applyTo: "app/backend/src/routes/**"
3. ---
4. 
5. # API Route Instructions
6. 
7. These rules apply only when editing files under `app/backend/src/routes/`.
8. 
9. ## Route Handler Pattern
10. 
11. Every route handler MUST follow this template:
12. 
13. ```typescript
14. router.post("/path", authenticate, authorize("role"), async (req, res) => {
15.   const validated = schema.parse(req.body);
16.   const result = await ruleFunction(validated);
17.   await auditService.record({ action: "action_name", ...result });
18.   await persistenceService.save(result);
19.   res.status(201).json(result);
20. });
21. ```
22. 
23. ## Middleware Chain
24. 
25. Always apply in this order:
26. 
27. 1. `authenticate` — validates session token
28. 2. `authorize(role)` — checks role-based access
29. 3. Handler body — validates, delegates, responds
30. 
31. ## Error Handling
32. 
33. - Validation errors: 400 with `{ error: string, code: "VALIDATION_ERROR" }`
34. - Not found: 404 with `{ error: string, code: "NOT_FOUND" }`
35. - Feature flag disabled: 404 (NOT 403) with `{ error: string, code: "NOT_FOUND" }`
36. - Unauthorized: 401 with `{ error: "Unauthorized", code: "AUTH_REQUIRED" }`
37. - Forbidden: 403 with `{ error: string, code: "FORBIDDEN" }`
38. 
39. > **Note**: This file uses `applyTo` scoping — it is only active in VS Code
40. > and Copilot Coding Agent. It is NOT loaded in GitHub CLI or Code Review.
41. > The portable equivalent is the pattern documented in
42. > `.github/copilot-instructions.md` and `/docs/api-conventions.md`.
43.
````

</details>


---

<sub>⏱️ 33s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.github\agents\reviewer.agent.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.github\agents\reviewer.agent.md

<details>
<summary>63 lines</summary>

````
1. ---
2. name: reviewer
3. description: Reviews pull requests for architecture compliance, convention adherence, and security concerns.
4. tools:
5.   - search/codebase
6.   - read/problems
7.   - search/usages
8.   - read/readFile
9.   - search/textSearch
10. ---
11. 
12. # Code Reviewer Agent
13. 
14. You are a senior code reviewer for the Loan Workbench API. Review all changes
15. against the project's architecture and conventions.
16. 
17. ## Review Checklist
18. 
19. For every file changed, verify:
20. 
21. ### Architecture Compliance
22. 
23. - [ ] Routes only handle HTTP — no business logic
24. - [ ] Business logic is in `app/backend/src/rules/` — pure functions, no I/O
25. - [ ] Services handle persistence and external calls
26. - [ ] Audit events are recorded BEFORE persistence (fail-closed)
27. 
28. ### Convention Compliance
29. 
30. - [ ] ESM imports only (no `require()`)
31. - [ ] `const` over `let`, never `var`
32. - [ ] Structured JSON logging (no `console.log()`)
33. - [ ] Error responses: `{ error: string, code: string }`, no stack traces
34. - [ ] Feature flags: 404 not 403
35. 
36. ### Security
37. 
38. - [ ] No secrets in code or comments
39. - [ ] No stack traces in error responses
40. - [ ] Role checks applied on all new routes
41. - [ ] Delegated sessions — no permanent token elevation
42. 
43. ### Test Coverage
44. 
45. - [ ] New routes have corresponding test files
46. - [ ] Tests use Vitest (not Jest)
47. - [ ] FALSE POSITIVE / HARD NEGATIVE annotations where applicable
48. 
49. ## Output Format
50. 
51. For each issue found, report:
52. 
53. ```
54. **[SEVERITY]** file:line — description
55. Suggestion: what to change
56. ```
57. 
58. Severities: CRITICAL (must fix), WARNING (should fix), INFO (consider fixing).
59. 
60. > **Surface Note**: This agent is available in VS Code Chat. It is NOT
61. > available in GitHub CLI, Code Review, or Inline completions. For CLI
62. > users, reference the checklist in `/docs/api-conventions.md` instead.
63.
````

</details>


---

<sub>⏱️ 33s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\README.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\README.md

<details>
<summary>82 lines</summary>

````
1. # Lesson 07 — Surface Strategy
2. 
3. > **App:** Loan Workbench (TypeScript Express API + SQLite)
4. > **Topic:** Tailoring context for different Copilot surfaces and ensuring portability across environments.
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
15. Different Copilot surfaces consume context differently.
16. 
17. | Surface | Context Access | Best For |
18. | --- | --- | --- |
19. | Agent mode (Chat) | Full `.github/`, agents, prompts, tools | Complex multi-step tasks |
20. | Inline completions | `.github/instructions/` auto-scoped by file | Line-by-line generation |
21. | CLI (`copilot`) | Baseline repo context plus what it discovers | Quick scripted prompting |
22. | Other IDEs | Portable baseline instructions | Cross-IDE consistency |
23. 
24. ## Context Files
25. 
26. | Path | Purpose |
27. | --- | --- |
28. | `.github/copilot-instructions.md` | Universal baseline |
29. | `.github/instructions/api.instructions.md` | API-scoped rules |
30. | `.github/agents/reviewer.agent.md` | Review agent |
31. | `docs/cli-guide.md` | CLI usage reference |
32. | `docs/portability-matrix.md` | Surface compatibility reference |
33. | `docs/surface-strategy-example.md` | Concrete lesson-07 demo target and assessment constraints |
34. 
35. ## Example Goal
36. 
37. This lesson should demonstrate surface-portability analysis through produced artifacts.
38. 
39. For this example, the intended outcome is:
40. 
41. - inspect the lesson's baseline instructions, scoped instructions, agent, and docs
42. - discover the relevant portability artifacts instead of relying on a hardcoded read list
43. - create a portable-baseline instruction file extracting the cross-surface-portable subset
44. - create a surface-portability notes document with risk taxonomy and recommendations
45. - the changes are assessable via actual vs expected file and pattern comparison
46. 
47. ## Copilot CLI Workflow
48. 
49. Run from the lesson root:
50. 
51. ```bash
52. copilot -p "Inspect the lesson's surface-strategy artifacts before answering. Discover the relevant baseline instructions, scoped instructions, agents, prompts, MCP, hooks, and docs that exist here rather than assuming a fixed file list. Then create two new files based on your analysis: 1. Create .github/instructions/portable-baseline.instructions.md containing the extracted cross-surface-portable subset of the existing instructions that works on CLI, Chat, inline completions, coding agent, and code review surfaces. Use applyTo: '**' scope. 2. Create docs/surface-portability-notes.md documenting which features are portable vs surface-specific, one concrete portability risk, one false positive, one hard negative, and recommendations for where each kind of guidance should live. Follow the discovered instruction architecture conventions. Apply the changes directly in files. Do not run shell commands and do not use SQL." --allow-all-tools --deny-tool=powershell --deny-tool=sql
53. ```
54. 
55. Expected result:
56. 
57. - the CLI creates `.github/instructions/portable-baseline.instructions.md` and `docs/surface-portability-notes.md`
58. - the portable baseline instruction contains only cross-surface guidance
59. - the portability notes document includes risk taxonomy with false positive and hard negative
60. - `.output/change/demo.patch` contains the new files
61. - `.output/change/comparison.md` shows actual vs expected file and pattern match results
62. 
63. ## VS Code Chat Workflow
64. 
65. Compare the same repository ask across three surfaces:
66. 
67. - Agent mode for full multi-step assistance
68. - Inline completions inside an API file for scoped instruction activation
69. - Ask mode with explicit file attachments where needed
70. 
71. Use the portability matrix and ask which guidance belongs in the universal baseline versus scoped instructions.
72. 
73. Expected result: you see why some guidance must live in `copilot-instructions.md`, while more specialized rules should remain scoped.
74. 
75. For the captured demo run, use `python util.py --demo --model gpt-5.4`.
76. 
77. ## Cleanup
78. 
79. ```bash
80. python util.py --clean
81. ```
82.
````

</details>


---

<sub>⏱️ 33s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\surface-strategy-example.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\surface-strategy-example.md

<details>
<summary>48 lines</summary>

```
1. # Lesson 07 — Surface Strategy Example
2. 
3. This document defines the concrete example used in Lesson 07.
4. 
5. ## Objective
6. 
7. Show that the CLI can analyze surface-portability concerns and produce actionable artifacts: a portable baseline instruction file and a surface-portability analysis document.
8. 
9. ## Expected Output Shape
10. 
11. The demo must produce two new files:
12. 
13. 1. `.github/instructions/portable-baseline.instructions.md` — extracted cross-surface-portable instruction subset with `applyTo: '**'` scope
14. 2. `docs/surface-portability-notes.md` — analysis documenting portable vs surface-specific features, risks, and recommendations
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
25. 1. The portable baseline instruction must work across CLI, Chat, inline completions, coding agent, and code review surfaces.
26. 2. The analysis must compare CLI, VS Code Chat, inline completions, coding agent, and code review explicitly.
27. 3. The analysis must treat `.github/copilot-instructions.md` as the universal baseline and explain why.
28. 4. The analysis must note that `.instructions.md`, agents, prompts, MCP, and hooks are not equally portable.
29. 5. If lesson artifacts disagree, the analysis must identify which one should be treated as canonical and why.
30. 6. The portability notes must include one portability risk, one false positive, and one hard negative.
31. 7. Do not run shell commands during the assessment run.
32. 8. Do not use SQL during the assessment run.
33. 
34. ## Concrete Scenario
35. 
36. Use the lesson's current files to extract what guidance would still help on the widest range of Copilot surfaces and capture that in a dedicated portable-baseline instruction file.
37. 
38. ## What Good Output Looks Like
39. 
40. Good output will usually:
41. 
42. - create a portable-baseline instruction file scoped to all files
43. - extract only guidance that works across all five surfaces
44. - create a portability notes document with risk taxonomy
45. - explain why `api.instructions.md` is stronger but less portable than the baseline
46. - call out one false positive where a CLI limitation is mistaken for missing context
47. - call out one hard negative where teams put critical guidance only in a non-portable layer
48.
```

</details>


---

<sub>⏱️ 33s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\portability-matrix.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\portability-matrix.md

<details>
<summary>120 lines</summary>

````
1. # Portability Matrix — Context Artifacts × Surfaces
2. 
3. Use this matrix to decide where to place context based on which surfaces
4. your team uses.
5. 
6. ## Feature × Surface Support
7. 
8. | Context Artifact                  | VS Code Chat | VS Code Inline | GitHub CLI | Coding Agent | Code Review |
9. | --------------------------------- | :----------: | :------------: | :--------: | :----------: | :---------: |
10. | `.github/copilot-instructions.md` |      ✅      |       ✅       |     ✅     |      ✅      |     ✅      |
11. | `.instructions.md` (path-scoped)  |      ✅      |       ✅       |     ❌     |      ✅      |     ❌      |
12. | `.agent.md` (agents)              |      ✅      |       ❌       |     ❌     |      ✅      |     ❌      |
13. | `SKILL.md` (skills)               |      ✅      |       ❌       |     ❌     |      ❌      |     ❌      |
14. | `.prompt.md` (prompt files)       |      ✅      |       ❌       |     ❌     |      ✅      |     ❌      |
15. | `mcp.json` (tool servers)         |      ✅      |       ❌       |     ❌     |      ✅      |     ❌      |
16. | Copilot Hooks                     |      ✅      |       ❌       |     ❌     |      ❌      |     ❌      |
17. | `#file:` attachment               |      ✅      |       ❌       |     ❌     |      ✅      |     ❌      |
18. | `@workspace` indexing             |      ✅      |       ❌       |     ❌     |      ✅      |     ❌      |
19. | `docs/*.md` (semantic search)     |      ✅      |    Partial     |  Partial   |      ✅      |   Partial   |
20. 
21. ## The Portability Pyramid
22. 
23. ```
24.                     ┌─────────────┐
25.                     │    Hooks    │ ← VS Code only
26.                    ─┤   Skills   │ ← VS Code Chat only
27.                   ──┤   Agents   │ ← VS Code Chat + Coding Agent
28.                  ───┤  Prompts   │ ← VS Code Chat + Coding Agent
29.                 ────┤    MCP     │ ← VS Code + Coding Agent
30.                ─────┤ .instructions.md │ ← VS Code + Coding Agent
31.               ──────┤ docs/*.md  │ ← all (via search / #file:)
32.              ───────┤ copilot-instructions.md │ ← ALL SURFACES
33.              ───────┴────────────────────────┘
34. ```
35. 
36. **Foundation-first design**: Start at the base (most portable) and layer
37. upward. Each layer adds power but reduces portability.
38. 
39. ## Decision Framework
40. 
41. ### Choosing the Right Layer
42. 
43. **Question 1**: Does this context need to work for CLI users?
44. 
45. - YES → Must be in `.github/copilot-instructions.md` or `docs/`
46. - NO → Can use any layer
47. 
48. **Question 2**: Does this context need path activation?
49. 
50. - YES → Use `.instructions.md` (accepts `applyTo` globs)
51. - NO → Use `.github/copilot-instructions.md` for rules, `docs/` for knowledge
52. 
53. **Question 3**: Does this context define a role with specific tools?
54. 
55. - YES → Use `.agent.md` (with tool restrictions)
56. - NO → Use instructions or prompts
57. 
58. **Question 4**: Is this a repeatable multi-step workflow?
59. 
60. - YES → Use `.prompt.md` (with variables)
61. - NO → Put it in instructions
62. 
63. **Question 5**: Does this need automated enforcement (no human trigger)?
64. 
65. - YES → Use hooks (pre-commit, post-edit)
66. - NO → Use any appropriate layer
67. 
68. ### Example Decisions
69. 
70. | Context Need                         | Correct Layer             | Why                                      |
71. | ------------------------------------ | ------------------------- | ---------------------------------------- |
72. | "Use ESM imports"                    | `copilot-instructions.md` | Universal rule, all surfaces need it     |
73. | "Route handlers follow this pattern" | `api.instructions.md`     | Path-scoped to `app/backend/src/routes/` |
74. | "Review code against checklist"      | `reviewer.agent.md`       | Role + tool restrictions                 |
75. | "Plan a new feature"                 | `add-feature.prompt.md`   | Repeatable workflow with variables       |
76. | "Block commits with TODO"            | `pre-commit-guard` hook   | Automated enforcement                    |
77. | "System architecture"                | `docs/architecture.md`    | Deep knowledge, not a rule               |
78. | "Why Express over Fastify"           | `docs/adr/ADR-001.md`     | Decision record, referenceable knowledge |
79. 
80. ## Portability Testing Protocol
81. 
82. When adding or changing context, verify it works on your team's active surfaces:
83. 
84. ### 1. VS Code Chat Test
85. 
86. ```
87. Open Chat → ask about the topic → verify context is applied
88. ```
89. 
90. ### 2. VS Code Inline Test
91. 
92. ```
93. Start typing in a relevant file → verify completions follow conventions
94. ```
95. 
96. ### 3. CLI Test
97. 
98. ```bash
99. cd /project/root
100. copilot -p "relevant prompt about the topic" --allow-all
101. # Verify output follows conventions from copilot-instructions.md
102. ```
103. 
104. ### 4. Coding Agent Test
105. 
106. ```
107. Open Copilot Coding Agent → describe task → verify it picks up
108. instructions.md, agents, and prompts
109. ```
110. 
111. ### 5. Code Review Test
112. 
113. ```
114. Open a PR → check Copilot review suggestions → verify they reference
115. copilot-instructions.md conventions
116. ```
117. 
118. **If it only needs to work in VS Code Chat**: any layer is fine.
119. **If it needs to work everywhere**: `.github/copilot-instructions.md` only.
120.
````

</details>


---

<sub>⏱️ 33s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\cli-guide.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\cli-guide.md

<details>
<summary>157 lines</summary>

````
1. # GitHub Copilot CLI — Configuration Guide
2. 
3. This guide shows how to use the standalone GitHub Copilot CLI in the terminal
4. alongside the VS Code context already set up for the Loan Workbench.
5. 
6. ## Installation
7. 
8. ```bash
9. # Install the GitHub Copilot CLI (standalone)
10. npm install -g @githubnext/github-copilot-cli
11. 
12. # Verify installation
13. copilot --version
14. ```
15. 
16. ## Basic Commands
17. 
18. ```bash
19. # Get a code suggestion (non-interactive, auto-approve)
20. copilot -p "add a delete route for loan applications" --allow-all
21. 
22. # Explain existing code
23. copilot -p "explain app/backend/src/middleware/auth.ts" --allow-all
24. 
25. # Suggest a git command
26. copilot -p "undo last commit but keep changes" --allow-all
27. 
28. # Suggest a shell command
29. copilot -p "find all TypeScript files with console.log" --allow-all
30. 
31. # Save output to a markdown file
32. copilot -p "add a delete route" --allow-all --share=output.md
33. 
34. # Use a specific model
35. copilot -p "explain this code" --allow-all --model gpt-5.4
36. 
37. # Silent mode (no spinner)
38. copilot -p "explain this code" --allow-all -s
39. 
40. # Skip custom instructions
41. copilot -p "explain this code" --allow-all --no-custom-instructions
42. ```
43. 
44. ## How Context Loads in CLI
45. 
46. | Context Artifact                         | Loaded in CLI? | Notes                              |
47. | ---------------------------------------- | -------------- | ---------------------------------- |
48. | `.github/copilot-instructions.md`        | ✅ Yes         | Auto-loaded from repo root         |
49. | `.github/instructions/*.instructions.md` | ❌ No          | VS Code only (applyTo scoping)     |
50. | `.github/agents/*.agent.md`              | ❌ No          | VS Code Chat only                  |
51. | `.github/skills/*/SKILL.md`              | ❌ No          | VS Code Chat only                  |
52. | `.github/prompts/*.prompt.md`            | ❌ No          | VS Code Chat only (slash commands) |
53. | `.github/hooks/*`                        | ❌ No          | VS Code only                       |
54. | `.github/mcp.json`                       | ❌ No          | VS Code only                       |
55. | `docs/*.md` (via #file: attachment)      | ❌ No          | VS Code Chat only                  |
56. | `docs/*.md` (via semantic search)        | ✅ Partial     | If the repo is indexed             |
57. 
58. **Key insight**: `.github/copilot-instructions.md` is the ONLY context file
59. that is guaranteed to load across all surfaces. This is why Lesson 02 puts
60. the most critical context there.
61. 
62. ## Shell Aliases (Optional)
63. 
64. Add these to your shell profile (`~/.bashrc`, `~/.zshrc`, or PowerShell
65. `$PROFILE`) for faster workflows:
66. 
67. ```bash
68. # Bash/Zsh aliases
69. alias cq='copilot -p'            # quick prompt
70. alias cqa='copilot -p --allow-all' # auto-approve
71. ```
72. 
73. ```powershell
74. # PowerShell aliases
75. function cq  { copilot -p @args }
76. function cqa { copilot -p @args --allow-all }
77. ```
78. 
79. ## Workflow Examples
80. 
81. ### Generating a New Route (CLI)
82. 
83. ```bash
84. # Navigate to the project root (where .github/ lives)
85. cd /path/to/loan-workbench
86. 
87. # The CLI auto-loads .github/copilot-instructions.md
88. copilot -p "write an Express route handler for GET /api/v1/applications/:id
89. that follows the three-layer architecture (route → rules → service),
90. uses ESM imports, and returns structured JSON errors" --allow-all
91. ```
92. 
93. The suggestion will follow the conventions from `copilot-instructions.md`:
94. ESM imports, `const`, `async` handler, structured error responses.
95. 
96. But it will NOT know about the detailed architecture (state machine, fail-closed
97. audit) because `docs/architecture.md` is not auto-loaded in CLI.
98. 
99. ### Explaining Code (CLI)
100. 
101. ```bash
102. copilot -p "explain app/backend/src/rules/smsRestriction.ts" --allow-all
103. ```
104. 
105. The CLI will explain the code using whatever it can infer from the file content
106. plus the instructions in `.github/copilot-instructions.md`. It will know this
107. is an Express/TypeScript project with specific conventions.
108. 
109. ### Git Workflow (CLI)
110. 
111. ```bash
112. # Suggest the right git command
113. copilot -p "create a branch for adding delete functionality" --allow-all
114. 
115. # Suggest shell commands for project tasks
116. copilot -p "run only the tests in the rules directory" --allow-all
117. ```
118. 
119. ## Designing for CLI Parity
120. 
121. When adding new context to the Loan Workbench, follow this decision tree:
122. 
123. ```
124. Is this critical for ALL surfaces (VS Code, CLI, coding agent, review)?
125. ├── YES → Put it in .github/copilot-instructions.md
126. │         (keep it brief — summary + references)
127. └── NO  → Does it need path-scoped activation?
128.     ├── YES → Use .github/instructions/*.instructions.md
129.     │         (VS Code + coding agent only)
130.     └── NO  → Does it define a role or workflow?
131.         ├── YES → Use .github/agents/*.agent.md
132.         │         (VS Code Chat only)
133.         └── NO  → Put it in docs/*.md as referenceable knowledge
134.                   (VS Code via #file:, CLI via semantic search)
135. ```
136. 
137. **Rule of thumb**: If you can only put context in ONE place, put it in
138. `.github/copilot-instructions.md`. Everything else is a surface-specific
139. enhancement that improves the experience on surfaces that support it.
140. 
141. ## Limitations of CLI
142. 
143. - Single prompt → single response (use `-p` for non-interactive)
144. - No file attachment (`#file:` is VS Code Chat only)
145. - No agent invocation (`@agent` is VS Code Chat only)
146. - No prompt files (`/prompt` is VS Code Chat only)
147. - No custom instructions with path scoping
148. - No MCP tool access
149. - No pre/post-edit hooks
150. 
151. The CLI is best for:
152. 
153. - Quick code suggestions when you're already in the terminal
154. - Explaining unfamiliar code files
155. - Generating git or shell commands
156. - Verifying that your portable context (instructions) works without VS Code
157.
````

</details>


---

<sub>⏱️ 33s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\ASSESSMENT.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\ASSESSMENT.md

<details>
<summary>51 lines</summary>

````
1. # Lesson 07 CLI Prompt Assessment
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
12. Inspect the lesson's surface-strategy artifacts before answering. Discover the relevant baseline instructions, scoped instructions, agents, prompts, MCP, hooks, and docs that exist here rather than assuming a fixed file list. Then create two new files based on your analysis: 1. Create .github/instructions/portable-baseline.instructions.md containing the extracted cross-surface-portable subset of the existing instructions that works on CLI, Chat, inline completions, coding agent, and code review surfaces. Use applyTo: '**' scope. 2. Create docs/surface-portability-notes.md documenting which features are portable vs surface-specific, one concrete portability risk, one false positive, one hard negative, and recommendations for where each kind of guidance should live. Follow the discovered instruction architecture conventions. Apply the changes directly in files. Do not run shell commands and do not use SQL.
13. ```
14. 
15. The assessment run uses the model from `lessons/_common/assessment-config.json`.
16. 
17. ## Assessment Scope
18. 
19. The only question being evaluated is:
20. 
21. > Did the produced code changes implement the prompt in a way that follows the repository's surface-strategy conventions and instruction architecture?
22. 
23. ## Expected Change Artifacts
24. 
25. Assessment compares actual output against gold-standard expectations:
26. 
27. - `.output/change/expected-files.json` — expected files: `.github/instructions/portable-baseline.instructions.md` (added), `docs/surface-portability-notes.md` (added)
28. - `.output/change/expected-patterns.json` — required patterns in patch: scope, portable, CLI/surfaces, VS Code, risk taxonomy
29. 
30. The `compare_with_expected()` function writes `.output/change/comparison.md` with a structured match report.
31. 
32. ## Assessment Criteria
33. 
34. | Criterion | Source |
35. | --- | --- |
36. | Portable baseline instruction created | `expected-files.json` |
37. | Surface portability notes created | `expected-files.json` |
38. | Instruction uses cross-surface scope | `expected-patterns.json` |
39. | Content is portable across surfaces | `expected-patterns.json` |
40. | Multiple surfaces compared (CLI, VS Code) | `expected-patterns.json` |
41. | Risk taxonomy present | `expected-patterns.json` |
42. | No shell commands executed | Prompt constraint |
43. | No SQL tools used | Prompt constraint |
44. 
45. ## Captured Result
46. 
47. Pending re-run with the updated implementation-oriented prompt. Previous assessment was for a read-only surface-analysis demo that has been replaced.
48. 
49. ## Verdict
50. 
51. Pending re-run.
````

</details>


---

<sub>⏱️ 40s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy**

".github/prompts/**/*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy

```
No files matched the pattern.
```


---

<sub>⏱️ 40s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy**

".github/hooks/**/*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy

```
No files matched the pattern.
```


---

<sub>⏱️ 40s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy**

".github/skills/**/*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy

```
No files matched the pattern.
```


---

<sub>⏱️ 40s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy**

".github/*.json" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy

```
No files matched the pattern.
```


---

<sub>⏱️ 40s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy**

"**/*mcp*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy

```
No files matched the pattern.
```


---

<sub>⏱️ 40s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy**

"**/*prompt*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.output\logs\prompt.txt
```


---

<sub>⏱️ 40s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy**

"**/*hook*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy

```
No files matched the pattern.
```


---

<sub>⏱️ 52s</sub>

### 💬 Copilot

I found the core lesson artifacts and also confirmed what’s missing here: there are no prompt files, MCP config, hooks, or skills in this lesson snapshot. I’m checking the assessment-side expectations now so the added files line up with the lesson’s own architecture and vocabulary.

---

<sub>⏱️ 52s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy**

".output/change/**/*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy

```
No files matched the pattern.
```


---

<sub>⏱️ 52s</sub>

### ❌ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.output\change\expected-files.json.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.output\change\expected-files.json

```
Path does not exist
```


---

<sub>⏱️ 52s</sub>

### ❌ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.output\change\expected-patterns.json.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.output\change\expected-patterns.json

```
Path does not exist
```


---

<sub>⏱️ 1m 37s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Add File: C:\\Users\\nilay\\.copilot\\session-state\\91fc5598-5648-434f-abb8-13ff42b84815\\plan.md\n+1. Inspect discovered lesson artifacts and identify the portable baseline versus surface-specific layers.\n+2. Create a portable baseline instruction mirror using the repository's existing instruction-file conventions.\n+3. Write portability notes that document support boundaries, risks, and placement recommendations.\n+4. Review the new files for consistency with the lesson's architecture and prompt constraints.\n*** Add File: .github\\instructions\\portable-baseline.instructions.md\n+---\n+applyTo: \"**\"\n+---\n+\n+# Portable Baseline Instructions\n+\n+This file mirrors the subset of guidance from `.github/copilot-instructions.md`\n+that remains valid across CLI, Chat, inline completions, coding agent, and code\n+review surfaces.\n+\n+If this file and `.github/copilot-instructions.md` ever disagree, treat\n+`.github/copilot-instructions.md` as canonical because it is the repository-level\n+baseline instruction file.\n+\n+## Project\n+\n+Loan Workbench API is a TypeScript and Express REST service that manages loan\n+application lifecycles with regulatory compliance, role-based access, and\n+audit-first persistence.\n+\n+## Tech Stack\n+\n+- Runtime: Node.js 20 LTS\n+- Language: TypeScript 5.x in strict mode\n+- Framework: Express 4 with `better-sqlite3`\n+- Queue: in-process event broker for async side-effects\n+- Tests: Vitest, not Jest\n+- Modules: ESM only, not CommonJS\n+- Logging: structured JSON via pino\n+\n+## Architecture\n+\n+Use the established four-layer split:\n+\n+1. Routes handle HTTP concerns, parameter extraction, and delegation.\n+2. Rules contain pure business logic and do not perform I/O.\n+3. Services handle persistence, audit, and external integrations.\n+4. Queue code handles asynchronous side-effects.\n+\n+Request flow should remain: Route -> authenticate -> authorize -> validate ->\n+Rule -> Service -> respond.\n+\n+Audit events must be emitted before persistence. If audit recording fails, the\n+write must not proceed.\n+\n+## Coding Conventions\n+\n+- Prefer `const` over `let`; never use `var`.\n+- Keep route handlers `async`.\n+- Return structured JSON errors shaped like `{ error: string, code: string }`.\n+- Do not expose stack traces in error responses.\n+- Use 404 for feature-flag-disabled behavior instead of 403.\n+- Use structured logging and never `console.log()`.\n+- Keep test annotations such as `// FALSE POSITIVE` and `// HARD NEGATIVE`\n+  when the case warrants them.\n+\n+## References\n+\n+Use the existing docs for deeper detail:\n+\n+- `docs/architecture.md`\n+- `docs/api-conventions.md`\n+- `docs/adr/`\n*** Add File: docs\\surface-portability-notes.md\n+# Surface Portability Notes\n+\n+This lesson currently contains one universal baseline instruction file, one\n+path-scoped instruction file, one agent definition, and supporting lesson docs.\n+No prompt files, MCP configuration, hooks, or skills were discovered in this\n+lesson snapshot.\n+\n+## Discovered Instruction Architecture\n+\n+| Artifact | Role in this lesson | Portability |\n+| --- | --- | --- |\n+| `.github/copilot-instructions.md` | Universal baseline for project context and core conventions | Portable across CLI, Chat, inline completions, coding agent, and code review |\n+| `.github/instructions/api.instructions.md` | Path-scoped route guidance with `applyTo` | Surface-specific: VS Code and coding-agent style scoped loading |\n+| `.github/agents/reviewer.agent.md` | Reviewer role and checklist | Surface-specific: agent-enabled experiences, not universal |\n+| `docs/portability-matrix.md` | Explicit feature support matrix | Reference doc, portable as documentation rather than auto-loaded instruction |\n+| `docs/cli-guide.md` | CLI loading model and limitations | Reference doc for CLI behavior |\n+| `README.md` and `docs/surface-strategy-example.md` | Lesson goals, constraints, and expected outputs | Reference docs |\n+\n+## Portable vs Surface-Specific Features\n+\n+### Portable\n+\n+- Repository-level baseline rules in `.github/copilot-instructions.md`\n+- Deep reference material in `docs/*.md` when the surface can search or attach\n+  docs\n+- Cross-surface conventions such as ESM-only modules, Vitest, structured JSON\n+  errors, fail-closed audit ordering, and no `console.log()`\n+\n+### Surface-Specific\n+\n+- `.github/instructions/*.instructions.md` path scoping through `applyTo`\n+- `.github/agents/*.agent.md` role and tool specialization\n+- Prompt files, MCP configuration, hooks, and skills when they exist\n+\n+For this lesson, `.github/copilot-instructions.md` is the canonical source for\n+must-follow universal guidance. `docs/portability-matrix.md` is the canonical\n+reference for support boundaries because it explicitly maps features to\n+surfaces.\n+\n+## Concrete Portability Risk\n+\n+A team could place a critical route rule only in\n+`.github/instructions/api.instructions.md`, then see strong results in inline\n+completions and coding-agent flows while CLI and code review miss the rule\n+entirely. That creates inconsistent output across surfaces even though the team\n+believes the rule is \"in Copilot.\"\n+\n+## False Positive\n+\n+A reviewer might claim the CLI ignored route-template guidance because a CLI\n+response did not include the exact `authenticate -> authorize -> validate`\n+pattern from `api.instructions.md`. In this lesson that is a false positive:\n+the missing behavior is explained by surface loading limits, not by a failure to\n+follow the portable baseline.\n+\n+## Hard Negative\n+\n+Treat it as a hard negative when critical compliance or security guidance lives\n+only in a non-portable layer such as `.github/agents/reviewer.agent.md` or a\n+future prompt, MCP, or hook file. If the rule must affect CLI, inline, coding\n+agent, and code review behavior, it cannot live only in a surface-specific\n+artifact.\n+\n+## Where Each Kind of Guidance Should Live\n+\n+- Put universal, must-follow project rules in `.github/copilot-instructions.md`.\n+- Put file-pattern or subsystem-specific instructions in\n+  `.github/instructions/*.instructions.md`.\n+- Put role-based review or workflow specialization in `.github/agents/*.agent.md`.\n+- Put explanatory knowledge, rationale, and comparison tables in `docs/*.md`.\n+- Put prompts, MCP setup, and hooks only in surface-specific layers where their\n+  added power is worth the reduced portability.\n+\n+## Recommended Operating Model\n+\n+Start with the universal baseline, then add narrower layers only when the extra\n+precision is worth the portability trade-off. When artifacts disagree, keep the\n+portable rule in `.github/copilot-instructions.md` authoritative and use scoped\n+instructions, agents, and docs as layered enhancements rather than replacements.\n*** End Patch\n"
```

</details>

```
Added 3 file(s): C:\Users\nilay\.copilot\session-state\91fc5598-5648-434f-abb8-13ff42b84815\plan.md, Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.github\instructions\portable-baseline.instructions.md, Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\surface-portability-notes.md
```


---

<sub>⏱️ 1m 44s</sub>

### 💬 Copilot

The two requested files are in place. I’m doing a quick read-back now to make sure the wording stays faithful to the discovered architecture, especially the distinction between portable content and surface-specific loading.

---

<sub>⏱️ 1m 44s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.github\instructions\portable-baseline.instructions.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.github\instructions\portable-baseline.instructions.md

<details>
<summary>64 lines</summary>

```
1. ---
2. applyTo: "**"
3. ---
4. 
5. # Portable Baseline Instructions
6. 
7. This file mirrors the subset of guidance from `.github/copilot-instructions.md`
8. that remains valid across CLI, Chat, inline completions, coding agent, and code
9. review surfaces.
10. 
11. If this file and `.github/copilot-instructions.md` ever disagree, treat
12. `.github/copilot-instructions.md` as canonical because it is the repository-level
13. baseline instruction file.
14. 
15. ## Project
16. 
17. Loan Workbench API is a TypeScript and Express REST service that manages loan
18. application lifecycles with regulatory compliance, role-based access, and
19. audit-first persistence.
20. 
21. ## Tech Stack
22. 
23. - Runtime: Node.js 20 LTS
24. - Language: TypeScript 5.x in strict mode
25. - Framework: Express 4 with `better-sqlite3`
26. - Queue: in-process event broker for async side-effects
27. - Tests: Vitest, not Jest
28. - Modules: ESM only, not CommonJS
29. - Logging: structured JSON via pino
30. 
31. ## Architecture
32. 
33. Use the established four-layer split:
34. 
35. 1. Routes handle HTTP concerns, parameter extraction, and delegation.
36. 2. Rules contain pure business logic and do not perform I/O.
37. 3. Services handle persistence, audit, and external integrations.
38. 4. Queue code handles asynchronous side-effects.
39. 
40. Request flow should remain: Route -> authenticate -> authorize -> validate ->
41. Rule -> Service -> respond.
42. 
43. Audit events must be emitted before persistence. If audit recording fails, the
44. write must not proceed.
45. 
46. ## Coding Conventions
47. 
48. - Prefer `const` over `let`; never use `var`.
49. - Keep route handlers `async`.
50. - Return structured JSON errors shaped like `{ error: string, code: string }`.
51. - Do not expose stack traces in error responses.
52. - Use 404 for feature-flag-disabled behavior instead of 403.
53. - Use structured logging and never `console.log()`.
54. - Keep test annotations such as `// FALSE POSITIVE` and `// HARD NEGATIVE`
55.   when the case warrants them.
56. 
57. ## References
58. 
59. Use the existing docs for deeper detail:
60. 
61. - `docs/architecture.md`
62. - `docs/api-conventions.md`
63. - `docs/adr/`
64.
```

</details>


---

<sub>⏱️ 1m 44s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\surface-portability-notes.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\surface-portability-notes.md

<details>
<summary>80 lines</summary>

```
1. # Surface Portability Notes
2. 
3. This lesson currently contains one universal baseline instruction file, one
4. path-scoped instruction file, one agent definition, and supporting lesson docs.
5. No prompt files, MCP configuration, hooks, or skills were discovered in this
6. lesson snapshot.
7. 
8. ## Discovered Instruction Architecture
9. 
10. | Artifact | Role in this lesson | Portability |
11. | --- | --- | --- |
12. | `.github/copilot-instructions.md` | Universal baseline for project context and core conventions | Portable across CLI, Chat, inline completions, coding agent, and code review |
13. | `.github/instructions/api.instructions.md` | Path-scoped route guidance with `applyTo` | Surface-specific: VS Code and coding-agent style scoped loading |
14. | `.github/agents/reviewer.agent.md` | Reviewer role and checklist | Surface-specific: agent-enabled experiences, not universal |
15. | `docs/portability-matrix.md` | Explicit feature support matrix | Reference doc, portable as documentation rather than auto-loaded instruction |
16. | `docs/cli-guide.md` | CLI loading model and limitations | Reference doc for CLI behavior |
17. | `README.md` and `docs/surface-strategy-example.md` | Lesson goals, constraints, and expected outputs | Reference docs |
18. 
19. ## Portable vs Surface-Specific Features
20. 
21. ### Portable
22. 
23. - Repository-level baseline rules in `.github/copilot-instructions.md`
24. - Deep reference material in `docs/*.md` when the surface can search or attach
25.   docs
26. - Cross-surface conventions such as ESM-only modules, Vitest, structured JSON
27.   errors, fail-closed audit ordering, and no `console.log()`
28. 
29. ### Surface-Specific
30. 
31. - `.github/instructions/*.instructions.md` path scoping through `applyTo`
32. - `.github/agents/*.agent.md` role and tool specialization
33. - Prompt files, MCP configuration, hooks, and skills when they exist
34. 
35. For this lesson, `.github/copilot-instructions.md` is the canonical source for
36. must-follow universal guidance. `docs/portability-matrix.md` is the canonical
37. reference for support boundaries because it explicitly maps features to
38. surfaces.
39. 
40. ## Concrete Portability Risk
41. 
42. A team could place a critical route rule only in
43. `.github/instructions/api.instructions.md`, then see strong results in inline
44. completions and coding-agent flows while CLI and code review miss the rule
45. entirely. That creates inconsistent output across surfaces even though the team
46. believes the rule is "in Copilot."
47. 
48. ## False Positive
49. 
50. A reviewer might claim the CLI ignored route-template guidance because a CLI
51. response did not include the exact `authenticate -> authorize -> validate`
52. pattern from `api.instructions.md`. In this lesson that is a false positive:
53. the missing behavior is explained by surface loading limits, not by a failure to
54. follow the portable baseline.
55. 
56. ## Hard Negative
57. 
58. Treat it as a hard negative when critical compliance or security guidance lives
59. only in a non-portable layer such as `.github/agents/reviewer.agent.md` or a
60. future prompt, MCP, or hook file. If the rule must affect CLI, inline, coding
61. agent, and code review behavior, it cannot live only in a surface-specific
62. artifact.
63. 
64. ## Where Each Kind of Guidance Should Live
65. 
66. - Put universal, must-follow project rules in `.github/copilot-instructions.md`.
67. - Put file-pattern or subsystem-specific instructions in
68.   `.github/instructions/*.instructions.md`.
69. - Put role-based review or workflow specialization in `.github/agents/*.agent.md`.
70. - Put explanatory knowledge, rationale, and comparison tables in `docs/*.md`.
71. - Put prompts, MCP setup, and hooks only in surface-specific layers where their
72.   added power is worth the reduced portability.
73. 
74. ## Recommended Operating Model
75. 
76. Start with the universal baseline, then add narrower layers only when the extra
77. precision is worth the portability trade-off. When artifacts disagree, keep the
78. portable rule in `.github/copilot-instructions.md` authoritative and use scoped
79. instructions, agents, and docs as layered enhancements rather than replacements.
80.
```

</details>


---

<sub>⏱️ 1m 44s</sub>

### ✅ `view`

**view the file at C:\Users\nilay\.copilot\session-state\91fc5598-5648-434f-abb8-13ff42b84815\plan.md.**

C:\Users\nilay\.copilot\session-state\91fc5598-5648-434f-abb8-13ff42b84815\plan.md

```
1. 1. Inspect discovered lesson artifacts and identify the portable baseline versus surface-specific layers.
2. 2. Create a portable baseline instruction mirror using the repository's existing instruction-file conventions.
3. 3. Write portability notes that document support boundaries, risks, and placement recommendations.
4. 4. Review the new files for consistency with the lesson's architecture and prompt constraints.
5. 
```


---

<sub>⏱️ 1m 58s</sub>

### 💬 Copilot

I’ve got the core content right, but I want the notes to be more explicit about the five surfaces the lesson cares about. I’m tightening that doc with a direct surface comparison table so it’s easier to audit against the prompt and the lesson examples.

---

<sub>⏱️ 1m 58s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Update File: docs\\surface-portability-notes.md\n@@\n ## Discovered Instruction Architecture\n@@\n | `docs/cli-guide.md` | CLI loading model and limitations | Reference doc for CLI behavior |\n | `README.md` and `docs/surface-strategy-example.md` | Lesson goals, constraints, and expected outputs | Reference docs |\n \n+## Surface Comparison\n+\n+| Surface | Universal baseline | Scoped instructions | Agents | Docs |\n+| --- | --- | --- | --- | --- |\n+| VS Code Chat | Uses `.github/copilot-instructions.md` | Can use `applyTo`-scoped instruction files when relevant | Can use agent definitions | Can read lesson docs directly |\n+| VS Code Inline | Uses `.github/copilot-instructions.md` | Best surface for `applyTo`-scoped instruction files | Does not use agents | May benefit from nearby file context, not full doc workflows |\n+| GitHub CLI | Uses `.github/copilot-instructions.md` | Does not load `.github/instructions/*.instructions.md` | Does not load agents | Relies on discovery or indexed docs rather than auto-loading |\n+| Coding Agent | Uses `.github/copilot-instructions.md` | Can use scoped instruction files | Can use agent-oriented layers | Can use docs as supporting context |\n+| Code Review | Uses `.github/copilot-instructions.md` | Should not rely on scoped instruction files | Should not rely on agents | May use docs as reference, but not as guaranteed baseline |\n+\n ## Portable vs Surface-Specific Features\n*** End Patch\n"
```

</details>

```
Modified 1 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\surface-portability-notes.md
```


---

<sub>⏱️ 2m 3s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\surface-portability-notes.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\surface-portability-notes.md (lines 1-120)

<details>
<summary>89 lines</summary>

```
1. # Surface Portability Notes
2. 
3. This lesson currently contains one universal baseline instruction file, one
4. path-scoped instruction file, one agent definition, and supporting lesson docs.
5. No prompt files, MCP configuration, hooks, or skills were discovered in this
6. lesson snapshot.
7. 
8. ## Discovered Instruction Architecture
9. 
10. | Artifact | Role in this lesson | Portability |
11. | --- | --- | --- |
12. | `.github/copilot-instructions.md` | Universal baseline for project context and core conventions | Portable across CLI, Chat, inline completions, coding agent, and code review |
13. | `.github/instructions/api.instructions.md` | Path-scoped route guidance with `applyTo` | Surface-specific: VS Code and coding-agent style scoped loading |
14. | `.github/agents/reviewer.agent.md` | Reviewer role and checklist | Surface-specific: agent-enabled experiences, not universal |
15. | `docs/portability-matrix.md` | Explicit feature support matrix | Reference doc, portable as documentation rather than auto-loaded instruction |
16. | `docs/cli-guide.md` | CLI loading model and limitations | Reference doc for CLI behavior |
17. | `README.md` and `docs/surface-strategy-example.md` | Lesson goals, constraints, and expected outputs | Reference docs |
18. 
19. ## Surface Comparison
20. 
21. | Surface | Universal baseline | Scoped instructions | Agents | Docs |
22. | --- | --- | --- | --- | --- |
23. | VS Code Chat | Uses `.github/copilot-instructions.md` | Can use `applyTo`-scoped instruction files when relevant | Can use agent definitions | Can read lesson docs directly |
24. | VS Code Inline | Uses `.github/copilot-instructions.md` | Best surface for `applyTo`-scoped instruction files | Does not use agents | May benefit from nearby file context, not full doc workflows |
25. | GitHub CLI | Uses `.github/copilot-instructions.md` | Does not load `.github/instructions/*.instructions.md` | Does not load agents | Relies on discovery or indexed docs rather than auto-loading |
26. | Coding Agent | Uses `.github/copilot-instructions.md` | Can use scoped instruction files | Can use agent-oriented layers | Can use docs as supporting context |
27. | Code Review | Uses `.github/copilot-instructions.md` | Should not rely on scoped instruction files | Should not rely on agents | May use docs as reference, but not as guaranteed baseline |
28. 
29. ## Portable vs Surface-Specific Features
30. 
31. ### Portable
32. 
33. - Repository-level baseline rules in `.github/copilot-instructions.md`
34. - Deep reference material in `docs/*.md` when the surface can search or attach
35.   docs
36. - Cross-surface conventions such as ESM-only modules, Vitest, structured JSON
37.   errors, fail-closed audit ordering, and no `console.log()`
38. 
39. ### Surface-Specific
40. 
41. - `.github/instructions/*.instructions.md` path scoping through `applyTo`
42. - `.github/agents/*.agent.md` role and tool specialization
43. - Prompt files, MCP configuration, hooks, and skills when they exist
44. 
45. For this lesson, `.github/copilot-instructions.md` is the canonical source for
46. must-follow universal guidance. `docs/portability-matrix.md` is the canonical
47. reference for support boundaries because it explicitly maps features to
48. surfaces.
49. 
50. ## Concrete Portability Risk
51. 
52. A team could place a critical route rule only in
53. `.github/instructions/api.instructions.md`, then see strong results in inline
54. completions and coding-agent flows while CLI and code review miss the rule
55. entirely. That creates inconsistent output across surfaces even though the team
56. believes the rule is "in Copilot."
57. 
58. ## False Positive
59. 
60. A reviewer might claim the CLI ignored route-template guidance because a CLI
61. response did not include the exact `authenticate -> authorize -> validate`
62. pattern from `api.instructions.md`. In this lesson that is a false positive:
63. the missing behavior is explained by surface loading limits, not by a failure to
64. follow the portable baseline.
65. 
66. ## Hard Negative
67. 
68. Treat it as a hard negative when critical compliance or security guidance lives
69. only in a non-portable layer such as `.github/agents/reviewer.agent.md` or a
70. future prompt, MCP, or hook file. If the rule must affect CLI, inline, coding
71. agent, and code review behavior, it cannot live only in a surface-specific
72. artifact.
73. 
74. ## Where Each Kind of Guidance Should Live
75. 
76. - Put universal, must-follow project rules in `.github/copilot-instructions.md`.
77. - Put file-pattern or subsystem-specific instructions in
78.   `.github/instructions/*.instructions.md`.
79. - Put role-based review or workflow specialization in `.github/agents/*.agent.md`.
80. - Put explanatory knowledge, rationale, and comparison tables in `docs/*.md`.
81. - Put prompts, MCP setup, and hooks only in surface-specific layers where their
82.   added power is worth the reduced portability.
83. 
84. ## Recommended Operating Model
85. 
86. Start with the universal baseline, then add narrower layers only when the extra
87. precision is worth the portability trade-off. When artifacts disagree, keep the
88. portable rule in `.github/copilot-instructions.md` authoritative and use scoped
89. instructions, agents, and docs as layered enhancements rather than replacements.
```

</details>


---

<sub>⏱️ 2m 3s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.github\instructions\portable-baseline.instructions.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.github\instructions\portable-baseline.instructions.md (lines 1-120)

<details>
<summary>63 lines</summary>

```
1. ---
2. applyTo: "**"
3. ---
4. 
5. # Portable Baseline Instructions
6. 
7. This file mirrors the subset of guidance from `.github/copilot-instructions.md`
8. that remains valid across CLI, Chat, inline completions, coding agent, and code
9. review surfaces.
10. 
11. If this file and `.github/copilot-instructions.md` ever disagree, treat
12. `.github/copilot-instructions.md` as canonical because it is the repository-level
13. baseline instruction file.
14. 
15. ## Project
16. 
17. Loan Workbench API is a TypeScript and Express REST service that manages loan
18. application lifecycles with regulatory compliance, role-based access, and
19. audit-first persistence.
20. 
21. ## Tech Stack
22. 
23. - Runtime: Node.js 20 LTS
24. - Language: TypeScript 5.x in strict mode
25. - Framework: Express 4 with `better-sqlite3`
26. - Queue: in-process event broker for async side-effects
27. - Tests: Vitest, not Jest
28. - Modules: ESM only, not CommonJS
29. - Logging: structured JSON via pino
30. 
31. ## Architecture
32. 
33. Use the established four-layer split:
34. 
35. 1. Routes handle HTTP concerns, parameter extraction, and delegation.
36. 2. Rules contain pure business logic and do not perform I/O.
37. 3. Services handle persistence, audit, and external integrations.
38. 4. Queue code handles asynchronous side-effects.
39. 
40. Request flow should remain: Route -> authenticate -> authorize -> validate ->
41. Rule -> Service -> respond.
42. 
43. Audit events must be emitted before persistence. If audit recording fails, the
44. write must not proceed.
45. 
46. ## Coding Conventions
47. 
48. - Prefer `const` over `let`; never use `var`.
49. - Keep route handlers `async`.
50. - Return structured JSON errors shaped like `{ error: string, code: string }`.
51. - Do not expose stack traces in error responses.
52. - Use 404 for feature-flag-disabled behavior instead of 403.
53. - Use structured logging and never `console.log()`.
54. - Keep test annotations such as `// FALSE POSITIVE` and `// HARD NEGATIVE`
55.   when the case warrants them.
56. 
57. ## References
58. 
59. Use the existing docs for deeper detail:
60. 
61. - `docs/architecture.md`
62. - `docs/api-conventions.md`
63. - `docs/adr/`
```

</details>


---

<sub>⏱️ 2m 7s</sub>

### 💬 Copilot

Done — I inspected the lesson’s actual artifacts first, confirmed the current architecture (`.github/copilot-instructions.md`, `.github/instructions/api.instructions.md`, `.github/agents/reviewer.agent.md`, and the docs), and also confirmed there are no prompt, MCP, hook, or skill files in this lesson snapshot.

I added `.github/instructions/portable-baseline.instructions.md` as an `applyTo: "**"` portable-content mirror of the universal baseline, and `docs/surface-portability-notes.md` with explicit surface comparisons, portable vs surface-specific guidance, one portability risk, one false positive, one hard negative, and placement recommendations. I used `apply_patch` only—no shell commands or SQL.

---

<sub>Generated by [GitHub Copilot CLI](https://github.com/features/copilot/cli)</sub>
