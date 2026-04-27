# Module Dependency Map

This map shows the intended direction of dependency after the refactor.

## Shared Layer

`shared/paths.py` and `shared/tracing.py` should stay dependency-light.

## Lesson 02 Core Data Flow

- `input_loader.py` reads raw records
- `date_normalizer.py` normalizes dates
- `mutation_playbook.py` classifies and repairs amount anomalies
- `export_writer.py` writes the canonical exports
- `clean_data_runtime.py` coordinates the full pass

## Wrapper Rule

Root files like `util.py`, `clean_data.py`, `clean_data_starter.py`, `prepare.py`, and `challenger.py` stay as learner-facing wrappers or compatibility entrypoints while logic moves into lesson modules.
