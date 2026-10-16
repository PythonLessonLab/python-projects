"""Find conflicts between half-open booking intervals within one day."""

from __future__ import annotations


def find_conflicts(bookings):
    """Return overlapping name pairs in source pair order.

    Each booking is (name, start_minute, end_minute), representing [start, end).
    Touching endpoints are therefore not conflicts.
    """
    records = list(bookings)
    validated = []
    seen = set()
    for item in records:
        try:
            name, start, end = item
        except (TypeError, ValueError) as error:
            raise ValueError("invalid booking") from error
        if not isinstance(name, str) or not name.strip():
            raise ValueError("invalid booking")
        name = name.strip()
        if (
            name in seen
            or type(start) is not int
            or type(end) is not int
            or not 0 <= start < end <= 1440
        ):
            raise ValueError("invalid booking")
        seen.add(name)
        validated.append((name, start, end))
    conflicts = []
    for index, first in enumerate(validated):
        for second in validated[index + 1 :]:
            if first[1] < second[2] and second[1] < first[2]:
                conflicts.append((first[0], second[0]))
    return conflicts


if __name__ == "__main__":
    sample = [("A", 540, 600), ("B", 600, 660), ("C", 570, 630)]
    print(find_conflicts(sample))
