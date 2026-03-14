# 🤖 Copilot CLI Session

> [!NOTE]
> - **Session ID:** `869def1f-0950-48dc-820b-f6db23094ab7`  
> - **Started:** 14/03/2026, 01:57:28  
> - **Duration:** 2m 0s  
> - **Exported:** 14/03/2026, 01:59:28  

---

<sub>⏱️ 5s</sub>

### 👤 User

Inspect the lesson's context-maintenance artifacts before answering. Discover the relevant project instructions, audit scripts, clean and drifted examples, and maintenance docs that exist here rather than assuming a fixed file list. Then fix the drifted example at .github/examples/drifted/copilot-instructions.md by resolving all drift issues you find. Specifically: update stale technology references (Node.js version, logging library), remove contradictory rules (console.log vs structured logging), fix dead file path references (deleted helpers directory), remove over-specified inline code blocks that belong in scoped instructions, and align the drifted file with the clean example's conventions for accuracy and conciseness. Apply the fixes directly in the file. Do not run shell commands and do not use SQL.

---

<sub>⏱️ 18s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model**

".github/**/*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\scripts\detect_stale_refs.py
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\scripts\audit_context.py
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\copilot-instructions.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\clean\copilot-instructions.md
```


---

<sub>⏱️ 18s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model**

"docs/**/*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\docs\operating-model-example.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\docs\maintenance-schedule.md
```


---

<sub>⏱️ 18s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "context|drift|stale|audit|copilot-instructions|helpers",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\08-operating-model",
  "output_mode": "files_with_matches",
  "glob": "{.github/**,docs/**,README.md,ASSESSMENT.md}",
  "-i": true,
  "head_limit": 200
}
```

</details>

<details>
<summary>9 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\README.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\docs\operating-model-example.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\docs\maintenance-schedule.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\ASSESSMENT.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\copilot-instructions.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\clean\copilot-instructions.md
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\scripts\detect_stale_refs.py
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\scripts\audit_context.py
```

</details>


---

<sub>⏱️ 26s</sub>

### 💬 Copilot

I found the lesson’s maintenance artifacts and I’m reading the canonical instructions, examples, scripts, and docs first so the fix follows this lesson’s actual conventions instead of assumptions.

---

<sub>⏱️ 26s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\copilot-instructions.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\copilot-instructions.md

<details>
<summary>29 lines</summary>

```
1. # Loan Workbench — Operating Model Context
2. 
3. This is a TypeScript Express REST API with an embedded message broker and
4. SQLite persistence for commercial loan processing.
5. 
6. ## Context Maintenance Rules
7. 
8. - All context files (`.github/`, `docs/`) must stay in sync with the codebase.
9. - Stale references (wrong file paths, outdated technology names, removed APIs)
10.   degrade AI assistant output quality progressively over time.
11. - Run `.github/scripts/audit_context.py` periodically to detect drift.
12. - Run `.github/scripts/detect_stale_refs.py` to find broken references.
13. 
14. ## Anti-Patterns to Avoid
15. 
16. 1. **Copy-paste drift**: Instructions duplicated across files that diverge over time.
17. 2. **Stale technology references**: Mentioning libraries or APIs no longer in use.
18. 3. **Contradictory rules**: Instructions that conflict with each other across files.
19. 4. **Over-specification**: Rules so detailed they break on minor refactors.
20. 5. **Under-specification**: Vague guidance that provides no actionable constraint.
21. 
22. ## Architecture
23. 
24. - Backend: `app/backend/src/` — Express API + middleware + queue broker + SQLite DB.
25. - Frontend: `app/frontend/src/` — Vanilla TypeScript SPA.
26. - Loan applications follow a strict state machine: submitted → under_review → approved/denied → funded/closed.
27. - Business rules live in `app/backend/src/rules/` — pure functions, no side effects.
28. - Audit logging is mandatory for all mutating operations.
29.
```

</details>


---

<sub>⏱️ 26s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\clean\copilot-instructions.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\clean\copilot-instructions.md

<details>
<summary>54 lines</summary>

```
1. # Loan Workbench — Project Context (CLEAN)
2. 
3. > **This file demonstrates a healthy, well-maintained instructions file.**
4. > Compare with `../drifted/copilot-instructions.md` to see the anti-patterns fixed.
5. 
6. ## Project
7. 
8. Loan Workbench API — TypeScript + Express REST service managing loan
9. application lifecycles with regulatory compliance (California SMS restriction),
10. role-based access, and audit-first persistence.
11. 
12. ## Tech Stack
13. 
14. - Runtime: Node.js 20 LTS
15. - Language: TypeScript 5.x (strict mode)
16. - Framework: Express 4 (see ADR-001 — do NOT suggest Fastify)
17. - Tests: Vitest (see ADR-002 — do NOT suggest Jest)
18. - Modules: ESM only (see ADR-003 — no CommonJS)
19. - Logging: structured JSON via pino
20. - Database: Prisma ORM (see ADR-004 — do NOT suggest knex)
21. - Deploy: Azure Container Apps
22. 
23. ## Architecture
24. 
25. Three-layer separation:
26. 
27. 1. **Routes** (`app/backend/src/routes/`) — HTTP handling, parameter extraction, delegation
28. 2. **Rules** (`app/backend/src/rules/`) — pure business logic, no I/O
29. 3. **Services** (`app/backend/src/services/`) — persistence, external integrations, audit
30. 
31. Request flow: Route → authenticate → authorize → validate → Rule → Service → respond.
32. 
33. Audit events are recorded BEFORE persistence — if logging fails, the write
34. does NOT proceed (fail-closed semantics).
35. 
36. ## Coding Conventions
37. 
38. - `const` over `let`; never `var`
39. - All route handlers are `async`
40. - All errors return structured JSON: `{ error: string, code: string }`
41. - No stack traces in error responses (security)
42. - Feature flags use 404 (not found), not 403 (forbidden)
43. - Structured JSON logging only — never `console.log()`
44. - Tests annotated with `// FALSE POSITIVE` or `// HARD NEGATIVE` where applicable
45. 
46. ## References
47. 
48. - Full architecture: see `/docs/architecture.md`
49. - API conventions: see `/docs/api-conventions.md`
50. - Route handler template: see `.github/instructions/api.instructions.md`
51. - Notification rules: see `.github/instructions/notifications.instructions.md`
52. - Test conventions: see `.github/instructions/test.instructions.md`
53. - Technology decisions: see `/docs/adr/`
54.
```

</details>


---

<sub>⏱️ 26s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md

<details>
<summary>196 lines</summary>

````
1. # Loan Workbench — Project Context (DRIFTED)
2. 
3. > **This file demonstrates anti-patterns.** Compare with `../clean/copilot-instructions.md`.
4. 
5. <!-- ANTI-PATTERN #1: Bloated instructions (310 lines) -->
6. <!-- ANTI-PATTERN #2: Contradictory rules -->
7. <!-- ANTI-PATTERN #4: Stale references to deleted files -->
8. <!-- ANTI-PATTERN #5: Overly specific rules that should be in .instructions.md -->
9. 
10. ## Project
11. 
12. Loan Workbench API — TypeScript + Express REST service managing loan
13. application lifecycles with regulatory compliance.
14. 
15. ## Tech Stack
16. 
17. - Runtime: Node.js 18 LTS
18.   <!-- STALE: Upgraded to Node.js 20 three months ago -->
19. - Language: TypeScript 5.x (strict mode)
20. - Framework: Express 4
21. - Tests: Vitest
22. - Modules: ESM only
23. - Logging: structured JSON via winston
24.   <!-- STALE: Migrated from winston to pino two months ago -->
25. 
26. ## Architecture
27. 
28. Three-layer separation:
29. 
30. 1. **Routes** (`src/routes/`) — HTTP handling, parameter extraction, delegation
31. 2. **Rules** (`src/rules/`) — pure business logic, no I/O
32. 3. **Services** (`src/services/`) — persistence, external integrations, audit
33. 4. **Helpers** (`src/helpers/`) — shared utility functions
34.    <!-- STALE: Helpers directory was deleted during refactoring. All utils
35.         were moved into rules/ or services/. This reference is dead. -->
36. 
37. ## Coding Conventions
38. 
39. - `const` over `let`; never `var`
40. - All route handlers are `async`
41. - All errors return structured JSON: `{ error: string, code: string }`
42. - No stack traces in error responses
43. - Feature flags use 404, not 403
44. - Use `console.log()` for debugging during development
45.   <!-- CONTRADICTION: Line above says "structured JSON logging" but this
46.        says console.log. Which one? Teams will override AI constantly. -->
47. - All route handlers must include request timing:
48.   ```typescript
49.   const start = Date.now();
50.   // ... handler logic ...
51.   const duration = Date.now() - start;
52.   logger.info({ duration, path: req.path });
53.   ```
54.   <!-- ANTI-PATTERN #5: This implementation detail should be in
55.        .github/instructions/api.instructions.md with applyTo: "src/routes/**"
56.        not in the global instructions file. -->
57. 
58. ## Route Handler Template
59. 
60. Every route handler MUST follow this exact pattern:
61. 
62. ```typescript
63. import { Router } from "express";
64. import { authenticate } from "../middleware/auth.js";
65. import { authorize } from "../middleware/rbac.js";
66. 
67. const router = Router();
68. 
69. router.get(
70.   "/api/v1/resource",
71.   authenticate,
72.   authorize("role"),
73.   async (req, res) => {
74.     try {
75.       const result = await service.fetch(req.params.id);
76.       if (!result) {
77.         return res.status(404).json({ error: "Not found", code: "NOT_FOUND" });
78.       }
79.       res.json(result);
80.     } catch (err) {
81.       res.status(500).json({ error: "Internal error", code: "INTERNAL" });
82.     }
83.   },
84. );
85. 
86. router.post(
87.   "/api/v1/resource",
88.   authenticate,
89.   authorize("admin"),
90.   async (req, res) => {
91.     const validated = schema.parse(req.body);
92.     const rule = await businessRule(validated);
93.     await auditService.record({ action: "create", ...rule });
94.     const saved = await persistenceService.save(rule);
95.     res.status(201).json(saved);
96.   },
97. );
98. 
99. router.put(
100.   "/api/v1/resource/:id",
101.   authenticate,
102.   authorize("admin"),
103.   async (req, res) => {
104.     const existing = await service.fetch(req.params.id);
105.     if (!existing) {
106.       return res.status(404).json({ error: "Not found", code: "NOT_FOUND" });
107.     }
108.     const validated = schema.parse(req.body);
109.     const rule = await businessRule(validated, existing);
110.     await auditService.record({ action: "update", ...rule });
111.     const updated = await persistenceService.update(req.params.id, rule);
112.     res.json(updated);
113.   },
114. );
115. 
116. router.delete(
117.   "/api/v1/resource/:id",
118.   authenticate,
119.   authorize("admin"),
120.   async (req, res) => {
121.     const existing = await service.fetch(req.params.id);
122.     if (!existing) {
123.       return res.status(404).json({ error: "Not found", code: "NOT_FOUND" });
124.     }
125.     await auditService.record({ action: "delete", id: req.params.id });
126.     await persistenceService.remove(req.params.id);
127.     res.status(204).send();
128.   },
129. );
130. ```
131. 
132. <!-- ANTI-PATTERN #1: This 50-line code block inflates the file to 310 lines.
133.      The full template belongs in api.instructions.md or docs/api-conventions.md.
134.      copilot-instructions.md should contain a 2-line summary and a reference. -->
135. 
136. ## Notification System Rules
137. 
138. - SMS notifications must not be sent to California phone numbers (LEGAL-218)
139. - Email notifications are allowed for all states
140. - Push notifications require user opt-in
141. - Notification batching: max 100 per minute per user
142. - Retry policy: 3 attempts with exponential backoff
143. - Dead letter queue after 3 failures
144. 
145. <!-- ANTI-PATTERN #5: These operational details should be in
146.      .github/instructions/notifications.instructions.md with
147.      applyTo: "src/services/notification*"
148.      Not every file needs to know notification retry policy. -->
149. 
150. ## Database Conventions
151. 
152. - All queries use parameterized statements
153. - Connection pool: min 5, max 20
154. - Query timeout: 30 seconds
155. - Migrations: use knex migrate:latest
156.   <!-- STALE: Migrated from knex to Prisma four months ago -->
157. - Always use transactions for multi-table writes
158. 
159. ## Testing Conventions
160. 
161. - Test files: `*.test.ts` in `tests/` directory
162. - Use Vitest: `describe`, `it`, `expect`
163. - Mock external services in tests
164. - Use `beforeEach` for test isolation
165. - Annotate edge cases with `// FALSE POSITIVE` or `// HARD NEGATIVE`
166. - Integration tests: use `supertest` for HTTP assertions
167. - Coverage target: 80%
168. - Run tests: `npx vitest run`
169. - Run specific: `npx vitest run tests/rules/`
170. 
171. <!-- ANTI-PATTERN #5: Most of these testing conventions should be in
172.      .github/instructions/test.instructions.md with
173.      applyTo: "tests/**"
174.      Only the framework name (Vitest) belongs here. -->
175. 
176. ## Deployment
177. 
178. - CI: GitHub Actions
179. - Deploy: AWS ECS Fargate
180.   <!-- STALE: Migrated to Azure Container Apps two months ago -->
181. - Staging: auto-deploy on PR merge to `develop`
182. - Production: manual approval after staging validation
183. - Rollback: revert the deployment and re-deploy previous tag
184. 
185. ## References
186. 
187. - Full architecture: see `/docs/architecture.md`
188. - API conventions: see `/docs/api-conventions.md`
189. - Deployment guide: see `/docs/deployment.md`
190.   <!-- STALE: /docs/deployment.md was deleted — deployment is now in
191.        the separate infra repo -->
192. - Migration guide: see `/docs/knex-to-prisma.md`
193.   <!-- STALE: This migration guide was never created -->
194. - Helper utilities: see `/src/helpers/README.md`
195.   <!-- STALE: /src/helpers/ was deleted during refactoring -->
196.
````

</details>


---

<sub>⏱️ 26s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\scripts\audit_context.py.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\scripts\audit_context.py

<details>
<summary>182 lines</summary>

```
1. #!/usr/bin/env python3
2. """Context health audit script (Python replacement for audit-context.sh).
3. 
4. Scans a project's .github/ and docs/ for common context health issues.
5. Usage: python audit_context.py [--project-dir <path>]
6. """
7. import argparse
8. import os
9. import re
10. import sys
11. import time
12. from pathlib import Path
13. 
14. 
15. class AuditCounter:
16.     def __init__(self) -> None:
17.         self.warnings = 0
18.         self.errors = 0
19. 
20.     def warn(self, msg: str) -> None:
21.         print(f"  ⚠ WARNING: {msg}")
22.         self.warnings += 1
23. 
24.     def error(self, msg: str) -> None:
25.         print(f"  ✗ ERROR: {msg}")
26.         self.errors += 1
27. 
28.     def ok(self, msg: str) -> None:
29.         print(f"  ✓ PASS: {msg}")
30. 
31.     def info(self, msg: str) -> None:
32.         print(f"  ℹ INFO: {msg}")
33. 
34. 
35. def audit(project_dir: Path) -> int:
36.     c = AuditCounter()
37. 
38.     print("═" * 45)
39.     print(f" Context Health Audit")
40.     print(f" Project: {project_dir.name}")
41.     print("═" * 45)
42. 
43.     # ─── 1. Foundation ─────────────────────────────
44.     print("\n── 1. Foundation ──")
45.     ci = project_dir / ".github" / "copilot-instructions.md"
46.     if ci.exists():
47.         lines = ci.read_text(encoding="utf-8").splitlines()
48.         n = len(lines)
49.         if n > 200:
50.             c.warn(f".github/copilot-instructions.md is {n} lines (max recommended: 200)")
51.         elif n < 10:
52.             c.warn(f".github/copilot-instructions.md is only {n} lines (too minimal)")
53.         else:
54.             c.ok(f".github/copilot-instructions.md exists ({n} lines)")
55.     else:
56.         c.error(".github/copilot-instructions.md not found")
57. 
58.     # ─── 2. Instruction files ──────────────────────
59.     print("\n── 2. Instruction Files ──")
60.     inst_dir = project_dir / ".github" / "instructions"
61.     if inst_dir.is_dir():
62.         inst_files = list(inst_dir.rglob("*.instructions.md"))
63.         no_scope = 0
64.         for f in inst_files:
65.             head = f.read_text(encoding="utf-8")[:300]
66.             if "applyTo" not in head:
67.                 c.warn(f"{f.relative_to(project_dir)} missing applyTo frontmatter")
68.                 no_scope += 1
69.         if inst_files:
70.             c.ok(f"Found {len(inst_files)} instruction file(s)")
71.         if no_scope:
72.             c.warn(f"{no_scope} instruction file(s) without applyTo scope")
73.     else:
74.         c.info("No .github/instructions/ directory (optional — added in Lesson 03)")
75. 
76.     # ─── 3. Agents ─────────────────────────────────
77.     print("\n── 3. Agents ──")
78.     agents_dir = project_dir / ".github" / "agents"
79.     if agents_dir.is_dir():
80.         agent_files = list(agents_dir.rglob("*.agent.md"))
81.         for f in agent_files:
82.             head = f.read_text(encoding="utf-8")[:500]
83.             if "tools:" not in head:
84.                 c.warn(f"{f.relative_to(project_dir)} has no tools: restriction")
85.         c.ok(f"Found {len(agent_files)} agent(s)")
86.     else:
87.         c.info("No .github/agents/ directory (optional — added in Lesson 05)")
88. 
89.     # ─── 4. Prompts ────────────────────────────────
90.     print("\n── 4. Prompts ──")
91.     prompts_dir = project_dir / ".github" / "prompts"
92.     if prompts_dir.is_dir():
93.         prompt_count = len(list(prompts_dir.rglob("*.prompt.md")))
94.         c.ok(f"Found {prompt_count} prompt file(s)")
95.     else:
96.         c.info("No .github/prompts/ directory (optional — added in Lesson 04)")
97. 
98.     # ─── 5. Documentation ──────────────────────────
99.     print("\n── 5. Documentation ──")
100.     docs_dir = project_dir / "docs"
101.     if docs_dir.is_dir():
102.         doc_count = len(list(docs_dir.rglob("*.md")))
103.         c.ok(f"Found {doc_count} doc file(s) in docs/")
104.         adr_dir = docs_dir / "adr"
105.         if adr_dir.is_dir():
106.             adr_count = len(list(adr_dir.rglob("*.md")))
107.             c.ok(f"Found {adr_count} ADR(s)")
108.         else:
109.             c.info("No docs/adr/ directory (recommended for technology decisions)")
110.     else:
111.         c.warn("No docs/ directory (knowledge context layer missing)")
112. 
113.     # ─── 6. Cross-Reference Integrity ──────────────
114.     print("\n── 6. Cross-Reference Integrity ──")
115.     stale_refs = 0
116.     if ci.exists():
117.         text = ci.read_text(encoding="utf-8")
118.         # Match paths like /docs/something.md or docs/adr/
119.         refs = re.findall(r'[`/]([\w][\w./-]+\.(?:md|ts|js|json|yaml))[`\s]', text)
120.         refs += re.findall(r'(?:see |See )[`/]?([\w][\w./-]+)[`\s]', text)
121.         for ref in refs:
122.             ref_path = ref.lstrip("/")
123.             full = project_dir / ref_path
124.             if not full.exists():
125.                 c.warn(f"copilot-instructions.md references '{ref_path}' but it doesn't exist")
126.                 stale_refs += 1
127.     if stale_refs == 0:
128.         c.ok("No stale cross-references detected")
129. 
130.     # ─── 7. Content Freshness ──────────────────────
131.     print("\n── 7. Content Freshness ──")
132.     stale_days = 90
133.     stale_count = 0
134.     now = time.time()
135.     for search_dir in [project_dir / ".github", project_dir / "docs"]:
136.         if search_dir.is_dir():
137.             for f in search_dir.rglob("*.md"):
138.                 age_days = int((now - f.stat().st_mtime) / 86400)
139.                 if age_days > stale_days:
140.                     c.warn(f"{f.relative_to(project_dir)} not modified in {age_days} days (threshold: {stale_days})")
141.                     stale_count += 1
142.     if stale_count == 0:
143.         c.ok(f"All context files modified within {stale_days} days")
144. 
145.     # ─── 8. Anti-Pattern Detection ─────────────────
146.     print("\n── 8. Anti-Pattern Detection ──")
147.     if ci.exists():
148.         lines = ci.read_text(encoding="utf-8").splitlines()
149.         if len(lines) > 300:
150.             c.error(f"copilot-instructions.md is {len(lines)} lines — split into .instructions.md files")
151. 
152.     if agents_dir.is_dir():
153.         for f in agents_dir.rglob("*.agent.md"):
154.             head = f.read_text(encoding="utf-8")[:1000]
155.             if "tools:" not in head:
156.                 c.error(f"{f.relative_to(project_dir)} has no tool restrictions — over-privileged agent")
157. 
158.     # ─── Summary ───────────────────────────────────
159.     print(f"\n{'═' * 45}")
160.     print(f" Summary: Warnings: {c.warnings} | Errors: {c.errors}")
161.     if c.errors > 0:
162.         print(f" ACTION REQUIRED: Fix {c.errors} error(s) before proceeding.")
163.         return 2
164.     elif c.warnings > 0:
165.         print(f" Review {c.warnings} warning(s).")
166.         return 1
167.     else:
168.         print(" All checks passed.")
169.         return 0
170. 
171. 
172. def main() -> None:
173.     parser = argparse.ArgumentParser(description="Context health audit")
174.     parser.add_argument("--project-dir", type=Path, default=Path.cwd(),
175.                         help="Project root to audit (default: cwd)")
176.     args = parser.parse_args()
177.     sys.exit(audit(args.project_dir))
178. 
179. 
180. if __name__ == "__main__":
181.     main()
182.
```

</details>


---

<sub>⏱️ 26s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\scripts\detect_stale_refs.py.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\scripts\detect_stale_refs.py

<details>
<summary>77 lines</summary>

```
1. #!/usr/bin/env python3
2. """Dead reference detection script (Python replacement for detect-stale-refs.sh).
3. 
4. Scans all .md files in .github/ and docs/ for internal path references
5. and reports any that point to files or directories that don't exist.
6. 
7. Usage: python detect_stale_refs.py [--project-dir <path>]
8. """
9. import argparse
10. import re
11. import sys
12. from pathlib import Path
13. 
14. 
15. def scan(project_dir: Path) -> int:
16.     stale = 0
17.     checked = 0
18. 
19.     print("Scanning for stale references...")
20.     print()
21. 
22.     search_dirs = [project_dir / ".github", project_dir / "docs"]
23.     md_files: list[Path] = []
24.     for d in search_dirs:
25.         if d.is_dir():
26.             md_files.extend(d.rglob("*.md"))
27. 
28.     for md_file in md_files:
29.         text = md_file.read_text(encoding="utf-8", errors="replace")
30.         rel_name = md_file.relative_to(project_dir)
31. 
32.         # Match file references: backtick-wrapped, markdown links, "see" references
33.         file_refs = re.findall(
34.             r'(?:`|(?:[Ss]ee\s+)|\]\()/?([a-zA-Z][\w./-]+\.(?:md|ts|js|json|yaml|yml))',
35.             text,
36.         )
37.         dir_refs = re.findall(
38.             r'(?:`|(?:[Ss]ee\s+)|\]\()/?([a-zA-Z][\w/-]+/)',
39.             text,
40.         )
41. 
42.         for ref in file_refs:
43.             checked += 1
44.             clean = ref.lstrip("/")
45.             if not (project_dir / clean).is_file():
46.                 print(f"  ✗ STALE {rel_name} → {clean} (file not found)")
47.                 stale += 1
48. 
49.         for ref in dir_refs:
50.             checked += 1
51.             clean = ref.lstrip("/")
52.             if not (project_dir / clean).is_dir():
53.                 print(f"  ✗ STALE {rel_name} → {clean} (directory not found)")
54.                 stale += 1
55. 
56.     print()
57.     print("─" * 30)
58.     print(f"Checked: {checked} references")
59.     if stale > 0:
60.         print(f"Found: {stale} stale reference(s)")
61.         return 1
62.     else:
63.         print("All references valid.")
64.         return 0
65. 
66. 
67. def main() -> None:
68.     parser = argparse.ArgumentParser(description="Detect stale references in context files")
69.     parser.add_argument("--project-dir", type=Path, default=Path.cwd(),
70.                         help="Project root to scan (default: cwd)")
71.     args = parser.parse_args()
72.     sys.exit(scan(args.project_dir))
73. 
74. 
75. if __name__ == "__main__":
76.     main()
77.
```

</details>


---

<sub>⏱️ 26s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\docs\operating-model-example.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\docs\operating-model-example.md

<details>
<summary>54 lines</summary>

```
1. # Lesson 08 — Operating Model Example
2. 
3. This document defines the concrete example used in Lesson 08.
4. 
5. ## Objective
6. 
7. Show that the CLI can discover context drift in a drifted instruction file and fix it — producing an assessable code change that resolves real maintenance issues.
8. 
9. ## Expected Output Shape
10. 
11. The demo must modify one file:
12. 
13. 1. `.github/examples/drifted/copilot-instructions.md` — fixed to resolve all discovered drift issues
14. 
15. The fixed file should resolve:
16. 
17. 1. Stale technology references (Node.js version, logging library)
18. 2. Contradictory rules (console.log vs structured logging)
19. 3. Dead file path references (deleted helpers directory)
20. 4. Over-specified inline code blocks that belong in scoped instructions
21. 5. Alignment with the clean example's conventions
22. 
23. ## Expected Change Artifacts
24. 
25. Assessment compares the actual `demo.patch` and `changed-files.json` against:
26. 
27. - `.output/change/expected-files.json` — expected added/modified/deleted files
28. - `.output/change/expected-patterns.json` — regex patterns that must appear in the patch
29. 
30. ## Required Constraints
31. 
32. 1. The fix must be applied directly to `.github/examples/drifted/copilot-instructions.md`.
33. 2. The fix must update stale Node.js version references (18 → 20).
34. 3. The fix must replace the stale logging library reference (winston → pino).
35. 4. The fix must remove contradictory console.log rules.
36. 5. The fix must remove or update dead file path references to non-existent helpers.
37. 6. The fix must remove over-specified inline code blocks.
38. 7. Do not run shell commands during the assessment run.
39. 8. Do not use SQL during the assessment run.
40. 
41. ## Concrete Scenario
42. 
43. Use the lesson's clean and drifted example instruction files plus the maintenance scripts and schedule to discover and fix all drift in the drifted file.
44. 
45. ## What Good Output Looks Like
46. 
47. Good output will usually:
48. 
49. - update Node.js 18 references to Node.js 20
50. - replace winston references with pino
51. - remove or resolve the console.log contradiction
52. - remove references to deleted helpers directory
53. - make the drifted file concise and accurate like the clean example
54.
```

</details>


---

<sub>⏱️ 26s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\docs\maintenance-schedule.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\docs\maintenance-schedule.md

<details>
<summary>69 lines</summary>

```
1. # Context Maintenance Schedule
2. 
3. Use this checklist to keep your AI context healthy over time.
4. 
5. ## Weekly (5 minutes)
6. 
7. - [ ] Run `python scripts/audit_context.py` and fix any ERRORS
8. - [ ] Review any new team PRs that touched `.github/` or `docs/`
9. - [ ] If a dependency was updated, check if `copilot-instructions.md` mentions
10.       the old version
11. 
12. ## Monthly (30 minutes)
13. 
14. - [ ] Run `python scripts/detect_stale_refs.py` and fix broken references
15. - [ ] Review instruction files for rules that are no longer needed
16. - [ ] Check for duplicate rules (same rule in `copilot-instructions.md` AND
17.       `.instructions.md` — deduplicate to the most appropriate location)
18. - [ ] Review agent tool lists — remove tools no longer relevant
19. - [ ] Check if any new ADRs should be documented
20. - [ ] Review prompt files — update variables if project structure changed
21. 
22. ## Quarterly (1 hour)
23. 
24. - [ ] Full context audit:
25.   - Are the architecture docs still accurate?
26.   - Are the coding conventions still followed?
27.   - Have any technologies been replaced?
28. - [ ] Review the Context Health Metrics (see below)
29. - [ ] Prune dead context:
30.   - Features decommissioned but context remains
31.   - Deprecated APIs still referenced in docs
32.   - Agents for workflows no longer used
33. - [ ] Review `#file:` attachment patterns — are learners/developers attaching
34.       the right files, or struggling to find them?
35. - [ ] Update `copilot-instructions.md` references if new docs were added
36. 
37. ## Context Health Metrics
38. 
39. Track these signals to measure context effectiveness:
40. 
41. ### Leading Indicators (predict problems)
42. 
43. | Signal                          | How to Measure                              | Target        |
44. | ------------------------------- | ------------------------------------------- | ------------- |
45. | Instruction file size           | `wc -l .github/copilot-instructions.md`     | < 200 lines   |
46. | Cross-reference validity        | `python scripts/detect_stale_refs.py`       | 0 stale refs  |
47. | Context freshness               | `find .github docs -mtime +90 -name '*.md'` | 0 stale files |
48. | Agent tool restriction coverage | Agents with `tools:` / total agents         | 100%          |
49. 
50. ### Lagging Indicators (confirm problems)
51. 
52. | Signal                          | How to Measure                                | Target     |
53. | ------------------------------- | --------------------------------------------- | ---------- |
54. | AI correction rate              | Count corrections in Copilot Chat per session | Decreasing |
55. | Convention violation rate       | Test failures due to wrong patterns           | Decreasing |
56. | "Ignore the instructions" rate  | Times users say "no, do it THIS way"          | Decreasing |
57. | Time to first useful suggestion | Minutes from opening Chat to usable code      | Decreasing |
58. 
59. ### Red Flags
60. 
61. These signals indicate context rot:
62. 
63. - [ ] Developers frequently override AI suggestions with "actually, we do it THIS way"
64. - [ ] New team members get wrong answers about project architecture
65. - [ ] PRs contain patterns that were documented as rejected (e.g., Jest tests when Vitest is required)
66. - [ ] `copilot-instructions.md` exceeds 300 lines (needs splitting)
67. - [ ] Agents suggest tools that are no longer installed
68. - [ ] Prompt files reference variables/paths that have been renamed
69.
```

</details>


---

<sub>⏱️ 26s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\README.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\README.md

<details>
<summary>82 lines</summary>

````
1. # Lesson 08 — Operating Model
2. 
3. > **App:** Loan Workbench (TypeScript Express API + SQLite)
4. > **Topic:** Maintaining context over time with audit scripts, drift detection, and clean versus drifted examples.
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
15. Context files drift as codebases evolve. This lesson shows how to detect and fix staleness.
16. 
17. | Tool | Purpose |
18. | --- | --- |
19. | `scripts/audit_context.py` | Audits `.github/` for completeness and quality |
20. | `scripts/detect_stale_refs.py` | Finds broken file references |
21. | `examples/clean/` | Well-maintained reference example |
22. | `examples/drifted/` | Drifted example to diagnose |
23. 
24. ## Context Files
25. 
26. | Path | Purpose |
27. | --- | --- |
28. | `.github/copilot-instructions.md` | Project-level instructions |
29. | `.github/scripts/audit_context.py` | Context audit script |
30. | `.github/scripts/detect_stale_refs.py` | Stale reference detector |
31. | `.github/examples/clean/copilot-instructions.md` | Clean example |
32. | `.github/examples/drifted/copilot-instructions.md` | Drifted example |
33. | `docs/maintenance-schedule.md` | Maintenance cadence |
34. | `docs/operating-model-example.md` | Concrete lesson-08 demo target and assessment constraints |
35. 
36. ## Example Goal
37. 
38. This lesson should demonstrate context-maintenance through direct drift repair.
39. 
40. For this example, the intended outcome is:
41. 
42. - inspect the maintenance scripts, clean example, drifted example, and schedule
43. - discover the relevant maintenance artifacts instead of relying on a hardcoded read list
44. - fix the drifted example by resolving all discovered drift issues directly in the file
45. - the changes are assessable via actual vs expected file and pattern comparison
46. 
47. ## Copilot CLI Workflow
48. 
49. Fix the drifted example:
50. 
51. ```bash
52. copilot -p "Inspect the lesson's context-maintenance artifacts before answering. Discover the relevant project instructions, audit scripts, clean and drifted examples, and maintenance docs that exist here rather than assuming a fixed file list. Then fix the drifted example at .github/examples/drifted/copilot-instructions.md by resolving all drift issues you find. Specifically: update stale technology references (Node.js version, logging library), remove contradictory rules (console.log vs structured logging), fix dead file path references (deleted helpers directory), remove over-specified inline code blocks that belong in scoped instructions, and align the drifted file with the clean example's conventions for accuracy and conciseness. Apply the fixes directly in the file. Do not run shell commands and do not use SQL." --allow-all-tools --deny-tool=powershell --deny-tool=sql
53. ```
54. 
55. Expected result:
56. 
57. - the CLI fixes `.github/examples/drifted/copilot-instructions.md`
58. - stale Node.js and logging references are updated
59. - contradictory rules are resolved
60. - dead file references are removed
61. - `.output/change/demo.patch` contains the drift fixes
62. - `.output/change/comparison.md` shows actual vs expected file and pattern match results
63. 
64. ## VS Code Chat Workflow
65. 
66. Ask the agent to:
67. 
68. - run the audit scripts
69. - interpret the findings
70. - compare clean and drifted examples
71. - propose a maintenance PR plan
72. 
73. Expected result: the model shifts from code generation to context maintenance and operational hygiene.
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

<sub>⏱️ 26s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\ASSESSMENT.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\ASSESSMENT.md

<details>
<summary>50 lines</summary>

````
1. # Lesson 08 CLI Prompt Assessment
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
12. Inspect the lesson's context-maintenance artifacts before answering. Discover the relevant project instructions, audit scripts, clean and drifted examples, and maintenance docs that exist here rather than assuming a fixed file list. Then fix the drifted example at .github/examples/drifted/copilot-instructions.md by resolving all drift issues you find. Specifically: update stale technology references (Node.js version, logging library), remove contradictory rules (console.log vs structured logging), fix dead file path references (deleted helpers directory), remove over-specified inline code blocks that belong in scoped instructions, and align the drifted file with the clean example's conventions for accuracy and conciseness. Apply the fixes directly in the file. Do not run shell commands and do not use SQL.
13. ```
14. 
15. The assessment run uses the model from `lessons/_common/assessment-config.json`.
16. 
17. ## Assessment Scope
18. 
19. The only question being evaluated is:
20. 
21. > Did the produced code changes implement the prompt in a way that correctly resolves the drift issues and follows the clean example's conventions?
22. 
23. ## Expected Change Artifacts
24. 
25. Assessment compares actual output against gold-standard expectations:
26. 
27. - `.output/change/expected-files.json` — expected file: `.github/examples/drifted/copilot-instructions.md` (modified)
28. - `.output/change/expected-patterns.json` — required patterns in patch: Node.js 20, pino, remove console.log, remove helpers
29. 
30. The `compare_with_expected()` function writes `.output/change/comparison.md` with a structured match report.
31. 
32. ## Assessment Criteria
33. 
34. | Criterion | Source |
35. | --- | --- |
36. | Drifted file modified | `expected-files.json` |
37. | Node.js version updated (18 → 20) | `expected-patterns.json` |
38. | Logging library updated (winston → pino) | `expected-patterns.json` |
39. | console.log contradiction resolved | `expected-patterns.json` |
40. | Dead helpers reference removed | `expected-patterns.json` |
41. | No shell commands executed | Prompt constraint |
42. | No SQL tools used | Prompt constraint |
43. 
44. ## Captured Result
45. 
46. Pending re-run with the updated implementation-oriented prompt. Previous assessment was for a read-only operating-model analysis demo that has been replaced.
47. 
48. ## Verdict
49. 
50. Pending re-run.
````

</details>


---

<sub>⏱️ 56s</sub>

### 💬 Copilot

I’ve got the full picture now: the maintenance scripts emphasize valid cross-references and avoiding drift/over-specification, and the clean example gives the right concise structure. Next I’m updating the drifted file to match that standard while keeping its references valid in this lesson.

---

<sub>⏱️ 56s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Add File: C:/Users/nilay/.copilot/session-state/869def1f-0950-48dc-820b-f6db23094ab7/plan.md\n+## Plan\n+\n+1. Use the lesson's discovered maintenance artifacts as the source of truth.\n+2. Replace stale technology and deployment references in the drifted example.\n+3. Remove contradictory, dead, and over-specified content.\n+4. Restructure the drifted file to match the clean example's concise sections.\n+5. Re-read the updated file to verify accuracy and valid references.\n*** End Patch\n"
```

</details>

```
Added 1 file(s): C:\Users\nilay\.copilot\session-state\869def1f-0950-48dc-820b-f6db23094ab7\plan.md
```


---

<sub>⏱️ 1m 1s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Delete File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\08-operating-model\\.github\\examples\\drifted\\copilot-instructions.md\n*** End Patch\n"
```

</details>

```
Deleted 1 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md
```


---

<sub>⏱️ 1m 8s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Add File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\08-operating-model\\.github\\examples\\drifted\\copilot-instructions.md\n+# Loan Workbench — Project Context\n+\n+> **This file shows the corrected version of the drifted example.**\n+> It now follows the clean example's structure and keeps references valid.\n+\n+## Project\n+\n+Loan Workbench API — TypeScript + Express REST service managing loan\n+application lifecycles with regulatory compliance, role-based access, and\n+audit-first persistence.\n+\n+## Tech Stack\n+\n+- Runtime: Node.js 20 LTS\n+- Language: TypeScript 5.x (strict mode)\n+- Framework: Express 4\n+- Tests: Vitest\n+- Modules: ESM only\n+- Logging: structured JSON via pino\n+- Database: Prisma ORM\n+- Deploy: Azure Container Apps\n+\n+## Architecture\n+\n+Three-layer separation:\n+\n+1. **Routes** (`src/routes/`) — HTTP handling, parameter extraction, delegation\n+2. **Rules** (`src/rules/`) — pure business logic, no I/O\n+3. **Services** (`src/services/`) — persistence, external integrations, audit\n+\n+Request flow: Route -> authenticate -> authorize -> validate -> Rule ->\n+Service -> respond.\n+\n+Audit events are recorded before persistence. Mutating operations should use\n+structured logging only; do not use `console.log()`.\n+\n+## Coding Conventions\n+\n+- `const` over `let`; never `var`\n+- All route handlers are `async`\n+- All errors return structured JSON: `{ error: string, code: string }`\n+- No stack traces in error responses\n+- Feature flags use 404, not 403\n+- Keep global instructions concise; detailed route, notification, and test\n+  patterns belong in scoped instructions or dedicated docs\n+- Annotate tests with `// FALSE POSITIVE` or `// HARD NEGATIVE` where applicable\n+\n+## References\n+\n+- Canonical project context: see `.github/copilot-instructions.md`\n+- Clean example: see `.github/examples/clean/copilot-instructions.md`\n+- Maintenance cadence: see `/docs/maintenance-schedule.md`\n+- Lesson scope and expected output: see `/docs/operating-model-example.md`\n+- Context audit: see `.github/scripts/audit_context.py`\n+- Stale reference detector: see `.github/scripts/detect_stale_refs.py`\n*** End Patch\n"
```

</details>

```
Added 1 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md
```


---

<sub>⏱️ 1m 15s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md

<details>
<summary>56 lines</summary>

```
1. # Loan Workbench — Project Context
2. 
3. > **This file shows the corrected version of the drifted example.**
4. > It now follows the clean example's structure and keeps references valid.
5. 
6. ## Project
7. 
8. Loan Workbench API — TypeScript + Express REST service managing loan
9. application lifecycles with regulatory compliance, role-based access, and
10. audit-first persistence.
11. 
12. ## Tech Stack
13. 
14. - Runtime: Node.js 20 LTS
15. - Language: TypeScript 5.x (strict mode)
16. - Framework: Express 4
17. - Tests: Vitest
18. - Modules: ESM only
19. - Logging: structured JSON via pino
20. - Database: Prisma ORM
21. - Deploy: Azure Container Apps
22. 
23. ## Architecture
24. 
25. Three-layer separation:
26. 
27. 1. **Routes** (`src/routes/`) — HTTP handling, parameter extraction, delegation
28. 2. **Rules** (`src/rules/`) — pure business logic, no I/O
29. 3. **Services** (`src/services/`) — persistence, external integrations, audit
30. 
31. Request flow: Route -> authenticate -> authorize -> validate -> Rule ->
32. Service -> respond.
33. 
34. Audit events are recorded before persistence. Mutating operations should use
35. structured logging only; do not use `console.log()`.
36. 
37. ## Coding Conventions
38. 
39. - `const` over `let`; never `var`
40. - All route handlers are `async`
41. - All errors return structured JSON: `{ error: string, code: string }`
42. - No stack traces in error responses
43. - Feature flags use 404, not 403
44. - Keep global instructions concise; detailed route, notification, and test
45.   patterns belong in scoped instructions or dedicated docs
46. - Annotate tests with `// FALSE POSITIVE` or `// HARD NEGATIVE` where applicable
47. 
48. ## References
49. 
50. - Canonical project context: see `.github/copilot-instructions.md`
51. - Clean example: see `.github/examples/clean/copilot-instructions.md`
52. - Maintenance cadence: see `/docs/maintenance-schedule.md`
53. - Lesson scope and expected output: see `/docs/operating-model-example.md`
54. - Context audit: see `.github/scripts/audit_context.py`
55. - Stale reference detector: see `.github/scripts/detect_stale_refs.py`
56.
```

</details>


---

<sub>⏱️ 1m 15s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "Node\\.js 18|winston|console\\.log\\(|src/helpers|helpers/README|knex migrate:latest|AWS ECS Fargate|/docs/deployment\\.md|/docs/knex-to-prisma\\.md",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\08-operating-model\\.github\\examples\\drifted\\copilot-instructions.md",
  "output_mode": "content",
  "-n": true,
  "head_limit": 50
}
```

</details>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md:35:structured logging only; do not use `console.log()`.
```


---

<sub>⏱️ 1m 15s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "\\.github/copilot-instructions\\.md|\\.github/examples/clean/copilot-instructions\\.md|/docs/maintenance-schedule\\.md|/docs/operating-model-example\\.md|\\.github/scripts/audit_context\\.py|\\.github/scripts/detect_stale_refs\\.py",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\08-operating-model\\.github\\examples\\drifted\\copilot-instructions.md",
  "output_mode": "content",
  "-n": true,
  "head_limit": 50
}
```

</details>

<details>
<summary>6 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md:50:- Canonical project context: see `.github/copilot-instructions.md`
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md:51:- Clean example: see `.github/examples/clean/copilot-instructions.md`
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md:52:- Maintenance cadence: see `/docs/maintenance-schedule.md`
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md:53:- Lesson scope and expected output: see `/docs/operating-model-example.md`
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md:54:- Context audit: see `.github/scripts/audit_context.py`
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md:55:- Stale reference detector: see `.github/scripts/detect_stale_refs.py`
```

</details>


---

<sub>⏱️ 1m 31s</sub>

### 💬 Copilot

One quick spot-check: I want to make sure the remaining in-file path mentions aren’t accidentally introducing fresh dead references, since the lesson’s scripts explicitly flag that kind of drift.

---

<sub>⏱️ 1m 31s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model**

"src/**/*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model

```
No files matched the pattern.
```


---

<sub>⏱️ 1m 31s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model**

"app/backend/src/**/*" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model

```
No files matched the pattern.
```


---

<sub>⏱️ 1m 47s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Update File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\08-operating-model\\.github\\examples\\drifted\\copilot-instructions.md\n@@\n-1. **Routes** (`src/routes/`) — HTTP handling, parameter extraction, delegation\n-2. **Rules** (`src/rules/`) — pure business logic, no I/O\n-3. **Services** (`src/services/`) — persistence, external integrations, audit\n+1. **Routes** — HTTP handling, parameter extraction, delegation\n+2. **Rules** — pure business logic, no I/O\n+3. **Services** — persistence, external integrations, audit\n*** End Patch\n"
```

</details>

```
Modified 1 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md
```


---

<sub>⏱️ 1m 52s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "`[^`]+`|see `[^`]+`",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\lessons\\08-operating-model\\.github\\examples\\drifted\\copilot-instructions.md",
  "output_mode": "content",
  "-n": true,
  "head_limit": 100
}
```

</details>

<details>
<summary>11 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md:35:structured logging only; do not use `console.log()`.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md:39:- `const` over `let`; never `var`
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md:40:- All route handlers are `async`
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md:41:- All errors return structured JSON: `{ error: string, code: string }`
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md:46:- Annotate tests with `// FALSE POSITIVE` or `// HARD NEGATIVE` where applicable
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md:50:- Canonical project context: see `.github/copilot-instructions.md`
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md:51:- Clean example: see `.github/examples/clean/copilot-instructions.md`
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md:52:- Maintenance cadence: see `/docs/maintenance-schedule.md`
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md:53:- Lesson scope and expected output: see `/docs/operating-model-example.md`
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md:54:- Context audit: see `.github/scripts/audit_context.py`
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md:55:- Stale reference detector: see `.github/scripts/detect_stale_refs.py`
```

</details>


---

<sub>⏱️ 1m 52s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\08-operating-model\.github\examples\drifted\copilot-instructions.md

<details>
<summary>56 lines</summary>

```
1. # Loan Workbench — Project Context
2. 
3. > **This file shows the corrected version of the drifted example.**
4. > It now follows the clean example's structure and keeps references valid.
5. 
6. ## Project
7. 
8. Loan Workbench API — TypeScript + Express REST service managing loan
9. application lifecycles with regulatory compliance, role-based access, and
10. audit-first persistence.
11. 
12. ## Tech Stack
13. 
14. - Runtime: Node.js 20 LTS
15. - Language: TypeScript 5.x (strict mode)
16. - Framework: Express 4
17. - Tests: Vitest
18. - Modules: ESM only
19. - Logging: structured JSON via pino
20. - Database: Prisma ORM
21. - Deploy: Azure Container Apps
22. 
23. ## Architecture
24. 
25. Three-layer separation:
26. 
27. 1. **Routes** — HTTP handling, parameter extraction, delegation
28. 2. **Rules** — pure business logic, no I/O
29. 3. **Services** — persistence, external integrations, audit
30. 
31. Request flow: Route -> authenticate -> authorize -> validate -> Rule ->
32. Service -> respond.
33. 
34. Audit events are recorded before persistence. Mutating operations should use
35. structured logging only; do not use `console.log()`.
36. 
37. ## Coding Conventions
38. 
39. - `const` over `let`; never `var`
40. - All route handlers are `async`
41. - All errors return structured JSON: `{ error: string, code: string }`
42. - No stack traces in error responses
43. - Feature flags use 404, not 403
44. - Keep global instructions concise; detailed route, notification, and test
45.   patterns belong in scoped instructions or dedicated docs
46. - Annotate tests with `// FALSE POSITIVE` or `// HARD NEGATIVE` where applicable
47. 
48. ## References
49. 
50. - Canonical project context: see `.github/copilot-instructions.md`
51. - Clean example: see `.github/examples/clean/copilot-instructions.md`
52. - Maintenance cadence: see `/docs/maintenance-schedule.md`
53. - Lesson scope and expected output: see `/docs/operating-model-example.md`
54. - Context audit: see `.github/scripts/audit_context.py`
55. - Stale reference detector: see `.github/scripts/detect_stale_refs.py`
56.
```

</details>


---

<sub>⏱️ 2m 0s</sub>

### 💬 Copilot

Updated `.github/examples/drifted/copilot-instructions.md` to remove the drift and match the clean example’s concise structure.

I fixed stale tech references (`Node.js 20`, `pino`, `Prisma ORM`, `Azure Container Apps`), removed the contradictory logging guidance, deleted dead helpers/path references, and cut the oversized inline implementation blocks and over-scoped operational detail.

I also made the remaining references point to lesson artifacts that actually exist here, including the canonical instructions, clean example, maintenance docs, and audit scripts.

No shell commands or SQL were used.

---

<sub>Generated by [GitHub Copilot CLI](https://github.com/features/copilot/cli)</sub>
