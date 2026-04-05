# Context Maintenance Schedule

Use this checklist to keep your AI context healthy over time.

## Weekly (5 minutes)

- [ ] Run `python scripts/audit_context.py` and fix any ERRORS
- [ ] Review any new team PRs that touched `.github/` or `docs/`
- [ ] If a dependency was updated, check if `copilot-instructions.md` mentions
      the old version

## Monthly (30 minutes)

- [ ] Run `python scripts/detect_stale_refs.py` and fix broken references
- [ ] Review instruction files for rules that are no longer needed
- [ ] Check for duplicate rules (same rule in `copilot-instructions.md` AND
      `.instructions.md` — deduplicate to the most appropriate location)
- [ ] Review agent tool lists — remove tools no longer relevant
- [ ] Check if any new ADRs should be documented
- [ ] Review prompt files — update variables if project structure changed

## Quarterly (1 hour)

- [ ] Full context audit:
  - Are the architecture docs still accurate?
  - Are the coding conventions still followed?
  - Have any technologies been replaced?
- [ ] Review the Context Health Metrics (see below)
- [ ] Prune dead context:
  - Features decommissioned but context remains
  - Deprecated APIs still referenced in docs
  - Agents for workflows no longer used
- [ ] Review `#file:` attachment patterns — are learners/developers attaching
      the right files, or struggling to find them?
- [ ] Update `copilot-instructions.md` references if new docs were added

## Context Health Metrics

Track these signals to measure context effectiveness:

### Leading Indicators (predict problems)

| Signal                          | How to Measure                              | Target        |
| ------------------------------- | ------------------------------------------- | ------------- |
| Instruction file size           | `wc -l .github/copilot-instructions.md`     | < 200 lines   |
| Cross-reference validity        | `python scripts/detect_stale_refs.py`       | 0 stale refs  |
| Context freshness               | `find .github docs -mtime +90 -name '*.md'` | 0 stale files |
| Agent tool restriction coverage | Agents with `tools:` / total agents         | 100%          |

### Lagging Indicators (confirm problems)

| Signal                          | How to Measure                                | Target     |
| ------------------------------- | --------------------------------------------- | ---------- |
| AI correction rate              | Count corrections in Copilot Chat per session | Decreasing |
| Convention violation rate       | Test failures due to wrong patterns           | Decreasing |
| "Ignore the instructions" rate  | Times users say "no, do it THIS way"          | Decreasing |
| Time to first useful suggestion | Minutes from opening Chat to usable code      | Decreasing |

### Red Flags

These signals indicate context rot:

- [ ] Developers frequently override AI suggestions with "actually, we do it THIS way"
- [ ] New team members get wrong answers about project architecture
- [ ] PRs contain patterns that were documented as rejected (e.g., Jest tests when Vitest is required)
- [ ] `copilot-instructions.md` exceeds 300 lines (needs splitting)
- [ ] Agents suggest tools that are no longer installed
- [ ] Prompt files reference variables/paths that have been renamed
