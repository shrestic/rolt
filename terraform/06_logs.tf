resource "aws_cloudwatch_log_group" "rolt-django-log-group" {
  name              = "/ecs/rolt-django"
  retention_in_days = var.log_retention_in_days
}

resource "aws_cloudwatch_log_group" "rolt-cmd-exe-log-group" {
  name              = "/ecs/rolt-cmd-exe"
  retention_in_days = var.log_retention_in_days
}

resource "aws_cloudwatch_log_group" "rolt-celery-worker-log-group" {
  name              = "/ecs/rolt-celeryworker"
  retention_in_days = var.log_retention_in_days
}

resource "aws_cloudwatch_log_group" "rolt-celery-beat-log-group" {
  name              = "/ecs/rolt-celerybeat"
  retention_in_days = var.log_retention_in_days
}

resource "aws_cloudwatch_log_group" "rolt-flower-log-group" {
  name              = "/ecs/rolt-flower"
  retention_in_days = var.log_retention_in_days
}

resource "aws_cloudwatch_log_group" "rolt-nginx-log-group" {
  name              = "/ecs/rolt-nginx"
  retention_in_days = var.log_retention_in_days
}

resource "aws_cloudwatch_log_stream" "rolt-nginx-log-stream" {
  name           = "rolt-nginx-log-stream"
  log_group_name = aws_cloudwatch_log_group.rolt-nginx-log-group.name
}
