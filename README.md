# Financial Transaction Analytics Platform

An end-to-end Python backend project that ingests financial transaction data, validates it, runs analytics and fraud-oriented rules, exposes it via a REST API, and (eventually) visualizes it on a dashboard.

## Build approach

This project is being built in three stages:

1. **Prototype** (current stage) — CSV data, Pandas, Pydantic validation, FastAPI, Streamlit, pytest.
2. **Production-style** — PostgreSQL, SQLAlchemy, Alembic migrations, service/repository layers, JWT auth, Redis, Celery, Docker, GitHub Actions, monitoring.
3. **Optional cloud deployment** — AWS (ECR, ECS/EC2, RDS, S3, CloudWatch, Secrets Manager).

Default rule: fully build and understand the prototype before adding production infrastructure.

## Project structure

app/
├── main.py          # FastAPI application entrypoint
├── schemas/         # Pydantic models (data validation)
├── ingestion/        # Code that loads transaction data
├── services/        # Business logic and analytics
└── utils/           # Shared helper functions
dashboard/           # Streamlit dashboard (later)
data/
├── raw/             # Original, untouched data
├── processed/       # Cleaned/transformed data
└── sample/          # Small example files safe to commit
scripts/             # One-off utility scripts (e.g. synthetic data generator)
tests/               # pytest test suite



## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Generate sample data

python scripts/generate_transactions.py
Run the API

uvicorn app.main:app --reload
API root: http://127.0.0.1:8000/
Health check: http://127.0.0.1:8000/health
Interactive docs: http://127.0.0.1:8000/docs
Status
Currently in Version 1 (Prototype). FastAPI skeleton and health check are live. Data ingestion, validation, and analytics endpoints are in progress.