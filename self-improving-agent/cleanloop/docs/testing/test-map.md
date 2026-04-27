# Test Map

The CleanLoop refactor is governed by three main test surfaces.

## Export Contract

`tests/test_cleanloop_exports.py`

Use this file when you change:

- finance fixture semantics
- mutation playbook behavior
- export partitioning
- output counts

## Compatibility and Regression Coverage

`tests/test_python_compat.py`

Use this file when you change:

- CLI behavior
- reset semantics
- reference output alignment
- loop compatibility
- dashboard metrics

## Structure and Packaging

`tests/test_cleanloop_course_structure.py`

Use this file when you change:

- docs placement
- standalone project packaging
- lesson-mapped package layout
- trace artifacts
