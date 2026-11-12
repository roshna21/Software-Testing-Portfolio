"""TC-DT-01 .. TC-DT-17: Decision Table tests.

Table 1 (R8) - deposit:     C1 party >= 6, C2 weekend (Sat/Sun), C3 peak 19:00-21:30
Table 2 (R10) - cancellation: status, notice >= 2h, deposit > 0
"""
from datetime import date, datetime, time

import pytest

from conftest import booking
from reservation_system.service import BookingError, calculate_deposit

WED, FRI, SAT, SUN = date(2026, 11, 18), date(2026, 11, 20), date(2026, 11, 21), date(2026, 11, 22)

DEPOSIT_RULES = [
    # id,        party, day, slot,         C1  C2  C3   expected deposit
    ("TC-DT-01", 6, SAT, time(19, 0)),   # Y   Y   Y -> 600 + 300
    ("TC-DT-02", 6, SAT, time(13, 0)),   # Y   Y   N -> 600
    ("TC-DT-03", 6, WED, time(19, 0)),   # Y   N   Y -> 600
    ("TC-DT-04", 6, WED, time(13, 0)),   # Y   N   N -> 600
    ("TC-DT-05", 2, SAT, time(20, 0)),   # N   Y   Y -> 300
    ("TC-DT-06", 2, SAT, time(13, 0)),   # N   Y   N -> 0
    ("TC-DT-07", 2, WED, time(19, 30)),  # N   N   Y -> 0
    ("TC-DT-08", 2, WED, time(13, 0)),   # N   N   N -> 0
    # extra checks on the condition edges
    ("TC-DT-09", 2, FRI, time(19, 0)),   # Friday is NOT weekend -> 0
    ("TC-DT-10", 2, SUN, time(21, 30)),  # Sunday, last peak slot -> 300
    ("TC-DT-11", 2, SAT, time(18, 30)),  # Saturday, just before peak -> 0
]
EXPECTED_DEPOSIT = {
    "TC-DT-01": 900, "TC-DT-02": 600, "TC-DT-03": 600, "TC-DT-04": 600,
    "TC-DT-05": 300, "TC-DT-06": 0, "TC-DT-07": 0, "TC-DT-08": 0,
    "TC-DT-09": 0, "TC-DT-10": 300, "TC-DT-11": 0,
}


@pytest.mark.parametrize("tc_id, party, day, slot", DEPOSIT_RULES, ids=[r[0] for r in DEPOSIT_RULES])
def test_deposit_decision_table(record, tc_id, party, day, slot):
    expected = EXPECTED_DEPOSIT[tc_id]
    actual = calculate_deposit(party, day, slot)
    record(f"Deposit Rs.{expected}", f"Deposit Rs.{actual}")
    assert actual == expected, f"{tc_id}: party={party}, {day:%A}, {slot} -> {actual}"


# ---------------- Table 2: cancellation & refund (R10) ----------------
SLOT = dict(date="2026-11-16", time="15:00")      # today 15:00
EARLY, LATE = datetime(2026, 11, 16, 12, 0), datetime(2026, 11, 16, 14, 0)  # 3h vs 1h notice

CANCEL_RULES = [
    # id,        party, cancel at, expected refund
    ("TC-DT-12", 6, EARLY, 600),   # CONFIRMED, notice >= 2h, deposit > 0 -> full refund
    ("TC-DT-13", 6, LATE, 0),      # CONFIRMED, notice < 2h,  deposit > 0 -> forfeited
    ("TC-DT-14", 2, EARLY, 0),     # CONFIRMED, notice >= 2h, no deposit  -> nothing to refund
    ("TC-DT-15", 2, LATE, 0),      # CONFIRMED, notice < 2h,  no deposit  -> nothing to refund
]


@pytest.mark.parametrize("tc_id, party, cancel_at, refund", CANCEL_RULES, ids=[r[0] for r in CANCEL_RULES])
def test_cancellation_decision_table(service, clock, record, tc_id, party, cancel_at, refund):
    r = service.create(booking(party_size=party, **SLOT))
    clock.now = cancel_at
    result = service.cancel(r.reservation_id)
    record(f"CANCELLED, refund Rs.{refund}", f"{result.status.value}, refund Rs.{result.refund}")
    assert result.status.value == "CANCELLED" and result.refund == refund


@pytest.mark.parametrize("tc_id, steps", [
    ("TC-DT-16", ["SEATED"]),        # not CONFIRMED (seated)    -> cancellation refused
    ("TC-DT-17", ["CANCELLED"]),     # not CONFIRMED (cancelled) -> cancellation refused
], ids=["TC-DT-16", "TC-DT-17"])
def test_cancellation_refused_when_not_confirmed(service, record, tc_id, steps):
    r = service.create(booking(**SLOT))
    for step in steps:
        service.change_status(r.reservation_id, step)
    try:
        service.cancel(r.reservation_id)
        actual = f"Cancelled (status {r.status.value})"
    except BookingError as err:
        actual = f"Refused: {err.message}"
    record("Refused", actual)
    assert actual.startswith("Refused")
