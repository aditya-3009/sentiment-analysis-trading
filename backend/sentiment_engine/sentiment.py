from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from db import get_connection

MODEL_NAME = "ProsusAI/finbert"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

LABELS = ["negative", "neutral", "positive"]


def analyze_and_store_sentiment():
    select_query = """
        SELECT id, cleaned_text
        FROM preprocessed_text
        WHERE id NOT IN (
            SELECT preprocessed_text_id FROM sentiment_scores
        );
    """

    insert_query = """
        INSERT INTO sentiment_scores
        (preprocessed_text_id, sentiment, score)
        VALUES (%s, %s, %s);
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(select_query)
            rows = cur.fetchall()

            for row in rows:
                inputs = tokenizer(
                    row["cleaned_text"],
                    return_tensors="pt",
                    truncation=True,
                    padding=True,
                    max_length=128
                )

                with torch.no_grad():
                    outputs = model(**inputs)

                probs = torch.nn.functional.softmax(outputs.logits, dim=1)
                confidence, predicted_class = torch.max(probs, dim=1)

                sentiment = LABELS[predicted_class.item()]
                score = confidence.item()

                cur.execute(
                    insert_query,
                    (row["id"], sentiment, score)
                )

            conn.commit()


if __name__ == "__main__":
    analyze_and_store_sentiment()
    print("BERT-based sentiment analysis completed.")
