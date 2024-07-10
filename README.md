# Kubernetes + Jenkins CI/CD Project for a Containerized Weather App

## Project Overview

This project demonstrates a CI/CD pipeline using Jenkins, Docker, and Kubernetes. \
It involves setting up an EKS cluster with Terraform, deploying a Containerized application, and managing Kubernetes deployments. \
The goal is to provide a robust pipeline for continuous integration and continuous deployment.

## Application
This project uses a Flask weather application that communicates with http requests to a remote REST API (visualcrossing). \
Exposed on kubernetes through ClusterIp and Ingress.

## Jenkins Agent Requirements

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Kubernetes**: [Install kubectl](https://kubernetes.io/docs/tasks/tools/)
- **Jenkins**: [Install Jenkins](https://www.jenkins.io/doc/book/installing/)
- **Terraform**: [Install Terraform](https://www.terraform.io/downloads.html)
- **AWS CLI**: [Install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)


### Configure Jenkins

Set up Jenkins with the necessary plugins for Docker, Kubernetes, AWS, and GitHub. \
Add your pipelines in Jenkins using the provided Jenkinsfiles.

## Jenkins Pipelines Overview
There are a total of 4 Jenkins Pipelines
- init: handles the initialization and provisioning of the AWS infrastructure using Terraform.
- select: triggered via github webhook, determines which subsequent pipeline (CI or CD) to trigger based on the changes detected in the repository.
- ci: handles the continuous integration process (and delivery), including building, testing, and pushing Docker images.
- cd: handles the continuous deployment process, deploying the Docker images to the Kubernetes cluster, exposing them through Ingress.

## Pipeline Steps

### `init`

- **Checkout**: Clones the repository from GitHub.
- **Terraform Init**: Initializes Terraform in the `tf_files` directory.
- **Terraform Plan**: Creates a Terraform execution plan.
- **Terraform Apply**: Applies the Terraform plan to provision the infrastructure.
- **Post Apply**: Retrieves and displays the EKS cluster name from Terraform output.

### `select`

- **Checkout**: Clones the repository from GitHub.
- **Determine Changed Files**: Analyzes the changes in the repository to decide which pipeline to trigger.
  - Triggers the CI pipeline if changes are detected in the application or CI-related files.
  - Triggers the CD pipeline if changes are detected in the deployment or CD-related files.
  - If no relevant changes are detected, no pipelines are triggered.

### `ci`

- **Clean Workspace**: Cleans the Jenkins workspace and removes any existing Docker containers and images.
- **Prep Workspace**: Clones the repository and sets up the application environment.
- **Increment Version**: Increments the application version and pushes the changes to the repository.
- **Build Docker Image**: Builds the Docker image and tags it with the new version and `latest`.
- **Test Application**: Runs tests on the Docker container to ensure the application works as expected.
- **Push Docker Image**: Pushes the Docker image to DockerHub (Delivery).
- **Edit Manifest Files**: Updates the Kubernetes deployment manifest with the new Docker image version and pushes the changes to the repository.

### `cd`

- **Check Changes**: Clones the repository from GitHub.
- **Read Replicas from Deployment YAML**: Reads the number of replicas from the Kubernetes deployment YAML file.
- **Configure AWS and Kubernetes**: Configures AWS and Kubernetes settings and applies the Kubernetes manifests to deploy the application.

## Versioning Logic
The project adheres to semantic versioning (Major.Minor.Patch) to ensure a structured and predictable versioning system.

## Links
- [DockerHub Project Registry](https://hub.docker.com/repository/docker/evgenyniko/kubernetes_weather_app)