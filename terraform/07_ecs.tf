locals {
  redis_url = "redis://${aws_elasticache_replication_group.rolt-redis-rep-group.primary_endpoint_address}:6379"
  rolt_container_definitions = templatefile("${path.module}/templates/rolt_container.json.tpl", {
    admin_url               = var.admin_url
    admin_username          = var.admin_username
    admin_password          = var.admin_password
    admin_email             = var.admin_email
    allowed_hosts           = join(",", var.allowed_hosts)
    aws_access_key_id       = var.aws_access_key_id
    aws_bucket_name         = var.aws_bucket_name
    aws_s3_custom_domain    = var.aws_s3_custom_domain
    aws_secret_access_key   = var.aws_secret_access_key
    django_debug            = var.django_debug
    db_host                 = aws_db_instance.rolt-prod-db.address
    db_name                 = var.rds_db_name
    db_password             = var.rds_password
    db_port                 = "5432"
    db_user                 = var.rds_username
    default_from_email      = var.default_from_email
    django_secret_key       = var.django_secret_key
    django_settings_module  = var.django_settings_module
    docker_image_url_django = var.docker_image_url_django
    docker_image_url_nginx  = var.docker_image_url_nginx
    google_oauth2_key       = var.google_oauth2_key
    google_oauth2_secret    = var.google_oauth2_secret
    redis_url               = local.redis_url
    region                  = var.region
    sendgrid_api_key        = var.sendgrid_api_key
    server_email            = var.server_email
    support_alert_email     = var.support_alert_email
    temp_domain             = var.temp_domain
    vnpay_hash_secret_key   = var.vnpay_hash_secret_key
    vnpay_return_url        = var.vnpay_return_url
    vnpay_tmn_code          = var.vnpay_tmn_code
  })

  rolt_migration_container_definitions = templatefile("${path.module}/templates/cmd_rolt_container.json.tpl", {
    admin_url               = var.admin_url
    admin_username          = var.admin_username
    admin_password          = var.admin_password
    admin_email             = var.admin_email
    allowed_hosts           = join(",", var.allowed_hosts)
    aws_access_key_id       = var.aws_access_key_id
    aws_bucket_name         = var.aws_bucket_name
    aws_s3_custom_domain    = var.aws_s3_custom_domain
    aws_secret_access_key   = var.aws_secret_access_key
    command                 = var.cmd_migration
    django_debug            = var.django_debug
    db_host                 = aws_db_instance.rolt-prod-db.address
    db_name                 = var.rds_db_name
    db_password             = var.rds_password
    db_port                 = "5432"
    db_user                 = var.rds_username
    default_from_email      = var.default_from_email
    django_secret_key       = var.django_secret_key
    django_settings_module  = var.django_settings_module
    docker_image_url_django = var.docker_image_url_django
    google_oauth2_key       = var.google_oauth2_key
    google_oauth2_secret    = var.google_oauth2_secret
    redis_url               = local.redis_url
    region                  = var.region
    sendgrid_api_key        = var.sendgrid_api_key
    server_email            = var.server_email
    support_alert_email     = var.support_alert_email
    temp_domain             = var.temp_domain
    vnpay_hash_secret_key   = var.vnpay_hash_secret_key
    vnpay_return_url        = var.vnpay_return_url
    vnpay_tmn_code          = var.vnpay_tmn_code
  })

  rolt_init_roles_container_definitions = templatefile("${path.module}/templates/cmd_rolt_container.json.tpl", {
    admin_url               = var.admin_url
    admin_username          = var.admin_username
    admin_password          = var.admin_password
    admin_email             = var.admin_email
    allowed_hosts           = join(",", var.allowed_hosts)
    aws_access_key_id       = var.aws_access_key_id
    aws_bucket_name         = var.aws_bucket_name
    aws_s3_custom_domain    = var.aws_s3_custom_domain
    aws_secret_access_key   = var.aws_secret_access_key
    command                 = var.cmd_init_roles
    django_debug            = var.django_debug
    db_host                 = aws_db_instance.rolt-prod-db.address
    db_name                 = var.rds_db_name
    db_password             = var.rds_password
    db_port                 = "5432"
    db_user                 = var.rds_username
    default_from_email      = var.default_from_email
    django_secret_key       = var.django_secret_key
    django_settings_module  = var.django_settings_module
    docker_image_url_django = var.docker_image_url_django
    google_oauth2_key       = var.google_oauth2_key
    google_oauth2_secret    = var.google_oauth2_secret
    redis_url               = local.redis_url
    region                  = var.region
    sendgrid_api_key        = var.sendgrid_api_key
    server_email            = var.server_email
    support_alert_email     = var.support_alert_email
    temp_domain             = var.temp_domain
    vnpay_hash_secret_key   = var.vnpay_hash_secret_key
    vnpay_return_url        = var.vnpay_return_url
    vnpay_tmn_code          = var.vnpay_tmn_code
  })
  rolt_create_superuser_container_definitions = templatefile("${path.module}/templates/cmd_rolt_container.json.tpl", {
    admin_url               = var.admin_url
    admin_username          = var.admin_username
    admin_password          = var.admin_password
    admin_email             = var.admin_email
    allowed_hosts           = join(",", var.allowed_hosts)
    aws_access_key_id       = var.aws_access_key_id
    aws_bucket_name         = var.aws_bucket_name
    aws_s3_custom_domain    = var.aws_s3_custom_domain
    aws_secret_access_key   = var.aws_secret_access_key
    command                 = var.cmd_createsuperuser
    django_debug            = var.django_debug
    db_host                 = aws_db_instance.rolt-prod-db.address
    db_name                 = var.rds_db_name
    db_password             = var.rds_password
    db_port                 = "5432"
    db_user                 = var.rds_username
    default_from_email      = var.default_from_email
    django_secret_key       = var.django_secret_key
    django_settings_module  = var.django_settings_module
    docker_image_url_django = var.docker_image_url_django
    google_oauth2_key       = var.google_oauth2_key
    google_oauth2_secret    = var.google_oauth2_secret
    redis_url               = local.redis_url
    region                  = var.region
    sendgrid_api_key        = var.sendgrid_api_key
    server_email            = var.server_email
    support_alert_email     = var.support_alert_email
    temp_domain             = var.temp_domain
    vnpay_hash_secret_key   = var.vnpay_hash_secret_key
    vnpay_return_url        = var.vnpay_return_url
    vnpay_tmn_code          = var.vnpay_tmn_code
  })

  celeryworker_container_definitions = templatefile("${path.module}/templates/celeryworker_container.json.tpl", {
    admin_url               = var.admin_url
    admin_username          = var.admin_username
    admin_password          = var.admin_password
    admin_email             = var.admin_email
    allowed_hosts           = join(",", var.allowed_hosts)
    aws_access_key_id       = var.aws_access_key_id
    aws_bucket_name         = var.aws_bucket_name
    aws_s3_custom_domain    = var.aws_s3_custom_domain
    aws_secret_access_key   = var.aws_secret_access_key
    django_debug            = var.django_debug
    db_host                 = aws_db_instance.rolt-prod-db.address
    db_name                 = var.rds_db_name
    db_password             = var.rds_password
    db_port                 = "5432"
    db_user                 = var.rds_username
    default_from_email      = var.default_from_email
    django_secret_key       = var.django_secret_key
    django_settings_module  = var.django_settings_module
    docker_image_url_django = var.docker_image_url_django
    docker_image_url_nginx  = var.docker_image_url_nginx
    google_oauth2_key       = var.google_oauth2_key
    google_oauth2_secret    = var.google_oauth2_secret
    redis_url               = local.redis_url
    region                  = var.region
    sendgrid_api_key        = var.sendgrid_api_key
    server_email            = var.server_email
    support_alert_email     = var.support_alert_email
    temp_domain             = var.temp_domain
    vnpay_hash_secret_key   = var.vnpay_hash_secret_key
    vnpay_return_url        = var.vnpay_return_url
    vnpay_tmn_code          = var.vnpay_tmn_code
  })

  celerybeat_container_definitions = templatefile("${path.module}/templates/celerybeat_container.json.tpl", {
    admin_url               = var.admin_url
    admin_username          = var.admin_username
    admin_password          = var.admin_password
    admin_email             = var.admin_email
    allowed_hosts           = join(",", var.allowed_hosts)
    aws_access_key_id       = var.aws_access_key_id
    aws_bucket_name         = var.aws_bucket_name
    aws_s3_custom_domain    = var.aws_s3_custom_domain
    aws_secret_access_key   = var.aws_secret_access_key
    django_debug            = var.django_debug
    db_host                 = aws_db_instance.rolt-prod-db.address
    db_name                 = var.rds_db_name
    db_password             = var.rds_password
    db_port                 = "5432"
    db_user                 = var.rds_username
    default_from_email      = var.default_from_email
    django_secret_key       = var.django_secret_key
    django_settings_module  = var.django_settings_module
    docker_image_url_django = var.docker_image_url_django
    docker_image_url_nginx  = var.docker_image_url_nginx
    google_oauth2_key       = var.google_oauth2_key
    google_oauth2_secret    = var.google_oauth2_secret
    redis_url               = local.redis_url
    region                  = var.region
    sendgrid_api_key        = var.sendgrid_api_key
    server_email            = var.server_email
    support_alert_email     = var.support_alert_email
    temp_domain             = var.temp_domain
    vnpay_hash_secret_key   = var.vnpay_hash_secret_key
    vnpay_return_url        = var.vnpay_return_url
    vnpay_tmn_code          = var.vnpay_tmn_code
  })

  flower_container_definitions = templatefile("${path.module}/templates/flower_container.json.tpl", {
    admin_url               = var.admin_url
    admin_username          = var.admin_username
    admin_password          = var.admin_password
    admin_email             = var.admin_email
    allowed_hosts           = join(",", var.allowed_hosts)
    aws_access_key_id       = var.aws_access_key_id
    aws_bucket_name         = var.aws_bucket_name
    aws_s3_custom_domain    = var.aws_s3_custom_domain
    aws_secret_access_key   = var.aws_secret_access_key
    django_debug            = var.django_debug
    db_host                 = aws_db_instance.rolt-prod-db.address
    db_name                 = var.rds_db_name
    db_password             = var.rds_password
    db_port                 = "5432"
    db_user                 = var.rds_username
    default_from_email      = var.default_from_email
    django_secret_key       = var.django_secret_key
    django_settings_module  = var.django_settings_module
    docker_image_url_django = var.docker_image_url_django
    docker_image_url_nginx  = var.docker_image_url_nginx
    flower_password         = var.flower_password
    flower_user             = var.flower_user
    google_oauth2_key       = var.google_oauth2_key
    google_oauth2_secret    = var.google_oauth2_secret
    redis_url               = local.redis_url
    region                  = var.region
    sendgrid_api_key        = var.sendgrid_api_key
    server_email            = var.server_email
    support_alert_email     = var.support_alert_email
    temp_domain             = var.temp_domain
    vnpay_hash_secret_key   = var.vnpay_hash_secret_key
    vnpay_return_url        = var.vnpay_return_url
    vnpay_tmn_code          = var.vnpay_tmn_code
  })
}
resource "aws_ecs_cluster" "rolt-prod-ecs-clt" {
  name = "${var.ecs_cluster_name}-ecs-cluster"
}

resource "aws_ecs_task_definition" "rolt-django-ecs-task" {
  family                   = "rolt-django-fam"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.rolt-ecs-task-execution-role.arn
  task_role_arn            = aws_iam_role.rolt-ecs-task-execution-role.arn
  container_definitions    = local.rolt_container_definitions
  depends_on = [
    aws_db_instance.rolt-prod-db,
    aws_elasticache_replication_group.rolt-redis-rep-group,
    aws_s3_bucket.rolt_bucket,
    aws_security_group.rolt-ecs-fargate,
    aws_iam_role.rolt-ecs-task-execution-role
  ]
}

resource "aws_ecs_task_definition" "rolt-django-migration-ecs-task" {
  family                   = "rolt-django-migration-fam"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.rolt-ecs-task-execution-role.arn
  task_role_arn            = aws_iam_role.rolt-ecs-task-execution-role.arn
  container_definitions    = local.rolt_migration_container_definitions
  depends_on = [
    aws_db_instance.rolt-prod-db,
    aws_elasticache_replication_group.rolt-redis-rep-group,
    aws_s3_bucket.rolt_bucket,
    aws_security_group.rolt-ecs-fargate,
    aws_iam_role.rolt-ecs-task-execution-role
  ]
}

resource "aws_ecs_task_definition" "rolt-django-init-roles-ecs-task" {
  family                   = "rolt-django-init-roles-fam"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.rolt-ecs-task-execution-role.arn
  task_role_arn            = aws_iam_role.rolt-ecs-task-execution-role.arn
  container_definitions    = local.rolt_init_roles_container_definitions
  depends_on = [
    aws_db_instance.rolt-prod-db,
    aws_elasticache_replication_group.rolt-redis-rep-group,
    aws_s3_bucket.rolt_bucket,
    aws_security_group.rolt-ecs-fargate,
    aws_iam_role.rolt-ecs-task-execution-role
  ]
}
resource "aws_ecs_task_definition" "rolt-django-create-superuser-ecs-task" {
  family                   = "rolt-django-create-superuser-fam"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.rolt-ecs-task-execution-role.arn
  task_role_arn            = aws_iam_role.rolt-ecs-task-execution-role.arn
  container_definitions    = local.rolt_create_superuser_container_definitions
  depends_on = [
    aws_db_instance.rolt-prod-db,
    aws_elasticache_replication_group.rolt-redis-rep-group,
    aws_s3_bucket.rolt_bucket,
    aws_security_group.rolt-ecs-fargate,
    aws_iam_role.rolt-ecs-task-execution-role
  ]
}

resource "aws_ecs_task_definition" "rolt-celeryworker-ecs-task" {
  family                   = "rolt-celeryworker-fam"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.rolt-ecs-task-execution-role.arn
  task_role_arn            = aws_iam_role.rolt-ecs-task-execution-role.arn
  container_definitions    = local.celeryworker_container_definitions
  depends_on = [
    aws_elasticache_replication_group.rolt-redis-rep-group,
    aws_security_group.rolt-ecs-fargate,
    aws_iam_role.rolt-ecs-task-execution-role
  ]
}

resource "aws_ecs_task_definition" "rolt-celerybeat-ecs-task" {
  family                   = "rolt-celerybeat-fam"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.rolt-ecs-task-execution-role.arn
  task_role_arn            = aws_iam_role.rolt-ecs-task-execution-role.arn
  container_definitions    = local.celerybeat_container_definitions
  depends_on = [
    aws_db_instance.rolt-prod-db,
    aws_elasticache_replication_group.rolt-redis-rep-group,
    aws_security_group.rolt-ecs-fargate,
    aws_iam_role.rolt-ecs-task-execution-role
  ]
}

resource "aws_ecs_task_definition" "rolt-flower-ecs-task" {
  family                   = "rolt-flower-fam"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.rolt-ecs-task-execution-role.arn
  task_role_arn            = aws_iam_role.rolt-ecs-task-execution-role.arn
  container_definitions    = local.flower_container_definitions
  depends_on = [
    aws_elasticache_replication_group.rolt-redis-rep-group,
    aws_security_group.rolt-ecs-fargate,
    aws_iam_role.rolt-ecs-task-execution-role
  ]
}


resource "aws_ecs_service" "rolt-django-ecs-service" {
  name            = "${var.ecs_cluster_name}-django-ecs-service"
  cluster         = aws_ecs_cluster.rolt-prod-ecs-clt.id
  task_definition = aws_ecs_task_definition.rolt-django-ecs-task.arn
  launch_type     = "FARGATE"
  desired_count   = var.app_count
  network_configuration {
    subnets          = [aws_subnet.private-subnet-1.id, aws_subnet.private-subnet-2.id]
    security_groups  = [aws_security_group.rolt-ecs-fargate.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_alb_target_group.rolt-df-tg.arn
    container_name   = "nginx"
    container_port   = 80
  }
}

resource "aws_ecs_service" "rolt-celeryworker-ecs-service" {
  name            = "${var.ecs_cluster_name}-celeryworker-ecs-service"
  cluster         = aws_ecs_cluster.rolt-prod-ecs-clt.id
  task_definition = aws_ecs_task_definition.rolt-celeryworker-ecs-task.arn
  launch_type     = "FARGATE"
  desired_count   = var.celeryworker_count
  network_configuration {
    subnets          = [aws_subnet.private-subnet-1.id, aws_subnet.private-subnet-2.id]
    security_groups  = [aws_security_group.rolt-ecs-fargate.id]
    assign_public_ip = false
  }
}

resource "aws_ecs_service" "rolt-celerybeat-ecs-service" {
  name            = "${var.ecs_cluster_name}-celerybeat-ecs-service"
  cluster         = aws_ecs_cluster.rolt-prod-ecs-clt.id
  task_definition = aws_ecs_task_definition.rolt-celerybeat-ecs-task.arn
  launch_type     = "FARGATE"
  desired_count   = 1
  network_configuration {
    subnets          = [aws_subnet.private-subnet-1.id, aws_subnet.private-subnet-2.id]
    security_groups  = [aws_security_group.rolt-ecs-fargate.id]
    assign_public_ip = false
  }
}

resource "aws_ecs_service" "rolt-flower-ecs-service" {
  name            = "${var.ecs_cluster_name}-flower-ecs-service"
  cluster         = aws_ecs_cluster.rolt-prod-ecs-clt.id
  task_definition = aws_ecs_task_definition.rolt-flower-ecs-task.arn
  launch_type     = "FARGATE"
  desired_count   = 1
  network_configuration {
    subnets          = [aws_subnet.private-subnet-1.id, aws_subnet.private-subnet-2.id]
    security_groups  = [aws_security_group.rolt-ecs-fargate.id]
    assign_public_ip = false
  }
}
