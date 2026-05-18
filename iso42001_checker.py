#!/usr/bin/env python3
"""
ISO/IEC 42001-style AI management system gap check (demo).

This script uses simple keyword matching against a free-text description of an
AI system. It is not a certification tool—use it for awareness and triage only.
"""

from __future__ import annotations

# -----------------------------------------------------------------------------
# Sample input (replace with your own description or read from a file later)
# -----------------------------------------------------------------------------
# This hardcoded example lets you run the script immediately with no arguments.
# It describes a fictional internal tool so the report shows a mix of pass/fail.
SAMPLE_AI_SYSTEM_DESCRIPTION = """
Cisco AI Defense — Enterprise AI Security Platform

Cisco AI Defense provides end-to-end protection for enterprises building using and innovating with AI. Whether the organization is using third-party AI applications or developing its own the platform addresses safety and security without sacrificing speed.

Using AI: Automatically surfaces third-party AI applications in use across the organization. Defines policies that manage employee access protect against threats and prevent sensitive data loss.

Developing AI: Detects AI assets across the environment. Algorithmically assesses models to identify vulnerabilities then deploys guardrails to protect AI applications and customers in real time.

Threat Mitigation: Protects AI applications against rapidly evolving threats including prompt injections denial of service and data leakage. Advanced guardrails go beyond prompt injection to detect model denial of service code detection and off-topic attacks.

Visibility and Risk: Detects misconfigurations security vulnerabilities and adversarial attacks. Automatically inventories AI models connected data sources and users across distributed cloud environments.

AI Model and Application Validation: Identifies safety and security vulnerabilities across models at scale using algorithmic red teaming technology to assess AI risk in seconds.

AI Runtime Protection: Protects production AI applications with guardrails embedded in the network blocking adversarial attacks and harmful responses in real time.

AI Access Management: Monitors and manages access to third-party AI applications. Enforces policies that limit sensitive data exposure and protect against external threats.

AI Supply Chain Risk Management: Provides governance and security over AI models and files. Manages risks associated with third-party AI components.

Standards Alignment: Cisco collaborated with AI security standards bodies including NIST MITRE ATLAS and OWASP LLM Top 10. AI Defense helps organizations align to these standards with a single integration.

Responsible AI: Cisco is dedicated to securing artificial intelligence and emerging technologies. Responsible AI principles are embedded in the platform design. Talos threat intelligence informs detections and provides instant platform updates.

Network-level visibility across the enterprise with mature guardrails and live threat intelligence updates makes Cisco AI Defense the enterprise choice to secure usage and development of AI.

"""


# -----------------------------------------------------------------------------
# ISO 42001–inspired controls (simplified for education)
# -----------------------------------------------------------------------------
# Each entry is one control. "keywords" are plain words or short phrases we
# look for in the system description. If at least one appears, we treat the
# control check as "passed" for this demo (real assessments need evidence).
ISO_42001_CONTROLS: dict[str, dict[str, object]] = {
    "ISO-42001-A.2.2": {
        "name": "Stakeholder needs and AI expectations",
        "description": (
            "The organization shall determine the needs and expectations of "
            "interested parties relevant to its AI management system"
        ),
        "keywords": [
            "stakeholder",
            "interested party",
            "expectation",
            "requirement",
            "customer",
            "regulatory",
        ],
    },
    "ISO-42001-A.4.1": {
        "name": "Organizational context for AI",
        "description": (
            "The organization shall determine external and internal issues "
            "relevant to its purpose that affect its ability to achieve intended "
            "outcomes of the AI management system"
        ),
        "keywords": [
            "context",
            "organizational",
            "internal",
            "external",
            "environment",
            "objective",
        ],
    },
    "ISO-42001-A.5.1": {
        "name": "Leadership and AI commitment",
        "description": (
            "Top management shall demonstrate leadership and commitment with "
            "respect to the AI management system"
        ),
        "keywords": [
            "leadership",
            "management",
            "commitment",
            "executive",
            "board",
            "sponsor",
        ],
    },
    "ISO-42001-A.5.2": {
        "name": "AI policy",
        "description": (
            "Top management shall establish an AI policy that is appropriate to "
            "the purpose of the organization and provides a framework for setting "
            "AI objectives"
        ),
        "keywords": [
            "policy",
            "principle",
            "commitment",
            "framework",
            "objective",
            "guideline",
        ],
    },
    "ISO-42001-A.6.1": {
        "name": "AI risk treatment and lifecycle",
        "description": (
            "The organization shall determine risks related to its AI systems "
            "and plan how they are addressed through the lifecycle"
        ),
        "keywords": [
            "risk",
            "lifecycle",
            "mitigation",
            "treatment",
            "impact",
            "assessment",
        ],
    },
    "ISO-42001-A.6.2": {
        "name": "Roles responsibilities and authorities",
        "description": (
            "Responsibilities for the AI management system shall be assigned "
            "and communicated"
        ),
        "keywords": [
            "responsib",
            "role",
            "owner",
            "accountable",
            "governance",
            "authority",
        ],
    },
    "ISO-42001-A.6.3": {
        "name": "AI system impact assessment",
        "description": (
            "The organization shall conduct an impact assessment for AI systems "
            "considering potential harms to individuals and society"
        ),
        "keywords": [
            "impact",
            "harm",
            "assessment",
            "bias",
            "fairness",
            "discrimination",
            "consequence",
        ],
    },
    "ISO-42001-A.7.1": {
        "name": "Competence and awareness",
        "description": (
            "People affecting AI performance shall be competent on the basis of "
            "education training or experience and awareness shall be promoted"
        ),
        "keywords": [
            "training",
            "competence",
            "awareness",
            "education",
            "skill",
            "certification",
        ],
    },
    "ISO-42001-A.7.2": {
        "name": "Documented information",
        "description": (
            "The AI management system shall include documented information "
            "needed for effectiveness"
        ),
        "keywords": [
            "document",
            "policy",
            "procedure",
            "record",
            "specification",
            "log",
        ],
    },
    "ISO-42001-A.8.1": {
        "name": "Operational planning and control",
        "description": (
            "AI processes shall be carried out under controlled conditions using "
            "established criteria"
        ),
        "keywords": [
            "operational",
            "control",
            "process",
            "monitor",
            "criteria",
            "procedure",
        ],
    },
    "ISO-42001-A.8.2": {
        "name": "Human oversight",
        "description": (
            "Appropriate human oversight shall be applied to AI systems especially "
            "for high-impact contexts"
        ),
        "keywords": [
            "human",
            "oversight",
            "review",
            "supervise",
            "intervention",
            "approval",
        ],
    },
    "ISO-42001-A.8.3": {
        "name": "Data governance for AI",
        "description": (
            "The organization shall ensure that data used in AI systems is managed "
            "appropriately with regard to quality relevance and privacy"
        ),
        "keywords": [
            "data",
            "quality",
            "privacy",
            "governance",
            "dataset",
            "training data",
            "sensitive",
        ],
    },
    "ISO-42001-A.8.4": {
        "name": "AI supply chain and third-party risk",
        "description": (
            "The organization shall manage risks associated with third-party AI "
            "components suppliers and services"
        ),
        "keywords": [
            "supply chain",
            "third-party",
            "vendor",
            "supplier",
            "model",
            "open source",
            "dependency",
        ],
    },
    "ISO-42001-A.8.5": {
        "name": "Responsible development and deployment",
        "description": (
            "The organization shall ensure that AI systems are developed and "
            "deployed responsibly with consideration for safety security and "
            "ethical implications"
        ),
        "keywords": [
            "responsible",
            "ethical",
            "safe",
            "secure",
            "deploy",
            "development",
            "guardrail",
        ],
    },
    "ISO-42001-A.8.6": {
        "name": "Adversarial robustness and threat protection",
        "description": (
            "The organization shall identify and address threats specific to AI "
            "systems including adversarial attacks prompt injection and model "
            "manipulation"
        ),
        "keywords": [
            "adversarial",
            "prompt injection",
            "attack",
            "threat",
            "robustness",
            "red team",
            "manipulation",
        ],
    },
    "ISO-42001-A.8.7": {
        "name": "Transparency and explainability",
        "description": (
            "The organization shall ensure appropriate transparency and "
            "explainability of AI system decisions and outputs"
        ),
        "keywords": [
            "transparent",
            "explain",
            "interpret",
            "explainab",
            "visible",
            "understandab",
        ],
    },
    "ISO-42001-A.9.1": {
        "name": "Monitoring measurement and evaluation",
        "description": (
            "The organization shall evaluate performance and effectiveness of "
            "the AI management system"
        ),
        "keywords": [
            "metric",
            "measure",
            "dashboard",
            "monitor",
            "evaluate",
            "performance",
            "kpi",
        ],
    },
    "ISO-42001-A.9.2": {
        "name": "Internal audit",
        "description": (
            "Internal audits shall be conducted at planned intervals to verify "
            "conformance"
        ),
        "keywords": [
            "audit",
            "internal audit",
            "assurance",
            "conformance",
            "verification",
            "assessment",
        ],
    },
    "ISO-42001-A.10.1": {
        "name": "Nonconformity and corrective action",
        "description": (
            "Nonconformities shall be reacted to and corrected and continual "
            "improvement shall be supported"
        ),
        "keywords": [
            "corrective",
            "improvement",
            "nonconform",
            "incident",
            "remediation",
            "lesson",
        ],
    },
    "ISO-42001-A.10.2": {
        "name": "Continual improvement of AI systems",
        "description": (
            "The organization shall continually improve the suitability adequacy "
            "and effectiveness of the AI management system"
        ),
        "keywords": [
            "improve",
            "enhance",
            "iterate",
            "update",
            "evolve",
            "maturity",
            "continuous",
        ],
    },
}


def normalize_for_matching(text: str) -> str:
    """Lowercase the text so keyword checks are case-insensitive."""
    return text.lower()


def find_matching_keywords(description: str, keywords: list[str]) -> list[str]:
    """
    Return which control keywords actually appear in the description.

    We use simple substring matching: if a keyword string appears anywhere in
    the description, it counts as a match. (This is quick but can occasionally
    match inside unrelated words—acceptable for a teaching/demo script.)
    """
    desc_lower = normalize_for_matching(description)
    matches: list[str] = []
    for term in keywords:
        if term.lower() in desc_lower:
            matches.append(term)
    return matches


def evaluate_control(control_id: str, control: dict[str, object], description: str) -> tuple[bool, str, str | None]:
    """
    Run the keyword check for one control.

    Returns:
        passed: True if at least one keyword was found.
        note: Short human-readable explanation for the report.
        matched_terms: Comma-separated list of matched keywords, or None.
    """
    keywords = control["keywords"]  # type: ignore[assignment]
    assert isinstance(keywords, list)
    matched = find_matching_keywords(description, keywords)
    if matched:
        terms = ", ".join(matched)
        note = (
            f"Passed: the description mentions term(s) aligned with this control "
            f"({terms})."
        )
        return True, note, terms
    note = (
        f"Failed: none of the lookup terms for this control were found "
        f"({', '.join(keywords)})."
    )
    return False, note, None


def print_findings_report(description: str) -> tuple[int, int]:
    """
    Print each control's result, then return (total_checked, passed_count).

    The summary line at the end of the script uses these counts to compute the
    compliance score.
    """
    total = 0
    passed_count = 0

    print("\n" + "=" * 72)
    print("ISO 42001–style keyword assessment — findings")
    print("=" * 72 + "\n")

    for control_id in ISO_42001_CONTROLS:
        total += 1
        control = ISO_42001_CONTROLS[control_id]
        assert isinstance(control, dict)
        name = str(control["name"])
        passed, note, _ = evaluate_control(control_id, control, description)

        if passed:
            passed_count += 1
            status = "PASS"
        else:
            status = "FAIL"

        print(f"Control:   {control_id}")
        print(f"Name:      {name}")
        print(f"Status:    {status}")
        print(f"Note:      {note}")
        print("-" * 72)

    return total, passed_count


def print_summary(total: int, passed: int) -> None:
    """Print totals and a simple compliance percentage (passed / total)."""
    failed = total - passed
    if total == 0:
        pct = 0.0
    else:
        pct = (passed / total) * 100.0

    print("\n" + "=" * 72)
    print("Summary")
    print("=" * 72)
    print(f"Controls checked:        {total}")
    print(f"Passed (keyword match): {passed}")
    print(f"Failed:                 {failed}")
    print(f"Compliance score:      {pct:.1f}%")
    print(
        "\nNote: This score reflects keyword overlap only, not formal conformance "
        "to ISO/IEC 42001."
    )
    print("=" * 72 + "\n")


def main() -> None:
    """Entry point: assess the sample description and print the full report."""
    total, passed = print_findings_report(SAMPLE_AI_SYSTEM_DESCRIPTION)
    print_summary(total, passed)


if __name__ == "__main__":
    main()
