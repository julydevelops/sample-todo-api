data "aws_s3_object" "lambda_zip" {
  bucket = var.lambda_bucket
  key    = var.lambda_key
}

resource "aws_lambda_function" "todo_handler" {
  function_name = "todo-api"
  runtime       = "python3.12"
  handler       = "handler.lambda_handler"

  role = aws_iam_role.todo_lambda.arn

  s3_bucket        = var.lambda_bucket
  s3_key           = var.lambda_key
  source_code_hash = data.aws_s3_object.lambda_zip.etag

  environment {
    variables = {
      ENV        = "development" 
      TABLE_NAME = "todo-items"
    }
  }
}

resource "aws_lambda_permission" "allow_apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.todo_handler.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.todo_api.execution_arn}/*/*"
}
