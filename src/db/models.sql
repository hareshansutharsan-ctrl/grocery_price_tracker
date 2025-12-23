-- Stores (dimension)
CREATE TABLE IF NOT EXISTS stores (
  store_id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL
);

-- Items (dimension)
CREATE TABLE IF NOT EXISTS items (
  item_id SERIAL PRIMARY KEY,
  canonical_name TEXT UNIQUE NOT NULL
);

-- Prices (fact table)
CREATE TABLE IF NOT EXISTS prices (
  price_id SERIAL PRIMARY KEY,
  price_date DATE NOT NULL,
  store_id INT NOT NULL REFERENCES stores(store_id),
  item_id INT NOT NULL REFERENCES items(item_id),

  item_name_raw TEXT,
  quantity_raw TEXT,

  quantity_amount DOUBLE PRECISION,
  quantity_unit TEXT,

  price DOUBLE PRECISION,
  price_per_unit DOUBLE PRECISION,
  ppu_unit TEXT,

  created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for query performance
CREATE INDEX IF NOT EXISTS idx_prices_date ON prices(price_date);
CREATE INDEX IF NOT EXISTS idx_prices_item ON prices(item_id);
CREATE INDEX IF NOT EXISTS idx_prices_store ON prices(store_id);

-- Prevent duplicate loads of the same observation
CREATE UNIQUE INDEX IF NOT EXISTS uq_price_observation
ON prices (price_date, store_id, item_id, quantity_raw, price);
