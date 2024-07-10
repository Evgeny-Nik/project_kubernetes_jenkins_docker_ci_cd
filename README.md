Sure, here is the README updated to reflect your specific project requirements:

---

# CI/CD Project for Containerized Weather App

## Source Code
The project uses a GitLab repository: \
[Weather App Repository](ssh://git@172.31.32.98:50/majestic_potatoes/weather_app.git)

## Jenkins CI/CD Stages
This Jenkins pipeline automates the process of building, tagging, and pushing a Docker image of a Python application, provisioning an AWS EKS cluster using Terraform, deploying the Docker image to EKS, and making the application accessible via an ingress.

## Workflow Overview

### Trigger:
The workflow is triggered via a webhook.

## Pipelines:
The Jenkins pipeline consists of two main pipelines:

1. **Build and Deploy**: This pipeline handles the following tasks:
   - Builds the Docker image from the GitLab repository.
   - Pushes the Docker image to Docker Hub.
   - Updates the `deployment.yaml` file with the new Docker image name.
   - Deploys the Docker image to the EKS cluster.
   - Makes the application accessible via ingress.

2. **Scale Application**: This pipeline adjusts the number of replicas for the deployed application in the EKS cluster.

## Steps

### 1. Pipeline - Build and Deploy

- **Clean Workspace**:
  - Cleans up the workspace and removes any existing Docker containers and images.

- **Prepare Workspace**:
  - Checks out the repository from GitLab.
  - Loads environment variables from a `.env` file.

- **Build Docker Image**:
  - Builds the Docker image using the specified Dockerfile.
  - Tags the Docker image with the build number and latest tag.

- **Push Docker Image to Docker Hub**:
  - Logs in to Docker Hub using credentials.
  - Pushes the newly built Docker image to Docker Hub.

- **Deploy to EKS**:
  - Updates the `deployment.yaml` file with the new Docker image name.
  - Applies the updated deployment file to the EKS cluster using `kubectl`.
  - Makes the application accessible via ingress.

### 2. Pipeline - Scale Application

- **Update Replicas**:
  - Uses the specified parameter to set the desired number of replicas for the deployment.

## Jenkinsfile for Build and Deploy Pipeline

```groovy
pipeline {
    agent any

    stages {
        stage('clean') {
            steps {
                sh '''
                    rm -rf ~/workspace/kubernetes_jenkins_docker_project/*
                    docker 2>/dev/null rm -f $(docker ps -aq) | true
                    docker 2>/dev/null rmi $(docker images -aq) | true
                '''
            }
        }
        stage('Prep workspace') {
            steps {
                git branch: 'master', credentialsId: 'gitlab-ssh', url: 'ssh://git@172.31.32.98:50/majestic_potatoes/weather_app.git'
                dir('weather_app') {
                    withCredentials([file(credentialsId: '.env-file', variable: 'ENV_FILE')]) {
                        writeFile file: '.env', text: readFile(ENV_FILE)
                    }
                }
            }
        }
        stage('Build Containers') {
            steps {
                sh '''docker-compose up --build -d
                docker ps -a
                docker images
                ls -la'''
            }
        }
        stage('Test') {
            steps {
                sh 'python3 weather_app/tests/website_connectivity_unittest.py'
            }
        }
        stage('Upload Container') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub_creds', usernameVariable: 'HUB_USER', passwordVariable: 'HUB_TOKEN')]) {
                    sh '''
                        echo $HUB_TOKEN | docker login -u $HUB_USER --password-stdin
                        docker images
                        docker tag kubernetes_jenkins_docker_project-weather_app $HUB_USER/helm_weather_app:$BUILD_NUMBER
                        docker tag kubernetes_jenkins_docker_project-nginx $HUB_USER/nginx_weather:v1
                        docker images
                        docker push $HUB_USER/helm_weather_app:$BUILD_NUMBER
                        docker push $HUB_USER/nginx_weather:v1
                        docker logout
                    '''
                }
            }
        }
        stage('Deploy to EKS') {
            steps {
                withAWS(credentials: 'eks-admin', region: 'eu-north-1') {
                    sh '''
                    aws eks update-kubeconfig --region eu-north-1 --name pc-eks
                    kubectl get nodes
                    '''
                    sh '''
                        yq -i '.spec.template.spec.containers.[].image = "evgenyniko/helm_weather_app:"+strenv(BUILD_NUMBER)' k8s_files/deployment.yml
                        cat k8s_files/deployment.yml
                        kubectl apply -f k8s_files/deployment.yml
                        kubectl get svc,ingress,deploy,pods
                    '''
                }
            }
        }
    }
}
```

## Multi-Stage Dockerfile

### Build and Tag Image

```bash
docker build -t ${DOCKERHUB_USERNAME}/weather_app:${{env.BUILD_NUMBER}} .
```

### Inside Dockerfile

#### Arguments & Environment Variables

`ENV APP_VERSION` - Get argument for image building

#### Dockerfile Stages

```dockerfile
FROM python:alpine3.19

WORKDIR /home/weather_app_user

COPY ./requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "-m", "gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "wsgi:app"]
```

## Versioning Logic
The project adheres to semantic versioning (Major.Minor.Patch) to ensure a structured and predictable versioning system.

## Links

- [Weather App Repository](ssh://git@172.31.32.98:50/majestic_potatoes/weather_app.git)
- [DockerHub Project Registry](https://hub.docker.com/repository/docker/${DOCKERHUB_USERNAME}/weather_app)

---

This README provides an overview of the CI/CD pipeline setup in Jenkins, including the steps for building and deploying the Docker image, as well as the multi-stage Dockerfile used in the process. Adjust the placeholders such as `${DOCKERHUB_USERNAME}` and repository URLs as per your project specifics.hi
