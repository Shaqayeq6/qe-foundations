"""Configure logging for the qe_foundations package."""

import logging
import sys


def setup_logging(level="INFO", logfile=None):
    """Configure console and optional file logging once."""
    logger = logging.getLogger("qe_foundations")
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if logfile is not None:
        file_handler = logging.FileHandler(
            logfile, encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.propagate = False
    return logger