from app.ingestion.csv_ingestion import load_transactions


def test_load_transactions_returns_expected_columns():
    df = load_transactions("data/sample/transactions_sample.csv")

    expected_columns = {
        "transaction_id", "customer_id", "merchant_name", "merchant_category",
        "amount", "currency", "status", "channel", "city",
        "transaction_timestamp", "is_fraud",
    }
    assert set(df.columns) == expected_columns


def test_load_transactions_returns_expected_row_count():
    df = load_transactions("data/sample/transactions_sample.csv")
    assert len(df) == 200

