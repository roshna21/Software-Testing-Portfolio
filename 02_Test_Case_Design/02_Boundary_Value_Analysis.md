# Boundary Value Analysis (BVA)

## What it is (plain English)

Programmers most often make mistakes **at the edges** of a range – writing `<` where they meant `<=`. BVA tests the values right at, just inside and just outside each edge.

For a range **min…max** we test: **min-1, min, min+1, max-1, max, max+1** (the "robust" 6-value form).

```
 party size:   0 | 1   2  .....  7   8 | 9
             ✗  |  ✓  ✓         ✓   ✓ |  ✗
              min-1 min min+1 max-1 max max+1
```

## Boundaries identified

| Rule | Range | Boundary values tested |
|---|---|---|
| R4 Party size | 1 – 8 | 0, 1, 2, 7, 8, 9 |
| R1 Name length (after trimming) | 2 – 50 chars | 1, 2, 3, 49, 50, 51, plus `" A "` (3 chars with spaces, 1 after trim) |
| R2 Phone length | exactly 10 | 9, 10, 11 |
| R5 Booking date | today … today+30 | today-1, today, today+1, today+29, today+30, today+31 |
| R6 Time slot | 11:00 … 21:30 | 10:30, 11:00, 11:30, 21:00, 21:30, 22:00 |
| R6 Not already passed | slot > now | slot = now |
| R7 90-minute table hold | existing booking 19:00–20:30 | new start 17:30, 18:00, 18:30, 19:00, 20:00, 20:30 |
| R10 Free-cancellation window | ≥ 2 hours notice | 2h 01m, 2h 00m, 1h 59m |

## Test cases

Fixed clock: **Mon 16 Nov 2026, 10:00** → today+30 = 16 Dec 2026.

| TC ID | Rule | Input | Expected |
|---|---|---|---|
| TC-BVA-01 | R4 | party = 0 | Rejected – *party size* error |
| TC-BVA-02 | R4 | party = 1 | Accepted |
| TC-BVA-03 | R4 | party = 2 | Accepted |
| TC-BVA-04 | R4 | party = 7 | Accepted |
| TC-BVA-05 | R4 | party = 8 | Accepted |
| TC-BVA-06 | R4 | party = 9 | Rejected – *party size* error (not "no table") |
| TC-BVA-07 | R1 | name = `A` (1) | Rejected |
| TC-BVA-08 | R1 | name = `Al` (2) | Accepted |
| TC-BVA-09 | R1 | name = `Ali` (3) | Accepted |
| TC-BVA-10 | R1 | name = 49 × `A` | Accepted |
| TC-BVA-11 | R1 | name = 50 × `A` | Accepted |
| TC-BVA-12 | R1 | name = 51 × `A` | Rejected |
| TC-BVA-13 | R1 | name = `" A "` (1 letter after trim) | Rejected |
| TC-BVA-14 | R2 | phone = `987654321` (9) | Rejected |
| TC-BVA-15 | R2 | phone = `9876543210` (10) | Accepted |
| TC-BVA-16 | R2 | phone = `98765432101` (11) | Rejected |
| TC-BVA-17 | R5 | date = 2026-11-15 (yesterday) | Rejected |
| TC-BVA-18 | R5 | date = 2026-11-16 (today) | Accepted |
| TC-BVA-19 | R5 | date = 2026-11-17 | Accepted |
| TC-BVA-20 | R5 | date = 2026-12-15 (+29) | Accepted |
| TC-BVA-21 | R5 | date = 2026-12-16 (+30) | Accepted |
| TC-BVA-22 | R5 | date = 2026-12-17 (+31) | Rejected |
| TC-BVA-23 | R6 | time = 10:30 | Rejected |
| TC-BVA-24 | R6 | time = 11:00 | Accepted |
| TC-BVA-25 | R6 | time = 11:30 | Accepted |
| TC-BVA-26 | R6 | time = 21:00 | Accepted |
| TC-BVA-27 | R6 | time = 21:30 | Accepted |
| TC-BVA-28 | R6 | time = 22:00 | Rejected |

### Overlap boundaries (R7)

Setup: a party of 7 is booked at **19:00** (only table T8 seats 7, so it holds T8 until 20:30). A second party of 7 then tries to book the same day.

| TC ID | New booking | New booking ends | Clash? | Expected |
|---|---|---|---|---|
| TC-BVA-29 | 17:30 | 19:00 | No – ends exactly when the other starts | Accepted |
| TC-BVA-30 | 18:00 | 19:30 | Yes – 30 min | Rejected (no table) |
| TC-BVA-31 | 18:30 | 20:00 | Yes – 60 min | Rejected (no table) |
| TC-BVA-32 | 19:00 | 20:30 | Yes – same slot | Rejected (no table) |
| TC-BVA-33 | 20:00 | 21:30 | Yes – starts before 20:30 | Rejected (no table) |
| TC-BVA-34 | 20:30 | 22:00 | No – starts exactly when the other ends | Accepted |

### Refund boundaries (R10)

Setup: party of 6 (deposit ₹600) booked for today 14:00, then cancelled at the time shown.

| TC ID | Cancelled at | Notice | Expected refund |
|---|---|---|---|
| TC-BVA-35 | 11:59 | 2 h 01 m | ₹600 |
| TC-BVA-36 | 12:00 | 2 h 00 m | ₹600 |
| TC-BVA-37 | 12:01 | 1 h 59 m | ₹0 |

### Added after mutation testing

| TC ID | Rule | Input | Expected |
|---|---|---|---|
| TC-BVA-38 | R6 | Clock 13:00, book today 13:00 (slot = now) | Rejected – *This time has already passed* |

**Automation:** `05_Test_Automation/unit/test_boundary_value_analysis.py`
