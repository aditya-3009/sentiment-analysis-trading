"""PostgreSQL connection helpers. Credentials come from environment variables."""
import os
import psycopg
from psycopg.rows import dict_row

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "sentiment_trading"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
}

def get_connection():
    if not DB_CONFIG["password"]:
        raise RuntimeError("DB_PASSWORD is not set. Configure it in your environment.")
    return psycopg.connect(row_factory=dict_row, **DB_CONFIG)
