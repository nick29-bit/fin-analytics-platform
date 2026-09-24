import pandas as pd

from app.ingestion.csv_ingestion import load_transactions

SAMPLE_FRAUD_COUNT = 30
SAMPLE_NON_FRAUD_COUNT = 470

if __name__ == "__main__":
    df = load_transactions("data/raw/fraudTrain.csv")

    fraud_df = df[df["is_fraud"]]
    non_fraud_df = df[~df["is_fraud"]]

    sample_fraud = fraud_df.sample(n=SAMPLE_FRAUD_COUNT, random_state=42)
    sample_non_fraud = non_fraud_df.sample(n=SAMPLE_NON_FRAUD_COUNT, random_state=42)

    sample_df = pd.concat([sample_fraud, sample_non_fraud]).sample(frac=1, random_state=42).reset_index(drop=True)
    sample_df.to_csv("data/sample/transactions_sample.csv", index=False)

    print(f"Wrote {len(sample_df)}-row sample ({SAMPLE_FRAUD_COUNT} fraud, {SAMPLE_NON_FRAUD_COUNT} non-fraud)")
