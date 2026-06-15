"""Reusable display helpers for the Streamlit frontend."""

from __future__ import annotations

import pandas as pd

FRAMEWORK_LABELS = {
    "iso42001": "🤖 ISO 42001 — AI Management",
    "iso27017": "☁️ ISO 27017 — Cloud Security",
    "iso27018": "🔒 ISO 27018 — Cloud PII",
}

FRAMEWORK_DESCRIPTIONS = {
    "iso42001": "AI Management System — 20 controls covering responsible AI development, risk management, and governance.",
    "iso27017": "Cloud Security Controls — security controls for cloud service providers and customers.",
    "iso27018": "Cloud PII Protection — controls for protecting personally identifiable information in public cloud.",
}


def framework_label(fw_id: str) -> str:
    return FRAMEWORK_LABELS.get(fw_id, fw_id)


def status_emoji(status: str) -> str:
    return {"ADDRESSED": "✅", "PARTIAL": "⚠️", "GAP": "❌"}.get(status, "❓")


def maturity_badge(maturity: str) -> str:
    colors = {
        "Defined": "🟢",
        "Developing": "🔵",
        "Initial": "🟡",
        "Not Implemented": "🔴",
    }
    return f"{colors.get(maturity, '⚪')} {maturity}"


def score_grade(score_pct: float) -> str:
    if score_pct >= 80:
        return "A"
    if score_pct >= 65:
        return "B"
    if score_pct >= 50:
        return "C"
    if score_pct >= 35:
        return "D"
    return "F"


def results_to_dataframe(controls: list[dict]) -> pd.DataFrame:
    rows = []
    for r in controls:
        rows.append({
            "Control ID": r["control_id"],
            "Control Name": r["control_name"],
            "Status": f"{status_emoji(r['status'])} {r['status']}",
            "Maturity": r["maturity"],
            "Confidence": f"{int(r['confidence_score'] * 100)}%",
            "Evidence Found": "Yes" if r["evidence_snippets"] else "No",
        })
    return pd.DataFrame(rows)


def summary_card_html(fw_id: str, summary: dict) -> str:
    """Return HTML for a metric summary card."""
    label = FRAMEWORK_LABELS.get(fw_id, fw_id)
    score = summary["score_pct"]
    grade = score_grade(score)
    return f"""
    <div style="border:1px solid #d0d8e4; border-radius:8px; padding:16px; background:#f8fafc; margin-bottom:8px;">
        <div style="font-size:13px; color:#555; margin-bottom:4px;">{label}</div>
        <div style="font-size:28px; font-weight:600; color:#1F4E79;">{score}% <span style="font-size:16px; color:#888;">({grade})</span></div>
        <div style="font-size:13px; margin-top:8px;">
            ✅ {summary['addressed']} addressed &nbsp;|&nbsp;
            ⚠️ {summary['partial']} partial &nbsp;|&nbsp;
            ❌ {summary['gap']} gaps
        </div>
    </div>
    """
