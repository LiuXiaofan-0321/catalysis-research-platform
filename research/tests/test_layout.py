from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = RESEARCH_ROOT / "src"
sys.path.insert(0, str(SOURCE_ROOT))

from catalysis_research.layout import (
    REQUIRED_DIRECTORIES,
    REQUIRED_DOCUMENTS,
    inspect_layout,
)


class ResearchLayoutTests(unittest.TestCase):
    def test_repository_layout_is_complete(self) -> None:
        status = inspect_layout(RESEARCH_ROOT)

        self.assertTrue(status["valid"])
        self.assertEqual(set(status["directories"]), set(REQUIRED_DIRECTORIES))
        self.assertEqual(set(status["documents"]), set(REQUIRED_DOCUMENTS))
        self.assertTrue(all(item["is_file"] for item in status["documents"].values()))

    def test_missing_directory_fails_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            status = inspect_layout(Path(temporary_directory))

        self.assertFalse(status["valid"])
        self.assertTrue(
            all(not item["exists"] for item in status["directories"].values())
        )

    def test_doctor_outputs_machine_readable_status(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(RESEARCH_ROOT / "scripts" / "research.py"),
                "doctor",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["valid"])


if __name__ == "__main__":
    unittest.main()
