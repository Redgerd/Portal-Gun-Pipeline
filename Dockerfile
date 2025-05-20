FROM apache/airflow:2.7.1-python3.9

USER root

# Copy only requirements.txt first (cache this layer if requirements.txt unchanged)
COPY requirements.txt .

# Install dependencies only if requirements.txt changes (cached otherwise)
RUN pip install --no-cache-dir -r requirements.txt

USER airflow

# Copy the rest of the project files (changes here won't invalidate cached pip install)
COPY dags/ /opt/airflow/dags/
COPY plugins/ /opt/airflow/plugins/
COPY dbt_project/ /opt/airflow/dbt_project/
COPY great_expectations/ /opt/airflow/great_expectations/
