resource "google_bigquery_table" "stg_generation_prices" {
  dataset_id          = google_bigquery_dataset.energy.dataset_id
  table_id            = "stg_generation_prices"
  description         = "Silver layer: quarter-hourly data with Berlin time and total renewable generation"
  deletion_protection = false

  view {
    query          = file("${path.module}/../sql/staging/stg_generation_prices.sql")
    use_legacy_sql = false
  }
}

resource "google_bigquery_table" "mart_daily_summary" {
  dataset_id          = google_bigquery_dataset.energy.dataset_id
  table_id            = "mart_daily_summary"
  description         = "Gold layer: one row per day with price and generation indicators"
  deletion_protection = false

  view {
    query          = file("${path.module}/../sql/marts/mart_daily_summary.sql")
    use_legacy_sql = false
  }

  depends_on = [google_bigquery_table.stg_generation_prices]
}
