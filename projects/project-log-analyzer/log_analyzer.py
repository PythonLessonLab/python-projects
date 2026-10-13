"""A small, format-specific Python log analyzer.

Expected record: timestamp | level | message. Timestamp syntax is not
validated; this teaching project checks the three-field shape only.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def summarize_log(log_text: str) -> tuple[dict[str, int], list[str], int]:
    """Return level counts, ERROR messages in input order, and skipped rows."""
    counts: dict[str, int] = {}
    errors: list[str] = []
    skipped = 0
    for raw_line in log_text.splitlines():
        if not raw_line.strip():
            continue
        parts = [part.strip() for part in raw_line.split("|", 2)]
        if len(parts) != 3 or not all(parts):
            skipped += 1
            continue
        timestamp, level, message = parts
        level = level.upper()
        counts[level] = counts.get(level, 0) + 1
        if level == "ERROR":
            errors.append(message)
    return counts, errors, skipped


def format_report(summary: tuple[dict[str, int], list[str], int]) -> str:
    counts, errors, skipped = summary
    lines = [f"{level}: {counts[level]}" for level in sorted(counts)]
    lines.append(f"Skipped: {skipped}")
    lines.append("Errors: " + ("; ".join(errors) if errors else "none"))
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize pipe-delimited log records")
    parser.add_argument("path", type=Path, help="UTF-8 log file to inspect")
    args = parser.parse_args()
    print(format_report(summarize_log(args.path.read_text(encoding="utf-8"))))


if __name__ == "__main__":
    main()
