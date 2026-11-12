"""Restaurant Table Reservation System - Flask application factory."""
import os
from datetime import datetime

from flask import Flask

from .service import ReservationService

__version__ = "1.0.0"


def create_app(config: dict = None) -> Flask:
    app = Flask(__name__)
    app.config.update(SECRET_KEY="dev-only-secret", ENABLE_RESET=False, FIXED_NOW=None)
    if os.environ.get("RESERVATION_FIXED_NOW"):
        app.config["FIXED_NOW"] = os.environ["RESERVATION_FIXED_NOW"]
    if os.environ.get("RESERVATION_ENABLE_RESET") == "1":
        app.config["ENABLE_RESET"] = True
    if config:
        app.config.update(config)

    fixed_now = app.config.get("FIXED_NOW")
    if fixed_now:
        frozen = datetime.fromisoformat(fixed_now) if isinstance(fixed_now, str) else fixed_now
        clock = lambda: frozen  # noqa: E731 - deterministic clock for testing
    else:
        clock = datetime.now

    app.extensions["reservations"] = ReservationService(clock=clock)
    app.config["VERSION"] = __version__

    from .api import api
    from .web import web
    app.register_blueprint(api)
    app.register_blueprint(web)
    return app


def get_service() -> ReservationService:
    from flask import current_app
    return current_app.extensions["reservations"]
