# Cycle 1 – Test Execution Log

| Item | Detail |
|---|---|
| Build under test | Restaurant Table Reservation System **v1.0.0** |
| Executed on | 12 Nov 2026, 07:40 |
| Test clock | Mon 16 Nov 2026, 10:00 (frozen) |
| Environment | Python 3, Flask, pytest, Selenium 4 + Chrome (headless), Newman |
| Executed | **127** test cases + **15** Postman requests |
| Result | **114 passed**, **13 failed**, 0 skipped → pass rate **89.8%** |

## Summary by technique

| Technique | Executed | Passed | Failed | Pass % |
|---|---:|---:|---:|---:|
| Equivalence Partitioning | 29 | 27 | 2 | 93% |
| Boundary Value Analysis | 37 | 31 | 6 | 84% |
| Decision Table | 17 | 15 | 2 | 88% |
| State Transition | 16 | 14 | 2 | 88% |
| Table Allocation | 7 | 7 | 0 | 100% |
| REST API (pytest) | 13 | 13 | 0 | 100% |
| Web UI (Selenium) | 8 | 7 | 1 | 88% |
| Postman / Newman (assertions) | 31 | 25 | 6 | 81% |
| **Total (test cases)** | **127** | **114** | **13** | **90%** |

## Failed test cases

| TC ID | Expected | Actual | Defect |
|---|---|---|---|
| TC-EP-05 | Rejected | Accepted (R1001, table T1, deposit Rs.0) | to be logged |
| TC-EP-10 | Rejected | Accepted (R1001, table T1, deposit Rs.0) | to be logged |
| TC-BVA-05 | Accepted | Rejected: Party size must be between 1 and 8 | to be logged |
| TC-BVA-13 | Rejected | Accepted (R1001, table T1, deposit Rs.0) | to be logged |
| TC-BVA-16 | Rejected | Accepted (R1001, table T1, deposit Rs.0) | to be logged |
| TC-BVA-22 | Rejected | Accepted (R1001, table T1, deposit Rs.0) | to be logged |
| TC-BVA-30 | Rejected | Accepted (R1002, table T8, deposit Rs.700) | to be logged |
| TC-BVA-31 | Rejected | Accepted (R1002, table T8, deposit Rs.700) | to be logged |
| TC-DT-09 | Deposit Rs.0 | Deposit Rs.300 | to be logged |
| TC-DT-16 | Refused | Cancelled (status CANCELLED) | to be logged |
| TC-ST-06 | Refused, status stays SEATED | Allowed: status is now CANCELLED | to be logged |
| TC-ST-08 | Refused, status stays COMPLETED | Allowed: status is now CANCELLED | to be logged |
| TC-UI-04 | Name 'Rahul Verma', phone '12345', guests '3' still filled in | Name '', phone '', guests '2' | to be logged |

## Equivalence Partitioning

| TC ID | Test input / scenario | Expected result | Actual result | Status | Defect |
|---|---|---|---|---|---|
| TC-EP-01 | V1 · name = `Priya Sharma` | Accepted | Accepted (R1001, table T1, deposit Rs.0) | ✅ Pass |  |
| TC-EP-02 | I1 · name = `` (empty) | Rejected | Rejected: Name must be 2 to 50 characters | ✅ Pass |  |
| TC-EP-03 | I2 · name = `Priya123` | Rejected | Rejected: Name may contain only letters and spaces | ✅ Pass |  |
| TC-EP-04 | I3 · name = `Priya@#` | Rejected | Rejected: Name may contain only letters and spaces | ✅ Pass |  |
| TC-EP-05 | I4 · name = `"    "` (4 spaces) | Rejected | Accepted (R1001, table T1, deposit Rs.0) | ❌ Fail |  |
| TC-EP-06 | V2 · phone = `9876543210` | Accepted | Accepted (R1001, table T1, deposit Rs.0) | ✅ Pass |  |
| TC-EP-07 | I5 · phone = `5876543210` | Rejected | Rejected: Phone must be a 10-digit mobile number starting with 6-9 | ✅ Pass |  |
| TC-EP-08 | I6 · phone = `98765abcde` | Rejected | Rejected: Phone must be a 10-digit mobile number starting with 6-9 | ✅ Pass |  |
| TC-EP-09 | I7 · phone = `98765` | Rejected | Rejected: Phone must be a 10-digit mobile number starting with 6-9 | ✅ Pass |  |
| TC-EP-10 | I8 · phone = `987654321012` (12 digits) | Rejected | Accepted (R1001, table T1, deposit Rs.0) | ❌ Fail |  |
| TC-EP-11 | V3 · email = blank | Accepted | Accepted (R1001, table T1, deposit Rs.0) | ✅ Pass |  |
| TC-EP-12 | V4 · email = `priya@example.com` | Accepted | Accepted (R1001, table T1, deposit Rs.0) | ✅ Pass |  |
| TC-EP-13 | I9 · email = `priya.example.com` | Rejected | Rejected: Email address is not valid | ✅ Pass |  |
| TC-EP-14 | V5 · party = `4` | Accepted | Accepted (R1001, table T3, deposit Rs.0) | ✅ Pass |  |
| TC-EP-15 | I10 · party = `-3` | Rejected | Rejected: Party size must be between 1 and 8 | ✅ Pass |  |
| TC-EP-16 | I11 · party = `15` | Rejected | Rejected: Party size must be between 1 and 8 | ✅ Pass |  |
| TC-EP-17 | I12 · party = `four` | Rejected | Rejected: Party size must be a whole number | ✅ Pass |  |
| TC-EP-18 | I13 · party = `2.5` | Rejected | Rejected: Party size must be a whole number | ✅ Pass |  |
| TC-EP-19 | V6 · date = `2026-11-25` | Accepted | Accepted (R1001, table T1, deposit Rs.0) | ✅ Pass |  |
| TC-EP-20 | I14 · date = `2026-11-01` | Rejected | Rejected: Date cannot be in the past | ✅ Pass |  |
| TC-EP-21 | I15 · date = `2027-03-01` | Rejected | Rejected: Bookings open only 30 days in advance | ✅ Pass |  |
| TC-EP-22 | I16 · date = `25/11/2026` | Rejected | Rejected: Date must be in YYYY-MM-DD format | ✅ Pass |  |
| TC-EP-23 | V7 · time = `13:00` | Accepted | Accepted (R1001, table T1, deposit Rs.0) | ✅ Pass |  |
| TC-EP-24 | I17 · time = `09:00` | Rejected | Rejected: Bookings are accepted from 11:00 to 21:30 | ✅ Pass |  |
| TC-EP-25 | I18 · time = `22:30` | Rejected | Rejected: Bookings are accepted from 11:00 to 21:30 | ✅ Pass |  |
| TC-EP-26 | I19 · time = `13:15` | Rejected | Rejected: Time must be on the hour or half hour | ✅ Pass |  |
| TC-EP-27 | I20 · today 13:00 when clock is 15:00 | Rejected | Rejected: This time has already passed | ✅ Pass |  |
| TC-EP-28 | I21 · same phone books 13:00 and 19:00 on same day | Rejected | Rejected: Phone 9876543210 already has reservation R1001 on this date | ✅ Pass |  |
| TC-EP-29 | V8 · same phone books 18 Nov and 19 Nov | Accepted | Accepted (R1002, table T1, deposit Rs.0) | ✅ Pass |  |

## Boundary Value Analysis

| TC ID | Test input / scenario | Expected result | Actual result | Status | Defect |
|---|---|---|---|---|---|
| TC-BVA-01 | R4 · party = 0 | Rejected | Rejected: Party size must be between 1 and 8 | ✅ Pass |  |
| TC-BVA-02 | R4 · party = 1 | Accepted | Accepted (R1001, table T1, deposit Rs.0) | ✅ Pass |  |
| TC-BVA-03 | R4 · party = 2 | Accepted | Accepted (R1001, table T1, deposit Rs.0) | ✅ Pass |  |
| TC-BVA-04 | R4 · party = 7 | Accepted | Accepted (R1001, table T8, deposit Rs.700) | ✅ Pass |  |
| TC-BVA-05 | R4 · party = 8 | Accepted | Rejected: Party size must be between 1 and 8 | ❌ Fail |  |
| TC-BVA-06 | R4 · party = 9 | Rejected | Rejected: Party size must be between 1 and 8 | ✅ Pass |  |
| TC-BVA-07 | R1 · name = `A` (1) | Rejected | Rejected: Name must be 2 to 50 characters | ✅ Pass |  |
| TC-BVA-08 | R1 · name = `Al` (2) | Accepted | Accepted (R1001, table T1, deposit Rs.0) | ✅ Pass |  |
| TC-BVA-09 | R1 · name = `Ali` (3) | Accepted | Accepted (R1001, table T1, deposit Rs.0) | ✅ Pass |  |
| TC-BVA-10 | R1 · name = 49 × `A` | Accepted | Accepted (R1001, table T1, deposit Rs.0) | ✅ Pass |  |
| TC-BVA-11 | R1 · name = 50 × `A` | Accepted | Accepted (R1001, table T1, deposit Rs.0) | ✅ Pass |  |
| TC-BVA-12 | R1 · name = 51 × `A` | Rejected | Rejected: Name must be 2 to 50 characters | ✅ Pass |  |
| TC-BVA-13 | R1 · name = `" A "` (1 letter after trim) | Rejected | Accepted (R1001, table T1, deposit Rs.0) | ❌ Fail |  |
| TC-BVA-14 | R2 · phone = `987654321` (9) | Rejected | Rejected: Phone must be a 10-digit mobile number starting with 6-9 | ✅ Pass |  |
| TC-BVA-15 | R2 · phone = `9876543210` (10) | Accepted | Accepted (R1001, table T1, deposit Rs.0) | ✅ Pass |  |
| TC-BVA-16 | R2 · phone = `98765432101` (11) | Rejected | Accepted (R1001, table T1, deposit Rs.0) | ❌ Fail |  |
| TC-BVA-17 | R5 · date = 2026-11-15 (yesterday) | Rejected | Rejected: Date cannot be in the past | ✅ Pass |  |
| TC-BVA-18 | R5 · date = 2026-11-16 (today) | Accepted | Accepted (R1001, table T1, deposit Rs.0) | ✅ Pass |  |
| TC-BVA-19 | R5 · date = 2026-11-17 | Accepted | Accepted (R1001, table T1, deposit Rs.0) | ✅ Pass |  |
| TC-BVA-20 | R5 · date = 2026-12-15 (+29) | Accepted | Accepted (R1001, table T1, deposit Rs.0) | ✅ Pass |  |
| TC-BVA-21 | R5 · date = 2026-12-16 (+30) | Accepted | Accepted (R1001, table T1, deposit Rs.0) | ✅ Pass |  |
| TC-BVA-22 | R5 · date = 2026-12-17 (+31) | Rejected | Accepted (R1001, table T1, deposit Rs.0) | ❌ Fail |  |
| TC-BVA-23 | R6 · time = 10:30 | Rejected | Rejected: Bookings are accepted from 11:00 to 21:30 | ✅ Pass |  |
| TC-BVA-24 | R6 · time = 11:00 | Accepted | Accepted (R1001, table T1, deposit Rs.0) | ✅ Pass |  |
| TC-BVA-25 | R6 · time = 11:30 | Accepted | Accepted (R1001, table T1, deposit Rs.0) | ✅ Pass |  |
| TC-BVA-26 | R6 · time = 21:00 | Accepted | Accepted (R1001, table T1, deposit Rs.0) | ✅ Pass |  |
| TC-BVA-27 | R6 · time = 21:30 | Accepted | Accepted (R1001, table T1, deposit Rs.0) | ✅ Pass |  |
| TC-BVA-28 | R6 · time = 22:00 | Rejected | Rejected: Bookings are accepted from 11:00 to 21:30 | ✅ Pass |  |
| TC-BVA-29 | 17:30 · 19:00 · No – ends exactly when the other starts | Accepted | Accepted (R1002, table T8, deposit Rs.700) | ✅ Pass |  |
| TC-BVA-30 | 18:00 · 19:30 · Yes – 30 min | Rejected | Accepted (R1002, table T8, deposit Rs.700) | ❌ Fail |  |
| TC-BVA-31 | 18:30 · 20:00 · Yes – 60 min | Rejected | Accepted (R1002, table T8, deposit Rs.700) | ❌ Fail |  |
| TC-BVA-32 | 19:00 · 20:30 · Yes – same slot | Rejected | Rejected: No table available for this party size and time | ✅ Pass |  |
| TC-BVA-33 | 20:00 · 21:30 · Yes – starts before 20:30 | Rejected | Rejected: No table available for this party size and time | ✅ Pass |  |
| TC-BVA-34 | 20:30 · 22:00 · No – starts exactly when the other ends | Accepted | Accepted (R1002, table T8, deposit Rs.700) | ✅ Pass |  |
| TC-BVA-35 | 11:59 · 2 h 01 m | Refund Rs.600 | Refund Rs.600 | ✅ Pass |  |
| TC-BVA-36 | 12:00 · 2 h 00 m | Refund Rs.600 | Refund Rs.600 | ✅ Pass |  |
| TC-BVA-37 | 12:01 · 1 h 59 m | Refund Rs.0 | Refund Rs.0 | ✅ Pass |  |

## Decision Table

| TC ID | Test input / scenario | Expected result | Actual result | Status | Defect |
|---|---|---|---|---|---|
| TC-DT-01 | 1 · 6 · Sat 21 Nov · 19:00 | Deposit Rs.900 | Deposit Rs.900 | ✅ Pass |  |
| TC-DT-02 | 2 · 6 · Sat 21 Nov · 13:00 | Deposit Rs.600 | Deposit Rs.600 | ✅ Pass |  |
| TC-DT-03 | 3 · 6 · Wed 18 Nov · 19:00 | Deposit Rs.600 | Deposit Rs.600 | ✅ Pass |  |
| TC-DT-04 | 4 · 6 · Wed 18 Nov · 13:00 | Deposit Rs.600 | Deposit Rs.600 | ✅ Pass |  |
| TC-DT-05 | 5 · 2 · Sat 21 Nov · 20:00 | Deposit Rs.300 | Deposit Rs.300 | ✅ Pass |  |
| TC-DT-06 | 6 · 2 · Sat 21 Nov · 13:00 | Deposit Rs.0 | Deposit Rs.0 | ✅ Pass |  |
| TC-DT-07 | 7 · 2 · Wed 18 Nov · 19:30 | Deposit Rs.0 | Deposit Rs.0 | ✅ Pass |  |
| TC-DT-08 | 8 · 2 · Wed 18 Nov · 13:00 | Deposit Rs.0 | Deposit Rs.0 | ✅ Pass |  |
| TC-DT-09 | Friday is **not** a weekend (C2 = N) · 2 · Fri 20 Nov · 19:00 | Deposit Rs.0 | Deposit Rs.300 | ❌ Fail |  |
| TC-DT-10 | Sunday + last peak slot (C2 = Y, C3 = Y) · 2 · Sun 22 Nov · 21:30 | Deposit Rs.300 | Deposit Rs.300 | ✅ Pass |  |
| TC-DT-11 | Just before peak (C3 = N) · 2 · Sat 21 Nov · 18:30 | Deposit Rs.0 | Deposit Rs.0 | ✅ Pass |  |
| TC-DT-12 | 1 · Party 6, deposit ₹600 · 12:00 (3 h notice) | CANCELLED, refund Rs.600 | CANCELLED, refund Rs.600 | ✅ Pass |  |
| TC-DT-13 | 2 · Party 6, deposit ₹600 · 14:00 (1 h notice) | CANCELLED, refund Rs.0 | CANCELLED, refund Rs.0 | ✅ Pass |  |
| TC-DT-14 | 3 · Party 2, no deposit · 12:00 | CANCELLED, refund Rs.0 | CANCELLED, refund Rs.0 | ✅ Pass |  |
| TC-DT-15 | 4 · Party 2, no deposit · 14:00 | CANCELLED, refund Rs.0 | CANCELLED, refund Rs.0 | ✅ Pass |  |
| TC-DT-16 | 5 · Booking already SEATED · any | Refused | Cancelled (status CANCELLED) | ❌ Fail |  |
| TC-DT-17 | 5 · Booking already CANCELLED · any | Refused | Refused: Cannot change status from CANCELLED to CANCELLED | ✅ Pass |  |

## State Transition

| TC ID | Test input / scenario | Expected result | Actual result | Status | Defect |
|---|---|---|---|---|---|
| TC-ST-01 | Valid · CONFIRMED · seat | CONFIRMED -> SEATED | CONFIRMED -> SEATED | ✅ Pass |  |
| TC-ST-02 | Valid · SEATED · complete | SEATED -> COMPLETED | SEATED -> COMPLETED | ✅ Pass |  |
| TC-ST-03 | Valid · CONFIRMED · cancel | CONFIRMED -> CANCELLED | CONFIRMED -> CANCELLED | ✅ Pass |  |
| TC-ST-04 | Valid · CONFIRMED · no-show | CONFIRMED -> NO_SHOW | CONFIRMED -> NO_SHOW | ✅ Pass |  |
| TC-ST-05 | Invalid · CONFIRMED · complete | Refused, status stays CONFIRMED | Refused, status stays CONFIRMED (Cannot change status from CONFIRMED to COMPLETED) | ✅ Pass |  |
| TC-ST-06 | Invalid · SEATED · cancel | Refused, status stays SEATED | Allowed: status is now CANCELLED | ❌ Fail |  |
| TC-ST-07 | Invalid · SEATED · no-show | Refused, status stays SEATED | Refused, status stays SEATED (Cannot change status from SEATED to NO_SHOW) | ✅ Pass |  |
| TC-ST-08 | Invalid · COMPLETED · cancel | Refused, status stays COMPLETED | Allowed: status is now CANCELLED | ❌ Fail |  |
| TC-ST-09 | Invalid · COMPLETED · seat | Refused, status stays COMPLETED | Refused, status stays COMPLETED (Cannot change status from COMPLETED to SEATED) | ✅ Pass |  |
| TC-ST-10 | Invalid · CANCELLED · seat | Refused, status stays CANCELLED | Refused, status stays CANCELLED (Cannot change status from CANCELLED to SEATED) | ✅ Pass |  |
| TC-ST-11 | Invalid · CANCELLED · cancel | Refused, status stays CANCELLED | Refused, status stays CANCELLED (Cannot change status from CANCELLED to CANCELLED) | ✅ Pass |  |
| TC-ST-12 | Invalid · NO_SHOW · seat | Refused, status stays NO_SHOW | Refused, status stays NO_SHOW (Cannot change status from NO_SHOW to SEATED) | ✅ Pass |  |
| TC-ST-13 | Invalid · NO_SHOW · cancel | Refused, status stays NO_SHOW | Refused, status stays NO_SHOW (Cannot change status from NO_SHOW to CANCELLED) | ✅ Pass |  |
| TC-ST-14 | Invalid event · CONFIRMED · "PAID" (unknown) | Refused: unknown status | Refused: Unknown status 'PAID' | ✅ Pass |  |
| TC-ST-15 | Full path · – · book → seat → complete | COMPLETED; same table bookable again | COMPLETED; next booking Accepted (R1002, table T8, deposit Rs.700) | ✅ Pass |  |
| TC-ST-16 | Side effect · CONFIRMED · cancel | Rejected before cancel, accepted after | Before: Rejected: No table available for this party size and time | After: Accepted (R1002, table T8, deposit Rs.700) | ✅ Pass |  |

## Table Allocation

| TC ID | Test input / scenario | Expected result | Actual result | Status | Defect |
|---|---|---|---|---|---|
| TC-TA-01 | Party of 2 | Accepted, table T1 | Accepted (R1001, table T1, deposit Rs.0) | ✅ Pass |  |
| TC-TA-02 | Party of 3 | Accepted, table T3 | Accepted (R1001, table T3, deposit Rs.0) | ✅ Pass |  |
| TC-TA-03 | Party of 5 | Accepted, table T6 | Accepted (R1001, table T6, deposit Rs.0) | ✅ Pass |  |
| TC-TA-04 | Two couples, same slot | T1 then T2 | Accepted (R1001, table T1, deposit Rs.0) | Accepted (R1002, table T2, deposit Rs.0) | ✅ Pass |  |
| TC-TA-05 | Third couple, same slot | Accepted, table T3 | Accepted (R1003, table T3, deposit Rs.0) | ✅ Pass |  |
| TC-TA-06 | All 8 tables booked, then a party of 1 | Rejected: No table available | Rejected: No table available for this party size and time | ✅ Pass |  |
| TC-TA-07 | T8 taken, another party of 7 | Rejected: No table available | Rejected: No table available for this party size and time | ✅ Pass |  |

## REST API (pytest)

| TC ID | Test input / scenario | Expected result | Actual result | Status | Defect |
|---|---|---|---|---|---|
| TC-API-01 | `GET /api/health` | 200, status ok | 200, status ok | ✅ Pass |  |
| TC-API-02 | `GET /api/tables` | 200, 8 tables, 36 seats | 200, 8 tables, 36 seats | ✅ Pass |  |
| TC-API-03 | `POST /api/reservations` valid body | 201, CONFIRMED, id assigned | 201, CONFIRMED, id R1001 | ✅ Pass |  |
| TC-API-04 | `POST` with phone `12345` | 400, field=phone | 400, field=phone | ✅ Pass |  |
| TC-API-05 | `POST` with a non-JSON body | 400 | 400 | ✅ Pass |  |
| TC-API-06 | `GET /api/reservations/{id}` | 200, id R1001 | 200, id R1001 | ✅ Pass |  |
| TC-API-07 | `GET /api/reservations/R9999` | 404 | 404 | ✅ Pass |  |
| TC-API-08 | `GET /api/reservations?date=2026-11-19` | 200, only 2026-11-19 bookings | 200, dates ['2026-11-19'] | ✅ Pass |  |
| TC-API-09 | `PATCH …/status` → SEATED | 200, SEATED | 200, SEATED | ✅ Pass |  |
| TC-API-10 | `PATCH …/status` CONFIRMED → COMPLETED | 409, invalid_transition | 409, invalid_transition | ✅ Pass |  |
| TC-API-11 | `DELETE /api/reservations/{id}` | 200, CANCELLED | 200, CANCELLED | ✅ Pass |  |
| TC-API-12 | `GET /api/availability` after booking T1 at 19:00, check 19:30 | 200, T1 unavailable | 200, T1 available=False | ✅ Pass |  |
| TC-API-13 | Same phone, same day, second booking | 409, duplicate | 409, duplicate | ✅ Pass |  |

## Web UI (Selenium)

| TC ID | Test input / scenario | Expected result | Actual result | Status | Defect |
|---|---|---|---|---|---|
| TC-UI-01 | Open home page | Booking form visible, title contains 'Book a table' | Form visible=True, title='Book a table · Reservations' | ✅ Pass |  |
| TC-UI-02 | Fill valid details (2 guests, Wed 13:00) → Reserve | Confirmation page with reservation ID and table T1 | Banner shown, R1001, table T1 | ✅ Pass |  |
| TC-UI-03 | Enter phone `12345` → Reserve | Error message about phone number | Phone must be a 10-digit mobile number starting with 6-9 | ✅ Pass |  |
| TC-UI-04 | Name "Rahul Verma", phone `12345`, 3 guests → Reserve | Name 'Rahul Verma', phone '12345', guests '3' still filled in | Name '', phone '', guests '2' | ❌ Fail |  |
| TC-UI-05 | Book 6 guests Wed 19:00 → Cancel reservation | Status CANCELLED, refund ₹600 | Status CANCELLED, refund ₹600 | ✅ Pass |  |
| TC-UI-06 | Book → Staff view → Seat → Complete | SEATED then COMPLETED | SEATED then COMPLETED | ✅ Pass |  |
| TC-UI-07 | Book 6 guests Sat 21 Nov 19:00 | Deposit ₹900 | Deposit ₹900 | ✅ Pass |  |
| TC-UI-08 | Open `/reservation/R9999` | 'Reservation R9999 not found' | Reservation R9999 not found | ✅ Pass |  |

## Postman collection (Newman)

| ID | Request | Assertions passed | Status | Failed assertions | Defect |
|---|---|---|---|---|---|
| PM-00 | Setup: reset test data | 1/1 | ✅ Pass |  |  |
| PM-01 | Health check | 3/3 | ✅ Pass |  |  |
| PM-02 | List tables | 3/3 | ✅ Pass |  |  |
| PM-03 | Create reservation (valid) | 4/4 | ✅ Pass |  |  |
| PM-04 | Get reservation by ID | 2/2 | ✅ Pass |  |  |
| PM-05 | Invalid phone rejected | 2/2 | ✅ Pass |  |  |
| PM-06 | Party of 8 accepted (upper boundary) | 0/2 | ❌ Fail | Status 201 Created; Table T8 assigned |  |
| PM-07 | Party of 7 at 19:00 (takes T8) | 1/1 | ✅ Pass |  |  |
| PM-08 | Overlapping booking at 18:30 refused | 0/2 | ❌ Fail | Status 409 Conflict (no double booking); Code no_table |  |
| PM-09 | Duplicate phone same day refused | 2/2 | ✅ Pass |  |  |
| PM-10 | Seat the guest | 2/2 | ✅ Pass |  |  |
| PM-11 | Complete the visit | 2/2 | ✅ Pass |  |  |
| PM-12 | Cancelling a completed visit is refused | 0/2 | ❌ Fail | Status 409; Code invalid_transition |  |
| PM-13 | Unknown reservation gives 404 | 1/1 | ✅ Pass |  |  |
| PM-14 | Availability shows T8 busy | 2/2 | ✅ Pass |  |  |
