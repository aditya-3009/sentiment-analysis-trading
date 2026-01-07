from db import get_connection


def generate_signal(sentiment: str, score: float) -> str:
    if sentiment == "positive" and score >= 0.6:
        return "BUY"
    if sentiment == "negative" and score >= 0.6:
        return "SELL"
    return "HOLD"


def generate_and_store_signals():
    select_query = """
        SELECT id, sentiment, score
        FROM sentiment_scores
        WHERE id NOT IN (
            SELECT sentiment_score_id FROM trading_signals
        );
    """

    insert_query = """
        INSERT INTO trading_signals (sentiment_score_id, signal)
        VALUES (%s, %s);
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(select_query)
            rows = cur.fetchall()

            for row in rows:
                signal = generate_signal(row["sentiment"], row["score"])
                cur.execute(
                    insert_query,
                    (row["id"], signal)
                )

            conn.commit()


if __name__ == "__main__":
    generate_and_store_signals()
    print("Trading signals generated.")
