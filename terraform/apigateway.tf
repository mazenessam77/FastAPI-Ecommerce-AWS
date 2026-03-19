###############################################################################
# API Gateway — REST API Entry Point with JWT Authorizer
###############################################################################

resource "aws_apigatewayv2_api" "main" {
  name          = "${var.project_name}-api"
  protocol_type = "HTTP"
  description   = "E-Commerce API Gateway — routes to Lambda microservices"

  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allow_headers = ["Content-Type", "Authorization", "refresh_token"]
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
      requestId      = "$context.requestId"
      ip             = "$context.identity.sourceIp"
      requestTime    = "$context.requestTime"
      httpMethod     = "$context.httpMethod"
      routeKey       = "$context.routeKey"
      status         = "$context.status"
      protocol       = "$context.protocol"
      responseLength = "$context.responseLength"
      integrationError = "$context.integrationErrorMessage"
    })
  }
}

# ── JWT Authorizer ──

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

# Auth routes (no authorizer needed)
resource "aws_apigatewayv2_route" "auth" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "ANY /auth/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.microservice["auth"].id}"
}

# Users routes (JWT protected)
resource "aws_apigatewayv2_route" "users" {
  api_id             = aws_apigatewayv2_api.main.id
  route_key          = "ANY /users/{proxy+}"
  target             = "integrations/${aws_apigatewayv2_integration.microservice["users"].id}"
  authorization_type = "CUSTOM"
  authorizer_id      = aws_apigatewayv2_authorizer.jwt.id
}

# Products routes — GET is public, writes (POST/PUT/DELETE) require JWT
resource "aws_apigatewayv2_route" "products_read" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "GET /products/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.microservice["products"].id}"
}

resource "aws_apigatewayv2_route" "products_write" {
  api_id             = aws_apigatewayv2_api.main.id
  route_key          = "ANY /products/{proxy+}"
  target             = "integrations/${aws_apigatewayv2_integration.microservice["products"].id}"
  authorization_type = "CUSTOM"
  authorizer_id      = aws_apigatewayv2_authorizer.jwt.id
}

# Categories routes — GET is public, writes require JWT
resource "aws_apigatewayv2_route" "categories_read" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "GET /categories/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.microservice["categories"].id}"
}

resource "aws_apigatewayv2_route" "categories_write" {
  api_id             = aws_apigatewayv2_api.main.id
  route_key          = "ANY /categories/{proxy+}"
  target             = "integrations/${aws_apigatewayv2_integration.microservice["categories"].id}"
  authorization_type = "CUSTOM"
  authorizer_id      = aws_apigatewayv2_authorizer.jwt.id
}

# Carts routes (JWT protected)
resource "aws_apigatewayv2_route" "carts" {
  api_id             = aws_apigatewayv2_api.main.id
  route_key          = "ANY /carts/{proxy+}"
  target             = "integrations/${aws_apigatewayv2_integration.microservice["carts"].id}"
  authorization_type = "CUSTOM"
  authorizer_id      = aws_apigatewayv2_authorizer.jwt.id
}

# Account/profile routes (JWT protected) — was missing entirely
resource "aws_apigatewayv2_route" "me" {
  api_id             = aws_apigatewayv2_api.main.id
  route_key          = "ANY /me/{proxy+}"
  target             = "integrations/${aws_apigatewayv2_integration.microservice["users"].id}"
  authorization_type = "CUSTOM"
  authorizer_id      = aws_apigatewayv2_authorizer.jwt.id
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
