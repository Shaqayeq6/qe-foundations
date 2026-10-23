"""Validate and normalize individual test records."""

import math

from .exceptions import InvalidValueError, MissingFieldError

REQUIRED_FIELDS = ("id", "title", "status", "duration")
VALID_STATUSES = ("pass", "fail", "blocked")


def validate_record(row, raw):
    """Return a clean record or raise a record validation error."""
    if not isinstance(raw, dict):
        raise InvalidValueError(row, "record", raw, "a dictionary")

    for field in REQUIRED_FIELDS:
        value = raw.get(field)

        if value is None or (
            isinstance(value, str) and not value.strip()
        ):
            raise MissingFieldError(row, field)

    status = str(raw["status"]).strip().lower()

    if status not in VALID_STATUSES:
        raise InvalidValueError(
            row, "status", raw["status"], "pass, fail, or blocked"
        )

    expected_duration = "a finite number greater than or equal to zero"
    raw_duration = raw["duration"]

    if isinstance(raw_duration, bool):
        raise InvalidValueError(
            row, "duration", raw_duration, expected_duration
        )

    try:
        duration = float(raw_duration)
    except (TypeError, ValueError, OverflowError) as error:
        raise InvalidValueError(
            row, "duration", raw_duration, expected_duration
        ) from error

    if not math.isfinite(duration) or duration < 0:
        raise InvalidValueError(
            row, "duration", raw_duration, expected_duration
        )

    return {
        "id": str(raw["id"]).strip(),
        "title": str(raw["title"]).strip(),
        "status": status,
        "duration": duration,
    }