variable "region" {
  type    = string
  default = "us-region-1"
}

variable "stage" {
  type    = string
  default = "dev"
}

variable "lambda_zip_hash" {
  description = "Base64-encoded SHA256 hash of the Lambda zip file"
  type        = string
}

variable "lambda_bucket" {
  type = string
  default = "julyvision-deployments"
}

variable "lambda_key" {
  type = string
  default = "todo-api/function.zip"
}