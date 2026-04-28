CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(100),
    city VARCHAR(50),
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price NUMERIC(12,2)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    product_id VARCHAR(50),
    quantity INT,
    total_amount NUMERIC(12,2),
    order_status VARCHAR(30),
    order_timestamp TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);