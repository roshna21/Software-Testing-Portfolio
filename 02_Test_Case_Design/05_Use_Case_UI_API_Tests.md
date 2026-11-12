# Functional, API and UI Test Cases (Use-case / scenario based)

These cover how the pieces work together: table allocation (R7), the REST API (R12) and the web interface (R13).

## A. Table allocation (R7)

All bookings on Wed 18 Nov 2026, 19:00. Tables: T1(2) T2(2) T3(4) T4(4) T5(4) T6(6) T7(6) T8(8).

| TC ID | Scenario | Expected |
|---|---|---|
| TC-TA-01 | Party of 2 | Gets T1 (smallest that fits) |
| TC-TA-02 | Party of 3 | Gets T3 (first 4-seater) |
| TC-TA-03 | Party of 5 | Gets T6 (first 6-seater) |
| TC-TA-04 | Two couples, same slot | T1 then T2 |
| TC-TA-05 | Third couple, same slot | T3 (moves up a size) |
| TC-TA-06 | All 8 tables booked, then a party of 1 | Rejected – "No table available" |
| TC-TA-07 | T8 taken, another party of 7 | Rejected – tables are not combined |

## B. REST API (R12)

| TC ID | Request | Expected |
|---|---|---|
| TC-API-01 | `GET /api/health` | 200, `status: ok` |
| TC-API-02 | `GET /api/tables` | 200, 8 tables, 36 seats |
| TC-API-03 | `POST /api/reservations` valid body | 201, status CONFIRMED, ID assigned |
| TC-API-04 | `POST` with phone `12345` | 400, `field: phone` |
| TC-API-05 | `POST` with a non-JSON body | 400 |
| TC-API-06 | `GET /api/reservations/{id}` | 200, same ID |
| TC-API-07 | `GET /api/reservations/R9999` | 404 |
| TC-API-08 | `GET /api/reservations?date=2026-11-19` | 200, only that date |
| TC-API-09 | `PATCH …/status` → SEATED | 200, SEATED |
| TC-API-10 | `PATCH …/status` CONFIRMED → COMPLETED | 409, `invalid_transition` |
| TC-API-11 | `DELETE /api/reservations/{id}` | 200, CANCELLED |
| TC-API-12 | `GET /api/availability` after booking T1 at 19:00, check 19:30 | T1 `available: false`; the other 7 tables `available: true` |
| TC-API-13 | Same phone, same day, second booking | 409, `duplicate` |

The same API is also tested from **Postman** (15 requests, 31 assertions): `05_Test_Automation/postman/`.

| Postman ID | Request | Key assertions |
|---|---|---|
| PM-00 | Reset test data | 200 |
| PM-01 | Health | 200, `ok`, response < 500 ms |
| PM-02 | List tables | 8 tables, 36 seats |
| PM-03 | Create valid booking | 201, CONFIRMED, T1, schema fields; saves ID |
| PM-04 | Get by ID | 200, same ID |
| PM-05 | Invalid phone | 400, field = phone |
| PM-06 | Party of 8 (upper boundary) | 201, T8 |
| PM-07 | Party of 7 at 19:00 | 201 |
| PM-08 | Party of 7 at 18:30 (overlaps PM-07) | 409, `no_table` |
| PM-09 | Duplicate phone same day | 409, `duplicate` |
| PM-10 | Seat guest | 200, SEATED |
| PM-11 | Complete visit | 200, COMPLETED |
| PM-12 | Cancel completed visit | 409, `invalid_transition` |
| PM-13 | Unknown ID | 404 |
| PM-14 | Availability at 19:30 | T8 not available |

## C. Web UI – Selenium WebDriver (R7, R13)

| TC ID | Steps | Expected |
|---|---|---|
| TC-UI-01 | Open home page | Booking form visible; title contains "Book a table" |
| TC-UI-02 | Fill valid details (2 guests, Wed 13:00) → Reserve | Confirmation page, reservation ID shown, table T1 |
| TC-UI-03 | Enter phone `12345` → Reserve | Error message about the phone number |
| TC-UI-04 | Name "Rahul Verma", phone `12345`, 3 guests → Reserve | Error shown **and** name, phone and guests are still filled in |
| TC-UI-05 | Book 6 guests Wed 19:00 → Cancel reservation | Status CANCELLED, refund ₹600 |
| TC-UI-06 | Book → Staff view → Seat → Complete | Status SEATED, then COMPLETED |
| TC-UI-07 | Book 6 guests Sat 21 Nov 19:00 | Deposit ₹900 |
| TC-UI-08 | Open `/reservation/R9999` | "Reservation R9999 not found" |

**Automation:** `05_Test_Automation/unit/test_table_allocation.py`, `05_Test_Automation/api/test_api.py`, `05_Test_Automation/ui/test_ui_selenium.py`
