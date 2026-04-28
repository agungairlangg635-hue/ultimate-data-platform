import json
import time
import random
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

products = ["Laptop", "Mouse", "Keyboard", "Shoes"]

while True:
    event = {
        "product": random.choice(products),
        "amount": random.randint(100000, 5000000),
    }

    producer.send("transactions", event)
    print("Sent:", event)

    time.sleep(2)