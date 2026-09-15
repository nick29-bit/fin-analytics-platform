import pandas as pd

from app.services.fraud_detection import flag_suspicious_transactions


def test_large_amount_is_flagged():
    df = pd.DataFrame([{"amount": 200, "status": "approved"}])
    result = flag_suspicious_transactions(df)
    assert result["is_suspicious"].iloc[0] == True


def test_small_approved_amount_is_not_flagged():
    df = pd.DataFrame([{"amount": 20, "status": "approved"}])
    result = flag_suspicious_transactions(df)
    assert result["is_suspicious"].iloc[0] == False


def test_declined_moderate_amount_is_flagged():
    df = pd.DataFrame([{"amount": 100, "status": "declined"}])
    result = flag_suspicious_transactions(df)
    assert result["is_suspicious"].iloc[0] == True


def test_declined_small_amount_is_not_flagged():
    df = pd.DataFrame([{"amount": 50, "status": "declined"}])
    result = flag_suspicious_transactions(df)
    assert result["is_suspicious"].iloc[0] == False
