# Production Load Balancer
resource "aws_lb" "rolt-prod-lb" {
  name               = "${var.ecs_cluster_name}-alb"
  load_balancer_type = "application"
  internal           = false
  security_groups    = [aws_security_group.rolt-load-balancer.id]
  subnets            = [aws_subnet.public-subnet-1.id, aws_subnet.public-subnet-2.id]
}

# Target group for ECS Fargate
resource "aws_alb_target_group" "rolt-df-tg" {
  name        = "${var.ecs_cluster_name}-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.rolt-prod-vpc.id
  target_type = "ip"

  health_check {
    path                = var.health_check_path
    port                = "traffic-port"
    healthy_threshold   = 5
    unhealthy_threshold = 2
    timeout             = 2
    interval            = 5
    matcher             = "200"
  }
}

# Listener (redirects traffic from the load balancer to the target group)
resource "aws_alb_listener" "rolt-prod-listener" {
  load_balancer_arn = aws_lb.rolt-prod-lb.id
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = var.certificate_arn
  depends_on        = [aws_alb_target_group.rolt-df-tg]

  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.rolt-df-tg.arn
  }
}
