from datetime import date
from decimal import Decimal

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
