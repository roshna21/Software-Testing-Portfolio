"""TC-BVA-01 .. TC-BVA-37: Boundary Value Analysis tests.

For each range we test min-1, min, min+1, max-1, max, max+1.
"Today" is frozen at Monday 2026-11-16 10:00 (see conftest.py).
"""
from datetime import datetime

import pytest

from conftest import attempt, booking

ACCEPT, REJECT = "Accepted", "Rejected"

BVA_CASES = [
    # --- R4 party size: 1 .. 8 ---
    ("TC-BVA-01", "party_size", 0, REJECT),
    ("TC-BVA-02", "party_size", 1, ACCEPT),
    ("TC-BVA-03", "party_size", 2, ACCEPT),
    ("TC-BVA-04", "party_size", 7, ACCEPT),
    ("TC-BVA-05", "party_size", 8, ACCEPT),
    ("TC-BVA-06", "party_size", 9, REJECT),
    # --- R1 name length: 2 .. 50 ---
    ("TC-BVA-07", "customer_name", "A", REJECT),
    ("TC-BVA-08", "customer_name", "Al", ACCEPT),
    ("TC-BVA-09", "customer_name", "Ali", ACCEPT),
    ("TC-BVA-10", "customer_name", "A" * 49, ACCEPT),
    ("TC-BVA-11", "customer_name", "A" * 50, ACCEPT),
    ("TC-BVA-12", "customer_name", "A" * 51, REJECT),
    ("TC-BVA-13", "customer_name", " A ", REJECT),          # trims to 1 char
    # --- R2 phone length: exactly 10 ---
    ("TC-BVA-14", "phone", "987654321", REJECT),             # 9 digits
    ("TC-BVA-15", "phone", "9876543210", ACCEPT),            # 10 digits
    ("TC-BVA-16", "phone", "98765432101", REJECT),           # 11 digits
    # --- R5 date window: today .. today + 30 ---
    ("TC-BVA-17", "date", "2026-11-15", REJECT),             # yesterday
    ("TC-BVA-18", "date", "2026-11-16", ACCEPT),             # today
    ("TC-BVA-19", "date", "2026-11-17", ACCEPT),             # today + 1
    ("TC-BVA-20", "date", "2026-12-15", ACCEPT),             # today + 29
    ("TC-BVA-21", "date", "2026-12-16", ACCEPT),             # today + 30
    ("TC-BVA-22", "date", "2026-12-17", REJECT),             # today + 31
    # --- R6 time window: 11:00 .. 21:30 ---
    ("TC-BVA-23", "time", "10:30", REJECT),
    ("TC-BVA-24", "time", "11:00", ACCEPT),
    ("TC-BVA-25", "time", "11:30", ACCEPT),
    ("TC-BVA-26", "time", "21:00", ACCEPT),
    ("TC-BVA-27", "time", "21:30", ACCEPT),
    ("TC-BVA-28", "time", "22:00", REJECT),
]


@pytest.mark.parametrize("tc_id, field, value, expected", BVA_CASES, ids=[c[0] for c in BVA_CASES])
def test_input_boundaries(service, record, tc_id, field, value, expected):
    actual = attempt(service, booking(**{field: value}))
    record(expected, actual)
    assert actual.startswith(expected), f"{tc_id}: {field}={value!r} -> {actual}"


# --- R7 overlap boundaries ---------------------------------------------------
# Party of 7 fits only table T8. An existing T8 booking runs 19:00-20:30.
# A new booking lasts 90 minutes, so it is free only if it ends by 19:00
# or starts at/after 20:30.
OVERLAP_CASES = [
    ("TC-BVA-29", "17:30", ACCEPT),   # ends exactly 19:00
    ("TC-BVA-30", "18:00", REJECT),   # ends 19:30 -> overlaps 30 min
    ("TC-BVA-31", "18:30", REJECT),   # ends 20:00 -> overlaps 60 min
    ("TC-BVA-32", "19:00", REJECT),   # same start
    ("TC-BVA-33", "20:00", REJECT),   # starts before 20:30
    ("TC-BVA-34", "20:30", ACCEPT),   # starts exactly when existing ends
]


@pytest.mark.parametrize("tc_id, new_time, expected", OVERLAP_CASES, ids=[c[0] for c in OVERLAP_CASES])
def test_overlap_boundaries(service, record, tc_id, new_time, expected):
    service.create(booking(customer_name="Existing Guest", phone="9000000001",
                           party_size=7, time="19:00"))
    actual = attempt(service, booking(phone="9000000002", party_size=7, time=new_time))
    record(expected, actual)
    assert actual.startswith(expected), f"{tc_id}: new booking at {new_time} -> {actual}"


# --- R10 refund boundary: 2 hours before the slot ----------------------------
REFUND_CASES = [
    ("TC-BVA-35", datetime(2026, 11, 16, 11, 59), 600),   # 2h 01m notice -> refund
    ("TC-BVA-36", datetime(2026, 11, 16, 12, 0), 600),    # exactly 2h    -> refund
    ("TC-BVA-37", datetime(2026, 11, 16, 12, 1), 0),      # 1h 59m        -> no refund
]


@pytest.mark.parametrize("tc_id, cancel_at, expected_refund", REFUND_CASES,
                         ids=[c[0] for c in REFUND_CASES])
def test_refund_boundaries(service, clock, record, tc_id, cancel_at, expected_refund):
    r = service.create(booking(date="2026-11-16", time="14:00", party_size=6))  # deposit 600
    clock.now = cancel_at
    cancelled = service.cancel(r.reservation_id)
    record(f"Refund Rs.{expected_refund}", f"Refund Rs.{cancelled.refund}")
    assert cancelled.refund == expected_refund
