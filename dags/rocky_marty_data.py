from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import boto3
import json
import os

# Configs
MINIO_ENDPOINT = "minio:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin123"
BUCKET_NAME = "rickandmorty"
API_BASE_URL = "https://rickandmortyapi.com/api"

default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry_delay': timedelta(seconds=10),
}

dag = DAG(
    dag_id='extract_rick_and_morty',
    default_args=default_args,
    description='Extract data from Rick and Morty API and store raw JSON in MinIO',
    schedule_interval=None  # Manual runs only
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["rick_and_morty"],
)


def ensure_bucket():
    s3 = boto3.client(
        's3',
        endpoint_url=f"http://{MINIO_ENDPOINT}",
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
    )
    buckets = [b["Name"] for b in s3.list_buckets().get("Buckets", [])]
    if BUCKET_NAME not in buckets:
        s3.create_bucket(Bucket=BUCKET_NAME)


def fetch_and_store_data(endpoint_label: str, endpoint_path: str, **context):
    s3 = boto3.client(
        's3',
        endpoint_url=f"http://{MINIO_ENDPOINT}",
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
    )

    page = 1
    all_data = []
    while True:
        url = f"{API_BASE_URL}/{endpoint_path}?page={page}"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch {url}: {response.status_code}")
        data = response.json()
        all_data.extend(data.get("results", []))

        if data.get("info", {}).get("next") is None:
            break
        page += 1

    # Logging the number of records
    print(f"Fetched {len(all_data)} records from {endpoint_label}")

    # Timestamped filename
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    key = f"raw/{endpoint_label}_{timestamp}.json"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=json.dumps(all_data, indent=2).encode("utf-8"),
        ContentType="application/json",
    )
    print(f"Stored data to MinIO at key: {key}")


with dag:
    ensure_bucket_task = PythonOperator(
        task_id='ensure_bucket_exists',
        python_callable=ensure_bucket,
    )

    extract_characters = PythonOperator(
        task_id='extract_characters',
        python_callable=fetch_and_store_data,
        op_kwargs={
            'endpoint_label': 'characters',
            'endpoint_path': 'character'
        },
    )

    extract_locations = PythonOperator(
        task_id='extract_locations',
        python_callable=fetch_and_store_data,
        op_kwargs={
            'endpoint_label': 'locations',
            'endpoint_path': 'location'
        },
    )

    extract_episodes = PythonOperator(
        task_id='extract_episodes',
        python_callable=fetch_and_store_data,
        op_kwargs={
            'endpoint_label': 'episodes',
            'endpoint_path': 'episode'
        },
    )

