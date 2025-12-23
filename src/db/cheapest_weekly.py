import os
from pathlib import Path
import psycopg2


def get_conn():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "grocery_prices"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )


def main():
    sql = Path("src/db/queries.sql").read_text(encoding="utf-8")
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

    for item, store, ppu, unit in rows:
        print(f"{item}: cheapest at {store} -> {ppu:.3f} per {unit}")


if __name__ == "__main__":
    main()
