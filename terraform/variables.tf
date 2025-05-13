# -------------------------------
# Core
# -------------------------------

variable "region" {
  description = "The AWS region to create resources in."
  default     = "ap-southeast-1"
}

variable "environment" {
  description = "Name of the environment (e.g., production, staging)"
  type        = string
  default     = "production"
}

# -------------------------------
# Networking
# -------------------------------

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["ap-southeast-1a", "ap-southeast-1b"]
}

variable "public_subnet_1_cidr" {
  default = "10.0.1.0/24"
}

variable "public_subnet_2_cidr" {
  default = "10.0.2.0/24"
}

variable "private_subnet_1_cidr" {
  default = "10.0.3.0/24"
}

variable "private_subnet_2_cidr" {
  default = "10.0.4.0/24"
}

# -------------------------------
# Load Balancer
# -------------------------------

variable "health_check_path" {
  default = "/ping/"
}

# -------------------------------
# ECS
# -------------------------------

variable "ecs_cluster_name" {
  default = "rolt-prod"
}

variable "docker_image_url_django" {
  description = "Docker image URL for Django container"
  type        = string
}

variable "docker_image_url_nginx" {
  default = "362262895301.dkr.ecr.ap-southeast-1.amazonaws.com/mainkode/nginx:latest"
}

variable "app_count" {
  default = 2
}

variable "fargate_cpu" {
  type    = number
  default = 256
}

variable "fargate_memory" {
  type    = number
  default = 512
}

variable "autoscale_min" {
  type    = number
  default = 1
}

variable "autoscale_max" {
  type    = number
  default = 10
}

variable "autoscale_desired" {
  type    = number
  default = 4
}

variable "allowed_hosts" {
  type    = list(string)
  default = ["www.rolt.cloud", "rolt.cloud", "rolt-prod-alb-261433099.ap-southeast-1.elb.amazonaws.com"]
}

# -------------------------------
# Logs
# -------------------------------

variable "log_retention_in_days" {
  type    = number
  default = 30
}

# -------------------------------
# RDS
# -------------------------------

variable "rds_db_name" {
  default = "roltdb"
}

variable "rds_username" {
  default = "nhatphongcgp"
}

variable "rds_password" {
  type      = string
  sensitive = true
}

variable "rds_instance_class" {
  default = "db.t3.micro"
}

# -------------------------------
# S3
# -------------------------------

variable "aws_bucket_name" {
  default = "rolt-vn-69"
}

variable "aws_s3_custom_domain" {
  type    = string
  default = ""
}

# -------------------------------
# SSL/Domain
# -------------------------------

variable "certificate_arn" {
  default = "arn:aws:acm:ap-southeast-1:362262895301:certificate/6d0f6add-2ca8-4773-919f-f14992453c07"
}

variable "temp_domain" {
  default = "a365-14-191-121-112.ngrok-free.app"
}

# -------------------------------
# Django App Configuration
# -------------------------------

variable "django_debug" {
  type    = bool
  default = false
}

variable "django_settings_module" {
  default = "config.settings.production"
}

variable "django_secret_key" {
  type      = string
  sensitive = true
}

variable "admin_url" {
  default = "vJhuA92t1ODp7tc4vryOacApWGBBBCts/"
}

variable "admin_username" {
  default = "nhatphongcgp"
}

variable "admin_password" {
  type      = string
  sensitive = true
}

variable "admin_email" {
  default = "nhatphongcgp@gmail.com"
}

variable "default_from_email" {
  default = "no-reply@rolt.cloud"
}

variable "support_alert_email" {
  default = "support@rolt.cloud"
}

variable "server_email" {
  default = "server@rolt.cloud"
}

# -------------------------------
# External Services
# -------------------------------

variable "sendgrid_api_key" {
  type      = string
  sensitive = true
}

variable "aws_access_key_id" {
  type      = string
  sensitive = true
}

variable "aws_secret_access_key" {
  type      = string
  sensitive = true
}

variable "google_oauth2_key" {
  default = "606444304279-fuh659i2jgs85ms58d9rjns8aj94h466.apps.googleusercontent.com"
}

variable "google_oauth2_secret" {
  type      = string
  sensitive = true
}

# -------------------------------
# VNPAY
# -------------------------------

variable "vnpay_return_url" {
  default = "https://www.rolt.cloud/shop/payment/ipn"
}

variable "vnpay_tmn_code" {
  default = "7ZRJTRMX"
}

variable "vnpay_hash_secret_key" {
  type      = string
  sensitive = true
}

# -------------------------------
# Celery / Flower
# -------------------------------

variable "flower_user" {
  default = "debug"
}

variable "flower_password" {
  default = "debug"
}

variable "celeryworker_count" {
  default = 2
}

variable "cmd_migration" {
  default = "python manage.py migrate --noinput"
}

variable "cmd_createsuperuser" {
  default = "python manage.py init_admin"
}

variable "cmd_init_roles" {
  default = "python manage.py init_roles"
}
