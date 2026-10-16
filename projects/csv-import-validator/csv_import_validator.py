"""Return accepted CSV orders and line-specific row errors."""

from __future__ import annotations

import csv
import io


def validate_orders(csv_text):
    """Validate sku/qty records while continuing after ordinary row errors."""
    reader = csv.DictReader(io.StringIO(csv_text))
    accepted = []
    errors = []
    if not {"sku", "qty"} <= set(reader.fieldnames or []):
        return {"accepted": accepted, "errors": [(1, "missing required headers")]}
    for row in reader:
        line = reader.line_num
        if None in row or not isinstance(row.get("sku"), str) or not isinstance(row.get("qty"), str):
            errors.append((line, "malformed row"))
            continue
        sku = row["sku"].strip()
        if not sku:
            errors.append((line, "missing sku"))
            continue
        try:
            quantity = int(row["qty"].strip())
        except ValueError:
            errors.append((line, "invalid qty"))
            continue
        if quantity <= 0:
            errors.append((line, "invalid qty"))
            continue
        accepted.append((sku, quantity))
    return {"accepted": accepted, "errors": errors}


if __name__ == "__main__":
    sample = "sku,qty\nA-1,2\n,4\nB-2,not-an-int\nC-3,1\n"
    print(validate_orders(sample))
