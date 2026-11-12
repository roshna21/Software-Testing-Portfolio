# Equivalence Partitioning (EP)

## What it is (plain English)

If a rule treats a group of inputs the same way, testing one input from that group is as good as testing all of them. So we split every input into **classes** (valid and invalid) and pick **one representative value per class**.

Example: for party size 1–8, the values 2, 4 and 6 all behave the same ("accepted"), so one test with `4` covers the whole valid class. `-3`, `15`, `"four"` and `2.5` each represent a different *invalid* class.

## Equivalence classes

| Input | Valid classes | Invalid classes |
|---|---|---|
| Name (R1) | V1: 2–50 letters/spaces | I1: empty · I2: contains digits · I3: special characters · I4: only spaces |
| Phone (R2) | V2: 10 digits starting 6–9 | I5: starts with 0–5 · I6: contains letters · I7: fewer than 10 digits · I8: more than 10 digits |
| Email (R3) | V3: blank · V4: valid format | I9: invalid format |
| Party size (R4) | V5: 1–8 | I10: negative · I11: greater than 8 · I12: not a number · I13: decimal |
| Date (R5) | V6: today … today+30 | I14: past · I15: beyond 30 days · I16: wrong format |
| Time (R6) | V7: 11:00–21:30 at :00/:30 | I17: before 11:00 · I18: after 21:30 · I19: not :00/:30 · I20: already passed today |
| Phone per day (R11) | V8: same phone, different day | I21: same phone, same day |

## Test cases

All tests start from a valid booking (Priya Sharma · 9876543210 · 2 guests · Wed 18 Nov 2026 · 13:00) and change **one** field. "Today" is fixed at Mon 16 Nov 2026, 10:00.

| TC ID | Class | Input | Expected result |
|---|---|---|---|
| TC-EP-01 | V1 | name = `Priya Sharma` | Accepted |
| TC-EP-02 | I1 | name = `` (empty) | Rejected – name required |
| TC-EP-03 | I2 | name = `Priya123` | Rejected – letters only |
| TC-EP-04 | I3 | name = `Priya@#` | Rejected – letters only |
| TC-EP-05 | I4 | name = `"    "` (4 spaces) | Rejected – name required/too short |
| TC-EP-06 | V2 | phone = `9876543210` | Accepted |
| TC-EP-07 | I5 | phone = `5876543210` | Rejected |
| TC-EP-08 | I6 | phone = `98765abcde` | Rejected |
| TC-EP-09 | I7 | phone = `98765` | Rejected |
| TC-EP-10 | I8 | phone = `987654321012` (12 digits) | Rejected |
| TC-EP-11 | V3 | email = blank | Accepted |
| TC-EP-12 | V4 | email = `priya@example.com` | Accepted |
| TC-EP-13 | I9 | email = `priya.example.com` | Rejected |
| TC-EP-14 | V5 | party = `4` | Accepted |
| TC-EP-15 | I10 | party = `-3` | Rejected |
| TC-EP-16 | I11 | party = `15` | Rejected |
| TC-EP-17 | I12 | party = `four` | Rejected |
| TC-EP-18 | I13 | party = `2.5` | Rejected |
| TC-EP-19 | V6 | date = `2026-11-25` | Accepted |
| TC-EP-20 | I14 | date = `2026-11-01` | Rejected – past |
| TC-EP-21 | I15 | date = `2027-03-01` | Rejected – too far ahead |
| TC-EP-22 | I16 | date = `25/11/2026` | Rejected – format |
| TC-EP-23 | V7 | time = `13:00` | Accepted |
| TC-EP-24 | I17 | time = `09:00` | Rejected |
| TC-EP-25 | I18 | time = `22:30` | Rejected |
| TC-EP-26 | I19 | time = `13:15` | Rejected |
| TC-EP-27 | I20 | today 13:00 when clock is 15:00 | Rejected – time passed |
| TC-EP-28 | I21 | same phone books 13:00 and 19:00 on same day | Second booking rejected (409 duplicate) |
| TC-EP-29 | V8 | same phone books 18 Nov and 19 Nov | Both accepted |

**Automation:** `05_Test_Automation/unit/test_equivalence_partitioning.py`
