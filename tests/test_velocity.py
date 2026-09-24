import pandas as pd

from app.services.velocity import flag_velocity


def test_velocity_window_and_card_separation():
    df = pd.DataFrame({
        "card_number": ["A", "A", "A", "A", "A", "B"],
        "transaction_timestamp": pd.to_datetime([
            "2020-01-01 10:00:00",
            "2020-01-01 10:01:00",
            "2020-01-01 10:02:00",
            "2020-01-01 10:03:00",
            "2020-01-01 10:05:00",
            "2020-01-01 10:03:00",
        ]),
    })

    # Shuffle input to verify the rule sorts transactions itself.
    df = df.sample(frac=1, random_state=42)
    result = flag_velocity(df)

    assert result["transactions_in_window"].tolist() == [
        1, 2, 3, 4, 4, 1,
    ]
    assert result["velocity_flag"].tolist() == [
        False, False, False, True, True, False,
    ]