# Project: Inventory Reorder Planner

Companion lesson: https://pythonlessonlab.com/lessons/project-inventory-reorder-planner/

Turn stock records into an order proposal. An item is reordered only when
`stock < minimum`; the quantity is `target - stock`. The report follows input
order, validates the complete catalog, and leaves the source unchanged.

From this directory:

```powershell
py -3 inventory_planner.py
py -3 -m unittest -v
```

Expected demo output: `[('Pen', 6), ('Tape', 4)]`.

Try stock exactly equal to minimum, a zero-stock item, and two names that differ
only in surrounding spaces. This is a teaching model: it does not account for
lead time, pack sizes, reservations, or purchasing costs.
