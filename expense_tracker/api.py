import datetime
from collections.abc import Iterator
from contextlib import asynccontextmanager
from dataclasses import asdict
from decimal import Decimal

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from expense_tracker import db
from expense_tracker.categorizer import categorize
from expense_tracker.models import Expense
from expense_tracker.summary import monthly_total, total_by_category

engine = create_engine("sqlite:///expenses.db")


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.Base.metadata.create_all(engine)
    yield


MONTH_PATTERN = r"^\d{4}-(0[1-9]|1[0-2])$"


app = FastAPI(lifespan=lifespan)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


def get_today() -> datetime.date:
    return datetime.date.today()


class ExpenseIn(BaseModel):
    amount: Decimal
    currency: str
    date: datetime.date | None = None
    description: str
    category: str | None = None


class ExpenseOut(BaseModel):
    id: int
    amount: Decimal
    currency: str
    date: datetime.date
    description: str
    category: str


@app.post("/expenses", status_code=201)
def create_expense(
    payload: ExpenseIn,
    session: Session = Depends(get_session),
    today: datetime.date = Depends(get_today),
) -> ExpenseOut:
    try:
        category = payload.category or categorize(payload.description)
        expense = Expense(
            amount=payload.amount,
            currency=payload.currency,
            date=payload.date or today,
            description=payload.description,
            category=category,
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    expense.id = db.add_expense(session, expense)
    return ExpenseOut(**asdict(expense))


@app.get("/expenses")
def get_expenses(
    month: str = Query(pattern=MONTH_PATTERN),
    session: Session = Depends(get_session),
) -> list[ExpenseOut]:
    year, month_number = (int(part) for part in month.split("-"))
    expenses = db.list_expenses(session, year, month_number)
    return [ExpenseOut(**asdict(expense)) for expense in expenses]


class SummaryOut(BaseModel):
    month: str
    total: Decimal
    by_category: dict[str, Decimal]


@app.get("/summary")
def get_summary(
    month: str = Query(pattern=MONTH_PATTERN),
    session: Session = Depends(get_session),
) -> SummaryOut:
    year, month_number = (int(part) for part in month.split("-"))
    expenses = db.list_expenses(session, year, month_number)
    return SummaryOut(
        month=month,
        total=monthly_total(expenses, year, month_number),
        by_category=total_by_category(expenses),
    )


@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int, session: Session = Depends(get_session)) -> None:
    if not db.delete_expense(session, expense_id):
        raise HTTPException(status_code=404, detail=f"expense {expense_id} not found")
