from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal


SUPPORTED_CURRENCIES = {"NOK", "EUR", "USD", "SEK"}


@dataclass
class Expense:
    amount: Decimal
    currency: str
    date: date
    description: str
    category: str
    id: int | None = field(default=None, compare=False)

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError(f"amount must not be negative, got {self.amount}")
        if not self.description.strip():
            raise ValueError("description must not be empty")
        if self.currency not in SUPPORTED_CURRENCIES:
            raise ValueError(f"unsupported currency: {self.currency}")
    