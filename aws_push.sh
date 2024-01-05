#!/bin/bash


# Set AWS credentials
export AWS_ACCESS_KEY_ID="$CI_AWS_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="$CI_AWS_SECRET_ACCESS_KEY"
export AWS_DEFAULT_REGION="$CI_AWS_DEFAULT_REGION"

# Set the names of your Docker images
images=( "service1" "service2" "api_gateway_service" "monitoring_service" )

# Log in to AWS ECR
aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $ECR_REPO_URL

# Push Docker images to AWS ECR
for image in "${images[@]}"; do
  docker tag $image:latest $ECR_REPO_URL/$image:latest
  docker push $ECR_REPO_URL/$image:latest
done

# Clean up - log out from AWS ECR
docker logout $ECR_REPO_URL
