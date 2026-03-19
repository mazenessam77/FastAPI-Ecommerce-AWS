###############################################################################
# Secrets Manager — Database Credentials & JWT Secret
###############################################################################

resource "aws_secretsmanager_secret" "db_credentials" {
  name                    = "${var.project_name}/db-credentials"
  description             = "PostgreSQL database credentials for E-Commerce API"
  recovery_window_in_days = 7

  tags = { Name = "${var.project_name}-db-secret" }
}

resource "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = aws_secretsmanager_secret.db_credentials.id

  secret_string = jsonencode({
    db_username = var.db_username
    db_password = var.db_password
    db_hostname = aws_db_instance.postgres.address
    db_port     = tostring(aws_db_instance.postgres.port)
    db_name     = var.db_name
  })
}

resource "aws_secretsmanager_secret" "jwt_secret" {
  name                    = "${var.project_name}/jwt-secret"
  description             = "JWT signing secret for E-Commerce API"
  recovery_window_in_days = 7

  tags = { Name = "${var.project_name}-jwt-secret" }
}

resource "aws_secretsmanager_secret_version" "jwt_secret" {
  secret_id = aws_secretsmanager_secret.jwt_secret.id

  secret_string = jsonencode({
    secret_key                  = var.jwt_secret_key
    algorithm                   = var.jwt_algorithm
    access_token_expire_minutes = var.access_token_expire_minutes
  })
}
