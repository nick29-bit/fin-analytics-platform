import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

NUM_TRANSACTIONS = 1000

MERCHANTS = ["Amazon", "Walmart", "Starbucks", "Uber", "Netflix", "Target", "Shell", "Delta Airlines", "Best Buy", "Costco"]
CATEGORIES = ["groceries", "travel", "entertainment", "utilities", "dining", "shopping", "fuel"]
PAYMENT_METHODS = ["credit_card", "debit_card", "bank_transfer"]


def random_timestamp(start_days_ago=90):
    start = datetime.now() - timedelta(days=start_days_ago)
    random_seconds = random.randint(0, start_days_ago * 24 * 60 * 60)
    return start + timedelta(seconds=random_seconds)


def generate_transactions(n):
    rows = []
    for i in range(1, n + 1):
        amount = round(np.random.exponential(scale=60) + 1, 2)
        rows.append({
            "transaction_id": f"TXN{i:06d}",
            "timestamp": random_timestamp(),
            "customer_id": f"CUST{random.randint(1, 200):04d}",
            "merchant": random.choice(MERCHANTS),
            "category": random.choice(CATEGORIES),
            "amount": amount,
            "currency": "USD",
            "payment_method": random.choice(PAYMENT_METHODS),
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = generate_transactions(NUM_TRANSACTIONS)
    df.to_csv("data/raw/transactions.csv", index=False)
    print(f"Generated {len(df)} transactions -> data/transactions.csv")
    print(df.head())
