"""Tests for ingestion using temporary input files."""

import tempfile
import unittest
from pathlib import Path

from qe_foundations.ingestion.exceptions import (
    MissingColumnsError,
    SourceNotFoundError,
)
from qe_foundations.ingestion.loader import load_test_cases


class TestIngestion(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.folder = Path(temporary.name)

    def test_good_file_loads_all_rows(self):
        path = self.folder / "good.csv"
        path.write_text(
            "id,title,status,duration\n"
            "TC-1,Login test,pass,10\n"
            "TC-2,Search test,fail,20\n",
            encoding="utf-8",
        )

        report = load_test_cases(path)

        self.assertEqual(report.rows_seen, 2)
        self.assertEqual(report.valid, [
            {
                "id": "TC-1",
                "title": "Login test",
                "status": "pass",
                "duration": 10.0,
            },
            {
                "id": "TC-2",
                "title": "Search test",
                "status": "fail",
                "duration": 20.0,
            },
        ])
        self.assertEqual(report.rejected, [])

    def test_bad_row_logs_warning_and_keeps_good_rows(self):
        path = self.folder / "mixed.csv"
        path.write_text(
            "id,title,status,duration\n"
            "TC-1,Login test,pass,10\n"
            "TC-2,Invalid test,invalid,20\n",
            encoding="utf-8",
        )

        with self.assertLogs(
            "qe_foundations.ingestion.loader", level="WARNING"
        ) as captured:
            report = load_test_cases(path)

        self.assertEqual(report.rows_seen, 2)
        self.assertEqual(len(report.valid), 1)
        self.assertEqual(report.valid[0]["id"], "TC-1")
        self.assertEqual(len(report.rejected), 1)
        self.assertEqual(report.rejected[0].row, 2)
        self.assertTrue(
            any("row 2 skipped" in message for message in captured.output)
        )

    def test_missing_file_raises_source_not_found(self):
        path = self.folder / "missing.csv"

        with self.assertRaises(SourceNotFoundError):
            load_test_cases(path)

    def test_missing_column_raises_missing_columns(self):
        path = self.folder / "missing_column.csv"
        path.write_text(
            "id,title,status\n"
            "TC-1,Login test,pass\n",
            encoding="utf-8",
        )

        with self.assertRaises(MissingColumnsError):
            load_test_cases(path)


if __name__ == "__main__":
    unittest.main()