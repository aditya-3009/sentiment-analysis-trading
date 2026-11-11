"""Batch FinBERT scoring for rows in the preprocessed_text table."""
from db import get_connection
from inference import predict_sentiment


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
                prediction = predict_sentiment(row["cleaned_text"])
                cur.execute(
                    insert_query,
                    (row["id"], prediction["sentiment"], prediction["confidence"]),
                )
        conn.commit()


if __name__ == "__main__":
    analyze_and_store_sentiment()
    print("FinBERT sentiment analysis completed.")
