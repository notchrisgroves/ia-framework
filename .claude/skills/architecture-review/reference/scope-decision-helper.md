# Architecture Review - Scope Decision Helper

**Use this guide to determine when to use architecture-review vs other skills**

---

## Quick Decision Tree

### Q1: Are you reviewing SYSTEM DESIGN / ARCHITECTURE?

**NO** → Not architecture-review
- Source code → **code-review** skill
- Configuration files → **secure-config** skill
- Active testing → **security-testing** skill
- Dependencies → **dependency-audit** skill
- CVE research → **threat-intel** skill

**YES** → Continue to Q2

---

### Q2: What stage are you in?

**Design phase** (before code is written) → **architecture-review** ✅

**Implementation phase** (code exists) → **code-review** ✅ (or both)

**Deployment phase** (infrastructure config) → **secure-config** ✅

**Testing phase** (active exploitation) → **security-testing** ✅

---

### Q3: What type of review?

**Threat modeling, attack paths, design flaws** → **architecture-review** ✅

**Code-level vulnerabilities (SQL injection, XSS)** → **code-review** ✅

**Network segmentation, firewall rules** → **secure-config** ✅ or **architecture-review** ✅ (high-level)

**Active penetration testing** → **security-testing** ✅

---

## Use Architecture Review For

### ✅ System Design Security Analysis

**When:**
- Reviewing architecture diagrams for security weaknesses
- Threat modeling applications and systems (STRIDE, PASTA, ATT&CK)
- Evaluating microservices, cloud architectures, enterprise systems
- Validating secure design patterns and principles

**Examples:**
- "Threat model this microservices architecture"
- "Review authentication design for security flaws"
- "Validate zero trust architecture implementation"
- "Evaluate API gateway security design"
- "Review cloud architecture for security weaknesses"

**Standards:** NIST SP 800-160, OWASP ASVS V1 (Architecture), CSA Cloud Security

---

### ✅ Defense-in-Depth Validation

**When:**
- Assessing layered security controls across architecture
- Identifying single points of failure
- Reviewing security zone segmentation (high-level)
- Validating fail-safe and fail-secure mechanisms

**Examples:**
- "Evaluate defense-in-depth for payment processing system"
- "Identify single points of failure in architecture"
- "Review security zone design (DMZ, internal, restricted)"
- "Validate fail-safe mechanisms in authentication"

**Standards:** NIST SP 800-160 Appendix D (Defense in Depth)

---

### ✅ Architecture Compliance Review

**When:**
- Validating NIST SP 800-160 systems security engineering compliance
- Checking OWASP ASVS architecture requirements (L1/L2/L3)
- Reviewing CSA cloud security guidance compliance
- Validating Zero Trust Architecture (NIST SP 800-207)

**Examples:**
- "Review architecture for NIST SP 800-160 compliance"
- "Validate OWASP ASVS L2 architecture requirements"
- "Check zero trust architecture implementation"
- "Evaluate cloud architecture against CSA guidance"

**Standards:** NIST SP 800-160, OWASP ASVS, CSA, NIST SP 800-207

---

## Use Other Skills For

### ❌ Source Code Vulnerability Analysis

**Use:** `/code-review` (code-review skill)

**When:**
- Analyzing source code for vulnerabilities
- Checking for SQL injection, XSS, CSRF in code
- Reviewing secure coding standards compliance
- Validating input validation and output encoding

**Examples:**
- "Review this authentication module for vulnerabilities"
- "Check this API code for SQL injection"
- "Analyze this React component for XSS vulnerabilities"
- "Review this Python code for secure coding issues"

**Why not architecture-review:** Code-review operates at source code level, architecture-review at design level

---

### ❌ Active Penetration Testing

**Use:** `/pentest` (security-testing skill)

**When:**
- Actively exploiting vulnerabilities
- Conducting penetration tests
- Validating security controls through testing
- Attempting to breach systems

**Examples:**
- "Test this web application for exploitable bugs"
- "Attempt to bypass authentication on admin portal"
- "Conduct penetration test on internal network"
- "Test API for vulnerabilities"

**Why not architecture-review:** Security-testing is active exploitation, architecture-review is design analysis

---

### ❌ Infrastructure Configuration Hardening

**Use:** `/secure-config` (secure-config skill)

**When:**
- Hardening Linux/Windows servers
- Reviewing firewall rule configurations
- Applying CIS benchmarks or DISA STIGs
- Validating infrastructure-as-code security

**Examples:**
- "Harden this Linux server configuration"
- "Review these firewall rules for security"
- "Apply CIS benchmark to Kubernetes cluster"
- "Validate Terraform security configurations"

**Why not architecture-review:** Secure-config operates at configuration file level, architecture-review at high-level design

---

### ❌ Dependency Vulnerability Scanning

**Use:** `/dependency-audit` (dependency-audit skill)

**When:**
- Scanning dependencies for known vulnerabilities
- Generating SBOMs (Software Bill of Materials)
- Assessing supply chain risk
- Reviewing third-party library security

**Examples:**
- "Scan npm dependencies for vulnerabilities"
- "Generate SBOM for this application"
- "Review third-party library security risks"
- "Audit Python dependencies for CVEs"

**Why not architecture-review:** Dependency-audit focuses on supply chain, architecture-review on design

---

### ❌ CVE Research and Threat Intelligence

**Use:** `/threat-intel` (threat-intel skill)

**When:**
- Researching specific CVEs
- Analyzing threat landscape
- Mapping threats to MITRE ATT&CK
- Gathering vulnerability intelligence

**Examples:**
- "Research CVE-2024-1234 impact and mitigations"
- "Analyze threat actors targeting financial sector"
- "Map ransomware TTPs to MITRE ATT&CK"
- "Identify vulnerabilities in Apache web server"

**Why not architecture-review:** Threat-intel focuses on vulnerability research, architecture-review on design security

---

## Overlap Scenarios

### Scenario 1: "Review authentication for security"

**Ambiguous** - Could be architecture or code review

**Clarify:**
- **Design-level** (flow diagrams, OAuth vs SAML decision) → architecture-review
- **Implementation-level** (actual code with password hashing) → code-review
- **Both** → Start with architecture-review, then code-review

---

### Scenario 2: "Review network segmentation"

**Ambiguous** - Could be architecture or secure-config

**Clarify:**
- **High-level design** (DMZ architecture, security zones) → architecture-review
- **Firewall rule configuration** (specific iptables rules) → secure-config
- **Both** → Start with architecture-review (design), then secure-config (implementation)

---

### Scenario 3: "Threat model this API"

**Architecture-review** ✅

**Why:** Threat modeling is a design-level activity (STRIDE, PASTA, ATT&CK) that identifies threats before/alongside implementation

---

### Scenario 4: "Test this API for vulnerabilities"

**Security-testing** ✅

**Why:** Active testing/exploitation, not design analysis

---

### Scenario 5: "Review cloud architecture diagrams"

**Architecture-review** ✅

**Why:** Analyzing architecture diagrams for security weaknesses is core architecture-review activity

---

## Still Unsure?

### If you have ARCHITECTURE DIAGRAMS → architecture-review

### If you have SOURCE CODE → code-review

### If you need THREAT MODELING → architecture-review

### If you need ACTIVE TESTING → security-testing

### If you have CONFIG FILES → secure-config

### If you need CVE RESEARCH → threat-intel

---

## Related Documentation

- **Architecture Review:** `skills/architecture-review/SKILL.md`
- **Code Review:** `skills/code-review/SKILL.md`
- **Secure Config:** `skills/secure-config/SKILL.md`
- **Security Testing:** `skills/security-testing/SKILL.md`
- **Dependency Audit:** `skills/dependency-audit/SKILL.md`
- **Threat Intel:** `skills/threat-intel/SKILL.md`

---

**Version:** 2.0
**Last Updated:** 2025-12-02
