"""Context managers for safe file reading and load timing."""

import time
from contextlib import contextmanager
from pathlib import Path

from .exceptions import (
    MalformedSourceError,
    SourceNotFoundError,
    SourceUnreadableError,
)


@contextmanager
def open_source(path):
    """Open a source safely and translate file and decoding errors."""
    try:
        handle = open(path, encoding="utf-8-sig", newline="")
    except FileNotFoundError as error:
        raise SourceNotFoundError(path) from error
    except OSError as error:
        raise SourceUnreadableError(path, error) from error

    try:
        yield handle
    except UnicodeDecodeError as error:
        raise MalformedSourceError(path, "invalid UTF-8 encoding") from error
    finally:
        handle.close()


class LoadSession:
    """Track the elapsed time and outcome of a load."""

    def __init__(self, path):
        self.path = Path(path)
        self.outcome = None
        self.elapsed = None

    def __enter__(self):
        """Start timing and return the session."""
        self._started = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Record the result and allow exceptions to propagate."""
        self.elapsed = time.perf_counter() - self._started

        if exc_type is None:
            self.outcome = "completed"
        else:
            self.outcome = "failed"

        return False