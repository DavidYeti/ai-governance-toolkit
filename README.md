# AI Governance Toolkit

**Automated AI governance tooling for compliance assessment, intake control, and executive focus.**

This repository is a portfolio collection of Python utilities that operationalize AI governance workflows aligned with **ISO/IEC 42001** (AI management systems) and related risk-management practices. Each tool targets a distinct stage of the AI lifecycle—from control gap assessment and tool adoption intake to personal execution planning—so organizations (and practitioners) can move from policy on paper to repeatable, auditable automation.

---

## ISO 42001 Control Checker

**File:** `iso42001_checker.py`

### Problem it solves

Manual gap assessments against ISO 42001 controls are slow, inconsistent, and hard to scale across many AI systems. Teams need a fast first pass that surfaces likely control gaps before deeper audit work begins.

### What it demonstrates

Automated gap assessment for AI governance: the script evaluates a plain-text AI system description against a curated set of ISO 42001–inspired controls using keyword-based checks, then produces a structured findings report with **PASS/FAIL** per control and an overall **compliance percentage score**. It is intended for triage and education—not certification.

### How to run

```bash
python3 iso42001_checker.py
```

The script runs against a built-in sample system description. Edit `SAMPLE_AI_SYSTEM_DESCRIPTION` in the file to assess your own system.

---

## AI Tool Intake Form

**File:** `ai_intake_form.py`

### Problem it solves

Ad hoc requests to adopt new AI tools create shadow IT, unclear data-handling risk, and weak audit trails. Security and governance teams need a consistent intake path that scores risk and records decisions.

### What it demonstrates

AI tool intake automation: structured adoption requests are scored as **Low**, **Medium**, or **High** risk based on data classification, PII handling, and external API connectivity. Each request yields a formal intake report with a recommended next step (for example, auto-approve or CISO approval required). All reports are appended to a persistent JSON audit log at `intake_log.json`.

### How to run

```bash
python3 ai_intake_form.py
```

The script processes bundled sample requests and writes results to `intake_log.json` in the project directory. Customize `SAMPLE_REQUESTS` in the file to model your organization’s intake scenarios.

---

## Morning Standup Assistant

**File:** `morning_standup.py`

### Problem it solves

Weekly plans and long-term priorities are easy to lose in a crowded calendar. A daily briefing should connect “what’s on the schedule” with “what actually matters”—without manual synthesis every morning.

### What it demonstrates

Claude-powered executive briefing: the assistant reads your weekly schedule and priorities, combines them with full life and career architecture context, and calls the **Anthropic Claude API** to generate a concise, personalized daily briefing that highlights what matters today and why.

### How to run

1. Complete [Setup](#setup) (API key and dependencies).
2. Edit `WEEKLY_SCHEDULE`, `WEEKLY_PRIORITIES`, and related context blocks at the top of `morning_standup.py`.
3. Run:

```bash
python3 morning_standup.py
```

---

## Setup

### Install dependencies

`morning_standup.py` requires the Anthropic SDK and `python-dotenv`. Install them with:

```bash
pip3 install anthropic python-dotenv
```

The other two scripts use only the Python standard library.

### Configure your API key

Create a `.env` file in the project root (do not commit this file):

```bash
ANTHROPIC_API_KEY=your_key_here
```

`morning_standup.py` loads this file automatically via `python-dotenv`. You may alternatively set `ANTHROPIC_API_KEY` in your shell environment or paste a key into `ANTHROPIC_API_KEY` at the top of `morning_standup.py` (environment variable is preferred for security).

Obtain an API key from the [Anthropic Console](https://console.anthropic.com/).

---

## Frameworks & standards

| Area | Reference |
|------|-----------|
| AI management systems | ISO/IEC 42001 |
| Risk management | NIST AI RMF (conceptual alignment) |
| Intake & audit | Internal governance / third-party risk patterns |

---

**David Yeti** — Compliance & Information Security Engineering  
Securtopia LLC — AI Governance and Compliance Consulting  
[davidyeti.com](https://davidyeti.com)
