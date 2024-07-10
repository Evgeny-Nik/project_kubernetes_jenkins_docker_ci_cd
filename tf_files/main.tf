terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.41"
    }
  }
}

#Adding Provider details
provider "aws" {
  region     = var.region
}