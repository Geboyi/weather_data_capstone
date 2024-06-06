variable "region" {
  description = "The AWS region where the s3 bucket will be provisioned"
  default = "eu-west-1"
}

variable "s3_bucket_name" {
  description = "The desired name for the s3 bucket"
  default = "trestle-7878-weather-b"
}