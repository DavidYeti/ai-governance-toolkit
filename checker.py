#!/usr/bin/env python3
"""
Unified multi-framework compliance checker.

Runs keyword-based gap assessment against ISO 42001, ISO 27017, or both.
This is a triage and education tool—not a certification instrument.
"""

from __future__ import annotations

import argparse
import importlib
import sys
from typing import Any

# Sample input for immediate runs; replace with your own description or file input.
SAMPLE_SYSTEM_DESCRIPTION = """
Enterprise Cloud Platform — Multi-Region AWS Deployment

Our organization operates a production cloud environment on AWS spanning three
regions. A shared responsibility matrix documents which security controls are
owned by AWS versus our internal teams. All cloud resources are tracked in an
automated asset inventory with assigned owners and classification tags.

Virtual machines are deployed from CIS-hardened golden images. Production,
staging, and development workloads run in segregated VPCs with least-privilege
security groups and network ACLs. VPC flow logs and CloudWatch monitoring feed
a centralized SIEM with alerting for anomalous traffic and unauthorized access.

Administrative access requires MFA and just-in-time privileged elevation.
Administrator activity is logged and reviewed weekly. All systems synchronize
clocks via NTP with UTC timestamps across logs.

Backup policies cover all cloud-hosted data with encrypted snapshots, quarterly
restore tests, and documented RTO and RPO targets. Vulnerability scanning runs
continuously with defined SLAs for critical patch remediation.

Software installation on production instances is restricted to approved packages
deployed through infrastructure-as-code with change management approval and
rollback procedures. Development and test environments are segregated from
production; test data uses masking and anonymization.

Cloud provider agreements define security responsibilities, SLAs, data ownership,
and breach notification timelines. Supply chain assessments are conducted for
all cloud vendors annually. A cloud-specific incident response plan defines
escalation paths and provider communication channels.

Business continuity plans include multi-region failover tested annually.
Compliance requirements including GDPR data residency are tracked in a legal
register reviewed against provider certification reports each year.
"""

MATURITY_DOES_NOT_EXIST = "Does Not Exist"
MATURITY_PARTIALLY_IMPLEMENTED = "Partially Implemented"
MATURITY_LARGELY_IMPLEMENTED = "Largely Implemented"
MATURITY_FULLY_IMPLEMENTED = "Fully Implemented"

MATURITY_LEVEL_ORDER = (
    MATURITY_DOES_NOT_EXIST,
    MATURITY_PARTIALLY_IMPLEMENTED,
    MATURITY_LARGELY_IMPLEMENTED,
    MATURITY_FULLY_IMPLEMENTED,
)

# Controls at Largely Implemented or Fully Implemented count toward compliance %.
COMPLIANT_MATURITY_LEVELS = frozenset(
    {MATURITY_LARGELY_IMPLEMENTED, MATURITY_FULLY_IMPLEMENTED}
)

FRAMEWORK_REGISTRY: dict[str, str] = {
    "iso42001": "frameworks.iso42001",
    "iso27017": "frameworks.iso27017",
}


def load_framework(framework_key: str) -> dict[str, Any]:
    """
    Import a framework module and return its controls and metadata.

    Each framework module exports FRAMEWORK_METADATA, a controls dictionary,
    and MATURITY_LEVEL_DESCRIPTIONS.
    """
    module_path = FRAMEWORK_REGISTRY[framework_key]
    module = importlib.import_module(module_path)

    if framework_key == "iso42001":
        controls = module.ISO_42001_CONTROLS
    elif framework_key == "iso27017":
        controls = module.ISO_27017_CONTROLS
    else:
        raise ValueError(f"Unknown framework key: {framework_key}")

    return {
        "key": framework_key,
        "metadata": module.FRAMEWORK_METADATA,
        "controls": controls,
        "maturity_descriptions": module.MATURITY_LEVEL_DESCRIPTIONS,
    }


def normalize_for_matching(text: str) -> str:
    """Lowercase the text so keyword checks are case-insensitive."""
    return text.lower()


def find_matching_keywords(description: str, keywords: list[str]) -> list[str]:
    """
    Return which control keywords actually appear in the description.

    Uses simple substring matching: if a keyword string appears anywhere in
    the description, it counts as a match.
    """
    desc_lower = normalize_for_matching(description)
    matches: list[str] = []
    for term in keywords:
        if term.lower() in desc_lower:
            matches.append(term)
    return matches


def compute_confidence(matched_count: int, total_count: int) -> tuple[int, int, int]:
    """
    Build the confidence score as matched keywords out of total keywords.

    Returns (matched_count, total_count, percentage) where percentage is
    rounded to the nearest whole number for display.
    """
    if total_count == 0:
        return 0, 0, 0
    pct = round((matched_count / total_count) * 100)
    return matched_count, total_count, pct


def maturity_from_confidence_pct(pct: int) -> str:
    """
    Map confidence percentage to a four-level maturity rating.

    Maturity thresholds (based on keyword-match confidence):
      0%           -> Does Not Exist
      1% to 49%    -> Partially Implemented
      50% to 79%   -> Largely Implemented
      80% to 100%  -> Fully Implemented
    """
    if pct == 0:
        return MATURITY_DOES_NOT_EXIST
    if pct <= 49:
        return MATURITY_PARTIALLY_IMPLEMENTED
    if pct <= 79:
        return MATURITY_LARGELY_IMPLEMENTED
    return MATURITY_FULLY_IMPLEMENTED


def evaluate_control(
    control: dict[str, object], description: str
) -> tuple[str, str, int, int, int]:
    """
    Run the keyword check for one control and derive maturity from confidence.

    Returns:
        maturity: Four-level status label for the report Status line.
        note: Short human-readable explanation of keyword matches.
        matched_count, total_count, confidence_pct: for Confidence line display.
    """
    keywords = control["keywords"]  # type: ignore[assignment]
    assert isinstance(keywords, list)
    matched = find_matching_keywords(description, keywords)
    total_count = len(keywords)
    matched_count = len(matched)
    matched_count, total_count, confidence_pct = compute_confidence(
        matched_count, total_count
    )
    maturity = maturity_from_confidence_pct(confidence_pct)

    if matched:
        terms = ", ".join(matched)
        note = (
            f"Passed: the description mentions term(s) aligned with this control "
            f"({terms})."
        )
    else:
        note = (
            f"Failed: none of the lookup terms for this control were found "
            f"({', '.join(keywords)})."
        )
    return maturity, note, matched_count, total_count, confidence_pct


def print_maturity_level_key(maturity_descriptions: dict[str, str]) -> None:
    """Print the maturity rating scale before individual control findings."""
    print("\n" + "=" * 72)
    print("MATURITY LEVEL KEY")
    print("=" * 72 + "\n")
    for level in MATURITY_LEVEL_ORDER:
        print(f"{level}")
        print(f"  {maturity_descriptions[level]}")
        print()
    print("=" * 72)


def print_recommended_actions(control: dict[str, object]) -> None:
    """
    Print actionable recommendations for controls below Fully Implemented.

    Fully Implemented controls already show strong keyword evidence; others
    receive remediation guidance from the control's recommendations list.
    """
    recommendations = control["recommendations"]  # type: ignore[assignment]
    assert isinstance(recommendations, list)
    print("Recommended Actions:")
    for index, action in enumerate(recommendations, start=1):
        print(f"  {index}. {action}")


def empty_maturity_counts() -> dict[str, int]:
    """Return a zeroed maturity count dictionary for summary aggregation."""
    return {level: 0 for level in MATURITY_LEVEL_ORDER}


def print_findings_report(
    framework: dict[str, Any], description: str
) -> tuple[int, dict[str, int], float]:
    """
    Print each control's result for one framework.

    Returns total controls checked, maturity counts, and compliance score.
    """
    metadata = framework["metadata"]
    controls = framework["controls"]
    maturity_descriptions = framework["maturity_descriptions"]

    total = 0
    maturity_counts = empty_maturity_counts()

    print_maturity_level_key(maturity_descriptions)
    print(f"\n{metadata['name']} — keyword assessment — findings")
    print("=" * 72 + "\n")

    for control_id in controls:
        total += 1
        control = controls[control_id]
        assert isinstance(control, dict)
        name = str(control["name"])
        maturity, note, matched_count, total_count, confidence_pct = evaluate_control(
            control, description
        )
        maturity_counts[maturity] += 1

        print(f"Control:   {control_id}")
        print(f"Name:      {name}")
        print(f"Status:    {maturity}")
        print(f"Confidence: {matched_count}/{total_count} ({confidence_pct}%)")
        print(f"Note:      {note}")
        if maturity != MATURITY_FULLY_IMPLEMENTED:
            print_recommended_actions(control)
        print("-" * 72)

    compliance_score = compute_compliance_score(total, maturity_counts)
    print_summary(metadata, total, maturity_counts, compliance_score)
    return total, maturity_counts, compliance_score


def compute_compliance_score(
    total: int, maturity_counts: dict[str, int]
) -> float:
    """
    Calculate compliance percentage from maturity counts.

    Compliance = share of controls rated Largely Implemented or Fully Implemented.
    """
    if total == 0:
        return 0.0
    compliant_count = (
        maturity_counts[MATURITY_LARGELY_IMPLEMENTED]
        + maturity_counts[MATURITY_FULLY_IMPLEMENTED]
    )
    return (compliant_count / total) * 100.0


def print_summary(
    metadata: dict[str, object],
    total: int,
    maturity_counts: dict[str, int],
    compliance_score: float,
) -> None:
    """Print maturity-level totals and compliance percentage for one framework."""
    print("\n" + "=" * 72)
    print("Summary")
    print("=" * 72)
    print(f"Framework:                  {metadata['name']}")
    print(f"Controls checked:           {total}")
    print(f"Does Not Exist:             {maturity_counts[MATURITY_DOES_NOT_EXIST]}")
    print(
        f"Partially Implemented:    {maturity_counts[MATURITY_PARTIALLY_IMPLEMENTED]}"
    )
    print(f"Largely Implemented:      {maturity_counts[MATURITY_LARGELY_IMPLEMENTED]}")
    print(f"Fully Implemented:        {maturity_counts[MATURITY_FULLY_IMPLEMENTED]}")
    print(f"Compliance score:          {compliance_score:.1f}%")
    print(
        "\nNote: This score reflects keyword overlap only, not formal conformance "
        f"to {metadata['name']}."
    )
    print("=" * 72 + "\n")


def print_combined_summary(
    results: list[tuple[dict[str, Any], float]],
) -> None:
    """Print a side-by-side compliance summary when running all frameworks."""
    print("\n" + "=" * 72)
    print("COMBINED SUMMARY")
    print("=" * 72 + "\n")

    header = f"{'Framework':<30} {'Domain':<20} {'Controls':<10} {'Score':<10}"
    print(header)
    print("-" * 72)

    for framework, score in results:
        metadata = framework["metadata"]
        print(
            f"{metadata['name']:<30} "
            f"{metadata['domain']:<20} "
            f"{metadata['total_controls']:<10} "
            f"{score:.1f}%"
        )

    print("\n" + "=" * 72 + "\n")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments for framework selection."""
    parser = argparse.ArgumentParser(
        description="Multi-framework compliance checker using keyword matching."
    )
    parser.add_argument(
        "--framework",
        choices=["iso42001", "iso27017", "all"],
        required=True,
        help="Compliance framework to assess (iso42001, iso27017, or all).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Entry point: load framework(s), assess sample description, print reports."""
    args = parse_args(argv)
    description = SAMPLE_SYSTEM_DESCRIPTION

    if args.framework == "all":
        combined_results: list[tuple[dict[str, Any], float]] = []
        for framework_key in ("iso42001", "iso27017"):
            framework = load_framework(framework_key)
            _, _, compliance_score = print_findings_report(framework, description)
            combined_results.append((framework, compliance_score))
        print_combined_summary(combined_results)
        return

    framework = load_framework(args.framework)
    print_findings_report(framework, description)


if __name__ == "__main__":
    main()
