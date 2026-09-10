from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class TransactionStatus(str, Enum):
    approved = "approved"
    declined = "declined"
    pending = "pending"


class Channel(str, Enum):
    online = "online"
    in_store = "in-store"
    mobile = "mobile"


class Transaction(BaseModel):
    transaction_id: str
    customer_id: str
    merchant_name: str
    merchant_category: str
    amount: float = Field(gt=0, description="Transaction amount, must be positive")
    currency: str
    status: TransactionStatus
    channel: Channel
    city: str
    transaction_timestamp: datetime
    is_fraud: bool
