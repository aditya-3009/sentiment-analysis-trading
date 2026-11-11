"""FastAPI service for financial text sentiment analysis."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from inference import predict_sentiment

app = FastAPI(
    title="Financial Sentiment Analysis API",
    description="Financial text classification using ProsusAI FinBERT.",
    version="1.0.0",
)


class SentimentRequest(BaseModel):
    text: str = Field(min_length=1, max_length=4000)


@app.get("/health")
def health():
    return {"status": "ok", "model": "ProsusAI/finbert", "model_loading": "lazy"}


@app.post("/analyze")
def analyze_sentiment(request: SentimentRequest):
    try:
        return predict_sentiment(request.text)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
