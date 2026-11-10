from datetime import date
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from expense_tracker.api import app, get_session
from expense_tracker.db import Base
from expense_tracker.models import Expense


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    engine.dispose()


@pytest.fixture
def client(db_session):
    app.dependency_overrides[get_session] = lambda: db_session
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def sample_expenses():
    return [
        Expense(Decimal("349.90"), "NOK", date(2026, 11, 2), "Rema 1000 groceries", "groceries"),
        Expense(Decimal("189.00"), "NOK", date(2026, 11, 14), "Uber to office", "transport"),
        Expense(Decimal("12.50"), "EUR", date(2026, 11, 30), "Coffee", "other"),
        Expense(Decimal("899.00"), "NOK", date(2026, 10, 31), "Lidl big shop", "groceries"),
        Expense(Decimal("250.00"), "NOK", date(2026, 12, 1), "Taxi home", "transport"),
    ]
