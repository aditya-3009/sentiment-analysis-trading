from app.services import sentiment


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_persists_result(client, monkeypatch):
    monkeypatch.setattr(sentiment, "predict_sentiment", lambda text: ("positive", 0.97))
    response = client.post(
        "/predict",
        json={"text": "The company reported record quarterly revenue."},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["sentiment"] == "positive"
    assert body["confidence"] == 0.97
    assert body["id"] == 1

    history = client.get("/predictions")
    assert history.status_code == 200
    assert len(history.json()) == 1
    assert history.json()[0]["text"] == "The company reported record quarterly revenue."


def test_rejects_blank_text(client):
    response = client.post("/predict", json={"text": "   "})
    assert response.status_code == 422


def test_rejects_missing_text(client):
    response = client.post("/predict", json={})
    assert response.status_code == 422
