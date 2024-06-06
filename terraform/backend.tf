terraform {
  backend "s3" {
    bucket  = "technologiesoutcomes-7878-terraform-backend"
    encrypt = true
    key     = "weather_data_p/terraform.tfstate"
    region  = "eu-west-1"
  }
}