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
