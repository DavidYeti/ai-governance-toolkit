"""ISO/IEC 42001:2023 control library for the unified compliance checker."""

from __future__ import annotations

FRAMEWORK_METADATA = {
    "name": "ISO/IEC 42001:2023",
    "description": (
        "AI Management System standard covering governance, risk, "
        "and responsible AI practices"
    ),
    "total_controls": 20,
    "domain": "AI Governance",
}

MATURITY_DOES_NOT_EXIST = "Does Not Exist"
MATURITY_PARTIALLY_IMPLEMENTED = "Partially Implemented"
MATURITY_LARGELY_IMPLEMENTED = "Largely Implemented"
MATURITY_FULLY_IMPLEMENTED = "Fully Implemented"

MATURITY_LEVEL_DESCRIPTIONS: dict[str, str] = {
    MATURITY_DOES_NOT_EXIST: (
        "No evidence found that this control requirement is addressed in the "
        "system description or documentation. Immediate remediation is required "
        "before this control can be considered for compliance."
    ),
    MATURITY_PARTIALLY_IMPLEMENTED: (
        "Some evidence exists that this control area is being addressed but "
        "coverage is insufficient to satisfy the full control requirement. "
        "Targeted remediation is needed to close the identified gaps."
    ),
    MATURITY_LARGELY_IMPLEMENTED: (
        "Most control requirements are addressed with evidence present for the "
        "majority of expected criteria. Minor gaps remain and specific evidence "
        "collection is needed to achieve full implementation."
    ),
    MATURITY_FULLY_IMPLEMENTED: (
        "Strong evidence exists across all or nearly all control criteria "
        "indicating this requirement is well addressed. Maintain current practices "
        "and verify evidence remains current during periodic reviews."
    ),
}

ISO_42001_CONTROLS: dict[str, dict[str, object]] = {
    "ISO-42001-A.2.2": {
        "name": "Stakeholder needs and AI expectations",
        "description": (
            "The organization shall determine the needs and expectations of "
            "interested parties relevant to its AI management system"
        ),
        "keywords": [
            "stakeholder",
            "interested party",
            "expectation",
            "requirement",
            "customer",
            "regulatory",
        ],
        "recommendations": [
            "Document a stakeholder register identifying all interested parties affected by AI systems including customers regulators and employees.",
            "Conduct periodic stakeholder needs assessments and update AI governance policies accordingly.",
            "Establish a formal feedback mechanism for stakeholders to raise AI-related concerns.",
        ],
    },
    "ISO-42001-A.4.1": {
        "name": "Organizational context for AI",
        "description": (
            "The organization shall determine external and internal issues "
            "relevant to its purpose that affect its ability to achieve intended "
            "outcomes of the AI management system"
        ),
        "keywords": [
            "context",
            "organizational",
            "internal",
            "external",
            "environment",
            "objective",
        ],
        "recommendations": [
            "Conduct and document an organizational context analysis covering internal capabilities and external regulatory requirements affecting AI.",
            "Maintain a risk register that captures environmental factors influencing AI system design and deployment.",
            "Review context analysis at least annually or when significant changes occur.",
        ],
    },
    "ISO-42001-A.5.1": {
        "name": "Leadership and AI commitment",
        "description": (
            "Top management shall demonstrate leadership and commitment with "
            "respect to the AI management system"
        ),
        "keywords": [
            "leadership",
            "management",
            "commitment",
            "executive",
            "board",
            "sponsor",
        ],
        "recommendations": [
            "Obtain and document executive sponsorship for the AI management system with named accountability at the leadership level.",
            "Include AI governance in board-level reporting and strategic planning cycles.",
            "Ensure leadership allocates sufficient resources and authority to the AI governance function.",
        ],
    },
    "ISO-42001-A.5.2": {
        "name": "AI policy",
        "description": (
            "Top management shall establish an AI policy that is appropriate to "
            "the purpose of the organization and provides a framework for setting "
            "AI objectives"
        ),
        "keywords": [
            "policy",
            "principle",
            "commitment",
            "framework",
            "objective",
            "guideline",
        ],
        "recommendations": [
            "Draft and approve a formal AI policy signed by executive leadership covering responsible use safety security and ethics.",
            "Communicate the AI policy to all relevant personnel and make it accessible to external stakeholders where appropriate.",
            "Review and update the AI policy at least annually.",
        ],
    },
    "ISO-42001-A.6.1": {
        "name": "AI risk treatment and lifecycle",
        "description": (
            "The organization shall determine risks related to its AI systems "
            "and plan how they are addressed through the lifecycle"
        ),
        "keywords": [
            "risk",
            "lifecycle",
            "mitigation",
            "treatment",
            "impact",
            "assessment",
        ],
        "recommendations": [
            "Develop a formal AI risk assessment methodology covering the full system lifecycle from design through decommission.",
            "Document risk treatment plans for each identified AI risk with assigned owners and target resolution dates.",
            "Integrate AI risk reviews into existing enterprise risk management processes.",
        ],
    },
    "ISO-42001-A.6.2": {
        "name": "Roles responsibilities and authorities",
        "description": (
            "Responsibilities for the AI management system shall be assigned "
            "and communicated"
        ),
        "keywords": [
            "responsib",
            "role",
            "owner",
            "accountable",
            "governance",
            "authority",
        ],
        "recommendations": [
            "Define and document roles and responsibilities for AI governance including an AI system owner for each deployed system.",
            "Establish an AI governance committee or oversight body with clear decision-making authority.",
            "Communicate role assignments to all affected personnel through documented organizational charts or RACI matrices.",
        ],
    },
    "ISO-42001-A.6.3": {
        "name": "AI system impact assessment",
        "description": (
            "The organization shall conduct an impact assessment for AI systems "
            "considering potential harms to individuals and society"
        ),
        "keywords": [
            "impact",
            "harm",
            "assessment",
            "bias",
            "fairness",
            "discrimination",
            "consequence",
        ],
        "recommendations": [
            "Conduct documented impact assessments for each AI system evaluating potential harms to individuals groups and society before deployment.",
            "Include bias fairness and discrimination analysis in all AI system impact assessments.",
            "Establish a threshold above which a formal third-party impact assessment is required.",
        ],
    },
    "ISO-42001-A.7.1": {
        "name": "Competence and awareness",
        "description": (
            "People affecting AI performance shall be competent on the basis of "
            "education training or experience and awareness shall be promoted"
        ),
        "keywords": [
            "training",
            "competence",
            "awareness",
            "education",
            "skill",
            "certification",
        ],
        "recommendations": [
            "Develop a competency framework for all roles involved in AI system design development and operation.",
            "Deliver and document mandatory AI awareness training for all personnel interacting with AI systems.",
            "Track training completion and establish a minimum refresh cycle of annually.",
        ],
    },
    "ISO-42001-A.7.2": {
        "name": "Documented information",
        "description": (
            "The AI management system shall include documented information "
            "needed for effectiveness"
        ),
        "keywords": [
            "document",
            "policy",
            "procedure",
            "record",
            "specification",
            "log",
        ],
        "recommendations": [
            "Establish a document control process for all AI governance artifacts including policies procedures risk assessments and audit reports.",
            "Maintain version-controlled records of AI system configurations model versions and change histories.",
            "Define retention periods and access controls for all AI governance documentation.",
        ],
    },
    "ISO-42001-A.8.1": {
        "name": "Operational planning and control",
        "description": (
            "AI processes shall be carried out under controlled conditions using "
            "established criteria"
        ),
        "keywords": [
            "operational",
            "control",
            "process",
            "monitor",
            "criteria",
            "procedure",
        ],
        "recommendations": [
            "Document operational procedures for all AI system processes including data ingestion model inference and output handling.",
            "Implement monitoring and alerting for AI system performance against defined operational criteria.",
            "Establish incident response procedures specific to AI system failures or unexpected behaviors.",
        ],
    },
    "ISO-42001-A.8.2": {
        "name": "Human oversight",
        "description": (
            "Appropriate human oversight shall be applied to AI systems especially "
            "for high-impact contexts"
        ),
        "keywords": [
            "human",
            "oversight",
            "review",
            "supervise",
            "intervention",
            "approval",
        ],
        "recommendations": [
            "Define and document the human oversight requirements for each AI system including when human review is mandatory before action is taken.",
            "Implement technical controls that require human approval for high-risk AI-generated outputs or decisions.",
            "Maintain logs of human oversight interventions and their outcomes for audit purposes.",
        ],
    },
    "ISO-42001-A.8.3": {
        "name": "Data governance for AI",
        "description": (
            "The organization shall ensure that data used in AI systems is managed "
            "appropriately with regard to quality relevance and privacy"
        ),
        "keywords": [
            "data",
            "quality",
            "privacy",
            "governance",
            "dataset",
            "training data",
            "sensitive",
        ],
        "recommendations": [
            "Document a data governance policy covering data quality privacy and appropriate use for all AI training and inference data.",
            "Implement data classification controls that restrict sensitive data from being used in AI systems without appropriate safeguards.",
            "Establish data retention and deletion procedures aligned with privacy regulations for all AI-related data.",
        ],
    },
    "ISO-42001-A.8.4": {
        "name": "AI supply chain and third-party risk",
        "description": (
            "The organization shall manage risks associated with third-party AI "
            "components suppliers and services"
        ),
        "keywords": [
            "supply chain",
            "third-party",
            "vendor",
            "supplier",
            "model",
            "open source",
            "dependency",
        ],
        "recommendations": [
            "Maintain an inventory of all third-party AI components models and services used across the organization.",
            "Conduct security and governance assessments of AI vendors and suppliers before procurement and annually thereafter.",
            "Include AI supply chain security requirements in all third-party contracts and service agreements.",
        ],
    },
    "ISO-42001-A.8.5": {
        "name": "Responsible development and deployment",
        "description": (
            "The organization shall ensure that AI systems are developed and "
            "deployed responsibly with consideration for safety security and "
            "ethical implications"
        ),
        "keywords": [
            "responsible",
            "ethical",
            "safe",
            "secure",
            "deploy",
            "development",
            "guardrail",
        ],
        "recommendations": [
            "Establish a responsible AI development framework covering ethical review safety testing and security validation before deployment.",
            "Implement pre-deployment testing procedures that verify AI system behavior against defined safety and security requirements.",
            "Document and communicate responsible AI principles to all development teams with accountability for compliance.",
        ],
    },
    "ISO-42001-A.8.6": {
        "name": "Adversarial robustness and threat protection",
        "description": (
            "The organization shall identify and address threats specific to AI "
            "systems including adversarial attacks prompt injection and model "
            "manipulation"
        ),
        "keywords": [
            "adversarial",
            "prompt injection",
            "attack",
            "threat",
            "robustness",
            "red team",
            "manipulation",
        ],
        "recommendations": [
            "Conduct regular adversarial testing including red team exercises and prompt injection testing for all externally-facing AI systems.",
            "Implement technical controls to detect and block adversarial inputs at the inference layer.",
            "Maintain threat intelligence subscriptions specific to AI security and update detection rules accordingly.",
        ],
    },
    "ISO-42001-A.8.7": {
        "name": "Transparency and explainability",
        "description": (
            "The organization shall ensure appropriate transparency and "
            "explainability of AI system decisions and outputs"
        ),
        "keywords": [
            "transparent",
            "explain",
            "interpret",
            "explainab",
            "visible",
            "understandab",
        ],
        "recommendations": [
            "Document how each AI system makes decisions and what factors influence its outputs in language accessible to non-technical stakeholders.",
            "Implement explainability features that allow end users and auditors to understand why specific AI outputs were generated.",
            "Establish a process for responding to stakeholder requests for explanation of AI-generated decisions.",
        ],
    },
    "ISO-42001-A.9.1": {
        "name": "Monitoring measurement and evaluation",
        "description": (
            "The organization shall evaluate performance and effectiveness of "
            "the AI management system"
        ),
        "keywords": [
            "metric",
            "measure",
            "dashboard",
            "monitor",
            "evaluate",
            "performance",
            "kpi",
        ],
        "recommendations": [
            "Define and track key performance indicators for each AI system covering accuracy reliability and business impact.",
            "Implement automated monitoring that generates alerts when AI system performance falls below defined thresholds.",
            "Conduct formal quarterly reviews of AI system performance metrics with leadership reporting.",
        ],
    },
    "ISO-42001-A.9.2": {
        "name": "Internal audit",
        "description": (
            "Internal audits shall be conducted at planned intervals to verify "
            "conformance"
        ),
        "keywords": [
            "audit",
            "internal audit",
            "assurance",
            "conformance",
            "verification",
            "assessment",
        ],
        "recommendations": [
            "Establish an internal audit schedule for the AI management system with audits conducted at least annually.",
            "Train internal auditors on ISO 42001 requirements and AI-specific audit techniques.",
            "Document audit findings corrective actions and follow-up verification in a centralized audit management system.",
        ],
    },
    "ISO-42001-A.10.1": {
        "name": "Nonconformity and corrective action",
        "description": (
            "Nonconformities shall be reacted to and corrected and continual "
            "improvement shall be supported"
        ),
        "keywords": [
            "corrective",
            "improvement",
            "nonconform",
            "incident",
            "remediation",
            "lesson",
        ],
        "recommendations": [
            "Implement a formal nonconformity management process that captures investigates and resolves deviations from AI governance requirements.",
            "Assign root cause analysis and corrective action ownership for all significant AI system failures or governance gaps.",
            "Track corrective action completion and verify effectiveness before closing nonconformities.",
        ],
    },
    "ISO-42001-A.10.2": {
        "name": "Continual improvement of AI systems",
        "description": (
            "The organization shall continually improve the suitability adequacy "
            "and effectiveness of the AI management system"
        ),
        "keywords": [
            "improve",
            "enhance",
            "iterate",
            "update",
            "evolve",
            "maturity",
            "continuous",
        ],
        "recommendations": [
            "Conduct an annual management review of the AI management system covering performance trends audit results and improvement opportunities.",
            "Establish a continuous improvement roadmap for AI governance maturity with measurable targets and timelines.",
            "Implement a lessons learned process that captures insights from AI incidents and improvement initiatives.",
        ],
    },
}
