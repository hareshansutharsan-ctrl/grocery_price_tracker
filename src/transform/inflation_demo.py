from src.ingest.sources.sample_csv_ingest import read_grocery_csv
from src.normalize.normalize_units import add_parsed_quantity
from src.normalize.normalize_items import add_canonical_item
from src.transform.price_per_unit import compute_price_per_unit
from src.transform.inflation_index import weekly_item_avg, week_over_week_inflation


def run_demo():
    records = []
    for r in read_grocery_csv("data/raw/sample_prices.csv"):
        r = add_parsed_quantity(r)
        r = add_canonical_item(r)
        r = compute_price_per_unit(r)
        records.append(r)

    avgs = weekly_item_avg(records)
    rows = week_over_week_inflation(avgs)

    for row in rows:
        if row["pct_change"] is None:
            continue
        print(f"{row['item']}: {row['week']} change = {row['pct_change']:.1f}%")

if __name__ == "__main__":
    run_demo()
