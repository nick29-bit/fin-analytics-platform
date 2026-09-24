# Financial Transaction Analytics Platform

A Python prototype that ingests transaction data, validates it, applies
six fraud-detection rules, and presents results through FastAPI and Streamlit.

## Build approach

1. **Prototype (current)** — CSV, pandas, Pydantic, FastAPI, Streamlit, pytest.
2. **Production-style (planned)** — PostgreSQL, migrations, authentication,
   background jobs, Docker, CI, and monitoring.
3. **Optional cloud deployment (planned)** — AWS infrastructure.

Build and understand the prototype before adding production infrastructure.

## Project structure

```text
app/
├── main.py          # FastAPI endpoints
├── schemas/         # Transaction schema
├── ingestion/       # CSV loading and column mapping
├── services/        # Validation and fraud rules
└── utils/           # Shared helpers
dashboard/           # Streamlit dashboard
data/
├── raw/             # Original downloaded data
├── processed/       # Reserved for transformed outputs
└── sample/          # Development samples and test fixtures
scripts/             # Data preparation, quality checks, and evaluation
tests/               # Automated tests
```

## Setup

Run commands from the project root:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

## Data

The project uses the Kaggle Credit Card Transactions Fraud Detection
dataset, published by kartik2112 and generated with Sparkov.
It contains simulated transactions, not actual customer card activity.

Download and extract the dataset from:
https://www.kaggle.com/datasets/kartik2112/fraud-detection

Place `fraudTrain.csv` in `data/raw/`.

Data used during development:

| File | Contents |
|---|---|
| `data/raw/fraudTrain.csv` | 1,296,675 transactions across 983 cards |
| `data/sample/transactions_sample.csv` | 500 selected transactions: 30 fraud, 470 non-fraud |
| `data/sample/transactions_history.csv` | 989 transactions for one selected card, including 19 fraud |
| `data/sample/transactions_sample_invalid.csv` | Five deliberately invalid rows for validation tests |

The 500-row sample deliberately oversamples fraud and does not preserve
complete card histories. The API and dashboard use the 989-row history file.

The old synthetic generator is retained for reference and is not part
of the current workflow.

## Processing flow

CSV → column mapping and type conversion → validation → fraud rules → results.

The internal Transaction schema contains 11 fields. Ingestion supports
both raw Kaggle columns and normalized sample columns.

The API and dashboard stop processing if validation finds invalid rows.
The evaluation script assumes the raw dataset has passed the separate
data-quality checks.

## Fraud rules

| Rule | Default behavior |
|---|---|
| Velocity | Flags the fourth or later transaction within five minutes |
| Impossible travel | Flags required speed above 900 km/h between successive merchant locations |
| Spending anomaly | Flags amounts above three times the previous average, after five prior transactions |
| Category anomaly | Flags an unseen category after five prior transactions |
| Dormancy | Flags activity after a gap of at least 30 days |
| Unusual time | Flags an unseen merchant from midnight to before 6 a.m., after five prior transactions |

Histories are evaluated separately per card in chronological order.
A transaction is suspicious if any rule flags it.

`is_suspicious` is the rules' output.
`is_fraud` is the dataset label used for evaluation.

Thresholds are development assumptions. Merchant coordinates are a proxy
for transaction location, and unusual-time detection uses the recorded
timestamp hour without timezone conversion.

## Run data-quality checks

```bash
python -m scripts.check_data_quality
```

Checks the full raw file in batches for missing values, repeated transaction
IDs, invalid timestamps, nonpositive/nonfinite amounts, coordinate ranges,
and fraud labels outside 0 or 1.

The checked training file passed these checks. A pass applies only to
these checks; it does not guarantee every aspect of data quality.

## Evaluate fraud rules

```bash
python -m scripts.evaluate_fraud
```

Selects 20 cards using random seed 42 without using fraud labels for
selection, retains their available histories, and reports combined and
per-rule performance.

Development baseline with the current rules:

| Metric | One selected card | 20 selected cards |
|---|---:|---:|
| Transactions | 989 | 26,467 |
| Actual fraud | 19 | 165 |
| Flagged transactions | 104 | 3,694 |
| Fraud caught | 16 | 121 |
| False alarms | 88 | 3,573 |
| Fraud missed | 3 | 44 |
| Precision | 15.4% | 3.3% |
| Recall | 84.2% | 73.3% |

Precision measures fraud among flagged transactions.
Recall measures the share of labeled fraud caught.

These are development results, not held-out performance estimates.
The false-alarm burden is high; the rules are not production-ready.

## Run the API

```bash
python -m uvicorn app.main:app --reload
```

- Root: http://127.0.0.1:8000/
- Health: http://127.0.0.1:8000/health
- Transactions: http://127.0.0.1:8000/transactions
- Suspicious transactions: http://127.0.0.1:8000/transactions/suspicious
- Interactive documentation: http://127.0.0.1:8000/docs

Missing and infinite diagnostic values are returned as JSON null.

## Run the dashboard

```bash
python -m streamlit run dashboard/main.py
```

Open http://localhost:8501.

The dashboard reads the CSV directly and does not require the API server.
It shows transaction totals, fraud metrics, rule counts, and transaction tables.

## Run tests

```bash
python -m pytest -q
```

Tests cover ingestion, validation, individual rules, combined detection,
and API behavior, including JSON handling.

Some API tests assert the current one-card sample counts. Review those
expectations when changing the data source or rule behavior.

## Remaining work

- Reserve separate evaluation data before tuning thresholds.
- Reduce false alarms and assess performance across more cards.
- Improve loading and computation efficiency before expanding the live app.
- Complete review and the branch → PR → merge workflow.