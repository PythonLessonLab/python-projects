# Project: CSV Import Validator

Companion lesson: https://pythonlessonlab.com/lessons/project-csv-import-validator/

Read `sku,qty` CSV text and return both accepted rows and line-specific errors.
The importer continues after an ordinary bad row instead of losing later valid
records. It uses `csv.DictReader`, so quoted commas and reordered headers work.

From this directory:

```powershell
py -3 csv_import_validator.py
py -3 -m unittest -v
```

The demo accepts `A-1` and `C-3`, then reports errors on source lines 3 and 4.
Try a header-only file and a row with an extra cell. This code reads the sample
string in memory and does not write imported data to a database.
