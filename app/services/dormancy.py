import pandas as pd


def flag_dormancy(df: pd.DataFrame, dormant_days: float = 30) -> pd.DataFrame:
    """Flag reactivation after at least dormant_days without an observed transaction."""
    if dormant_days <= 0:
        raise ValueError("dormant_days must be positive")
    result = df.sort_values(
        ["card_number", "transaction_timestamp"], kind="stable"
    ).copy()
    previous = result.groupby("card_number")["transaction_timestamp"].shift(1)
    result["days_since_previous"] = (
        result["transaction_timestamp"] - previous
    ).dt.total_seconds() / 86400
    result["dormancy_flag"] = result["days_since_previous"].ge(dormant_days)
    return result
