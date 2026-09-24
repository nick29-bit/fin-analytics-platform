import pandas as pd


def flag_unusual_time(
    df: pd.DataFrame,
    start_hour: int = 0,
    end_hour: int = 6,
    min_history: int = 5,
) -> pd.DataFrame:
    """Flag unseen merchants during [start_hour, end_hour), using source clock time.

    Overnight windows (e.g. 22 to 6) are supported. Merchant familiarity is
    based on name, separately per card, and uses only preceding rows.
    """
    if not (0 <= start_hour < 24 and 0 <= end_hour <= 24):
        raise ValueError("Hours must satisfy 0 <= start_hour < 24 and 0 <= end_hour <= 24")
    if start_hour == end_hour:
        raise ValueError("Start and end hours must differ")
    if min_history < 0:
        raise ValueError("min_history must be nonnegative")

    result = df.sort_values(
        ["card_number", "transaction_timestamp"], kind="stable"
    ).copy()
    previous_count = result.groupby("card_number").cumcount()
    result["is_new_merchant"] = result.groupby(
        ["card_number", "merchant_name"]
    ).cumcount().eq(0)
    hour = result["transaction_timestamp"].dt.hour
    if start_hour < end_hour:
        result["is_unusual_hour"] = hour.ge(start_hour) & hour.lt(end_hour)
    else:
        result["is_unusual_hour"] = hour.ge(start_hour) | hour.lt(end_hour)
    result["unusual_time_flag"] = (
        result["is_new_merchant"]
        & result["is_unusual_hour"]
        & previous_count.ge(min_history)
    )
    return result
