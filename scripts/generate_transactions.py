import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

NUM_TRANSACTIONS = 5000
SAMPLE_SIZE = 200

MERCHANTS = ["Amazon", "Walmart", "Starbucks", "Uber", "Netflix", "Target", "Shell", "Delta Airlines", "Best Buy", "Costco"]
CATEGORIES = ["groceries", "travel", "entertainment", "utilities", "dining", "shopping", "fuel"]
STATUSES = ["approved", "declined", "pending"]
STATUS_WEIGHTS = [0.92, 0.06, 0.02]
CHANNELS = ["online", "in-store", "mobile"]
CITIES = ["Chicago", "New York", "Austin", "Seattle", "Denver", "Atlanta", "Miami", "Phoenix"]


def random_timestamp(start_days_ago=90):
    start = datetime.now() - timedelta(days=start_days_ago)
    random_seconds = random.randint(0, start_days_ago * 24 * 60 * 60)
    return start + timedelta(seconds=random_seconds)


def generate_transactions(n):
    rows = []
    for i in range(1, n + 1):
        amount = round(np.random.exponential(scale=60) + 1, 2)
        is_fraud = random.random() < 0.02
        rows.append({
            "transaction_id": f"TXN-{i:06d}",
            "customer_id": f"CUST-{random.randint(1, 200):04d}",
            "merchant_name": random.choice(MERCHANTS),
            "merchant_category": random.choice(CATEGORIES),
            "amount": amount,
            "currency": "USD",
            "status": random.choices(STATUSES, weights=STATUS_WEIGHTS, k=1)[0],
            "channel": random.choice(CHANNELS),
            "city": random.choice(CITIES),
            "transaction_timestamp": random_timestamp(),
            "is_fraud": is_fraud,
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = generate_transactions(NUM_TRANSACTIONS)
    df.to_csv("data/raw/transactions.csv", index=False)
    print(f"Generated {len(df)} transactions -> data/raw/transactions.csv")
    print(df.head())

    sample_df = df.head(SAMPLE_SIZE)
    sample_df.to_csv("data/sample/transactions_sample.csv", index=False)
    print(f"Wrote {len(sample_df)}-row sample -> data/sample/transactions_sample.csv")
