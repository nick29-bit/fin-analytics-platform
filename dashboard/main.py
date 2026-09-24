from pathlib import Path

import pandas as pd
import streamlit as st

from app.ingestion.csv_ingestion import load_transactions
from app.services.validation import validate_transactions
from app.services.fraud_detection import (
    RULE_COLUMNS,
    flag_suspicious_transactions,
)


st.title("Financial Transaction Analytics — Prototype Dashboard")
st.caption(
    "Development results for one selected card using simulated Kaggle data. "
    "These results do not represent performance across all cards."
)

data_path = (
    Path(__file__).resolve().parents[1]
    / "data/sample/transactions_history.csv"
)

raw = load_transactions(data_path)
valid, errors = validate_transactions(raw)

if not errors.empty:
    st.error(f"Dataset contains {len(errors)} invalid rows.")
    st.stop()

if not valid:
    st.info("No transactions available.")
    st.stop()

df = pd.DataFrame([transaction.model_dump() for transaction in valid])
df = flag_suspicious_transactions(df)

# Preserve detection flags; clean diagnostic values for display.
display_df = df.replace(
    [float("inf"), float("-inf")], float("nan")
)

flagged = df["is_suspicious"]
fraud = df["is_fraud"]

caught = int((flagged & fraud).sum())
false_alarms = int((flagged & ~fraud).sum())
missed = int((~flagged & fraud).sum())

precision = caught / int(flagged.sum()) if flagged.any() else None
recall = caught / int(fraud.sum()) if fraud.any() else None

st.subheader("Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Transactions", len(df))
col2.metric("Total Amount", f"${df['amount'].sum():,.2f}")
col3.metric("Flagged Suspicious", int(flagged.sum()))

st.subheader("Detection Results")
col4, col5, col6, col7 = st.columns(4)
col4.metric("Actual Fraud", int(fraud.sum()))
col5.metric("Caught", caught)
col6.metric("Missed", missed)
col7.metric("False Alarms", false_alarms)

col8, col9 = st.columns(2)
col8.metric(
    "Precision", f"{precision:.1%}" if precision is not None else "N/A"
)
col9.metric(
    "Recall", f"{recall:.1%}" if recall is not None else "N/A"
)

st.subheader("Flags by Rule")
st.caption("A transaction can trigger more than one rule.")
rule_counts = df[RULE_COLUMNS].sum().astype(int)
st.bar_chart(rule_counts)

st.subheader("Suspicious Transactions")
st.dataframe(display_df[flagged])

st.subheader("Actual Fraud Transactions")
actual_fraud = display_df[fraud].copy()
actual_fraud["caught_by_rules"] = actual_fraud["is_suspicious"]
st.dataframe(actual_fraud)

st.subheader("All Transactions")
st.dataframe(display_df)