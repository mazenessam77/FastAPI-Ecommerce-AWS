###############################################################################
# Terraform — AWS Serverless E-Commerce Infrastructure
# Provisions: VPC, RDS PostgreSQL, Lambda (container), API Gateway,
#             SQS, SES, CloudWatch, ECR, Secrets Manager, CloudFront + S3
###############################################################################

terraform {
  required_version = ">= 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "ecommerce-terraform-state-541405370428"
    key    = "serverless-ecommerce/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "ecommerce-api"
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

# ─────────────────────────────────────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────────────────────────────────────

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
