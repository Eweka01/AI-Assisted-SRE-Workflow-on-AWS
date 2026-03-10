import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).parent / ".env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

INCIDENT_FILE = Path(__file__).parent / "sample_incident.json"


def load_incident_data(file_path: Path) -> dict:
    with open(file_path, "r") as f:
        return json.load(f)


def build_prompt(incident: dict) -> str:
    return f"""
You are an SRE incident triage assistant.

Analyze the following incident and produce a structured triage report.

Incident data:
{json.dumps(incident, indent=2)}

Return your response with these sections:

1. Incident Summary
2. Likely Cause
3. Severity Assessment
4. Immediate Response Steps
5. Suggested Investigation Checks
6. Rollback or Remediation Recommendation
7. Draft Postmortem Notes

Be practical, concise, and technical.
Assume this service runs on AWS ECS Fargate behind an Application Load Balancer.
"""


def get_triage_report(prompt: str) -> str:
    response = client.responses.create(
        model="gpt-5",
        input=prompt
    )
    return response.output_text


def main():
    incident = load_incident_data(INCIDENT_FILE)
    prompt = build_prompt(incident)
    report = get_triage_report(prompt)

    output_file = Path(__file__).parent / "triage_report.md"

    with open(output_file, "w") as f:
        f.write("# AI-Assisted Incident Triage Report\n\n")
        f.write(report)

    print("\n" + "=" * 80)
    print("AI-ASSISTED INCIDENT TRIAGE REPORT")
    print("=" * 80)
    print(report)
    print("=" * 80)
    print(f"\nReport saved to: {output_file}\n")


if __name__ == "__main__":
    main()