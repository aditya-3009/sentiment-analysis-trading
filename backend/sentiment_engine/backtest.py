import csv
from db import get_connection


def load_prices(path="data/raw/prices.csv"):
    prices = {}
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prices[row["date"]] = float(row["price"])
    return prices


def backtest():
    prices = load_prices()

    query = """
        SELECT ts.signal, ss.created_at::date AS signal_date
        FROM trading_signals ts
        JOIN sentiment_scores ss ON ts.sentiment_score_id = ss.id;
    """

    correct = 0
    total = 0

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

            for row in rows:
                date = str(row["signal_date"])
                signal = row["signal"]

                if date not in prices:
                    continue

                next_day = str(
                    (row["signal_date"]).fromordinal(
                        row["signal_date"].toordinal() + 1
                    )
                )

                if next_day not in prices:
                    continue

                price_today = prices[date]
                price_next = prices[next_day]
                delta = price_next - price_today

                if signal == "BUY" and delta > 0:
                    correct += 1
                elif signal == "SELL" and delta < 0:
                    correct += 1
                elif signal == "HOLD":
                    correct += 1

                total += 1

    accuracy = correct / total if total > 0 else 0
    print(f"Backtest accuracy: {accuracy:.2f}")


if __name__ == "__main__":
    backtest()
