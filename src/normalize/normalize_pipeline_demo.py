from src.ingest.sources.sample_csv_ingest import read_grocery_csv
from src.normalize.normalize_units import add_parsed_quantity


def run_demo():
    for record in read_grocery_csv("data/raw/sample_prices.csv"):
        enriched = add_parsed_quantity(record)
        print(enriched)


if __name__ == "__main__":
    run_demo()

