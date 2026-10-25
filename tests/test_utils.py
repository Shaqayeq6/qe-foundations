"""Tests for the project's utility functions."""

import unittest

from qe_foundations.utils.numbers import percent
from qe_foundations.utils.strings import normalize_whitespace, slugify


class TestUtils(unittest.TestCase):
    def test_normalize_whitespace_removes_extra_spaces(self):
        result = normalize_whitespace("  hello   world  ")
        self.assertEqual(result, "hello world")

    def test_slugify_creates_lowercase_hyphenated_text(self):
        result = slugify("  Login Test!  ")
        self.assertEqual(result, "login-test")

    def test_percent_calculates_percentage(self):
        result = percent(3, 4)
        self.assertAlmostEqual(result, 75.0)

    def test_normalize_whitespace_none_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            normalize_whitespace(None)


if __name__ == "__main__":
    unittest.main()