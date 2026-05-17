#!/usr/bin/env python3
"""
AI tool intake automation (demo).

Employees submit requests to adopt new AI tools; this script scores risk,
generates intake reports, and persists them to intake_log.json for audit.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

# -----------------------------------------------------------------------------
# Intake request data model
# -----------------------------------------------------------------------------
# A dataclass gives named fields, type hints, and easy conversion to dict/JSON.


@dataclass
class AIIntakeRequest:
    """One employee request to adopt a new AI tool inside the organization."""

    tool_name: str
    vendor_name: str
    intended_use_case: str
    # Allowed values: public, internal, confidential, restricted
    data_classification_level: str
    estimated_number_of_users: int
    # Use "yes" or "no" for consistency with governance questionnaires
    processes_personal_data: str
    connects_to_external_apis: str
    business_justification: str
    requestor_name: str


# -----------------------------------------------------------------------------
# Sample intake requests (low, medium, and high risk profiles)
# -----------------------------------------------------------------------------
# These hardcoded examples let you run the script with no input file.
# Risk outcomes are driven mainly by classification, PII, and external APIs.

SAMPLE_REQUESTS: list[AIIntakeRequest] = [
    # Low risk: public data only, no PII, no outbound API calls
    AIIntakeRequest(
        tool_name="Marketing Copy Assistant",
        vendor_name="WriteBright Inc.",
        intended_use_case="Draft blog posts and social captions from public brand guidelines.",
        data_classification_level="public",
        estimated_number_of_users=25,
        processes_personal_data="no",
        connects_to_external_apis="no",
        business_justification="Speed up content production for the marketing team.",
        requestor_name="Jordan Lee",
    ),
    # Medium risk: internal data with personal information, but no external APIs
    AIIntakeRequest(
        tool_name="HR Policy Q&A Bot",
        vendor_name="PeopleAssist LLC",
        intended_use_case="Answer employee questions about benefits and policies using internal HR documents.",
        data_classification_level="internal",
        estimated_number_of_users=500,
        processes_personal_data="yes",
        connects_to_external_apis="no",
        business_justification="Reduce repetitive HR ticket volume and improve self-service.",
        requestor_name="Samira Patel",
    ),
    # High risk: restricted data, PII processing, and third-party API connectivity
    AIIntakeRequest(
        tool_name="Customer Support Copilot",
        vendor_name="CloudServe AI",
        intended_use_case="Suggest replies and summarize tickets using CRM and payment support history.",
        data_classification_level="restricted",
        estimated_number_of_users=120,
        processes_personal_data="yes",
        connects_to_external_apis="yes",
        business_justification="Improve first-response time and agent productivity in Tier-2 support.",
        requestor_name="Alex Chen",
    ),
]


# -----------------------------------------------------------------------------
# Risk scoring
# -----------------------------------------------------------------------------
# Point values map governance signals to a single risk tier. Higher totals
# mean more sensitive data exposure and a broader attack surface.

_CLASSIFICATION_POINTS: dict[str, int] = {
    "public": 0,
    "internal": 1,
    "confidential": 2,
    "restricted": 3,
}

_PERSONAL_DATA_POINTS: dict[str, int] = {
    "yes": 2,
    "no": 0,
}

_EXTERNAL_API_POINTS: dict[str, int] = {
    "yes": 1,
    "no": 0,
}

# Total score bands: 0–1 Low, 2–3 Medium, 4+ High
_LOW_MAX_SCORE = 1
_MEDIUM_MAX_SCORE = 3


def _normalize_yes_no(value: str) -> str:
    """Normalize yes/no answers so scoring and reports stay consistent."""
    normalized = value.strip().lower()
    if normalized not in ("yes", "no"):
        raise ValueError(f"Expected 'yes' or 'no', got: {value!r}")
    return normalized


def calculate_risk_level(request: AIIntakeRequest) -> str:
    """
    Assign Low, Medium, or High risk from classification, PII, and API use.

    Classification drives baseline sensitivity; personal data and external APIs
    add exposure and integration risk on top of that baseline.
    """
    classification_key = request.data_classification_level.strip().lower()
    if classification_key not in _CLASSIFICATION_POINTS:
        allowed = ", ".join(sorted(_CLASSIFICATION_POINTS))
        raise ValueError(
            f"Invalid data_classification_level {request.data_classification_level!r}; "
            f"expected one of: {allowed}"
        )

    pii = _normalize_yes_no(request.processes_personal_data)
    external_apis = _normalize_yes_no(request.connects_to_external_apis)

    score = (
        _CLASSIFICATION_POINTS[classification_key]
        + _PERSONAL_DATA_POINTS[pii]
        + _EXTERNAL_API_POINTS[external_apis]
    )

    if score <= _LOW_MAX_SCORE:
        return "Low"
    if score <= _MEDIUM_MAX_SCORE:
        return "Medium"
    return "High"


# -----------------------------------------------------------------------------
# Report generation and workflow recommendations
# -----------------------------------------------------------------------------
# Each report is a plain dict so it serializes cleanly to JSON.

_RECOMMENDED_NEXT_STEP: dict[str, str] = {
    "Low": "Auto-approve",
    "Medium": "Security review required",
    "High": "CISO approval required",
}


def build_intake_report(request: AIIntakeRequest) -> dict[str, object]:
    """Build a full intake report dict including risk tier and timestamp."""
    risk_level = calculate_risk_level(request)
    return {
        "request": asdict(request),
        "risk_level": risk_level,
        "recommended_next_step": _RECOMMENDED_NEXT_STEP[risk_level],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def format_intake_report(report: dict[str, object]) -> str:
    """Return a human-readable multi-line report for logging or display."""
    req = report["request"]
    assert isinstance(req, dict)

    lines = [
        "=" * 60,
        "AI TOOL INTAKE REPORT",
        "=" * 60,
        f"Generated at (UTC): {report['generated_at']}",
        "",
        f"Tool name:              {req['tool_name']}",
        f"Vendor name:            {req['vendor_name']}",
        f"Intended use case:      {req['intended_use_case']}",
        f"Data classification:    {req['data_classification_level']}",
        f"Estimated users:        {req['estimated_number_of_users']}",
        f"Processes personal data: {req['processes_personal_data']}",
        f"Connects to external APIs: {req['connects_to_external_apis']}",
        f"Business justification: {req['business_justification']}",
        f"Requestor:              {req['requestor_name']}",
        "",
        f"Calculated risk level:  {report['risk_level']}",
        f"Recommended next step:  {report['recommended_next_step']}",
        "=" * 60,
    ]
    return "\n".join(lines)


# -----------------------------------------------------------------------------
# Persistence
# -----------------------------------------------------------------------------
# Append all reports from this run to intake_log.json for an audit trail.

INTAKE_LOG_PATH = Path(__file__).resolve().parent / "intake_log.json"


def save_reports_to_json(reports: list[dict[str, object]], path: Path) -> None:
    """Write intake reports to JSON, merging with any existing log entries."""
    existing: list[dict[str, object]] = []
    if path.exists():
        with path.open(encoding="utf-8") as handle:
            loaded = json.load(handle)
        if isinstance(loaded, list):
            existing = loaded
        else:
            raise ValueError(f"Expected a JSON array in {path}, got {type(loaded).__name__}")

    combined = existing + reports
    with path.open("w", encoding="utf-8") as handle:
        json.dump(combined, handle, indent=2)
        handle.write("\n")


# -----------------------------------------------------------------------------
# Console summary
# -----------------------------------------------------------------------------


def print_processing_summary(reports: list[dict[str, object]]) -> None:
    """Print how many requests were processed and counts by risk level."""
    total = len(reports)
    breakdown: dict[str, int] = {"Low": 0, "Medium": 0, "High": 0}
    for report in reports:
        level = str(report["risk_level"])
        breakdown[level] = breakdown.get(level, 0) + 1

    print()
    print("INTAKE PROCESSING SUMMARY")
    print("-" * 40)
    print(f"Requests processed: {total}")
    print(f"  Low:    {breakdown['Low']}")
    print(f"  Medium: {breakdown['Medium']}")
    print(f"  High:   {breakdown['High']}")
    print(f"Reports saved to: {INTAKE_LOG_PATH}")


# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------


def main() -> None:
    """Process sample requests, print reports, persist JSON, and show summary."""
    reports: list[dict[str, object]] = []

    for request in SAMPLE_REQUESTS:
        report = build_intake_report(request)
        reports.append(report)
        print(format_intake_report(report))
        print()

    save_reports_to_json(reports, INTAKE_LOG_PATH)
    print_processing_summary(reports)


if __name__ == "__main__":
    main()
