import random
import uuid
from datetime import datetime, timedelta

import psycopg2
from faker import Faker


fake = Faker("id_ID")

import os
DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", "5433")),
    "database": os.getenv("POSTGRES_DB", "retail_warehouse"),
    "user": os.getenv("POSTGRES_USER", "platform_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "platform_password"),
}

PRODUCTS = [
    ("Laptop Pro 14", "Electronics", 18500000),
    ("Wireless Mouse", "Electronics", 250000),
    ("Mechanical Keyboard", "Electronics", 850000),
    ("Office Chair", "Furniture", 1750000),
    ("Standing Desk", "Furniture", 3200000),
    ("Running Shoes", "Fashion", 950000),
    ("Hoodie Oversize", "Fashion", 350000),
    ("Coffee Beans Arabica", "Groceries", 120000),
    ("Smart Watch", "Electronics", 2100000),
    ("Backpack Travel", "Fashion", 450000),
]


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def clear_tables(conn):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM orders;")
        cur.execute("DELETE FROM products;")
        cur.execute("DELETE FROM customers;")
    conn.commit()


def generate_customers(conn, total=100):
    customers = []

    with conn.cursor() as cur:
        for _ in range(total):
            customer_id = str(uuid.uuid4())
            full_name = fake.name()
            email = fake.email()
            city = fake.city()
            created_at = fake.date_time_between(start_date="-1y", end_date="now")

            customers.append(customer_id)

            cur.execute(
                """
                INSERT INTO customers (
                    customer_id, full_name, email, city, created_at
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (customer_id, full_name, email, city, created_at),
            )

    conn.commit()
    return customers


def generate_products(conn):
    product_ids = []

    with conn.cursor() as cur:
        for product_name, category, price in PRODUCTS:
            product_id = str(uuid.uuid4())
            product_ids.append((product_id, price))

            cur.execute(
                """
                INSERT INTO products (
                    product_id, product_name, category, price
                )
                VALUES (%s, %s, %s, %s)
                """,
                (product_id, product_name, category, price),
            )

    conn.commit()
    return product_ids


def generate_orders(conn, customers, products, total=500):
    statuses = ["completed", "pending", "cancelled", "failed"]

    with conn.cursor() as cur:
        for _ in range(total):
            order_id = str(uuid.uuid4())
            customer_id = random.choice(customers)
            product_id, price = random.choice(products)
            quantity = random.randint(1, 5)
            total_amount = price * quantity
            order_status = random.choices(
                statuses,
                weights=[75, 12, 8, 5],
                k=1,
            )[0]
            order_timestamp = datetime.now() - timedelta(
                days=random.randint(0, 90),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
            )

            cur.execute(
                """
                INSERT INTO orders (
                    order_id, customer_id, product_id, quantity,
                    total_amount, order_status, order_timestamp
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    order_id,
                    customer_id,
                    product_id,
                    quantity,
                    total_amount,
                    order_status,
                    order_timestamp,
                ),
            )

    conn.commit()


def main():
    print("Connecting to PostgreSQL...")
    conn = get_connection()

    print("Clearing existing data...")
    clear_tables(conn)

    print("Generating customers...")
    customers = generate_customers(conn, total=100)

    print("Generating products...")
    products = generate_products(conn)

    print("Generating orders...")
    generate_orders(conn, customers, products, total=500)

    conn.close()
    print("Retail data generated successfully!")


if __name__ == "__main__":
    main()