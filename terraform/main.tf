provider "aws" {
  region = var.aws_region
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../build"
  output_path = "${path.module}/../dist/lambda.zip"
}

resource "aws_iam_role" "lambda_exec" {
  name               = "lambda_update_inventory_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_lambda_function" "update_inventory" {
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  function_name    = "update_inventory_function"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "update_inventory.handler"
  runtime          = "python3.14"
  timeout          = 60

  environment {
    variables = {
      appid   = var.appid
      devid = var.devid
      certid = var.certid
      token = var.token
      UPSTASH_REDIS_REST_URL = var.UPSTASH_REDIS_REST_URL
      UPSTASH_REDIS_REST_TOKEN = var.UPSTASH_REDIS_REST_TOKEN
    }
  }
}