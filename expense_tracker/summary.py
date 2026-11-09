from collections import defaultdict
from decimal import Decimal

from expense_tracker.models import Expense


def monthly_total(expenses: list[Expense], year: int, month: int) -> Decimal:
    return sum(
        (e.amount for e in expenses if e.date.year == year and e.date.month == month),
        Decimal("0"),
    )


def total_by_category(expenses: list[Expense]) -> dict[str, Decimal]:
    totals: defaultdict[str, Decimal] = defaultdict(Decimal)
    for e in expenses:
        totals[e.category] += e.amount
    return dict(totals)
