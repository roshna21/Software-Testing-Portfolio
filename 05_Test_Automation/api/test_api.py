"""TC-API-01 .. TC-API-13: REST API integration tests (R12)."""
from conftest import booking


def _create(client, **overrides):
    return client.post("/api/reservations", json=booking(**overrides))


def test_TC_API_01_health(client, record):
    res = client.get("/api/health")
    record("200, status ok", f"{res.status_code}, status {res.json['status']}")
    assert res.status_code == 200 and res.json["status"] == "ok"


def test_TC_API_02_list_tables(client, record):
    res = client.get("/api/tables")
    seats = sum(t["capacity"] for t in res.json)
    record("200, 8 tables, 36 seats", f"{res.status_code}, {len(res.json)} tables, {seats} seats")
    assert res.status_code == 200 and len(res.json) == 8 and seats == 36


def test_TC_API_03_create_reservation(client, record):
    res = _create(client)
    body = res.json
    record("201, CONFIRMED, id assigned", f"{res.status_code}, {body.get('status')}, id {body.get('reservation_id')}")
    assert res.status_code == 201 and body["status"] == "CONFIRMED" and body["reservation_id"].startswith("R")


def test_TC_API_04_invalid_input_returns_400_with_field(client, record):
    res = _create(client, phone="12345")
    record("400, field=phone", f"{res.status_code}, field={res.json.get('field')}")
    assert res.status_code == 400 and res.json["field"] == "phone"


def test_TC_API_05_body_not_json(client, record):
    res = client.post("/api/reservations", data="name=Priya", content_type="text/plain")
    record("400", str(res.status_code))
    assert res.status_code == 400


def test_TC_API_06_get_reservation(client, record):
    rid = _create(client).json["reservation_id"]
    res = client.get(f"/api/reservations/{rid}")
    record(f"200, id {rid}", f"{res.status_code}, id {res.json.get('reservation_id')}")
    assert res.status_code == 200 and res.json["reservation_id"] == rid


def test_TC_API_07_unknown_reservation_404(client, record):
    res = client.get("/api/reservations/R9999")
    record("404", str(res.status_code))
    assert res.status_code == 404


def test_TC_API_08_list_filtered_by_date(client, record):
    _create(client, date="2026-11-18")
    _create(client, date="2026-11-19", phone="9123456780")
    res = client.get("/api/reservations?date=2026-11-19")
    dates = {r["date"] for r in res.json}
    record("200, only 2026-11-19 bookings", f"{res.status_code}, dates {sorted(dates)}")
    assert res.status_code == 200 and dates == {"2026-11-19"}


def test_TC_API_09_patch_status_valid(client, record):
    rid = _create(client).json["reservation_id"]
    res = client.patch(f"/api/reservations/{rid}/status", json={"status": "SEATED"})
    record("200, SEATED", f"{res.status_code}, {res.json.get('status')}")
    assert res.status_code == 200 and res.json["status"] == "SEATED"


def test_TC_API_10_patch_status_invalid_transition(client, record):
    rid = _create(client).json["reservation_id"]
    res = client.patch(f"/api/reservations/{rid}/status", json={"status": "COMPLETED"})
    record("409, invalid_transition", f"{res.status_code}, {res.json.get('code')}")
    assert res.status_code == 409 and res.json["code"] == "invalid_transition"


def test_TC_API_11_delete_cancels(client, record):
    rid = _create(client).json["reservation_id"]
    res = client.delete(f"/api/reservations/{rid}")
    record("200, CANCELLED", f"{res.status_code}, {res.json.get('status')}")
    assert res.status_code == 200 and res.json["status"] == "CANCELLED"


def test_TC_API_12_availability_marks_booked_table(client, record):
    _create(client, time="19:00")                 # party of 2 -> T1
    res = client.get("/api/availability?date=2026-11-18&time=19:30")
    free = {t["table_id"]: t["available"] for t in res.json}
    others_free = all(v for k, v in free.items() if k != "T1")
    record("200, T1 unavailable, other 7 tables available",
           f"{res.status_code}, T1 available={free['T1']}, others all available={others_free}")
    # Checking the *other* tables too was added after mutation testing.
    assert res.status_code == 200 and free["T1"] is False and others_free


def test_TC_API_13_duplicate_returns_409(client, record):
    _create(client, time="13:00")
    res = _create(client, time="20:00")
    record("409, duplicate", f"{res.status_code}, {res.json.get('code')}")
    assert res.status_code == 409 and res.json["code"] == "duplicate"
