resource "google_project_service" "iam" {
  service            = "iam.googleapis.com"
  disable_on_destroy = false
}

resource "google_service_account" "cloud_build" {
  account_id   = "cloud-build-sa"
  display_name = "Cloud Build service account for the energy pipeline"

  depends_on = [google_project_service.iam]
}

resource "google_project_iam_member" "cloud_build_roles" {
  for_each = toset([
    "roles/logging.logWriter",
    "roles/artifactregistry.writer",
    "roles/storage.objectViewer",
  ])

  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.cloud_build.email}"
}
