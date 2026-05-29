# Evidence Collection — Layer 2

This directory is reserved for the evidence collection automation layer.

## Current Status
Layer 1 (text input keyword matching) is complete and live.
Layer 2 (multi-format evidence input) is in development.

## Planned Capabilities
- PDF evidence extraction using PyPDF2
- Screenshot and image text extraction using pytesseract  
- Word document parsing using python-docx
- Automatic URL evidence collection for cloud documentation
- Evidence storage routing to Google Drive or AWS S3

## Usage (Coming Soon)
python checker.py --framework iso27017 --evidence ./evidence/client_docs/
