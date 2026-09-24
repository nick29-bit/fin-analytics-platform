import pandas as pd

from app.services.velocity import flag_velocity
from app.services.impossible_travel import flag_impossible_travel
from app.services.spending_anomaly import flag_spending_anomaly
from app.services.category_anomaly import flag_category_anomaly
from app.services.dormancy import flag_dormancy
from app.services.unusual_time import flag_unusual_time


RULE_COLUMNS = [
    "velocity_flag",
    "impossible_travel_flag",
    "spending_anomaly_flag",
    "category_anomaly_flag",
    "dormancy_flag",
    "unusual_time_flag",
]


def flag_suspicious_transactions(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    for rule in [
        flag_velocity,
        flag_impossible_travel,
        flag_spending_anomaly,
        flag_category_anomaly,
        flag_dormancy,
        flag_unusual_time,
    ]:
        result = rule(result)

    result["is_suspicious"] = result[RULE_COLUMNS].any(axis=1)
    return result


def evaluate_against_ground_truth(df: pd.DataFrame) -> None:
    flagged = df["is_suspicious"]
    actual_fraud = df["is_fraud"]

    true_positives = (flagged & actual_fraud).sum()
    false_positives = (flagged & ~actual_fraud).sum()
    false_negatives = (~flagged & actual_fraud).sum()

    print(f"Flagged as suspicious: {flagged.sum()} / {len(df)}")
    print(f"Actual fraud in data: {actual_fraud.sum()}")
    print(f"Correctly caught: {true_positives}")
    print(f"False alarms: {false_positives}")
    print(f"Missed fraud: {false_negatives}")


if __name__ == "__main__":
    from app.ingestion.csv_ingestion import load_transactions

    df = load_transactions("data/sample/transactions_history.csv")
    df = flag_suspicious_transactions(df)
    evaluate_against_ground_truth(df)