# Reset and Recovery

Reset is part of Lesson 07 because recovery is a production control, not a convenience feature.

## Current Reset Rule

`python util.py reset` restores `clean_data.py` from `clean_data_starter.py` and preserves `.output/`.

That means learners can inspect the shipped sample artifacts even after a reset.

## Why This Matters

If reset deleted the sample outputs, the example would become harder to trust.
The learner would lose the exact artifacts that explain the current export contract.

## Current Implementation Split

- CLI entry: [util.py#L457](../../util.py#L457)
- recovery workflow: [reset_workflow.py#L9](../../reset_workflow.py#L9)
