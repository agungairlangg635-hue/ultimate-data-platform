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


def create_analytics_tables(conn):
    with conn.cursor() as cur:

        # DAILY REVENUE
        cur.execute("""
        DROP TABLE IF EXISTS daily_revenue;
        CREATE TABLE daily_revenue AS
        SELECT
            DATE(order_timestamp) AS order_date,
            SUM(total_amount) AS total_revenue,
            COUNT(*) AS total_orders
        FROM orders
        WHERE order_status = 'completed'
        GROUP BY 1
        ORDER BY 1;
        """)

        # TOP PRODUCTS
        cur.execute("""
        DROP TABLE IF EXISTS top_products;
        CREATE TABLE top_products AS
        SELECT
            p.product_name,
            SUM(o.quantity) AS total_sold,
            SUM(o.total_amount) AS revenue
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        WHERE o.order_status = 'completed'
        GROUP BY 1
        ORDER BY revenue DESC
        LIMIT 10;
        """)

        # CUSTOMER METRICS
        cur.execute("""
        DROP TABLE IF EXISTS customer_metrics;
        CREATE TABLE customer_metrics AS
        SELECT
            c.customer_id,
            c.full_name,
            COUNT(o.order_id) AS total_orders,
            SUM(o.total_amount) AS total_spent,
            AVG(o.total_amount) AS avg_order_value
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY 1,2;
        """)

    conn.commit()


def main():
    print("Running analytics transformations...")
    conn = get_connection()

    create_analytics_tables(conn)

    conn.close()
    print("Analytics tables created successfully!")


if __name__ == "__main__":
    main()