from pathlib import Path

import numpy as np
import pandas as pd


DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data/raw/fraudTrain.csv"
)


def main():
    total_rows = 0
    missing = None
    seen_ids = set()
    duplicate_ids = 0
    totals = {}

    for chunk in pd.read_csv(
        DATA_PATH,
        chunksize=100_000,
        dtype={"cc_num": str, "trans_num": str},
    ):
        total_rows += len(chunk)

        # Count missing values across all columns.
        counts = chunk.isna().sum()
        missing = counts if missing is None else missing.add(counts)

        # Detect repeated transaction IDs within and across batches.
        for transaction_id in chunk["trans_num"].dropna().tolist():
            if transaction_id in seen_ids:
                duplicate_ids += 1
            else:
                seen_ids.add(transaction_id)

        dates = pd.to_datetime(
            chunk["trans_date_trans_time"],
            format="%Y-%m-%d %H:%M:%S",
            errors="coerce",
        )
        amounts = pd.to_numeric(chunk["amt"], errors="coerce")

        issues = {
            "Invalid timestamps": int(dates.isna().sum()),
            "Invalid amounts": int(
                (~np.isfinite(amounts) | amounts.le(0)).sum()
            ),
        }

        # Latitude must be within ±90; longitude within ±180.
        for column, limit in [
            ("lat", 90),
            ("long", 180),
            ("merch_lat", 90),
            ("merch_long", 180),
        ]:
            values = pd.to_numeric(chunk[column], errors="coerce")
            issues[f"Invalid {column}"] = int(
                (~values.between(-limit, limit)).sum()
            )

        labels = pd.to_numeric(chunk["is_fraud"], errors="coerce")
        issues["Invalid fraud labels"] = int(
            (~labels.isin([0, 1])).sum()
        )

        for name, count in issues.items():
            totals[name] = totals.get(name, 0) + count

        print(f"Checked {total_rows:,} rows", flush=True)

    print(f"\nTotal rows: {total_rows:,}")
    print("Missing values per column:")
    if missing is not None:
        print(missing.to_string())

    print(f"Repeated transaction IDs: {duplicate_ids}")
    for name, count in totals.items():
        print(f"{name}: {count}")

    failed = (
        total_rows == 0
        or duplicate_ids > 0
        or (missing is not None and missing.sum() > 0)
        or any(totals.values())
    )

    print("\nRESULT:", "FAIL" if failed else "PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())