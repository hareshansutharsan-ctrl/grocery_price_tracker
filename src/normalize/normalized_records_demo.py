from src.ingest.sources.sample_csv_ingest import read_grocery_csv
from src.normalize.normalize_units import add_parsed_quantity
from src.normalize.normalize_items import add_canonical_item


def normalize_record(record: dict) -> dict:
    record = add_parsed_quantity(record)
    record = add_canonical_item(record)
    return record


def run_demo():
    for record in read_grocery_csv("data/raw/sample_prices.csv"):
        normalized = normalize_record(record)
        print(normalized)


if __name__ == "__main__":
    run_demo()
