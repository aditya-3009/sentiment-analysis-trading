from functools import lru_cache

from transformers import pipeline

from app.core.config import settings


@lru_cache(maxsize=1)
def _classifier():
    return pipeline(
        task="text-classification",
        model=settings.model_name,
        tokenizer=settings.model_name,
        top_k=1,
    )


def predict_sentiment(text: str) -> tuple[str, float]:
    """Return the top FinBERT label and its confidence score."""
    result = _classifier()(text, truncation=True)[0]
    label = str(result["label"]).lower()
    if label not in {"positive", "negative", "neutral"}:
        raise ValueError(f"Unexpected sentiment label from model: {label}")
    return label, float(result["score"])


def model_is_loaded() -> bool:
    return _classifier.cache_info().currsize > 0
