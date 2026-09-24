import pandas as pd

from app.services.fraud_detection import (
    RULE_COLUMNS,
    flag_suspicious_transactions,
)


def make_transactions():
    return pd.DataFrame({
        "card_number": ["A"] * 6,
        "transaction_timestamp": pd.date_range(
            "2020-01-01 12:00:00", periods=6, freq="min"
        ),
        "amount": [10, 10, 10, 10, 10, 100],
        "merchant_name": ["Store"] * 6,
        "merchant_category": ["groceries"] * 6,
        "merchant_lat": [0.0] * 6,
        "merchant_long": [0.0] * 6,
    })


def test_combined_rules_preserve_flags_and_input():
    df = make_transactions()
    original = df.copy(deep=True)

    result = flag_suspicious_transactions(df)

    assert result["is_suspicious"].tolist() == [
        False, False, False, True, True, True,
    ]
    assert result["velocity_flag"].iloc[-1]
    assert result["spending_anomaly_flag"].iloc[-1]
    assert result["is_suspicious"].equals(
        result[RULE_COLUMNS].any(axis=1)
    )
    assert len(result) == len(df)
    pd.testing.assert_frame_equal(df, original)


def test_fraud_labels_do_not_influence_detection():
    df = make_transactions()

    without_labels = flag_suspicious_transactions(df)
    df["is_fraud"] = True
    with_labels = flag_suspicious_transactions(df)

    columns = RULE_COLUMNS + ["is_suspicious"]
    pd.testing.assert_frame_equal(
        without_labels[columns],
        with_labels[columns],
    )