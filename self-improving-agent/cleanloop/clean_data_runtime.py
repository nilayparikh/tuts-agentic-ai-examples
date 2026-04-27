"""Shared finance cleaning runtime for the CleanLoop starter and mutable genome."""

from __future__ import annotations

from pathlib import Path

from cleanloop import datasets as cleanloop_datasets
from cleanloop.dataset_contract import FAILURE_COLUMNS
from cleanloop.export_writer import write_rows
from cleanloop.input_loader import read_finance_records
from cleanloop.mutation_playbook import (
    apply_mutation_playbook,
    build_failure_row,
    build_normalized_row,
    normalize_numeric_amount,
)
from cleanloop.tracing import TraceRecorder


# =====================================================================
# SECTION: Finance Cleaning Runtime
# This file stays as the learner-facing pipeline entrypoint. The helper
# modules now use flat, job-based names so readers can follow the runtime
# without translating lesson-folder indirection first.
# =====================================================================


def _clean_impl(input_dir: Path, output_path: Path, *, allow_mutations: bool) -> None:
    """Run the finance cleaner with optional mutation-playbook support."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    config = cleanloop_datasets.get_dataset_config()
    success_path = cleanloop_datasets.get_mutation_success_path(output_path.parent)
    failure_path = cleanloop_datasets.get_mutation_failures_path(output_path.parent)
    trace = TraceRecorder(output_dir=output_path.parent, component="clean_data_runtime")
    trace.record_run_event(
        stage="clean-start",
        decision="begin",
        dataset=config.name,
        allow_mutations=allow_mutations,
        output_file=output_path.name,
    )

    deterministic_rows: list[dict[str, str]] = []
    mutation_rows: list[dict[str, str]] = []
    failure_rows: list[dict[str, str]] = []

    for csv_file in cleanloop_datasets.get_input_paths(input_dir):
        trace.record_run_event(
            stage="input-file",
            decision="scan",
            source_file=csv_file.name,
        )
        for record in read_finance_records(csv_file):
            value, anomaly_reason = normalize_numeric_amount(record)
            if value is not None:
                row = build_normalized_row(record, value)
                if row is not None:
                    deterministic_rows.append(row)
                    trace.record_row_decision(
                        stage="deterministic-pass",
                        decision="deterministic_row",
                        invoice_id=record["invoice_id"],
                        source_file=record["source_file"],
                        value=row["value"],
                        category=row["category"],
                    )
                    continue
                failure_rows.append(
                    build_failure_row(
                        record,
                        "unparseable_date",
                        "Normalize the issued date before exporting the canonical row.",
                    )
                )
                trace.record_row_decision(
                    stage="deterministic-pass",
                    decision="failure_unparseable_date",
                    invoice_id=record["invoice_id"],
                    source_file=record["source_file"],
                    anomaly_reason="unparseable_date",
                )
                continue

            if not allow_mutations:
                failure_rows.append(
                    build_failure_row(
                        record,
                        anomaly_reason or "unmapped_amount_token",
                        "Starter genome stops at the deterministic pass.",
                    )
                )
                trace.record_row_decision(
                    stage="starter-stop",
                    decision="requires_mutation_playbook",
                    invoice_id=record["invoice_id"],
                    source_file=record["source_file"],
                    anomaly_reason=anomaly_reason or "unmapped_amount_token",
                )
                continue

            mutated_row, mutation_reason, mutation_hint = apply_mutation_playbook(
                record
            )
            if mutated_row is not None:
                mutation_rows.append(mutated_row)
                trace.record_row_decision(
                    stage="mutation-playbook",
                    decision="mutation_fixed",
                    invoice_id=record["invoice_id"],
                    source_file=record["source_file"],
                    value=mutated_row["value"],
                    category=mutated_row["category"],
                )
                continue

            failure_rows.append(
                build_failure_row(
                    record,
                    anomaly_reason or mutation_reason,
                    mutation_hint,
                )
            )
            trace.record_row_decision(
                stage="mutation-playbook",
                decision="mutation_failure",
                invoice_id=record["invoice_id"],
                source_file=record["source_file"],
                anomaly_reason=anomaly_reason or mutation_reason,
            )

    master_rows = deterministic_rows + mutation_rows
    write_rows(output_path, master_rows, config.required_columns)
    write_rows(
        success_path,
        mutation_rows,
        config.required_columns,
        prioritize_non_zero=True,
    )
    write_rows(failure_path, failure_rows, FAILURE_COLUMNS)
    trace.record_run_event(
        stage="clean-finish",
        decision="written",
        deterministic_rows=len(deterministic_rows),
        mutation_rows=len(mutation_rows),
        failure_rows=len(failure_rows),
        master_rows=len(master_rows),
    )


def clean(input_dir: Path, output_path: Path) -> None:
    """Run the shipped deterministic-plus-mutation export pipeline."""
    _clean_impl(input_dir, output_path, allow_mutations=True)


def clean_starter(input_dir: Path, output_path: Path) -> None:
    """Run only the deterministic stage so the loop still has mutation work to do."""
    _clean_impl(input_dir, output_path, allow_mutations=False)
