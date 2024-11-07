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

variable "image_tag" {
  description = "Tag of the Docker image"
  default     = "latest"
}

variable "service_name" {
  description = "Name of the Cloud Run service"
  default     = "ClassificationService"
}

variable "dockerfile_dir" {
  description = "Directory containing the Dockerfile"
  type        = string
  default     = "."
}


# Configure the Google Cloud provider
provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable required APIs
resource "google_project_service" "container_registry_api" {
  service            = "containerregistry.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloud_run_api" {
  service            = "run.googleapis.com"
  disable_on_destroy = false
}

# Build and push Docker image

terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 2.15.0"
    }
  }
  required_version = ">= 0.14"
}

# Configure the Docker provider
provider "docker" {
  registry_auth {
    address  = "gcr.io"
    username = "oauth2accesstoken"
    password = data.google_client_config.default.access_token
  }
}

# Get the default Google client configuration
data "google_client_config" "default" {}

# Define the Docker image resource
resource "docker_image" "app" {
  name = "gcr.io/${var.project_id}/${var.image_name}:${var.image_tag}"
  build {
    path="Dockerfile"
    dockerfile = "Dockerfile"
  }
}

# Push the Docker image to GCR
resource "docker_registry_image" "app" {
  name = docker_image.app.name
}

# Deploy to Cloud Run
resource "google_cloud_run_v2_service" "default" {
  name     = var.service_name
  location = var.region

  template {
    containers {
      image = "gcr.io/${var.project_id}/${var.image_name}:${var.image_tag}"
    }
  }

  traffic {
    percent = 100
  }

  depends_on = [
    google_project_service.cloud_run_api,
    docker_registry_image.docker_build_push
  ]
}

# Make the service publicly accessible
resource "google_cloud_run_service_iam_member" "public_access" {
  service  = google_cloud_run_v2_service.default.name
  location = google_cloud_run_v2_service.default.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Output the service URL
output "service_url" {
  value = google_cloud_run_v2_service.default.uri
}

