from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class Expense:
    amount: Decimal
    currency: str
    date: date
    description: str
    category: str
    