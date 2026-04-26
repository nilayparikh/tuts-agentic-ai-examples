"""Finance-only dataset configuration for CleanLoop.

CleanLoop now teaches one arena all the way through: a messy finance invoice
ledger that the mutable genome must normalize into a single master CSV.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


CLEANLOOP_DATASET_ENV = "CLEANLOOP_DATASET"
DEFAULT_DATASET = "finance"
AGENDA_PATH = Path(__file__).resolve().parent / "README.md"


@dataclass(frozen=True)
class DatasetConfig:
    """Describe the single CleanLoop arena."""

    name: str
    label: str
    input_filenames: tuple[str, ...]
    reference_filename: str
    output_filename: str
    mutation_success_filename: str
    mutation_failures_filename: str
    history_filename: str
    required_columns: tuple[str, ...]
    row_count_range: tuple[int, int]
    goal: str
    requirements: tuple[str, ...]


FINANCE_CONFIG = DatasetConfig(
    name="finance",
    label="Finance Invoice Ledger",
    input_filenames=(
        "finance_invoices.csv",
        "finance_invoices_flags.csv",
        "finance_invoices_regional.csv",
        "finance_invoices_collections.csv",
        "finance_invoices_adjustments.csv",
    ),
    reference_filename="finance_expected.csv",
    output_filename="finance_master.csv",
    mutation_success_filename="finance_mutation_success.csv",
    mutation_failures_filename="finance_mutation_failures.csv",
    history_filename="finance_eval_history.json",
    required_columns=("date", "entity", "value", "category"),
    row_count_range=(50, 120),
    goal=(
        "Run a deterministic finance cleaning pass, then export mutation successes "
        "and unresolved failures beside the canonical master CSV."
    ),
    requirements=(
        "Use only the five finance_*.csv inputs.",
        "Write finance_master.csv with date, entity, value, category.",
        "Write finance_mutation_success.csv with the same canonical schema.",
        "Write finance_mutation_failures.csv as the unresolved anomaly dump.",
        "Preserve good rows even when amount strings contain symbols, sentinels, or notes.",
        "Handle mixed date formats without inventing or dropping records.",
        "Match the canonical finance reference in cleanloop/.gold/finance_expected.csv.",
    ),
)


DATASET_CONFIGS: dict[str, DatasetConfig] = {FINANCE_CONFIG.name: FINANCE_CONFIG}


def get_dataset_choices() -> tuple[str, ...]:
    """Return the supported CleanLoop dataset names."""
    return (FINANCE_CONFIG.name,)


def get_dataset_config(name: str | None = None) -> DatasetConfig:
    """Return the finance config and reject removed dataset names."""
    selected = DEFAULT_DATASET if name is None else name
    if selected != FINANCE_CONFIG.name:
        raise ValueError(
            "Unknown CleanLoop dataset "
            f"'{selected}'. Choose from: {FINANCE_CONFIG.name}"
        )
    return FINANCE_CONFIG


def detect_dataset_from_output_path(output_path: Path) -> str:
    """Treat every CleanLoop output as the finance arena."""
    _ = output_path
    return FINANCE_CONFIG.name


def get_input_paths(input_dir: Path, dataset_name: str | None = None) -> list[Path]:
    """Return the ordered finance input files."""
    config = get_dataset_config(dataset_name)
    return [input_dir / filename for filename in config.input_filenames]


def get_output_path(output_dir: Path, dataset_name: str | None = None) -> Path:
    """Return the finance output CSV path."""
    config = get_dataset_config(dataset_name)
    return output_dir / config.output_filename


def get_mutation_success_path(
    output_dir: Path, dataset_name: str | None = None
) -> Path:
    """Return the finance mutation-success report path."""
    config = get_dataset_config(dataset_name)
    return output_dir / config.mutation_success_filename


def get_mutation_failures_path(
    output_dir: Path, dataset_name: str | None = None
) -> Path:
    """Return the finance mutation-failure report path."""
    config = get_dataset_config(dataset_name)
    return output_dir / config.mutation_failures_filename


def get_output_artifact_paths(
    output_dir: Path, dataset_name: str | None = None
) -> tuple[Path, Path, Path]:
    """Return the finance master plus both mutation sidecar paths."""
    return (
        get_output_path(output_dir, dataset_name),
        get_mutation_success_path(output_dir, dataset_name),
        get_mutation_failures_path(output_dir, dataset_name),
    )


def get_history_path(output_dir: Path, dataset_name: str | None = None) -> Path:
    """Return the finance eval-history path."""
    config = get_dataset_config(dataset_name)
    return output_dir / config.history_filename


def get_reference_path(reference_dir: Path, dataset_name: str | None = None) -> Path:
    """Return the finance reference CSV path."""
    config = get_dataset_config(dataset_name)
    return reference_dir / config.reference_filename


def build_program_text(dataset_name: str | None = None) -> str:
    """Load the CleanLoop agenda text from the example README."""
    _ = get_dataset_config(dataset_name)
    return AGENDA_PATH.read_text(encoding="utf-8").strip()


def build_assertion_registry(dataset_name: str | None = None) -> list[dict[str, str]]:
    """Return the finance assertion registry used in prompts and docs."""
    _ = get_dataset_config(dataset_name)
    return [
        {
            "name": "can_read_mutation_success_output",
            "severity": "critical",
            "description": "Mutation success report exists and is valid CSV",
        },
        {
            "name": "mutation_success_has_required_columns",
            "severity": "critical",
            "description": "Mutation success report uses date, entity, value, category",
        },
        {
            "name": "can_read_mutation_failures_output",
            "severity": "critical",
            "description": "Mutation failure dump exists and is valid CSV",
        },
        {
            "name": "can_read_output",
            "severity": "critical",
            "description": "Output file exists and is valid CSV",
        },
        {
            "name": "has_required_columns",
            "severity": "critical",
            "description": "Output has date, entity, value, category columns",
        },
        {
            "name": "value_is_numeric",
            "severity": "critical",
            "description": "Value column contains only numeric values",
        },
        {
            "name": "date_is_parseable",
            "severity": "critical",
            "description": "Every date value can be parsed to a datetime",
        },
        {
            "name": "no_nan_date",
            "severity": "high",
            "description": "Zero NaN values in date",
        },
        {
            "name": "no_nan_entity",
            "severity": "high",
            "description": "Zero NaN values in entity",
        },
        {
            "name": "no_nan_value",
            "severity": "high",
            "description": "Zero NaN values in value",
        },
        {
            "name": "matches_reference_output",
            "severity": "medium",
            "description": (
                "Output should match the canonical cleaned finance reference without "
                "dropping or inventing rows."
            ),
        },
    ]


def build_mutation_playbook(dataset_name: str | None = None) -> list[dict[str, str]]:
    """Return the shipped mutation rules for known finance amount anomalies."""
    _ = get_dataset_config(dataset_name)
    return [
        {
            "token": "FREE TRIAL",
            "route": "finance_mutation_success.csv",
            "action": "Write value 0.0 and preserve the existing active category.",
        },
        {
            "token": "COMPLIMENTARY",
            "route": "finance_mutation_success.csv",
            "action": "Write value 0.0 and preserve the existing active category.",
        },
        {
            "token": "OFFSET",
            "route": "finance_mutation_success.csv",
            "action": "Write value 0.0 and preserve the disputed category.",
        },
        {
            "token": "PENDING / TBD / ERROR / ERR / CHARGEBACK / REVERSAL",
            "route": "finance_mutation_failures.csv",
            "action": "Dump the unresolved row for later mutation review when no rule applies.",
        },
    ]
