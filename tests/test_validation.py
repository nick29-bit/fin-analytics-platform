from app.ingestion.csv_ingestion import load_transactions
from app.services.validation import validate_transactions


def test_valid_sample_all_pass():
    df = load_transactions("data/sample/transactions_sample.csv")
    valid, errors = validate_transactions(df)

    assert len(valid) == 500
    assert errors.empty


def test_invalid_sample_all_fail():
    df = load_transactions("data/sample/transactions_sample_invalid.csv")
    valid, errors = validate_transactions(df)

    assert len(valid) == 0
    assert len(errors) == 5

    expected_fields = ["amount", "amount", "transaction_timestamp", "merchant_lat", "is_fraud"]
    for error, field in zip(errors["error"], expected_fields):
        assert "1 validation error for Transaction" in error
        assert f"\n{field}\n" in error
