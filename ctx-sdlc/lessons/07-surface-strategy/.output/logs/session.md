# 🤖 Copilot CLI Session

> [!NOTE]
> - **Session ID:** `b5e6470b-0e11-4a17-a3d3-f8859a8d4e54`  
> - **Started:** 14/03/2026, 17:09:21  
> - **Duration:** 1m 53s  
> - **Exported:** 14/03/2026, 17:11:14  

---

<sub>⏱️ 5s</sub>

### 👤 User

Inspect the lesson's surface-strategy artifacts before answering. Discover the relevant baseline instructions, scoped instructions, agents, prompts, MCP, hooks, and docs that exist here rather than assuming a fixed file list. Then create two new files based on your analysis: 1. Create .github/instructions/portable-baseline.instructions.md containing the extracted cross-surface-portable subset of the existing instructions that works on CLI, Chat, inline completions, coding agent, and code review surfaces. Use applyTo: '**' scope. 2. Create docs/surface-portability-notes.md documenting which features are portable vs surface-specific, one concrete portability risk, one false positive, one hard negative, and recommendations for where each kind of guidance should live. Follow the discovered instruction architecture conventions. Apply the changes directly in files. Do not run shell commands and do not use SQL.

---

<sub>⏱️ 19s</sub>

### 💬 Copilot

I’m mapping the lesson’s actual instruction surfaces first so the new files match what’s already here, not a guessed structure. After that I’ll extract the portable subset and write the portability notes in place.

---

<sub>⏱️ 19s</sub>

### ✅ `glob`

**.github/**/***

".github/**/*"

```
.\.github\copilot-instructions.md
.\.github\agents\reviewer.agent.md
.\.github\instructions\api.instructions.md
```


---

<sub>⏱️ 19s</sub>

### ✅ `glob`

**docs/**/***

"docs/**/*"

```
.\docs\surface-strategy-example.md
.\docs\portability-matrix.md
.\docs\cli-guide.md
```


---

<sub>⏱️ 19s</sub>

### ✅ `glob`

****/*.md**

"**/*.md"

<details>
<summary>8 matches</summary>

```
.\README.md
.\ASSESSMENT.md
.\docs\portability-matrix.md
.\docs\cli-guide.md
.\docs\surface-strategy-example.md
.\.github\instructions\api.instructions.md
.\.github\copilot-instructions.md
.\.github\agents\reviewer.agent.md
```

</details>


---

<sub>⏱️ 19s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "applyTo:|copilot|prompt|agent|mcp|hook|instruction",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\07-surface-strategy",
  "output_mode": "content",
  "glob": "*.{md,json,yml,yaml}",
  "-n": true,
  "head_limit": 300
}
```

</details>

```
Output too large to read at once (20.4 KB). Saved to: C:\Users\nilay\AppData\Local\Temp\copilot-tool-output-1773508181204-z851ju.txt
Consider using tools like grep (for searching), head/tail (for viewing start/end), view with view_range (for specific sections), or jq (for JSON) to examine portions of the output.

Preview (first 500 chars):
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\README.md:19:| Agent 
```


---

<sub>⏱️ 28s</sub>

### 💬 Copilot

I found the lesson’s actual surfaces: baseline instructions, a scoped instruction, an agent file, and supporting docs. Next I’m reading those directly to extract only the genuinely portable subset and mirror the lesson’s architecture.

---

<sub>⏱️ 28s</sub>

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

<sub>⏱️ 28s</sub>

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

<sub>⏱️ 28s</sub>

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

<sub>⏱️ 28s</sub>

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

<sub>⏱️ 28s</sub>

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

<sub>⏱️ 28s</sub>

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

<sub>⏱️ 28s</sub>

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

<sub>⏱️ 37s</sub>

### 💬 Copilot

I’ve confirmed there are no prompt, MCP, or hook artifacts in this lesson folder—only the baseline instruction, one scoped instruction, one agent, and the docs. I’m doing one last read of the assessment target so the new files line up with the lesson’s expected shape before I write them.

---

<sub>⏱️ 37s</sub>

### ✅ `glob`

**.github/prompts/**/***

".github/prompts/**/*"

```
No files matched the pattern.
```


---

<sub>⏱️ 37s</sub>

### ✅ `glob`

**.github/hooks/**/***

".github/hooks/**/*"

```
No files matched the pattern.
```


---

<sub>⏱️ 37s</sub>

### ✅ `glob`

**.github/mcp***

".github/mcp*"

```
No files matched the pattern.
```


---

<sub>⏱️ 37s</sub>

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

<sub>⏱️ 1m 39s</sub>

### 💬 Copilot

I’ve got enough context now: the portable baseline should come from `.github/copilot-instructions.md`, not from the route-only or agent-only layers. I’m writing the new instruction file plus the notes doc, and I’m also leaving a small session plan artifact as required by the workspace conventions.

---

<sub>⏱️ 1m 39s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Add File: C:/Users/nilay/.copilot/session-state/b5e6470b-0e11-4a17-a3d3-f8859a8d4e54/plan.md\n+# Plan\n+\n+1. Inspect the lesson's actual surface-strategy artifacts and identify what exists here versus what is absent.\n+2. Extract only the cross-surface-portable guidance from the existing baseline instructions into a new all-files scoped instruction file.\n+3. Document portability behavior, risks, false positives, hard negatives, and placement recommendations in a new docs note that follows the lesson's instruction architecture.\n*** Add File: .github/instructions/portable-baseline.instructions.md\n+---\n+applyTo: \"**\"\n+---\n+\n+# Portable Baseline Instructions\n+\n+This file mirrors the cross-surface-portable subset of the lesson's existing\n+baseline guidance.\n+\n+Use `.github/copilot-instructions.md` as the canonical universal baseline,\n+because that repository-level file is the artifact explicitly designed to load\n+across CLI, Chat, inline completions, coding agent, and code review surfaces.\n+Keep narrower or stronger rules in scoped instructions, agents, or docs.\n+\n+## Project\n+\n+Loan Workbench API — TypeScript + Express REST service managing loan\n+application lifecycles with regulatory compliance (California SMS restriction),\n+role-based access, and audit-first persistence.\n+\n+## Tech Stack\n+\n+- Runtime: Node.js 20 LTS\n+- Language: TypeScript 5.x (strict mode)\n+- Framework: Express 4 with better-sqlite3 for persistence\n+- Queue: in-process event broker for async side-effects\n+- Tests: Vitest, not Jest\n+- Modules: ESM only, not CommonJS\n+- Logging: structured JSON via pino\n+\n+## Architecture\n+\n+Preserve the four-layer separation:\n+\n+1. Routes handle HTTP concerns and delegation.\n+2. Rules contain pure business logic with no I/O.\n+3. Services handle persistence and external integrations.\n+4. Queue handles async side-effects.\n+\n+Follow this request flow:\n+\n+Route -> authenticate -> authorize -> validate -> Rule -> Service -> respond.\n+\n+Audit events must be emitted before persistence. If audit recording fails, the\n+write must not proceed.\n+\n+## Cross-Surface Conventions\n+\n+- Prefer `const` over `let`; never use `var`.\n+- Keep route handlers `async`.\n+- Return structured JSON errors shaped as `{ error: string, code: string }`.\n+- Do not return stack traces in error responses.\n+- Treat disabled features as 404, not 403.\n+- Use structured logging; do not use `console.log()`.\n+- When applicable, annotate tests with `// FALSE POSITIVE` or\n+  `// HARD NEGATIVE`.\n+\n+## References\n+\n+- `/docs/architecture.md`\n+- `/docs/api-conventions.md`\n+- `/docs/adr/`\n*** Add File: docs/surface-portability-notes.md\n+# Surface Portability Notes\n+\n+This lesson currently contains these relevant surface-strategy artifacts:\n+\n+- `.github/copilot-instructions.md` — universal baseline instructions\n+- `.github/instructions/api.instructions.md` — path-scoped route rules\n+- `.github/agents/reviewer.agent.md` — reviewer role and checklist\n+- `docs/cli-guide.md` — CLI behavior and usage notes\n+- `docs/portability-matrix.md` — surface compatibility reference\n+- `docs/surface-strategy-example.md` — lesson-specific target and constraints\n+\n+No prompt files, MCP configuration, or hook artifacts are present in this\n+lesson directory today, so portability analysis here is based on the baseline\n+instruction, the scoped instruction, the agent, and the docs.\n+\n+## Portable vs Surface-Specific\n+\n+| Artifact or feature | Present here | Portability | Notes |\n+| --- | --- | --- | --- |\n+| `.github/copilot-instructions.md` | Yes | Portable | This is the universal baseline and the only lesson artifact explicitly positioned to work across CLI, Chat, inline completions, coding agent, and code review. |\n+| `.github/instructions/*.instructions.md` with `applyTo` | Yes | Surface-specific | Useful for scoped activation in supported editors and coding agent flows, but not a reliable cross-surface baseline. |\n+| `.github/agents/*.agent.md` | Yes | Surface-specific | Agent files define a role and checklist, but they are not a portable foundation. |\n+| `docs/*.md` reference docs | Yes | Partially portable | Helpful as discoverable knowledge, but not guaranteed to auto-load on every surface. |\n+| Prompt files | No | Surface-specific | Not present here; if added later, they should be treated as workflow helpers rather than universal guidance. |\n+| MCP configuration | No | Surface-specific | Not present here; if added later, it should be treated as a tool availability layer, not baseline policy. |\n+| Hooks | No | Surface-specific | Not present here; if added later, they would enforce editor-side behavior rather than provide portable context. |\n+\n+## Canonical Baseline\n+\n+Treat `.github/copilot-instructions.md` as the canonical cross-surface\n+instruction source for this lesson.\n+\n+That conclusion is supported by multiple lesson artifacts:\n+\n+- `README.md` labels it the \"Universal baseline\".\n+- `docs/cli-guide.md` says it is the only context file guaranteed to load in\n+  the CLI.\n+- `docs/portability-matrix.md` places it at the base of the portability\n+  pyramid.\n+\n+There is one lesson-level disagreement about agent portability. The portability\n+matrix says `.agent.md` is available in VS Code Chat and coding agent, while\n+`README.md` and the note inside `reviewer.agent.md` speak more narrowly about\n+VS Code Chat usage. For portability decisions, `docs/portability-matrix.md`\n+should be treated as canonical because it is the dedicated compatibility\n+reference, while the README and agent note are explanatory summaries.\n+\n+## Why the New Portable Baseline Is Smaller\n+\n+The route template in `.github/instructions/api.instructions.md` is stronger\n+than the portable baseline, but it is intentionally scoped to\n+`app/backend/src/routes/**`.\n+\n+The reviewer checklist in `.github/agents/reviewer.agent.md` is also stronger,\n+but it depends on agent-style role framing and tool assumptions.\n+\n+For that reason, the extracted portable baseline should keep only guidance that\n+still makes sense everywhere:\n+\n+- project and stack identity\n+- architecture boundaries\n+- fail-closed audit ordering\n+- universal coding conventions\n+- error-shape and logging rules\n+\n+It should not copy route-only templates or agent-only review workflow details\n+into the universal layer.\n+\n+## Portability Risk Taxonomy\n+\n+### Concrete portability risk\n+\n+A team could place the route error-handling requirements only in\n+`.github/instructions/api.instructions.md` and assume CLI or code review will\n+enforce them. That creates inconsistent behavior because surfaces that do not\n+load scoped instructions may still generate code, comments, or review output\n+without the same guarantees.\n+\n+### False positive\n+\n+A developer may notice that the CLI did not apply the reviewer checklist and\n+conclude that the repository baseline is broken. In this lesson, that is a\n+false positive: the missing checklist can be caused by the CLI not loading the\n+agent layer, not by missing or incorrect universal instructions.\n+\n+### Hard negative\n+\n+Putting a must-follow universal rule such as \"no stack traces in error\n+responses\" only in an agent file or only in a path-scoped instruction is a hard\n+negative. That guidance becomes unavailable on surfaces that do not support the\n+chosen layer, so the most critical rule is absent exactly where portability was\n+required.\n+\n+## Recommendations\n+\n+Put universal project identity, architecture boundaries, security rules, error\n+shape requirements, and logging conventions in\n+`.github/copilot-instructions.md`.\n+\n+Put file-pattern-specific implementation guidance in\n+`.github/instructions/*.instructions.md`. In this lesson, the route handler\n+template belongs there, not in the portable baseline.\n+\n+Put role-based review behavior, checklists, and tool-constrained workflows in\n+`.github/agents/*.agent.md`.\n+\n+Put explanatory reference material, rationale, examples, and compatibility\n+tables in `docs/*.md`.\n+\n+If prompt files, MCP, or hooks are added later, treat them as surface-specific\n+enhancement layers. They can improve supported surfaces, but they should not be\n+the only home for guidance that the whole team depends on.\n*** End Patch\n"
```

</details>

```
Added 3 file(s): C:\Users\nilay\.copilot\session-state\b5e6470b-0e11-4a17-a3d3-f8859a8d4e54\plan.md, Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.github\instructions\portable-baseline.instructions.md, Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\surface-portability-notes.md
```


---

<sub>⏱️ 1m 45s</sub>

### 💬 Copilot

The files are written. I’m doing a quick read-back now to verify they match the discovered lesson architecture and that I didn’t accidentally pull route-only or agent-only guidance into the portable subset.

---

<sub>⏱️ 1m 45s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.github\instructions\portable-baseline.instructions.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\.github\instructions\portable-baseline.instructions.md

<details>
<summary>63 lines</summary>

```
1. ---
2. applyTo: "**"
3. ---
4. 
5. # Portable Baseline Instructions
6. 
7. This file mirrors the cross-surface-portable subset of the lesson's existing
8. baseline guidance.
9. 
10. Use `.github/copilot-instructions.md` as the canonical universal baseline,
11. because that repository-level file is the artifact explicitly designed to load
12. across CLI, Chat, inline completions, coding agent, and code review surfaces.
13. Keep narrower or stronger rules in scoped instructions, agents, or docs.
14. 
15. ## Project
16. 
17. Loan Workbench API — TypeScript + Express REST service managing loan
18. application lifecycles with regulatory compliance (California SMS restriction),
19. role-based access, and audit-first persistence.
20. 
21. ## Tech Stack
22. 
23. - Runtime: Node.js 20 LTS
24. - Language: TypeScript 5.x (strict mode)
25. - Framework: Express 4 with better-sqlite3 for persistence
26. - Queue: in-process event broker for async side-effects
27. - Tests: Vitest, not Jest
28. - Modules: ESM only, not CommonJS
29. - Logging: structured JSON via pino
30. 
31. ## Architecture
32. 
33. Preserve the four-layer separation:
34. 
35. 1. Routes handle HTTP concerns and delegation.
36. 2. Rules contain pure business logic with no I/O.
37. 3. Services handle persistence and external integrations.
38. 4. Queue handles async side-effects.
39. 
40. Follow this request flow:
41. 
42. Route -> authenticate -> authorize -> validate -> Rule -> Service -> respond.
43. 
44. Audit events must be emitted before persistence. If audit recording fails, the
45. write must not proceed.
46. 
47. ## Cross-Surface Conventions
48. 
49. - Prefer `const` over `let`; never use `var`.
50. - Keep route handlers `async`.
51. - Return structured JSON errors shaped as `{ error: string, code: string }`.
52. - Do not return stack traces in error responses.
53. - Treat disabled features as 404, not 403.
54. - Use structured logging; do not use `console.log()`.
55. - When applicable, annotate tests with `// FALSE POSITIVE` or
56.   `// HARD NEGATIVE`.
57. 
58. ## References
59. 
60. - `/docs/architecture.md`
61. - `/docs/api-conventions.md`
62. - `/docs/adr/`
63.
```

</details>


---

<sub>⏱️ 1m 45s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\surface-portability-notes.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\07-surface-strategy\docs\surface-portability-notes.md

<details>
<summary>113 lines</summary>

```
1. # Surface Portability Notes
2. 
3. This lesson currently contains these relevant surface-strategy artifacts:
4. 
5. - `.github/copilot-instructions.md` — universal baseline instructions
6. - `.github/instructions/api.instructions.md` — path-scoped route rules
7. - `.github/agents/reviewer.agent.md` — reviewer role and checklist
8. - `docs/cli-guide.md` — CLI behavior and usage notes
9. - `docs/portability-matrix.md` — surface compatibility reference
10. - `docs/surface-strategy-example.md` — lesson-specific target and constraints
11. 
12. No prompt files, MCP configuration, or hook artifacts are present in this
13. lesson directory today, so portability analysis here is based on the baseline
14. instruction, the scoped instruction, the agent, and the docs.
15. 
16. ## Portable vs Surface-Specific
17. 
18. | Artifact or feature | Present here | Portability | Notes |
19. | --- | --- | --- | --- |
20. | `.github/copilot-instructions.md` | Yes | Portable | This is the universal baseline and the only lesson artifact explicitly positioned to work across CLI, Chat, inline completions, coding agent, and code review. |
21. | `.github/instructions/*.instructions.md` with `applyTo` | Yes | Surface-specific | Useful for scoped activation in supported editors and coding agent flows, but not a reliable cross-surface baseline. |
22. | `.github/agents/*.agent.md` | Yes | Surface-specific | Agent files define a role and checklist, but they are not a portable foundation. |
23. | `docs/*.md` reference docs | Yes | Partially portable | Helpful as discoverable knowledge, but not guaranteed to auto-load on every surface. |
24. | Prompt files | No | Surface-specific | Not present here; if added later, they should be treated as workflow helpers rather than universal guidance. |
25. | MCP configuration | No | Surface-specific | Not present here; if added later, it should be treated as a tool availability layer, not baseline policy. |
26. | Hooks | No | Surface-specific | Not present here; if added later, they would enforce editor-side behavior rather than provide portable context. |
27. 
28. ## Canonical Baseline
29. 
30. Treat `.github/copilot-instructions.md` as the canonical cross-surface
31. instruction source for this lesson.
32. 
33. That conclusion is supported by multiple lesson artifacts:
34. 
35. - `README.md` labels it the "Universal baseline".
36. - `docs/cli-guide.md` says it is the only context file guaranteed to load in
37.   the CLI.
38. - `docs/portability-matrix.md` places it at the base of the portability
39.   pyramid.
40. 
41. There is one lesson-level disagreement about agent portability. The portability
42. matrix says `.agent.md` is available in VS Code Chat and coding agent, while
43. `README.md` and the note inside `reviewer.agent.md` speak more narrowly about
44. VS Code Chat usage. For portability decisions, `docs/portability-matrix.md`
45. should be treated as canonical because it is the dedicated compatibility
46. reference, while the README and agent note are explanatory summaries.
47. 
48. ## Why the New Portable Baseline Is Smaller
49. 
50. The route template in `.github/instructions/api.instructions.md` is stronger
51. than the portable baseline, but it is intentionally scoped to
52. `app/backend/src/routes/**`.
53. 
54. The reviewer checklist in `.github/agents/reviewer.agent.md` is also stronger,
55. but it depends on agent-style role framing and tool assumptions.
56. 
57. For that reason, the extracted portable baseline should keep only guidance that
58. still makes sense everywhere:
59. 
60. - project and stack identity
61. - architecture boundaries
62. - fail-closed audit ordering
63. - universal coding conventions
64. - error-shape and logging rules
65. 
66. It should not copy route-only templates or agent-only review workflow details
67. into the universal layer.
68. 
69. ## Portability Risk Taxonomy
70. 
71. ### Concrete portability risk
72. 
73. A team could place the route error-handling requirements only in
74. `.github/instructions/api.instructions.md` and assume CLI or code review will
75. enforce them. That creates inconsistent behavior because surfaces that do not
76. load scoped instructions may still generate code, comments, or review output
77. without the same guarantees.
78. 
79. ### False positive
80. 
81. A developer may notice that the CLI did not apply the reviewer checklist and
82. conclude that the repository baseline is broken. In this lesson, that is a
83. false positive: the missing checklist can be caused by the CLI not loading the
84. agent layer, not by missing or incorrect universal instructions.
85. 
86. ### Hard negative
87. 
88. Putting a must-follow universal rule such as "no stack traces in error
89. responses" only in an agent file or only in a path-scoped instruction is a hard
90. negative. That guidance becomes unavailable on surfaces that do not support the
91. chosen layer, so the most critical rule is absent exactly where portability was
92. required.
93. 
94. ## Recommendations
95. 
96. Put universal project identity, architecture boundaries, security rules, error
97. shape requirements, and logging conventions in
98. `.github/copilot-instructions.md`.
99. 
100. Put file-pattern-specific implementation guidance in
101. `.github/instructions/*.instructions.md`. In this lesson, the route handler
102. template belongs there, not in the portable baseline.
103. 
104. Put role-based review behavior, checklists, and tool-constrained workflows in
105. `.github/agents/*.agent.md`.
106. 
107. Put explanatory reference material, rationale, examples, and compatibility
108. tables in `docs/*.md`.
109. 
110. If prompt files, MCP, or hooks are added later, treat them as surface-specific
111. enhancement layers. They can improve supported surfaces, but they should not be
112. the only home for guidance that the whole team depends on.
113.
```

</details>


---

<sub>⏱️ 1m 53s</sub>

### 💬 Copilot

Done — I added both requested files and kept them aligned with the lesson’s discovered instruction architecture.

Created `.github/instructions/portable-baseline.instructions.md` with `applyTo: "**"` and only the cross-surface subset extracted from the existing universal baseline: project identity, stack, architecture boundaries, fail-closed audit ordering, and universal conventions.

Created `docs/surface-portability-notes.md` documenting the artifacts actually present here, portable vs surface-specific layers, the canonical-source decision, one portability risk, one false positive, one hard negative, and guidance on where each type of instruction should live.

I did not use shell commands or SQL.

---

<sub>Generated by [GitHub Copilot CLI](https://github.com/features/copilot/cli)</sub>
