# ALB Security Group (Traffic Internet -> ALB)
resource "aws_security_group" "rolt-load-balancer" {
  name        = "rolt-load-balancer"
  description = "Controls access to the ALB"
  vpc_id      = aws_vpc.rolt-prod-vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ECS Fargate Security group (traffic ALB -> ECS Fargate Tasks)
resource "aws_security_group" "rolt-ecs-fargate" {
  name        = "rolt-ecs-fargate"
  description = "Allows inbound access from the ALB only"
  vpc_id      = aws_vpc.rolt-prod-vpc.id

  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    security_groups = [aws_security_group.rolt-load-balancer.id]
  }

  # No SSH ingress rule since Fargate tasks are abstracted and not directly accessible via SSH

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# RDS Security Group (traffic Fargate -> RDS)
resource "aws_security_group" "rolt-rds" {
  name        = "rds-security-group"
  description = "Allows inbound access from Fargate only"
  vpc_id      = aws_vpc.rolt-prod-vpc.id

  ingress {
    protocol        = "tcp"
    from_port       = "5432"
    to_port         = "5432"
    security_groups = [aws_security_group.rolt-ecs-fargate.id]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}
# REDIS Security Group (traffic Fargate -> Redis)
resource "aws_security_group" "rolt-elasticache_sg" {
  name        = "rolt-elasticache_sg"
  description = "Security group for ElastiCache"
  vpc_id      = aws_vpc.rolt-prod-vpc.id

  ingress {
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [aws_security_group.rolt-ecs-fargate.id]
    description     = "Allow Redis access from ECS Fargate"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }
}
