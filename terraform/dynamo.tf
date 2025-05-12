resource "aws_dynamodb_table" "todo_table" {
  name         = "todo-items"
  billing_mode = "PAY_PER_REQUEST"

  hash_key = "id"

  attribute {
    name = "id"
    type = "S"
  }
}
