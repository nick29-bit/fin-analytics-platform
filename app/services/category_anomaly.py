import pandas as pd


def flag_category_anomaly(
    df: pd.DataFrame,
    min_history: int = 5,
) -> pd.DataFrame:
    result = df.sort_values(
        ["card_number", "transaction_timestamp"],
        kind="stable",
    ).copy()

    previous_count = result.groupby("card_number").cumcount()

    category_count = result.groupby(
        ["card_number", "merchant_category"]
    ).cumcount()

    result["is_new_category"] = category_count.eq(0)

    result["category_anomaly_flag"] = (
        result["is_new_category"]
        & previous_count.ge(min_history)
    )

    return result
