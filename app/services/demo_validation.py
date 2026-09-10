from app.ingestion.csv_ingestion import load_transactions
from app.services.validation import validate_transactions

print("=== Clean sample ===")
df_clean = load_transactions("data/sample/transactions_sample.csv")
valid, errors = validate_transactions(df_clean)
print(f"Valid: {len(valid)} / {len(df_clean)}")
print()
print("=== Invalid sample ===")
df_invalid = load_transactions("data/sample/transactions_sample_invalid.csv")
valid_bad, errors_bad = validate_transactions(df_invalid)
print(f"Valid: {len(valid_bad)} / {len(df_invalid)}")
print()
print("Errors found:")
for err in errors_bad["error"]:
    print("-", err)
