# CSV Expense Tracker

Build a small category report from CSV rows. The [interactive lesson](https://pythonlessonlab.com/lessons/project-csv-expense-tracker/) and [video walkthrough](https://youtu.be/A5l-ok68lrI) first show two mistakes: splitting CSV by hand breaks on quoted commas, and adding amount strings concatenates text. This repository version uses `csv.DictReader` and `Decimal` and adds basic input validation for local files.

## Run the sample

From the repository root:

```sh
python projects/csv-expense-tracker/expense_tracker.py
```

Expected output:

```text
Food: $15.50
Travel: $4.25
```

The command reads the fictional `sample-expenses.csv` next to the program. To analyze a different local CSV file with `category` and `amount` headers:

```sh
python projects/csv-expense-tracker/expense_tracker.py path/to/expenses.csv
```

The script only reads the file. It does not upload it, save a copy, or modify it. Do not commit private financial exports to a public repository.

## Try it yourself

1. Change a Food amount in `sample-expenses.csv`. Predict the new total before running the command again.
2. Add `"Food, snacks",2.40` as a CSV row. The comma inside the quoted category remains part of one field.
3. Put the headers in `amount,category` order and swap each row's values. Named fields keep the report correct.
4. Run the tests:

   ```sh
   python -m unittest discover -s projects/csv-expense-tracker -p "test_*.py"
   ```

The core function, `summarize_expenses(csv_text)`, returns a dictionary whose values are `Decimal` objects. It accepts header-only CSV and returns an empty dictionary. The command displays totals in sorted category order with two decimal places. It reports missing fields, blank categories, non-numeric amounts, and non-finite values as input errors.

This is a learning example for one USD-like decimal amount column. It does not handle multiple currencies, tax rules, duplicate transaction IDs, or real accounting requirements.
