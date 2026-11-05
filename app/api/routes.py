from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db
from app.db.models import Prediction
from app.schemas import PredictionRequest, PredictionResponse
from app.services.sentiment import predict_sentiment

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest, db: Session = Depends(get_db)):
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=422, detail="Text must not be blank.")
    if len(text) > settings.max_text_length:
        raise HTTPException(
            status_code=422,
            detail=f"Text exceeds the {settings.max_text_length} character limit.",
        )

    try:
        sentiment, confidence = predict_sentiment(text)
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Sentiment model is unavailable.") from exc

    record = Prediction(text=text, sentiment=sentiment, confidence=confidence)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/predictions", response_model=list[PredictionResponse])
def list_predictions(
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    statement = select(Prediction).order_by(desc(Prediction.created_at)).limit(limit)
    return list(db.scalars(statement).all())
