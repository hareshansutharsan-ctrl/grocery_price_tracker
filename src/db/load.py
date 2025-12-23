import os
from pathlib import Path
import psycopg2

from src.ingest.sources.sample_csv_ingest import read_grocery_csv
from src.normalize.normalize_units import add_parsed_quantity
from src.normalize.normalize_items import add_canonical_item
from src.transform.price_per_unit import compute_price_per_unit


def get_conn():
    db = os.getenv("POSTGRES_DB", "grocery_prices")
    user = os.getenv("POSTGRES_USER", "postgres")
    pw = os.getenv("POSTGRES_PASSWORD", "postgres")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")

    return psycopg2.connect(
        dbname=db,
        user=user,
        password=pw,
        host=host,
        port=port,
    )


def run_schema(conn):
    sql_path = Path("src/db/models.sql")
    sql = sql_path.read_text(encoding="utf-8")
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()


def get_or_create_store(cur, store_name: str) -> int:
    cur.execute(
        "INSERT INTO stores (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;",
        (store_name,),
    )
    cur.execute("SELECT store_id FROM stores WHERE name=%s;", (store_name,))
    return cur.fetchone()[0]


def get_or_create_item(cur, canonical: str) -> int:
    cur.execute(
        "INSERT INTO items (canonical_name) VALUES (%s) ON CONFLICT (canonical_name) DO NOTHING;",
        (canonical,),
    )
    cur.execute("SELECT item_id FROM items WHERE canonical_name=%s;", (canonical,))
    return cur.fetchone()[0]


def load_prices(conn, csv_path="data/raw/sample_prices.csv"):
    with conn.cursor() as cur:
        for r in read_grocery_csv(csv_path):
            r = add_parsed_quantity(r)
            r = add_canonical_item(r)
            r = compute_price_per_unit(r)

            # Required fields (skip bad rows)
            if (
                not r.get("date")
                or not r.get("store")
                or not r.get("item_canonical")
                or r.get("price") is None
            ):
                continue

            store_id = get_or_create_store(cur, r["store"])
            item_id = get_or_create_item(cur, r["item_canonical"])

            cur.execute(
                """
                INSERT INTO prices (
                  price_date, store_id, item_id,
                  item_name_raw, quantity_raw,
                  quantity_amount, quantity_unit,
                  price, price_per_unit, ppu_unit
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT DO NOTHING;
                """,
                (
                    r["date"],
                    store_id,
                    item_id,
                    r.get("item_name"),
                    r.get("quantity"),
                    r.get("quantity_amount"),
                    r.get("quantity_unit"),
                    r.get("price"),
                    r.get("price_per_unit"),
                    r.get("ppu_unit"),
                ),
            )

    conn.commit()


def main():
    conn = get_conn()
    try:
        run_schema(conn)
        load_prices(conn)
        print("✅ Loaded data into Postgres.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()

