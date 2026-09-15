from fastapi import FastAPI
from app.ingestion.csv_ingestion import load_transactions
from app.services.validation import validate_transactions
from app.services.fraud_detection import flag_suspicious_transactions


app = FastAPI(title="Financial Transaction Analytics API")


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Financial Transaction Analytics API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/transactions")
def get_transactions():
    df = load_transactions("data/sample/transactions_sample.csv")
    valid, _ = validate_transactions(df)
    return valid

@app.get("/transactions/suspicious")
def get_suspicious_transactions():
    df = load_transactions("data/sample/transactions_sample.csv")
    df = flag_suspicious_transactions(df)
    suspicious_df = df[df["is_suspicious"]]
    return suspicious_df.to_dict(orient="records")
