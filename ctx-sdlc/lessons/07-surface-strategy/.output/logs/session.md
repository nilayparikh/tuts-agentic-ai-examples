# 🤖 Copilot CLI Session

> [!NOTE]
> - **Session ID:** `655e9746-0a86-4e72-99fb-891fa689eb9a`  
> - **Started:** 13/03/2026, 23:45:13  
> - **Duration:** 38s  
> - **Exported:** 13/03/2026, 23:45:51  

---

<sub>⏱️ 6s</sub>

### 👤 User

Read .github/copilot-instructions.md, .github/instructions/api.instructions.md, .github/agents/reviewer.agent.md, docs/cli-guide.md, and docs/portability-matrix.md. Produce a read-only surface-strategy analysis for this lesson. Return: summary, what is portable across all surfaces, what is VS Code-only, one concrete portability risk, one false positive, one hard negative, and prioritized recommendations for where each kind of guidance should live. Explicitly compare CLI, VS Code Chat, inline completions, coding agent, and code review surfaces, and call out path-scoped instructions, agents, prompts, MCP, hooks, and docs separately. Do not modify files, do not run shell commands, and do not use SQL or any other write-capable tools. Inspect and read only.

---

<sub>⏱️ 18s</sub>

### 💬 Copilot

I’m reading the requested guidance files now and will synthesize a surface-by-surface portability analysis without making any changes.

---

<sub>⏱️ 18s</sub>

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

<sub>⏱️ 18s</sub>

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

<sub>⏱️ 18s</sub>

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

<sub>⏱️ 18s</sub>

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

<sub>⏱️ 18s</sub>

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

<sub>⏱️ 38s</sub>

### 💬 Copilot

## Summary

This lesson’s core portability point is correct: `.github/copilot-instructions.md` is the only **guaranteed cross-surface foundation**. Everything else is a narrower enhancement layer. The main inconsistency is that `.github/agents/reviewer.agent.md` says agents are **VS Code Chat only**, while `docs/portability-matrix.md` says agents also work in **Coding Agent**.

## Surface comparison

| Surface | Guaranteed context |
|---|---|
| CLI | `.github/copilot-instructions.md`; `docs/*.md` only partial via search/indexing |
| VS Code Chat | `copilot-instructions`, path-scoped instructions, agents, prompts, MCP, hooks, docs, attachments |
| Inline completions | `copilot-instructions`, path-scoped instructions, partial docs; no agents/prompts/MCP/hooks |
| Coding Agent | `copilot-instructions`, path-scoped instructions, prompts, MCP, docs, attachments; matrix says agents too |
| Code Review | `copilot-instructions` guaranteed; docs partial; no path-scoped instructions/agents/prompts/MCP/hooks |

## Portable across all surfaces

- `.github/copilot-instructions.md`
- High-level architecture, conventions, and “always true” rules placed there
- Docs only as **partial/discoverable reference**, not guaranteed auto-context

## VS Code-only

- Path-scoped `.instructions.md` behavior is effectively VS Code-family only
- Hooks are VS Code-only
- `#file:` attachment is VS Code Chat + Coding Agent, not CLI/review
- Inline only gets a subset of VS Code capabilities

## One concrete portability risk

`reviewer.agent.md` conflicts with the matrix on Coding Agent support. Teams may place review guidance in an agent and assume Coding Agent will always use it, but the lesson materials disagree.

## One false positive

Assuming `reviewer.agent.md` improves the **Code Review** surface because it is a “reviewer” artifact. The file itself says it is not available there.

## One hard negative

Assuming `.github/instructions/api.instructions.md` will affect **CLI** behavior. It explicitly will not.

## Prioritized recommendations

1. Put **must-never-break, all-surface rules** in `.github/copilot-instructions.md`.
2. Put **path-specific implementation rules** in `.github/instructions/*.instructions.md`.
3. Put **deep reference knowledge** in `docs/*.md`.
4. Put **repeatable workflows** in `.prompt.md`.
5. Put **role/tool-constrained behavior** in `.agent.md`, but do not rely on it for portability.
6. Put **tool access** in MCP config only for VS Code/Coding Agent scenarios.
7. Put **automatic enforcement** in hooks, never as the only source of critical guidance.

---

<sub>Generated by [GitHub Copilot CLI](https://github.com/features/copilot/cli)</sub>
