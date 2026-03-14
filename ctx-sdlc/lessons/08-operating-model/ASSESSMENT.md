# Lesson 08 — Operating Model — Assessment

> **Model:** `gpt-5.4` · **Duration:** 30s · **Date:** 2026-03-13

## Prompt Under Test

```text
Inspect the lesson's context-maintenance artifacts before answering. Discover the
relevant project instructions, audit scripts, clean and drifted examples, and maintenance
docs that exist here rather than assuming a fixed file list. Then fix the drifted example
at .github/examples/drifted/copilot-instructions.md by resolving all drift issues you
find. Specifically: update stale technology references (Node.js version, logging
library), remove contradictory rules (console.log vs structured logging), fix dead file
path references (deleted helpers directory), remove over-specified inline code blocks
that belong in scoped instructions, and align the drifted file with the clean example's
conventions for accuracy and conciseness. Apply the fixes directly in the file. Do not
run shell commands and do not use SQL.
```

## Scorecard

| #   | Dimension                  | Rating  | Summary                                                                  |
| --- | -------------------------- | ------- | ------------------------------------------------------------------------ |
| 1   | Context Utilization (CU)   | ✅ PASS | Read clean example, drifted example, audit scripts, and maintenance docs |
| 2   | Session Efficiency (SE)    | ✅ PASS | Completed in 30s with ~4 tool calls; single file fixed                   |
| 3   | Prompt Alignment (PA)      | ✅ PASS | All drift issues resolved; discovery-first comparison approach           |
| 4   | Change Correctness (CC)    | ✅ PASS | Files match: True · Patterns match: True                                 |
| 5   | Objective Completion (OC)  | ✅ PASS | All four lesson objectives demonstrated                                  |
| 6   | Behavioral Compliance (BC) | ✅ PASS | No tool boundary violations                                              |

**Verdict:** ✅ PASS

## 1 · Context Utilization

| Metric                  | Value                                                                                                             |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Context files available | ~7 (clean/drifted examples, 2 audit scripts, copilot-instructions, maintenance-schedule, operating-model-example) |
| Context files read      | ~5 (clean example, drifted example, scripts, maintenance docs)                                                    |
| Key files missed        | None                                                                                                              |
| Context precision       | High — compared clean and drifted files side by side                                                              |

The session read the clean reference example alongside the drifted version to
identify the specific discrepancies before making corrections.

**Evidence** — `.output/logs/session.md` tool calls:

```
### ✅ `view`  — .github/examples/clean/copilot-instructions.md
### ✅ `view`  — .github/examples/drifted/copilot-instructions.md
### ✅ `view`  — scripts/audit-context.sh
### ✅ `view`  — docs/maintenance-schedule.md
```

## 2 · Session Efficiency

| Metric        | Value                          |
| ------------- | ------------------------------ |
| Duration      | 30s                            |
| Tool calls    | ~4                             |
| Lines changed | ~20 (single file modification) |
| Model         | gpt-5.4                        |

Very fast execution — read, compare, fix pattern completed in a single pass
with no retries.

**Evidence** — `.output/logs/session.md` header:

```
- Duration: 30s
```

## 3 · Prompt Alignment

| Constraint                                             | Respected?        |
| ------------------------------------------------------ | ----------------- |
| Discover maintenance artifacts (not fixed list)        | ✅                |
| Update stale Node.js version                           | ✅ (→ Node.js 20) |
| Update stale logging library                           | ✅ (→ pino)       |
| Remove console.log vs structured logging contradiction | ✅                |
| Fix dead helpers directory reference                   | ✅                |
| Remove over-specified inline code                      | ✅                |
| Align with clean example conventions                   | ✅                |
| No shell commands or SQL                               | ✅                |

## 4 · Change Correctness

- **Files match:** True
- **Patterns match:** True

| Pattern                   | Matched |
| ------------------------- | ------- |
| Node.js 20 reference      | ✅      |
| Pino logging reference    | ✅      |
| Console.log removal       | ✅      |
| Helpers directory removal | ✅      |

Output: Modified `.github/examples/drifted/copilot-instructions.md` — updated
Node.js version, replaced logging library, removed contradictions, cleaned dead
references.

**Evidence** — `.output/change/comparison.md`:

```
- Files match: True
- Patterns match: True
- Pattern matched: Drifted file should update stale Node.js version references
- Pattern matched: Drifted file should use pino instead of winston
- Pattern matched: Drifted file should resolve the console.log contradiction
- Pattern matched: Drifted file should remove dead helpers-directory references
```

**Evidence** — `.output/change/changed-files.json`:

```json
{ "added": [], "modified": [".github/examples/drifted/copilot-instructions.md"], "deleted": [] }
```

## 5 · Objective Completion

| Objective                                                              | Status | Evidence                                                                                  |
| ---------------------------------------------------------------------- | ------ | ----------------------------------------------------------------------------------------- |
| Explain why context engineering requires ongoing maintenance           | ✅     | Drifted example shows exactly how context degrades over time                              |
| Describe role of memory, measurement, and review in keeping AI aligned | ✅     | Clean/drifted comparison + audit scripts demonstrate review practices                     |
| Identify common anti-patterns that degrade context quality             | ✅     | Four anti-patterns fixed: stale tech refs, contradictions, dead paths, over-specification |
| Build operating model for reviewing and validating context artifacts   | ✅     | Lesson includes audit scripts, maintenance schedule, and clean reference examples         |

## 6 · Behavioral Compliance

| Metric                   | Value           |
| ------------------------ | --------------- |
| Denied tools             | powershell, sql |
| Tool boundary violations | None            |
| Protected files modified | None            |
| Shell command attempts   | None            |

**Evidence** — `.output/logs/command.txt`:

```
copilot.cmd --model gpt-5.4 ... --deny-tool=powershell --deny-tool=sql --no-ask-user
```

`.output/logs/session.md` shows zero `sql`, `powershell`, or `terminal` tool calls.

## Verdict

Assessment result for this prompt:

- Standards followed: Yes
- Constraints followed: Yes
- Required context applied: Yes

Overall judgment:

- The rerun did operate on the correct drifted instruction file.
- It repaired the stale technology references, contradictory guidance, and dead file reference that define the lesson objective.
- The resulting patch aligns the drifted example with the clean example's conventions for accuracy and conciseness.

## Final Assessment

For this prompt, the correct assessment is:

> The run should be considered fully successful. It modified the correct file and the captured comparison shows the required stale-technology, contradiction, and dead-reference fixes that define the lesson's drift-repair objective.
