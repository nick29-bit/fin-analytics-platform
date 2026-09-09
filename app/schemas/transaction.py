from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class PaymentMethod(str, Enum):
    credit_card = "credit_card"
    debit_card = "debit_card"
    bank_transfer = "bank_transfer"


class Transaction(BaseModel):
    transaction_id: str
    timestamp: datetime
    customer_id: str
    merchant: str
    category: str
    amount: float = Field(gt=0, description="Transaction amount, must be positive")
    currency: str
    payment_method: PaymentMethod
