import csv
from db import get_connection


def ingest_csv(path: str):
    query = """
        INSERT INTO raw_text_data (source, content)
        VALUES (%s, %s);
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cur.execute(query, (row["source"], row["content"]))
            conn.commit()


if __name__ == "__main__":
    ingest_csv("data/raw/news.csv")
    print("CSV ingestion completed.")
