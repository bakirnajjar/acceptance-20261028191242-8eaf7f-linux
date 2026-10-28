import pytest

from pricing import LineItem, discount_percent, receipt, subtotal_cents, total_cents


def test_subtotal_multiplies_quantity_by_unit_price():
    assert subtotal_cents([LineItem("A", 2, 150), LineItem("B", 1, 999)]) == 1299


def test_discount_codes_ignore_case_and_whitespace():
    assert discount_percent(" spring10 ") == 10
    assert discount_percent("LOYAL5") == 5


def test_unknown_or_missing_codes_give_no_discount():
    assert discount_percent(None) == 0
    assert discount_percent("") == 0
    assert discount_percent("UNKNOWN") == 0


def test_discount_rounds_half_up():
    assert total_cents([LineItem("A", 1, 105)], "SPRING10") == (11, 94)


def test_receipt_reports_count_discount_and_total():
    items = [LineItem("A", 2, 1000), LineItem("B", 3, 250)]
    assert receipt(items, "LOYAL5") == "5 item(s), discount 1.38, total 26.12"


def test_invalid_lines_are_rejected():
    with pytest.raises(ValueError):
        LineItem("A", 0, 100)
    with pytest.raises(ValueError):
        LineItem("A", 1, -1)
