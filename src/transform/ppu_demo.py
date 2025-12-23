from src.ingest.sources.sample_csv_ingest import read_grocery_csv
from src.normalize.normalize_units import add_parsed_quantity
from src.normalize.normalize_items import add_canonical_item
from src.transform.price_per_unit import compute_price_per_unit


def run_demo():
    for record in read_grocery_csv("data/raw/sample_prices.csv"):
        record = add_parsed_quantity(record)
        record = add_canonical_item(record)
        record = compute_price_per_unit(record)
        print(record["store"], record["item_canonical"], record["price_per_unit"], f"per {record['ppu_unit']}")


if __name__ == "__main__":
    run_demo()
