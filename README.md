# Smart Grocery Price Tracker & Inflation Alerts

Goal: Ingest grocery price data, normalize messy item/unit formats, compute price-per-unit and weekly inflation trends, and send alerts when prices change meaningfully.

## Pipeline
Ingest → Normalize → Transform → Store → Alert


# 🛒 Smart Grocery Price Tracker & Inflation Alert System

An end-to-end data engineering pipeline that helps households save money by
tracking grocery prices, normalizing messy real-world data, detecting weekly
food inflation, and alerting users when cheaper alternatives exist.

---

## 🚀 What This Project Does

- Ingests raw grocery price data (CSV-based, extensible to scraping/APIs)
- Normalizes:
  - Item names (e.g., “Milk 2L”, “Milk 2 L” → `milk`)
  - Units (lb → kg, ml → l, ct → count)
- Computes:
  - Price-per-unit for fair store comparisons
  - Weekly inflation by product
- Generates alerts such as:
  - “Milk is 18% cheaper at No Frills vs Walmart”
  - “Egg prices spiked 5.6% this week”
- Stores normalized data in PostgreSQL with idempotent loading
- Queries cheapest store per item for the latest week directly from SQL

---

## 🧱 Architecture

