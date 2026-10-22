"""Load test sources, collect record errors, and summarize results."""

import csv
import logging
from pathlib import Path

from .contexts import LoadSession
from .exceptions import (
    DuplicateIdError,
    RecordValidationError,
    SourceError,
    SourceNotFoundError,
    UnsupportedFormatError,
)
from .readers import read_csv_records, read_json_records, read_xml_records
from .validation import validate_record
logger = logging.getLogger(__name__)
READERS = {
    ".csv": read_csv_records,
    ".json": read_json_records,
    ".xml": read_xml_records,
}


class IngestionReport:
    """Store valid records and record errors from one source."""

    def __init__(self, source, rows_seen=0):
        self.source = Path(source).name
        self.rows_seen = rows_seen
        self.valid = []
        self.rejected = []

    def summary(self):
        """Return a one-line summary of the source."""
        return (
            f"{Path(self.source).name}: {self.rows_seen} rows seen, "
            f"{len(self.valid)} valid, {len(self.rejected)} rejected"
        )

    def rejected_rows(self):
        """Return rejected-record details ordered by row number."""
        return [
            {
                "source": Path(self.source).name,
                "row": error.row,
                "field": error.field,
                "reason": str(error),
            }
            for error in sorted(self.rejected, key=lambda error: error.row)
        ]

    def check_invariants(self):
        """Check that internal record bookkeeping is consistent."""
        assert len(self.valid) + len(self.rejected) == self.rows_seen, (
            "Valid and rejected counts must add up to rows_seen"
        )

        ids = [record["id"] for record in self.valid]
        assert len(ids) == len(set(ids)), (
            "Valid records must have unique IDs"
        )

        assert all(
            isinstance(error, RecordValidationError)
            for error in self.rejected
        ), "Every rejected entry must be a RecordValidationError"


class BatchResult:
    """Store reports and source errors from loading a folder."""

    def __init__(self):
        self.reports = []
        self.failed_sources = []

    def totals(self):
        """Return file and record totals across the batch."""
        return {
            "files_ok": len(self.reports),
            "files_failed": len(self.failed_sources),
            "valid": sum(len(report.valid) for report in self.reports),
            "rejected": sum(len(report.rejected) for report in self.reports),
        }


def load_test_cases(path):
    """Load one source and collect its invalid records."""
    logger.info("Loading source %s", path)
    with LoadSession(path):
        path = Path(path)
        suffix = path.suffix.lower()
        reader = READERS.get(suffix)

        if reader is None:
            raise UnsupportedFormatError(path, suffix)

        raw_records = reader(path)
        report = IngestionReport(path)
        seen_ids = set()

        for row, raw in enumerate(raw_records, start=1):
            report.rows_seen += 1

            try:
                record = validate_record(row, raw)

                if record["id"] in seen_ids:
                    raise DuplicateIdError(row, record["id"])

            except RecordValidationError as error:
                report.rejected.append(error)
                logger.warning(
                    "Source %s row %d skipped: %s",
                    path.name, row, error
                )
            else:
                seen_ids.add(record["id"])
                report.valid.append(record)

        report.check_invariants()
        logger.info(
            "Loaded %s: %d good rows, %d bad rows",
            path.name, len(report.valid), len(report.rejected)
        )
        return report


def load_directory(folder):
    """Load files in name order and collect unusable-source errors."""
    folder = Path(folder)

    if not folder.is_dir():
        raise SourceNotFoundError(folder)

    batch = BatchResult()

    for path in sorted(folder.iterdir(), key=lambda path: path.name):
        if not path.is_file():
            continue

        try:
            report = load_test_cases(path)
        except SourceError as error:
            batch.failed_sources.append(error)
        else:
            batch.reports.append(report)

    return batch


def write_rejected_csv(report, out_path):
    """Write rejected-record details to CSV and return its path."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["source", "row", "field", "reason"],
        )
        writer.writeheader()
        writer.writerows(report.rejected_rows())

    return out_path