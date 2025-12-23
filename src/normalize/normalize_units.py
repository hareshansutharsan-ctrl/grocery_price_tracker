import re

LB_TO_KG = 0.45359237


def parse_quantity(quantity_raw: str):
    """
    Convert messy quantity strings into (amount, unit) in standard units.

    Standard units we use:
      - weight: kg
      - volume: l
      - count: ct

    Examples:
      "2L" -> (2.0, "l")
      "2 L" -> (2.0, "l")
      "4.5 kg" -> (4.5, "kg")
      "10 lb" -> (4.5359..., "kg")
      "30 ct" -> (30.0, "ct")
    """
    if quantity_raw is None:
        return None, None

    s = quantity_raw.strip().lower()

    # Extract number + unit (handles: "2L", "2 L", "4.5kg", "30 ct")
    m = re.match(r"^\s*(\d+(\.\d+)?)\s*([a-z]+)\s*$", s)
    if not m:
        return None, None

    amount = float(m.group(1))
    unit = m.group(3)

    # Normalize common unit aliases
    if unit in ["kg", "kgs", "kilogram", "kilograms"]:
        return amount, "kg"

    if unit in ["g", "gram", "grams"]:
        return amount / 1000.0, "kg"

    if unit in ["lb", "lbs", "pound", "pounds"]:
        return amount * LB_TO_KG, "kg"

    if unit in ["l", "lt", "liter", "litre", "liters", "litres"]:
        return amount, "l"

    if unit in ["ml", "milliliter", "millilitre", "milliliters", "millilitres"]:
        return amount / 1000.0, "l"

    if unit in ["ct", "count", "pc", "pcs", "piece", "pieces", "pack"]:
        return amount, "ct"

    return None, None


def add_parsed_quantity(record: dict) -> dict:
    """
    Takes a raw record and adds:
      - quantity_amount
      - quantity_unit
    """
    amount, unit = parse_quantity(record.get("quantity"))
    out = dict(record)
    out["quantity_amount"] = amount
    out["quantity_unit"] = unit
    return out


if __name__ == "__main__":
    # Quick manual test
    samples = ["2L", "2 L", "4.5kg", "10 lb", "30 ct", "500g", "750ml"]
    for q in samples:
        print(q, "->", parse_quantity(q))
