# Configure the Google Cloud provider
provider "google" {
  project = var.project_id
  region  = var.region
}


terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }
  }
  required_version = ">= 1.9.8"
}
#
# # Configure the Docker provider
# provider "docker" {
#   registry_auth {
#     address  = "gcr.io"
#     username = "oauth2accesstoken"
#     password = data.google_client_config.default.access_token
#   }
# }

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

# # Build and push Docker image
# resource "docker_image" "app" {
#   name = "gcr.io/${var.project_id}/${var.image_name}:latest"
#   build {
#       context    = ".."
#     dockerfile = "Dockerfile"
#     platform   = "linux/amd64"
#     build_args = {
#       BUILDKIT_INLINE_CACHE = "1"
#     }
#   }
# }


# resource "docker_registry_image" "app" {
#   name = docker_image.app.name
#   keep_remotely=true
#   depends_on = [docker_image.app]
#
# }

# Deploy to Cloud Run
resource "google_cloud_run_service" "app" {
  name     = "my-app-service"
  location = var.region

  template {
    spec {
      containers {
#         image = docker_registry_image.app.name
image="gcr.io/herondatabackendexercise/classification_service_image"
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