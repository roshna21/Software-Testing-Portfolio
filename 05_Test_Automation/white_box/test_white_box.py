"""TC-WB-01 .. TC-WB-06: White-box tests (statement coverage and branch coverage).

Black-box tests are designed from the requirements. These tests are designed
by READING THE CODE, so that every statement runs and every decision (if)
goes both ways. Design: 02_Test_Case_Design/06_White_Box_Testing.md

Functions under test
  F1  calculate_deposit()    application/reservation_system/service.py
  F2  validate_party_size()  application/reservation_system/validators.py

Run and see the coverage of each function:
  bash demo.sh wb
"""
from datetime import date, time

import pytest

from reservation_system.service import calculate_deposit
from reservation_system.validators import ValidationError, validate_party_size

SAT, WED = date(2026, 11, 21), date(2026, 11, 18)


# ---------------------------------------------------------------- F1 calculate_deposit
# Decisions:  D1  if party_size >= LARGE_PARTY       (True / False)
#             D2  if is_weekend and is_peak          (True / False)

def test_TC_WB_01_deposit_all_statements(record):
    """Statement coverage: party 6, Saturday 19:00 makes D1 True and D2 True,
    so EVERY statement of calculate_deposit runs (100% statement coverage).
    But the False side of D1 and D2 is never taken (only 50% branch coverage)."""
    actual = calculate_deposit(6, SAT, time(19, 0))
    record("Rs.900 (path D1=True, D2=True)", f"Rs.{actual}")
    assert actual == 900


def test_TC_WB_02_deposit_false_branches(record):
    """Branch coverage: party 2, Wednesday 13:00 makes D1 False and D2 False.
    Together with TC-WB-01 every branch outcome is taken (100% branch coverage)."""
    actual = calculate_deposit(2, WED, time(13, 0))
    record("Rs.0 (path D1=False, D2=False)", f"Rs.{actual}")
    assert actual == 0


# ---------------------------------------------------------------- F2 validate_party_size
# Decisions:  D3  int(...) raises an error?          (Yes -> except block / No)
#             D4  if not 1 <= size <= 8              (True -> raise / False -> return)

def test_TC_WB_03_party_size_valid_path(record):
    """D3 = No, D4 = False: the 'return size' statement runs."""
    actual = validate_party_size("4")
    record("returns 4", f"returns {actual}")
    assert actual == 4


def test_TC_WB_04_party_size_not_a_number_path(record):
    """D3 = Yes: the except block runs."""
    with pytest.raises(ValidationError) as err:
        validate_party_size("four")
    record("ValidationError: whole number", f"ValidationError: {err.value.message}")
    assert "whole number" in err.value.message


def test_TC_WB_05_party_size_out_of_range_path(record):
    """D3 = No, D4 = True (size too big): the range error statement runs.
    After TC-WB-03, 04 and 05: 100% statement and 100% branch coverage of F2."""
    with pytest.raises(ValidationError) as err:
        validate_party_size(9)
    record("ValidationError: between 1 and 8", f"ValidationError: {err.value.message}")
    assert "between 1 and 8" in err.value.message


def test_TC_WB_06_party_size_lower_side_of_condition(record):
    """D4 is a compound condition (1 <= size AND size <= 8). Branch coverage is
    already 100% after TC-WB-05, but only the 'size <= 8' part has been false.
    This test makes the '1 <= size' part false too (condition coverage - extra)."""
    with pytest.raises(ValidationError) as err:
        validate_party_size(0)
    record("ValidationError: between 1 and 8", f"ValidationError: {err.value.message}")
    assert "between 1 and 8" in err.value.message
