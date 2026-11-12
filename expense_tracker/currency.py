from decimal import ROUND_HALF_UP, Decimal

import httpx2

RATES_URL = "https://api.frankfurter.dev/v1/latest"
CENT = Decimal("0.01")


class ExchangeRateError(Exception):
    """The exchange rate could not be fetched."""


def get_rate(from_: str, to: str) -> Decimal:
    if from_ == to:
        return Decimal("1")
    try:
        response = httpx2.get(RATES_URL, params={"base": from_, "symbols": to}, timeout=5)
        response.raise_for_status()
        return Decimal(str(response.json()["rates"][to]))
    except httpx2.TimeoutException as error:
        raise ExchangeRateError(f"exchange-rate API timed out: {error}") from error
    except httpx2.HTTPStatusError as error:
        status = error.response.status_code
        raise ExchangeRateError(f"exchange-rate API returned HTTP {status}") from error
    except KeyError as error:
        raise ExchangeRateError(f"exchange-rate API response has no rate for {to}") from error


def convert(amount: Decimal, from_: str, to: str) -> Decimal:
    return (amount * get_rate(from_, to)).quantize(CENT, rounding=ROUND_HALF_UP)
