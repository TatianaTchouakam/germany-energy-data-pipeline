resource "google_project_service" "cloud_run" {
  service            = "run.googleapis.com"
  disable_on_destroy = false
}

resource "google_service_account" "pipeline" {
  account_id   = "energy-pipeline-sa"
  display_name = "Runtime service account for the energy pipeline job"

  depends_on = [google_project_service.iam]
}

resource "google_storage_bucket_iam_member" "pipeline_bucket" {
  bucket = google_storage_bucket.raw_data.name
  role   = "roles/storage.objectUser"
  member = "serviceAccount:${google_service_account.pipeline.email}"
}

resource "google_bigquery_dataset_iam_member" "pipeline_dataset" {
  dataset_id = google_bigquery_dataset.energy.dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = "serviceAccount:${google_service_account.pipeline.email}"
}

resource "google_project_iam_member" "pipeline_job_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.pipeline.email}"
}

resource "google_cloud_run_v2_job" "fetch_data" {
  name                = "fetch-data"
  location            = var.region
  deletion_protection = false

  template {
    task_count = 1

    template {
      service_account = google_service_account.pipeline.email
      max_retries     = 1
      timeout         = "600s"

      containers {
        image = "europe-west3-docker.pkg.dev/${var.project_id}/energy-pipeline/fetch-data:${var.image_tag}"

        resources {
          limits = {
            cpu    = "1"
            memory = "1Gi"
          }
        }
      }
    }
  }

  depends_on = [
    google_project_service.cloud_run,
    google_storage_bucket_iam_member.pipeline_bucket,
    google_bigquery_dataset_iam_member.pipeline_dataset,
    google_project_iam_member.pipeline_job_user,
  ]
}
