from db import get_connection

def test_connection():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            print(cur.fetchone())

if __name__ == "__main__":
    test_connection()
