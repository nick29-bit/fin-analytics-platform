import pandas as pd
import pytest

from app.services.dormancy import flag_dormancy


def test_boundary_sorting_and_card_separation():
    df = pd.DataFrame({
        "card_number": ["A", "A", "A", "A", "B"],
        "transaction_timestamp": pd.to_datetime([
            "2020-01-01", "2020-01-30", "2020-02-29", "2020-04-01", "2020-06-01",
        ]),
    })
    result = flag_dormancy(df.sample(frac=1, random_state=42))
    assert result["dormancy_flag"].tolist() == [False, False, True, True, False]
    assert result["days_since_previous"].iloc[1:4].tolist() == [29, 30, 32]
    assert flag_dormancy(df, dormant_days=31)["dormancy_flag"].sum() == 1


def test_invalid_threshold():
    with pytest.raises(ValueError, match="positive"):
        flag_dormancy(pd.DataFrame(), dormant_days=0)
