import json
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException

from app.ingestion.csv_ingestion import load_transactions
from app.services.validation import validate_transactions
from app.services.fraud_detection import flag_suspicious_transactions


app = FastAPI(title="Financial Transaction Analytics API")

DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data/sample/transactions_history.csv"
)


def load_validated_transactions():
    df = load_transactions(DATA_PATH)
    valid, errors = validate_transactions(df)

    if not errors.empty:
        raise HTTPException(
            status_code=500,
            detail=f"Dataset contains {len(errors)} invalid rows.",
        )

    return valid


@app.get("/")
def read_root():
    return {
        "status": "ok",
        "message": "Financial Transaction Analytics API is running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/transactions")
def get_transactions():
    return load_validated_transactions()


@app.get("/transactions/suspicious")
def get_suspicious_transactions():
    valid = load_validated_transactions()

    if not valid:
        return []

    df = pd.DataFrame([
        transaction.model_dump() for transaction in valid
    ])
    result = flag_suspicious_transactions(df)
    suspicious = result[result["is_suspicious"]]

    safe = suspicious.replace(
        [float("inf"), float("-inf")],
        float("nan"),
    )

    return json.loads(
        safe.to_json(orient="records", date_format="iso")
    )