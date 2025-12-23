import re


STOPWORDS = {
    "pack", "ct", "count", "pcs", "pc", "piece", "pieces",
    "kg", "g", "lb", "lbs", "l", "ml", "litre", "liter", "litres", "liters"
}


def canonical_item_name(raw_name: str) -> str | None:
    if raw_name is None:
        return None

    s = raw_name.strip().lower()

    # Remove punctuation (keep spaces)
    s = re.sub(r"[^a-z0-9\s]", " ", s)

    # Remove number+unit combos like 2l, 4.5kg, 10lb
    s = re.sub(r"\b\d+(\.\d+)?\s*(kg|g|lb|lbs|l|ml|ct|pack)\b", " ", s)

    # Remove remaining standalone numbers
    s = re.sub(r"\b\d+(\.\d+)?\b", " ", s)

    # Tokenize and remove stopwords
    tokens = [t for t in s.split() if t and t not in STOPWORDS]

    return " ".join(tokens) if tokens else None



def add_canonical_item(record: dict) -> dict:
    out = dict(record)
    out["item_canonical"] = canonical_item_name(record.get("item_name"))
    return out


if __name__ == "__main__":
    samples = [
        "Milk 2L",
        "Milk 2 L",
        "Eggs 30 pack",
        "Eggs 12",
        "Basmati Rice 10 lb",
        "Basmati rice 4.5kg",
        "Chicken Breast 1.2kg",
        "Chicken breast 2.5 lb",
    ]
    for s in samples:
        print(s, "->", canonical_item_name(s))
