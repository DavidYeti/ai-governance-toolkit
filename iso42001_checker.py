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
ACME Corp Internal Candidate Screening Assistant (ICSA)

We operate a resume ranking and shortlisting tool used by HR. The system ingests
applicant PDFs, extracts skills with an LLM API, and scores fit against job
descriptions. Model versions are logged in a model registry. HR staff review
every shortlist before outreach—no fully automated hiring decisions.

We track latency, cost, and weekly usage in a dashboard. Annual vendor security
reviews cover the API provider. We have a short data retention policy for raw
resumes. Incident reports go to the security mailbox but we have not run a
full internal audit cycle yet. Training for recruiters on fair use is planned
for next quarter.
"""


# -----------------------------------------------------------------------------
# ISO 42001–inspired controls (simplified for education)
# -----------------------------------------------------------------------------
# Each entry is one control. "keywords" are plain words or short phrases we
# look for in the system description. If at least one appears, we treat the
# control check as "passed" for this demo (real assessments need evidence).
ISO_42001_CONTROLS: dict[str, dict[str, object]] = {
    "ISO-42001-A.6.1": {
        "name": "AI system lifecycle and risk treatment",
        "description": (
            "The organization shall determine risks related to its AI systems "
            "and plan how they are addressed through the lifecycle."
        ),
        "keywords": ["risk", "lifecycle", "mitigation", "treatment", "impact"],
    },
    "ISO-42001-A.6.2": {
        "name": "Roles, responsibilities, and authorities",
        "description": (
            "Responsibilities for the AI management system shall be assigned "
            "and communicated."
        ),
        "keywords": ["responsib", "role", "owner", "accountable", "governance"],
    },
    "ISO-42001-A.7.1": {
        "name": "Competence and awareness",
        "description": (
            "People affecting AI performance shall be competent on the basis of "
            "education, training, or experience; awareness shall be promoted."
        ),
        "keywords": ["training", "competen", "awareness", "education", "skill"],
    },
    "ISO-42001-A.7.2": {
        "name": "Documented information",
        "description": (
            "The AI management system shall include documented information "
            "needed for effectiveness."
        ),
        "keywords": ["document", "policy", "procedure", "record", "specification"],
    },
    "ISO-42001-A.8.1": {
        "name": "Operational planning and control",
        "description": (
            "AI processes shall be carried out under controlled conditions using "
            "established criteria."
        ),
        "keywords": ["operational", "control", "process", "monitor", "criteria"],
    },
    "ISO-42001-A.8.2": {
        "name": "Human oversight",
        "description": (
            "Appropriate human oversight shall be applied to AI systems, "
            "especially for high-impact contexts."
        ),
        "keywords": ["human", "oversight", "review", "supervis", "intervention"],
    },
    "ISO-42001-A.9.1": {
        "name": "Monitoring, measurement, analysis, evaluation",
        "description": (
            "The organization shall evaluate performance and effectiveness of "
            "the AI management system."
        ),
        "keywords": ["metric", "measure", "dashboard", "kpi", "evaluation"],
    },
    "ISO-42001-A.9.2": {
        "name": "Internal audit",
        "description": (
            "Internal audits shall be conducted at planned intervals to verify "
            "conformance."
        ),
        "keywords": ["internal audit", "audit", "assurance"],
    },
    "ISO-42001-A.10.1": {
        "name": "Nonconformity and corrective action",
        "description": (
            "Nonconformities shall be reacted to and corrected; continual "
            "improvement shall be supported."
        ),
        "keywords": ["corrective", "improvement", "nonconform", "incident", "lesson"],
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
