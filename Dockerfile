FROM apache/airflow:2.7.1-python3.9

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Copy requirements first for cache optimization
COPY requirements.txt .

# Install Python packages including duckdb, dbt, GE, etc.
RUN pip install --no-cache-dir -r requirements.txt

# Copy project folders
COPY dags/ /opt/airflow/dags/
COPY plugins/ /opt/airflow/plugins/
COPY dbt_project/ /opt/airflow/dbt_project/
COPY great_expectations/ /opt/airflow/great_expectations/
