# AI Governance Toolkit

**Automated AI governance tooling for multi-framework compliance assessment, intake control, and executive focus.**

This repository is a portfolio collection of Python utilities that operationalize AI governance and cloud security workflows aligned with **ISO/IEC 42001** (AI management systems), **ISO/IEC 27017** (cloud security controls), **ISO/IEC 27018** (cloud PII protection), and related risk-management practices. Each tool targets a distinct stage of the lifecycle—from control gap assessment and tool adoption intake to personal execution planning—so organizations can move from policy on paper to repeatable, auditable automation.

---

## Multi-Framework Compliance Checker

**File:** `checker.py`

### Problem it solves

Manual gap assessments against ISO standards are slow, inconsistent, and hard to scale across many systems. Teams need a fast first pass that surfaces likely control gaps before deeper audit work begins.

### What it demonstrates

Unified compliance assessment across multiple frameworks: the checker evaluates a plain-text system description against a curated control library using keyword-based checks, confidence scoring, four-level maturity ratings, and actionable recommendations. It is intended for triage and education—not certification.

### How to run

```bash
python checker.py --framework iso42001
python checker.py --framework iso27017
python checker.py --framework iso27018
python checker.py --framework all
```

The script runs against a built-in sample system description. Edit `SAMPLE_SYSTEM_DESCRIPTION` in `checker.py` to assess your own environment.

### Supported Frameworks

| Framework | Controls | Domain |
|-----------|----------|--------|
| ISO/IEC 42001:2023 | 20 | AI Governance |
| ISO/IEC 27017:2015 | 24 | Cloud Security |
| ISO/IEC 27018:2019 | 26 | Cloud PII Protection |

Control libraries live in `frameworks/iso42001.py`, `frameworks/iso27017.py`, and `frameworks/iso27018.py`. The original standalone checker remains at `iso42001_checker.py` for reference.

### Roadmap

- **Multi-format evidence input** (PDF, images, Word) — in development
- **Evidence storage integration** (Google Drive, AWS S3) — planned
- **Multi-framework console UI** — planned

See `evidence/README.md` for the planned evidence collection layer.

---

## AI Tool Intake Form

**File:** `ai_intake_form.py`

### Problem it solves

Ad hoc requests to adopt new AI tools create shadow IT, unclear data-handling risk, and weak audit trails. Security and governance teams need a consistent intake path that scores risk and records decisions.

### What it demonstrates

AI tool intake automation: structured adoption requests are scored as **Low**, **Medium**, or **High** risk based on data classification, PII handling, and external API connectivity. Each request yields a formal intake report with a recommended next step (for example, auto-approve or CISO approval required). All reports are appended to a persistent JSON audit log at `intake_log.json`.

### How to run

```bash
python ai_intake_form.py
```

The script processes bundled sample requests and writes results to `intake_log.json` in the project directory. Customize `SAMPLE_REQUESTS` in the file to model your organization's intake scenarios.

---

## Project Structure

```
ai-governance-toolkit/
├── checker.py                  # Unified multi-framework compliance engine
├── iso42001_checker.py         # Original standalone ISO 42001 checker
├── ai_intake_form.py           # AI tool intake and risk scoring
├── frameworks/
│   ├── iso42001.py             # ISO 42001 control library
│   ├── iso27017.py             # ISO 27017 control library
│   └── iso27018.py             # ISO 27018 control library
├── evidence/
│   └── README.md               # Evidence collection layer (planned)
├── requirements.txt
└── README.md
```

---

## Setup

### Install dependencies

```bash
pip install -r requirements.txt
```

The compliance checker uses only the Python standard library today. Additional packages in `requirements.txt` support planned evidence collection and other toolkit scripts.

### Configure your API key (optional)

For scripts that call the Anthropic API, create a `.env` file in the project root (do not commit this file):

```bash
ANTHROPIC_API_KEY=your_key_here
```

Obtain an API key from the [Anthropic Console](https://console.anthropic.com/).

---

## Frameworks & Standards

| Area | Reference |
|------|-----------|
| AI management systems | ISO/IEC 42001 |
| Cloud security controls | ISO/IEC 27017 |
| Cloud PII protection | ISO/IEC 27018 |
| Risk management | NIST AI RMF (conceptual alignment) |
| Intake & audit | Internal governance / third-party risk patterns |

---

**David Yeti** — Compliance & Information Security Engineering   
[davidyeti.com](https://davidyeti.com)
