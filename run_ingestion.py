"""Run ingestion with logging enabled."""

import sys

from qe_foundations.ingestion.__main__ import main
from qe_foundations.utils.logging_setup import setup_logging


if __name__ == "__main__":
    setup_logging(logfile="ingestion.log")
    sys.exit(main(sys.argv[1:]))