import pytest
from fastapi.testclient import TestClient
import app as api
from inference import predict_sentiment

def test_predict_rejects_blank_text():
    with pytest.raises(ValueError):
        predict_sentiment("   ")

def test_health_endpoint():
    response = TestClient(api.app).get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_analyze_endpoint_uses_model(monkeypatch):
    def fake_predict(text):
        return {
            "sentiment": "positive", "confidence": 0.91,
            "scores": {"positive": 0.91, "negative": 0.03, "neutral": 0.06},
            "model": "ProsusAI/finbert",
        }
    monkeypatch.setattr(api, "predict_sentiment", fake_predict)
    response = TestClient(api.app).post("/analyze", json={"text": "Revenue increased."})
    assert response.status_code == 200
    assert response.json()["sentiment"] == "positive"

def test_analyze_endpoint_rejects_empty_text():
    response = TestClient(api.app).post("/analyze", json={"text": ""})
    assert response.status_code == 422
