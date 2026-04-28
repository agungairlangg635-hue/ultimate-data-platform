import pickle
import random

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def generate_training_data(n=2000):
    rows = []

    for _ in range(n):
        amount = random.randint(50_000, 10_000_000)
        hour = random.randint(0, 23)
        transactions_last_10_min = random.randint(1, 20)

        is_fraud = 0

        if amount > 5_000_000 and transactions_last_10_min > 8:
            is_fraud = 1

        if hour >= 0 and hour <= 4 and amount > 3_000_000:
            is_fraud = 1

        rows.append({
            "amount": amount,
            "hour": hour,
            "transactions_last_10_min": transactions_last_10_min,
            "is_fraud": is_fraud
        })

    return pd.DataFrame(rows)


def main():
    df = generate_training_data()

    X = df[["amount", "hour", "transactions_last_10_min"]]
    y = df["is_fraud"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy: {accuracy:.2f}")

    with open("ml/fraud_model.pkl", "wb") as f:
        pickle.dump(model, f)

    print("Model saved to ml/fraud_model.pkl")


if __name__ == "__main__":
    main()