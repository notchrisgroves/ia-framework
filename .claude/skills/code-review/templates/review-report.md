---
type: template
name: review-report
category: CATEGORY_NAME
classification: public
version: 1.0
last_updated: 2025-12-02
---

# Security Code Review Report

**Client:** [Client Name]
**Review Date:** [YYYY-MM-DD]
**Reviewer:** [Your Name]
**Application:** [Application Name]
**Languages Reviewed:** [Python 3.11, JavaScript/Node.js 18, etc.]

---

## Executive Summary

**Purpose:** Security code review to identify vulnerabilities and validate secure coding practices

**Scope:** [What was reviewed - components, modules, LOC]

**Methodology:** OWASP Code Review Guide + Language-Specific Security Standards (dynamically researched for each language)

**Languages Analyzed:**
- [Language 1] [Version]: [Standards applied]
- [Language 2] [Version]: [Standards applied]

**Security Posture:** [Strong / Adequate / Weak - overall assessment]

### Key Findings Summary

| Severity | Count | Examples |
|---|---|---|
| **Critical** | [N] | [Brief description] |
| **High** | [N] | [Brief description] |
| **Medium** | [N] | [Brief description] |
| **Low** | [N] | [Brief description] |
| **Total** | [N] | |

### Top Recommendations

1. **[Critical Issue 1]** - [Impact] - [Effort: Hours/Days]
2. **[Critical Issue 2]** - [Impact] - [Effort: Hours/Days]
3. **[High Issue 1]** - [Impact] - [Effort: Hours/Days]

---

## Application Overview

### System Description

[Describe the application, its purpose, and key functionality]

**Technology Stack:**
- **Languages:** [Python 3.11, JavaScript/Node.js 18, etc.]
- **Frameworks:** [Django 4.2, Express.js 4.18, etc.]
- **Database:** [PostgreSQL 15, MongoDB 6, etc.]
- **Infrastructure:** [Cloud provider, containerization, etc.]
- **Authentication:** [OAuth 2.0, JWT, session-based, etc.]

### Review Scope

**In Scope:**
- [Module/Component 1] ([LOC] lines)
- [Module/Component 2] ([LOC] lines)
- Total: [X] files, [Y] lines of code

**Out of Scope:**
- [Component 1] (to be reviewed separately)
- [Component 2] (third-party library)

---

## Methodology

### Standards Applied

**General Standards:**
- OWASP Code Review Guide v2.0
- CWE Top 25 Most Dangerous Weaknesses (2023)
- CVSS v3.1 for severity scoring

**Language-Specific Standards (Dynamically Researched):**

**[Language 1] [Version]:**
- [Standard/Resource 1] - [URL]
- [Standard/Resource 2] - [URL]
- [Primary vulnerability focus]

**[Language 2] [Version]:**
- [Standard/Resource 1] - [URL]
- [Standard/Resource 2] - [URL]
- [Primary vulnerability focus]

### Review Process

1. **EXPLORE:** Identified languages, mapped codebase structure, reviewed existing security controls
2. **PLAN:** Dynamically researched language-specific security standards, created review checklist
3. **CODE:** Conducted security review with language-specific vulnerability analysis (WHAT/WHY/HOW approach)
4. **COMMIT:** Generated findings with POC, remediation guidance, and prioritization

---

## Findings by Severity

### Critical Findings

---

#### F-001: [Vulnerability Title]

**Severity:** Critical (CVSS 9.0)
**CWE:** [CWE-XXX] ([CWE Name])
**Location:** `[file.py:line]`
**Language:** [Python 3.11]

**WHAT (Vulnerability Description):**
[Description of what the vulnerability is in this specific language]

**WHY (Root Cause in This Language):**
[Explanation of WHY this vulnerability exists in this language]
[What language feature/design enables this vulnerability?]

**Vulnerable Code:**
```[language]
# file.py:42
[vulnerable code snippet]
```

**Impact:**
[Business impact - what can attacker do?]
- Data breach: [Specific data exposed]
- System compromise: [Extent of access]
- Business disruption: [Operational impact]

**Proof-of-Concept:**
```[language]
# Demonstrates exploitability
[POC code showing how to exploit the vulnerability]
```

**WHY POC WORKS:**
[Explanation of why/how the POC exploits the vulnerability]

**HOW TO FIX (Remediation):**
```[language]
# file.py:42 - SECURE version
[secure code example]
```

**WHY REMEDIATION WORKS:**
[Explanation of why the secure code prevents the vulnerability]
[What makes this approach secure in this language?]

**CVSS v3.1 Breakdown:**
- Attack Vector: [Network/Adjacent/Local/Physical]
- Attack Complexity: [Low/High]
- Privileges Required: [None/Low/High]
- User Interaction: [None/Required]
- Scope: [Unchanged/Changed]
- Confidentiality Impact: [None/Low/High]
- Integrity Impact: [None/Low/High]
- Availability Impact: [None/Low/High]
- **Score:** [X.X] (Critical)

**References:**
- OWASP: [Link to relevant OWASP resource]
- CWE-XXX: [Link to CWE description]
- [Language]-specific: [Link to language security guide]

**Remediation Effort:** [X hours/days]
**Priority:** Immediate (0-7 days)

---

[Repeat for each Critical finding]

---

### High Findings

---

#### F-XXX: [Vulnerability Title]

[Follow same structure as Critical findings: WHAT/WHY/HOW/POC/Remediation with language-specific context]

---

### Medium Findings

---

#### F-XXX: [Vulnerability Title]

[Follow same structure]

---

### Low Findings

---

#### F-XXX: [Vulnerability Title]

[Follow same structure]

---

## Language-Specific Analysis

### [Language 1] Security Analysis

**Language:** [Python 3.11]
**Framework:** [Django 4.2]
**Lines of Code:** [X] lines

**Standards Researched:**
- Python Security Advisories (2025)
- Django Security Documentation
- OWASP Python Security Cheat Sheet

**Vulnerability Focus Areas:**
1. **Deserialization:** pickle, YAML, JSON handling
2. **SQL Injection:** ORM usage, raw queries
3. **Command Injection:** subprocess, os.system usage
4. **Cryptography:** Password hashing, random number generation

**Findings in This Language:**
- Critical: [N] findings
- High: [N] findings
- Medium: [N] findings
- Low: [N] findings

**Language-Specific Observations:**
- [Observation 1: e.g., "bcrypt correctly used for password hashing"]
- [Observation 2: e.g., "No instances of pickle.loads with untrusted data"]
- [Concern 1: e.g., "Several instances of f-strings in SQL queries"]

**Secure Coding Patterns Observed:**
- ✅ [Pattern 1]
- ✅ [Pattern 2]

**Anti-Patterns Observed:**
- ❌ [Anti-pattern 1]
- ❌ [Anti-pattern 2]

---

### [Language 2] Security Analysis

[Repeat same structure for each language]

---

## Defense-in-Depth Analysis

### Security Layers

| Layer | Controls Present | Status | Gaps Identified |
|---|---|---|---|
| **Input Validation** | [Controls] | ✅ / ⚠️ / ❌ | [Gaps] |
| **Authentication** | [Controls] | ✅ / ⚠️ / ❌ | [Gaps] |
| **Authorization** | [Controls] | ✅ / ⚠️ / ❌ | [Gaps] |
| **Cryptography** | [Controls] | ✅ / ⚠️ / ❌ | [Gaps] |
| **Output Encoding** | [Controls] | ✅ / ⚠️ / ❌ | [Gaps] |
| **Error Handling** | [Controls] | ✅ / ⚠️ / ❌ | [Gaps] |
| **Logging** | [Controls] | ✅ / ⚠️ / ❌ | [Gaps] |

### Security Controls Assessment

**Authentication:**
- [Control 1]: [Status and observations]
- [Control 2]: [Status and observations]

**Input Validation:**
- [Control 1]: [Status and observations]
- [Control 2]: [Status and observations]

**Output Encoding:**
- [Control 1]: [Status and observations]
- [Control 2]: [Status and observations]

---

## Remediation Roadmap

### Critical Priority (Immediate Action - 0-7 Days)

| Finding ID | Title | Impact | Effort | Owner |
|---|---|---|---|---|
| F-001 | [Title] | [Impact] | [X hours] | [Team] |
| F-002 | [Title] | [Impact] | [X hours] | [Team] |

**Total Effort:** [X] hours/days
**Business Risk if Not Fixed:** [Description]

---

### High Priority (Urgent - 7-30 Days)

| Finding ID | Title | Impact | Effort | Owner |
|---|---|---|---|---|
| F-XXX | [Title] | [Impact] | [X hours] | [Team] |

**Total Effort:** [X] hours/days

---

### Medium Priority (Planned - 30-90 Days)

| Finding ID | Title | Impact | Effort | Owner |
|---|---|---|---|---|
| F-XXX | [Title] | [Impact] | [X hours] | [Team] |

**Total Effort:** [X] hours/days

---

### Low Priority (Informational - When Resources Available)

| Finding ID | Title | Impact | Effort | Owner |
|---|---|---|---|---|
| F-XXX | [Title] | [Impact] | [X hours] | [Team] |

**Total Effort:** [X] hours/days

---

### Quick Wins (Low Effort, High Impact)

1. **[Quick Win 1]** - [Description] - [Effort: 1-2 hours]
2. **[Quick Win 2]** - [Description] - [Effort: 1-2 hours]
3. **[Quick Win 3]** - [Description] - [Effort: 1-2 hours]

---

## Standards Compliance

### OWASP Top 10 (2021) Coverage

| Category | Findings | Status | Notes |
|---|---|---|---|
| A01: Broken Access Control | [N] | ⚠️ | [Notes] |
| A02: Cryptographic Failures | [N] | ⚠️ | [Notes] |
| A03: Injection | [N] | ❌ | [Notes] |
| A04: Insecure Design | [N] | ✅ | [Notes] |
| A05: Security Misconfiguration | [N] | ⚠️ | [Notes] |
| A06: Vulnerable Components | [N] | ✅ | [Notes] |
| A07: Auth Failures | [N] | ⚠️ | [Notes] |
| A08: Integrity Failures | [N] | ✅ | [Notes] |
| A09: Logging Failures | [N] | ⚠️ | [Notes] |
| A10: SSRF | [N] | ✅ | [Notes] |

**Legend:** ✅ No issues | ⚠️ Some issues | ❌ Critical issues

---

### CWE Top 25 Coverage

[List relevant CWEs found and addressed]

---

## Conclusion

**Overall Assessment:**
[Summary of code security posture]

**Strengths:**
- [Strength 1]
- [Strength 2]
- [Strength 3]

**Areas for Improvement:**
- [Area 1]
- [Area 2]
- [Area 3]

**Language-Specific Observations:**
- [Language 1]: [Overall security maturity for this language]
- [Language 2]: [Overall security maturity for this language]

**Next Steps:**
1. [Immediate action 1]
2. [Immediate action 2]
3. [Follow-up review timeline]

---

## Appendices

### Appendix A: Findings Register

[Link to complete findings register with all details]

### Appendix B: Proof-of-Concept Examples

[Link to POC code examples directory]

### Appendix C: Language-Specific Standards Research

[Link to standards research documentation]

### Appendix D: Automated Scan Results

[Include results from Bandit, npm audit, etc. if used]

### Appendix E: References

**OWASP Resources:**
- OWASP Code Review Guide: https://owasp.org/www-project-code-review-guide/
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/

**CWE Resources:**
- CWE Top 25: https://cwe.mitre.org/top25/
- CWE Database: https://cwe.mitre.org/

**Language-Specific Resources:**
- [Language 1]: [URLs from research]
- [Language 2]: [URLs from research]

**Tools Used:**
- [Tool 1]: [Purpose]
- [Tool 2]: [Purpose]

---

**Report Version:** 1.0
**Review Completion Date:** [YYYY-MM-DD]
**Next Review Date:** [YYYY-MM-DD] (recommended after remediation)

**Confidential:** This document contains sensitive security information and should be protected accordingly.
