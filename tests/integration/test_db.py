from datetime import date
from decimal import Decimal

import pytest

from expense_tracker.db import add_expense, delete_expense, get_expense, list_expenses
from expense_tracker.models import Expense


def test_add_expense_saves_it_and_returns_an_id(db_session):
    expense = Expense(
        amount=Decimal("125.50"),
        currency="NOK",
        date=date(2026, 11, 9),
        description="Lidl weekly shop",
        category="groceries",
    )

    expense_id = add_expense(db_session, expense)

    assert get_expense(db_session, expense_id) == expense


def test_list_expenses_returns_only_that_month_in_date_order(db_session, sample_expenses):
    for expense in sample_expenses:
        add_expense(db_session, expense)

    november = list_expenses(db_session, 2026, 11)

    assert november == sample_expenses[:3]


def test_delete_expense_removes_it(db_session, sample_expenses):
    expense_id = add_expense(db_session, sample_expenses[0])

    assert delete_expense(db_session, expense_id) is True
    assert get_expense(db_session, expense_id) is None


def test_delete_expense_returns_false_for_missing_id(db_session):
    assert delete_expense(db_session, 999) is False


@pytest.mark.parametrize(
    ("day", "year", "month", "included"),
    [
        pytest.param(date(2026, 11, 1), 2026, 11, True, id="first day of month"),
        pytest.param(date(2026, 11, 30), 2026, 11, True, id="last day of month"),
        pytest.param(date(2026, 10, 31), 2026, 11, False, id="day before month"),
        pytest.param(date(2026, 12, 1), 2026, 11, False, id="day after month"),
        pytest.param(date(2028, 2, 29), 2028, 2, True, id="Feb 29 in leap year"),
        pytest.param(date(2028, 2, 29), 2028, 3, False, id="Feb 29 not in March"),
        pytest.param(date(2026, 12, 31), 2026, 12, True, id="Dec 31 in December"),
        pytest.param(date(2027, 1, 1), 2026, 12, False, id="Jan 1 not in previous December"),
        pytest.param(date(2025, 12, 15), 2026, 12, False, id="same month, other year"),
    ],
)
def test_list_expenses_month_boundaries(db_session, day, year, month, included):
    expense = Expense(Decimal("10.00"), "NOK", day, "Test expense", "other")
    add_expense(db_session, expense)

    result = list_expenses(db_session, year, month)

    assert (expense in result) is included
