from collections import defaultdict


def best_price_by_item(records: list[dict]) -> dict:
    """
    Returns:
      item_canonical -> {
        "best_store": str,
        "best_ppu": float,
        "best_unit": str,
        "all": [(store, ppu), ...] sorted
      }
    """
    groups = defaultdict(list)

    for r in records:
        item = r.get("item_canonical")
        ppu = r.get("price_per_unit")
        store = r.get("store")
        unit = r.get("ppu_unit")

        if not item or ppu is None or not store or not unit:
            continue

        groups[item].append((store, ppu, unit))

    result = {}
    for item, rows in groups.items():
        rows_sorted = sorted(rows, key=lambda x: x[1])
        best_store, best_ppu, best_unit = rows_sorted[0]
        result[item] = {
            "best_store": best_store,
            "best_ppu": best_ppu,
            "best_unit": best_unit,
            "all": rows_sorted,
        }

    return result


def savings_alerts(summary: dict, min_savings_pct: float = 10.0) -> list[str]:
    """
    For each item, compare best vs second-best (or any other store),
    and generate an alert if savings >= min_savings_pct.
    """
    alerts = []

    for item, info in summary.items():
        rows = info["all"]
        if len(rows) < 2:
            continue

        best_store, best_ppu, unit = rows[0]
        second_store, second_ppu, _ = rows[1]

        # percent cheaper than second-best
        savings_pct = ((second_ppu - best_ppu) / second_ppu) * 100.0

        if savings_pct >= min_savings_pct:
            alerts.append(
                f"{item.title()} is {savings_pct:.0f}% cheaper at {best_store} "
                f"({best_ppu:.3f} per {unit}) vs {second_store} ({second_ppu:.3f} per {unit})."
            )

    return alerts
