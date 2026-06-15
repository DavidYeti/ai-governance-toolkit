#!/usr/bin/env python3
"""
ISO/IEC -style AI management system gap check (demo).

This script uses simple keyword matching against a free-text description of an
system. It is not a certification tool—use it for awareness and triage only.
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
# Each entry is one control: keywords for matching, recommendations for remediation
# when maturity is below Fully Implemented. Maturity uses keyword confidence;
# real assessments still need evidence beyond keywords.
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
        "recommendations": [
            "Document a stakeholder register identifying all interested parties affected by AI systems including customers regulators and employees.",
            "Conduct periodic stakeholder needs assessments and update AI governance policies accordingly.",
            "Establish a formal feedback mechanism for stakeholders to raise AI-related concerns.",
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
        "recommendations": [
            "Conduct and document an organizational context analysis covering internal capabilities and external regulatory requirements affecting AI.",
            "Maintain a risk register that captures environmental factors influencing AI system design and deployment.",
            "Review context analysis at least annually or when significant changes occur.",
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
        "recommendations": [
            "Obtain and document executive sponsorship for the AI management system with named accountability at the leadership level.",
            "Include AI governance in board-level reporting and strategic planning cycles.",
            "Ensure leadership allocates sufficient resources and authority to the AI governance function.",
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
        "recommendations": [
            "Draft and approve a formal AI policy signed by executive leadership covering responsible use safety security and ethics.",
            "Communicate the AI policy to all relevant personnel and make it accessible to external stakeholders where appropriate.",
            "Review and update the AI policy at least annually.",
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
        "recommendations": [
            "Develop a formal AI risk assessment methodology covering the full system lifecycle from design through decommission.",
            "Document risk treatment plans for each identified AI risk with assigned owners and target resolution dates.",
            "Integrate AI risk reviews into existing enterprise risk management processes.",
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
        "recommendations": [
            "Define and document roles and responsibilities for AI governance including an AI system owner for each deployed system.",
            "Establish an AI governance committee or oversight body with clear decision-making authority.",
            "Communicate role assignments to all affected personnel through documented organizational charts or RACI matrices.",
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
        "recommendations": [
            "Conduct documented impact assessments for each AI system evaluating potential harms to individuals groups and society before deployment.",
            "Include bias fairness and discrimination analysis in all AI system impact assessments.",
            "Establish a threshold above which a formal third-party impact assessment is required.",
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
        "recommendations": [
            "Develop a competency framework for all roles involved in AI system design development and operation.",
            "Deliver and document mandatory AI awareness training for all personnel interacting with AI systems.",
            "Track training completion and establish a minimum refresh cycle of annually.",
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
        "recommendations": [
            "Establish a document control process for all AI governance artifacts including policies procedures risk assessments and audit reports.",
            "Maintain version-controlled records of AI system configurations model versions and change histories.",
            "Define retention periods and access controls for all AI governance documentation.",
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
        "recommendations": [
            "Document operational procedures for all AI system processes including data ingestion model inference and output handling.",
            "Implement monitoring and alerting for AI system performance against defined operational criteria.",
            "Establish incident response procedures specific to AI system failures or unexpected behaviors.",
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
        "recommendations": [
            "Define and document the human oversight requirements for each AI system including when human review is mandatory before action is taken.",
            "Implement technical controls that require human approval for high-risk AI-generated outputs or decisions.",
            "Maintain logs of human oversight interventions and their outcomes for audit purposes.",
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
        "recommendations": [
            "Document a data governance policy covering data quality privacy and appropriate use for all AI training and inference data.",
            "Implement data classification controls that restrict sensitive data from being used in AI systems without appropriate safeguards.",
            "Establish data retention and deletion procedures aligned with privacy regulations for all AI-related data.",
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
        "recommendations": [
            "Maintain an inventory of all third-party AI components models and services used across the organization.",
            "Conduct security and governance assessments of AI vendors and suppliers before procurement and annually thereafter.",
            "Include AI supply chain security requirements in all third-party contracts and service agreements.",
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
        "recommendations": [
            "Establish a responsible AI development framework covering ethical review safety testing and security validation before deployment.",
            "Implement pre-deployment testing procedures that verify AI system behavior against defined safety and security requirements.",
            "Document and communicate responsible AI principles to all development teams with accountability for compliance.",
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
        "recommendations": [
            "Conduct regular adversarial testing including red team exercises and prompt injection testing for all externally-facing AI systems.",
            "Implement technical controls to detect and block adversarial inputs at the inference layer.",
            "Maintain threat intelligence subscriptions specific to AI security and update detection rules accordingly.",
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
        "recommendations": [
            "Document how each AI system makes decisions and what factors influence its outputs in language accessible to non-technical stakeholders.",
            "Implement explainability features that allow end users and auditors to understand why specific AI outputs were generated.",
            "Establish a process for responding to stakeholder requests for explanation of AI-generated decisions.",
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
        "recommendations": [
            "Define and track key performance indicators for each AI system covering accuracy reliability and business impact.",
            "Implement automated monitoring that generates alerts when AI system performance falls below defined thresholds.",
            "Conduct formal quarterly reviews of AI system performance metrics with leadership reporting.",
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
        "recommendations": [
            "Establish an internal audit schedule for the AI management system with audits conducted at least annually.",
            "Train internal auditors on ISO 42001 requirements and AI-specific audit techniques.",
            "Document audit findings corrective actions and follow-up verification in a centralized audit management system.",
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
        "recommendations": [
            "Implement a formal nonconformity management process that captures investigates and resolves deviations from AI governance requirements.",
            "Assign root cause analysis and corrective action ownership for all significant AI system failures or governance gaps.",
            "Track corrective action completion and verify effectiveness before closing nonconformities.",
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
        "recommendations": [
            "Conduct an annual management review of the AI management system covering performance trends audit results and improvement opportunities.",
            "Establish a continuous improvement roadmap for AI governance maturity with measurable targets and timelines.",
            "Implement a lessons learned process that captures insights from AI incidents and improvement initiatives.",
        ],
    },
}

# -----------------------------------------------------------------------------
# Maturity levels (four-tier rating from keyword-match confidence percentage)
# -----------------------------------------------------------------------------
# Confidence = matched_keywords / total_keywords for each control.
# The percentage maps to exactly one maturity label for the Status line.
MATURITY_DOES_NOT_EXIST = "Does Not Exist"
MATURITY_PARTIALLY_IMPLEMENTED = "Partially Implemented"
MATURITY_LARGELY_IMPLEMENTED = "Largely Implemented"
MATURITY_FULLY_IMPLEMENTED = "Fully Implemented"

# Two-sentence explanations of each maturity rating for readers of the report.
MATURITY_LEVEL_DESCRIPTIONS: dict[str, str] = {
    MATURITY_DOES_NOT_EXIST: (
        "No evidence found that this control requirement is addressed in the "
        "system description or documentation. Immediate remediation is required "
        "before this control can be considered for compliance."
    ),
    MATURITY_PARTIALLY_IMPLEMENTED: (
        "Some evidence exists that this control area is being addressed but "
        "coverage is insufficient to satisfy the full control requirement. "
        "Targeted remediation is needed to close the identified gaps."
    ),
    MATURITY_LARGELY_IMPLEMENTED: (
        "Most control requirements are addressed with evidence present for the "
        "majority of expected criteria. Minor gaps remain and specific evidence "
        "collection is needed to achieve full implementation."
    ),
    MATURITY_FULLY_IMPLEMENTED: (
        "Strong evidence exists across all or nearly all control criteria "
        "indicating this requirement is well addressed. Maintain current practices "
        "and verify evidence remains current during periodic reviews."
    ),
}

# Controls at Largely Implemented or Fully Implemented count toward compliance %.
COMPLIANT_MATURITY_LEVELS = frozenset(
    {MATURITY_LARGELY_IMPLEMENTED, MATURITY_FULLY_IMPLEMENTED}
)


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


def compute_confidence(matched_count: int, total_count: int) -> tuple[int, int, int]:
    """
    Build the confidence score as matched keywords out of total keywords.

    Returns (matched_count, total_count, percentage) where percentage is
    rounded to the nearest whole number for display (e.g. 4/6 -> 67%).
    """
    if total_count == 0:
        return 0, 0, 0
    pct = round((matched_count / total_count) * 100)
    return matched_count, total_count, pct


def maturity_from_confidence_pct(pct: int) -> str:
    """
    Map confidence percentage to a four-level maturity rating.

    0% -> Does Not Exist; 1-49% -> Partially Implemented;
    50-79% -> Largely Implemented; 80-100% -> Fully Implemented.
    """
    if pct == 0:
        return MATURITY_DOES_NOT_EXIST
    if pct <= 49:
        return MATURITY_PARTIALLY_IMPLEMENTED
    if pct <= 79:
        return MATURITY_LARGELY_IMPLEMENTED
    return MATURITY_FULLY_IMPLEMENTED


def evaluate_control(
    control_id: str, control: dict[str, object], description: str
) -> tuple[str, str, int, int, int]:
    """
    Run the keyword check for one control and derive maturity from confidence.

    Returns:
        maturity: Four-level status label for the report Status line.
        note: Short human-readable explanation (which keywords matched or not).
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


def print_maturity_level_key() -> None:
    """Print the maturity rating scale before individual control findings."""
    print("\n" + "=" * 72)
    print("MATURITY LEVEL KEY")
    print("=" * 72 + "\n")
    for level in (
        MATURITY_DOES_NOT_EXIST,
        MATURITY_PARTIALLY_IMPLEMENTED,
        MATURITY_LARGELY_IMPLEMENTED,
        MATURITY_FULLY_IMPLEMENTED,
    ):
        print(f"{level}")
        print(f"  {MATURITY_LEVEL_DESCRIPTIONS[level]}")
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


def print_findings_report(description: str) -> tuple[int, dict[str, int]]:
    """
    Print each control's result, then return (total_checked, maturity_counts).

    Maturity counts feed the summary; compliance uses Largely + Fully Implemented.
    """
    total = 0
    maturity_counts: dict[str, int] = {
        MATURITY_DOES_NOT_EXIST: 0,
        MATURITY_PARTIALLY_IMPLEMENTED: 0,
        MATURITY_LARGELY_IMPLEMENTED: 0,
        MATURITY_FULLY_IMPLEMENTED: 0,
    }

    print_maturity_level_key()
    print("\nISO 42001–style keyword assessment — findings")
    print("=" * 72 + "\n")

    for control_id in ISO_42001_CONTROLS:
        total += 1
        control = ISO_42001_CONTROLS[control_id]
        assert isinstance(control, dict)
        name = str(control["name"])
        maturity, note, matched_count, total_count, confidence_pct = evaluate_control(
            control_id, control, description
        )
        maturity_counts[maturity] += 1

        print(f"Control:   {control_id}")
        print(f"Name:      {name}")
        print(f"Status:    {maturity}")
        print(
            f"Confidence: {matched_count}/{total_count} ({confidence_pct}%)"
        )
        print(f"Note:      {note}")
        if maturity != MATURITY_FULLY_IMPLEMENTED:
            print_recommended_actions(control)
        print("-" * 72)

    return total, maturity_counts


def print_summary(total: int, maturity_counts: dict[str, int]) -> None:
    """
    Print maturity-level totals and compliance percentage.

    Compliance = share of controls rated Largely Implemented or Fully Implemented.
    """
    compliant_count = (
        maturity_counts[MATURITY_LARGELY_IMPLEMENTED]
        + maturity_counts[MATURITY_FULLY_IMPLEMENTED]
    )
    if total == 0:
        pct = 0.0
    else:
        pct = (compliant_count / total) * 100.0

    print("\n" + "=" * 72)
    print("Summary")
    print("=" * 72)
    print(f"Controls checked:           {total}")
    print(f"Does Not Exist:             {maturity_counts[MATURITY_DOES_NOT_EXIST]}")
    print(
        f"Partially Implemented:    {maturity_counts[MATURITY_PARTIALLY_IMPLEMENTED]}"
    )
    print(f"Largely Implemented:      {maturity_counts[MATURITY_LARGELY_IMPLEMENTED]}")
    print(f"Fully Implemented:        {maturity_counts[MATURITY_FULLY_IMPLEMENTED]}")
    print(f"Compliance score:          {pct:.1f}%")
    print(
        "\nNote: This score reflects keyword overlap only, not formal conformance "
        "to ISO/IEC 42001."
    )
    print("=" * 72 + "\n")


def main() -> None:
    """Entry point: assess the sample description and print the full report."""
    total, maturity_counts = print_findings_report(SAMPLE_AI_SYSTEM_DESCRIPTION)
    print_summary(total, maturity_counts)


if __name__ == "__main__":
    main()
