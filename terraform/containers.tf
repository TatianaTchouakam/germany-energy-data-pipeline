resource "google_project_service" "artifact_registry" {
  service            = "artifactregistry.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloud_build" {
  service            = "cloudbuild.googleapis.com"
  disable_on_destroy = false
}

resource "google_artifact_registry_repository" "pipeline" {
  repository_id = "energy-pipeline"
  location      = var.region
  format        = "DOCKER"
  description   = "Container images for the energy data pipeline"

  depends_on = [google_project_service.artifact_registry]
}