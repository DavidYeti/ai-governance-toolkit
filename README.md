# AI Governance Toolkit

A collection of Python tools for automating AI governance assessments based on international standards including ISO 42001.

## Project 1 — ISO 42001 Control Checker

Automates the initial gap assessment of an AI system against ISO/IEC 42001 controls — the international standard for AI management systems.

### What It Does
- Defines 9 ISO 42001 controls covering risk treatment, human oversight, internal audit, and corrective action
- Accepts a plain-text description of an AI system
- Checks the description against each control using keyword analysis
- Generates a findings report showing PASS or FAIL for each control
- Produces a compliance score and summary

### Why It Matters
Manual AI governance assessments take compliance engineers hours to complete. This tool automates the initial triage, identifies gaps instantly, and produces a structured findings report — making AI governance scalable across an organization.

### How To Run
python3 iso42001_checker.py

### Frameworks
- ISO/IEC 42001 — AI Management Systems
- NIST AI RMF — AI Risk Management Framework

### Author
David Yeti — Compliance Information Security Engineer  
Securtopia LLC — AI Governance and Compliance Consulting  
davidyeti.com