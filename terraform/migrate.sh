#!/bin/bash

# This script runs Django migrations as a one-time task in ECS
# Usage: ./run_django_migrations.sh

set -e
CLUSTER_NAME="rolt-prod-ecs-cluster"
# Run the migration task and capture task ARN
echo "Starting Django migration task..."
TASK_ARN=$(aws ecs run-task \
  --cluster $CLUSTER_NAME  \
  --task-definition rolt-django-migration-fam \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=$(terraform output -json public_subnet_ids | jq -c '.'),securityGroups=[$(terraform output -raw ecs_security_group_id)],assignPublicIp=ENABLED}" \
  --query 'tasks[0].taskArn' \
  --output text)

echo "Migration task started with ARN: $TASK_ARN"

# Wait for the task to complete
echo "Waiting for migration task to complete..."
aws ecs wait tasks-stopped \
  --cluster $CLUSTER_NAME \
  --tasks $TASK_ARN

# Check if the task was successful
EXIT_CODE=$(aws ecs describe-tasks \
  --cluster $CLUSTER_NAME \
  --tasks $TASK_ARN \
  --query 'tasks[0].containers[0].exitCode' \
  --output text)

if [ "$EXIT_CODE" -eq 0 ]; then
  echo "Django migrations completed successfully."
else
  echo "Django migrations failed with exit code $EXIT_CODE."
  echo "Check the logs for more details"
fi
