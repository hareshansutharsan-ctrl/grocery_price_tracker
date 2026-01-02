# Smart Grocery Price Tracker & Inflation Alerts

This project is a practical data engineering pipeline that tracks grocery prices across stores, cleans up inconsistent real-world data, and makes it easy to compare prices fairly over time.

The focus is on solving a real problem: grocery prices are messy, hard to compare, and change constantly. This pipeline turns raw price data into something usable and meaningful.

---

## Why I Built This

Grocery data isn’t clean:

- The same item appears under different names  
  (e.g. `Milk 2L`, `Milk 2 L`, `2L Milk`)
- Units aren’t consistent  
  (lb vs kg, ml vs L, count vs packs)
- Raw prices don’t tell you what’s actually cheaper

I built this project to normalize that data, track how prices change week to week, and surface insights that actually help people save money.

---

## What the Pipeline Does

### 1. Ingest
- Loads raw grocery price data from CSV files  
- Designed so scraping or API data can be added later

### 2. Normalize
- Standardizes product names  
  - Example: `Milk 2L`, `Milk 2 L` → `milk`
- Converts all units into a common system  
  - lb → kg  
  - ml → L  
  - ct → count

### 3. Transform
- Calculates **price per unit** so items can be compared fairly
- Groups prices by week
- Computes week-over-week price changes to track inflation

### 4. Store
- Saves cleaned data in PostgreSQL
- Uses idempotent loads so the pipeline can be rerun safely

### 5. Analyze & Alert
- Finds the cheapest store for each item
- Flags meaningful price changes
- Produces alerts like:
  - “Milk is 18% cheaper at No Frills than Walmart”
  - “Egg prices increased 5.6% this week”

---

## Architecture
Raw CSVs
↓
Python ingestion scripts
↓
Data cleaning & unit normalization
↓
Price-per-unit + weekly aggregation
↓
PostgreSQL
↓
SQL queries & alerts


---

## Tech Stack

- Python – ingestion, cleaning, transformations  
- PostgreSQL – data storage and analytics  
- SQL – price comparisons and inflation queries  
- Docker – consistent local environment  

---

## Example Output
basmati rice: cheapest at No Frills → $3.66 / kg
chicken breast: cheapest at Walmart → $11.46 / kg
eggs: cheapest at Walmart → $0.29 / egg
milk: cheapest at No Frills → $2.45 / L


---

## What This Project Shows

- Working with messy, real-world data
- Designing transformations that support analysis
- Writing SQL that answers practical questions
- Building pipelines that are safe to rerun
- Thinking about cost, trends, and user impact

This project is built to reflect the kind of problems you’d see in a real data engineering role.

---

## Possible Next Steps

- Automate data collection from grocery flyers
- Schedule weekly pipeline runs
- Send alerts via email or notifications
- Add a simple dashboard for trends over time




