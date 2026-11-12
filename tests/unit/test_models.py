from datetime import date
from decimal import Decimal

import pytest

from expense_tracker.models import Expense


def test_expense_stores_its_fields():
    expense = Expense(
        amount=Decimal("125.50"),
        currency="NOK",
        date=date(2026, 11, 9),
        description="Lidl weekly shop",
        category="groceries",
    )

    assert expense.amount == Decimal("125.50")
    assert expense.currency == "NOK"
    assert expense.date == date(2026, 11, 9)
    assert expense.description == "Lidl weekly shop"
    assert expense.category == "groceries"


def test_expense_rejects_negative_amount():
    with pytest.raises(ValueError, match="amount"):
        Expense(
            amount=Decimal("-10.00"),
            currency="NOK",
            date=date(2026, 11, 9),
            description="Refund?",
            category="other",
        )


def test_expense_rejects_empty_description():
    with pytest.raises(ValueError, match="description"):
        Expense(
            amount=Decimal("10.00"),
            currency="NOK",
            date=date(2026, 11, 9),
            description="",
            category="other",
        )


def test_expense_rejects_unsupported_currency():
    with pytest.raises(ValueError, match="currency"):
        Expense(
            amount=Decimal("10.00"),
            currency="XYZ",
            date=date(2026, 11, 9),
            description="Mystery purchase",
            category="other",
        )
