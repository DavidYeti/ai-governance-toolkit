"""Rule-based text-to-control scoring via keyword matching."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

STOPWORDS = {
    "this", "that", "with", "from", "have", "will", "should", "must", "each",
    "such", "also", "when", "where", "which", "been", "their", "there", "these",
    "those", "does", "into", "more", "some", "than", "then", "they", "them",
    "what", "your", "used", "make", "using", "ensure", "provide", "include",
    "within", "across", "about", "between",
}

SYNONYMS = {
    "risk": ["risk", "threat", "vulnerability", "hazard", "exposure", "likelihood"],
    "policy": ["policy", "procedure", "guideline", "standard", "framework", "directive"],
    "security": ["security", "protection", "safeguard", "control", "measure", "defence"],
    "data": ["data", "information", "record", "dataset", "content", "asset"],
    "privacy": ["privacy", "confidential", "sensitive", "personal", "private", "pii"],
    "cloud": ["cloud", "hosted", "saas", "iaas", "paas", "provider", "service"],
    "consent": ["consent", "permission", "authorization", "opt-in", "opt-out", "agreement"],
    "audit": ["audit", "review", "assessment", "evaluation", "inspection", "verification"],
    "incident": ["incident", "breach", "event", "alert", "violation", "compromise"],
    "access": ["access", "authentication", "authorization", "permission", "credential", "identity"],
    "training": ["training", "awareness", "education", "competence", "learning", "skill"],
    "monitoring": ["monitoring", "logging", "surveillance", "detection", "oversight", "tracking"],
    "governance": ["governance", "management", "oversight", "accountability", "responsibility"],
    "transparency": ["transparency", "disclosure", "explainability", "interpretability", "openness"],
}

FRAMEWORK_FILE_MAP = {
    "iso42001": "iso_42001",
    "iso27017": "iso_27017",
    "iso27018": "iso_27018",
}

TEXT_FIELDS = (
    "description",
    "evidence_required",
    "control_name",
    "name",
    "title",
    "remediation",
    "guidance",
    "recommendations",
)


class ControlMatcher:
    """Score document text against ISO control libraries using keyword matching."""

    def __init__(self) -> None:
        self.controls: dict[str, list[dict]] = {
            "iso42001": [],
            "iso27017": [],
            "iso27018": [],
        }
        self.keyword_index: dict[str, dict[str, list[str]]] = {
            "iso42001": {},
            "iso27017": {},
            "iso27018": {},
        }
        self._load_controls()

    def _load_controls(self) -> None:
        """Load control JSON files from known search paths."""
        base = Path(__file__).resolve().parent.parent
        search_roots = [base, base / "data", base / "data" / "controls", base / "controls"]

        for fw_key, file_stem in FRAMEWORK_FILE_MAP.items():
            filename = f"{file_stem}_controls.json"
            found_path = None
            for root in search_roots:
                candidate = root / filename
                if candidate.is_file():
                    found_path = candidate
                    break

            if found_path is None:
                logger.warning("Control file not found for %s: %s", fw_key, filename)
                continue

            try:
                with open(found_path, encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    controls = [
                        {"control_id": cid, **ctrl}
                        for cid, ctrl in data.items()
                    ]
                else:
                    controls = data
                self.controls[fw_key] = controls
                self.keyword_index[fw_key] = self._build_keyword_index(controls)
                logger.info("Loaded %d controls for %s from %s", len(controls), fw_key, found_path)
            except Exception as e:
                logger.warning("Failed to load controls for %s: %s", fw_key, e)

    def _build_keyword_index(self, controls: list[dict]) -> dict[str, list[str]]:
        """Build deduplicated keyword lists per control from text fields."""
        index: dict[str, list[str]] = {}

        for control in controls:
            control_id = (
                control.get("control_id")
                or control.get("id")
                or "Unknown"
            )

            parts: list[str] = []

            existing_keywords = control.get("keywords", [])
            if isinstance(existing_keywords, list):
                parts.extend(str(kw) for kw in existing_keywords)

            for field in TEXT_FIELDS:
                value = control.get(field)
                if isinstance(value, str):
                    parts.append(value)
                elif isinstance(value, list):
                    parts.extend(str(v) for v in value)

            combined = " ".join(parts).lower()
            tokens = re.split(r"[^a-z0-9]+", combined)
            keywords: set[str] = set()

            for token in tokens:
                if len(token) >= 4 and token not in STOPWORDS:
                    keywords.add(token)
                    for key, synonyms in SYNONYMS.items():
                        if token == key or token in synonyms:
                            keywords.update(synonyms)

            index[control_id] = sorted(keywords)

        return index

    def score_text_against_control(
        self, text_original: str, text_lower: str, keywords: list[str]
    ) -> tuple[int, list[str]]:
        """Return hit count and evidence snippets for a control."""
        hits: set[str] = set()
        snippets: list[str] = []
        sentences = re.split(r"(?<=[.!?])\s+", text_original)

        for keyword in keywords:
            pattern = r"\b" + re.escape(keyword) + r"\b"
            if not re.search(pattern, text_lower):
                continue
            hits.add(keyword)

            for sentence in sentences:
                word_count = len(sentence.split())
                if word_count < 8 or word_count > 250:
                    continue
                if re.search(pattern, sentence, re.IGNORECASE):
                    snippet = sentence.strip()
                    if snippet and snippet not in snippets:
                        snippets.append(snippet)
                    if len(snippets) >= 5:
                        break
            if len(snippets) >= 5:
                break

        return len(hits), snippets[:5]

    def _score_to_maturity(self, hit_count: int, keyword_total: int) -> str:
        ratio = hit_count / max(keyword_total, 1)
        if ratio == 0:
            return "Not Implemented"
        if ratio <= 0.20:
            return "Initial"
        if ratio <= 0.50:
            return "Developing"
        return "Defined"

    def _maturity_to_status(self, maturity: str) -> str:
        return {
            "Defined": "ADDRESSED",
            "Developing": "ADDRESSED",
            "Initial": "PARTIAL",
            "Not Implemented": "GAP",
        }.get(maturity, "GAP")

    def analyze(self, text: str, framework: str) -> list[dict]:
        """Analyze text against all controls in a framework."""
        text_lower = text.lower()
        results = []

        for control in self.controls.get(framework, []):
            control_id = control.get("control_id") or control.get("id") or "Unknown"
            control_name = (
                control.get("control_name")
                or control.get("name")
                or control.get("title")
                or ""
            )
            description = control.get("description") or ""
            keywords = self.keyword_index.get(framework, {}).get(control_id, [])
            hit_count, snippets = self.score_text_against_control(text, text_lower, keywords)
            maturity = self._score_to_maturity(hit_count, len(keywords))
            status = self._maturity_to_status(maturity)
            confidence = round(hit_count / max(len(keywords), 1), 2)

            results.append({
                "control_id": control_id,
                "control_name": control_name,
                "description": description,
                "maturity": maturity,
                "status": status,
                "hit_count": hit_count,
                "keyword_total": len(keywords),
                "confidence_score": confidence,
                "evidence_snippets": snippets,
            })

        return sorted(results, key=lambda x: x["control_id"])

    def compare_frameworks(self, text: str, frameworks: list[str]) -> dict:
        """Analyze text across multiple frameworks and return summary stats."""
        output = {}
        for fw in frameworks:
            results = self.analyze(text, fw)
            addressed = sum(1 for r in results if r["status"] == "ADDRESSED")
            partial = sum(1 for r in results if r["status"] == "PARTIAL")
            gap = sum(1 for r in results if r["status"] == "GAP")
            total = len(results)
            score_pct = round((addressed + partial * 0.5) / max(total, 1) * 100, 1)
            output[fw] = {
                "controls": results,
                "summary": {
                    "addressed": addressed,
                    "partial": partial,
                    "gap": gap,
                    "total": total,
                    "score_pct": score_pct,
                },
            }
        return output
