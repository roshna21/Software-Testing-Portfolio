"""Data models for the Restaurant Table Reservation System."""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum

# How long one reservation keeps a table busy.
RESERVATION_DURATION = timedelta(minutes=90)


class Status(str, Enum):
    CONFIRMED = "CONFIRMED"
    SEATED = "SEATED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"


@dataclass(frozen=True)
class Table:
    table_id: str
    capacity: int


# The restaurant floor: 8 tables, 36 seats in total.
DEFAULT_TABLES = [
    Table("T1", 2), Table("T2", 2),
    Table("T3", 4), Table("T4", 4), Table("T5", 4),
    Table("T6", 6), Table("T7", 6),
    Table("T8", 8),
]


@dataclass
class Reservation:
    reservation_id: str
    customer_name: str
    phone: str
    email: str
    party_size: int
    start: datetime
    table_id: str
    deposit: int
    status: Status = Status.CONFIRMED
    refund: int = 0
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def end(self) -> datetime:
        return self.start + RESERVATION_DURATION

    @property
    def is_active(self) -> bool:
        """Active reservations block their table."""
        return self.status in (Status.CONFIRMED, Status.SEATED)

    def to_dict(self) -> dict:
        data = asdict(self)
        data["status"] = self.status.value
        data["date"] = self.start.strftime("%Y-%m-%d")
        data["time"] = self.start.strftime("%H:%M")
        data["end_time"] = self.end.strftime("%H:%M")
        data["start"] = self.start.isoformat(timespec="minutes")
        data["created_at"] = self.created_at.isoformat(timespec="seconds")
        return data
