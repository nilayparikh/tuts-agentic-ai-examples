# Lesson 09 — AI-Assisted SDLC Capstone — Setup

## Prerequisites

- Node.js 20+
- Python 3.11+
- GitHub Copilot CLI (`copilot` v1.0.4+)

## Workspace Setup

```bash
# Set up stage 1 (Day One) — or any stage 1-5
python default.py --stage 1 --clean
cd src && npm install
```

This copies the **complex** template into `src/`, then applies cumulative stage
deltas from `stages/1-day-one/` through the requested stage.

## Stages

| Stage | Label     | Context Added                  |
| ----- | --------- | ------------------------------ |
| 1     | Day One   | `copilot-instructions.md` only |
| 2     | Week One  | + `.instructions.md` + `docs/` |
| 3     | Week Two  | + `.prompt.md` + ADRs          |
| 4     | Month One | + `.agent.md` + `SKILL.md`     |
| 5     | Mature    | + `mcp.json` + hooks + CLI     |

## Context Files

| Path                              | Purpose                               |
| --------------------------------- | ------------------------------------- |
| `.github/copilot-instructions.md` | Project identity (TaskFlow project)   |
| `docs/`                           | Architecture, conventions             |
| `stages/`                         | Cumulative context overlays per stage |

## Validation

```bash
# Run all 5 stages with the same prompt
python validate.py --all

# Run a specific stage
python validate.py --stage 3
```

The same prompt runs at each stage to demonstrate how progressive context
enrichment improves output quality. Outputs are written to `output/`.
