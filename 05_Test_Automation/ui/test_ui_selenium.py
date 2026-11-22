"""TC-UI-01 .. TC-UI-08: Selenium WebDriver tests of the web interface.

The app is started in a background thread on a free port with the clock
frozen at Monday 2026-11-16 10:00. Chrome runs headless by default;
set SHOW_BROWSER=1 to watch the browser during a live demo.
Screenshots are saved to 07_Screenshots/selenium/ as evidence.
"""
import os
import socket
import threading
import time
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from werkzeug.serving import make_server

from conftest import FIXED_NOW
from reservation_system import create_app

pytestmark = pytest.mark.ui

SHOTS = Path(__file__).resolve().parents[2] / "07_Screenshots" / "selenium"
CYCLE = os.environ.get("TEST_CYCLE", "cycle2")


def _free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture
def base_url():
    """Fresh app (empty data) for every test."""
    app = create_app({"FIXED_NOW": FIXED_NOW, "ENABLE_RESET": True})
    port = _free_port()
    server = make_server("127.0.0.1", port, app, threaded=True)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{port}"
    server.shutdown()


@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    for arg in ("--no-sandbox", "--disable-dev-shm-usage", "--window-size=1280,900"):
        options.add_argument(arg)
    if os.environ.get("SHOW_BROWSER") != "1":
        options.add_argument("--headless=new")
    if os.environ.get("CHROME_BINARY"):
        options.binary_location = os.environ["CHROME_BINARY"]
    # Selenium Manager finds a matching driver automatically; CHROMEDRIVER overrides it.
    service = Service(os.environ["CHROMEDRIVER"]) if os.environ.get("CHROMEDRIVER") else Service()
    drv = webdriver.Chrome(options=options, service=service)
    drv.implicitly_wait(2)
    yield drv
    drv.quit()


def pause():
    """Slow down so people can follow each step when SHOW_BROWSER=1."""
    if os.environ.get("SHOW_BROWSER") == "1":
        time.sleep(float(os.environ.get("DEMO_DELAY", "1.5")))


def shot(driver, name):
    pause()
    SHOTS.mkdir(parents=True, exist_ok=True)
    driver.save_screenshot(str(SHOTS / f"{CYCLE}_{name}.png"))


def fill_form(driver, name="Priya Sharma", phone="9876543210", email="", date="2026-11-18",
              time="13:00", party="2"):
    for field, value in (("customer_name", name), ("phone", phone), ("email", email),
                         ("date", date), ("party_size", party)):
        box = driver.find_element(By.ID, field)
        box.clear()
        box.send_keys(value)
    Select(driver.find_element(By.ID, "time")).select_by_value(time)


def submit(driver):
    driver.find_element(By.ID, "submit-booking").click()


def wait_for(driver, element_id):
    return WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, element_id)))


def test_TC_UI_01_home_page_loads(driver, base_url, record):
    driver.get(base_url)
    form = wait_for(driver, "booking-form")
    shot(driver, "TC-UI-01_home_page")
    record("Booking form visible, title contains 'Book a table'",
           f"Form visible={form.is_displayed()}, title='{driver.title}'")
    assert form.is_displayed() and "Book a table" in driver.title


def test_TC_UI_02_successful_booking(driver, base_url, record):
    driver.get(base_url)
    fill_form(driver)
    submit(driver)
    banner = wait_for(driver, "success-banner")
    rid = driver.find_element(By.ID, "reservation-id").text
    table = driver.find_element(By.ID, "detail-table").text
    shot(driver, "TC-UI-02_booking_confirmed")
    record("Confirmation page with reservation ID and table T1",
           f"Banner shown, {rid}, table {table}")
    assert banner.is_displayed() and rid.startswith("R") and table == "T1"


def test_TC_UI_03_invalid_phone_shows_error(driver, base_url, record):
    driver.get(base_url)
    fill_form(driver, phone="12345")
    submit(driver)
    error = wait_for(driver, "form-error").text
    shot(driver, "TC-UI-03_invalid_phone_error")
    record("Error message about phone number", error)
    assert "Phone" in error


def test_TC_UI_04_form_keeps_input_after_error(driver, base_url, record):
    driver.get(base_url)
    fill_form(driver, name="Rahul Verma", phone="12345", party="3")
    submit(driver)
    wait_for(driver, "form-error")
    kept_name = driver.find_element(By.ID, "customer_name").get_attribute("value")
    kept_phone = driver.find_element(By.ID, "phone").get_attribute("value")
    kept_party = driver.find_element(By.ID, "party_size").get_attribute("value")
    shot(driver, "TC-UI-04_form_after_error")
    record("Name 'Rahul Verma', phone '12345', guests '3' still filled in",
           f"Name '{kept_name}', phone '{kept_phone}', guests '{kept_party}'")
    assert (kept_name, kept_phone, kept_party) == ("Rahul Verma", "12345", "3")


def test_TC_UI_05_cancel_from_confirmation_page(driver, base_url, record):
    driver.get(base_url)
    fill_form(driver, party="6", time="19:00")       # Wednesday 19:00, deposit 600
    submit(driver)
    old_status = wait_for(driver, "reservation-status")
    driver.find_element(By.ID, "cancel-button").click()
    WebDriverWait(driver, 5).until(EC.staleness_of(old_status))     # wait for page reload
    status = wait_for(driver, "reservation-status").text
    refund = driver.find_element(By.ID, "detail-refund").text
    shot(driver, "TC-UI-05_cancelled")
    record("Status CANCELLED, refund ₹600", f"Status {status}, refund {refund}")
    assert status == "CANCELLED" and refund == "₹600"


def test_TC_UI_06_staff_seat_and_complete(driver, base_url, record):
    driver.get(base_url)
    fill_form(driver)
    submit(driver)
    rid = wait_for(driver, "reservation-id").text
    driver.get(f"{base_url}/reservations?date=2026-11-18")
    row = f"row-{rid}"

    def click_action(action):
        old_row = wait_for(driver, row)
        old_row.find_element(By.CSS_SELECTOR, f"[data-action={action}]").click()
        WebDriverWait(driver, 5).until(EC.staleness_of(old_row))   # wait for page reload
        return wait_for(driver, row).find_element(By.CSS_SELECTOR, "[data-status]").text

    seated = click_action("SEATED")
    shot(driver, "TC-UI-06a_staff_seated")
    completed = click_action("COMPLETED")
    shot(driver, "TC-UI-06b_staff_completed")
    record("SEATED then COMPLETED", f"{seated} then {completed}")
    assert (seated, completed) == ("SEATED", "COMPLETED")


def test_TC_UI_07_weekend_peak_large_party_deposit(driver, base_url, record):
    driver.get(base_url)
    fill_form(driver, party="6", date="2026-11-21", time="19:00")   # Saturday peak
    submit(driver)
    deposit = wait_for(driver, "detail-deposit").text
    shot(driver, "TC-UI-07_weekend_deposit")
    record("Deposit ₹900", f"Deposit {deposit}")
    assert deposit == "₹900"


def test_TC_UI_08_unknown_reservation_page(driver, base_url, record):
    driver.get(f"{base_url}/reservation/R9999")
    text = wait_for(driver, "message-text").text
    shot(driver, "TC-UI-08_not_found")
    record("'Reservation R9999 not found'", text)
    assert "not found" in text
