import unittest

from booking_conflicts import find_conflicts


class BookingConflictTests(unittest.TestCase):
    def test_pairs_are_reported_in_source_order(self):
        bookings = [("A", 540, 600), ("B", 600, 660), ("C", 570, 630)]
        self.assertEqual(find_conflicts(bookings), [("A", "C"), ("B", "C")])

    def test_touching_is_clear_but_containment_overlaps(self):
        self.assertEqual(find_conflicts([("A", 0, 60), ("B", 60, 90)]), [])
        self.assertEqual(
            find_conflicts([("outer", 10, 90), ("inner", 20, 30), ("later", 80, 100)]),
            [("outer", "inner"), ("outer", "later")],
        )

    def test_empty_input(self):
        self.assertEqual(find_conflicts([]), [])

    def test_invalid_intervals_and_duplicate_names(self):
        cases = [
            [("A", 1, 1)],
            [("A", 60, 10)],
            [("A", True, 5)],
            [("A", 0, 1441)],
            [("A", 0, 60), (" A ", 70, 80)],
        ]
        for bookings in cases:
            with self.subTest(bookings=bookings), self.assertRaises(ValueError):
                find_conflicts(bookings)


if __name__ == "__main__":
    unittest.main()
