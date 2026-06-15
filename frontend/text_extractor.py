"""Text extraction from pasted text, uploaded files, and URLs."""

from __future__ import annotations

import re
from io import BytesIO


class TextExtractor:
    """Extract clean text from various input sources."""

    def extract_from_file(self, file_bytes: bytes, filename: str) -> dict:
        """Extract text from PDF, DOCX, or TXT file bytes."""
        try:
            ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
            if ext == "pdf":
                import fitz

                doc = fitz.open(stream=file_bytes, filetype="pdf")
                pages = [page.get_text() for page in doc]
                doc.close()
                raw = "\n".join(pages)
            elif ext == "docx":
                from docx import Document

                doc = Document(BytesIO(file_bytes))
                raw = "\n".join(para.text.strip() for para in doc.paragraphs if para.text.strip())
            elif ext == "txt":
                raw = file_bytes.decode("utf-8", errors="replace")
            else:
                return {
                    "text": "",
                    "source": filename,
                    "word_count": 0,
                    "error": "Unsupported file type. Upload a PDF, Word (.docx), or .txt file.",
                }

            text = self._clean_text(raw)
            return {
                "text": text,
                "source": filename,
                "word_count": len(text.split()) if text else 0,
                "error": None,
            }
        except Exception as e:
            return {
                "text": "",
                "source": filename,
                "word_count": 0,
                "error": f"Could not read file: {e}",
            }

    def extract_from_url(self, url: str) -> dict:
        """Extract text from a publicly accessible URL."""
        if not url.startswith(("http://", "https://")):
            return {
                "text": "",
                "source": url,
                "word_count": 0,
                "error": "URL must start with http:// or https://",
            }

        try:
            import trafilatura

            html = trafilatura.fetch_url(url)
            text = ""
            if html:
                extracted = trafilatura.extract(html, include_tables=True, no_fallback=False)
                if extracted:
                    text = extracted

            if not text:
                import requests
                from bs4 import BeautifulSoup

                response = requests.get(
                    url,
                    timeout=15,
                    headers={"User-Agent": "Mozilla/5.0 (compatible; AIGovernanceToolkit/1.0)"},
                )
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                for tag in soup(["script", "style", "nav", "footer", "header"]):
                    tag.decompose()
                text = soup.get_text(separator=" ", strip=True)

            text = self._clean_text(text)
            word_count = len(text.split()) if text else 0

            if word_count < 50:
                return {
                    "text": "",
                    "source": url,
                    "word_count": word_count,
                    "error": (
                        "Could not extract meaningful text from this URL. "
                        "The page may require JavaScript, a login, or be blocking automated access. "
                        "Copy and paste the page text directly into the text input instead."
                    ),
                }

            return {
                "text": text,
                "source": url,
                "word_count": word_count,
                "error": None,
            }
        except Exception as e:
            return {
                "text": "",
                "source": url,
                "word_count": 0,
                "error": f"Could not fetch URL: {e}",
            }

    def extract_from_text(self, text: str) -> dict:
        """Normalize pasted text input."""
        cleaned = self._clean_text(text)
        return {
            "text": cleaned,
            "source": "Pasted text",
            "word_count": len(cleaned.split()) if cleaned else 0,
            "error": None,
        }

    def _clean_text(self, text: str) -> str:
        """Collapse whitespace and remove control characters."""
        if not text:
            return ""
        text = text.replace("\x00", "")
        text = re.sub(r"[\x01-\x08\x0b\x0c\x0e-\x1f]", "", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()
