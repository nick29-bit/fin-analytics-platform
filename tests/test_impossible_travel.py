import pandas as pd
import pytest

from app.services.impossible_travel import (
    flag_impossible_travel,
    haversine_km,
)


def test_known_distances():
    assert haversine_km(0, 0, 0, 0) == 0
    assert haversine_km(0, 0, 0, 1) == pytest.approx(
        111.195, abs=0.001
    )


def test_travel_speed_and_card_separation():
    df = pd.DataFrame({
        "card_number": ["A", "A", "A", "B"],
        "transaction_timestamp": pd.to_datetime([
            "2020-01-01 10:00:00",
            "2020-01-01 11:00:00",
            "2020-01-01 11:01:00",
            "2020-01-01 11:02:00",
        ]),
        "merchant_lat": [0, 0, 0, 0],
        "merchant_long": [0, 1, 2, 50],
    })

    result = flag_impossible_travel(
        df.sample(frac=1, random_state=42)
    )

    assert result["impossible_travel_flag"].tolist() == [
        False, False, True, False,
    ]


def test_same_timestamp():
    df = pd.DataFrame({
        "card_number": ["A", "A", "A"],
        "transaction_timestamp": pd.to_datetime([
            "2020-01-01 10:00:00",
            "2020-01-01 10:00:00",
            "2020-01-01 10:00:00",
        ]),
        "merchant_lat": [0, 0, 0],
        "merchant_long": [0, 0, 1],
    })

    result = flag_impossible_travel(df)

    assert result["impossible_travel_flag"].tolist() == [
        False, False, True,
    ]