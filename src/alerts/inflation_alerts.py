def inflation_spike_alerts(inflation_rows: list[dict], spike_pct: float = 5.0) -> list[str]:
    """
    Turn week-over-week inflation rows into human alerts.
    Triggers when pct_change >= spike_pct.
    """
    alerts = []

    for r in inflation_rows:
        item = r.get("item")
        week = r.get("week")
        pct = r.get("pct_change")

        if item and week and pct is not None and pct >= spike_pct:
            alerts.append(f"{item.title()} prices spiked {pct:.1f}% in {week}.")

    return alerts
