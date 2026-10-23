-- =============================================================================
-- sql/validation_queries.sql  --  STARTER (skeleton)
-- Project 1 (QE Foundations) -- Thursday milestone: data validation queries
-- Table under test: test_runs   (schema: qe_foundations/data/test_runs_schema.sql)
--
-- YOUR JOB (as a pair, swapping the keyboard every 30 minutes):
--   replace every placeholder query below with a real query.
--
-- THE FORMAT (the runner and check_exercise.py parse it -- keep it exactly):
--   * keep every "@rule <ID> | <Dimension> | <description>" header line AS IS
--     (ids and wording); the "@expect N" line is the number of rows that means PASS
--       violation queries (R-xx): 0 rows = PASS      expectation queries (E-xx): 1 row = PASS
--   * ONE read-only SELECT per rule, ending with ';'
--   * the FIRST column you SELECT must be run_id (it is the evidence), then any
--     columns that help a reader see WHY the row is bad
--   * Thursday toolkit only: SELECT, WHERE, AND/OR/NOT, IN, BETWEEN, LIKE,
--     IS NULL, TRIM, UPPER/LOWER, LENGTH, date('now'), ORDER BY, LIMIT.
--     (No JOIN, GROUP BY, HAVING, sub-queries or INSERT/UPDATE/DELETE: that is Friday.)
--
-- THE TRAP: every placeholder below is  WHERE 1 = 0  -- it returns NO rows, so
-- the runner reports PASS. That is a FALSE PASS. Replace each one and PREDICT
-- the result aloud before you run it ("I expect two rows: 5xxx and 5yyy").
-- =============================================================================

-- @rule R-01 | Completeness | executed_by must be present (not NULL, not blank)
-- TODO: completeness: 'missing' can be NULL *or* an empty/space-only string.
SELECT run_id, executed_by
FROM test_runs
WHERE executed_by IS NULL
   OR TRIM(executed_by) = '';

-- @rule R-02 | Validity | executed_by, when present, must look like an e-mail (contain '@' and a '.' after it)
-- TODO: one defect = one rule: do not re-report the rows R-01 already catches.
SELECT run_id, executed_by
FROM test_runs
WHERE executed_by IS NOT NULL
  AND TRIM(executed_by) <> ''
  AND executed_by NOT LIKE '%@%.%';

-- @rule R-03 | Validity | status must be exactly PASSED, FAILED, SKIPPED or ERROR (upper case)
-- TODO: exact match against a list; what does NOT IN do with NULL?
SELECT run_id, status
FROM test_runs
WHERE status IS NULL
   OR status NOT IN ('PASSED', 'FAILED', 'SKIPPED', 'ERROR');

-- @rule R-04 | Validity | duration_ms must be present and not negative (0 is legal, e.g. SKIPPED)
-- TODO: 0 is LEGAL (a SKIPPED run takes 0 ms) -- do not raise a false alarm. NULL needs its own test.
SELECT run_id, status, duration_ms
FROM test_runs
WHERE duration_ms IS NULL
   OR duration_ms < 0;

-- @rule R-05 | Accuracy | duration_ms above 600000 (10 minutes) is an outlier needing review
-- TODO: a plain threshold. Show the worst first (ORDER BY ... DESC).
SELECT run_id, duration_ms
FROM test_runs
WHERE duration_ms > 600000 order by duration_ms desc;

-- @rule R-06 | Validity | retries must be present and between 0 and 3 inclusive
-- TODO: a range with BETWEEN -- and what happens to NULL?
SELECT run_id, retries
FROM test_runs
WHERE retries is NULL or retries NOT BETWEEN 0 and 3

-- @rule R-07 | Validity | environment must be exactly DEV, QA or STAGING
-- TODO: exact, case-sensitive list; 'qa' is not 'QA' for = / IN in SQLite.
SELECT run_id, environment
FROM test_runs
WHERE environment NOT in ('DEV','QA','STAGING') or environment is NULL;

-- @rule R-08 | Consistency | test_name, suite and status must have no leading/trailing spaces
-- TODO: a value that changes when you TRIM it has stray spaces. Three columns -> OR.
SELECT run_id, test_name, suite, status 
FROM test_runs
WHERE test_name != TRIM(test_name) OR suite != TRIM(suite) OR status != TRIM(status);

-- @rule R-09 | Validity | started_at and finished_at must be present and shaped 'YYYY-MM-DD HH:MM:SS'
-- TODO: the LIKE pattern _ matches exactly one character; these timestamps are 19 characters long.
SELECT run_id, started_at, finished_at
FROM test_runs
WHERE started_at IS NULL
   OR finished_at IS NULL
   OR started_at NOT LIKE '____-__-__ __:__:__'
   OR finished_at NOT LIKE '____-__-__ __:__:__';

-- @rule R-10 | Consistency | a run cannot finish before it starts, and cannot start in the future
-- TODO: ISO-format text sorts in time order, so < works on it. date('now') is today.
SELECT run_id, started_at, finished_at
FROM test_runs
WHERE finished_at < started_at
   OR started_at > datetime('now');

-- @rule R-11 | Consistency | FAILED/ERROR runs need a failure_message; PASSED runs must not have one
-- TODO: two sub-rules joined with OR; use parentheses so AND/OR bind the way you mean.
SELECT run_id, status, failure_message
FROM test_runs
WHERE (
    status IN ('FAILED', 'ERROR')
    AND (
        failure_message IS NULL
        OR TRIM(failure_message) = ''
    )
)
OR (
    status = 'PASSED'
    AND failure_message IS NOT NULL
    AND TRIM(failure_message) <> ''
);

-- @rule R-12 | Validity | build_id must be present and look like B-1042 (upper-case 'B', dash, 4 characters)
-- TODO: careful: LIKE ignores letter case in SQLite -- which function would expose 'b-1044'?
SELECT run_id, build_id
FROM test_runs
WHERE build_id IS NULL
   OR build_id NOT GLOB 'B-????'
ORDER BY run_id;

-- @rule E-01 | Expectation | run 5001 was saved as expected (test_login_valid_user, SMOKE, QA, PASSED, build B-1042)
-- @expect 1
-- TODO: expectation query: name EVERY value you expect; the rule passes when exactly 1 row comes back.
SELECT run_id, test_name, suite, environment, status, build_id
FROM test_runs
WHERE run_id = 5001
  AND test_name = 'test_login_valid_user'
  AND suite = 'SMOKE'
  AND environment = 'QA'
  AND status = 'PASSED'
  AND build_id = 'B-1042';


-- @rule E-02 | Expectation | test-data discovery: the most recent FAILED run in QA exists (exactly one row returned)
-- @expect 1
-- TODO: test-data discovery: filter, ORDER BY ... DESC, then keep only the first row.
SELECT *
FROM test_runs
WHERE status = 'FAILED'
  AND environment = 'QA'
ORDER BY started_at DESC
LIMIT 1;

-- ---------------------------- STRETCH (bonus) --------------------------------
-- Add these only when R-01..R-12, E-01 and E-02 are done and checked. Use "@expect any"
-- (informational: the runner prints INFO instead of PASS/FAIL). Un-comment and complete.
--
-- -- @rule S-01 | Stretch | combined dirty-rows list: every run_id that breaks ANY of R-01..R-12 (each run once)
-- -- @expect any
-- SELECT run_id FROM test_runs WHERE ... OR ... ;
--
-- -- @rule S-02 | Stretch | uniqueness: show the two suspected duplicate runs side by side
-- -- @expect any
-- SELECT run_id, test_name, environment, build_id, started_at FROM test_runs WHERE ... ;
--
-- -- @rule S-03 | Stretch | test-data discovery: the 3 slowest runs whose duration is plausible (0..600000 ms)
-- -- @expect any
-- SELECT run_id, test_name, duration_ms FROM test_runs WHERE ... ORDER BY ... LIMIT 3;










