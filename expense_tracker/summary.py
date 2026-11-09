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


WARNING_THRESHOLD = Decimal("0.8")


def budget_status(expenses: list[Expense], budget: Decimal) -> str:
    if budget < 0:
        raise ValueError(f"budget must not be negative, got {budget}")
    spent = sum((e.amount for e in expenses), Decimal("0"))
    if spent > budget:
        return "exceeded"
    if spent >= budget * WARNING_THRESHOLD:
        return "warning"
    return "ok"
