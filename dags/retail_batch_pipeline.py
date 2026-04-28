from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "data-engineering-team",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}


COMMON_ENV = """
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=retail_warehouse
POSTGRES_USER=platform_user
POSTGRES_PASSWORD=platform_password
"""


with DAG(
    dag_id="retail_batch_pipeline",
    description="Generate, validate, and load realistic retail data into PostgreSQL warehouse",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["retail", "batch", "quality", "postgres"],
) as dag:

    generate_retail_data = BashOperator(
        task_id="generate_retail_data",
        bash_command=f"""
        pip install faker psycopg2-binary &&
        {COMMON_ENV}
        python /opt/airflow/data_generator/generate_retail_data.py
        """,
    )

    run_quality_checks = BashOperator(
        task_id="run_quality_checks",
        bash_command=f"""
        pip install psycopg2-binary &&
        {COMMON_ENV}
        python /opt/airflow/data_generator/quality_checks.py
        """,
    )

    generate_retail_data >> run_quality_checks