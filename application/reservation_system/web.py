"""Server-rendered web pages for customers and restaurant staff."""
from datetime import datetime, timedelta

from flask import Blueprint, flash, redirect, render_template, request, url_for

from . import get_service
from .service import BookingError
from .validators import ValidationError

web = Blueprint("web", __name__)

TIME_SLOTS = [f"{h:02d}:{m:02d}" for h in range(11, 22) for m in (0, 30)]


def _form_defaults():
    tomorrow = (get_service().clock() + timedelta(days=1)).strftime("%Y-%m-%d")
    return {"date": tomorrow, "time": "19:00", "party_size": "2"}


@web.get("/")
def index():
    return render_template("index.html", form=_form_defaults(), slots=TIME_SLOTS, error=None)


@web.post("/book")
def book():
    try:
        reservation = get_service().create(request.form.to_dict())
    except (ValidationError, BookingError) as err:
        # Show the error and send the user back to the form.
        return render_template("index.html", form=_form_defaults(), slots=TIME_SLOTS,
                               error=err.message), 400
    return redirect(url_for("web.reservation", reservation_id=reservation.reservation_id, new=1))


@web.get("/reservation/<reservation_id>")
def reservation(reservation_id):
    try:
        item = get_service().get(reservation_id)
    except BookingError as err:
        return render_template("message.html", title="Not found", message=err.message), 404
    return render_template("reservation.html", r=item, new=request.args.get("new"))


@web.post("/reservation/<reservation_id>/cancel")
def cancel(reservation_id):
    try:
        get_service().cancel(reservation_id)
        flash("Reservation cancelled", "success")
    except BookingError as err:
        flash(err.message, "error")
    return redirect(request.form.get("next") or url_for("web.reservation", reservation_id=reservation_id))


@web.post("/reservation/<reservation_id>/status")
def change_status(reservation_id):
    try:
        get_service().change_status(reservation_id, request.form.get("status", ""))
        flash(f"{reservation_id} updated", "success")
    except BookingError as err:
        flash(err.message, "error")
    return redirect(request.form.get("next") or url_for("web.reservations"))


@web.get("/reservations")
def reservations():
    service = get_service()
    day = request.args.get("date") or service.clock().strftime("%Y-%m-%d")
    try:
        on_date = datetime.strptime(day, "%Y-%m-%d").date()
    except ValueError:
        on_date = service.clock().date()
        day = on_date.isoformat()
    return render_template("reservations.html", items=service.list(on_date), day=day,
                           tables=service.tables)
