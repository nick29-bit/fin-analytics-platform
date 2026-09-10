import pandas as pd

AMOUNT_THRESHOLD = 150
DECLINED_THRESHOLD = 75


def flag_suspicious_transactions(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    large_amount = df["amount"] > AMOUNT_THRESHOLD
    declined_and_moderate = (df["status"] == "declined") & (df["amount"] > DECLINED_THRESHOLD)
    df["is_suspicious"] = large_amount | declined_and_moderate
    return df

def evaluate_against_ground_truth(df: pd.DataFrame) -> None:
    flagged = df["is_suspicious"]
    actual_fraud = df["is_fraud"]

    true_positives = (flagged & actual_fraud).sum()
    false_positives = (flagged & ~actual_fraud).sum()
    false_negatives = (~flagged & actual_fraud).sum()

    print(f"Flagged as suspicious: {flagged.sum()} / {len(df)}")
    print(f"Actual fraud in data: {actual_fraud.sum()}")
    print(f"Correctly caught (true positives): {true_positives}")
    print(f"Flagged but not fraud (false positives): {false_positives}")
    print(f"Missed fraud (false negatives): {false_negatives}")


if __name__ == "__main__":
    from app.ingestion.csv_ingestion import load_transactions

    df = load_transactions("data/sample/transactions_sample.csv")
    df = flag_suspicious_transactions(df)
    evaluate_against_ground_truth(df)
