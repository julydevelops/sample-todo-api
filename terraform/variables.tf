variable "region" {
  type    = string
  default = "us-region-1"
}

variable "stage" {
  type    = string
  default = "dev"
}

variable "lambda_bucket" {
  type = string
  default = "julyvision-deployments"
}

variable "lambda_key" {
  type = string
  default = "sample-todo-api/function.zip"
}