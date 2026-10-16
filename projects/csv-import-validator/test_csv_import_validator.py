import unittest

from csv_import_validator import validate_orders


class CsvImportValidatorTests(unittest.TestCase):
    def test_keeps_later_good_row_after_two_errors(self):
        text = "sku,qty\nA-1,2\n,4\nB-2,not-an-int\nC-3,1\n"
        self.assertEqual(
            validate_orders(text),
            {
                "accepted": [("A-1", 2), ("C-3", 1)],
                "errors": [(3, "missing sku"), (4, "invalid qty")],
            },
        )

    def test_header_only_and_missing_header(self):
        self.assertEqual(validate_orders("qty,sku\n"), {"accepted": [], "errors": []})
        self.assertEqual(
            validate_orders("sku\nA-1\n"),
            {"accepted": [], "errors": [(1, "missing required headers")]},
        )

    def test_quoted_sku_and_reordered_header(self):
        self.assertEqual(
            validate_orders('qty,sku\n5,"A,blue"\n'),
            {"accepted": [("A,blue", 5)], "errors": []},
        )

    def test_bad_shape_and_nonpositive_quantity_are_reported(self):
        text = "sku,qty\nA-1\nB-2,0\nC-3,2,extra\nD-4,3\n"
        self.assertEqual(
            validate_orders(text),
            {
                "accepted": [("D-4", 3)],
                "errors": [(2, "malformed row"), (3, "invalid qty"), (4, "malformed row")],
            },
        )


if __name__ == "__main__":
    unittest.main()
