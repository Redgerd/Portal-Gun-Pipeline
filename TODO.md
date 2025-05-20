# TODO – Portal Gun Pipeline

## Project Setup

- [x] Add `docker-compose.yml` for:
  - Apache Airflow
  - MinIO
  - Duck DB
- [x] Make `Docker` file:

- [x] Folders:
  - `dags/`
  - `plugins/`
  - `logs/`
  - `dbt_project/`
  - `expectations/`

## ETL Workflow (Airflow DAG)

- [ ] Write DAG `dags/extract_rick_and_morty.py`
  - [ ] Task: Extract data from `/api/character`, `/api/location`, `/api/episode`
  - [ ] Task: Store raw JSON in MinIO bucket under `raw/`
  - [ ] Task: Paginate through API until all pages are fetched
- [ ] Add error handling & retries to DAG tasks
- [ ] Register DAG in Airflow (ensure `airflow webserver` picks it up)

## Data Modeling (dbt)

- [ ] Initialize dbt project inside `dbt_project/`
- [ ] Create staging models in `dbt_project/models/staging/`:
  - `stg_character.sql`
  - `stg_location.sql`
  - `stg_episode.sql`
- [ ] Create marts in `dbt_project/models/marts/`:
  - `dim_character.sql`
  - `fact_episode_appearance.sql`
- [ ] Configure `profiles.yml` for DuckDB and MinIO paths
- [ ] Add Airflow task to run `dbt run` after extraction

## Data Quality (Great Expectations)

- [ ] Initialize GE project in `expectations/`
- [ ] Create expectation suites:
  - Character suite (nulls, accepted values for `status`, etc.)
  - Location suite (nulls, unique constraints)
  - Episode suite (row counts, date formats)
- [ ] Add GE checkpoint YAML configs
- [ ] Add Airflow task to execute `great_expectations checkpoint run`
- [ ] Fail DAG run if any expectations fail

## Local Access & Validation

- [ ] Run `docker-compose up`
- [ ] Access Airflow UI: http://localhost:8080 (username/password as configured)
- [ ] Access MinIO Console: http://localhost:9001
  - Credentials: `minioadmin` / `minioadmin`
- [ ] Verify raw JSON in MinIO bucket (`raw/character/...`)
