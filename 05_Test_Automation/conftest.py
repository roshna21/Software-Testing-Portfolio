"""Shared pytest fixtures for the Restaurant Table Reservation System test suite."""
import sys
from datetime import datetime
from pathlib import Path

import pytest

APP_DIR = Path(__file__).resolve().parents[1] / "application"
sys.path.insert(0, str(APP_DIR))

from reservation_system import create_app  # noqa: E402
from reservation_system.service import BookingError, ReservationService  # noqa: E402
from reservation_system.validators import ValidationError  # noqa: E402

# All date rules are tested against this frozen "now": Monday 16 Nov 2026, 10:00.
FIXED_NOW = datetime(2026, 11, 16, 10, 0)
TODAY = "2026-11-16"


class Clock:
    """A clock the tests can move forward or back."""

    def __init__(self, now: datetime = FIXED_NOW):
        self.now = now

    def __call__(self) -> datetime:
        return self.now


def booking(**overrides) -> dict:
    """A valid booking request; tests override one field at a time."""
    data = {
        "customer_name": "Priya Sharma",
        "phone": "9876543210",
        "email": "",
        "party_size": 2,
        "date": "2026-11-18",   # Wednesday
        "time": "13:00",
    }
    data.update(overrides)
    return data


def attempt(service: ReservationService, data: dict) -> str:
    """Try a booking and describe the outcome in plain words (used as 'actual result')."""
    try:
        r = service.create(data)
        return f"Accepted ({r.reservation_id}, table {r.table_id}, deposit Rs.{r.deposit})"
    except ValidationError as err:
        return f"Rejected: {err.message}"
    except BookingError as err:
        return f"Rejected: {err.message}"


@pytest.fixture
def clock():
    return Clock()


@pytest.fixture
def service(clock):
    return ReservationService(clock=clock)


@pytest.fixture
def app():
    return create_app({"TESTING": True, "FIXED_NOW": FIXED_NOW, "ENABLE_RESET": True})


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def record(record_property):
    """Store expected/actual results in the JUnit XML so the execution log can be generated."""
    def _record(expected: str, actual: str):
        record_property("expected", expected)
        record_property("actual", actual)
    return _record
