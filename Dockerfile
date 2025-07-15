FROM apache/airflow:2.10.5
WORKDIR /opt/airflow
USER root
RUN apt update
COPY requirements.txt /opt/airflow/requirements.txt
USER airflow
RUN pip install --upgrade pip \
	&& pip install --no-cache-dir astronomer-cosmos==1.9.2 dbt-core==1.7.9 dbt-postgres==1.7.9
RUN python -m venv dbt_venv \
	&& source dbt_venv/bin/activate \
	&& pip install --upgrade pip \
	&& pip install --no-cache-dir -r /opt/airflow/requirements.txt