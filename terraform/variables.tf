variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name prefix"
  type        = string
  default     = "ai-sre"
}

variable "container_image" {
  description = "ECR image URI"
  type        = string
}

variable "container_port" {
  description = "Application container port"
  type        = number
  default     = 5000
}

variable "app_count" {
  description = "Number of ECS tasks"
  type        = number
  default     = 1
}