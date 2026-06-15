# AI Governance Toolkit — Deployment Guide

## Streamlit Community Cloud (recommended — free, no setup)

1. Push all new files to the `main` branch of [github.com/DavidYeti/ai-governance-toolkit](https://github.com/DavidYeti/ai-governance-toolkit)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account (DavidYeti)
4. Click **New app**
5. Repository: `DavidYeti/ai-governance-toolkit`
6. Branch: `main`
7. Main file path: `app.py`
8. Click **Deploy**

Your app will be live at: `https://ai-governance-toolkit.streamlit.app` (Streamlit assigns the subdomain — you can customize it in app settings).

**Auto-deploy:** Every push to `main` triggers an automatic redeploy. No manual steps needed after initial setup.

**Sharing:** Send anyone the Streamlit Cloud URL. They click it, the app opens instantly in their browser. No installation required.

---

## Local development

```bash
git clone https://github.com/DavidYeti/ai-governance-toolkit
cd ai-governance-toolkit
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
# Opens at http://localhost:8501
```

---

## CLI (unchanged — always works independently)

```bash
python checker.py --framework iso42001
python checker.py --framework all
python ai_intake_form.py
```

---

## Project structure (new files)

```
ai-governance-toolkit/
├── app.py                        # Streamlit entry point
├── frontend/
│   ├── text_extractor.py         # PDF / DOCX / URL / text extraction
│   ├── control_matcher.py        # Rule-based text → control scoring
│   ├── report_generator.py       # PDF + Word export
│   └── ui_helpers.py             # Reusable display functions
├── data/
│   ├── iso_42001_controls.json   # 20 ISO 42001 controls
│   ├── iso_27017_controls.json   # 24 ISO 27017 controls
│   └── iso_27018_controls.json   # 26 ISO 27018 controls
├── .streamlit/
│   └── config.toml               # Theme and layout settings
├── packages.txt                  # System deps for Streamlit Cloud
└── DEPLOY.md                     # This file
```

---

## Technical notes

- **No API keys required.** All analysis is rule-based keyword matching — works fully offline.
- **No data persistence.** Results live in `st.session_state` only.
- **Existing CLI files are unchanged.** `checker.py`, `iso42001_checker.py`, and `ai_intake_form.py` work exactly as before.
- Control data is sourced from `data/*_controls.json`, generated from the `frameworks/` Python modules.
