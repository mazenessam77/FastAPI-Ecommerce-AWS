###############################################################################
# Variables
###############################################################################

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "production"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "ecommerce"
}

# ── Database ──

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_name" {
  description = "PostgreSQL database name"
  type        = string
  default     = "ecommerce_db"
}

variable "db_username" {
  description = "Database master username"
  type        = string
  default     = "ecommerce_admin"
  sensitive   = true
}

variable "db_password" {
  description = "Database master password"
  type        = string
  sensitive   = true
}

# ── JWT ──

variable "jwt_secret_key" {
  description = "Secret key for JWT token signing"
  type        = string
  sensitive   = true
}

variable "jwt_algorithm" {
  description = "JWT signing algorithm"
  type        = string
  default     = "HS256"
}

variable "access_token_expire_minutes" {
  description = "JWT access token expiry in minutes"
  type        = number
  default     = 30
}

# ── Seed ──

variable "seed_secret" {
  description = "Secret key required to call the /orders/seed endpoint"
  type        = string
  sensitive   = true
  default     = "change-me-in-prod"
}

# ── Lambda ──

variable "lambda_memory" {
  description = "Lambda memory size in MB"
  type        = number
  default     = 512
}

variable "lambda_timeout" {
  description = "Lambda timeout in seconds"
  type        = number
  default     = 30
}
