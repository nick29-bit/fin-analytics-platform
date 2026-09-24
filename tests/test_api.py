import pandas as pd
from fastapi.testclient import TestClient

import app.main as api


client = TestClient(api.app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_transactions():
    response = client.get("/transactions")

    assert response.status_code == 200
    rows = response.json()
    assert len(rows) == 989
    assert {row["card_number"] for row in rows} == {
        "3520550088202337"
    }


def test_suspicious_transactions():
    response = client.get("/transactions/suspicious")

    assert response.status_code == 200
    rows = response.json()
    assert len(rows) == 104
    assert all(row["is_suspicious"] for row in rows)


def test_invalid_data_stops_detection(monkeypatch):
    invalid = pd.read_csv(
        "data/sample/transactions_sample_invalid.csv",
        dtype={"card_number": str},
    )
    monkeypatch.setattr(api, "load_transactions", lambda path: invalid)

    def unexpected_detection(df):
        raise AssertionError("Invalid data reached fraud detection")

    monkeypatch.setattr(
        api, "flag_suspicious_transactions", unexpected_detection
    )

    response = client.get("/transactions/suspicious")

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Dataset contains 5 invalid rows."
    }


def test_nonfinite_diagnostics_become_json_null(monkeypatch):
    def detection_with_nonfinite_values(df):
        result = df.head(1).copy()
        result["is_suspicious"] = True
        result["distance_km"] = float("nan")
        result["required_speed_kmh"] = float("inf")
        result["previous_average"] = float("-inf")
        return result

    monkeypatch.setattr(
        api,
        "flag_suspicious_transactions",
        detection_with_nonfinite_values,
    )

    response = client.get("/transactions/suspicious")

    assert response.status_code == 200
    rows = response.json()
    assert len(rows) == 1
    assert rows[0]["distance_km"] is None
    assert rows[0]["required_speed_kmh"] is None
    assert rows[0]["previous_average"] is None
    assert rows[0]["is_suspicious"] is True