def compute_price_per_unit(record: dict) -> dict:
    """
    Adds `price_per_unit` and `ppu_unit` to a normalized record.

    Requires:
      - price (float)
      - quantity_amount (float)
      - quantity_unit (str: "kg" | "l" | "ct")
    """
    price = record.get("price")
    qty = record.get("quantity_amount")
    unit = record.get("quantity_unit")

    out = dict(record)

    if price is None or qty is None or unit is None or qty == 0:
        out["price_per_unit"] = None
        out["ppu_unit"] = None
        return out

    out["price_per_unit"] = price / qty
    out["ppu_unit"] = f"{unit}"
    return out


if __name__ == "__main__":
    # Quick sanity tests
    samples = [
        {"price": 5.99, "quantity_amount": 2.0, "quantity_unit": "l"},
        {"price": 18.99, "quantity_amount": 4.5359, "quantity_unit": "kg"},
        {"price": 9.99, "quantity_amount": 30.0, "quantity_unit": "ct"},
    ]

    for s in samples:
        print(compute_price_per_unit(s))
