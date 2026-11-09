from datetime import date
from decimal import Decimal

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
