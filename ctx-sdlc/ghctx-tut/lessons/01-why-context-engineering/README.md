# Lesson 01 — Why Context Engineering

[![Watch: Context Engineering for GitHub Copilot [Course Intro] | Lesson 01](https://img.youtube.com/vi/YBXo_hxr9k4/maxresdefault.jpg)](https://www.youtube.com/watch?v=YBXo_hxr9k4)

> <strong>Watch the video:</strong> <a href="https://www.youtube.com/watch?v=YBXo_hxr9k4" target="_blank" rel="noopener noreferrer">Context Engineering for GitHub Copilot [Course Intro] | Lesson 01</a>
> <strong>Website:</strong> <a href="https://tuts.localm.dev/" target="_blank" rel="noopener noreferrer">LocalM Tuts</a>
> <strong>Course Page:</strong> <a href="https://tuts.localm.dev/ctx-sdlc" target="_blank" rel="noopener noreferrer">Context Engineering for GitHub Copilot</a>

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** A weak or fast model only becomes repository-aware when the workspace exposes the right context.

## Setup

```bash
python with-context/util.py --setup
python without-context/util.py --setup
python with-context/util.py --run
python without-context/util.py --run
```

## What This Demonstrates

This lesson uses a hidden-spec workflow rather than a generic CRUD prompt.
The same short prompt is sent in two different workspace conditions:

| Scenario        | Context                                    | Expected Result                                           |
| --------------- | ------------------------------------------ | --------------------------------------------------------- |
| Without context | `src/` only or `src/` + `without-context/` | Plausible but repo-wrong implementation                   |
| With context    | `src/` + `with-context/`                   | Repository-aware implementation that follows hidden rules |

The prompt intentionally omits route shape, role restrictions, audit behavior,
queue contract usage, and California-specific nuance. Those rules live only in
the contextual folder.

This lesson is assessed comparatively rather than through a single prompt-scoped
CLI artifact bundle. See `COMPARE.md` and `ASSESSMENT.md` for the current
evaluation framing.

## Context Files

| Path                                            | Purpose                                |
| ----------------------------------------------- | -------------------------------------- |
| `with-context/.github/copilot-instructions.md`  | Project identity and behavioral rules  |
| `with-context/docs/architecture.md`             | System shape and domain constraints    |
| `with-context/docs/manual-review-escalation.md` | Hidden workflow specification          |
| `with-context/docs/experiment.md`               | Scoring rubric and evaluation guidance |

## Workspace Layout

```text
01-why-context-engineering/
  README.md
  CHAT.md
  CLI.md
  COMPARE.md
  compare_outputs.py
  with-context/
  without-context/
```

## Copilot CLI Workflow

Use this exact prompt in both runs:

```text
Implement the manual review escalation workflow for this repository.
Follow existing repo conventions and architecture.
Return the exact files you would change and the code for each change.
```

Baseline run:

```bash
cd without-context
copilot -p "Implement the manual review escalation workflow for this repository. Follow existing repo conventions and architecture. Return the exact files you would change and the code for each change." --allow-all-tools
```

Contextual run:

```bash
cd with-context
copilot -p "Implement the manual review escalation workflow for this repository. Follow existing repo conventions and architecture. Return the exact files you would change and the code for each change." --allow-all-tools
```

Notes:

- `copilot` uses prompt mode rather than separate `suggest` and `explain` commands.
- This lesson is still strongest in editor chat because it depends on workspace composition.
- Save outputs under `with-context/output/` and `without-context/output/`, then run `python compare_outputs.py`.

## VS Code Chat Workflow

Use the same prompt in both scenarios.

Without context:

- Open `src/` and optionally `without-context/`
- Do not open `with-context/`

With context:

- Open `src/` and `with-context/`
- Send the same prompt again

Expected difference:

- with context: route location, service split, delegated-session rules, audit behavior, queue contract reuse, and California high-risk subject prefix are discovered
- without context: the answer usually drifts into plausible but incorrect domain changes

To verify context loading, ask:

```text
What specific rules control the manual review escalation workflow in this repository?
```

## Cleanup

```bash
python with-context/util.py --clean
python without-context/util.py --clean
```

---

## Series Navigation

| #   | Lesson                    | Video                                                | Example Code                                                    |
| --- | ------------------------- | ---------------------------------------------------- | --------------------------------------------------------------- |
| 01  | Why Context Engineering   | [Watch](https://www.youtube.com/watch?v=YBXo_hxr9k4) | [01-why-context-engineering](../01-why-context-engineering)     |
| 02  | Curate Project Context    | _Coming soon_                                        | [02-curate-project-context](../02-curate-project-context)       |
| 03  | Instruction Architecture  | _Coming soon_                                        | [03-instruction-architecture](../03-instruction-architecture)   |
| 04  | Planning Workflows        | _Coming soon_                                        | [04-planning-workflows](../04-planning-workflows)               |
| 05  | Implementation Workflows  | _Coming soon_                                        | [05-implementation-workflows](../05-implementation-workflows)   |
| 06  | Tools and Guardrails      | _Coming soon_                                        | [06-tools-and-guardrails](../06-tools-and-guardrails)           |
| 07  | Surface Strategy          | _Coming soon_                                        | [07-surface-strategy](../07-surface-strategy)                   |
| 08  | Operating Model           | _Coming soon_                                        | [08-operating-model](../08-operating-model)                     |
| 09  | AI-Assisted SDLC Capstone | _Coming soon_                                        | [09-ai-assisted-sdlc-capstone](../09-ai-assisted-sdlc-capstone) |

Full Course: <https://tuts.localm.dev/ctx-sdlc>
