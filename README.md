# germany-energy-data-pipeline
Automated data pipeline for German electricity generation (wind, solar) and day-ahead prices, built on Google Cloud with Terraform, BigQuery and Cloud Run

## Key Insights

### Solar pushes the day-ahead price down to zero (21 September 2026)

![Day-ahead price vs. wind and solar generation in Germany, 21 September 2026](docs/images/price_vs_solar_2026-09-21.png)

**Findings** (all times in Berlin time):
- From **11:45 to 15:45**, the day-ahead price stayed **below 1 €/MWh** for 4 hours in a row, including **105 minutes at exactly 0 €/MWh** between 13:00 and 15:15.
- This window matches the **solar peak**: solar generation stayed between 29 and 37 GW, with a maximum of **36,814 MW at 13:15**.
- The most expensive moments came **when solar was absent**: **257.09 €/MWh at 08:00** (morning peak) and **275.90 €/MWh at 19:45** (evening peak, solar at 0 MW). Four of the five most expensive quarter-hours were in the evening.
- The spread between the cheapest and the most expensive quarter-hour reached **almost 276 €/MWh within a single day**.

**Why it matters:**
Wind and solar have near-zero marginal costs. When they cover most of the demand, expensive gas and coal plants are no longer needed and the price collapses (merit order effect). As soon as the sun sets, demand is still high but solar is gone, and prices spike. These daily price spreads are what batteries, smart charging and flexible consumption can take advantage of: storing or using electricity when it is cheap, and avoiding the expensive hours.

**Queries used in BigQuery:** see [`sql/`](sql/)
- [`cheap_quarter_hours.sql`](sql/cheap_quarter_hours.sql) – quarter-hours below 5 €/MWh
- [`zero_price_window.sql`](sql/zero_price_window.sql) – time window and duration at 0 €/MWh
- [`most_expensive_quarter_hours.sql`](sql/most_expensive_quarter_hours.sql) – five most expensive quarter-hours

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