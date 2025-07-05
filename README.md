# Rick & Morty Portal Gun Pipeline

This project builds a local data engineering pipeline that extracts data from the Rick & Morty public API, stores raw data locally, transforms it into structured tables, and validates data quality — all orchestrated using Apache Airflow.

## Project Overview

- Extract character, location, and episode data from the Rick & Morty REST API
- Store raw JSON files in a local S3-compatible MinIO bucket (Bronze layer)
- Use PostgreSQL as the central database to transform data into cleaned Silver and Gold tables
- Perform transformations using dbt (Data Build Tool)
- Validate data quality using Great Expectations
- Orchestrate the entire pipeline with Apache Airflow (scheduled daily)
- Analyze data directly from PostgreSQL using any SQL client

## Architecture Diagram

![image](https://github.com/user-attachments/assets/b8074537-c408-444e-81b3-72226b143353)

## Technologies Used

| Tool                   | Purpose                                                  |
| ---------------------- | -------------------------------------------------------- |
| **Airflow**            | Orchestrate and schedule pipeline tasks                  |
| **MinIO**              | S3-compatible object storage for raw data (Bronze layer) |
| **PostgreSQL**         | Central database for transformation and analysis         |
| **dbt**                | SQL-based transformations and data modeling              |
| **Great Expectations** | Data quality testing and validation                      |
| **Docker Compose**     | Manage services in a local containerized environment     |

## Project Structure

```
.
├── dags/                   # Airflow DAGs
│   └── extract_rick_and_morty.py
├── dbt_project/            # dbt project files
│   ├── models/
│   ├── profiles.yml
├── expectations/          # Great Expectations setup
├── logs/                  # Airflow logs
├── plugins/               # Airflow plugins (if any)
├── src/                   # Python helpers (optional)
├── data/
│   └── last_processed.json
├── Dockerfile             # Shared Dockerfile for all Airflow services
├── docker-compose.yml     # Stack definition
├── requirements.txt       # Python dependencies
└── README.md
```

### Step 1: Extraction

- The DAG `extract_rick_and_morty.py` fetches paginated data from:
  - `/api/character`
  - `/api/location`
  - `/api/episode`
- Data is stored as raw JSON in a MinIO bucket under:
  ```
  s3://rickandmorty/raw/character.json
  s3://rickandmorty/raw/location.json
  s3://rickandmorty/raw/episode.json
  ```

## Step 2: Transformation (dbt + PostgreSQL)

- dbt models transform the raw JSON (after loading into Postgres) into clean staging tables:
- `stg_character.sql`, `stg_location.sql`, etc.
- Then dbt builds data marts like:
- `dim_character.sql`, `fact_episode_appearance.sql`
- PostgreSQL acts as the central database for querying and modeling.

## Step 3: Validation (Great Expectations)

- Great Expectations suites validate:
- Nulls, accepted values, uniqueness, formatting
- A DAG task runs `great_expectations checkpoint run`
- The DAG will fail if expectations fail

---

## Docker Services (`docker-compose.yml`)

- **Airflow Webserver** → http://localhost:8080
- **Airflow Scheduler**
- **MinIO Console** → http://localhost:9001 (admin/admin)
- **PostgreSQL** → Database for transformations
- **airflow-init** → Bootstraps Airflow, dbt, and folder setup

---

## ⚙️ Setup Instructions

```bash
# 1. Clone the repo
git clone https://github.com/Redgerd/Portal-Gun-Pipeline
cd portal-gun-pipeline

# 2. Build containers
docker compose build

# 3. Initialize Airflow and DBT
docker compose up airflow-init

# 4. Launch the full stack
docker compose up
```

> Access Airflow UI at: `http://localhost:8080`  
> Access MinIO at: `http://localhost:9001`  
> Username: `minioadmin`  
> Password: `minioadmin123`

## Environment Variables (optional)

Can be added to `.env` or exported directly:

```env
AIRFLOW_UID=50000
_PIP_ADDITIONAL_REQUIREMENTS=""
_AIRFLOW_WWW_USER_USERNAME=airflow
_AIRFLOW_WWW_USER_PASSWORD=airflow
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin123
```

---
