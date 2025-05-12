output "alb_hostname" {
  value = aws_lb.rolt-prod-lb.dns_name
}

output "ecs_task_execution_role_arn" {
  value = aws_iam_role.rolt-ecs-task-execution-role.arn
}

output "public_subnet_ids" {
  value = [aws_subnet.public-subnet-1.id, aws_subnet.public-subnet-2.id]
}

output "ecs_security_group_id" {
  value = aws_security_group.rolt-ecs-fargate.id
}

output "dns_load_balancer" {
  value = aws_lb.rolt-prod-lb.dns_name
}

output "redis_url" {
  value = "redis://${aws_elasticache_replication_group.rolt-redis-rep-group.primary_endpoint_address}:6379"
}


output "bucket_name" {
  value = aws_s3_bucket.rolt_bucket.bucket
}

output "bucket_arn" {
  value = aws_s3_bucket.rolt_bucket.arn
}

output "bucket_domain_name" {
  value = aws_s3_bucket.rolt_bucket.bucket_domain_name
}
