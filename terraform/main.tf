provider "aws" {
  region = var.region
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_s3_bucket" "weather_data" {
  bucket = var.s3_bucket_name

  tags = {
    Name        = "DataEngProject"
    Environment = "Dev"
  }
}