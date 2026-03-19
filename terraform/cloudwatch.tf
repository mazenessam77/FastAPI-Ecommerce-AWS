###############################################################################
# CloudWatch — Centralized Logging & Monitoring
###############################################################################

# ── API Gateway Logs ──

resource "aws_cloudwatch_log_group" "apigw" {
  name              = "/aws/apigateway/${var.project_name}-api"
  retention_in_days = 30

  tags = { Name = "${var.project_name}-apigw-logs" }
}

# ── Lambda Log Groups ──

resource "aws_cloudwatch_log_group" "lambda" {
  for_each = local.microservices

  name              = "/aws/lambda/${var.project_name}-${each.key}"
  retention_in_days = 14

  tags = { Microservice = each.key }
}

resource "aws_cloudwatch_log_group" "worker" {
  name              = "/aws/lambda/${var.project_name}-worker"
  retention_in_days = 14

  tags = { Microservice = "worker" }
}

# ── CloudWatch Alarms ──

resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  for_each = local.microservices

  alarm_name          = "${var.project_name}-${each.key}-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 5
  alarm_description   = "Lambda ${each.key} error count exceeded threshold"

  dimensions = {
    FunctionName = aws_lambda_function.microservice[each.key].function_name
  }
}

resource "aws_cloudwatch_metric_alarm" "rds_cpu" {
  alarm_name          = "${var.project_name}-rds-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 3
  metric_name         = "CPUUtilization"
  namespace           = "AWS/RDS"
  period              = 300
  statistic           = "Average"
  threshold           = 80
  alarm_description   = "RDS CPU utilization exceeded 80%"

  dimensions = {
    DBInstanceIdentifier = aws_db_instance.postgres.identifier
  }
}

resource "aws_cloudwatch_metric_alarm" "sqs_dlq" {
  alarm_name          = "${var.project_name}-dlq-messages"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "ApproximateNumberOfMessagesVisible"
  namespace           = "AWS/SQS"
  period              = 300
  statistic           = "Sum"
  threshold           = 0
  alarm_description   = "Messages appearing in dead letter queue"

  dimensions = {
    QueueName = aws_sqs_queue.order_dlq.name
  }
}
