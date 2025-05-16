resource "aws_iam_role" "rolt-ecs-task-execution-role" {
  name               = "rolt_ecs_task_execution_role_prod"
  assume_role_policy = file("policies/ecs-role.json")
}

resource "aws_iam_role_policy" "rolt-ecs-task-execution-role-policy" {
  name   = "rolt_ecs_task_execution_role_policy"
  policy = file("policies/ecs-task-execution-policy.json")
  role   = aws_iam_role.rolt-ecs-task-execution-role.id
}

resource "aws_iam_role" "rolt-ecs-service-role" {
  name               = "rolt_ecs_service_role_prod"
  assume_role_policy = file("policies/ecs-role.json")
}

resource "aws_iam_role_policy" "rolt-ecs-service-role-policy" {
  name   = "rolt_ecs_service_role_policy"
  policy = file("policies/ecs-service-role-policy.json")
  role   = aws_iam_role.rolt-ecs-service-role.id
}
