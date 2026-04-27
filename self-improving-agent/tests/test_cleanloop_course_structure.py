"""Structure and packaging regressions for the course-aligned CleanLoop refactor."""

from __future__ import annotations

import importlib
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


CLEANLOOP_ROOT = PROJECT_ROOT / "cleanloop"


class CleanLoopCourseStructureTests(unittest.TestCase):
    """Keep the CleanLoop example aligned to the seven-lesson course structure."""

    def test_docs_live_under_docs_except_root_readme(self) -> None:
        """Move non-README documentation out of the CleanLoop root."""
        self.assertTrue((CLEANLOOP_ROOT / "README.md").exists())
        self.assertTrue((CLEANLOOP_ROOT / "docs" / "architecture").exists())
        self.assertTrue((CLEANLOOP_ROOT / "docs" / "lessons").exists())
        self.assertTrue((CLEANLOOP_ROOT / "docs" / "reference").exists())
        self.assertTrue((CLEANLOOP_ROOT / "docs" / "operations").exists())
        self.assertTrue((CLEANLOOP_ROOT / "docs" / "testing").exists())
        self.assertTrue(
            (CLEANLOOP_ROOT / "docs" / "architecture" / "system-overview.md").exists()
        )
        self.assertTrue(
            (CLEANLOOP_ROOT / "docs" / "operations" / "setup-and-verify.md").exists()
        )
        self.assertFalse((CLEANLOOP_ROOT / "ARCHITECTURE.md").exists())
        self.assertFalse((CLEANLOOP_ROOT / "EXAMPLE.md").exists())
        self.assertFalse((CLEANLOOP_ROOT / "lessons").exists())

    def test_cleanloop_has_standalone_pyproject(self) -> None:
        """Ship a self-sufficient project definition inside the CleanLoop folder."""
        pyproject_path = CLEANLOOP_ROOT / "pyproject.toml"
        self.assertTrue(pyproject_path.exists())

        data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
        project = data["project"]

        self.assertEqual(project["requires-python"], ">=3.11")
        self.assertIn("pandas>=2.2.0", project["dependencies"])
        self.assertIn("python-dotenv>=1.0.0", project["dependencies"])
        self.assertIn("streamlit>=1.45.0", project["dependencies"])
        self.assertIn("scripts", project)
        self.assertEqual(project["scripts"]["cleanloop"], "util:main")
        self.assertEqual(
            project["scripts"]["cleanloop-verify"],
            "cleanloop_console:verify_main",
        )

    def test_root_helper_modules_exist(self) -> None:
        """Expose flat root helper modules instead of a duplicate lesson package."""
        expected_modules = [
            "cleanloop.cleanloop_console",
            "cleanloop.dataset_contract",
            "cleanloop.input_loader",
            "cleanloop.date_normalizer",
            "cleanloop.export_writer",
            "cleanloop.mutation_playbook",
            "cleanloop.status_snapshot",
            "cleanloop.history_store",
            "cleanloop.reset_workflow",
            "cleanloop.tracing",
        ]

        for module_name in expected_modules:
            with self.subTest(module=module_name):
                self.assertIsNotNone(importlib.import_module(module_name))

    def test_clean_pipeline_writes_trace_artifacts(self) -> None:
        """Emit structured trace files beside the exports for learner observability."""
        clean_data_runtime = importlib.import_module("cleanloop.clean_data_runtime")

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            clean_data_runtime.clean(
                CLEANLOOP_ROOT / ".input",
                output_dir / "finance_master.csv",
            )

            traces_dir = output_dir / "traces"
            self.assertTrue((traces_dir / "run-events.jsonl").exists())
            self.assertTrue((traces_dir / "row-decisions.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
