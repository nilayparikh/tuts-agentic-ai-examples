# pyright: reportMissingImports=false, reportMissingModuleSource=false
# mypy: disable-error-code=import-not-found
# pylint: disable=import-error

"""Regression tests for the CleanLoop finance export contract."""

from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from importlib import import_module
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from cleanloop import datasets as cleanloop_datasets


def _read_rows(csv_path: Path) -> tuple[list[str], list[dict[str, str]]]:
    """Read one CSV file into headers plus row dictionaries."""
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        return list(reader.fieldnames or []), rows


class CleanLoopExportContractTests(unittest.TestCase):
    """Verify the finance cleaner emits deterministic and mutation artifacts."""

    def test_shipped_clean_data_module_matches_reference_output(self) -> None:
        """Ship the full cleaner, not the starter genome, in clean_data.py."""
        clean_data = import_module("cleanloop.clean_data")
        prepare = import_module("cleanloop.prepare")
        input_dir = PROJECT_ROOT / "cleanloop" / ".input"

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            master_path = cleanloop_datasets.get_output_path(output_dir)

            clean_data.clean(input_dir, master_path)

            results = prepare.evaluate(master_path)
            self.assertEqual(results["score"], results["total"])

    def test_starter_genome_requires_contextual_mutation_repairs(self) -> None:
        """Keep the starter genome incomplete so the loop has real work to do."""
        clean_data_starter = import_module("cleanloop.clean_data_starter")
        prepare = import_module("cleanloop.prepare")
        input_dir = PROJECT_ROOT / "cleanloop" / ".input"

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            master_path = cleanloop_datasets.get_output_path(output_dir)
            success_path = cleanloop_datasets.get_mutation_success_path(output_dir)
            failure_path = cleanloop_datasets.get_mutation_failures_path(output_dir)

            clean_data_starter.clean(input_dir, master_path)

            results = prepare.evaluate(master_path)
            _, success_rows = _read_rows(success_path)
            _, failure_rows = _read_rows(failure_path)

            self.assertLess(results["score"], results["total"])
            self.assertTrue(
                any(
                    item.startswith("matches_reference_output:")
                    for item in results["failed"]
                )
            )
            self.assertFalse(success_rows)
            failure_lookup = {
                (
                    row.get("invoice_id", ""),
                    row.get("anomaly_reason", ""),
                )
                for row in failure_rows
            }
            self.assertIn(("INV-502", "requires_mutation_playbook"), failure_lookup)
            self.assertIn(("INV-404", "requires_mutation_playbook"), failure_lookup)

    def test_clean_pipeline_writes_master_success_and_failure_exports(self) -> None:
        """Write three exports and partition fixed versus failed anomalies."""
        clean_data_runtime = import_module("cleanloop.clean_data_runtime")
        input_dir = PROJECT_ROOT / "cleanloop" / ".input"

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            master_path = cleanloop_datasets.get_output_path(output_dir)
            success_path = output_dir / "finance_mutation_success.csv"
            failure_path = output_dir / "finance_mutation_failures.csv"

            clean_data_runtime.clean(input_dir, master_path)

            self.assertTrue(master_path.exists())
            self.assertTrue(success_path.exists())
            self.assertTrue(failure_path.exists())

            expected_columns = ["date", "entity", "currency", "value", "category"]
            master_headers, master_rows = _read_rows(master_path)
            success_headers, success_rows = _read_rows(success_path)
            failure_headers, failure_rows = _read_rows(failure_path)

            self.assertEqual(master_headers, expected_columns)
            self.assertEqual(success_headers, expected_columns)
            self.assertIn("source_file", failure_headers)
            self.assertIn("invoice_id", failure_headers)
            self.assertIn("raw_amount", failure_headers)
            self.assertIn("anomaly_reason", failure_headers)

            self.assertTrue(success_rows)
            self.assertTrue(failure_rows)

            for row in success_rows:
                for column in expected_columns:
                    self.assertTrue(
                        row[column].strip(), f"blank {column} in success row"
                    )

            master_lookup = {
                (
                    row["date"],
                    row["entity"],
                    row["currency"],
                    row["value"],
                    row["category"],
                )
                for row in master_rows
            }
            success_lookup = {
                (
                    row["date"],
                    row["entity"],
                    row["currency"],
                    row["value"],
                    row["category"],
                )
                for row in success_rows
            }

            self.assertTrue(
                {
                    (
                        "2024-01-15",
                        "Acme Manufacturing",
                        "USD",
                        "15000.0",
                        "paid",
                    ),
                    (
                        "2024-04-25",
                        "Acme Manufacturing",
                        "CHF",
                        "4100.0",
                        "paid",
                    ),
                    (
                        "2024-06-21",
                        "Contoso Retail",
                        "GBP",
                        "4410.15",
                        "paid",
                    ),
                    (
                        "2024-07-24",
                        "Wide World Importers",
                        "AUD",
                        "7800.0",
                        "paid",
                    ),
                    (
                        "2024-08-23",
                        "Fabrikam GmbH",
                        "EUR",
                        "16110.0",
                        "paid",
                    ),
                }.issubset(master_lookup)
            )
            self.assertTrue(
                {
                    (
                        "2024-03-15",
                        "Soylent Foods",
                        "USD",
                        "0.0",
                        "active",
                    ),
                    (
                        "2024-03-18",
                        "Acme Manufacturing",
                        "USD",
                        "15420.0",
                        "disputed",
                    ),
                    (
                        "2024-07-18",
                        "Contoso Retail",
                        "GBP",
                        "0.0",
                        "disputed",
                    ),
                    (
                        "2024-07-22",
                        "Fabrikam GmbH",
                        "EUR",
                        "12495.0",
                        "review",
                    ),
                    (
                        "2024-08-14",
                        "Blue Yonder",
                        "USD",
                        "11890.0",
                        "paid",
                    ),
                    (
                        "2024-08-15",
                        "Fabrikam GmbH",
                        "EUR",
                        "17990.0",
                        "paid",
                    ),
                    (
                        "2024-08-16",
                        "Contoso Retail",
                        "GBP",
                        "-6020.4",
                        "adjustment",
                    ),
                }.issubset(success_lookup)
            )

            failure_lookup = {
                (
                    row.get("invoice_id", ""),
                    row.get("raw_amount", ""),
                    row.get("anomaly_reason", ""),
                )
                for row in failure_rows
            }
            self.assertIn(
                ("INV-312", "CHARGEBACK ⚠", "unmapped_amount_token"),
                failure_lookup,
            )
            self.assertTrue(any(row["value"] != "0.0" for row in success_rows))

            self.assertEqual(
                failure_lookup,
                {
                    ("INV-112", "SEE PDF 📎", "unmapped_amount_token"),
                    ("INV-214", "MANUAL ONLY 🧾", "unmapped_amount_token"),
                    ("INV-312", "CHARGEBACK ⚠", "unmapped_amount_token"),
                    (
                        "INV-412",
                        "ESCALATE TO TREASURY 🚫",
                        "unmapped_amount_token",
                    ),
                    (
                        "INV-510",
                        "CHECK ATTACHMENT 📎",
                        "unmapped_amount_token",
                    ),
                },
            )

            self.assertEqual(len(master_rows), 55)
            self.assertEqual(len(success_rows), 25)
            self.assertEqual(len(failure_rows), 5)

    def test_prepare_evaluate_requires_mutation_sidecars(self) -> None:
        """Fail evaluation when the mutation export sidecars are missing."""
        clean_data_runtime = import_module("cleanloop.clean_data_runtime")
        prepare = import_module("cleanloop.prepare")
        input_dir = PROJECT_ROOT / "cleanloop" / ".input"

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            master_path = cleanloop_datasets.get_output_path(output_dir)
            success_path = output_dir / "finance_mutation_success.csv"

            clean_data_runtime.clean(input_dir, master_path)
            success_path.unlink()

            results = prepare.evaluate(master_path)

            self.assertTrue(
                any(
                    item.startswith("can_read_mutation_success_output:")
                    for item in results["failed"]
                )
            )

    def test_build_system_prompt_includes_mutation_playbook(self) -> None:
        """Describe the mutation sidecars and the shipped anomaly-fix playbook."""
        cleanloop_loop = import_module("cleanloop.loop")

        system_prompt = cleanloop_loop.build_system_prompt()

        self.assertIn("finance_mutation_success.csv", system_prompt)
        self.assertIn("finance_mutation_failures.csv", system_prompt)
        self.assertIn("FREE TRIAL", system_prompt)
        self.assertIn("COMPLIMENTARY", system_prompt)
        self.assertIn("OFFSET", system_prompt)
        self.assertIn("DISCOUNTED", system_prompt)
        self.assertIn("FX HOLD", system_prompt)
        self.assertIn("REVERSAL", system_prompt)
        self.assertIn("BLANK_CANCELLED_OR_VOID", system_prompt)
        self.assertIn("Prefer a two-stage repair strategy", system_prompt)

    def test_prepare_evaluate_rejects_failure_sidecar_schema_drift(self) -> None:
        """Fail evaluation when the mutation-failure dump loses required columns."""
        clean_data_runtime = import_module("cleanloop.clean_data_runtime")
        prepare = import_module("cleanloop.prepare")
        input_dir = PROJECT_ROOT / "cleanloop" / ".input"

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            master_path = cleanloop_datasets.get_output_path(output_dir)
            failure_path = cleanloop_datasets.get_mutation_failures_path(output_dir)

            clean_data_runtime.clean(input_dir, master_path)

            failure_headers, failure_rows = _read_rows(failure_path)
            self.assertIn("anomaly_reason", failure_headers)
            with failure_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        header
                        for header in failure_headers
                        if header != "anomaly_reason"
                    ],
                )
                writer.writeheader()
                for row in failure_rows:
                    row.pop("anomaly_reason", None)
                    writer.writerow(row)

            results = prepare.evaluate(master_path)

            self.assertTrue(
                any(
                    item.startswith("mutation_failures_has_required_columns:")
                    for item in results["failed"]
                )
            )

    def test_prepare_evaluate_rejects_blank_failure_diagnostics(self) -> None:
        """Fail evaluation when the mutation-failure dump keeps blank diagnostic fields."""
        clean_data_runtime = import_module("cleanloop.clean_data_runtime")
        prepare = import_module("cleanloop.prepare")
        input_dir = PROJECT_ROOT / "cleanloop" / ".input"

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            master_path = cleanloop_datasets.get_output_path(output_dir)
            failure_path = cleanloop_datasets.get_mutation_failures_path(output_dir)

            clean_data_runtime.clean(input_dir, master_path)

            failure_headers, failure_rows = _read_rows(failure_path)
            failure_rows[0]["anomaly_reason"] = ""
            with failure_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=failure_headers)
                writer.writeheader()
                writer.writerows(failure_rows)

            results = prepare.evaluate(master_path)

            self.assertTrue(
                any(
                    item.startswith("mutation_failures_have_diagnostics:")
                    for item in results["failed"]
                )
            )

    def test_prepare_evaluate_rejects_mutation_success_rows_missing_from_master(
        self,
    ) -> None:
        """Fail evaluation when mutation-success rows are not folded into the master export."""
        clean_data_runtime = import_module("cleanloop.clean_data_runtime")
        prepare = import_module("cleanloop.prepare")
        input_dir = PROJECT_ROOT / "cleanloop" / ".input"

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            master_path = cleanloop_datasets.get_output_path(output_dir)

            clean_data_runtime.clean(input_dir, master_path)

            master_headers, master_rows = _read_rows(master_path)
            trimmed_rows = [
                row
                for row in master_rows
                if not (
                    row["date"] == "2024-08-14"
                    and row["entity"] == "Blue Yonder"
                    and row["currency"] == "USD"
                    and row["value"] == "11890.0"
                    and row["category"] == "paid"
                )
            ]
            with master_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=master_headers)
                writer.writeheader()
                writer.writerows(trimmed_rows)

            results = prepare.evaluate(master_path)

            self.assertTrue(
                any(
                    item.startswith("mutation_success_rows_in_master:")
                    for item in results["failed"]
                )
            )

    def test_dataset_contract_centralizes_schema_and_mutation_rules(self) -> None:
        """Expose schema and mutation-rule contracts from datasets for reuse."""
        self.assertEqual(
            cleanloop_datasets.get_dataset_config().required_columns,
            cleanloop_datasets.FINANCE_COLUMNS,
        )
        self.assertEqual(
            cleanloop_datasets.get_failure_columns(),
            cleanloop_datasets.FAILURE_COLUMNS,
        )

        playbook = cleanloop_datasets.build_mutation_playbook()
        rule_tokens = {item["token"] for item in playbook}
        self.assertIn("FREE TRIAL", rule_tokens)
        self.assertIn("COMPLIMENTARY", rule_tokens)
        self.assertIn("DISCOUNTED", rule_tokens)
        self.assertIn("FX HOLD", rule_tokens)
        self.assertIn("REVERSAL", rule_tokens)
        self.assertIn("RESOLUTION_AMOUNT", rule_tokens)
        self.assertIn("BLANK_CANCELLED_OR_VOID", rule_tokens)
        self.assertIn(
            "PENDING / TBD / ERROR / ERR / CHARGEBACK",
            rule_tokens,
        )


if __name__ == "__main__":
    unittest.main()
