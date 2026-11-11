"""Lazy FinBERT inference with labels read from model metadata."""
from functools import lru_cache
from typing import Dict

MODEL_NAME = "ProsusAI/finbert"

@lru_cache(maxsize=1)
def _load_pipeline():
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise RuntimeError("Install dependencies from requirements.txt to use FinBERT.") from exc
    return pipeline("text-classification", model=MODEL_NAME, tokenizer=MODEL_NAME, top_k=None)

def predict_sentiment(text: str) -> Dict[str, object]:
    if not text or not text.strip():
        raise ValueError("text must not be empty")
    results = _load_pipeline()(text[:4000], truncation=True)
    scores = results[0] if results and isinstance(results[0], list) else results
    score_map = {item["label"].lower(): float(item["score"]) for item in scores}
    sentiment = max(score_map, key=score_map.get)
    return {
        "sentiment": sentiment,
        "confidence": score_map[sentiment],
        "scores": {
            "positive": score_map.get("positive", 0.0),
            "negative": score_map.get("negative", 0.0),
            "neutral": score_map.get("neutral", 0.0),
        },
        "model": MODEL_NAME,
    }
