import pandas as pd

from app.services.spending_anomaly import flag_spending_anomaly


def test_spending_history_threshold_and_card_separation():
    df = pd.DataFrame({
        "card_number": ["A"] * 7 + ["B"],
        "transaction_timestamp": pd.date_range(
            "2020-01-01", periods=8, freq="h"
        ),
        "amount": [10, 10, 10, 10, 10, 30, 41, 1000],
    })

    result = flag_spending_anomaly(
        df.sample(frac=1, random_state=42)
    )

    assert result["previous_count"].tolist() == [
        0, 1, 2, 3, 4, 5, 6, 0,
    ]
    assert result["spending_anomaly_flag"].tolist() == [
        False, False, False, False,
        False, False, True, False,
    ]


def test_insufficient_history_prevents_flag():
    df = pd.DataFrame({
        "card_number": ["A", "A"],
        "transaction_timestamp": pd.to_datetime([
            "2020-01-01 10:00:00",
            "2020-01-01 11:00:00",
        ]),
        "amount": [10, 1000],
    })

    result = flag_spending_anomaly(df)

    assert not result["spending_anomaly_flag"].any()