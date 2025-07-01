FROM apache/airflow:3.0.2-python3.9

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Copy requirements first
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files

# Airflow
COPY dags/ /opt/airflow/dags/
COPY plugins/ /opt/airflow/plugins/
COPY config/ /opt/airflow/config/

COPY dbt_project/ /opt/airflow/dbt_project/
COPY great_expectations/ /opt/airflow/great_expectations/