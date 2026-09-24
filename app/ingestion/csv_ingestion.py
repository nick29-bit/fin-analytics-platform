import pandas as pd

COLUMN_MAPPING = {
    "trans_num": "transaction_id",
    "cc_num": "card_number",
    "merchant": "merchant_name",
    "category": "merchant_category",
    "amt": "amount",
    "trans_date_trans_time": "transaction_timestamp",
    "lat": "cardholder_lat",
    "long": "cardholder_long",
    "merch_lat": "merchant_lat",
    "merch_long": "merchant_long",
    "is_fraud": "is_fraud",
}


def load_transactions(path: str, nrows: int | None = None) -> pd.DataFrame:
    """Load raw Kaggle or normalized CSVs, retaining invalid values for validation."""
    columns = pd.read_csv(path, nrows=0).columns
    raw_columns = list(COLUMN_MAPPING)
    normalized_columns = list(COLUMN_MAPPING.values())
    if set(raw_columns).issubset(columns):
        selected_columns = raw_columns
        card_column = "cc_num"
    elif set(normalized_columns).issubset(columns):
        selected_columns = normalized_columns
        card_column = "card_number"
    else:
        raise ValueError("CSV must contain all required Kaggle or normalized transaction columns")

    df = pd.read_csv(
        path, nrows=nrows, usecols=selected_columns, dtype={card_column: str}
    )
    df = df[selected_columns].rename(columns=COLUMN_MAPPING)

    timestamps = pd.to_datetime(df["transaction_timestamp"], errors="coerce")
    if timestamps.notna().all():
        df["transaction_timestamp"] = timestamps
    else:
        df["transaction_timestamp"] = timestamps.astype(object).where(
            timestamps.notna(), df["transaction_timestamp"]
        )

    # Avoid astype(bool): even an invalid nonempty string becomes True.
    boolean_values = {"0": False, "1": True, "False": False, "True": True}
    df["is_fraud"] = df["is_fraud"].map(
        lambda value: boolean_values.get(str(value), value)
    )

    return df
