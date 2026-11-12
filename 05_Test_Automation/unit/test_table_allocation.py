"""TC-TA-01 .. TC-TA-07: Table allocation tests (R7)."""
from conftest import attempt, booking


def _book(service, n, party, time="19:00"):
    return attempt(service, booking(phone=f"90000{n:05d}", party_size=party, time=time))


def test_TC_TA_01_party_of_2_gets_smallest_table(service, record):
    actual = _book(service, 1, 2)
    record("Accepted, table T1", actual)
    assert "table T1" in actual


def test_TC_TA_02_party_of_3_gets_4_seater(service, record):
    actual = _book(service, 1, 3)
    record("Accepted, table T3", actual)
    assert "table T3" in actual


def test_TC_TA_03_party_of_5_gets_6_seater(service, record):
    actual = _book(service, 1, 5)
    record("Accepted, table T6", actual)
    assert "table T6" in actual


def test_TC_TA_04_two_couples_same_slot(service, record):
    first, second = _book(service, 1, 2), _book(service, 2, 2)
    record("T1 then T2", f"{first} | {second}")
    assert "table T1" in first and "table T2" in second


def test_TC_TA_05_third_couple_moves_up_a_size(service, record):
    _book(service, 1, 2), _book(service, 2, 2)
    third = _book(service, 3, 2)
    record("Accepted, table T3", third)
    assert "table T3" in third


def test_TC_TA_06_restaurant_full(service, record):
    for n, party in enumerate([7, 6, 6, 4, 4, 4, 2, 2], start=1):   # fills all 8 tables
        assert _book(service, n, party).startswith("Accepted")
    actual = _book(service, 99, 1)
    record("Rejected: No table available", actual)
    assert actual.startswith("Rejected") and "No table available" in actual


def test_TC_TA_07_tables_are_not_combined(service, record):
    """Party of 7 needs T8; two free 6-seaters are not joined together."""
    _book(service, 1, 7)
    actual = _book(service, 2, 7)
    record("Rejected: No table available", actual)
    assert actual.startswith("Rejected")
