import pandas as pd


def flag_spending_anomaly(
    df: pd.DataFrame,
    multiplier: float = 3.0,
    min_history: int = 5,
) -> pd.DataFrame:
    result = df.sort_values(
        ["card_number", "transaction_timestamp"],
        kind="stable",
    ).copy()

    grouped = result.groupby("card_number")

    result["previous_count"] = grouped.cumcount()

    result["previous_average"] = grouped["amount"].transform(
        lambda amounts: amounts.shift(1).expanding().mean()
    )

    result["spending_anomaly_flag"] = (
        (result["previous_count"] >= min_history)
        & (result["amount"] > multiplier * result["previous_average"])
    )

    return result