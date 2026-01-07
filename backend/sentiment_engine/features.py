from db import get_connection

FINANCE_KEYWORDS = {
    "earnings", "revenue", "profit", "loss",
    "shares", "stock", "market", "inflation",
    "investors", "trading"
}


def extract_features(text: str) -> dict:
    tokens = text.split()
    token_count = len(tokens)

    avg_word_length = (
        sum(len(word) for word in tokens) / token_count
        if token_count > 0 else 0
    )

    has_financial_keyword = any(
        word in FINANCE_KEYWORDS for word in tokens
    )

    return {
        "token_count": token_count,
        "avg_word_length": avg_word_length,
        "has_financial_keyword": has_financial_keyword
    }


def extract_and_store_features():
    select_query = """
        SELECT id, cleaned_text
        FROM preprocessed_text
        WHERE id NOT IN (
            SELECT preprocessed_text_id FROM text_features
        );
    """

    insert_query = """
        INSERT INTO text_features
        (preprocessed_text_id, token_count, avg_word_length, has_financial_keyword)
        VALUES (%s, %s, %s, %s);
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(select_query)
            rows = cur.fetchall()

            for row in rows:
                features = extract_features(row["cleaned_text"])
                cur.execute(
                    insert_query,
                    (
                        row["id"],
                        features["token_count"],
                        features["avg_word_length"],
                        features["has_financial_keyword"]
                    )
                )

            conn.commit()


if __name__ == "__main__":
    extract_and_store_features()
    print("Feature extraction completed.")
