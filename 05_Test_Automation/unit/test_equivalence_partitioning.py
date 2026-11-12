"""TC-EP-01 .. TC-EP-29: Equivalence Partitioning tests (R1-R6, R11).

One representative value is picked from each valid and invalid class.
"""
from datetime import datetime

import pytest

from conftest import attempt, booking

ACCEPT, REJECT = "Accepted", "Rejected"

EP_CASES = [
    # id,        field,           value,              expected
    ("TC-EP-01", "customer_name", "Priya Sharma",     ACCEPT),   # valid: letters + space
    ("TC-EP-02", "customer_name", "",                 REJECT),   # invalid: empty
    ("TC-EP-03", "customer_name", "Priya123",         REJECT),   # invalid: digits
    ("TC-EP-04", "customer_name", "Priya@#",          REJECT),   # invalid: special chars
    ("TC-EP-05", "customer_name", "    ",             REJECT),   # invalid: only spaces
    ("TC-EP-06", "phone",         "9876543210",       ACCEPT),   # valid mobile
    ("TC-EP-07", "phone",         "5876543210",       REJECT),   # invalid: starts with 5
    ("TC-EP-08", "phone",         "98765abcde",       REJECT),   # invalid: letters
    ("TC-EP-09", "phone",         "98765",            REJECT),   # invalid: too short
    ("TC-EP-10", "phone",         "987654321012",     REJECT),   # invalid: too long
    ("TC-EP-11", "email",         "",                 ACCEPT),   # valid: optional, blank
    ("TC-EP-12", "email",         "priya@example.com", ACCEPT),  # valid format
    ("TC-EP-13", "email",         "priya.example.com", REJECT),  # invalid: no @
    ("TC-EP-14", "party_size",    4,                  ACCEPT),   # valid 1-8
    ("TC-EP-15", "party_size",    -3,                 REJECT),   # invalid: negative
    ("TC-EP-16", "party_size",    15,                 REJECT),   # invalid: above 8
    ("TC-EP-17", "party_size",    "four",             REJECT),   # invalid: not a number
    ("TC-EP-18", "party_size",    "2.5",              REJECT),   # invalid: decimal
    ("TC-EP-19", "date",          "2026-11-25",       ACCEPT),   # valid: inside window
    ("TC-EP-20", "date",          "2026-11-01",       REJECT),   # invalid: past
    ("TC-EP-21", "date",          "2027-03-01",       REJECT),   # invalid: too far ahead
    ("TC-EP-22", "date",          "25/11/2026",       REJECT),   # invalid: wrong format
    ("TC-EP-23", "time",          "13:00",            ACCEPT),   # valid slot
    ("TC-EP-24", "time",          "09:00",            REJECT),   # invalid: before opening
    ("TC-EP-25", "time",          "22:30",            REJECT),   # invalid: after last slot
    ("TC-EP-26", "time",          "13:15",            REJECT),   # invalid: not :00 / :30
]


@pytest.mark.parametrize("tc_id, field, value, expected", EP_CASES, ids=[c[0] for c in EP_CASES])
def test_equivalence_classes(service, record, tc_id, field, value, expected):
    actual = attempt(service, booking(**{field: value}))
    record(expected, actual)
    assert actual.startswith(expected), f"{tc_id}: {field}={value!r} -> {actual}"


def test_TC_EP_27_time_already_passed_today(service, clock, record):
    """Same-day booking for a slot that has already passed is rejected."""
    clock.now = datetime(2026, 11, 16, 15, 0)
    actual = attempt(service, booking(date="2026-11-16", time="13:00"))
    record(REJECT, actual)
    assert actual.startswith(REJECT)


def test_TC_EP_28_same_phone_same_day_rejected(service, record):
    """R11: second active booking for the same phone on the same day is refused."""
    service.create(booking(time="13:00"))
    actual = attempt(service, booking(time="19:00"))
    record(REJECT, actual)
    assert actual.startswith(REJECT) and "already has reservation" in actual


def test_TC_EP_29_same_phone_different_day_allowed(service, record):
    """R11: the same phone may book on a different day."""
    service.create(booking(date="2026-11-18"))
    actual = attempt(service, booking(date="2026-11-19"))
    record(ACCEPT, actual)
    assert actual.startswith(ACCEPT)
