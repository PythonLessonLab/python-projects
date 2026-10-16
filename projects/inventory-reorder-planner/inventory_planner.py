"""Produce a deterministic reorder proposal without mutating stock records."""

from __future__ import annotations


def plan_reorders(items):
    """Return (name, units_to_target) for stock strictly below its minimum.

    Validate the full iterable before returning a plan. Names are unique after
    trimming, quantities are nonnegative integers, and target >= minimum.
    """
    records = list(items)
    validated = []
    seen = set()
    for item in records:
        try:
            name = item["name"].strip()
            stock, minimum, target = (item[key] for key in ("stock", "minimum", "target"))
        except (KeyError, AttributeError, TypeError) as error:
            raise ValueError("invalid item") from error
        if (
            not name
            or name in seen
            or any(type(value) is not int or value < 0 for value in (stock, minimum, target))
            or target < minimum
        ):
            raise ValueError("invalid item")
        seen.add(name)
        validated.append((name, stock, minimum, target))
    return [(name, target - stock) for name, stock, minimum, target in validated if stock < minimum]


if __name__ == "__main__":
    sample = [
        {"name": "Pen", "stock": 2, "minimum": 3, "target": 8},
        {"name": "Paper", "stock": 5, "minimum": 5, "target": 9},
        {"name": "Tape", "stock": 0, "minimum": 2, "target": 4},
    ]
    print(plan_reorders(sample))
