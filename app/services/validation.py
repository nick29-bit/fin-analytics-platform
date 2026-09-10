import pandas as pd
from pydantic import ValidationError

from app.schemas.transaction import Transaction


def validate_transactions(df: pd.DataFrame) -> tuple[list[Transaction], pd.DataFrame]:
    valid = []
    errors = []

    for row in df.to_dict(orient="records"):
        try:
            valid.append(Transaction(**row))
        except ValidationError as e:
            errors.append({"row": row, "error": str(e)})

    return valid, pd.DataFrame(errors)


if __name__ == "__main__":
    from app.ingestion.csv_ingestion import load_transactions

    df = load_transactions("data/sample/transactions_sample.csv")
    valid, error_df = validate_transactions(df)

    print(f"Valid: {len(valid)} / {len(df)}")
    if not error_df.empty:
        print(f"Invalid rows: {len(error_df)}")
        print(error_df.head())
