# Testing and logging

Run tests from the qe-foundations repository root:
`python -m unittest discover -s tests`

Run ingestion with logging:
`python run_ingestion.py data/ingestion/test_cases_messy.csv`

Console logging shows INFO and higher messages.
The log file is ingestion.log in the working directory and is ignored by Git.
Tests create temporary files and remove them automatically.