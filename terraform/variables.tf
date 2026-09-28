variable "project_id" {
  description = "Google Cloud project ID"
  type        = string
  default     = "tatiana-energy-pipeline"
}

variable "region" {
  description = "Region for all resources (Frankfurt)"
  type        = string
  default     = "europe-west3"
}
variable "image_tag" {
  description = "Version of the pipeline container image to deploy"
  type        = string
  default     = "v2"
}
