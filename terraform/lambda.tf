###############################################################################
# Lambda — Serverless Microservices (Container Images)
# Each Lambda represents a microservice endpoint group.
###############################################################################

# ── IAM Role for all Lambda functions ──

resource "aws_iam_role" "lambda_exec" {
  name = "${var.project_name}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_vpc" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_iam_role_policy" "lambda_secrets" {
  name = "${var.project_name}-lambda-secrets"
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = [
          aws_secretsmanager_secret.db_credentials.arn,
          aws_secretsmanager_secret.jwt_secret.arn,
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_sqs" {
  name = "${var.project_name}-lambda-sqs"
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "sqs:SendMessage",
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ]
        Resource = [aws_sqs_queue.order_queue.arn]
      }
    ]
  })
}

# ── Lambda Functions (Container Image) ──

locals {
  lambda_common = {
    role          = aws_iam_role.lambda_exec.arn
    package_type  = "Image"
    image_uri     = "${aws_ecr_repository.api.repository_url}:latest"
    memory_size   = var.lambda_memory
    timeout       = var.lambda_timeout
    architectures = ["x86_64"]
  }

  lambda_env_vars = {
    db_username                 = var.db_username
    db_password                 = var.db_password
    db_hostname                 = aws_db_instance.postgres.address
    db_port                     = tostring(aws_db_instance.postgres.port)
    db_name                     = var.db_name
    secret_key                  = var.jwt_secret_key
    algorithm                   = var.jwt_algorithm
    access_token_expire_minutes = tostring(var.access_token_expire_minutes)
    DB_SECRET_ARN               = aws_secretsmanager_secret.db_credentials.arn
    SQS_QUEUE_URL               = aws_sqs_queue.order_queue.url
  }

  microservices = {
    auth       = { description = "Authentication microservice — signup, login, refresh" }
    users      = { description = "User management microservice — admin CRUD" }
    products   = { description = "Product catalog microservice — CRUD + search" }
    categories = { description = "Category management microservice" }
    carts      = { description = "Shopping cart microservice — cart + checkout" }
  }
}

resource "aws_lambda_function" "microservice" {
  for_each = local.microservices

  function_name = "${var.project_name}-${each.key}"
  description   = each.value.description
  role          = local.lambda_common.role
  package_type  = local.lambda_common.package_type
  image_uri     = local.lambda_common.image_uri
  memory_size   = local.lambda_common.memory_size
  timeout       = local.lambda_common.timeout
  architectures = local.lambda_common.architectures

  vpc_config {
    subnet_ids         = [aws_subnet.private_a.id, aws_subnet.private_b.id]
    security_group_ids = [aws_security_group.lambda_sg.id]
  }

  environment {
    variables = local.lambda_env_vars
  }

  tags = { Microservice = each.key }

  depends_on = [aws_db_instance.postgres]
}

# ── Background Worker Lambda (SQS consumer) ──

resource "aws_lambda_function" "worker" {
  function_name = "${var.project_name}-worker"
  description   = "Background worker — processes order events from SQS"
  role          = aws_iam_role.lambda_exec.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.api.repository_url}:latest"
  memory_size   = 256
  timeout       = 60
  architectures = ["x86_64"]

  vpc_config {
    subnet_ids         = [aws_subnet.private_a.id, aws_subnet.private_b.id]
    security_group_ids = [aws_security_group.lambda_sg.id]
  }

  environment {
    variables = merge(local.lambda_env_vars, {
      HANDLER_TYPE = "worker"
    })
  }

  tags = { Microservice = "worker" }
}

resource "aws_lambda_event_source_mapping" "sqs_worker" {
  event_source_arn = aws_sqs_queue.order_queue.arn
  function_name    = aws_lambda_function.worker.arn
  batch_size       = 10
  enabled          = true
}
