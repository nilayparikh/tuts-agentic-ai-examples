# 🤖 Copilot CLI Session

> [!NOTE]
> - **Session ID:** `e68da63f-dafa-4652-8f6e-e898fabe21e5`  
> - **Started:** 13/03/2026, 23:46:03  
> - **Duration:** 30s  
> - **Exported:** 13/03/2026, 23:46:33  

---

<sub>⏱️ 5s</sub>

### 👤 User

Read .github/copilot-instructions.md, .github/scripts/audit_context.py, .github/scripts/detect_stale_refs.py, .github/examples/clean/copilot-instructions.md, .github/examples/drifted/copilot-instructions.md, and docs/maintenance-schedule.md. Produce a read-only operating-model analysis for context maintenance. Return: summary, what kinds of drift the lesson is trying to catch, the most dangerous differences between the clean and drifted examples, one false positive, one hard negative, a maintenance cadence recommendation, and prioritized fixes. Explicitly call out copy-paste drift, stale references, contradictory rules, over-specification, and under-specification. Do not modify files, do not run shell commands, and do not use SQL or any other write-capable tools. Inspect and read only.

---

<sub>⏱️ 14s</sub>

### 💬 Copilot

I’m reading the requested context files and comparing the clean vs. drifted examples to produce a read-only operating-model analysis.

---

<sub>⏱️ 14s</sub>

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

<sub>⏱️ 14s</sub>

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

<sub>⏱️ 14s</sub>

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

<sub>⏱️ 14s</sub>

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

<sub>⏱️ 14s</sub>

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

<sub>⏱️ 14s</sub>

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

<sub>⏱️ 29s</sub>

### 💬 Copilot

**Summary:** The lesson defines context maintenance as an operating model: keep `.github/` and `docs/` synchronized with the real codebase, and use lightweight audits to catch rot before it degrades AI suggestions.

**Drift it’s trying to catch:** copy-paste drift, stale references, contradictory rules, over-specification, under-specification, oversized global instructions, missing scoped instruction metadata, over-privileged agents, broken internal links, and stale-but-unchanged context files.

**Most dangerous clean vs drifted differences:** wrong stack/platform facts (`Node 18` vs `20`, `winston` vs `pino`, `knex` vs `Prisma`, `AWS ECS` vs `Azure Container Apps`), wrong paths (`src/...` vs `app/backend/src/...`), and contradictory logging guidance (`structured logging only` vs `console.log()`).

**One false positive:** the 90-day freshness warning can flag accurate, intentionally stable docs.

**One hard negative:** the scripts won’t reliably catch semantically wrong-but-existing guidance, like outdated technology choices or contradictory behavior rules.

**Maintenance cadence:** weekly quick audit, monthly stale-reference/dedup review, quarterly deep review, plus event-driven checks after refactors, dependency/platform changes, or doc moves.

**Prioritized fixes:**  
1. Fix stale technology/path references.  
2. Remove contradictions.  
3. Split over-specified global rules into scoped `.instructions.md`.  
4. Deduplicate copy-pasted guidance.  
5. Tighten under-specified rules with short actionable constraints.

---

<sub>Generated by [GitHub Copilot CLI](https://github.com/features/copilot/cli)</sub>
