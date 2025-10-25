terraform {
  backend "s3" {
    bucket  = "mlops-tfstate-maksymp"
    key     = "global/l11/ecr/terraform.tfstate"
    region  = "us-east-1"
    encrypt = true
    profile = "goit-terraform"
  }
}