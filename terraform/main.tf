terraform {
  required_version = ">= 1.5"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 7.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_project_service" "storage" {
  service            = "storage.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "bigquery" {
  service            = "bigquery.googleapis.com"
  disable_on_destroy = false
}

resource "google_storage_bucket" "raw_data" {
  name                        = "${var.project_id}-raw"
  location                    = var.region
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  force_destroy               = true

  depends_on = [google_project_service.storage]
}

resource "google_bigquery_dataset" "energy" {
  dataset_id  = "energy"
  location    = var.region
  description = "German wind and solar generation and day-ahead prices"

  depends_on = [google_project_service.bigquery]
}