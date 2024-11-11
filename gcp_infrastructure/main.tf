# Configure the Google Cloud provider
provider "google" {
  project = var.project_id
  region  = var.region
}



# Get the default Google client configuration
data "google_client_config" "default" {}

# Variables
variable "project_id" {
  description = "ID of our Google Cloud Project"
  default     = "herondatabackendexercise"
}


variable "region" {
  description = "Google Cloud region"
  default     = "europe-west2"
}

variable "image_name" {
  description = "Name of the Docker image"
  default     = "classification_service_image"
}

# Enable required APIs
resource "google_project_service" "services" {
  for_each = toset([
    "containerregistry.googleapis.com",
    "run.googleapis.com",
  ])
  service = each.key
  disable_on_destroy = false
}



# Deploy to Cloud Run
resource "google_cloud_run_service" "app" {
  name     = "document-classification-service"
  location = var.region

  template {
    spec {
      containers {
          image="gcr.io/herondatabackendexercise/classification_service_image:latest"

        resources {
          limits = {
            memory = "32Gi"   # Set memory limit to 20GB
            cpu    = "8"      # Set CPU limit to 8 vCPU
          }
        }
      }
      }
    }


  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [
    google_project_service.services["run.googleapis.com"],
#     docker_registry_image.app
  ]
}

# Make the service publicly accessible
resource "google_cloud_run_service_iam_member" "public_access" {
  service  = google_cloud_run_service.app.name
  location = google_cloud_run_service.app.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Output the service URL
output "service_url" {
  value = google_cloud_run_service.app.status[0].url
}