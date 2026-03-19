###############################################################################
# Outputs
###############################################################################

output "api_gateway_url" {
  description = "API Gateway invoke URL"
  value       = aws_apigatewayv2_api.main.api_endpoint
}

output "ecr_repository_url" {
  description = "ECR repository URL for backend Docker images"
  value       = aws_ecr_repository.api.repository_url
}

output "rds_endpoint" {
  description = "RDS PostgreSQL endpoint"
  value       = aws_db_instance.postgres.endpoint
  sensitive   = true
}

output "sqs_queue_url" {
  description = "SQS order queue URL"
  value       = aws_sqs_queue.order_queue.url
}

output "s3_bucket_name" {
  description = "S3 static assets bucket name"
  value       = aws_s3_bucket.static_assets.id
}

# ── Frontend Outputs ──

output "frontend_ecr_url" {
  description = "ECR repository URL for frontend images"
  value       = aws_ecr_repository.frontend.repository_url
}

output "frontend_alb_dns" {
  description = "Frontend ALB DNS name (production URL)"
  value       = aws_lb.frontend.dns_name
}

output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = aws_ecs_cluster.main.name
}
