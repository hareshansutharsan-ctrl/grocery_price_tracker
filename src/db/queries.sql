-- Cheapest store per item for the latest week in the table
WITH latest_week AS (
  SELECT date_trunc('week', MAX(price_date)) AS wk_start
  FROM prices
),
week_prices AS (
  SELECT
    p.price_date,
    date_trunc('week', p.price_date) AS wk_start,
    s.name AS store,
    i.canonical_name AS item,
    p.price_per_unit,
    p.ppu_unit
  FROM prices p
  JOIN stores s ON s.store_id = p.store_id
  JOIN items i ON i.item_id = p.item_id
),
ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY item ORDER BY price_per_unit ASC) AS rn
  FROM week_prices
  WHERE wk_start = (SELECT wk_start FROM latest_week)
)
SELECT item, store, price_per_unit, ppu_unit
FROM ranked
WHERE rn = 1
ORDER BY item;
