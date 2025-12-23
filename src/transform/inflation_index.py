from collections import defaultdict
from datetime import datetime


def week_key(date_str: str) -> str | None:
    if not date_str:
        return None
    d = datetime.strptime(date_str, "%Y-%m-%d").date()
    iso_year, iso_week, _ = d.isocalendar()
    return f"{iso_year}-W{iso_week:02d}"


def weekly_item_avg(records: list[dict]) -> dict:
    """
    Returns:
      (week, item_canonical) -> avg price_per_unit
    """
    buckets = defaultdict(list)
    for r in records:
        wk = week_key(r.get("date"))
        item = r.get("item_canonical")
        ppu = r.get("price_per_unit")
        if wk and item and ppu is not None:
            buckets[(wk, item)].append(ppu)

    return {k: sum(v) / len(v) for k, v in buckets.items()}


def week_over_week_inflation(weekly_avgs: dict) -> list[dict]:
    """
    Output rows:
      {week, item, avg_ppu, prev_avg_ppu, pct_change}
    """
    # group by item
    by_item = defaultdict(list)
    for (wk, item), avg in weekly_avgs.items():
        by_item[item].append((wk, avg))

    out = []
    for item, rows in by_item.items():
        rows_sorted = sorted(rows, key=lambda x: x[0])
        prev = None
        for wk, avg in rows_sorted:
            if prev is None:
                out.append({"week": wk, "item": item, "avg_ppu": avg, "prev_avg_ppu": None, "pct_change": None})
            else:
                prev_wk, prev_avg = prev
                pct = ((avg - prev_avg) / prev_avg) * 100.0 if prev_avg else None
                out.append({"week": wk, "item": item, "avg_ppu": avg, "prev_avg_ppu": prev_avg, "pct_change": pct})
            prev = (wk, avg)

    return out
