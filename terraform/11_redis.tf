resource "aws_elasticache_subnet_group" "rolt-redis-subnet-group" {
  name = "rolt-redis-subnet-group"
  subnet_ids = [
    aws_subnet.private-subnet-1.id,
    aws_subnet.private-subnet-2.id,
  ]
}

resource "aws_elasticache_replication_group" "rolt-redis-rep-group" {
  replication_group_id       = "rolt-valkey-single-node"
  description                = "Valkey cluster with single node"
  engine                     = "redis"
  engine_version             = "7.0"
  node_type                  = "cache.t4g.micro"
  automatic_failover_enabled = false
  port                       = 6379
  subnet_group_name          = aws_elasticache_subnet_group.rolt-redis-subnet-group.name
  security_group_ids         = [aws_security_group.rolt-elasticache_sg.id]
  apply_immediately          = true

  depends_on = [
    aws_elasticache_subnet_group.rolt-redis-subnet-group,
    aws_security_group.rolt-elasticache_sg
  ]
}
