terraform {
  backend "s3" {
    bucket         = "tf-kubernetes-jenkins-docker-bucket"
    key            = "terraform.tfstate"
    region         = "eu-north-1"
    dynamodb_table = "terraform-state-lock-dynamo"
    encrypt        = true
  }
}
