from decimal import Decimal

import httpx2
import pytest

from expense_tracker import currency


def fake_response(status_code, json):
    request = httpx2.Request("GET", currency.RATES_URL)
    return httpx2.Response(status_code, json=json, request=request)


def test_convert_uses_the_rate_from_the_api(monkeypatch):
    def fake_get(url, params, timeout):
        assert params == {"base": "EUR", "symbols": "NOK"}
        return fake_response(200, {"base": "EUR", "rates": {"NOK": 11.5}})

    monkeypatch.setattr(currency.httpx2, "get", fake_get)

    assert currency.convert(Decimal("10.00"), "EUR", "NOK") == Decimal("115.00")


def test_convert_raises_exchange_rate_error_on_timeout(monkeypatch):
    def fake_get(url, params, timeout):
        raise httpx2.ReadTimeout("read timed out")

    monkeypatch.setattr(currency.httpx2, "get", fake_get)

    with pytest.raises(currency.ExchangeRateError, match="timed out"):
        currency.convert(Decimal("10.00"), "EUR", "NOK")


@pytest.mark.parametrize(
    ("status_code", "body"),
    [
        pytest.param(500, {"message": "internal error"}, id="server error"),
        pytest.param(404, {"message": "not found"}, id="not found"),
        pytest.param(200, {"base": "EUR", "rates": {}}, id="rate missing"),
        pytest.param(200, {"unexpected": "shape"}, id="no rates in body"),
    ],
)
def test_convert_raises_exchange_rate_error_on_bad_response(monkeypatch, status_code, body):
    def fake_get(url, params, timeout):
        return fake_response(status_code, body)

    monkeypatch.setattr(currency.httpx2, "get", fake_get)

    with pytest.raises(currency.ExchangeRateError):
        currency.convert(Decimal("10.00"), "EUR", "NOK")


def test_convert_same_currency_returns_amount_without_calling_api(monkeypatch):
    def fake_get(url, params, timeout):
        raise AssertionError("the API should not be called for a same-currency conversion")

    monkeypatch.setattr(currency.httpx2, "get", fake_get)

    assert currency.convert(Decimal("42.50"), "NOK", "NOK") == Decimal("42.50")


@pytest.mark.parametrize(
    ("amount", "rate", "expected"),
    [
        pytest.param("1.00", 10.125, "10.13", id="exact half cent rounds up"),
        pytest.param("0.50", 0.25, "0.13", id="small exact half rounds up"),
        pytest.param("1.00", 10.1249, "10.12", id="just below half rounds down"),
    ],
)
def test_convert_rounds_half_cents_up(monkeypatch, amount, rate, expected):
    def fake_get(url, params, timeout):
        return fake_response(200, {"base": "EUR", "rates": {"NOK": rate}})

    monkeypatch.setattr(currency.httpx2, "get", fake_get)

    assert currency.convert(Decimal(amount), "EUR", "NOK") == Decimal(expected)
