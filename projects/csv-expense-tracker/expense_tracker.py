"""Summarize a small CSV expense report by category.

Companion project: https://pythonlessonlab.com/lessons/project-csv-expense-tracker/
"""

import argparse
import csv
from decimal import Decimal, InvalidOperation
from io import StringIO
from pathlib import Path


def summarize_expenses(csv_text):
    """Return category totals as Decimal values from CSV text.

    Required headers are ``category`` and ``amount``. Extra named columns are
    ignored. A header-only CSV returns an empty dictionary.
    """
    reader = csv.DictReader(StringIO(csv_text, newline=""), strict=True)
    if reader.fieldnames is None:
        raise ValueError("CSV needs a category,amount header row")

    missing = {"category", "amount"} - set(reader.fieldnames)
    if missing:
        raise ValueError("CSV is missing required header(s): " + ", ".join(sorted(missing)))

    totals = {}
    try:
        for row in reader:
            if None in row or row["category"] is None or row["amount"] is None:
                raise ValueError(f"CSV row ending at line {reader.line_num} has missing or extra fields")

            category = row["category"].strip()
            if not category:
                raise ValueError(f"CSV row ending at line {reader.line_num} has a blank category")

            try:
                amount = Decimal(row["amount"].strip())
            except InvalidOperation as exc:
                raise ValueError(f"CSV row ending at line {reader.line_num} has an invalid amount") from exc
            if not amount.is_finite():
                raise ValueError(f"CSV row ending at line {reader.line_num} has a non-finite amount")

            totals[category] = totals.get(category, Decimal("0")) + amount
    except csv.Error as exc:
        raise ValueError(f"Invalid CSV: {exc}") from exc

    return totals


def main():
    parser = argparse.ArgumentParser(description="Sum CSV expenses by category")
    parser.add_argument(
        "csv_file",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("sample-expenses.csv"),
        help="CSV file with category and amount headers (default: bundled sample)",
    )
    args = parser.parse_args()

    try:
        csv_text = args.csv_file.read_text(encoding="utf-8-sig")
        totals = summarize_expenses(csv_text)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    for category in sorted(totals):
        print(f"{category}: ${totals[category]:.2f}")


if __name__ == "__main__":
    main()
