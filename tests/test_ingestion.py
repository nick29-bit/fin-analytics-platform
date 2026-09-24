from app.ingestion.csv_ingestion import load_transactions


def test_load_transactions_returns_expected_columns():
    df = load_transactions("data/sample/transactions_sample.csv")

    expected_columns = {
        "transaction_id", "card_number", "merchant_name", "merchant_category",
        "amount", "cardholder_lat", "cardholder_long", "merchant_lat", "merchant_long",
        "transaction_timestamp", "is_fraud",
    }
    assert set(df.columns) == expected_columns


def test_load_transactions_returns_expected_row_count():
    df = load_transactions("data/sample/transactions_sample.csv")
    assert len(df) == 500



def test_raw_and_normalized_formats_match(tmp_path):
    from app.ingestion.csv_ingestion import COLUMN_MAPPING
    import pandas as pd

    normalized = pd.read_csv("data/sample/transactions_sample.csv", nrows=2,
                             dtype={"card_number": str})
    normalized.loc[0, "card_number"] = "00123456789"
    normalized["is_fraud"] = [False, True]
    raw = normalized.rename(columns={v: k for k, v in COLUMN_MAPPING.items()})
    raw["is_fraud"] = [0, 1]
    raw["unused_column"] = "ignored"
    raw_path = tmp_path / "raw.csv"
    normalized_path = tmp_path / "normalized.csv"
    raw.to_csv(raw_path, index=False)
    normalized.to_csv(normalized_path, index=False)

    actual = load_transactions(raw_path)
    pd.testing.assert_frame_equal(actual, load_transactions(normalized_path))
    assert actual.loc[0, "card_number"] == "00123456789"
    assert actual["is_fraud"].tolist() == [False, True]
    assert len(load_transactions(raw_path, nrows=1)) == 1


def test_missing_columns_raise_clear_error(tmp_path):
    import pytest

    path = tmp_path / "incomplete.csv"
    path.write_text("amt,is_fraud\n25,0\n")
    with pytest.raises(ValueError, match="required Kaggle or normalized"):
        load_transactions(path)
