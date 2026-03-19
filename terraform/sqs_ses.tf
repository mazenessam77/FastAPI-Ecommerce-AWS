###############################################################################
# SQS — Order/Checkout Event Queue
###############################################################################

resource "aws_sqs_queue" "order_queue" {
  name                       = "${var.project_name}-order-queue"
  visibility_timeout_seconds = 120
  message_retention_seconds  = 86400  # 1 day
  receive_wait_time_seconds  = 10     # long polling

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.order_dlq.arn
    maxReceiveCount     = 3
  })

  tags = { Name = "${var.project_name}-order-queue" }
}

resource "aws_sqs_queue" "order_dlq" {
  name                      = "${var.project_name}-order-dlq"
  message_retention_seconds = 604800  # 7 days

  tags = { Name = "${var.project_name}-order-dlq" }
}

###############################################################################
# SES — Order Confirmation Emails
###############################################################################

resource "aws_ses_email_identity" "notifications" {
  email = "noreply@ecommerce.example.com"
}

resource "aws_iam_role_policy" "lambda_ses" {
  name = "${var.project_name}-lambda-ses"
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["ses:SendEmail", "ses:SendRawEmail"]
        Resource = "*"
      }
    ]
  })
}
