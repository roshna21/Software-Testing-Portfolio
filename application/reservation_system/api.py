"""REST API (JSON). Used by the Postman collection and the API test suite."""
from flask import Blueprint, current_app, jsonify, request

from . import get_service
from .service import BookingError, NotFoundError, ReservationService
from .validators import ValidationError, validate_date, validate_time

api = Blueprint("api", __name__, url_prefix="/api")


@api.errorhandler(ValidationError)
def _validation_error(err):
    return jsonify(error=err.message, field=err.field), 400


@api.errorhandler(NotFoundError)
def _not_found(err):
    return jsonify(error=err.message, code=err.code), 404


@api.errorhandler(BookingError)
def _booking_error(err):
    return jsonify(error=err.message, code=err.code), 409


@api.get("/health")
def health():
    return jsonify(status="ok", version=current_app.config["VERSION"])


@api.get("/tables")
def tables():
    return jsonify([{"table_id": t.table_id, "capacity": t.capacity} for t in get_service().tables])


@api.get("/availability")
def availability():
    service = get_service()
    booking_date = validate_date(request.args.get("date", ""), service.clock().date())
    slot = validate_time(request.args.get("time", ""))
    return jsonify(get_service().availability(booking_date, slot))


@api.post("/reservations")
def create_reservation():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Request body must be a JSON object"), 400
    reservation = get_service().create(data)
    return jsonify(reservation.to_dict()), 201


@api.get("/reservations")
def list_reservations():
    service = get_service()
    on_date = None
    if request.args.get("date"):
        from datetime import datetime
        try:
            on_date = datetime.strptime(request.args["date"], "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError("date", "Date must be in YYYY-MM-DD format")
    return jsonify([r.to_dict() for r in service.list(on_date)])


@api.get("/reservations/<reservation_id>")
def get_reservation(reservation_id):
    return jsonify(get_service().get(reservation_id).to_dict())


@api.patch("/reservations/<reservation_id>/status")
def update_status(reservation_id):
    data = request.get_json(silent=True) or {}
    reservation = get_service().change_status(reservation_id, data.get("status", ""))
    return jsonify(reservation.to_dict())


@api.delete("/reservations/<reservation_id>")
def cancel_reservation(reservation_id):
    return jsonify(get_service().cancel(reservation_id).to_dict())


@api.post("/_reset")
def reset():
    """Test helper: wipe all data. Only enabled in test runs."""
    if not current_app.config.get("ENABLE_RESET"):
        return jsonify(error="Not found"), 404
    old = get_service()
    current_app.extensions["reservations"] = ReservationService(clock=old.clock)
    return jsonify(status="reset")
