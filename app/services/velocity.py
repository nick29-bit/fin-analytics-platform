import pandas as pd


def flag_velocity(
    df: pd.DataFrame,
    window: str = "5min",
    max_transactions: int = 3,
) -> pd.DataFrame:
    result = df.sort_values(
        ["card_number", "transaction_timestamp"],
        kind="stable",
    ).copy()

    counts = []

    for _, card_history in result.groupby("card_number", sort=False):
        timestamps = pd.DatetimeIndex(
            card_history["transaction_timestamp"]
        )
        events = pd.Series(1, index=timestamps)

        card_counts = events.rolling(window, closed="right").sum()
        counts.extend(card_counts.astype(int).tolist())

    result["transactions_in_window"] = counts
    result["velocity_flag"] = (
        result["transactions_in_window"] > max_transactions
    )

    return result