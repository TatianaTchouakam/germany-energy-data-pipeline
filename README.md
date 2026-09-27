# germany-energy-data-pipeline
Automated data pipeline for German electricity generation (wind, solar) and day-ahead prices, built on Google Cloud with Terraform, BigQuery and Cloud Run

## Key Insights

### Solar pushes the day-ahead price down to zero (21 September 2026)

Query used in BigQuery:

```sql
SELECT
  DATETIME(timestamp_utc, "Europe/Berlin") AS time_berlin,
  solar_mw,
  price_eur_mwh
FROM `tatiana-energy-pipeline.energy.generation_prices`
ORDER BY price_eur_mwh
LIMIT 5;
```

**Findings:**
- Between **13:00 and 14:00 (Berlin time)**, the day-ahead price dropped to **0 €/MWh**.
- This matches the **solar peak**: 36,814 MW at 13:15, when wind and solar together produced about 60 GW.
- In contrast, the price reached **194 €/MWh around 07:30** (morning demand peak, before solar ramps up), and stayed around **40 €/MWh at night**.

![Day-ahead price vs. wind and solar generation in Germany, 21 September 2026](docs/images/price_vs_solar_2026-09-21.png)

**Why it matters:**
Wind and solar have near-zero marginal costs. When they cover most of the demand, expensive gas and coal plants are no longer needed and the price collapses (merit order effect). These daily price spreads are what batteries, smart charging and flexible consumption can take advantage of: storing or using electricity when it is cheap, and avoiding the expensive hours.


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
- [BigQuery query syntax (SELECT, ORDER BY, LIMIT)](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax)
- [BigQuery pricing](https://cloud.google.com/bigquery/pricing) – on-demand queries, first 1 TiB per month free


### Visualization
- [pandas.read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html) – reading the processed CSV with `parse_dates`
- [matplotlib fill_between](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.fill_between.html) – solar area under the curve
- [matplotlib twinx](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.twinx.html) – second y-axis for the price
- [matplotlib DateFormatter](https://matplotlib.org/stable/api/dates_api.html#matplotlib.dates.DateFormatter) – hours on the x-axis in Berlin time
- [matplotlib savefig](https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html) – exporting the chart as PNG
- [Images in GitHub Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#images) – embedding the chart in this README