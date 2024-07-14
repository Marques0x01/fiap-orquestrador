terraform {
  backend "s3" {
    bucket         = "backend-projeto"
    key            = "fiap_orquestrador/terraform.tfstate"
    region         = "us-east-2"
    
  }
}
