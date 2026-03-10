# AI-Assisted Incident Triage Report

1. Incident Summary
- Service/environment: ai-sre-service on AWS ECS Fargate behind an ALB (environment: terraform)
- Time (UTC): 2026-03-10T20:45:05Z
- Symptoms/alarms:
  - CloudWatch alarms: ai-sre-tf-5xx-errors (ALARM), ai-sre-tf-high-response-time (ALARM)
  - ALB target group returned HTTP 500s; average target response time > 1s
- Metrics (last 60s):
  - HTTPCode_Target_5XX_Count: 20
  - TargetResponseTime (avg): 1.735 s
- Affected endpoints: /error (5xx), /slow (latency)
- Logs:
  - GET /error returned 500 multiple times
  - GET /slow showed elevated response times
  - Gunicorn serving requests successfully
  - Health endpoint remained healthy
- Change context: Recent deploy via GitHub Actions to ECS Fargate; infra via Terraform
- Notes: 500s and slowness were intentionally triggered for alert validation

2. Likely Cause
- Alarms were triggered by intentional test traffic to /error and /slow that produces 500 responses and slow processing by design.
- No evidence of ECS/ALB health degradation or app/server instability (Gunicorn OK, health checks OK, only test URLs affected).

3. Severity Assessment
- Severity: Low (Informational/Test)
  - Reasoning: Impact isolated to test endpoints; health checks and core service paths unaffected; errors/slowness intentionally induced.

4. Immediate Response Steps
- Acknowledge alarms and annotate incident as “intentional alert validation.”
- Verify blast radius is limited to test endpoints:
  - Check app logs for 5xx and latency by path.
  - Validate no other routes show increased 5xx or latency.
- Confirm service health:
  - Target group healthy, ECS tasks RUNNING, no restarts/crashes, CPU/mem within baseline.
- Temporarily suppress alarm notifications during the test window to avoid paging noise (disable alarm actions or mute SNS subscription), then re-enable after tests.
- Notify stakeholders/on-call that this was a planned test and no rollback is required.

Example quick checks (replace placeholders):
- ECS service/tasks:
  - aws ecs describe-services --cluster <cluster> --services <service>
  - aws ecs list-tasks --cluster <cluster> --service-name <service> --desired-status RUNNING
  - aws ecs describe-tasks --cluster <cluster> --tasks $(...)
- ALB target health:
  - aws elbv2 describe-target-health --target-group-arn <tg-arn>
- CloudWatch alarm actions (temporary mute during testing):
  - aws cloudwatch disable-alarm-actions --alarm-names ai-sre-tf-5xx-errors ai-sre-tf-high-response-time
  - aws cloudwatch enable-alarm-actions --alarm-names ai-sre-tf-5xx-errors ai-sre-tf-high-response-time

5. Suggested Investigation Checks
- Confirm only /error and /slow requests produced anomalies:
  - Query ALB access logs (S3/Athena) for time window and paths /error and /slow; ensure other paths have normal 2xx/3xx and typical latencies.
- Validate there’s no unexpected increase in RequestCount or 4xx/5xx on non-test routes.
- Verify autoscaling wasn’t triggered and resource headroom remains healthy:
  - CPU/memory metrics on ECS tasks; concurrent requests; connection errors.
- Check target group unhealthy host count remains 0 and health check success rate is 100%.
- Confirm deployment state is stable (no recent rollouts failing, no crash loops).
- Ensure test traffic identifiers (source IP/User-Agent) are as expected.

6. Rollback or Remediation Recommendation
- Rollback: Not needed (behavior is by design for testing).
- Remediation (alerting hygiene and test safety):
  - Refine 5xx alerting to reduce noise:
    - Use error rate (%) with a minimum traffic guard instead of absolute 5xx count.
      - Example metric math: IF(RequestCount>=N, 100*HTTPCode_Target_5XX_Count/RequestCount, 0) > threshold for M periods.
    - Add a “test window” or maintenance toggle that suppresses alarms during intentional exercises (CloudWatch composite alarm with a “Testing=0/1” custom metric, or disable alarm actions via automation).
    - Exclude known test endpoints from alerting using application-level custom metrics (e.g., emit http_server_requests{path!=/error,/slow} and alert from those), or generate path-filtered custom CloudWatch metrics from app/OTel.
  - For latency alerts, alert on high percentiles (p95/p99) of non-test paths and require sustained breaches (e.g., 3/5 minutes) with request count guard.
  - Document a standard operating procedure to coordinate alert tests and notify on-call before execution.

7. Draft Postmortem Notes
- What happened:
  - 20:45:05Z CloudWatch alarms for 5xx and high response time entered ALARM.
  - Test endpoints /error and /slow were exercised to validate alerting; health checks and other endpoints remained normal.
- Impact:
  - ALB target 5xx: 20 within 60s on /error only.
  - Avg target response time: 1.735 s driven by /slow tests.
  - No known customer impact; core functionality unaffected; no task/host health issues.
- Detection:
  - CloudWatch alarms as designed; signals were accurate but noisy for intentional tests.
- Root cause:
  - Intentional alert validation traffic to endpoints that generate 500s and latency by design.
- Contributing factors:
  - 5xx alarm based on aggregate target group metrics (no path filtering).
  - No temporary suppression during planned testing.
- What went well:
  - Health checks stayed green; Gunicorn served normally; alarms successfully detected the test conditions.
- What went poorly:
  - On-call noise from expected test behavior.
- Action items:
  - Implement error-rate alarm using metric math with request count guard and path-excluded application metrics.
  - Add a “testing” suppression mechanism (composite alarm or automation to disable/enable alarm actions).
  - Update runbook to require notifying on-call and enabling suppression before executing alert tests.
  - Optionally segregate test endpoints to a separate stage/environment or behind an auth header to simplify exclusion.