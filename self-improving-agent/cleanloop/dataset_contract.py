"""Shared finance dataset constants used by the cleaning runtime."""

from __future__ import annotations

from cleanloop import datasets as cleanloop_datasets


FINANCE_COLUMNS = cleanloop_datasets.FINANCE_COLUMNS
FAILURE_COLUMNS = cleanloop_datasets.get_failure_columns()
MUTATION_RULES = cleanloop_datasets.get_mutation_rule_lookup()


def get_dataset_config() -> cleanloop_datasets.DatasetConfig:
    """Return the active dataset configuration for the current CleanLoop run."""
    return cleanloop_datasets.get_dataset_config()
