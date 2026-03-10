# AI-Assisted SRE Workflow on AWS

## Overview
Built a cloud-native SRE project that deploys a containerized Python application to AWS ECS Fargate using Terraform and GitHub Actions. The project includes monitoring, alerting, incident simulation, and an AI-assisted triage workflow for analyzing service incidents.

## Architecture
- Python Flask application
- Docker container
- Amazon ECR
- Amazon ECS Fargate
- Application Load Balancer
- Terraform
- GitHub Actions
- CloudWatch Logs and Alarms
- SNS email notifications
- OpenAI-powered incident triage script

## Features
- Infrastructure as Code with Terraform
- CI/CD pipeline with GitHub Actions
- ECS Fargate deployment behind ALB
- Health checks and CloudWatch logging
- Alerting with SNS notifications
- Simulated 5xx and latency incidents
- AI-generated incident summary and response guidance

## Incident Scenarios Tested
- Repeated 500 errors using `/error`
- Slow endpoint latency using `/slow`
- Intermittent failures using `/random`

## AI-Assisted Triage
The triage script reads structured incident data and uses an LLM API to generate:
- incident summary
- likely cause
- severity assessment
- response steps
- investigation suggestions
- remediation recommendation
- draft postmortem notes

## Results
- Terraform deployment successful
- ECS service healthy behind ALB
- CloudWatch alarms triggered successfully
- SNS email notifications received
- AI triage report generated successfully

## Lessons Learned
- Debugged ECS task startup failures caused by incorrect secret references
- Resolved container architecture mismatch between Apple Silicon and ECS runtime
- Fixed ALB-to-target connectivity with security group changes
- Validated monitoring and alerting through controlled incident testing