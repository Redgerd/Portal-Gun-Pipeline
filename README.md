# Rick & Morty Portal Gun Pipeline
 
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

| Tool               | Purpose                                                   |
|--------------------|-----------------------------------------------------------|
| **Airflow**        | Orchestration of the ETL pipeline                         |
| **MinIO**          | S3-compatible object storage for raw data                 |
| **DuckDB**         | Local columnar database for transformations               |
| **dbt**            | SQL-based transformation and modeling                     |
| **Great Expectations** | Data quality testing and validation                     |
| **Docker Compose** | Containerized local environment                           |

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

### Step 2: Transformation (dbt + DuckDB)

- dbt models transform raw JSON into clean staging tables:
  - `stg_character.sql`, `stg_location.sql`, etc.
- Then they build marts like:
  - `dim_character.sql`, `fact_episode_appearance.sql`
- DuckDB is used as the target database (`.duckdb` file persisted locally).

### Step 3: Validation (Great Expectations)

- GE suites validate:
  - Nulls, accepted values, uniqueness, format correctness
- A DAG task runs `great_expectations checkpoint run`
- DAG fails if validations fail

---

## Docker Services (`docker-compose.yml`)

- **Airflow Webserver** → http://localhost:8080
- **MinIO Console** → http://localhost:9001 (admin/admin)
- **Airflow Scheduler**
- **DuckDB CLI** (mounted for interaction)
- **airflow-init** → Bootstraps DB, user, folders

---

## ⚙️ Setup Instructions

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd portal-gun-pipeline

# 2. Build containers
docker compose build

# 3. Initialize Airflow
docker compose up airflow-init

# 4. Run the stack
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
```

---

