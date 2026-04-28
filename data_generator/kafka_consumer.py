import json

import psycopg2
from kafka import KafkaConsumer


DB_CONFIG = {
    "host": "postgres",
    "port": 5432,
    "database": "retail_warehouse",
    "user": "platform_user",
    "password": "platform_password",
}


def get_conn():
    return psycopg2.connect(**DB_CONFIG)


def main():
    consumer = KafkaConsumer(
        "transactions",
        bootstrap_servers="kafka:9092",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id="realtime-transaction-consumer",
    )

    conn = get_conn()
    cur = conn.cursor()

    print("Consumer started. Waiting for Kafka events...")

    for message in consumer:
        event = message.value

        product = event.get("product")
        amount = event.get("amount")

        cur.execute(
            """
            INSERT INTO realtime_transactions (product_name, amount)
            VALUES (%s, %s)
            """,
            (product, amount),
        )

        conn.commit()
        print("Inserted event:", event)


if __name__ == "__main__":
    main()