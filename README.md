# Financial Sentiment Analysis & Trading Research

An experimental financial-news sentiment analysis project using **ProsusAI FinBERT**, **FastAPI**, and **PostgreSQL**. It includes a batch-processing pipeline and exploratory signal/backtesting modules.

## Current capabilities
- Financial text sentiment classification: positive, negative, or neutral.
- REST API with per-class confidence scores.
- CSV ingestion and PostgreSQL-backed batch processing.
- Text preprocessing, feature extraction, and data-quality checks.
- Exploratory signal-generation and backtesting modules.
- Environment-based database configuration.
- Automated tests that do not download FinBERT model weights.

## Quick start
See [backend/sentiment_engine/README.md](backend/sentiment_engine/README.md) for installation, API usage, and test instructions.

Run from `backend/sentiment_engine`:
```bash
uvicorn app:app --reload
```

Endpoints: `GET /health`, `POST /analyze`. Interactive docs: `/docs`.

## Project layout
- `backend/sentiment_engine/`: inference API and batch pipeline
- `data/raw/`: sample news and price CSVs
- `database/schema.sql`: PostgreSQL schema
- `docker/`: container build
- `docs/`: architecture notes
- `.github/workflows/`: automated tests

## Research disclaimer
This is an educational/research prototype, not an investment system. Sentiment labels do not reliably predict future returns. Trading rules require rigorous out-of-sample validation, transaction costs, and risk controls before real-world use.
