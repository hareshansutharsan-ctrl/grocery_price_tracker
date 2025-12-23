import csv
from pathlib import Path


def read_grocery_csv(file_path: str):
    """
    Reads a raw grocery price CSV and yields rows as dictionaries.
    No cleaning or normalization happens here.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield {
                "date": row.get("date"),           # ✅ added
                "store": row.get("store"),
                "item_name": row.get("item"),
                "price": float(row["price"]) if row.get("price") else None,
                "quantity": row.get("quantity"),
            }


if __name__ == "__main__":
    sample_file = "data/raw/sample_prices.csv"

    for record in read_grocery_csv(sample_file):
        print(record)

