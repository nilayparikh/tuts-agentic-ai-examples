"""Finance-only dataset configuration for CleanLoop.

CleanLoop now teaches one arena all the way through: a messy finance invoice
ledger that the mutable genome must normalize into a single master CSV.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import cast

CLEANLOOP_DATASET_ENV = "CLEANLOOP_DATASET"
DEFAULT_DATASET = "finance"
AGENDA_PATH = Path(__file__).resolve().parent / "README.md"
TRACES_DIRNAME = "traces"
LOGS_DIRNAME = "logs"
RUNS_DIRNAME = "runs"
RUN_EVENTS_FILENAME = "run-events.jsonl"
ROW_DECISIONS_FILENAME = "row-decisions.jsonl"
PROPOSAL_EVENTS_FILENAME = "proposal-events.jsonl"
OTEL_SPANS_FILENAME = "otel-spans.jsonl"
OTEL_EVENTS_FILENAME = "otel-events.jsonl"
OTEL_LOGS_FILENAME = "otel-logs.jsonl"
RUN_MANIFEST_FILENAME = "run-manifest.json"
RUN_DIAGNOSTICS_FILENAME = "run-diagnostics.json"
STRATEGY_FILENAME = "finance_strategy.json"
CHALLENGE_MANIFEST_FILENAME = "challenge_manifest.json"

FINANCE_COLUMNS = ("date", "entity", "currency", "value", "category")
FAILURE_COLUMNS = (
    "source_file",
    "invoice_id",
    "customer",
    "raw_date",
    "raw_amount",
    "currency",
    "status",
    "anomaly_reason",
    "mutation_hint",
)
MUTATION_RULES = (
    {
        "token": "FREE TRIAL",
        "route": "finance_mutation_success.csv",
        "strategy": "resolution_amount",
        "action": (
            "Use resolution_amount as the final numeric value when the trial "
            "conversion is approved."
        ),
        "mutation_hint": (
            "Read resolution_amount and resolution_flag to recover the approved "
            "post-trial invoice value."
        ),
    },
    {
        "token": "COMPLIMENTARY",
        "route": "finance_mutation_success.csv",
        "strategy": "resolution_amount",
        "action": (
            "Use resolution_amount as the final numeric value when the "
            "complimentary invoice is reclassified and approved."
        ),
        "mutation_hint": (
            "Read resolution_amount and resolution_flag to recover the approved "
            "billable amount."
        ),
    },
    {
        "token": "OFFSET",
        "route": "finance_mutation_success.csv",
        "strategy": "resolution_amount",
        "action": (
            "Use resolution_amount as the signed offset value when the dispute "
            "resolution is approved."
        ),
        "mutation_hint": (
            "Read resolution_amount and resolution_flag to recover the approved "
            "offset amount."
        ),
    },
    {
        "token": "DISCOUNTED",
        "route": "finance_mutation_success.csv",
        "strategy": "adjusted_amount",
        "action": (
            "Use adjusted_amount as the final numeric value when the adjustment is approved."
        ),
        "mutation_hint": (
            "Read adjusted_amount and approval_flag to recover the approved discounted value."
        ),
    },
    {
        "token": "FX HOLD",
        "route": "finance_mutation_success.csv",
        "strategy": "adjusted_amount",
        "action": (
            "Use adjusted_amount as the final numeric value when the FX update is approved."
        ),
        "mutation_hint": (
            "Read adjusted_amount and approval_flag to recover the approved FX-adjusted value."
        ),
    },
    {
        "token": "REVERSAL",
        "route": "finance_mutation_success.csv",
        "strategy": "adjusted_amount",
        "action": (
            "Use adjusted_amount as the signed reversal value when the adjustment is approved."
        ),
        "mutation_hint": (
            "Read adjusted_amount and approval_flag to recover the approved signed reversal value."
        ),
    },
    {
        "token": "HOLDBACK RELEASE",
        "route": "finance_mutation_success.csv",
        "strategy": "adjusted_amount",
        "action": (
            "Use adjusted_amount as the final billed value when the holdback release is approved."
        ),
        "mutation_hint": (
            "Read adjusted_amount and approval_flag to recover the approved "
            "holdback release amount."
        ),
    },
    {
        "token": "CREDIT SWAP",
        "route": "finance_mutation_success.csv",
        "strategy": "adjusted_amount",
        "action": (
            "Use adjusted_amount as the signed reclassification value when the "
            "credit swap is approved."
        ),
        "mutation_hint": (
            "Read adjusted_amount and approval_flag to recover the approved "
            "signed credit-swap value."
        ),
    },
    {
        "token": "RESOLUTION_AMOUNT",
        "route": "finance_mutation_success.csv",
        "strategy": "resolution_amount",
        "action": (
            "Use resolution_amount as the final numeric value when resolution_flag is approved."
        ),
        "mutation_hint": (
            "Read resolution_amount and resolution_flag to recover the analyst-approved amount."
        ),
    },
    {
        "token": "PRO FORMA",
        "route": "finance_mutation_success.csv",
        "strategy": "resolution_amount",
        "action": (
            "Use resolution_amount as the final numeric value when the pro forma "
            "invoice is approved."
        ),
        "mutation_hint": (
            "Read resolution_amount and resolution_flag to recover the approved pro forma amount."
        ),
    },
    {
        "token": "BLANK_CANCELLED_OR_VOID",
        "route": "finance_mutation_success.csv",
        "strategy": "zero_value",
        "statuses": ("cancelled", "void"),
        "action": (
            "Write value 0.0 when amount is blank and the invoice status is cancelled or void."
        ),
        "mutation_hint": (
            "Map blank cancelled or void invoices to 0.0 and preserve the status."
        ),
    },
)
UNRESOLVED_MUTATION_TOKEN_GROUP = "PENDING / TBD / ERROR / ERR / CHARGEBACK"
UNRESOLVED_MUTATION_ACTION = (
    "Dump the unresolved row for later mutation review when no shipped rule or "
    "resolution metadata applies."
)


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
    required_columns=FINANCE_COLUMNS,
    row_count_range=(78, 80),
    goal=(
        "Run a deterministic finance cleaning pass, then export mutation successes "
        "and unresolved failures beside the canonical master CSV."
    ),
    requirements=(
        "Use only the five finance_*.csv inputs.",
        "Write finance_master.csv with date, entity, currency, value, category.",
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
    shipped_paths = [input_dir / filename for filename in config.input_filenames]
    return [*shipped_paths, *get_challenge_input_paths(input_dir)]


def get_shipped_input_paths(
    input_dir: Path,
    dataset_name: str | None = None,
) -> list[Path]:
    """Return only the fixed course input CSV files."""
    config = get_dataset_config(dataset_name)
    return [input_dir / filename for filename in config.input_filenames]


def get_challenge_input_paths(input_dir: Path) -> list[Path]:
    """Return generated adversarial CSV files that are active in the arena."""
    return sorted(input_dir.glob("adversarial_d*.csv"))


def get_challenge_manifest_path(output_dir: Path) -> Path:
    """Return the generated challenge manifest artifact path."""
    return output_dir / CHALLENGE_MANIFEST_FILENAME


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


def get_strategy_path(output_dir: Path, dataset_name: str | None = None) -> Path:
    """Return the finance strategy snapshot path."""
    _ = get_dataset_config(dataset_name)
    return output_dir / STRATEGY_FILENAME


def get_runs_dir(output_dir: Path) -> Path:
    """Return the directory that stores per-run snapshots."""
    return output_dir / RUNS_DIRNAME


def get_run_instance_dir(output_dir: Path, run_instance: str) -> Path:
    """Return the storage directory for one run instance."""
    return get_runs_dir(output_dir) / run_instance


def get_run_manifest_path(output_dir: Path, run_instance: str) -> Path:
    """Return the manifest path for one run instance."""
    return get_run_instance_dir(output_dir, run_instance) / RUN_MANIFEST_FILENAME


def get_run_diagnostics_path(output_dir: Path, run_instance: str) -> Path:
    """Return the diagnostics path for one run instance."""
    return get_run_instance_dir(output_dir, run_instance) / RUN_DIAGNOSTICS_FILENAME


def get_run_history_path(
    output_dir: Path,
    run_instance: str,
    dataset_name: str | None = None,
) -> Path:
    """Return the per-run eval-history snapshot path."""
    config = get_dataset_config(dataset_name)
    return get_run_instance_dir(output_dir, run_instance) / config.history_filename


def get_run_strategy_path(
    output_dir: Path,
    run_instance: str,
    dataset_name: str | None = None,
) -> Path:
    """Return the per-run strategy snapshot path."""
    _ = get_dataset_config(dataset_name)
    return get_run_instance_dir(output_dir, run_instance) / STRATEGY_FILENAME


def get_run_output_path(
    output_dir: Path,
    run_instance: str,
    dataset_name: str | None = None,
) -> Path:
    """Return the per-run master CSV snapshot path."""
    config = get_dataset_config(dataset_name)
    return get_run_instance_dir(output_dir, run_instance) / config.output_filename


def get_run_mutation_success_path(
    output_dir: Path,
    run_instance: str,
    dataset_name: str | None = None,
) -> Path:
    """Return the per-run mutation-success snapshot path."""
    config = get_dataset_config(dataset_name)
    return (
        get_run_instance_dir(output_dir, run_instance)
        / config.mutation_success_filename
    )


def get_run_mutation_failures_path(
    output_dir: Path,
    run_instance: str,
    dataset_name: str | None = None,
) -> Path:
    """Return the per-run mutation-failure snapshot path."""
    config = get_dataset_config(dataset_name)
    return (
        get_run_instance_dir(output_dir, run_instance)
        / config.mutation_failures_filename
    )


def get_run_output_artifact_paths(
    output_dir: Path,
    run_instance: str,
    dataset_name: str | None = None,
) -> tuple[Path, Path, Path]:
    """Return per-run master, mutation-success, and mutation-failure paths."""
    return (
        get_run_output_path(output_dir, run_instance, dataset_name),
        get_run_mutation_success_path(output_dir, run_instance, dataset_name),
        get_run_mutation_failures_path(output_dir, run_instance, dataset_name),
    )


def get_traces_dir(output_dir: Path) -> Path:
    """Return the shared trace export directory."""
    return output_dir / TRACES_DIRNAME


def get_run_traces_dir(output_dir: Path, run_instance: str) -> Path:
    """Return the per-run trace export directory."""
    return get_run_instance_dir(output_dir, run_instance) / TRACES_DIRNAME


def _trace_file_path(output_dir: Path, filename: str, run_instance: str | None) -> Path:
    """Return one global or per-run trace file path."""
    if run_instance is not None:
        return get_run_traces_dir(output_dir, run_instance) / filename
    return get_traces_dir(output_dir) / filename


def get_run_events_path(output_dir: Path, run_instance: str | None = None) -> Path:
    """Return the run-level trace export path."""
    return _trace_file_path(output_dir, RUN_EVENTS_FILENAME, run_instance)


def get_row_decisions_path(output_dir: Path, run_instance: str | None = None) -> Path:
    """Return the row-decision trace export path."""
    return _trace_file_path(output_dir, ROW_DECISIONS_FILENAME, run_instance)


def get_proposal_events_path(output_dir: Path, run_instance: str | None = None) -> Path:
    """Return the proposal-event trace export path."""
    return _trace_file_path(output_dir, PROPOSAL_EVENTS_FILENAME, run_instance)


def get_otel_spans_path(output_dir: Path, run_instance: str | None = None) -> Path:
    """Return the OTEL-style span export path."""
    return _trace_file_path(output_dir, OTEL_SPANS_FILENAME, run_instance)


def get_otel_events_path(output_dir: Path, run_instance: str | None = None) -> Path:
    """Return the OTEL-style event export path."""
    return _trace_file_path(output_dir, OTEL_EVENTS_FILENAME, run_instance)


def get_otel_logs_path(output_dir: Path, run_instance: str | None = None) -> Path:
    """Return the OTEL-style log export path."""
    return _trace_file_path(output_dir, OTEL_LOGS_FILENAME, run_instance)


def get_logs_dir(output_dir: Path) -> Path:
    """Return the exported loop-log directory."""
    return output_dir / LOGS_DIRNAME


def get_exported_logs_path(
    output_dir: Path,
    dataset_name: str | None = None,
    run_instance: str | None = None,
) -> Path:
    """Return the raw loop-log export path used by the dashboard."""
    config = get_dataset_config(dataset_name)
    logs_dir = (
        get_run_instance_dir(output_dir, run_instance) / LOGS_DIRNAME
        if run_instance is not None
        else get_logs_dir(output_dir)
    )
    return logs_dir / f"{config.name}_round_logs.jsonl"


def get_reference_path(reference_dir: Path, dataset_name: str | None = None) -> Path:
    """Return the finance reference CSV path."""
    config = get_dataset_config(dataset_name)
    return reference_dir / config.reference_filename


def build_program_text(dataset_name: str | None = None) -> str:
    """Load the CleanLoop agenda text from the example README."""
    _ = get_dataset_config(dataset_name)
    return AGENDA_PATH.read_text(encoding="utf-8").strip()


def get_failure_columns() -> tuple[str, ...]:
    """Return the canonical mutation-failure dump schema."""
    return FAILURE_COLUMNS


def get_mutation_rule_lookup() -> dict[str, dict[str, object]]:
    """Return the shipped mutation rules keyed by raw amount token."""
    return {cast(str, rule["token"]): dict(rule) for rule in MUTATION_RULES}


def build_export_contract(dataset_name: str | None = None) -> tuple[str, ...]:
    """Return the stable export-contract lines used by prompts and docs."""
    config = get_dataset_config(dataset_name)
    return (
        f"{config.output_filename} stores deterministic rows plus mutation-fixed rows.",
        (
            f"{config.mutation_success_filename} stores only the rows fixed by the "
            "mutation playbook."
        ),
        f"{config.mutation_failures_filename} stores unresolved anomaly rows for review.",
    )


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
            "description": (
                "Mutation success report uses date, entity, currency, value, category"
            ),
        },
        {
            "name": "mutation_success_rows_in_master",
            "severity": "critical",
            "description": (
                "Every mutation-success row is also present in finance_master.csv"
            ),
        },
        {
            "name": "can_read_mutation_failures_output",
            "severity": "critical",
            "description": "Mutation failure dump exists and is valid CSV",
        },
        {
            "name": "mutation_failures_has_required_columns",
            "severity": "critical",
            "description": (
                "Mutation failure dump uses the canonical failure-sidecar schema"
            ),
        },
        {
            "name": "mutation_failures_have_diagnostics",
            "severity": "high",
            "description": (
                "Mutation failure rows keep source, invoice, amount, and anomaly details"
            ),
        },
        {
            "name": "can_read_output",
            "severity": "critical",
            "description": "Output file exists and is valid CSV",
        },
        {
            "name": "has_required_columns",
            "severity": "critical",
            "description": "Output has date, entity, currency, value, category columns",
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
    playbook: list[dict[str, str]] = [
        {
            "token": cast(str, rule["token"]),
            "route": cast(str, rule["route"]),
            "action": cast(str, rule["action"]),
        }
        for rule in MUTATION_RULES
    ]
    playbook.append(
        {
            "token": UNRESOLVED_MUTATION_TOKEN_GROUP,
            "route": "finance_mutation_failures.csv",
            "action": UNRESOLVED_MUTATION_ACTION,
        }
    )
    return playbook
