# Financial Sentiment Engine

Financial text classification using **ProsusAI FinBERT**, FastAPI, and an optional PostgreSQL batch pipeline.

## Features
- Positive, negative, and neutral sentiment classification.
- Per-class confidence scores.
- FastAPI endpoints: `GET /health`, `POST /analyze`.
- Lazy FinBERT loading: model weights are downloaded on the first prediction.
- PostgreSQL batch scoring for preprocessed news.
- Environment-based database credentials.
- Tests that mock model inference and do not download model weights.

## Run locally

From this directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000/docs`. The first call to `POST /analyze` downloads the FinBERT weights from Hugging Face.

Example JSON:
```json
{"text":"The company reported stronger-than-expected quarterly revenue."}
```

## Tests
```powershell
pytest -q
```

The tests do not require downloaded model weights.

## PostgreSQL batch pipeline

Apply `database/schema.sql` to the `sentiment_trading` database, set `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT`, then run these from the repository root:

```powershell
python backend/sentiment_engine/ingest_csv.py
python backend/sentiment_engine/preprocessing.py
python backend/sentiment_engine/sentiment.py
```

## Research limitations

Sentiment classification measures language tone, not future market direction. Experimental BUY/SELL/HOLD rules are not investment advice. Credible strategy evaluation requires time-aligned data, leakage controls, baselines, transaction costs, and out-of-sample validation.
