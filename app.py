"""AI Governance Toolkit — Streamlit web frontend."""

from __future__ import annotations

from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from frontend.control_matcher import ControlMatcher
from frontend.report_generator import ReportGenerator
from frontend.text_extractor import TextExtractor
from frontend.ui_helpers import (
    framework_label,
    results_to_dataframe,
    score_grade,
    summary_card_html,
)

st.set_page_config(
    page_title="AI Governance Toolkit",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

for key in ["ws_results", "ws_text", "ws_source", "ws_frameworks", "ws_word_count"]:
    if key not in st.session_state:
        st.session_state[key] = None

for fw_key, default in [("fw_42001", True), ("fw_27017", True), ("fw_27018", True)]:
    if fw_key not in st.session_state:
        st.session_state[fw_key] = default


@st.cache_resource
def get_control_matcher() -> ControlMatcher:
    """Load control libraries once per session."""
    return ControlMatcher()


with st.sidebar:
    st.markdown("## 🛡️ AI Governance Toolkit")
    st.caption("Compliance gap assessment — no API key required")
    st.divider()

    st.markdown("### Select frameworks")

    col_a, col_b = st.columns(2)
    if col_a.button("Select All", use_container_width=True):
        st.session_state.fw_42001 = True
        st.session_state.fw_27017 = True
        st.session_state.fw_27018 = True
        st.rerun()
    if col_b.button("Clear All", use_container_width=True):
        st.session_state.fw_42001 = False
        st.session_state.fw_27017 = False
        st.session_state.fw_27018 = False
        st.rerun()

    fw_42001 = st.checkbox("🤖 ISO 42001 — AI Management", key="fw_42001")
    fw_27017 = st.checkbox("☁️ ISO 27017 — Cloud Security", key="fw_27017")
    fw_27018 = st.checkbox("🔒 ISO 27018 — Cloud PII", key="fw_27018")

    selected_frameworks = []
    if fw_42001:
        selected_frameworks.append("iso42001")
    if fw_27017:
        selected_frameworks.append("iso27017")
    if fw_27018:
        selected_frameworks.append("iso27018")

    st.divider()
    st.markdown("### 💻 CLI quick reference")
    st.code(
        "python checker.py --framework iso42001\n"
        "python checker.py --framework iso27017\n"
        "python checker.py --framework iso27018\n"
        "python checker.py --framework all",
        language="bash",
    )

    st.divider()
    with st.expander("About this tool"):
        st.markdown(
            "AI Governance Toolkit evaluates your policy documents against major AI and cloud governance frameworks.\n\n"
            "**No data is stored or sent externally.** Analysis runs entirely in your browser session.\n\n"
            "[GitHub →](https://github.com/DavidYeti/ai-governance-toolkit)"
        )

tab_analyze, tab_results, tab_howto = st.tabs(["📥  Analyze", "📊  Results", "ℹ️  How to Use"])

with tab_analyze:
    st.header("Check your governance document")
    st.markdown(
        "Upload, paste, or link to a policy document. We extract the text and score it "
        "against your selected frameworks — rule-based, offline, no API keys needed."
    )

    if not selected_frameworks:
        st.warning("⚠️ Select at least one framework in the sidebar before running.")

    st.divider()

    input_method = st.radio(
        "How would you like to provide your document?",
        ["📝  Paste text", "📁  Upload a file", "🔗  Enter a URL"],
        horizontal=True,
        label_visibility="collapsed",
    )

    extracted_text = ""
    input_source = ""
    input_ready = False

    if "Paste" in input_method:
        pasted = st.text_area(
            "Paste your document text here",
            height=320,
            placeholder=(
                "Paste your AI policy, governance framework, risk assessment, "
                "data handling procedures, or any compliance-relevant text here..."
            ),
        )
        if pasted.strip():
            word_count = len(pasted.split())
            st.caption(f"📄 {word_count:,} words detected")
            if word_count < 50:
                st.warning(
                    "The text is very short. Results will be limited — try pasting a fuller document."
                )
            extracted_text = pasted
            input_source = "Pasted text"
            input_ready = word_count >= 20

    elif "Upload" in input_method:
        uploaded = st.file_uploader(
            "Upload your document",
            type=["pdf", "docx", "txt"],
            help="Supports PDF, Word (.docx), and plain text. Recommended max: 50MB.",
        )
        if uploaded:
            extractor = TextExtractor()
            with st.spinner(f"Reading {uploaded.name}..."):
                result = extractor.extract_from_file(uploaded.read(), uploaded.name)
            if result["error"]:
                st.error(f"❌ {result['error']}")
            else:
                st.success(f"✅ {uploaded.name} — {result['word_count']:,} words extracted")
                extracted_text = result["text"]
                input_source = result["source"]
                input_ready = result["word_count"] >= 20

    elif "URL" in input_method:
        url = st.text_input(
            "Enter a URL",
            placeholder="https://example.com/ai-governance-policy",
            help="Must be a publicly accessible page. No login-required pages.",
        )
        st.caption(
            "⚠️ Pages requiring JavaScript or a login may not extract correctly. "
            "Use Paste text as a fallback."
        )
        if url.strip():
            if not url.startswith(("http://", "https://")):
                st.error("URL must start with http:// or https://")
            else:
                extractor = TextExtractor()
                with st.spinner("Fetching and extracting text from URL..."):
                    result = extractor.extract_from_url(url.strip())
                if result["error"]:
                    st.error(f"❌ {result['error']}")
                else:
                    st.success(f"✅ {result['word_count']:,} words extracted from {url}")
                    extracted_text = result["text"]
                    input_source = result["source"]
                    input_ready = result["word_count"] >= 20

    st.divider()

    run_disabled = not input_ready or not selected_frameworks
    run_btn = st.button(
        "▶  Run Analysis",
        type="primary",
        disabled=run_disabled,
        use_container_width=False,
    )

    if run_btn and extracted_text and selected_frameworks:
        matcher = get_control_matcher()
        progress = st.progress(0, text="Analyzing...")
        results = {}
        for i, fw in enumerate(selected_frameworks):
            progress.progress((i / len(selected_frameworks)), text=f"Checking {fw}...")
            fw_result = matcher.analyze(extracted_text, fw)
            addressed = sum(1 for r in fw_result if r["status"] == "ADDRESSED")
            partial = sum(1 for r in fw_result if r["status"] == "PARTIAL")
            gap = sum(1 for r in fw_result if r["status"] == "GAP")
            total = len(fw_result)
            score_pct = round((addressed + partial * 0.5) / max(total, 1) * 100, 1)
            results[fw] = {
                "controls": fw_result,
                "summary": {
                    "addressed": addressed,
                    "partial": partial,
                    "gap": gap,
                    "total": total,
                    "score_pct": score_pct,
                },
            }
        progress.progress(1.0, text="Complete")
        progress.empty()
        st.session_state["ws_results"] = results
        st.session_state["ws_text"] = extracted_text
        st.session_state["ws_source"] = input_source
        st.session_state["ws_frameworks"] = selected_frameworks
        st.session_state["ws_word_count"] = len(extracted_text.split())
        st.success("✅ Analysis complete — click the **📊 Results** tab to view your report.")

with tab_results:
    results = st.session_state.get("ws_results")
    if not results:
        st.info("👈 Go to the **Analyze** tab to run a compliance check first.")
        st.stop()

    source = st.session_state.get("ws_source", "")
    frameworks = st.session_state.get("ws_frameworks", [])
    word_count = st.session_state.get("ws_word_count") or 0

    st.header("Compliance Assessment Results")
    st.caption(
        f"Source: {source} · {word_count:,} words analyzed · {len(frameworks)} framework(s)"
    )

    cols = st.columns(len(frameworks))
    for i, fw in enumerate(frameworks):
        summary = results[fw]["summary"]
        with cols[i]:
            st.markdown(summary_card_html(fw, summary), unsafe_allow_html=True)

    st.divider()

    report_gen = ReportGenerator()
    dl_col1, dl_col2, _ = st.columns([1, 1, 4])
    date_str = datetime.now().strftime("%Y%m%d")
    with dl_col1:
        pdf_bytes = report_gen.generate_pdf(results, frameworks, source)
        st.download_button(
            "📥 Download PDF",
            data=pdf_bytes,
            file_name=f"compliance_report_{date_str}.pdf",
            mime="application/pdf",
            type="primary",
        )
    with dl_col2:
        docx_bytes = report_gen.generate_docx(results, frameworks, source)
        st.download_button(
            "📄 Download Word Doc",
            data=docx_bytes,
            file_name=f"compliance_report_{date_str}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    st.divider()

    tab_labels = [framework_label(fw) for fw in frameworks]
    if len(frameworks) > 1:
        tab_labels.append("⚖️  Comparison")

    result_tabs = st.tabs(tab_labels)

    for i, fw in enumerate(frameworks):
        with result_tabs[i]:
            controls = results[fw]["controls"]
            summary = results[fw]["summary"]

            m1, m2, m3 = st.columns(3)
            m1.metric("✅ Addressed", summary["addressed"])
            m2.metric("⚠️ Partial", summary["partial"])
            m3.metric("❌ Gaps", summary["gap"])

            status_filter = st.multiselect(
                "Filter by status",
                ["ADDRESSED", "PARTIAL", "GAP"],
                default=["ADDRESSED", "PARTIAL", "GAP"],
                key=f"filter_{fw}",
            )
            filtered = [c for c in controls if c["status"] in status_filter]

            df = results_to_dataframe(filtered)
            st.dataframe(df, use_container_width=True, hide_index=True)

            controls_with_evidence = [c for c in filtered if c["evidence_snippets"]]
            if controls_with_evidence:
                with st.expander(
                    f"📋 Evidence highlights ({len(controls_with_evidence)} controls)"
                ):
                    for c in controls_with_evidence[:10]:
                        st.markdown(f"**{c['control_id']} — {c['control_name']}**")
                        for snippet in c["evidence_snippets"][:2]:
                            st.markdown(f"> {snippet.strip()}")
                        st.divider()

    if len(frameworks) > 1:
        with result_tabs[-1]:
            st.subheader("Framework comparison")
            st.caption(
                "Side-by-side view of how your document performs across all selected frameworks."
            )

            comp_rows = []
            for fw in frameworks:
                s = results[fw]["summary"]
                comp_rows.append({
                    "Framework": framework_label(fw),
                    "Total Controls": s["total"],
                    "✅ Addressed": s["addressed"],
                    "⚠️ Partial": s["partial"],
                    "❌ Gaps": s["gap"],
                    "Score": f"{s['score_pct']}%",
                    "Grade": score_grade(s["score_pct"]),
                })
            st.dataframe(pd.DataFrame(comp_rows), use_container_width=True, hide_index=True)

            fig = go.Figure()
            fw_labels = [framework_label(fw) for fw in frameworks]
            fig.add_trace(
                go.Bar(
                    name="Addressed",
                    x=fw_labels,
                    y=[results[fw]["summary"]["addressed"] for fw in frameworks],
                    marker_color="#2d7a2d",
                )
            )
            fig.add_trace(
                go.Bar(
                    name="Partial",
                    x=fw_labels,
                    y=[results[fw]["summary"]["partial"] for fw in frameworks],
                    marker_color="#b87333",
                )
            )
            fig.add_trace(
                go.Bar(
                    name="Gap",
                    x=fw_labels,
                    y=[results[fw]["summary"]["gap"] for fw in frameworks],
                    marker_color="#cc3300",
                )
            )
            fig.update_layout(
                barmode="stack",
                title="Control coverage by framework",
                height=350,
                margin=dict(t=40, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
            )
            st.plotly_chart(fig, use_container_width=True)

            st.caption(
                "💡 LLM-powered cross-framework control mapping and overlap analysis "
                "will be added in Phase 3."
            )

with tab_howto:
    st.header("How to use this tool")

    st.markdown("""
## Using the web interface

### Step 1 — Select frameworks
In the left sidebar, check the frameworks you want to assess against:
- **ISO 42001** — AI Management System (20 controls for responsible AI development and governance)
- **ISO 27017** — Cloud Security Controls (controls for cloud service providers and customers)
- **ISO 27018** — Cloud PII Protection (controls for protecting personal data in public cloud environments)

You can select one, two, or all three. When multiple frameworks are selected, a **Comparison** tab appears in your results.

### Step 2 — Provide your document
Choose one of three input methods:

**📝 Paste text** — Copy and paste your AI policy, data handling procedures, security controls documentation, or any governance text. Best for quick checks.

**📁 Upload a file** — Upload a PDF, Word document (.docx), or plain text file. The tool extracts the text automatically. Supports files up to 50MB (recommend under 10MB for best performance).

**🔗 Enter a URL** — Paste the URL of a publicly accessible policy page or governance document. Works well for most static pages. Pages that require login or heavy JavaScript may not extract correctly — if that happens, copy and paste the text directly.

### Step 3 — Run the analysis
Click **Run Analysis**. The tool scans your document for evidence of each control using keyword matching. No data leaves your browser session.

### Step 4 — Review your results
The Results tab shows:
- A score card per framework (percentage of controls evidenced)
- A filterable table of every control with status, maturity level, and confidence score
- Evidence highlights — the actual sentences from your document that matched each control
- A comparison chart if you selected multiple frameworks

### Step 5 — Download your report
Click **Download PDF** or **Download Word Doc** to save a formatted compliance assessment report to your workstation.

---

## Understanding your scores

| Status | Maturity | What it means |
|--------|----------|---------------|
| ✅ ADDRESSED | Defined | Strong keyword evidence across multiple areas of this control |
| ✅ ADDRESSED | Developing | Moderate evidence — the control is partially covered |
| ⚠️ PARTIAL | Initial | Minimal evidence — the topic is mentioned but not well documented |
| ❌ GAP | Not Implemented | No evidence found for this control |

**Confidence score** reflects what percentage of expected control-relevant keywords appeared in your document. Higher is better, but the tool rewards depth of coverage, not length.

> **Important**: This tool identifies evidence of compliance documentation — it does not certify compliance with any standard. Use results to guide your gap remediation work, not as a formal audit output.

---

## Running via command line

The CLI tools are unchanged and still fully functional:

```bash
# Activate your virtual environment first
source venv/bin/activate

# Single framework
python checker.py --framework iso42001
python checker.py --framework iso27017
python checker.py --framework iso27018

# All frameworks — combined summary
python checker.py --framework all

# AI Tool Intake Form (risk scoring)
python ai_intake_form.py
```

---

## Tips for better results

- **Longer documents produce more accurate scores** — a one-page policy will score lower than a full governance framework document, even if both cover the same topics
- **Include multiple document types** — risk assessments, data handling procedures, security policies, and AI governance frameworks all address different control areas
- **Use the comparison view** to see which frameworks your existing documentation covers best
- **Evidence highlights** show you which specific passages in your document triggered each control match — useful for identifying what to expand or clarify

---

## About this tool

Built by David Yeti · [github.com/DavidYeti/ai-governance-toolkit](https://github.com/DavidYeti/ai-governance-toolkit)

No data is stored, logged, or transmitted externally. All analysis runs within your browser session. Session data is cleared when you close the tab.
    """)
