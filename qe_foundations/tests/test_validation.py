"""Tests for the SQL validation runner."""

import unittest

from qe_foundations.validation import runner
from qe_foundations.validation.exceptions import ValidationFailedError


class ValidationRunnerTests(unittest.TestCase):
    def setUp(self):
        self.conn = runner.connect(":memory:")
        self.addCleanup(self.conn.close)
        runner.load_seed(self.conn)

    def test_seed_loads_expected_number_of_rows(self):
        (count,) = self.conn.execute(
            "SELECT COUNT(*) FROM test_runs"
        ).fetchone()

        self.assertEqual(count, 60)

    def test_parse_rules_finds_the_required_rule_ids(self):
        ids = {rule.rule_id for rule in runner.parse_rules()}
        required = {
            f"R-{n:02d}" for n in range(1, 13)
        } | {"E-01", "E-02"}

        self.assertTrue(required <= ids)

    def test_run_rule_returns_rows_when_rule_holds(self):
        # Arrange
        rule = runner.Rule(
            rule_id="TEST-01",
            dimension="Validity",
            description="No violations",
            sql="SELECT run_id FROM test_runs WHERE run_id = -1;",
            expect=0,
        )

        # Act
        rows = runner.run_rule(self.conn, rule)

        # Assert
        self.assertEqual(rows, [])

    def test_run_rule_raises_validation_failed_error_with_the_evidence(self):
        rule = runner.Rule(
            rule_id="TEST-02",
            dimension="Validity",
            description="Selected row violates this test rule",
            sql="SELECT run_id FROM test_runs WHERE run_id = 5003;",
            expect=0,
        )

        with self.assertRaises(ValidationFailedError) as context:
            runner.run_rule(self.conn, rule)

        error = context.exception
        self.assertEqual(error.rule_id, "TEST-02")
        self.assertEqual(error.description, rule.description)
        self.assertEqual(error.rows, [(5003,)])

    def test_duration_rule_catches_the_known_bad_runs(self):
        rule = next(
            rule for rule in runner.parse_rules()
            if rule.rule_id == "R-04"
        )

        _, rows = runner.fetch_rows(self.conn, rule.sql)

        self.assertEqual({row[0] for row in rows}, {5009, 5016})

    def test_expectation_rule_fails_when_the_expected_row_is_missing(self):
        rule = runner.Rule(
            rule_id="TEST-03",
            dimension="Expectation",
            description="One row must exist",
            sql="SELECT run_id FROM test_runs WHERE run_id = -1;",
            expect=1,
        )

        with self.assertRaises(ValidationFailedError):
            runner.run_rule(self.conn, rule)

    def test_duration_rule_does_not_flag_legal_zero_duration_runs(self):
        rule = next(
            rule for rule in runner.parse_rules()
            if rule.rule_id == "R-04"
        )
        _, legal_rows = runner.fetch_rows(
            self.conn,
            "SELECT run_id FROM test_runs "
            "WHERE status = 'SKIPPED' AND duration_ms = 0;",
        )
        legal_ids = {row[0] for row in legal_rows}
        self.assertEqual(legal_ids, {5004, 5021, 5042, 5057})

        _, violations = runner.fetch_rows(self.conn, rule.sql)
        flagged_ids = {row[0] for row in violations}

        self.assertTrue(legal_ids.isdisjoint(flagged_ids))


if __name__ == "__main__":
    unittest.main()