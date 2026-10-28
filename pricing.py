"""Synthetic order pricing for Futuristic acceptance testing (not production code)."""

from typing import Dict, List, Optional, Tuple

DISCOUNTS = {"SPRING10": 10, "LOYAL5": 5}  # type: Dict[str, int]


class LineItem(object):
    """One order line; prices are integer cents."""

    def __init__(self, sku, quantity, unit_cents):
        # type: (str, int, int) -> None
        if quantity <= 0:
            raise ValueError("quantity must be positive: %r" % (quantity,))
        if unit_cents < 0:
            raise ValueError("unit price must not be negative: %r" % (unit_cents,))
        self.sku = sku
        self.quantity = quantity
        self.unit_cents = unit_cents

    def __repr__(self):
        return "LineItem(%r, %r, %r)" % (self.sku, self.quantity, self.unit_cents)


def subtotal_cents(items):
    # type: (List[LineItem]) -> int
    total = 0
    for item in items:
        total += item.quantity * item.unit_cents
    return total


def discount_percent(code):
    # type: (Optional[str]) -> int
    if not code:
        return 0
    return DISCOUNTS.get(code.strip().upper(), 0)


def total_cents(items, code=None):
    # type: (List[LineItem], Optional[str]) -> Tuple[int, int]
    """Return (discount, total) in cents, rounding the discount half up."""
    subtotal = subtotal_cents(items)
    discount = (subtotal * discount_percent(code) + 50) // 100
    return discount, subtotal - discount


def receipt(items, code=None):
    # type: (List[LineItem], Optional[str]) -> str
    discount, total = total_cents(items, code)
    count = sum([item.quantity for item in items])
    return "%d item(s), discount %d.%02d, total %d.%02d" % (
        count,
        discount // 100,
        discount % 100,
        total // 100,
        total % 100,
    )
