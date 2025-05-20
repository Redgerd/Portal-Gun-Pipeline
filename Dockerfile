FROM apache/airflow:2.7.1-python3.9

USER root

# Install system dependencies needed for duckdb, minio CLI, or others (if any)
RUN apt-get update && apt-get install -y \
    curl unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies including duckdb (add duckdb in your requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Copy dags, plugins, and other project folders into image
COPY dags/ /opt/airflow/dags/
COPY plugins/ /opt/airflow/plugins/
COPY dbt_project/ /opt/airflow/dbt_project/
COPY great_expectations/ /opt/airflow/great_expectations/
