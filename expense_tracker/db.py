import datetime
from decimal import Decimal

from sqlalchemy import Numeric, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from expense_tracker.models import Expense


class Base(DeclarativeBase):
    pass


class ExpenseRow(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(String(3))
    date: Mapped[datetime.date]
    description: Mapped[str]
    category: Mapped[str]


def add_expense(session: Session, expense: Expense) -> int:
    row = ExpenseRow(
        amount=expense.amount,
        currency=expense.currency,
        date=expense.date,
        description=expense.description,
        category=expense.category,
    )
    session.add(row)
    session.commit()
    return row.id


def get_expense(session: Session, expense_id: int) -> Expense | None:
    row = session.get(ExpenseRow, expense_id)
    if row is None:
        return None
    return _to_expense(row)


def list_expenses(session: Session, year: int, month: int) -> list[Expense]:
    start = datetime.date(year, month, 1)
    if month == 12:
        end = datetime.date(year + 1, 1, 1)
    else:
        end = datetime.date(year, month + 1, 1)
    rows = session.scalars(
        select(ExpenseRow)
        .where(ExpenseRow.date >= start, ExpenseRow.date < end)
        .order_by(ExpenseRow.date, ExpenseRow.id)
    )
    return [_to_expense(row) for row in rows]


def delete_expense(session: Session, expense_id: int) -> bool:
    row = session.get(ExpenseRow, expense_id)
    if row is None:
        return False
    session.delete(row)
    session.commit()
    return True


def _to_expense(row: ExpenseRow) -> Expense:
    return Expense(
        amount=row.amount,
        currency=row.currency,
        date=row.date,
        description=row.description,
        category=row.category,
        id=row.id,
    )
