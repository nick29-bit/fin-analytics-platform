from datetime import datetime

from pydantic import BaseModel, Field


class Transaction(BaseModel):
    transaction_id: str
    card_number: str
    merchant_name: str
    merchant_category: str
    amount: float = Field(gt=0, description="Transaction amount, must be positive")
    transaction_timestamp: datetime
    cardholder_lat: float
    cardholder_long: float
    merchant_lat: float
    merchant_long: float
    is_fraud: bool
