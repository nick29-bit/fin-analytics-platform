import pandas as pd

from app.services.category_anomaly import flag_category_anomaly


def test_new_category_history_and_card_separation():
    df = pd.DataFrame({
        "card_number": ["A"] * 8 + ["B"] * 6,
        "transaction_timestamp": pd.date_range(
            "2020-01-01", periods=14, freq="h"
        ),
        "merchant_category": [
            "groceries", "travel", "groceries", "groceries",
            "groceries", "shopping", "shopping", "travel",
            "groceries", "groceries", "groceries", "groceries",
            "groceries", "shopping",
        ],
    })

    result = flag_category_anomaly(
        df.sample(frac=1, random_state=42)
    )

    assert result["is_new_category"].tolist() == [
        True, True, False, False, False, True, False, False,
        True, False, False, False, False, True,
    ]

    assert result["category_anomaly_flag"].tolist() == [
        False, False, False, False, False, True, False, False,
        False, False, False, False, False, True,
    ]