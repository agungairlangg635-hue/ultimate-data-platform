from fastapi import FastAPI
import psycopg2

app = FastAPI()


def get_conn():
    return psycopg2.connect(
        host="postgres",
        port=5432,
        database="retail_warehouse",
        user="platform_user",
        password="platform_password",
    )


# =========================
# BATCH DATA
# =========================
@app.get("/revenue")
def get_revenue():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM daily_revenue LIMIT 10;")
    rows = cur.fetchall()

    conn.close()
    return rows


# =========================
# REALTIME TRANSACTIONS
# =========================
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


# =========================
# REALTIME SUMMARY
# =========================
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