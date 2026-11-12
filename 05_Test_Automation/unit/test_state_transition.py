"""TC-ST-01 .. TC-ST-16: State Transition tests for the reservation life cycle (R9).

Valid:   CONFIRMED -> SEATED -> COMPLETED
         CONFIRMED -> CANCELLED
         CONFIRMED -> NO_SHOW
Everything else must be refused and leave the status unchanged.
"""
import pytest

from conftest import attempt, booking
from reservation_system.service import BookingError

# How to drive a fresh reservation into each starting state.
PATH_TO = {
    "CONFIRMED": [],
    "SEATED": ["SEATED"],
    "COMPLETED": ["SEATED", "COMPLETED"],
    "CANCELLED": ["CANCELLED"],
    "NO_SHOW": ["NO_SHOW"],
}

VALID = [
    ("TC-ST-01", "CONFIRMED", "SEATED"),
    ("TC-ST-02", "SEATED", "COMPLETED"),
    ("TC-ST-03", "CONFIRMED", "CANCELLED"),
    ("TC-ST-04", "CONFIRMED", "NO_SHOW"),
]
INVALID = [
    ("TC-ST-05", "CONFIRMED", "COMPLETED"),
    ("TC-ST-06", "SEATED", "CANCELLED"),
    ("TC-ST-07", "SEATED", "NO_SHOW"),
    ("TC-ST-08", "COMPLETED", "CANCELLED"),
    ("TC-ST-09", "COMPLETED", "SEATED"),
    ("TC-ST-10", "CANCELLED", "SEATED"),
    ("TC-ST-11", "CANCELLED", "CANCELLED"),
    ("TC-ST-12", "NO_SHOW", "SEATED"),
    ("TC-ST-13", "NO_SHOW", "CANCELLED"),
]


def _reservation_in(service, state):
    r = service.create(booking())
    for step in PATH_TO[state]:
        service.change_status(r.reservation_id, step)
    assert r.status.value == state
    return r


@pytest.mark.parametrize("tc_id, start, target", VALID, ids=[c[0] for c in VALID])
def test_valid_transitions(service, record, tc_id, start, target):
    r = _reservation_in(service, start)
    service.change_status(r.reservation_id, target)
    record(f"{start} -> {target}", f"{start} -> {r.status.value}")
    assert r.status.value == target


@pytest.mark.parametrize("tc_id, start, target", INVALID, ids=[c[0] for c in INVALID])
def test_invalid_transitions(service, record, tc_id, start, target):
    r = _reservation_in(service, start)
    try:
        service.change_status(r.reservation_id, target)
        actual = f"Allowed: status is now {r.status.value}"
    except BookingError as err:
        actual = f"Refused, status stays {r.status.value} ({err.message})"
    record(f"Refused, status stays {start}", actual)
    assert actual.startswith("Refused") and r.status.value == start


def test_TC_ST_14_unknown_status_refused(service, record):
    r = _reservation_in(service, "CONFIRMED")
    try:
        service.change_status(r.reservation_id, "PAID")
        actual = f"Allowed: {r.status.value}"
    except BookingError as err:
        actual = f"Refused: {err.message}"
    record("Refused: unknown status", actual)
    assert actual.startswith("Refused")


def test_TC_ST_15_full_happy_path(service, record):
    """book -> seat -> complete; the table is free again afterwards."""
    r = service.create(booking(party_size=7, time="19:00"))          # only T8 fits
    service.change_status(r.reservation_id, "SEATED")
    service.change_status(r.reservation_id, "COMPLETED")
    actual = attempt(service, booking(phone="9000000003", party_size=7, time="19:00"))
    record("COMPLETED; same table bookable again", f"{r.status.value}; next booking {actual}")
    assert r.status.value == "COMPLETED" and actual.startswith("Accepted")


def test_TC_ST_16_cancel_frees_table(service, record):
    """A cancelled booking no longer blocks its table."""
    r = service.create(booking(party_size=7, time="19:00"))
    blocked = attempt(service, booking(phone="9000000004", party_size=7, time="19:00"))
    service.cancel(r.reservation_id)
    actual = attempt(service, booking(phone="9000000004", party_size=7, time="19:00"))
    record("Rejected before cancel, accepted after", f"Before: {blocked} | After: {actual}")
    assert blocked.startswith("Rejected") and actual.startswith("Accepted")
