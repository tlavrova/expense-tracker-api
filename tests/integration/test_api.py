import pytest

from expense_tracker.db import add_expense

def test_post_expense_returns_201_with_the_saved_expense(client):
    response = client.post(
        "/expenses",
        json={
            "amount": "125.50",
            "currency": "NOK",
            "date": "2026-11-09",
            "description": "Lidl weekly shop",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "amount": "125.50",
        "currency": "NOK",
        "date": "2026-11-09",
        "description": "Lidl weekly shop",
        "category": "groceries",
    }


def test_get_expenses_returns_that_months_expenses_with_ids(client, db_session, sample_expenses):
    for expense in sample_expenses:
        add_expense(db_session, expense)

    response = client.get("/expenses", params={"month": "2026-11"})

    assert response.status_code == 200
    body = response.json()
    assert [item["description"] for item in body] == [
        "Rema 1000 groceries",
        "Uber to office",
        "Coffee",
    ]
    assert body[0] == {
        "id": 1,
        "amount": "349.90",
        "currency": "NOK",
        "date": "2026-11-02",
        "description": "Rema 1000 groceries",
        "category": "groceries",
    }


def test_get_summary_returns_month_total_and_category_totals(client, db_session, sample_expenses):
    nok_expenses = [e for e in sample_expenses if e.currency == "NOK"]
    for expense in nok_expenses:
        add_expense(db_session, expense)

    response = client.get("/summary", params={"month": "2026-11"})

    assert response.status_code == 200
    assert response.json() == {
        "month": "2026-11",
        "total": "538.90",
        "by_category": {
            "groceries": "349.90",
            "transport": "189.00",
        },
    }


def test_delete_expense_returns_204_and_removes_it(client, db_session, sample_expenses):
    expense_id = add_expense(db_session, sample_expenses[0])

    response = client.delete(f"/expenses/{expense_id}")

    assert response.status_code == 204
    assert client.get("/expenses", params={"month": "2026-11"}).json() == []


def test_delete_missing_expense_returns_404(client):
    response = client.delete("/expenses/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "expense 999 not found"}


VALID_PAYLOAD = {
    "amount": "125.50",
    "currency": "NOK",
    "date": "2026-11-09",
    "description": "Lidl weekly shop",
}


def without(field):
    return {key: value for key, value in VALID_PAYLOAD.items() if key != field}


def with_value(field, value):
    return {**VALID_PAYLOAD, field: value}


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param({}, id="empty body"),
        pytest.param(without("amount"), id="missing amount"),
        pytest.param(without("currency"), id="missing currency"),
        pytest.param(without("date"), id="missing date"),
        pytest.param(without("description"), id="missing description"),
        pytest.param(with_value("amount", "abc"), id="amount not a number"),
        pytest.param(with_value("date", "09.11.2026"), id="date in wrong format"),
        pytest.param(with_value("date", "2026-02-30"), id="impossible date"),
        pytest.param(with_value("description", 123), id="description not a string"),
        pytest.param(with_value("amount", "-10.00"), id="negative amount"),
        pytest.param(with_value("currency", "XYZ"), id="unsupported currency"),
        pytest.param(with_value("description", "   "), id="blank description"),
    ],
)
def test_post_expense_rejects_invalid_payload_with_422(client, payload):
    response = client.post("/expenses", json=payload)

    assert response.status_code == 422
