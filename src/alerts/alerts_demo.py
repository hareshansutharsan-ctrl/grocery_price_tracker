from src.ingest.sources.sample_csv_ingest import read_grocery_csv
from src.normalize.normalize_units import add_parsed_quantity
from src.normalize.normalize_items import add_canonical_item
from src.transform.price_per_unit import compute_price_per_unit
from src.alerts.rules import best_price_by_item, savings_alerts


def run_demo():
    records = []
    for r in read_grocery_csv("data/raw/sample_prices.csv"):
        r = add_parsed_quantity(r)
        r = add_canonical_item(r)
        r = compute_price_per_unit(r)
        records.append(r)

    summary = best_price_by_item(records)
    alerts = savings_alerts(summary, min_savings_pct=10.0)

    print("\n".join(alerts) if alerts else "No alerts triggered.")


if __name__ == "__main__":
    run_demo()
