resource "google_project_service" "cloud_scheduler" {
  service            = "cloudscheduler.googleapis.com"
  disable_on_destroy = false
}

resource "google_service_account" "scheduler" {
  account_id   = "scheduler-sa"
  display_name = "Cloud Scheduler service account that triggers the pipeline job"

  depends_on = [google_project_service.iam]
}

resource "google_cloud_run_v2_job_iam_member" "scheduler_invoker" {
  name     = google_cloud_run_v2_job.fetch_data.name
  location = google_cloud_run_v2_job.fetch_data.location
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.scheduler.email}"
}

resource "google_cloud_scheduler_job" "daily_fetch" {
  name        = "daily-fetch-data"
  description = "Runs the energy pipeline every morning for the previous day"
  region      = var.region
  schedule    = "0 7 * * *"
  time_zone   = "Europe/Berlin"

  http_target {
    http_method = "POST"
    uri         = "https://run.googleapis.com/v2/projects/${var.project_id}/locations/${var.region}/jobs/${google_cloud_run_v2_job.fetch_data.name}:run"

    oauth_token {
      service_account_email = google_service_account.scheduler.email
    }
  }

  depends_on = [
    google_project_service.cloud_scheduler,
    google_cloud_run_v2_job_iam_member.scheduler_invoker,
  ]
}
