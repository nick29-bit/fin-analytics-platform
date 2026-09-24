from pathlib import Path

import pandas as pd

from app.ingestion.csv_ingestion import load_transactions
from app.services.fraud_detection import (
    RULE_COLUMNS,
    evaluate_against_ground_truth,
    flag_suspicious_transactions,
)


DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data/raw/fraudTrain.csv"
)

CARD_COUNT = 20
RANDOM_SEED = 42


def main():
    print("Loading raw data...", flush=True)
    df = load_transactions(DATA_PATH)

    cards = (
        df["card_number"]
        .drop_duplicates()
        .sort_values()
        .sample(n=CARD_COUNT, random_state=RANDOM_SEED)
    )

    history = df[df["card_number"].isin(cards)].copy()

    print("Selected cards:", history["card_number"].nunique())
    print("Transactions:", len(history))
    print("Running all six rules...", flush=True)

    result = flag_suspicious_transactions(history)
    evaluate_against_ground_truth(result)

    fraud = result["is_fraud"]
    fraud_count = int(fraud.sum())
    rows = []

    for rule in RULE_COLUMNS:
        flagged = result[rule]
        caught = int((flagged & fraud).sum())
        false_alarms = int((flagged & ~fraud).sum())
        flag_count = int(flagged.sum())

        other_columns = [
            column for column in RULE_COLUMNS if column != rule
        ]
        other_flags = result[other_columns].any(axis=1)

        rows.append({
            "rule": rule,
            "flags": flag_count,
            "caught": caught,
            "false_alarms": false_alarms,
            "precision_pct": (
                round(100 * caught / flag_count, 1)
                if flag_count else None
            ),
            "recall_pct": (
                round(100 * caught / fraud_count, 1)
                if fraud_count else None
            ),
            "unique_fraud_caught": int(
                (flagged & fraud & ~other_flags).sum()
            ),
        })

    print("\nPer-rule results:")
    print(pd.DataFrame(rows).to_string(index=False))
    print("\nDevelopment evaluation on 20 selected cards.")


if __name__ == "__main__":
    main()