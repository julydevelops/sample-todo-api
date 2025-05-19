resource "aws_api_gateway_rest_api" "todo_api" {
  name        = "todo-api"
  description = "Serverless Todo API"
}

# catch-all proxy
resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.todo_api.id
  parent_id   = aws_api_gateway_rest_api.todo_api.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy_any" {
  rest_api_id   = aws_api_gateway_rest_api.todo_api.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "proxy_integration" {
  rest_api_id             = aws_api_gateway_rest_api.todo_api.id
  resource_id             = aws_api_gateway_resource.proxy.id
  http_method             = aws_api_gateway_method.proxy_any.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.todo_handler.invoke_arn
}

resource "aws_api_gateway_deployment" "deployment" {
  depends_on = [
    aws_api_gateway_integration.proxy_integration
  ]

  rest_api_id = aws_api_gateway_rest_api.todo_api.id

  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.todo_api.body))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "dev_stage" {
  stage_name    = "dev"
  rest_api_id   = aws_api_gateway_rest_api.todo_api.id
  deployment_id = aws_api_gateway_deployment.deployment.id
}