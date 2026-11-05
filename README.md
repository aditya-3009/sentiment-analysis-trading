# Financial Text Sentiment API

A portfolio project that classifies financial news and market commentary with **FinBERT**, exposes predictions through **FastAPI**, and stores prediction history with **SQLAlchemy**.

> Status: initial implementation scaffold. Benchmark metrics are intentionally not claimed until evaluated on a documented labelled dataset.

## Features
- FinBERT financial sentiment labels: positive, negative, neutral.
- REST API and interactive OpenAPI documentation.
- SQLite by default; PostgreSQL supported through `DATABASE_URL`.
- Prediction history, input validation, and health endpoint.
- Automated API/persistence tests.
- Docker and Docker Compose.

## Architecture
```text
Client -> FastAPI -> FinBERT inference -> sentiment + confidence
                               |
                               v
                     SQLAlchemy -> SQLite/PostgreSQL
```

## Quick start
Python 3.10+ recommended.
```bash
git clone https://github.com/aditya-3009/sentiment-analysis-trading.git
cd sentiment-analysis-trading
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs. The first prediction downloads the configured Hugging Face model (default: `ProsusAI/finbert`).

## Endpoints
- `GET /health`: service health.
- `POST /predict`: classify and persist one text.
- `GET /predictions?limit=20`: retrieve recent predictions.

Example request:
```json
{"text":"The company reported stronger-than-expected quarterly earnings."}
```
The response includes a record ID, original text, sentiment label, confidence score, and timestamp. Numerical examples are illustrative, not measured results.

## Configuration
Copy `.env.example` to `.env`.
| Variable | Default | Purpose |
|---|---|---|
| `MODEL_NAME` | `ProsusAI/finbert` | Hugging Face model |
| `DATABASE_URL` | `sqlite:///./sentiment.db` | SQLAlchemy database |
| `MAX_TEXT_LENGTH` | `5000` | Input character limit |

PostgreSQL URL example: `postgresql+psycopg://user:password@localhost:5432/sentiment`.

## Tests and Docker
```bash
pytest -q
docker compose up --build
```
Tests stub model inference and do not download model weights. Docker Compose starts the API with PostgreSQL.

## Structure
```text
app/
  api/routes.py
  core/config.py
  db/database.py
  db/models.py
  services/sentiment.py
  schemas.py
  main.py
tests/
docs/evaluation.md
Dockerfile
docker-compose.yml
requirements.txt
```

## Evaluation and limitations
See [docs/evaluation.md](docs/evaluation.md). Do not report accuracy, F1, latency, or trading returns until measured on a documented held-out dataset. Confidence scores are not calibrated probabilities. This project does not include live market feeds, brokerage integration, or automated trading, and its predictions are not investment advice.

## License
MIT
