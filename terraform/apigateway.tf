###############################################################################
# API Gateway — HTTP API routes to Lambda microservices
# JWT validation is handled inside each FastAPI Lambda (HTTPBearer + get_current_user).
# API Gateway just routes — no custom authorizer needed.
###############################################################################

resource "aws_apigatewayv2_api" "main" {
  name          = "${var.project_name}-api"
  protocol_type = "HTTP"
  description   = "E-Commerce API Gateway — routes to Lambda microservices"

  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allow_headers = ["Content-Type", "Authorization", "refresh_token", "x-seed-key"]
    max_age       = 3600
  }
}

resource "aws_apigatewayv2_stage" "prod" {
  api_id      = aws_apigatewayv2_api.main.id
  name        = "$default"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.apigw.arn
    format = jsonencode({
      requestId        = "$context.requestId"
      ip               = "$context.identity.sourceIp"
      requestTime      = "$context.requestTime"
      httpMethod       = "$context.httpMethod"
      routeKey         = "$context.routeKey"
      status           = "$context.status"
      protocol         = "$context.protocol"
      responseLength   = "$context.responseLength"
      integrationError = "$context.integrationErrorMessage"
    })
  }
}

# ── JWT Authorizer (kept to avoid destroy conflict — not referenced by any route) ──
# Routes no longer use this authorizer; FastAPI validates JWT internally.
# Safe to manually delete via console after this apply completes.
resource "aws_apigatewayv2_authorizer" "jwt" {
  api_id           = aws_apigatewayv2_api.main.id
  name             = "${var.project_name}-jwt-authorizer"
  authorizer_type  = "REQUEST"
  authorizer_uri   = aws_lambda_function.microservice["auth"].invoke_arn

  authorizer_payload_format_version = "2.0"
  enable_simple_responses           = true
}

# ── Route → Lambda Integrations ──

resource "aws_apigatewayv2_integration" "microservice" {
  for_each = local.microservices

  api_id                 = aws_apigatewayv2_api.main.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.microservice[each.key].invoke_arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

# Auth routes — public (login, signup, refresh)
resource "aws_apigatewayv2_route" "auth" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "ANY /auth/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.microservice["auth"].id}"
}

# Users routes — FastAPI enforces JWT + admin role internally
resource "aws_apigatewayv2_route" "users" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "ANY /users/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.microservice["users"].id}"
}

# Account/profile routes — FastAPI enforces JWT internally
resource "aws_apigatewayv2_route" "me" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "ANY /me/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.microservice["users"].id}"
}

# Products routes — GET is public, writes require JWT (enforced in FastAPI)
resource "aws_apigatewayv2_route" "products" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "ANY /products/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.microservice["products"].id}"
}

# Categories routes — GET is public, writes require JWT (enforced in FastAPI)
resource "aws_apigatewayv2_route" "categories" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "ANY /categories/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.microservice["categories"].id}"
}

# Carts routes — JWT enforced in FastAPI
resource "aws_apigatewayv2_route" "carts" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "ANY /carts/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.microservice["carts"].id}"
}

# Orders routes — JWT enforced in FastAPI; /orders/seed uses x-seed-key header
resource "aws_apigatewayv2_route" "orders" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "ANY /orders/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.microservice["orders"].id}"
}

# ── Lambda Permissions for API Gateway ──

resource "aws_lambda_permission" "apigw" {
  for_each = local.microservices

  statement_id  = "AllowAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.microservice[each.key].function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}
