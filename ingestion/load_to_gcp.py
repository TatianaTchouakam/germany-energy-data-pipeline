"""Upload a daily CSV to Cloud Storage and load it into BigQuery."""
from pathlib import Path

from google.cloud import bigquery, storage

PROJECT_ID = "tatiana-energy-pipeline"
LOCATION = "europe-west3"
BUCKET_NAME = "tatiana-energy-pipeline-raw"
TABLE_ID = f"{PROJECT_ID}.energy.generation_prices"

SCHEMA = [
    bigquery.SchemaField("unix_seconds", "INTEGER"),
    bigquery.SchemaField("wind_offshore_mw", "FLOAT"),
    bigquery.SchemaField("wind_onshore_mw", "FLOAT"),
    bigquery.SchemaField("solar_mw", "FLOAT"),
    bigquery.SchemaField("price_eur_mwh", "FLOAT"),
    bigquery.SchemaField("timestamp_utc", "TIMESTAMP"),
]


def upload_to_gcs(local_path):
    """Copy a local file into the bucket and return its gs:// address."""
    client = storage.Client(project=PROJECT_ID)
    blob_name = f"energy/{Path(local_path).name}"
    client.bucket(BUCKET_NAME).blob(blob_name).upload_from_filename(str(local_path))
    return f"gs://{BUCKET_NAME}/{blob_name}"


def delete_existing_rows(client, first_unix, last_unix):
    """Remove rows already loaded for this time range (makes reloads safe)."""
    query = f"""
        DELETE FROM `{TABLE_ID}`
        WHERE unix_seconds BETWEEN @first_unix AND @last_unix
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("first_unix", "INT64", first_unix),
            bigquery.ScalarQueryParameter("last_unix", "INT64", last_unix),
        ]
    )
    client.query(query, job_config=job_config).result()


def load_to_bigquery(gcs_uri, first_unix, last_unix):
    """Replace this time range in the BigQuery table with the file content."""
    client = bigquery.Client(project=PROJECT_ID, location=LOCATION)
    delete_existing_rows(client, first_unix, last_unix)

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        schema=SCHEMA,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )
    job = client.load_table_from_uri(gcs_uri, TABLE_ID, job_config=job_config)
    job.result()
    return job.output_rows