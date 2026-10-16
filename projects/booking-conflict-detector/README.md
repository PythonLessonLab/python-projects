# Project: Booking Conflict Detector

Companion lesson: https://pythonlessonlab.com/lessons/project-booking-conflict-detector/

Each booking is `(name, start_minute, end_minute)` within one day. Intervals are
half-open: `[start, end)`. A meeting ending at 10:00 does not conflict with one
starting at 10:00. Conflicts are returned as name pairs in input-pair order.

From this directory:

```powershell
py -3 booking_conflicts.py
py -3 -m unittest -v
```

Expected demo output: `[('A', 'C'), ('B', 'C')]`.

Try one interval entirely inside another and two intervals that only touch.
Dates, time zones, rooms, recurrence, and cancellations are outside this small
interval model.
