# Defect Reports


## DEF-01: Missing and negative test durations
- Rule: R-04
- Severity: High
- Status: Open
- Environment: Supplied SQLite test-run dataset

### Steps to reproduce

From the repository root, run:

python -m qe_foundations.validation --show R-04

### Exact query

```sql
SELECT run_id, status, duration_ms
FROM test_runs
WHERE duration_ms IS NULL
   OR duration_ms < 0;
```

### Expected result

Every run has a duration greater than or equal to zero.
The violation query returns no rows.

### Actual result and evidence

- Run 5009: PASSED, duration_ms = -250.
- Run 5016: PASSED, duration_ms = NULL.

### Impact

Negative durations can distort runtime averages. Missing durations
can be excluded from calculations, making reports incomplete.

### Could this be a false alarm?

Could NULL mean that timing was unavailable? The current requirement
explicitly requires a duration, so both rows violate R-04.
Zero-duration runs are legal and are not flagged.

## DEF-02: Test runs contain inconsistent timestamps

- Rule: R-10
- Severity: High
- Status: Open
- Environment: Supplied SQLite test-run dataset

### Steps to reproduce

From the repository root, run:

python -m qe_foundations.validation --show R-10

### Exact query

```sql
SELECT run_id, started_at, finished_at
FROM test_runs
WHERE finished_at < started_at
   OR started_at > datetime('now');
```

### Expected result

No run finishes before it starts or starts in the future.
The violation query returns no rows.

### Actual result and evidence

- Run 5005: started at 2025-04-02 09:15:00 and finished at
  2025-04-02 09:14:50, ten seconds before its start.
- Run 5032: started_at = 2099-01-01 08:00:00 and
  finished_at = 2099-01-01 08:00:05. Its start is in the future
  relative to the validation date, 2026-10-23.

### Impact

Incorrect timestamps can distort execution order, time-based
dashboards and reports that select the most recent test run.

### Could this be a false alarm?

Could clock differences or inconsistent time zones explain these
values? Confirm that timestamps share the same time basis.
The query uses SQLite's current UTC time.