---
type: template
name: audit-report
category: CATEGORY_NAME
classification: public
version: 1.0
last_updated: 2025-12-02
---

# Dependency Audit Report

**Client:** [Client Name]
**Audit Date:** [YYYY-MM-DD]
**Auditor:** [Your Name]
**Project:** [Project Name]
**Ecosystems:** [npm, PyPI, Maven, etc.]

---

## Executive Summary

**Purpose:** Supply chain security analysis to identify dependency vulnerabilities, assess SBOM compliance, and evaluate third-party component risks

**Scope:** [What was audited - direct dependencies, transitive dependencies, SBOM generation]

**Methodology:** NIST SP 800-161 Rev. 1 + SLSA Framework + NTIA SBOM Minimum Elements

**Ecosystems Analyzed:**
- [Ecosystem 1] ([X] packages): [Description]
- [Ecosystem 2] ([Y] packages): [Description]

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

1. **[Critical CVE 1]** - Immediate action - [Package name] - [Effort: X hours]
2. **[Critical CVE 2]** - Immediate action - [Package name] - [Effort: X hours]
3. **[High Risk Package]** - 7-30 days - [Abandoned/Vulnerable] - [Effort: X hours]

### SBOM Status

- **Format:** [SPDX 2.3 / CycloneDX 1.5]
- **NTIA Compliance:** [✅ PASS / ❌ FAIL]
- **Components:** [X] total ([Y] direct, [Z] transitive)
- **Licenses Identified:** [X]% ([Y]/[Z] components)
- **Vulnerabilities Mapped:** [X] CVEs

---

## Project Overview

### Project Description

[Describe the project, its purpose, and key functionality]

**Technology Stack:**
- **Languages:** [JavaScript/Node.js 18, Python 3.11, etc.]
- **Frameworks:** [Express.js 4.18, Django 4.2, etc.]
- **Build System:** [npm, Maven, Gradle, etc.]
- **Deployment:** [Docker, Kubernetes, etc.]

### Dependency Inventory

**Total Dependencies:** [X] packages
- **Direct Dependencies:** [Y] (explicitly declared in manifest)
- **Transitive Dependencies:** [Z] (pulled in by direct dependencies)
- **Deepest Dependency Chain:** [N] levels

**Ecosystems Present:**
- **npm (JavaScript):** [X] packages
- **PyPI (Python):** [Y] packages
- **Maven (Java):** [Z] packages

**Dependency Distribution:**
```
Direct:      ████████████░░░░░░░░ 15 packages (10.5%)
Transitive:  ████████████████████ 127 packages (89.5%)
```

### Audit Scope

**In Scope:**
- Direct dependencies (package.json, requirements.txt, etc.)
- Transitive dependencies (lock files)
- SBOM generation (SPDX or CycloneDX)
- CVE analysis (NIST NVD, GitHub Advisory Database)
- Supply chain risk assessment (SLSA, maintainer trust)

**Out of Scope:**
- Source code vulnerability analysis (use code-review skill)
- Infrastructure security (use secure-config skill)
- Penetration testing (use security-testing skill)

---

## Methodology

### Standards Applied

**Supply Chain Security:**
- NIST SP 800-161 Rev. 1 - Cybersecurity Supply Chain Risk Management
- SLSA Framework v1.0 - Build provenance and integrity
- NIST SP 800-218 - Secure Software Development Framework (SSDF)
- ISO/IEC 27036 - Security in Supplier Relationships

**SBOM Standards:**
- SPDX 2.3 (ISO/IEC 5962:2021) OR CycloneDX 1.5 (OWASP)
- NTIA Minimum Elements for SBOM

**Vulnerability Assessment:**
- NIST NVD (National Vulnerability Database)
- GitHub Advisory Database
- OSV (Open Source Vulnerabilities)
- CVSS v3.1 severity scoring
- EPSS (Exploit Prediction Scoring System)

### Audit Process

1. **EXPLORE:** Dependency inventory (parse manifests, build dependency tree, catalog components)
2. **PLAN:** Vulnerability research (query NVD/GitHub/OSV, verify CVEs, calculate CVSS/EPSS)
3. **CODE:** SBOM generation (generate SPDX or CycloneDX, validate NTIA compliance)
4. **CODE:** Risk assessment (SLSA maturity, maintainer trust, package popularity, freshness)
5. **COMMIT:** Remediation planning (prioritize, create upgrade roadmap, document workarounds)

---

## Findings by Severity

### Critical Findings

---

#### VULN-001: [CVE ID] - [Vulnerability Title]

**Severity:** Critical (CVSS 9.0+)
**CVE:** [CVE-2024-1234]
**CWE:** [CWE-XXX] ([CWE Name])
**Package:** [package-name@version]
**Dependency Type:** [Direct / Transitive]
**Ecosystem:** [npm / PyPI / Maven / etc.]

**Description:**
[What is the vulnerability?]

**Affected Versions:**
- Vulnerable: [package-name] < [patched-version]
- Current version: [project-version] (VULNERABLE)

**CVSS v3.1 Breakdown:**
- **Score:** [X.X] (Critical)
- **Vector:** CVSS:3.1/AV:[N/A/L/P]/AC:[L/H]/PR:[N/L/H]/UI:[N/R]/S:[U/C]/C:[N/L/H]/I:[N/L/H]/A:[N/L/H]
- **Attack Vector:** [Network / Adjacent / Local / Physical]
- **Attack Complexity:** [Low / High]
- **Privileges Required:** [None / Low / High]
- **User Interaction:** [None / Required]
- **Confidentiality Impact:** [None / Low / High]
- **Integrity Impact:** [None / Low / High]
- **Availability Impact:** [None / Low / High]

**Exploitability:**
- **EPSS Score:** [0.XX] ([XX]% probability of exploitation in next 30 days)
- **Public Exploit:** [YES / NO]
- **Exploit Sources:** [Exploit-DB, Metasploit, GitHub POC]

**Impact:**
[Business impact - what can attacker do?]
- Data breach: [Specific data exposed]
- System compromise: [Extent of access]
- Business disruption: [Operational impact]

**Affected Code Paths:**
- `[src/file.js:line]` - [Description of how vulnerability is reachable]

**Remediation:**
```bash
# Upgrade command
[npm update package-name@patched-version]
# OR
[pip install --upgrade package-name==patched-version]
```

**Patched Version:** [package-name@patched-version] or later

**Breaking Changes:** [None / List breaking changes]

**Testing Required:** [Regression test plan]

**Workaround (if upgrade blocked):**
[Compensating controls if patch cannot be applied immediately]
- Input validation
- WAF rules
- Network segmentation
- Monitoring/alerting

**References:**
- NVD: [https://nvd.nist.gov/vuln/detail/CVE-2024-1234]
- GitHub Advisory: [https://github.com/advisories/GHSA-...]
- Vendor Advisory: [https://...]

**Remediation Effort:** [X hours/days]
**Priority:** P0 (Immediate - 0-7 days)

---

[Repeat for each Critical finding]

---

### High Findings

---

#### VULN-XXX: [CVE ID] - [Vulnerability Title]

[Follow same structure as Critical findings]

**Remediation Effort:** [X hours/days]
**Priority:** P1 (Urgent - 7-30 days)

---

### Medium Findings

---

#### VULN-XXX: [CVE ID] - [Vulnerability Title]

[Follow same structure]

**Remediation Effort:** [X hours/days]
**Priority:** P2 (Planned - 30-90 days)

---

### Low Findings

---

#### VULN-XXX: [CVE ID] - [Vulnerability Title]

[Follow same structure]

**Remediation Effort:** [X hours/days]
**Priority:** P3 (Low - When resources available)

---

## SBOM Analysis

### SBOM Generation

**Format:** [SPDX 2.3 / CycloneDX 1.5]
**File:** [sbom-cyclonedx.json / sbom-spdx.json]
**Generation Tool:** [Syft / CycloneDX Generator / OWASP Dependency-Check]
**Generation Date:** [YYYY-MM-DD HH:MM:SS]

**Components Inventoried:**
- Total: [X] components
- Direct: [Y] components
- Transitive: [Z] components

**NTIA Minimum Elements Compliance:**
- ✅ Supplier Name (present for all [X] components)
- ✅ Component Name (present for all [X] components)
- ✅ Version (specific version, not range)
- ✅ Other Unique Identifiers (purl present for all components)
- ✅ Dependency Relationships (direct vs transitive documented)
- ✅ SBOM Author (dependency-audit-agent)
- ✅ Timestamp ([YYYY-MM-DD HH:MM:SS])

**NTIA Compliance:** ✅ PASS (all 7 minimum elements present)

### License Analysis

**Licenses Identified:** [X]% ([Y]/[Z] components)

**License Distribution:**
| License | Count | Type | Risk Level |
|---|---|---|---|
| MIT | [N] | Permissive | ✅ Low |
| Apache-2.0 | [N] | Permissive | ✅ Low |
| BSD-3-Clause | [N] | Permissive | ✅ Low |
| GPL-3.0 | [N] | Copyleft (Strong) | ⚠️ Medium |
| LGPL-3.0 | [N] | Copyleft (Weak) | ⚠️ Medium |
| Unknown | [N] | N/A | ❌ High |

**License Compliance Issues:**
- ⚠️ GPL-3.0 detected: [X] components (requires open-sourcing derived works)
- ⚠️ Unknown licenses: [Y] components (manual review required)

**License Conflicts:**
- None detected ✅
- OR
- ❌ [Package A] (Apache-2.0) + [Package B] (GPL-2.0) = INCOMPATIBLE (patent clause conflict)

---

## Supply Chain Risk Assessment

### SLSA Maturity Assessment

**SLSA Framework (Build Provenance Maturity):**
| SLSA Level | Package Count | Risk Rating |
|------------|---------------|-------------|
| **L0** (No guarantees) | [N] | HIGH RISK |
| **L1** (Documented) | [N] | MEDIUM-HIGH RISK |
| **L2** (Hosted builds) | [N] | MEDIUM RISK |
| **L3** (Hardened builds) | [N] | LOW RISK |
| **L4** (Two-party review) | [N] | MINIMAL RISK |

**Critical Dependencies with Low SLSA:**
- [Package name] (L0) - [Authentication/Cryptography/Data processing]
- [Package name] (L1) - [Authentication/Cryptography/Data processing]

**Recommendation:** Prioritize dependencies with SLSA L2+ for critical components

---

### Maintainer Trust Analysis

**Maintainer Trust Indicators:**
| Indicator | Pass Rate | Observations |
|---|---|---|
| Verified GitHub account | [X]% | [Observations] |
| Multiple maintainers | [X]% | [Observations] |
| Active commits (<6 months) | [X]% | [Observations] |
| Security policy (SECURITY.md) | [X]% | [Observations] |
| Known organization | [X]% | [Observations] |

**High-Risk Maintainers:**
- [Package name]: Single maintainer, anonymous, inactive (last commit 18 months ago)
- [Package name]: No security policy, unresponsive to security issues

**Typosquatting Detected:**
- None detected ✅
- OR
- ❌ [Package name] (potential typosquat of [legitimate package]) - [Evidence]

---

### Package Freshness

**Update Frequency:**
| Status | Count | Definition |
|---|---|---|
| **Current** (<6 months) | [N] | ✅ Acceptable |
| **Stale** (6-12 months) | [N] | ⚠️ Monitor |
| **Outdated** (12-24 months) | [N] | ⚠️ Plan upgrade |
| **Abandoned** (>24 months) | [N] | ❌ Replace |

**Abandoned Packages:**
- [Package name@version] (last updated [X] months ago) → Replace with [alternative]
- [Package name@version] (last updated [X] months ago) → Replace with [alternative]

---

## Remediation Roadmap

### Critical Priority (Immediate Action - 0-7 Days)

| VULN ID | Package | CVE | CVSS | EPSS | Action | Effort | Owner |
|---|---|---|---|---|---|---|---|
| VULN-001 | [name] | CVE-2024-1234 | 9.8 | 0.85 | Upgrade to [version] | [X]h | [Team] |
| VULN-002 | [name] | CVE-2024-5678 | 9.1 | 0.42 | Upgrade to [version] | [X]h | [Team] |

**Total Effort:** [X] hours
**Business Risk if Not Fixed:** [Description of critical business impact]

---

### High Priority (Urgent - 7-30 Days)

| VULN ID | Package | CVE | CVSS | EPSS | Action | Effort | Owner |
|---|---|---|---|---|---|---|---|
| VULN-XXX | [name] | CVE-2024-XXXX | [X.X] | [0.XX] | [Action] | [X]h | [Team] |

**Total Effort:** [X] hours

---

### Medium Priority (Planned - 30-90 Days)

| VULN ID | Package | CVE | CVSS | Action | Effort | Owner |
|---|---|---|---|---|---|---|
| VULN-XXX | [name] | CVE-2024-XXXX | [X.X] | [Action] | [X]h | [Team] |

**Total Effort:** [X] hours

---

### Low Priority (Informational - When Resources Available)

| VULN ID | Package | CVE | CVSS | Action | Effort | Owner |
|---|---|---|---|---|---|---|
| VULN-XXX | [name] | CVE-2024-XXXX | [X.X] | [Action] | [X]h | [Team] |

**Total Effort:** [X] hours

---

### Quick Wins (Low Effort, High Impact)

1. **[Package name]** - Upgrade to [version] - [Effort: 1-2 hours] - Fixes CVE-[XXXX] (CVSS [X.X])
2. **[Package name]** - Upgrade to [version] - [Effort: 1-2 hours] - Fixes CVE-[XXXX] (CVSS [X.X])
3. **[Package name]** - Upgrade to [version] - [Effort: 1-2 hours] - Fixes CVE-[XXXX] (CVSS [X.X])

---

### Alternative Packages (Replacements)

| Current Package | Reason for Replacement | Alternative | Migration Effort |
|---|---|---|---|
| [moment] | Abandoned (no updates in 60 months) | date-fns / dayjs | [X] hours |
| [package] | High risk (multiple CVEs, no patches) | [alternative] | [X] hours |

---

## Conclusion

**Overall Assessment:**
[Summary of dependency security posture]

**Strengths:**
- [Strength 1]
- [Strength 2]
- [Strength 3]

**Areas for Improvement:**
- [Area 1]
- [Area 2]
- [Area 3]

**SBOM Compliance:**
- NTIA Minimum Elements: ✅ PASS
- Format: [SPDX 2.3 / CycloneDX 1.5]
- Completeness: [X]% components documented

**Next Steps:**
1. Implement P0 fixes (Critical vulnerabilities - 0-7 days)
2. Plan P1 fixes (High vulnerabilities - 7-30 days)
3. Schedule P2 fixes (Medium vulnerabilities - 30-90 days)
4. Establish continuous dependency monitoring (Dependabot, Snyk, OWASP Dependency-Track)

---

## Appendices

### Appendix A: Complete Vulnerability Register

[Link to vulnerability register CSV/Excel]

### Appendix B: SBOM Files

- SBOM (CycloneDX): [sbom-cyclonedx.json]
- SBOM (SPDX): [sbom-spdx.json]
- License Report: [license-report.md]

### Appendix C: SLSA Assessment Details

[Link to SLSA assessment documentation]

### Appendix D: Dependency Tree

[Link to dependency tree visualization]

### Appendix E: References

**Standards:**
- NIST SP 800-161 Rev. 1: https://csrc.nist.gov/publications/detail/sp/800-161/rev-1/final
- SLSA Framework: https://slsa.dev/
- SPDX: https://spdx.dev/
- CycloneDX: https://cyclonedx.org/
- NTIA SBOM Minimum Elements: https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom

**Vulnerability Databases:**
- NIST NVD: https://nvd.nist.gov/
- GitHub Advisory Database: https://github.com/advisories
- OSV: https://osv.dev/

**Tools Used:**
- [Syft / CycloneDX Generator / OWASP Dependency-Check]
- [npm audit / pip-audit / cargo-audit]

---

**Report Version:** 1.0
**Audit Completion Date:** [YYYY-MM-DD]
**Next Audit Date:** [YYYY-MM-DD] (recommended after remediation or quarterly)

**Confidential:** This document contains sensitive security information and should be protected accordingly.
