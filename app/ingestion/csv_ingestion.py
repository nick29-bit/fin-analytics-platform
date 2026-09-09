import pandas as pd


def load_transactions(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


if __name__ == "__main__":
    df = load_transactions("data/raw/transactions.csv")
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print(df.head())
    print(df.dtypes)
