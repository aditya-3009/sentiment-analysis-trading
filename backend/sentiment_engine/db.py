import psycopg
from psycopg.rows import dict_row

DB_CONFIG = {
    "dbname": "sentiment_trading",
    "user": "postgres",
    "password": "2424",
    "host": "localhost",
    "port": 5432
}

def get_connection():
    return psycopg.connect(
        row_factory=dict_row,
        **DB_CONFIG
    )
