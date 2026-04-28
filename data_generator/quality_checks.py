import os
import psycopg2


DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", "5433")),
    "database": os.getenv("POSTGRES_DB", "retail_warehouse"),
    "user": os.getenv("POSTGRES_USER", "platform_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "platform_password"),
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def run_check(cursor, check_name, query):
    cursor.execute(query)
    result = cursor.fetchone()[0]

    if result > 0:
        raise ValueError(f"Data quality check failed: {check_name}. Found {result} bad records.")

    print(f"PASSED: {check_name}")


def main():
    conn = get_connection()

    with conn.cursor() as cur:
        run_check(
            cur,
            "orders_total_amount_not_null",
            "SELECT COUNT(*) FROM orders WHERE total_amount IS NULL;",
        )

        run_check(
            cur,
            "orders_quantity_positive",
            "SELECT COUNT(*) FROM orders WHERE quantity <= 0;",
        )

        run_check(
            cur,
            "orders_customer_id_not_null",
            "SELECT COUNT(*) FROM orders WHERE customer_id IS NULL;",
        )

        run_check(
            cur,
            "orders_product_id_not_null",
            "SELECT COUNT(*) FROM orders WHERE product_id IS NULL;",
        )

        run_check(
            cur,
            "customers_email_not_null",
            "SELECT COUNT(*) FROM customers WHERE email IS NULL;",
        )

        run_check(
            cur,
            "products_price_positive",
            "SELECT COUNT(*) FROM products WHERE price <= 0;",
        )

    conn.close()
    print("All data quality checks passed!")


if __name__ == "__main__":
    main()