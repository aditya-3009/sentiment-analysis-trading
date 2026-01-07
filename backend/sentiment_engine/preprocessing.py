import re
import string
from db import get_connection


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text


def preprocess_and_store():
    select_query = """
        SELECT id, content
        FROM raw_text_data
        WHERE id NOT IN (
            SELECT raw_text_id FROM preprocessed_text
        );
    """

    insert_query = """
        INSERT INTO preprocessed_text (raw_text_id, cleaned_text)
        VALUES (%s, %s);
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(select_query)
            rows = cur.fetchall()

            for row in rows:
                cleaned = clean_text(row["content"])
                cur.execute(insert_query, (row["id"], cleaned))

            conn.commit()


if __name__ == "__main__":
    preprocess_and_store()
    print("Preprocessing completed.")
