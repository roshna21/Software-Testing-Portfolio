"""Business logic: booking, table allocation, deposits, status changes (R7 - R11)."""
from datetime import date, datetime, time, timedelta
from itertools import count
from typing import Callable, Dict, List, Optional

from .models import DEFAULT_TABLES, RESERVATION_DURATION, Reservation, Status, Table
from . import validators as v

LARGE_PARTY = 6                 # R8: parties of 6+ pay a per-guest deposit
LARGE_PARTY_DEPOSIT_PER_GUEST = 100
PEAK_START, PEAK_END = time(19, 0), time(21, 30)
WEEKEND_PEAK_DEPOSIT = 300      # R8: flat deposit for weekend peak slots
SATURDAY = 5                    # date.weekday(): Monday = 0 ... Sunday = 6
FREE_CANCELLATION_WINDOW = timedelta(hours=2)   # R10

# R9: which status changes are allowed.
ALLOWED_TRANSITIONS = {
    Status.CONFIRMED: {Status.SEATED, Status.CANCELLED, Status.NO_SHOW},
    Status.SEATED: {Status.COMPLETED},
    Status.COMPLETED: set(),
    Status.CANCELLED: set(),
    Status.NO_SHOW: set(),
}


class BookingError(Exception):
    """Raised when a valid request still cannot be fulfilled."""

    def __init__(self, message: str, code: str = "booking_error"):
        super().__init__(message)
        self.message = message
        self.code = code


class NotFoundError(BookingError):
    def __init__(self, reservation_id: str):
        super().__init__(f"Reservation {reservation_id} not found", "not_found")


def calculate_deposit(party_size: int, booking_date: date, slot: time) -> int:
    """R8 decision table.

    * Large party (6 or more guests)   -> Rs.100 per guest
    * Weekend (Sat/Sun) AND peak time   -> Rs.300 flat
    * Both conditions                   -> both amounts added
    * Otherwise                         -> no deposit
    """
    deposit = 0
    if party_size >= LARGE_PARTY:
        deposit += party_size * LARGE_PARTY_DEPOSIT_PER_GUEST
    is_weekend = booking_date.weekday() >= SATURDAY
    is_peak = PEAK_START <= slot <= PEAK_END
    if is_weekend and is_peak:
        deposit += WEEKEND_PEAK_DEPOSIT
    return deposit


def overlaps(existing: Reservation, start: datetime, end: datetime) -> bool:
    """True when the new time window clashes with an existing reservation.

    Two intervals overlap when each one starts before the other ends.
    """
    return start < existing.end and existing.start < end


class ReservationService:
    def __init__(self, tables: Optional[List[Table]] = None,
                 clock: Callable[[], datetime] = datetime.now):
        self.tables = sorted(tables or DEFAULT_TABLES, key=lambda t: (t.capacity, t.table_id))
        self.clock = clock
        self._reservations: Dict[str, Reservation] = {}
        self._ids = count(1001)

    # ---------- queries ----------
    def get(self, reservation_id: str) -> Reservation:
        reservation = self._reservations.get(str(reservation_id).upper())
        if reservation is None:
            raise NotFoundError(reservation_id)
        return reservation

    def list(self, on_date: Optional[date] = None) -> List[Reservation]:
        items = self._reservations.values()
        if on_date:
            items = [r for r in items if r.start.date() == on_date]
        return sorted(items, key=lambda r: (r.start, r.table_id))

    def find_free_table(self, party_size: int, start: datetime) -> Optional[Table]:
        """R7: smallest free table that fits the party."""
        end = start + RESERVATION_DURATION
        for table in self.tables:
            if table.capacity < party_size:
                continue
            busy = any(r.table_id == table.table_id and r.is_active and overlaps(r, start, end)
                       for r in self._reservations.values())
            if not busy:
                return table
        return None

    def availability(self, booking_date: date, slot: time) -> List[dict]:
        start = datetime.combine(booking_date, slot)
        end = start + RESERVATION_DURATION
        result = []
        for table in self.tables:
            busy = any(r.table_id == table.table_id and r.is_active and overlaps(r, start, end)
                       for r in self._reservations.values())
            result.append({"table_id": table.table_id, "capacity": table.capacity, "available": not busy})
        return result

    # ---------- commands ----------
    def create(self, data: dict) -> Reservation:
        now = self.clock()
        name = v.validate_name(data.get("customer_name"))
        phone = v.validate_phone(data.get("phone"))
        email = v.validate_email(data.get("email"))
        party_size = v.validate_party_size(data.get("party_size"))
        booking_date = v.validate_date(data.get("date"), now.date())
        slot = v.validate_time(data.get("time"))
        start = datetime.combine(booking_date, slot)
        if start <= now:
            raise v.ValidationError("time", "This time has already passed")

        # R11: one active booking per phone number per day.
        for r in self._reservations.values():
            if r.phone == phone and r.is_active and r.start.date() == booking_date:
                raise BookingError(
                    f"Phone {phone} already has reservation {r.reservation_id} on this date",
                    "duplicate")

        table = self.find_free_table(party_size, start)
        if table is None:
            raise BookingError("No table available for this party size and time", "no_table")

        reservation = Reservation(
            reservation_id=f"R{next(self._ids)}",
            customer_name=name, phone=phone, email=email,
            party_size=party_size, start=start, table_id=table.table_id,
            deposit=calculate_deposit(party_size, booking_date, slot),
            created_at=now,
        )
        self._reservations[reservation.reservation_id] = reservation
        return reservation

    def change_status(self, reservation_id: str, new_status) -> Reservation:
        """R9: move a reservation through its life cycle."""
        reservation = self.get(reservation_id)
        try:
            new_status = Status(str(new_status).upper())
        except ValueError:
            raise BookingError(f"Unknown status '{new_status}'", "invalid_status")
        if new_status == Status.CANCELLED:
            return self.cancel(reservation_id)
        if new_status not in ALLOWED_TRANSITIONS[reservation.status]:
            raise BookingError(
                f"Cannot change status from {reservation.status.value} to {new_status.value}",
                "invalid_transition")
        reservation.status = new_status
        return reservation

    def cancel(self, reservation_id: str) -> Reservation:
        """R10: cancel; refund the deposit only if 2+ hours before the slot."""
        reservation = self.get(reservation_id)
        if Status.CANCELLED not in ALLOWED_TRANSITIONS[reservation.status]:
            raise BookingError(
                f"Cannot change status from {reservation.status.value} to CANCELLED",
                "invalid_transition")
        notice = reservation.start - self.clock()
        reservation.refund = reservation.deposit if notice >= FREE_CANCELLATION_WINDOW else 0
        reservation.status = Status.CANCELLED
        return reservation
