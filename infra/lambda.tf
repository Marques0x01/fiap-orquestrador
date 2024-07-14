resource "aws_lambda_function" "lambda" {
  filename      = "lambda.zip" # Nome do arquivo zip contendo seu código python
  function_name = var.lambda_name
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"

  source_code_hash = data.archive_file.zip.output_base64sha256

  environment {
    variables = var.env_vars
  }

  depends_on = [aws_iam_role.lambda_role]
}

data "archive_file" "zip" {
  type        = "zip"
  source_dir  = "${path.module}/../app"
  output_path = "${path.module}/lambda.zip"
}

resource "aws_lambda_event_source_mapping" "sqs_trigger" {
  event_source_arn = "arn:aws:sqs:us-east-2:381492057057:orquestrador_pedido"
  function_name    = aws_lambda_function.lambda.arn
  enabled          = true
  batch_size       = 1

  depends_on = [aws_lambda_function.lambda]
}