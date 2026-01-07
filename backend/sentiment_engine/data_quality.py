from db import get_connection


def check_quality(text: str) -> dict:
    length = len(text)

    return {
        "is_empty": length == 0,
        "is_too_short": length < 10,
        "is_too_long": length > 500
    }


def run_quality_checks():
    select_query = """
        SELECT id, cleaned_text
        FROM preprocessed_text
        WHERE id NOT IN (
            SELECT preprocessed_text_id FROM data_quality_checks
        );
    """

    insert_query = """
        INSERT INTO data_quality_checks
        (preprocessed_text_id, is_empty, is_too_short, is_too_long)
        VALUES (%s, %s, %s, %s);
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(select_query)
            rows = cur.fetchall()

            for row in rows:
                flags = check_quality(row["cleaned_text"])
                cur.execute(
                    insert_query,
                    (
                        row["id"],
                        flags["is_empty"],
                        flags["is_too_short"],
                        flags["is_too_long"]
                    )
                )

            conn.commit()


if __name__ == "__main__":
    run_quality_checks()
    print("Data quality checks completed.")
