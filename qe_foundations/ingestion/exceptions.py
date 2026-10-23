"""Custom exceptions for file loading and record validation."""

from pathlib import Path


class IngestionError(Exception):
    """Base exception for the ingestion module."""


class SourceError(IngestionError):
    """A whole source file cannot be used."""

    def __init__(self, path, detail):
        self.path = str(path)
        self.detail = detail
        super().__init__(f"{Path(path).name}: {detail}")


class SourceNotFoundError(SourceError):
    """The source file does not exist."""

    def __init__(self, path):
        super().__init__(path, "file not found")


class SourceUnreadableError(SourceError):
    """The source cannot be opened for reading."""

    def __init__(self, path, os_error):
        error_name = type(os_error).__name__
        super().__init__(path, f"cannot be read ({error_name})")


class UnsupportedFormatError(SourceError):
    """The file extension is not supported."""

    def __init__(self, path, suffix):
        self.suffix = suffix
        super().__init__(path, f"unsupported format: {suffix!r}")


class MalformedSourceError(SourceError):
    """The file contains malformed content or invalid encoding."""


class MissingColumnsError(SourceError):
    """The CSV file lacks required columns."""

    def __init__(self, path, missing):
        self.missing = list(missing)
        columns = ", ".join(self.missing)
        super().__init__(path, f"missing required columns: {columns}")


class RecordValidationError(IngestionError):
    """One record is invalid."""

    def __init__(self, row, field_name, message):
        self.row = row
        self.field = field_name
        super().__init__(f"Row {row}: {message}")


class MissingFieldError(RecordValidationError):
    """A required field is absent, None, or blank."""

    def __init__(self, row, field_name):
        super().__init__(
            row, field_name, f"missing required field '{field_name}'"
        )


class InvalidValueError(RecordValidationError):
    """A field contains an unacceptable value."""

    def __init__(self, row, field_name, value, expected):
        self.value = value
        self.expected = expected
        super().__init__(
            row,
            field_name,
            f"invalid value {value!r} for '{field_name}'; expected {expected}",
        )


class DuplicateIdError(RecordValidationError):
    """A test ID duplicates an earlier valid record."""

    def __init__(self, row, test_id):
        self.test_id = test_id
        super().__init__(row, "id", f"duplicate id {test_id!r}")