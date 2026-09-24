import pandas as pd

from app.services.unusual_time import flag_unusual_time


def test_history_familiarity_hours_and_card_separation():
    df = pd.DataFrame({
        "card_number": ["A"] * 10 + ["B"] * 6,
        "transaction_timestamp": pd.to_datetime([
            "2020-01-01 01:00", "2020-01-01 02:00", "2020-01-01 03:00",
            "2020-01-01 04:00", "2020-01-01 05:00", "2020-01-02 00:00",
            "2020-01-02 01:00", "2020-01-02 06:00", "2020-01-02 12:00",
            "2020-01-03 02:00",
            "2020-01-01 01:00", "2020-01-01 02:00", "2020-01-01 03:00",
            "2020-01-01 04:00", "2020-01-01 05:00", "2020-01-02 00:00",
        ]),
        "merchant_name": ["known"] * 5 + ["new", "known", "six", "day", "new"]
                         + ["other"] * 5 + ["new"],
    })
    original = df.copy(deep=True)
    result = flag_unusual_time(df.sample(frac=1, random_state=42))
    assert result["unusual_time_flag"].tolist() == (
        [False] * 5 + [True, False, False, False, False] + [False] * 5 + [True]
    )
    pd.testing.assert_frame_equal(df, original)


def test_overnight_window():
    df = pd.DataFrame({
        "card_number": ["A"] * 4,
        "merchant_name": ["a", "b", "c", "d"],
        "transaction_timestamp": pd.to_datetime([
            "2020-01-01 21:00", "2020-01-01 22:00",
            "2020-01-02 05:59", "2020-01-02 06:00",
        ]),
    })
    result = flag_unusual_time(df, start_hour=22, end_hour=6, min_history=0)
    assert result["unusual_time_flag"].tolist() == [False, True, True, False]
