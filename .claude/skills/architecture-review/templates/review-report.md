---
type: template
name: review-report
category: CATEGORY_NAME
classification: public
version: 1.0
last_updated: 2025-12-02
---

# Architecture Security Review Report

**Client:** [Client Name]
**Review Date:** [YYYY-MM-DD]
**Reviewer:** [Your Name]
**Architecture:** [System Name / Application Name]

---

## Executive Summary

**Purpose:** [Brief description of the architecture and review objectives]

**Scope:** [What was reviewed - components, systems, boundaries]

**Methodology:** [STRIDE threat modeling, NIST SP 800-160, OWASP ASVS, defense-in-depth analysis]

**Security Posture:** [Strong / Adequate / Weak - overall assessment]

### Key Findings Summary

| Severity | Count | Examples |
|---|---|---|
| **Critical** | [N] | [Brief description of critical findings] |
| **High** | [N] | [Brief description of high findings] |
| **Medium** | [N] | [Brief description of medium findings] |
| **Low** | [N] | [Brief description of low findings] |
| **Total** | [N] | |

### Top Recommendations

1. **[Recommendation 1]** - [Impact: High/Medium/Low] - [Effort: Hours/Days]
2. **[Recommendation 2]** - [Impact: High/Medium/Low] - [Effort: Hours/Days]
3. **[Recommendation 3]** - [Impact: High/Medium/Low] - [Effort: Hours/Days]

---

## Architecture Overview

### System Description

[Describe the system architecture, purpose, and key components]

**Technology Stack:**
- **Frontend:** [Technologies - React, Angular, etc.]
- **Backend:** [Technologies - Node.js, Python, Java, etc.]
- **Database:** [Technologies - PostgreSQL, MongoDB, etc.]
- **Infrastructure:** [Cloud provider, on-premises, hybrid]
- **Authentication:** [Method - OAuth 2.0, SAML, custom]
- **APIs:** [REST, GraphQL, gRPC, etc.]

### Architecture Diagrams

[Include architecture diagrams - logical, physical, network topology, data flow]

**Trust Boundaries:**
- External (Internet → DMZ)
- Internal (DMZ → Internal Network)
- Privileged (Internal → Database, Management Interfaces)

**Data Flows:**
- [Key data flows with security controls annotated]

---

## Threat Modeling Analysis

### Methodology

**Framework:** STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege)

**Process:**
1. Architecture decomposition (trust boundaries, data flows, assets, entry points)
2. STRIDE category application per component
3. Threat identification and documentation
4. Risk prioritization (DREAD scoring if applicable)

### Threat Register

| Threat ID | Category | Severity | Description | Affected Components | Risk Score | Recommended Mitigations |
|---|---|---|---|---|---|---|
| T-001 | Spoofing | Critical | [Description] | [Components] | [1-10] | [Mitigation] |
| T-002 | Tampering | High | [Description] | [Components] | [1-10] | [Mitigation] |
| T-003 | Info Disclosure | High | [Description] | [Components] | [1-10] | [Mitigation] |
| T-004 | DoS | Medium | [Description] | [Components] | [1-10] | [Mitigation] |

**See:** `02-threat-modeling/threat-register.md` for complete threat documentation

### Threat Model Diagram

[Include threat model diagram with threats annotated on architecture]

**See:** `02-threat-modeling/threat-model-diagram.png`

---

## Design Validation Findings

### Authentication Architecture

**Current Implementation:**
[Describe authentication design - MFA, password policies, session management]

**Findings:**

| Finding ID | Severity | Description | Standard Reference | Recommendation |
|---|---|---|---|---|
| F-001 | High | [Finding description] | OWASP ASVS V2.2.1 | [Recommendation] |
| F-002 | Medium | [Finding description] | NIST SP 800-63B | [Recommendation] |

### Authorization Architecture

**Current Implementation:**
[Describe authorization design - RBAC, ABAC, access controls]

**Findings:**

| Finding ID | Severity | Description | Standard Reference | Recommendation |
|---|---|---|---|---|
| F-003 | Critical | [Finding description] | OWASP ASVS V4.1.1 | [Recommendation] |

### Cryptography Architecture

**Current Implementation:**
[Describe encryption at rest, in transit, key management]

**Findings:**

| Finding ID | Severity | Description | Standard Reference | Recommendation |
|---|---|---|---|---|
| F-004 | High | [Finding description] | NIST SP 800-175B | [Recommendation] |

### Data Protection

**Current Implementation:**
[Describe input validation, output encoding, data classification]

**Findings:**

| Finding ID | Severity | Description | Standard Reference | Recommendation |
|---|---|---|---|---|
| F-005 | Medium | [Finding description] | OWASP ASVS V5.1.1 | [Recommendation] |

### API Security

**Current Implementation:**
[Describe API authentication, rate limiting, validation]

**Findings:**

| Finding ID | Severity | Description | Standard Reference | Recommendation |
|---|---|---|---|---|
| F-006 | High | [Finding description] | OWASP API Top 10 | [Recommendation] |

**See:** `03-findings/findings-register.md` for complete findings documentation

---

## Defense-in-Depth Analysis

### Security Layers

| Layer | Controls | Status | Gaps Identified |
|---|---|---|---|
| **Physical** | [Controls] | ✅ Adequate / ⚠️ Needs Improvement / ❌ Missing | [Gaps] |
| **Network** | [Controls] | ✅ Adequate / ⚠️ Needs Improvement / ❌ Missing | [Gaps] |
| **Host** | [Controls] | ✅ Adequate / ⚠️ Needs Improvement / ❌ Missing | [Gaps] |
| **Application** | [Controls] | ✅ Adequate / ⚠️ Needs Improvement / ❌ Missing | [Gaps] |
| **Data** | [Controls] | ✅ Adequate / ⚠️ Needs Improvement / ❌ Missing | [Gaps] |

### Single Points of Failure

**Identified SPOFs:**

1. **[SPOF 1]**
   - **Description:** [What is the single point of failure]
   - **Impact:** [What happens if this fails]
   - **Recommendation:** [How to add redundancy]

2. **[SPOF 2]**
   - **Description:** [What is the single point of failure]
   - **Impact:** [What happens if this fails]
   - **Recommendation:** [How to add redundancy]

### Network Segmentation

**Current Segmentation:**
[Describe network zones, security groups, firewalls]

**Assessment:**
- ✅ **DMZ Architecture:** [Adequate / Needs Improvement / Missing]
- ✅ **Micro-segmentation:** [Adequate / Needs Improvement / Missing]
- ✅ **Security Zones:** [Adequate / Needs Improvement / Missing]

**Gaps:**
- [Gap 1: Description and recommendation]
- [Gap 2: Description and recommendation]

**Standards:** NIST SP 800-125B, PCI DSS Req 1 (if applicable)

### Monitoring and Detection

**Current Monitoring:**
[Describe logging, SIEM, alerting, incident response]

**Assessment:**
- ✅ **Centralized Logging:** [Yes / No / Partial]
- ✅ **Security Event Coverage:** [Comprehensive / Adequate / Insufficient]
- ✅ **Real-Time Alerting:** [Yes / No / Partial]
- ✅ **Incident Response:** [Integrated / Manual / Missing]

**Gaps:**
- [Gap 1: Description and recommendation]
- [Gap 2: Description and recommendation]

**Standards:** NIST SP 800-92, PCI DSS Req 10 (if applicable)

### Fail-Safe Mechanisms

**Current Fail-Safe Design:**
[Describe failure modes and graceful degradation]

**Assessment:**
- ✅ **Fail-Secure:** [Yes / Partial / No]
- ✅ **Graceful Degradation:** [Yes / Partial / No]
- ✅ **Backup Mechanisms:** [Yes / Partial / No]

**Gaps:**
- [Gap 1: Description and recommendation]
- [Gap 2: Description and recommendation]

---

## Standards Compliance

### NIST SP 800-160 (Systems Security Engineering)

**Compliance Status:** [Compliant / Partial / Non-Compliant]

**Security Design Principles:**
- ✅ Least Privilege: [Compliant / Partial / Non-Compliant] - [Notes]
- ✅ Fail-Safe Defaults: [Compliant / Partial / Non-Compliant] - [Notes]
- ✅ Complete Mediation: [Compliant / Partial / Non-Compliant] - [Notes]
- ✅ Defense in Depth: [Compliant / Partial / Non-Compliant] - [Notes]

**Gaps:** [List non-compliant areas]

**See:** `04-compliance/NIST-800-160-compliance.md` for detailed analysis

### OWASP ASVS (Application Security Verification Standard)

**Target Verification Level:** [L1 / L2 / L3]

**Compliance Status:** [Compliant / Partial / Non-Compliant]

**Key Requirements:**
- V1 (Architecture): [Compliant / Partial / Non-Compliant] - [Notes]
- V2 (Authentication): [Compliant / Partial / Non-Compliant] - [Notes]
- V3 (Session Management): [Compliant / Partial / Non-Compliant] - [Notes]
- V4 (Access Control): [Compliant / Partial / Non-Compliant] - [Notes]
- V6 (Cryptography): [Compliant / Partial / Non-Compliant] - [Notes]

**Gaps:** [List non-compliant requirements]

**See:** `04-compliance/OWASP-ASVS-compliance.md` for detailed analysis

### Additional Compliance (if applicable)

**PCI DSS 4.0:**
- [Compliance status and gaps if payment card data is involved]

**HIPAA Security Rule:**
- [Compliance status and gaps if PHI is involved]

**GDPR:**
- [Compliance status and gaps if EU personal data is involved]

**SOC 2:**
- [Compliance status and gaps if SOC 2 certification is required]

---

## Recommendations Roadmap

### Critical Priority (Immediate Action Required)

| Rec ID | Recommendation | Impact | Effort | Timeline | Owner |
|---|---|---|---|---|---|
| R-001 | [Recommendation] | High | [Hours/Days] | [Days/Weeks] | [Team/Person] |
| R-002 | [Recommendation] | High | [Hours/Days] | [Days/Weeks] | [Team/Person] |

### High Priority (Implement Within 30 Days)

| Rec ID | Recommendation | Impact | Effort | Timeline | Owner |
|---|---|---|---|---|---|
| R-003 | [Recommendation] | Medium | [Hours/Days] | [Weeks] | [Team/Person] |
| R-004 | [Recommendation] | Medium | [Hours/Days] | [Weeks] | [Team/Person] |

### Medium Priority (Implement Within 90 Days)

| Rec ID | Recommendation | Impact | Medium | Effort | Timeline | Owner |
|---|---|---|---|---|---|---|
| R-005 | [Recommendation] | Medium | [Hours/Days] | [Months] | [Team/Person] |
| R-006 | [Recommendation] | Low | [Hours/Days] | [Months] | [Team/Person] |

### Low Priority (Implement When Resources Available)

| Rec ID | Recommendation | Impact | Effort | Timeline | Owner |
|---|---|---|---|---|---|
| R-007 | [Recommendation] | Low | [Hours/Days] | [Months] | [Team/Person] |

### Quick Wins (Low Effort, High Impact)

1. **[Quick Win 1]** - [Description] - [Effort: Hours]
2. **[Quick Win 2]** - [Description] - [Effort: Hours]
3. **[Quick Win 3]** - [Description] - [Effort: Hours]

**See:** `05-reporting/recommendations-roadmap.md` for detailed implementation guidance

---

## Conclusion

**Overall Assessment:**
[Summary of architecture security posture]

**Strengths:**
- [Strength 1]
- [Strength 2]
- [Strength 3]

**Areas for Improvement:**
- [Area 1]
- [Area 2]
- [Area 3]

**Next Steps:**
1. [Immediate action 1]
2. [Immediate action 2]
3. [Follow-up review timeline]

---

## Appendices

### Appendix A: Architecture Diagrams
[Include all architecture diagrams]

### Appendix B: Threat Model
[Include threat model diagram and detailed threat analysis]

### Appendix C: Findings Register
[Include complete findings register with all security weaknesses]

### Appendix D: Standards References
- NIST SP 800-160 Vol. 1: https://csrc.nist.gov/publications/detail/sp/800-160/vol-1/final
- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
- CSA Cloud Security Guidance: https://cloudsecurityalliance.org/research/guidance/
- NIST SP 800-207 (Zero Trust): https://csrc.nist.gov/publications/detail/sp/800-207/final

---

**Report Version:** 1.0
**Review Completion Date:** [YYYY-MM-DD]
**Next Review Date:** [YYYY-MM-DD] (recommended annual review)

**Confidential:** This document contains sensitive security information and should be protected accordingly.
