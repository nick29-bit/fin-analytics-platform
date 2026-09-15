import streamlit as st

from app.ingestion.csv_ingestion import load_transactions
from app.services.validation import validate_transactions
from app.services.fraud_detection import flag_suspicious_transactions

st.title("Financial Transaction Analytics — Prototype Dashboard")

df = load_transactions("data/sample/transactions_sample.csv")
valid, error_df = validate_transactions(df)
df = flag_suspicious_transactions(df)


st.subheader("All Transactions")
st.dataframe(df)
st.subheader("Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Transactions", len(df))
col2.metric("Total Amount", f"${df['amount'].sum():,.2f}")
col3.metric("Flagged Suspicious", int(df["is_suspicious"].sum()))

st.subheader("Suspicious Transactions")
st.dataframe(df[df["is_suspicious"]])
