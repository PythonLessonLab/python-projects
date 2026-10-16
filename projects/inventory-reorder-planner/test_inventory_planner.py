import unittest

from inventory_planner import plan_reorders


class InventoryPlannerTests(unittest.TestCase):
    def test_sample_plan_is_ordered_and_source_is_unchanged(self):
        items = [
            {"name": "Pen", "stock": 2, "minimum": 3, "target": 8},
            {"name": "Paper", "stock": 5, "minimum": 5, "target": 9},
            {"name": "Tape", "stock": 0, "minimum": 2, "target": 4},
        ]
        before = [dict(item) for item in items]
        self.assertEqual(plan_reorders(items), [("Pen", 6), ("Tape", 4)])
        self.assertEqual(items, before)

    def test_empty_and_exact_boundary(self):
        self.assertEqual(plan_reorders([]), [])
        self.assertEqual(
            plan_reorders([{"name": "Paper", "stock": 5, "minimum": 5, "target": 9}]),
            [],
        )

    def test_generator_is_consumed_once(self):
        items = ({"name": name, "stock": 0, "minimum": 1, "target": 3} for name in ("A", "B"))
        self.assertEqual(plan_reorders(items), [("A", 3), ("B", 3)])

    def test_invalid_records_are_rejected(self):
        cases = [
            [{"name": "A", "stock": True, "minimum": 1, "target": 3}],
            [{"name": "A", "stock": -1, "minimum": 1, "target": 3}],
            [{"name": "A", "stock": 0, "minimum": 3, "target": 2}],
            [{"name": " ", "stock": 0, "minimum": 1, "target": 3}],
            [
                {"name": "A", "stock": 0, "minimum": 1, "target": 3},
                {"name": " A ", "stock": 0, "minimum": 1, "target": 3},
            ],
        ]
        for items in cases:
            with self.subTest(items=items), self.assertRaises(ValueError):
                plan_reorders(items)


if __name__ == "__main__":
    unittest.main()
