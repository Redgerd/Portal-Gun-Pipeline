﻿# Rick & Morty Portal Gun Pipeline
 
This project builds a local data engineering pipeline that extracts data from the Rick & Morty public API, stores raw data locally, transforms it into structured tables, and validates data quality — all orchestrated using Apache Airflow.

## Project Overview

- Extract character, location, and episode data from the Rick & Morty REST API
- Store raw JSON files in a local S3-compatible MinIO bucket (Bronze layer)
- Use DuckDB as a local analytical database to transform raw data into cleaned Silver and Gold tables
- Validate data quality using Great Expectations
- Orchestrate the entire workflow with Apache Airflow running daily
- Query and analyze data locally with DuckDB CLI or Jupyter notebooks

## Architecture Diagram

![image](https://github.com/user-attachments/assets/b8074537-c408-444e-81b3-72226b143353)

## Technologies Used

| Layer               | Technology         |
|---------------------|--------------------|
| Data Source         | Rick & Morty API   |
| Orchestration       | Apache Airflow     |
| Object Storage      | MinIO (local S3)   |
| Data Warehouse      | DuckDB             |
| Data Modeling       | dbt                |
| Data Validation     | Great Expectations |
| Containerization    | Docker             |
