from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "data-engineering-team",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}


with DAG(
    dag_id="retail_batch_pipeline",
    description="Generate realistic retail data and load it into PostgreSQL warehouse",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["retail", "batch", "postgres"],
) as dag:

    generate_retail_data = BashOperator(
        task_id="generate_retail_data",
        bash_command="""
        pip install faker psycopg2-binary &&
        POSTGRES_HOST=postgres \
        POSTGRES_PORT=5432 \
        POSTGRES_DB=retail_warehouse \
        POSTGRES_USER=platform_user \
        POSTGRES_PASSWORD=platform_password \
        python /opt/airflow/data_generator/generate_retail_data.py
        """,
    )

    generate_retail_data