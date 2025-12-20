# Industry Standards & Methodology Sources

**Authoritative frameworks for threat intelligence and CVE research**

---

## Primary Standards

### MITRE ATT&CK Framework

**URL:** https://attack.mitre.org/

**Coverage:** Enterprise, Mobile, ICS tactics and techniques

**Focus:**
- Adversary behavior patterns and TTPs
- Detection methods for each technique
- Mitigation strategies and security controls
- Threat actor group profiles

**Application:** Primary framework for threat intelligence organization and standardized threat communication

**Matrices:**
- Enterprise ATT&CK: Windows, Linux, macOS, Cloud, Network
- Mobile ATT&CK: Android, iOS
- ICS ATT&CK: Industrial Control Systems

**Structure:**
- 14 Tactics (objectives): Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection, Command and Control, Exfiltration, Impact
- 200+ Techniques (how to achieve objectives)
- 400+ Sub-techniques (specific implementations)
- 130+ Groups (threat actor profiles)
- 700+ Software (malware, tools)

---

### NIST National Vulnerability Database (NVD)

**URL:** https://nvd.nist.gov/

**Coverage:** Comprehensive CVE database with CVSS scores, CWE mappings, affected products

**Focus:**
- Vulnerability technical details
- CWE weakness mappings
- References to vendor advisories and patches
- Affected product versions

**Application:** Authoritative source for CVE intelligence and vulnerability research

**Data Elements:**
- CVE ID (e.g., CVE-2024-12345)
- Description (vulnerability summary)
- CVSS v3.1 Base Score and Vector String
- CWE Classification
- Published/Modified Dates
- CPE (Common Platform Enumeration) for affected products
- References (vendor advisories, patches, exploits)

**API Access:** https://nvd.nist.gov/developers/vulnerabilities

---

### FIRST CVSSv3.1 Specification

**URL:** https://www.first.org/cvss/v3.1/specification-document

**Coverage:** Common Vulnerability Scoring System methodology

**Focus:**
- Base Score: Intrinsic vulnerability characteristics (Attack Vector, Complexity, Privileges, User Interaction, Scope, Confidentiality/Integrity/Availability Impact)
- Temporal Score: Exploit maturity, remediation level, report confidence
- Environmental Score: CIA requirements, modified base metrics for specific environments

**Application:** Standardized vulnerability severity assessment for prioritization

**Severity Ranges:**
- None: 0.0
- Low: 0.1-3.9
- Medium: 4.0-6.9
- High: 7.0-8.9
- Critical: 9.0-10.0

**Calculator:** https://www.first.org/cvss/calculator/3.1

**Vector String Example:** `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` = 9.8 (Critical)

---

### CISA Known Exploited Vulnerabilities (KEV) Catalog

**URL:** https://www.cisa.gov/known-exploited-vulnerabilities-catalog

**Coverage:** Actively exploited vulnerabilities in the wild

**Focus:**
- High-priority threats with confirmed active exploitation
- Required remediation timelines (typically 14-21 days)
- Vendor, product, and vulnerability details
- Due dates for Federal Civilian Executive Branch (FCEB) agencies

**Application:** Prioritization framework for patching and vulnerability management

**Binding Operational Directive 22-01:**
- Federal agencies MUST remediate KEV vulnerabilities within specified timelines
- Applies to internet-facing systems
- Failure to remediate = significant risk

**KEV Data Fields:**
- CVE ID
- Vendor/Product
- Vulnerability Name
- Date Added to Catalog
- Due Date (remediation deadline)
- Required Action (patch, mitigate, remove)
- Known Ransomware Campaign Use (yes/no)

**Usage:** Always check KEV status for CVEs to prioritize real-world threats over theoretical risks

---

## Supporting Standards

### MITRE CWE (Common Weakness Enumeration)

**URL:** https://cwe.mitre.org/

**Application:** Vulnerability classification and root cause analysis

**Purpose:** Categorize software weaknesses to understand vulnerability patterns

**Top 25 Most Dangerous:**
- CWE-89: SQL Injection
- CWE-79: Cross-site Scripting (XSS)
- CWE-787: Out-of-bounds Write
- CWE-20: Improper Input Validation
- CWE-125: Out-of-bounds Read
- CWE-78: OS Command Injection
- CWE-416: Use After Free
- CWE-22: Path Traversal
- CWE-352: Cross-Site Request Forgery (CSRF)
- CWE-434: Unrestricted Upload of Dangerous File Type

**Relationship:** CVEs map to CWEs (specific vulnerability → general weakness pattern)

---

### Exploit Prediction Scoring System (EPSS)

**URL:** https://www.first.org/epss/

**Application:** Exploitability probability scoring

**Purpose:** Predict likelihood of exploitation in the next 30 days

**Scoring:**
- Probability: 0.0-1.0 (e.g., 0.924 = 92.4% chance)
- Percentile: Comparison to all CVEs (e.g., 98th percentile = top 2%)

**Use Case:** Combine with CVSS for prioritization (high CVSS + high EPSS = critical priority)

**Data Factors:**
- CVE age
- Public exploit availability
- Vendor patch status
- Trending discussions (social media, dark web)
- Metasploit module existence

---

### OWASP Top 10

**URL:** https://owasp.org/www-project-top-ten/

**Application:** Web application threat prioritization

**Latest (2021):**
1. Broken Access Control
2. Cryptographic Failures
3. Injection
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable and Outdated Components
7. Identification and Authentication Failures
8. Software and Data Integrity Failures
9. Security Logging and Monitoring Failures
10. Server-Side Request Forgery (SSRF)

**Usage:** Map CVEs to OWASP categories for web application context

---

### SANS Internet Storm Center

**URL:** https://isc.sans.edu/

**Application:** Real-time threat intelligence and early warning system

**Capabilities:**
- DShield distributed intrusion detection (honeypots worldwide)
- Daily threat dashboards (top attacking IPs, ports, countries)
- Handler diaries (expert analysis)
- Podcast and video threat briefings

**Use Case:** Real-time threat landscape monitoring, emerging threat identification

---

## Standards Integration

**When performing threat intelligence:**

1. **CVE Research:** NIST NVD (authoritative source) + CISA KEV (active exploitation) + EPSS (exploitability prediction)

2. **Threat Classification:** CWE (weakness category) + CVSS (severity) + OWASP (application context)

3. **Threat Behavior:** MITRE ATT&CK (tactics, techniques, mitigations)

4. **Real-Time Intelligence:** SANS ISC (emerging threats, attack trends)

**Prioritization Framework:**
```
Priority = (CVSS Score × 0.4) + (EPSS Score × 100 × 0.3) + (KEV Status × 10 × 0.3)

Where:
- CVSS Score: 0.0-10.0
- EPSS Score: 0.0-1.0 (multiply by 100 for weighting)
- KEV Status: 1 (in catalog) or 0 (not in catalog)
```

**Example:**
- CVE-2024-12345: CVSS 9.8, EPSS 0.92, KEV Yes
- Priority = (9.8 × 0.4) + (92 × 0.3) + (1 × 10 × 0.3) = 3.92 + 27.6 + 3.0 = **34.52** (CRITICAL)

---

**Related:**
- `methodologies/cve-research.md` - CVE research process using NVD/KEV/EPSS
- `methodologies/attck-mapping.md` - MITRE ATT&CK mapping methodology
- `workflows/threat-intelligence.md` - Complete workflow integrating all standards
- `templates/cve-research-report.md` - CVE report template with all metadata
