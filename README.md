# Ultimate Data Platform

An end-to-end data engineering project that simulates a modern retail data platform with batch processing, real-time streaming, API access, analytics dashboards, fraud detection, and AI-assisted debugging.

## Overview

This project was built to demonstrate how data moves through a production-style platform: from raw transaction generation, batch orchestration, real-time Kafka events, warehouse storage, API services, dashboarding, and fraud monitoring.

The goal is not only to build a pipeline, but to show how different parts of a data platform work together in a realistic business scenario.

## What This Project Covers

- Batch ETL pipeline with Apache Airflow
- Real-time transaction streaming with Apache Kafka
- PostgreSQL as the analytics warehouse
- Data quality validation before transformation
- Analytics marts for revenue, products, and customer behavior
- FastAPI service for exposing data and fraud results
- Metabase dashboard for business monitoring
- Real-time fraud scoring from streaming transactions
- AI-style log analyzer for debugging common pipeline errors
- Docker Compose setup for local development

## Architecture

```text
Synthetic Retail Data
        |
        v
Airflow Batch Pipeline
        |
        v
PostgreSQL Warehouse
        |
        v
Analytics Tables
        |
        v
Metabase Dashboard


Kafka Producer
        |
        v
Kafka Topic: transactions
        |
        v
Kafka Consumer
        |
        +--> realtime_transactions
        |
        +--> fraud_predictions
        |
        v
Realtime Monitoring Dashboard


FastAPI
  ├── /revenue
  ├── /top-products
  ├── /realtime-transactions
  ├── /realtime-summary
  ├── /predict-fraud
  ├── /fraud-predictions
  ├── /fraud-summary
  └── /copilot/analyze-log




| Area             | Tools          |
| ---------------- | -------------- |
| Orchestration    | Apache Airflow |
| Streaming        | Apache Kafka   |
| Database         | PostgreSQL     |
| API              | FastAPI        |
| Dashboard        | Metabase       |
| Containerization | Docker Compose |
| Language         | Python, SQL    |
| CI               | GitHub Actions |



Main Features
Batch Pipeline

The batch pipeline generates synthetic retail data, validates data quality, and transforms raw tables into analytics-ready tables.

Main outputs:

daily_revenue
top_products
customer_metrics
Real-Time Streaming

Kafka is used to simulate real-time retail transactions. The consumer processes events and stores them in PostgreSQL for live monitoring.

Main outputs:

realtime_transactions
realtime_revenue_summary

Fraud Detection

The platform includes a fraud scoring flow that evaluates transaction risk based on amount, transaction frequency, and transaction time.

Main outputs:

fraud_predictions
fraud_prediction_summary
API Layer

FastAPI exposes data and monitoring endpoints.

Example endpoints:

GET  /revenue
GET  /top-products
GET  /realtime-transactions
GET  /realtime-summary
POST /predict-fraud
GET  /fraud-predictions
GET  /fraud-summary
POST /copilot/analyze-log

AI Copilot Debugger

The copilot endpoint analyzes common pipeline errors and suggests fixes.

Example request:

{
  "log_text": "ModuleNotFoundError: No module named kafka"
}

Example response:

{
  "severity": "MEDIUM",
  "root_cause": "Kafka Python dependency is missing inside the container.",
  "suggested_fix": "Install kafka-python inside the Airflow container or add it to the Docker command."
}



Dashboard

The Metabase dashboard includes:

Daily revenue trend
Top product performance
Customer metrics
Real-time revenue monitoring
Fraud prediction monitoring
Fraud risk KPI


How to Run

Clone the repository:

git clone https://github.com/agungairlangg635-hue/ultimate-data-platform.git
cd ultimate-data-platform

Start all services:

docker compose up -d



Open the services:

Service	URL
Airflow	http://localhost:8080

Metabase	http://localhost:3000

FastAPI Docs	http://localhost:8000/docs

PostgreSQL	localhost:5433


Default Airflow login:

username: admin
password: admin
Running the Batch Pipeline

Open Airflow, enable the DAG:

retail_batch_pipeline

Then trigger the DAG manually.

Pipeline flow:

generate_retail_data → run_quality_checks → run_transformations

Running the Streaming Pipeline

Start the Kafka consumer:

docker exec -it udp_airflow_webserver bash
python /opt/airflow/data_generator/kafka_consumer.py

Start the Kafka producer in another terminal:

docker exec -it udp_airflow_webserver bash
python /opt/airflow/data_generator/kafka_producer.py
Example Fraud Prediction

Open:

http://localhost:8000/docs

Run:

POST /predict-fraud

Example payload:

{
  "amount": 9000000,
  "hour": 2,
  "transactions_last_10_min": 15
}


Repository Structure
ultimate-data-platform/
├── api/
│   └── app.py
├── dags/
│   └── retail_batch_pipeline.py
├── data_generator/
│   ├── generate_retail_data.py
│   ├── quality_checks.py
│   ├── transform_analytics.py
│   ├── kafka_producer.py
│   └── kafka_consumer.py
├── warehouse/
│   └── schema.sql
├── ml/
├── docker-compose.yml
├── Makefile
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md



Portfolio Highlights

This project demonstrates practical data engineering skills:

Building batch and streaming pipelines
Designing a warehouse-backed analytics layer
Orchestrating workflows with Airflow
Handling real-time events with Kafka
Exposing data through APIs
Building dashboards for business users
Adding monitoring and fraud detection logic
Debugging containerized data services
Resume Bullet

Built an end-to-end retail data platform using Airflow, Kafka, PostgreSQL, FastAPI, Docker, and Metabase, featuring batch ETL, real-time streaming, data quality checks, fraud detection, API endpoints, and analytics dashboards.

Future Improvements
Deploy the API and dashboard to the cloud
Add dbt for transformation modeling
Add Telegram or Slack alerts for fraud spikes
Add proper ML training pipeline
Add data lineage and observability metrics
Add Kubernetes deployment

Saran cepat sebelum apply: hapus `.vscode` dan `logs` dari GitHub, lalu ubah repo About menjadi:

```text
End-to-end data engineering platform with Airflow, Kafka, PostgreSQL, FastAPI, Metabase, real-time









