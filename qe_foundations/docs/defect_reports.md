# Defect Reports

## DEF-01: Missing and negative test durations

Title: Missing and negative test durations

- Rule: R-04
- Severity: High
- Status: Open
- Environment: Supplied SQLite test-run dataset

### Steps to reproduce

1. Open a terminal in the qe-foundations repository root.
2. Run:

```powershell
python -m qe_foundations.validation --show R-04
```

### Exact query

```sql
SELECT run_id, status, duration_ms
FROM test_runs
WHERE duration_ms IS NULL
   OR duration_ms < 0;
```

### Expected result

Every test run has a duration greater than or equal to zero.
The violation query returns no rows.

### Actual result and evidence

The query returns two invalid records:

| run_id | status | duration_ms |
|---|---|---|
| 5009 | PASSED | -250 |
| 5016 | PASSED | NULL |

Run 5009 has a negative duration. Run 5016 has no duration.

### Impact

Negative durations can distort runtime averages. Missing durations
may be excluded from calculations, making performance reports
incomplete and potentially misleading.

### Could this be a false alarm?

Could NULL indicate that timing was unavailable? The current
requirement explicitly requires a duration, so both records violate
R-04. A duration of zero is legal and is not flagged by this query.

## DEF-02: Test runs contain inconsistent timestamps

Title: Test runs contain inconsistent timestamps

- Rule: R-10
- Severity: High
- Status: Open
- Environment: Supplied SQLite test-run dataset
- Validation date: 2026-10-23

### Steps to reproduce

1. Open a terminal in the qe-foundations repository root.
2. Run:

```powershell
python -m qe_foundations.validation --show R-10
```

### Exact query

```sql
SELECT run_id, started_at, finished_at
FROM test_runs
WHERE finished_at < started_at
   OR started_at > datetime('now');
```

### Expected result

No run finishes before it starts, and no run starts in the future.
The violation query returns no rows.

### Actual result and evidence

The query returns two invalid records:

| run_id | started_at | finished_at |
|---|---|---|
| 5005 | 2025-04-02 09:15:00 | 2025-04-02 09:14:50 |
| 5032 | 2099-01-01 08:00:00 | 2099-01-01 08:00:05 |

Run 5005 finished ten seconds before it started.

Run 5032 has a start timestamp in 2099, which is in the future
relative to the validation date of 2026-10-23.

### Impact

Incorrect timestamps can distort execution order, runtime calculations,
time-based dashboards and reports that select the most recent test run.

### Could this be a false alarm?

Could clock differences or inconsistent time zones explain these
values? Confirm that all timestamps use the same time basis.
The query uses SQLite's current UTC time. Under the stated business
rule, both records require investigation.