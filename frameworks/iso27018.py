"""ISO/IEC 27018:2019 cloud PII protection control library for the unified checker."""

from __future__ import annotations

FRAMEWORK_METADATA = {
    "name": "ISO/IEC 27018:2019",
    "description": (
        "Code of practice for protection of PII in public clouds "
        "acting as PII processors. Addresses consent, transparency, data subject "
        "rights, and PII security controls for cloud providers."
    ),
    "total_controls": 26,
    "domain": "Cloud PII Protection",
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

ISO_27018_CONTROLS: dict[str, dict[str, object]] = {
    "ISO-27018-A.1": {
        "name": "Consent and choice for processing PII in the cloud",
        "description": (
            "The cloud service provider shall obtain and record consent "
            "from PII principals or ensure the cloud service customer has obtained "
            "valid consent before processing PII."
        ),
        "keywords": [
            "consent",
            "choice",
            "pii",
            "opt-in",
            "permission",
            "recorded",
            "principal",
        ],
        "recommendations": [
            "Implement a consent management process that records PII principal "
            "consent before cloud processing begins.",
            "Document how the cloud service customer obtains and validates consent "
            "on behalf of PII principals in service agreements.",
            "Review consent records periodically and re-obtain consent when "
            "processing purposes change.",
        ],
    },
    "ISO-27018-A.2": {
        "name": "Legitimacy of PII processing purpose",
        "description": (
            "Processing of PII shall be limited to specified, explicit, "
            "and legitimate purposes communicated to the PII principal."
        ),
        "keywords": [
            "purpose",
            "legitimate",
            "specified",
            "explicit",
            "processing",
            "communicated",
            "pii",
        ],
        "recommendations": [
            "Document explicit and legitimate purposes for all PII processing "
            "activities in cloud services.",
            "Communicate processing purposes to PII principals through privacy "
            "notices and service documentation.",
            "Restrict cloud processing workflows to only the documented purposes "
            "and audit for purpose creep.",
        ],
    },
    "ISO-27018-A.3": {
        "name": "Limitation of PII collection",
        "description": (
            "PII collected by the cloud provider shall be adequate, "
            "relevant, and limited to what is necessary for the specified purpose."
        ),
        "keywords": [
            "collection",
            "adequate",
            "relevant",
            "necessary",
            "limited",
            "pii",
            "proportionate",
        ],
        "recommendations": [
            "Review data collection forms and cloud ingestion pipelines to "
            "eliminate unnecessary PII fields.",
            "Define data collection requirements tied to specific processing "
            "purposes and reject excess data at intake.",
            "Conduct periodic audits of stored PII to verify collected data "
            "remains adequate and relevant.",
        ],
    },
    "ISO-27018-A.4": {
        "name": "Data minimization in cloud PII processing",
        "description": (
            "The cloud provider shall collect and retain only the minimum "
            "PII necessary to fulfill the processing purpose."
        ),
        "keywords": [
            "data minimization",
            "minimum",
            "retain",
            "necessary",
            "reduce",
            "pii",
            "limit",
        ],
        "recommendations": [
            "Apply data minimization principles to all cloud PII collection "
            "and retention policies.",
            "Implement automated checks that flag PII fields exceeding "
            "documented minimum requirements.",
            "Schedule regular reviews to purge PII that is no longer necessary "
            "for the processing purpose.",
        ],
    },
    "ISO-27018-A.5": {
        "name": "Limitation on use, retention, and disclosure of PII",
        "description": (
            "PII shall not be used for purposes other than those for which "
            "it was collected without consent. Retention periods shall be defined "
            "and enforced."
        ),
        "keywords": [
            "retention",
            "disclosure",
            "use limitation",
            "consent",
            "retention period",
            "pii",
            "enforce",
        ],
        "recommendations": [
            "Define and enforce retention schedules for all PII categories "
            "processed in cloud environments.",
            "Implement technical controls preventing PII use beyond originally "
            "consented purposes without re-consent.",
            "Document disclosure restrictions and monitor cloud access logs "
            "for unauthorized PII sharing.",
        ],
    },
    "ISO-27018-A.6": {
        "name": "Accuracy and quality of PII in cloud environments",
        "description": (
            "The cloud provider shall implement controls to ensure PII "
            "processed is accurate, complete, and kept up to date as necessary."
        ),
        "keywords": [
            "accuracy",
            "quality",
            "complete",
            "up to date",
            "correct",
            "pii",
            "validation",
        ],
        "recommendations": [
            "Implement data validation rules at PII ingestion points in cloud "
            "processing pipelines.",
            "Establish procedures for PII principals to request corrections "
            "and propagate updates across cloud systems.",
            "Conduct periodic data quality audits on stored PII and remediate "
            "inaccuracies within defined SLAs.",
        ],
    },
    "ISO-27018-A.7": {
        "name": "Transparency of PII processing in cloud services",
        "description": (
            "Cloud service providers shall make information available "
            "about their PII processing practices, policies, and the purposes for "
            "which PII is processed."
        ),
        "keywords": [
            "transparency",
            "notice",
            "privacy policy",
            "disclosure",
            "practices",
            "pii",
            "inform",
        ],
        "recommendations": [
            "Publish a clear privacy notice describing PII processing practices, "
            "purposes, and cloud service provider responsibilities.",
            "Make PII processing documentation accessible to cloud service "
            "customers and PII principals upon request.",
            "Update transparency materials whenever processing practices or "
            "purposes change and notify affected parties.",
        ],
    },
    "ISO-27018-A.8": {
        "name": "PII principal access and participation rights",
        "description": (
            "PII principals shall have the right to access their PII "
            "held by the cloud service provider and request corrections or deletions."
        ),
        "keywords": [
            "access",
            "data subject",
            "correction",
            "deletion",
            "right",
            "pii principal",
            "request",
        ],
        "recommendations": [
            "Implement a data subject access request process with defined "
            "response timelines for cloud-hosted PII.",
            "Provide mechanisms for PII principals to request correction, "
            "deletion, or portability of their data.",
            "Log and track all data subject requests through to completion "
            "with audit evidence.",
        ],
    },
    "ISO-27018-A.9": {
        "name": "Accountability for PII processing in the cloud",
        "description": (
            "The cloud provider shall be accountable for complying with "
            "applicable PII protection principles and shall document compliance measures."
        ),
        "keywords": [
            "accountability",
            "compliance",
            "document",
            "responsible",
            "governance",
            "pii",
            "measure",
        ],
        "recommendations": [
            "Assign a data protection officer or accountable owner for cloud "
            "PII processing activities.",
            "Document compliance measures demonstrating adherence to PII "
            "protection principles.",
            "Conduct regular accountability reviews with documented evidence "
            "of compliance status.",
        ],
    },
    "ISO-27018-A.10": {
        "name": "Information security controls for PII in cloud",
        "description": (
            "The cloud provider shall implement and maintain appropriate "
            "technical and organizational security measures to protect PII against "
            "unauthorized access, disclosure, alteration, and destruction."
        ),
        "keywords": [
            "security",
            "protect",
            "unauthorized",
            "access control",
            "technical",
            "organizational",
            "pii",
        ],
        "recommendations": [
            "Implement defense-in-depth security controls specifically scoped "
            "to PII stored and processed in cloud environments.",
            "Apply role-based access controls and encryption to all PII "
            "repositories and processing systems.",
            "Conduct regular security assessments focused on PII protection "
            "and remediate findings promptly.",
        ],
    },
    "ISO-27018-A.11": {
        "name": "Privacy compliance and regulatory alignment",
        "description": (
            "The cloud provider shall identify and comply with applicable "
            "laws, regulations, and contractual obligations relating to PII protection "
            "in each jurisdiction where PII is processed."
        ),
        "keywords": [
            "privacy",
            "regulatory",
            "compliance",
            "gdpr",
            "jurisdiction",
            "legal",
            "pii",
        ],
        "recommendations": [
            "Maintain a register of applicable privacy laws and regulations "
            "for each jurisdiction where cloud PII is processed.",
            "Map cloud processing activities to regulatory requirements and "
            "document compliance controls for each.",
            "Review regulatory obligations annually and upon expansion into "
            "new geographic regions.",
        ],
    },
    "ISO-27018-B.1": {
        "name": "Disclosure of PII geographic processing locations",
        "description": (
            "The cloud service provider shall disclose to the cloud "
            "service customer the countries or regions where PII may be stored, "
            "processed, or transferred."
        ),
        "keywords": [
            "geolocation",
            "location",
            "region",
            "country",
            "data residency",
            "transfer",
            "disclose",
        ],
        "recommendations": [
            "Document and disclose all countries and regions where PII may "
            "be stored, processed, or transferred.",
            "Include geolocation disclosures in cloud service agreements and "
            "update when infrastructure changes.",
            "Notify cloud service customers before PII is processed in new "
            "geographic regions.",
        ],
    },
    "ISO-27018-B.2": {
        "name": "Disclosure of cloud subprocessors handling PII",
        "description": (
            "Before engaging subprocessors to handle PII, the cloud "
            "provider shall disclose subprocessor identities and obtain customer "
            "authorization."
        ),
        "keywords": [
            "subprocessor",
            "third party",
            "disclosure",
            "authorization",
            "vendor",
            "pii",
            "notify",
        ],
        "recommendations": [
            "Maintain a current list of subprocessors with access to PII "
            "and publish it to cloud service customers.",
            "Obtain customer authorization before engaging new subprocessors "
            "that will handle PII.",
            "Include subprocessor notification and objection rights in "
            "cloud service contracts.",
        ],
    },
    "ISO-27018-B.3": {
        "name": "Control of cloud provider employee access to PII",
        "description": (
            "The cloud provider shall ensure employees can only access "
            "PII on a need-to-know basis and shall implement technical controls to "
            "enforce this restriction."
        ),
        "keywords": [
            "employee",
            "need-to-know",
            "access",
            "privileged",
            "restrict",
            "pii",
            "enforce",
        ],
        "recommendations": [
            "Implement need-to-know access policies for all employees "
            "handling cloud PII with role-based enforcement.",
            "Require MFA and just-in-time access for employee PII access "
            "with full audit logging.",
            "Conduct quarterly access reviews to verify employee PII "
            "permissions remain appropriate.",
        ],
    },
    "ISO-27018-B.4": {
        "name": "PII breach notification in cloud environments",
        "description": (
            "The cloud provider shall notify the cloud service customer "
            "without undue delay upon discovery of a PII breach, and support breach "
            "notification obligations."
        ),
        "keywords": [
            "breach",
            "notification",
            "incident",
            "undue delay",
            "pii",
            "disclosure",
            "report",
        ],
        "recommendations": [
            "Define breach notification timelines and procedures in cloud "
            "service agreements aligned with regulatory requirements.",
            "Implement automated breach detection and escalation workflows "
            "for PII incidents in cloud environments.",
            "Provide cloud service customers with breach details sufficient "
            "to meet their own notification obligations.",
        ],
    },
    "ISO-27018-B.5": {
        "name": "Anonymization and pseudonymization of PII",
        "description": (
            "Where PII is no longer required in identifiable form, the "
            "cloud provider shall support anonymization or pseudonymization of the data."
        ),
        "keywords": [
            "anonymization",
            "pseudonymization",
            "de-identify",
            "masking",
            "pii",
            "identifiable",
            "transform",
        ],
        "recommendations": [
            "Implement anonymization and pseudonymization capabilities for "
            "PII no longer required in identifiable form.",
            "Document techniques used and verify re-identification risk "
            "before releasing anonymized datasets.",
            "Apply pseudonymization by default in non-production cloud "
            "environments processing PII.",
        ],
    },
    "ISO-27018-B.6": {
        "name": "Encryption of PII in cloud storage and transit",
        "description": (
            "PII shall be encrypted when stored and transmitted using "
            "current cryptographic standards appropriate to the sensitivity of the data."
        ),
        "keywords": [
            "encryption",
            "encrypt",
            "transit",
            "at rest",
            "cryptographic",
            "pii",
            "tls",
        ],
        "recommendations": [
            "Encrypt all PII at rest using AES-256 or equivalent standards "
            "with managed key rotation.",
            "Require TLS 1.2 or higher for all PII transmission between "
            "cloud systems and external endpoints.",
            "Document encryption standards and verify compliance through "
            "regular cryptographic audits.",
        ],
    },
    "ISO-27018-B.7": {
        "name": "Controls for PII transmission between cloud systems",
        "description": (
            "Controls shall be implemented to protect PII during "
            "transmission between cloud systems, including encryption, integrity "
            "checking, and access logging."
        ),
        "keywords": [
            "transmission",
            "integrity",
            "logging",
            "inter-system",
            "pii",
            "protect",
            "transfer",
        ],
        "recommendations": [
            "Implement end-to-end encryption and integrity checking for "
            "all inter-cloud PII transmissions.",
            "Log all PII transfers between cloud systems with source, "
            "destination, and data volume metadata.",
            "Restrict PII transmission paths to approved network routes "
            "with monitoring for unauthorized transfers.",
        ],
    },
    "ISO-27018-B.8": {
        "name": "Secure handling of temporary files containing PII",
        "description": (
            "Temporary files containing PII created during cloud "
            "processing shall be identified, tracked, and securely deleted when "
            "no longer needed."
        ),
        "keywords": [
            "temporary",
            "temp file",
            "delete",
            "secure deletion",
            "pii",
            "track",
            "cleanup",
        ],
        "recommendations": [
            "Identify and catalog all temporary file locations where PII "
            "may be created during cloud processing.",
            "Implement automated secure deletion of temporary PII files "
            "upon processing completion.",
            "Monitor for orphaned temporary files containing PII and "
            "remediate within defined SLAs.",
        ],
    },
    "ISO-27018-B.9": {
        "name": "Return, transfer, and secure disposal of PII",
        "description": (
            "Upon contract termination, the cloud provider shall return "
            "or securely dispose of all PII in accordance with customer instructions "
            "and applicable regulations."
        ),
        "keywords": [
            "disposal",
            "return",
            "termination",
            "deletion",
            "secure erase",
            "pii",
            "contract",
        ],
        "recommendations": [
            "Document PII return and secure disposal procedures for "
            "contract termination scenarios in service agreements.",
            "Provide customers with data export capabilities and certified "
            "evidence of secure PII deletion upon termination.",
            "Verify complete PII removal from all cloud systems including "
            "backups and temporary storage after disposal.",
        ],
    },
    "ISO-27018-B.10": {
        "name": "Audit logging for PII access in cloud environments",
        "description": (
            "The cloud provider shall maintain audit logs of access to "
            "PII including the identity of the accessor, time of access, and action taken."
        ),
        "keywords": [
            "audit log",
            "access log",
            "identity",
            "timestamp",
            "pii",
            "track",
            "record",
        ],
        "recommendations": [
            "Enable comprehensive audit logging for all PII access including "
            "read, write, modify, and delete operations.",
            "Ensure audit logs capture accessor identity, timestamp, action, "
            "and affected PII records.",
            "Protect audit logs from tampering and retain them per regulatory "
            "and contractual requirements.",
        ],
    },
    "ISO-27018-B.11": {
        "name": "Controls on hardcopy output containing PII",
        "description": (
            "Controls shall be implemented to prevent unauthorized "
            "creation of hardcopy output containing PII from cloud systems."
        ),
        "keywords": [
            "hardcopy",
            "print",
            "output",
            "physical",
            "pii",
            "prevent",
            "unauthorized",
        ],
        "recommendations": [
            "Restrict printing and hardcopy export of PII from cloud systems "
            "to authorized personnel with approval workflows.",
            "Implement technical controls blocking unauthorized print or "
            "export of PII-containing cloud data.",
            "Maintain logs of all hardcopy PII output and enforce secure "
            "disposal procedures for printed materials.",
        ],
    },
    "ISO-27018-B.12": {
        "name": "Customer PII policy enforcement in cloud usage",
        "description": (
            "The cloud service customer shall implement and enforce a "
            "policy governing acceptable use of cloud services for PII processing, "
            "communicated to all authorized users."
        ),
        "keywords": [
            "policy",
            "acceptable use",
            "customer",
            "enforce",
            "pii",
            "communicated",
            "users",
        ],
        "recommendations": [
            "Develop and publish an acceptable use policy for cloud services "
            "processing PII, communicated to all authorized users.",
            "Enforce the policy through technical controls including DLP "
            "and cloud access restrictions.",
            "Review and update the customer PII cloud usage policy annually "
            "and after significant service changes.",
        ],
    },
    "ISO-27018-C.1": {
        "name": "Prohibition on use of PII for provider marketing",
        "description": (
            "The cloud provider shall not use PII processed on behalf "
            "of the cloud service customer for the provider's own marketing or "
            "advertising purposes without explicit consent."
        ),
        "keywords": [
            "marketing",
            "advertising",
            "prohibition",
            "provider",
            "consent",
            "pii",
            "independent",
        ],
        "recommendations": [
            "Document a strict prohibition on using customer PII for provider "
            "marketing in service agreements and privacy policies.",
            "Implement technical and procedural controls preventing PII "
            "access by marketing or sales teams.",
            "Audit periodically to verify no customer PII is used for "
            "provider marketing without explicit consent.",
        ],
    },
    "ISO-27018-C.2": {
        "name": "Prohibition on unauthorized third-party PII disclosure",
        "description": (
            "The cloud provider shall not disclose PII to third parties "
            "except as required by law or as explicitly authorized by the cloud "
            "service customer."
        ),
        "keywords": [
            "third party",
            "disclosure",
            "prohibition",
            "authorized",
            "pii",
            "share",
            "restrict",
        ],
        "recommendations": [
            "Define and enforce policies prohibiting PII disclosure to third "
            "parties without customer authorization or legal requirement.",
            "Maintain an authorization log for all permitted third-party PII "
            "disclosures with customer approval evidence.",
            "Implement monitoring to detect and alert on unauthorized PII "
            "sharing from cloud systems.",
        ],
    },
    "ISO-27018-C.3": {
        "name": "PII processing limited to commissioned purposes",
        "description": (
            "The cloud provider shall process PII only for purposes "
            "specified by and on behalf of the cloud service customer, not for any "
            "independent purposes of the provider."
        ),
        "keywords": [
            "commissioned",
            "customer purpose",
            "limited",
            "provider",
            "processing",
            "pii",
            "on behalf",
        ],
        "recommendations": [
            "Document that PII processing is limited to customer-specified "
            "purposes in all cloud service agreements.",
            "Implement processing controls that prevent PII use for "
            "provider independent purposes.",
            "Conduct regular audits verifying PII processing aligns only "
            "with commissioned customer purposes.",
        ],
    },
}
