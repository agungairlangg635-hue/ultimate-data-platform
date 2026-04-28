CREATE TABLE IF NOT EXISTS realtime_transactions (
    event_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    amount NUMERIC(12,2),
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);