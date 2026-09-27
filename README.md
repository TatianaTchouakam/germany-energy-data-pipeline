# germany-energy-data-pipeline
Automated data pipeline for German electricity generation (wind, solar) and day-ahead prices, built on Google Cloud with Terraform, BigQuery and Cloud Run


## Documentation & References

### Data source
- [Energy-Charts API (Fraunhofer ISE)](https://api.energy-charts.info/) – electricity generation and day-ahead prices, license CC BY 4.0

### Python
- [requests](https://requests.readthedocs.io/) – calling the API
- [pandas.to_datetime](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html) – converting Unix timestamps
- [pandas.DataFrame.merge](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html) – joining generation and prices
- [argparse](https://docs.python.org/3/library/argparse.html) – command-line options (`--date`)

### Google Cloud setup
- [gcloud projects create](https://cloud.google.com/sdk/gcloud/reference/projects/create)
- [gcloud billing projects link](https://cloud.google.com/sdk/gcloud/reference/billing/projects/link)
- [Application Default Credentials (ADC)](https://cloud.google.com/docs/authentication/application-default-credentials)
- [Budgets and budget alerts](https://cloud.google.com/billing/docs/how-to/budgets)

### Terraform
- [Terraform CLI commands (init, plan, apply)](https://developer.hashicorp.com/terraform/cli/commands)
- [Google provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [google_project_service](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/google_project_service)
- [google_storage_bucket](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket)
- [google_bigquery_dataset](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset)

### Cloud Storage & BigQuery
- [gcloud storage cp](https://cloud.google.com/sdk/gcloud/reference/storage/cp) – uploading files to Cloud Storage
- [Loading CSV data from Cloud Storage](https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv)
- [bq load reference](https://cloud.google.com/bigquery/docs/reference/bq-cli-reference#bq_load)
- [BigQuery DATETIME function](https://cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions#datetime) – converting UTC to Berlin time