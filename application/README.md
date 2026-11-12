# Application Under Test – Restaurant Table Reservation System

A small web application for **"The Saffron Table"** restaurant. Customers book a table online; staff see the day's bookings and update their status.

## Run it

```bash
cd application
pip install -r requirements.txt
python run.py
# open http://127.0.0.1:5000
```

## Modules

| Module | File | What it does |
|---|---|---|
| Input validation | `reservation_system/validators.py` | Checks name, phone, email, party size, date, time |
| Booking engine | `reservation_system/service.py` | Picks a table, prevents double booking, calculates deposit, cancels, changes status |
| REST API | `reservation_system/api.py` | JSON endpoints under `/api` |
| Web UI | `reservation_system/web.py` + `templates/` | Booking form, confirmation page, staff view |

## REST API

| Method | Endpoint | Purpose | Success code |
|---|---|---|---|
| GET | `/api/health` | Health check | 200 |
| GET | `/api/tables` | List tables | 200 |
| GET | `/api/availability?date=&time=` | Free / busy tables for a slot | 200 |
| POST | `/api/reservations` | Create a booking | 201 |
| GET | `/api/reservations?date=` | List bookings | 200 |
| GET | `/api/reservations/{id}` | One booking | 200 (404 if missing) |
| PATCH | `/api/reservations/{id}/status` | Change status (`SEATED`, `COMPLETED`, `NO_SHOW`, `CANCELLED`) | 200 |
| DELETE | `/api/reservations/{id}` | Cancel a booking | 200 |

Errors: `400` for invalid input (with the failing `field`), `404` for unknown IDs, `409` for business-rule conflicts (no table, duplicate, invalid status change).

## Test mode

Two environment variables make the app predictable during automated tests:

* `RESERVATION_FIXED_NOW=2026-11-16T10:00` – freezes "now" so date rules give the same answer every run.
* `RESERVATION_ENABLE_RESET=1` – enables `POST /api/_reset` to clear data between tests.
