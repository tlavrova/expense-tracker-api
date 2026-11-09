from datetime import date
from decimal import Decimal

import pytest

from expense_tracker.models import Expense
from expense_tracker.summary import budget_status, monthly_total, total_by_category


def make_expense(amount, day, category="other"):
    return Expense(
        amount=Decimal(amount),
        currency="NOK",
        date=day,
        description="test",
        category=category,
    )


def test_monthly_total_sums_expenses_in_that_month():
    expenses = [
        make_expense("100.00", date(2026, 11, 1)),
        make_expense("50.25", date(2026, 11, 30)),
    ]
    assert monthly_total(expenses, 2026, 11) == Decimal("150.25")


def test_monthly_total_ignores_other_months():
    expenses = [
        make_expense("100.00", date(2026, 11, 15)),
        make_expense("999.00", date(2026, 10, 31)),
        make_expense("999.00", date(2026, 12, 1)),
    ]
    assert monthly_total(expenses, 2026, 11) == Decimal("100.00")


def test_monthly_total_of_empty_month_is_zero():
    assert monthly_total([], 2026, 11) == Decimal("0")


def test_total_by_category_sums_each_category():
    expenses = [
        make_expense("200.00", date(2026, 11, 1), "groceries"),
        make_expense("100.00", date(2026, 11, 2), "groceries"),
        make_expense("85.00", date(2026, 11, 3), "transport"),
    ]
    assert total_by_category(expenses) == {
        "groceries": Decimal("300.00"),
        "transport": Decimal("85.00"),
    }


def test_total_by_category_of_no_expenses_is_empty():
    assert total_by_category([]) == {}

def test_budget_status_returns_ok_below_80_percent():
    expenses = [make_expense("500.00", date(2026, 11, 1))]
    assert budget_status(expenses, Decimal("1000")) == "ok"


def test_budget_status_returns_warning_at_80_percent():
    expenses = [make_expense("800.00", date(2026, 11, 1))]
    assert budget_status(expenses, Decimal("1000")) == "warning"


def test_budget_status_returns_exceeded_over_100_percent():
    expenses = [make_expense("1000.01", date(2026, 11, 1))]
    assert budget_status(expenses, Decimal("1000")) == "exceeded"


def test_budget_status_rejects_negative_budget():
    with pytest.raises(ValueError, match="budget"):
        budget_status([], Decimal("-100"))
