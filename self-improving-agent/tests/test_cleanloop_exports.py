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

    def test_clean_pipeline_writes_master_success_and_failure_exports(self) -> None:
        """Write three exports and partition fixed versus failed anomalies."""
        clean_data = import_module("cleanloop.clean_data")
        input_dir = PROJECT_ROOT / "cleanloop" / ".input"

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            master_path = cleanloop_datasets.get_output_path(output_dir)
            success_path = output_dir / "finance_mutation_success.csv"
            failure_path = output_dir / "finance_mutation_failures.csv"

            clean_data.clean(input_dir, master_path)

            self.assertTrue(master_path.exists())
            self.assertTrue(success_path.exists())
            self.assertTrue(failure_path.exists())

            expected_columns = ["date", "entity", "value", "category"]
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

            master_lookup = {
                (row["date"], row["entity"], row["value"], row["category"])
                for row in master_rows
            }
            success_lookup = {
                (row["date"], row["entity"], row["value"], row["category"])
                for row in success_rows
            }

            self.assertTrue(success_lookup.issubset(master_lookup))
            self.assertIn(
                ("2024-01-03", "Soylent Foods", "0.0", "active"),
                success_lookup,
            )
            self.assertIn(
                ("2024-04-07", "Contoso Retail", "0.0", "disputed"),
                success_lookup,
            )
            self.assertIn(
                ("2024-08-05", "Acme Manufacturing", "0.0", "active"),
                success_lookup,
            )
            self.assertNotIn(
                ("2024-12-03", "Globex Retail", "12750.0", "paid"),
                success_lookup,
            )
            self.assertIn(
                ("2024-12-03", "Globex Retail", "12750.0", "paid"),
                master_lookup,
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
                ("INV-312", "CHARGEBACK", "unmapped_amount_token"),
                failure_lookup,
            )
            self.assertIn(
                ("INV-108", "PENDING", "unmapped_amount_token"),
                failure_lookup,
            )

            self.assertEqual(len(master_rows), 60)
            self.assertEqual(len(success_rows), 5)
            self.assertEqual(len(failure_rows), 15)

    def test_prepare_evaluate_requires_mutation_sidecars(self) -> None:
        """Fail evaluation when the mutation export sidecars are missing."""
        clean_data = import_module("cleanloop.clean_data")
        prepare = import_module("cleanloop.prepare")
        input_dir = PROJECT_ROOT / "cleanloop" / ".input"

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            master_path = cleanloop_datasets.get_output_path(output_dir)
            success_path = output_dir / "finance_mutation_success.csv"

            clean_data.clean(input_dir, master_path)
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


if __name__ == "__main__":
    unittest.main()
