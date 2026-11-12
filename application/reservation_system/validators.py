"""Input validation rules (requirements R1 - R6)."""
import re
from datetime import date, datetime, time, timedelta

MIN_PARTY, MAX_PARTY = 1, 8
MAX_DAYS_AHEAD = 30
OPENING_SLOT = time(11, 0)
LAST_SLOT = time(21, 30)

NAME_PATTERN = re.compile(r"^[A-Za-z ]+$")
EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class ValidationError(Exception):
    """Raised when user input breaks a business rule."""

    def __init__(self, field_name: str, message: str):
        super().__init__(message)
        self.field = field_name
        self.message = message


def validate_name(name) -> str:
    """R1: 2-50 characters, letters and spaces only."""
    if name is None:
        raise ValidationError("customer_name", "Name is required")
    name = str(name)
    if not 2 <= len(name) <= 50:
        raise ValidationError("customer_name", "Name must be 2 to 50 characters")
    if not NAME_PATTERN.match(name):
        raise ValidationError("customer_name", "Name may contain only letters and spaces")
    return name


def validate_phone(phone) -> str:
    """R2: Indian mobile number - exactly 10 digits starting with 6, 7, 8 or 9."""
    phone = str(phone or "").strip()
    if not re.fullmatch(r"[6-9]\d{9}", phone):
        raise ValidationError("phone", "Phone must be a 10-digit mobile number starting with 6-9")
    return phone


def validate_email(email) -> str:
    """R3: optional, but must look like an email address when given."""
    email = str(email or "").strip()
    if email and not EMAIL_PATTERN.match(email):
        raise ValidationError("email", "Email address is not valid")
    return email


def validate_party_size(party_size) -> int:
    """R4: whole number from 1 to 8."""
    try:
        size = int(str(party_size).strip())
    except (TypeError, ValueError):
        raise ValidationError("party_size", "Party size must be a whole number")
    if not MIN_PARTY <= size <= MAX_PARTY:
        raise ValidationError("party_size", f"Party size must be between {MIN_PARTY} and {MAX_PARTY}")
    return size


def validate_date(value, today: date) -> date:
    """R5: from today up to 30 days ahead."""
    try:
        booking_date = datetime.strptime(str(value).strip(), "%Y-%m-%d").date()
    except ValueError:
        raise ValidationError("date", "Date must be in YYYY-MM-DD format")
    if booking_date < today:
        raise ValidationError("date", "Date cannot be in the past")
    if booking_date > today + timedelta(days=MAX_DAYS_AHEAD + 1):
        raise ValidationError("date", f"Bookings open only {MAX_DAYS_AHEAD} days in advance")
    return booking_date


def validate_time(value) -> time:
    """R6: 11:00 to 21:30, on the hour or half hour."""
    try:
        slot = datetime.strptime(str(value).strip(), "%H:%M").time()
    except ValueError:
        raise ValidationError("time", "Time must be in HH:MM format")
    if slot.minute not in (0, 30):
        raise ValidationError("time", "Time must be on the hour or half hour")
    if not OPENING_SLOT <= slot <= LAST_SLOT:
        raise ValidationError("time", "Bookings are accepted from 11:00 to 21:30")
    return slot
