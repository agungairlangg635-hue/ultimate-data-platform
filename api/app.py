from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2

app = FastAPI(title="Ultimate Data Platform API")


# ========================
# DATABASE CONNECTION
# ========================
def get_conn():
    return psycopg2.connect(
        host="postgres",
        port=5432,
        database="retail_warehouse",
        user="platform_user",
        password="platform_password",
    )


# ========================
# MODELS
# ========================
class FraudRequest(BaseModel):
    amount: float
    hour: int
    transactions_last_10_min: int


# ========================
# ROOT
# ========================
@app.get("/")
def home():
    return {"message": "Ultimate Data Platform API is running"}


# ========================
# BATCH DATA ENDPOINTS
# ========================
@app.get("/revenue")
def get_revenue():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT order_date, total_revenue, total_orders
        FROM daily_revenue
        ORDER BY order_date DESC
        LIMIT 10;
    """)

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "date": str(r[0]),
            "revenue": float(r[1]),
            "orders": int(r[2]),
        }
        for r in rows
    ]


@app.get("/top-products")
def get_top_products():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT product_name, total_sold, revenue
        FROM top_products
        ORDER BY revenue DESC
        LIMIT 10;
    """)

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "product": r[0],
            "sold": int(r[1]),
            "revenue": float(r[2]),
        }
        for r in rows
    ]


# ========================
# REALTIME ENDPOINTS
# ========================
@app.get("/realtime-transactions")
def realtime_transactions():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT event_id, product_name, amount, event_timestamp
        FROM realtime_transactions
        ORDER BY event_timestamp DESC
        LIMIT 20;
    """)

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "event_id": r[0],
            "product": r[1],
            "amount": float(r[2]),
            "timestamp": str(r[3]),
        }
        for r in rows
    ]


@app.get("/realtime-summary")
def realtime_summary():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT event_minute, total_events, total_revenue, avg_transaction_amount
        FROM realtime_revenue_summary
        ORDER BY event_minute DESC
        LIMIT 20;
    """)

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "minute": str(r[0]),
            "events": int(r[1]),
            "revenue": float(r[2]),
            "avg_transaction": float(r[3]),
        }
        for r in rows
    ]


# ========================
# FRAUD PREDICTION (INSERT)
# ========================
@app.post("/predict-fraud")
def predict_fraud(payload: FraudRequest):

    # SIMPLE RULE-BASED MODEL (AMAN)
    fraud_probability = 0.10

    if payload.amount >= 5_000_000:
        fraud_probability += 0.35

    if payload.transactions_last_10_min >= 10:
        fraud_probability += 0.30

    if 0 <= payload.hour <= 4:
        fraud_probability += 0.20

    fraud_probability = min(fraud_probability, 0.99)

    is_fraud = fraud_probability >= 0.60

    if fraud_probability >= 0.75:
        risk_level = "HIGH"
    elif fraud_probability >= 0.40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO fraud_predictions (
            amount,
            hour,
            transactions_last_10_min,
            is_fraud,
            fraud_probability,
            risk_level
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING prediction_id, created_at;
        """,
        (
            payload.amount,
            payload.hour,
            payload.transactions_last_10_min,
            is_fraud,
            round(fraud_probability, 4),
            risk_level,
        ),
    )

    prediction_id, created_at = cur.fetchone()

    conn.commit()
    conn.close()

    return {
        "prediction_id": prediction_id,
        "amount": payload.amount,
        "hour": payload.hour,
        "transactions_last_10_min": payload.transactions_last_10_min,
        "is_fraud": is_fraud,
        "fraud_probability": round(fraud_probability, 4),
        "risk_level": risk_level,
        "created_at": str(created_at),
    }


# ========================
# FRAUD DATA (GET)
# ========================
@app.get("/fraud-predictions")
def get_fraud_predictions():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            prediction_id,
            amount,
            hour,
            transactions_last_10_min,
            is_fraud,
            fraud_probability,
            risk_level,
            created_at
        FROM fraud_predictions
        ORDER BY created_at DESC
        LIMIT 50;
    """)

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "prediction_id": r[0],
            "amount": float(r[1]),
            "hour": int(r[2]),
            "transactions_last_10_min": int(r[3]),
            "is_fraud": bool(r[4]),
            "fraud_probability": float(r[5]),
            "risk_level": r[6],
            "created_at": str(r[7]),
        }
        for r in rows
    ]


# ========================
# FRAUD SUMMARY
# ========================
@app.get("/fraud-summary")
def get_fraud_summary():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            prediction_minute,
            total_predictions,
            fraud_cases,
            avg_fraud_probability
        FROM fraud_prediction_summary
        ORDER BY prediction_minute DESC
        LIMIT 20;
    """)

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "prediction_minute": str(r[0]),
            "total_predictions": int(r[1]),
            "fraud_cases": int(r[2]),
            "avg_fraud_probability": float(r[3]),
        }
        for r in rows
    ]