# Threat Modeling Methodology

**Progressive context file - Load only when conducting threat modeling**

This document covers threat modeling methodologies for architecture security reviews.

---

## Overview

Threat modeling is the systematic identification of threats, attack vectors, and security weaknesses in system architectures. It must be conducted for ALL architecture reviews.

**Primary Methodologies:**
1. **STRIDE** - Comprehensive threat categorization (Microsoft)
2. **PASTA** - Risk-centric threat analysis (7-stage process)
3. **Attack Trees** - Visual attack path modeling
4. **MITRE ATT&CK** - Threat-informed architecture design

**When to use each:**
- **STRIDE** - Default for most architecture reviews (comprehensive, systematic)
- **PASTA** - Risk-driven reviews with business impact analysis
- **Attack Trees** - Complex attack path analysis, red team exercises
- **MITRE ATT&CK** - Threat actor-informed design, high-risk environments

---

## STRIDE Methodology

**STRIDE** = Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege

### Process

**Step 1: Decompose Architecture (30 min)**
- Identify trust boundaries (external, internal, privileged)
- Map data flows (input/output, processing, storage)
- Document assets (data, services, credentials, keys)
- Identify entry points (APIs, UIs, integrations)

**Step 2: Apply STRIDE Categories (45-60 min)**

| STRIDE Category | Definition | Example Threats | Mitigations |
|---|---|---|---|
| **Spoofing** | Pretending to be someone/something else | User impersonation, IP spoofing, certificate forgery | MFA, mutual TLS, strong authentication |
| **Tampering** | Modifying data or code | Man-in-the-middle, database tampering, code injection | Encryption in transit, integrity checks, signed code |
| **Repudiation** | Denying actions | User claims "I didn't do that", missing audit logs | Comprehensive logging, digital signatures, audit trails |
| **Information Disclosure** | Exposing information to unauthorized users | Data leaks, credential exposure, error messages | Encryption at rest, access controls, secure error handling |
| **Denial of Service** | Making system unavailable | Resource exhaustion, DDoS, logic bombs | Rate limiting, auto-scaling, failover |
| **Elevation of Privilege** | Gaining unauthorized permissions | Privilege escalation, insecure defaults, IDOR | Least privilege, role-based access, authorization checks |

**Step 3: Identify Attack Vectors (30 min)**
- External network attacks (internet-facing services)
- Internal network attacks (lateral movement)
- Supply chain attacks (dependencies, third-party code)
- Social engineering (phishing, credential theft)
- Physical access (insider threats, device theft)

**Step 4: Document Threats (30 min)**
- Threat ID, category (STRIDE), severity (Critical/High/Medium/Low)
- Attack scenario description
- Affected components
- Existing mitigations (if any)
- Recommended mitigations

**Step 5: Prioritize with DREAD (optional, 15 min)**

**DREAD Scoring** (1-10 scale):
- **D**amage - How bad would an attack be?
- **R**eproducibility - How easy is it to reproduce?
- **E**xploitability - How much effort to launch attack?
- **A**ffected Users - How many users impacted?
- **D**iscoverability - How easy to find vulnerability?

**Total Time:** 2-3 hours for comprehensive STRIDE threat model

---

## PASTA Methodology

**PASTA** = Process for Attack Simulation and Threat Analysis (7 stages, risk-centric)

### 7-Stage Process

**Stage 1: Define Objectives (30 min)**
- Business impact analysis
- Compliance requirements (PCI DSS, HIPAA, GDPR)
- Security objectives (confidentiality, integrity, availability)

**Stage 2: Define Technical Scope (30 min)**
- Architecture boundaries
- Technology stack
- Dependencies and integrations
- Data flows

**Stage 3: Application Decomposition (45 min)**
- Use cases and user roles
- Data flow diagrams (DFD)
- Trust boundaries
- Entry/exit points

**Stage 4: Threat Analysis (60 min)**
- Threat intelligence (MITRE ATT&CK, CVE databases)
- Threat actor profiles (nation-state, cybercrime, insider)
- Attack scenarios specific to architecture

**Stage 5: Vulnerability and Weakness Analysis (60 min)**
- Code-level vulnerabilities (OWASP Top 10)
- Design flaws (missing authentication, weak crypto)
- Configuration weaknesses (default credentials, open ports)

**Stage 6: Attack Modeling (60 min)**
- Attack trees for high-value assets
- Attack surface analysis
- Exploit path mapping

**Stage 7: Risk and Impact Analysis (45 min)**
- Business impact (financial, reputational, regulatory)
- Likelihood assessment
- Risk prioritization matrix
- Mitigation roadmap

**Total Time:** 5-6 hours for comprehensive PASTA threat model

**When to use PASTA:**
- Business-critical applications
- Regulatory compliance requirements
- Executive reporting needs (risk-based narrative)
- Post-incident architecture reviews

---

## Attack Trees Methodology

**Attack Trees** = Visual hierarchical models of attack paths

### Process

**Step 1: Identify High-Value Assets (15 min)**
- Customer data, credentials, financial data, intellectual property

**Step 2: Define Root Goal (10 min)**
- Example: "Exfiltrate customer PII database"

**Step 3: Decompose Attack Paths (60-90 min)**
- **AND nodes** - All child nodes required (e.g., "Gain access AND escalate privileges")
- **OR nodes** - Any child node sufficient (e.g., "Phish credentials OR exploit SQL injection")

**Example Attack Tree:**
```
Root: Exfiltrate Customer PII Database
├── OR: Gain Database Access
│   ├── AND: SQL Injection
│   │   ├── Find injectable parameter
│   │   └── Bypass input validation
│   ├── AND: Stolen Credentials
│   │   ├── OR: Phishing
│   │   │   ├── Spear phishing email
│   │   │   └── Credential harvesting site
│   │   └── OR: Credential Stuffing
│   │       └── Use leaked password lists
│   └── AND: Exploit RCE Vulnerability
│       ├── Find unpatched CVE
│       └── Execute reverse shell
└── AND: Exfiltrate Data
    ├── OR: Network Egress
    │   ├── HTTPS exfiltration
    │   └── DNS tunneling
    └── Avoid Detection
        ├── Disable logging
        └── Use encrypted channel
```

**Step 4: Assign Likelihood & Impact (30 min)**
- Each leaf node: Likelihood (High/Medium/Low), Impact (Critical/High/Medium/Low)
- Calculate path risk scores

**Step 5: Identify Mitigations (30 min)**
- Map security controls to attack tree nodes
- Identify coverage gaps

**Total Time:** 2-3 hours for attack tree analysis

**When to use Attack Trees:**
- Red team exercises
- Complex attack path analysis
- Visual communication with executives/stakeholders
- Identifying critical control gaps

---

## MITRE ATT&CK-Based Threat Modeling

**ATT&CK** = Adversarial Tactics, Techniques, and Common Knowledge

### Process

**Step 1: Identify Threat Actors (30 min)**
- Nation-state APTs (Lazarus, APT29, APT41)
- Cybercrime groups (ransomware, banking trojans)
- Insider threats
- Hacktivists

**Step 2: Map Relevant ATT&CK Tactics (45 min)**

**14 ATT&CK Tactics (Enterprise):**
1. Reconnaissance - Gather information (OSINT, network scanning)
2. Resource Development - Acquire infrastructure (C2 servers, domains)
3. Initial Access - Get foothold (phishing, public-facing apps)
4. Execution - Run malicious code (scripts, executables)
5. Persistence - Maintain access (backdoors, scheduled tasks)
6. Privilege Escalation - Gain higher permissions (exploit vulnerabilities, credential abuse)
7. Defense Evasion - Avoid detection (obfuscation, disable logging)
8. Credential Access - Steal credentials (credential dumping, keylogging)
9. Discovery - Understand environment (network scanning, account discovery)
10. Lateral Movement - Move through network (remote services, pass-the-hash)
11. Collection - Gather data (screen capture, data staging)
12. Command and Control - Communicate with attacker infrastructure (C2 channels)
13. Exfiltration - Steal data (network exfiltration, cloud storage)
14. Impact - Disrupt operations (data destruction, ransomware)

**Step 3: Identify Techniques for Architecture (60 min)**
- Map architecture components to ATT&CK techniques
- Example: "Web application" → T1190 (Exploit Public-Facing Application), T1505.003 (Web Shell)

**Step 4: Validate Mitigations (45 min)**
- Check if architecture implements ATT&CK mitigations (M-codes)
- Example: M1050 (Exploit Protection), M1026 (Privileged Account Management)

**Step 5: Generate ATT&CK Navigator Layer (30 min)**
- Visual heatmap of relevant techniques
- Export JSON for documentation

**Total Time:** 3-4 hours for ATT&CK-based threat model

**When to use ATT&CK:**
- High-risk environments (critical infrastructure, defense, finance)
- Threat actor-informed design
- Red team collaboration
- Detection engineering alignment

---

## Threat Modeling Deliverables

### Required Outputs

**1. Threat Register**
- Threat ID, category (STRIDE/ATT&CK), severity
- Attack scenario description
- Affected components
- Existing mitigations
- Recommended mitigations
- Risk score (if DREAD/PASTA used)

**2. Threat Model Diagram**
- Architecture diagram with threat annotations
- Trust boundaries highlighted
- Attack vectors marked
- Data flow security controls

**3. Mitigation Roadmap**
- Prioritized list of security improvements
- Implementation effort estimates
- Risk reduction impact
- Standards references (NIST, OWASP, CSA)

**4. Executive Summary**
- High-level threats (business language)
- Risk summary (Critical/High/Medium/Low counts)
- Top recommendations (3-5 actionable items)

---

## Common Mistakes to Avoid

**❌ Skipping threat modeling**
- Never approve architecture without threat identification
- Even "simple" architectures have threats

**❌ Generic threats without context**
- Bad: "SQL injection is possible"
- Good: "User input in search API (line 42) not parameterized → SQL injection → database compromise"

**❌ Missing trust boundaries**
- Always identify where data crosses security zones
- Internet → DMZ → Internal → Database

**❌ No prioritization**
- Not all threats are equal
- Use DREAD, CVSS, or business impact scoring

**❌ Mitigation-only (no threat identification)**
- Don't jump to "add firewall" without identifying specific threats
- Understand attack scenarios first

---

## Standards Integration

**NIST SP 800-160 Vol. 1** - Systems security engineering framework (threat modeling in Section 3.4)

**OWASP ASVS** - Architecture requirements (V1: Architecture, Design and Threat Modeling)

**CSA Cloud Security Guidance** - Cloud-specific threat modeling considerations

**See:** `reference/standards.md` for complete framework details

---

## Quick Reference - Methodology Selection

| Scenario | Recommended Methodology | Time Estimate |
|---|---|---|
| General web application | STRIDE | 2-3 hours |
| Cloud microservices | STRIDE + ATT&CK | 3-4 hours |
| High-risk/regulated | PASTA | 5-6 hours |
| Red team planning | Attack Trees + ATT&CK | 3-4 hours |
| Zero trust architecture | STRIDE + ATT&CK | 3-4 hours |
| Legacy system modernization | STRIDE + PASTA | 6-8 hours |

---

**Version:** 2.0
**Last Updated:** 2025-12-02
**Framework:** STRIDE, PASTA, Attack Trees, MITRE ATT&CK
