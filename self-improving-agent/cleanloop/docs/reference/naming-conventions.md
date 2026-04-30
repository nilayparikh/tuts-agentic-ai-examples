# Naming Conventions

The course title is `Building the Self-Evolving Data Engineer`.

## Folder Mapping Rule

- course slug: `self-evolving-data-engineer`
- runnable example root: `cleanloop/`
- core lesson notes: `docs/lessons/01-mutation-engine.md` through `docs/lessons/07-production-safety.md`
- companion lesson notes: `docs/lessons/08-dashboard-human-oversight.md` and `docs/lessons/09-autonomy-ladder.md`
- Python helpers: flat, root-level snake_case files named after the job they do

## File Naming Rules

Python files use snake case and name the job they do.

Examples:

- `status_snapshot.py`
- `input_loader.py`
- `mutation_playbook.py`
- `history_store.py`
- `reset_workflow.py`

Markdown lesson files use the course slug style.

Examples:

- `docs/lessons/01-mutation-engine.md`
- `docs/lessons/06-test-time-search.md`
- `docs/lessons/08-dashboard-human-oversight.md`
- `docs/lessons/09-autonomy-ladder.md`
