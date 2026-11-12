from decimal import Decimal

import pytest

from expense_tracker import currency

pytestmark = pytest.mark.external


def test_frankfurter_returns_a_plausible_eur_to_nok_rate():
    rate = currency.get_rate("EUR", "NOK")

    assert Decimal("5") < rate < Decimal("20")
