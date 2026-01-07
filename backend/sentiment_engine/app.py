from fastapi import FastAPI
from pydantic import BaseModel
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = FastAPI(title="Sentiment Analysis Engine")

analyzer = SentimentIntensityAnalyzer()


class SentimentRequest(BaseModel):
    text: str


class SentimentResponse(BaseModel):
    sentiment: str
    score: float


def label_sentiment(score: float) -> str:
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    return "neutral"


@app.post("/analyze", response_model=SentimentResponse)
def analyze_sentiment(request: SentimentRequest):
    scores = analyzer.polarity_scores(request.text)
    compound = scores["compound"]
    sentiment = label_sentiment(compound)

    return SentimentResponse(
        sentiment=sentiment,
        score=compound
    )
