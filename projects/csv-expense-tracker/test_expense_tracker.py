"""Behavior checks for the CSV Expense Tracker."""

import unittest
from decimal import Decimal

from expense_tracker import summarize_expenses


class ExpenseTrackerTests(unittest.TestCase):
    def test_repeated_categories_sum_as_decimal(self):
        report = summarize_expenses("category,amount\nFood,12.50\nFood,3.00\nTravel,4.25\n")
        self.assertEqual(report, {"Food": Decimal("15.50"), "Travel": Decimal("4.25")})

    def test_quoted_comma_and_reordered_headers(self):
        report = summarize_expenses('amount,category\n2.40,"Food, snacks"\n1.10,"Food, snacks"\n')
        self.assertEqual(report, {"Food, snacks": Decimal("3.50")})

    def test_header_only_is_empty(self):
        self.assertEqual(summarize_expenses("category,amount\n"), {})

    def test_invalid_amount_has_clear_error(self):
        with self.assertRaisesRegex(ValueError, "invalid amount"):
            summarize_expenses("category,amount\nFood,oops\n")

    def test_missing_header_has_clear_error(self):
        with self.assertRaisesRegex(ValueError, "missing required header"):
            summarize_expenses("category,price\nFood,12.50\n")

    def test_extra_fields_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "missing or extra fields"):
            summarize_expenses("category,amount\nFood,12.50,extra\n")

    def test_nan_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "non-finite amount"):
            summarize_expenses("category,amount\nFood,NaN\n")


if __name__ == "__main__":
    unittest.main()
