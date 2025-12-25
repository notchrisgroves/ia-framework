---
name: security-testing
description: Penetration testing, vulnerability scanning, and network segmentation testing with domain-specific methodologies. Use for security assessments.
async:
  safe: true
  parallel_safe: true
  phases:
    background:
      - explore          # Reconnaissance, scope parsing, attack surface mapping
      - scan             # Automated vulnerability scanning (vuln-scan mode)
      - qa               # Findings validation, CVSS verification
    foreground:
      - plan             # Requires user approval gate
      - code             # Active exploitation needs real-time decisions
      - commit           # Close-loop toggle requires user choice
  typical_duration:
    vuln_scan: 15-60min
    pentest_explore: 30-90min
    full_engagement: 4-8hrs
  background_invocation: |
    Task(subagent_type="security", run_in_background=true,
         prompt="/vuln-scan target OR /pentest --phase=explore")
---

# Security Testing Skill

**Auto-loaded when `security` agent invoked**

Unified security testing with 3 testing modes and 7 domain-specific methodologies. This skill acts as a decision tree router that selects the appropriate workflow + methodology combination based on user request and scope analysis.

**Core Philosophy:** Close-loop approach for self-hosted environments (find AND fix), report-only mode for bug bounty programs (find and report).

---

## 🚨 Critical Rules

**Before starting ANY engagement:**

1. **EXPLORE-PLAN-CODE-QA-COMMIT Enforced** - No testing without approved plan
2. **Scope Verification Mandatory** - Check scope before EVERY test
3. **Authorization Required** - Never test without written permission
4. **Real Examples Only** - Evidence-based findings, no fabrication
5. **Close-Loop Toggle** - Decide AFTER finding vulnerabilities: Fix (self-hosted) or Report (bug bounty)

**Scope Violations = Career Ending** - See `reference/SCOPE-COMPLIANCE-GUIDE.md`

**Tool Infrastructure:** VPS security servers with Docker deployment - See `../../servers/README.md` and `../../servers/SKILL-MAPPING.yaml` (VPS config in `.env`)

---

## Decision Tree: Testing Mode Selection

**Level 1: What TYPE of security work?**

### Mode 1: Penetration Testing (Full Exploitation)

**Detection Keywords:**
- User: "pentest", "penetration test", "exploit", "hack", "breach", "red team"
- Scope: "Full testing authorized", "Exploitation permitted", "Comprehensive assessment"

**Decision Path:** Penetration Testing → [Domain Detection] → Load workflow + methodology

**See:** [Domain Detection Logic](#domain-detection-penetration-testing) below

---

### Mode 2: Vulnerability Scanning (Detection Only)

**Detection Keywords:**
- User: "scan", "detect vulnerabilities", "identify issues", "vulnerability assessment"
- Scope: "Detection only", "No exploitation", "Scanning authorized"

**Decision Path:** Vulnerability Scanning → [Target Type Detection] → Load workflow

**Target Type Detection:**

| Target Format | Type | Workflow | Tools |
|---------------|------|----------|-------|
| `https://example.com`<br>`example.com` | Web Application | `workflows/vuln-scan.md` | nuclei, nikto, wpscan |
| `192.168.1.100`<br>`server.local` | Network Host | `workflows/vuln-scan.md` | nmap, nuclei, vulnerability scanners |
| `10.0.0.0/24`<br>`192.168.0.0/16` | IP Range (CIDR) | `workflows/vuln-scan.md` | nmap, masscan, nuclei |

**Characteristics:**
- NO exploitation - detection and reporting only
- Automated scanning with manual validation
- Faster than penetration testing (2-4 hours vs 4-8 hours)
- Deliverable: Vulnerability report with findings + remediation guidance

---

### Mode 3: Network Segmentation Testing

**Detection Keywords:**
- User: "segmentation", "isolation", "firewall rules", "VLAN", "network zones", "access controls"
- Scope: "Network architecture", "Segmentation validation", "Zone testing"

**Decision Path:** Segmentation Testing → Load workflow → Client engagement setup

**Workflow:** `workflows/segmentation-test.md`

**Characteristics:**
- Tests isolation between security zones (DMZ, Internal, Guest, Management)
- Validates firewall rules, VLANs, ACLs, routing policies
- Deliverable: Segmentation validation report with rule effectiveness analysis

---

## Domain Detection: Penetration Testing

**Level 2: What are we TESTING?**

### Domain 1: Network Infrastructure

**Detection Keywords:**
- "internal network", "servers", "IP range", "infrastructure", "firewall", "router", "switch"

**Scope Indicators:**
- IP addresses, CIDR ranges, network devices, internal infrastructure

**Routing:**
- **Methodology:** `methodologies/network/framework.md`
- **Workflow:** `workflows/pentest-init.md`
- **Foundation:** MITRE ATT&CK + NIST SP 800-115
- **Tools:** kali-pentest server (nmap, metasploit, responder, etc.)

**Key Test Areas:**
- Reconnaissance (passive + active)
- Initial access (exploitation, password attacks)
- Lateral movement
- Privilege escalation
- Persistence

---

### Domain 2: Web Application / API

**Detection Keywords:**
- "website", "web app", "web application", "API", "REST", "GraphQL", "HTTP", "HTTPS"

**Scope Indicators:**
- URLs, domains, web endpoints, API endpoints

**Routing:**
- **Methodology:** `methodologies/web-api/framework.md`
- **Workflow:** `workflows/pentest-init.md`
- **Foundation:** OWASP Top 10 + API Top 10 + ASVS + WSTG
- **Tools:** kali-pentest server (burp, nuclei, sqlmap, ffuf, etc.)

**Key Test Areas:**
- Broken access control (IDOR, privilege escalation)
- Injection (SQL, NoSQL, command, XSS)
- Authentication/authorization failures
- Cryptographic failures
- Server-side request forgery (SSRF)
- Business logic flaws

---

### Domain 3: Mobile Application

**Detection Keywords:**
- "mobile app", "iOS", "Android", "APK", "IPA", "mobile application"

**Scope Indicators:**
- Mobile applications, app stores, mobile API backends

**Routing:**
- **Methodology:** `methodologies/mobile/framework.md`
- **Workflow:** `workflows/pentest-init.md`
- **Foundation:** OWASP MASTG + MASVS
- **Tools:** mobile-security server (mobsf, frida, objection, etc.)

**Key Test Areas:**
- Insecure data storage
- Insecure communication
- Insecure authentication
- Code tampering
- Reverse engineering
- Insecure cryptography

---

### Domain 4: Smart Contracts (Web3)

**Detection Keywords:**
- "smart contract", "blockchain", "Ethereum", "Solidity", "DeFi", "Web3", "cryptocurrency"

**Scope Indicators:**
- Contract addresses, blockchain protocols, DeFi platforms

**Routing:**
- **Methodology:** `methodologies/web3/framework.md`
- **Workflow:** `workflows/pentest-init.md`
- **Foundation:** DeFiHackLabs + Immunefi Top 10
- **Tools:** web3-security server (slither, mythril, echidna, manticore, etc.)

**Key Test Areas:**
- Reentrancy attacks
- Oracle manipulation
- Flash loan attacks
- Access control issues
- Integer overflow/underflow
- Front-running vulnerabilities

---

### Domain 5: AI/LLM Systems

**Detection Keywords:**
- "AI", "LLM", "language model", "chatbot", "prompt injection", "model", "machine learning"

**Scope Indicators:**
- AI systems, language models, ML APIs, chatbots

**Routing:**
- **Methodology:** `methodologies/ai-llm/framework.md`
- **Workflow:** `workflows/pentest-init.md`
- **Foundation:** MITRE ATLAS + OWASP LLM Top 10 2025
- **Tools:** ai-security server (garak)

**Key Test Areas:**
- Prompt injection
- Sensitive data leakage
- Model extraction
- Training data poisoning
- Jailbreak techniques
- Plugin security

---

### Domain 6: Cloud Infrastructure

**Detection Keywords:**
- "AWS", "Azure", "GCP", "Google Cloud", "cloud", "S3", "IAM", "Lambda", "cloud infrastructure"

**Scope Indicators:**
- Cloud accounts, services, resources, cloud-native applications

**Routing (Level 3 - Cloud Provider Detection):**

| Provider | Keywords | Methodology | Tools |
|----------|----------|-------------|-------|
| **AWS** | "AWS", "S3", "EC2", "Lambda", "IAM" | `methodologies/cloud/aws-framework.md` | prowler (60+ CIS controls) |
| **Azure** | "Azure", "Entra", "AD", "Azure Functions" | `methodologies/cloud/azure-framework.md` | scoutsuite (90+ CIS controls) |
| **GCP** | "GCP", "Google Cloud", "Cloud Functions", "GKE" | `methodologies/cloud/gcp-framework.md` | scoutsuite (70+ CIS controls) |
| **Multi-cloud** | Multiple providers in scope | `methodologies/cloud/multi-cloud-framework.md` | prowler + scoutsuite |

**Workflow:** `workflows/pentest-init.md`
**Foundation:** CIS Benchmarks + Cloud security best practices
**Tools:** cloud-security server (prowler, scoutsuite)

**Key Test Areas:**
- IAM misconfigurations
- Public storage exposure
- Overly permissive security groups
- Missing encryption
- Compliance violations (CIS)
- Privilege escalation paths

---

### Domain 7: Active Directory

**Detection Keywords:**
- "Active Directory", "AD", "domain", "Kerberos", "LDAP", "Windows domain", "domain controller"

**Scope Indicators:**
- Windows domains, AD infrastructure, domain controllers

**Routing:**
- **Methodology:** `methodologies/active-directory/framework.md`
- **Workflow:** `workflows/pentest-init.md`
- **Foundation:** AD Security Assessment Framework + ATT&CK for Enterprise
- **Tools:** ad-security server (bloodhound, impacket, rubeus, etc.)

**Key Test Areas:**
- AD enumeration
- Kerberos attacks (Kerberoasting, AS-REP roasting)
- Privilege escalation (GPO abuse, delegation issues)
- Credential dumping
- Lateral movement
- Persistence mechanisms

---

## Routing Decision Matrix

**Quick reference table:**

| User Request | Testing Mode | Domain | Methodology | Workflow |
|--------------|-------------|--------|-------------|----------|
| "Pentest my web app" | Penetration Testing | Web/API | `methodologies/web-api/` | `workflows/pentest-init.md` |
| "Scan my network for vulnerabilities" | Vulnerability Scanning | N/A | N/A | `workflows/vuln-scan.md` |
| "Test firewall segmentation" | Segmentation Testing | N/A | N/A | `workflows/segmentation-test.md` |
| "Pentest AWS infrastructure" | Penetration Testing | Cloud (AWS) | `methodologies/cloud/aws/` | `workflows/pentest-init.md` |
| "Mobile app security test" | Penetration Testing | Mobile | `methodologies/mobile/` | `workflows/pentest-init.md` |
| "Smart contract audit" | Penetration Testing | Web3 | `methodologies/web3/` | `workflows/pentest-init.md` |

---

## Workflow Execution

**All workflows follow engagement mode selection:**

### Engagement Modes

| Mode | Use Case | Duration | Deliverables | Audit Logging |
|------|----------|----------|--------------|---------------|
| **Director** | Production pentests, bug bounties | 4-6 hours | Complete report + findings | ✅ Enabled (default) |
| **Mentor** | Training, learning by doing | 5-8 hours | Report + teaching notes | ✅ Enabled (default) |
| **Demo** | Tool testing, POC validation | 15-30 min | Minimal notes | ❌ Disabled (default) |

**Mode Selection:** Agent auto-detects from keywords OR presents 3-option dialog

---

## Model Selection

**Reference:** `library/model-selection-matrix.md` - Hook auto-detects escalation triggers and injects guidance.

**Default:** Sonnet | **Planning/Stuck:** Opus | **QA:** Grok | **OSINT:** Perplexity | **Validation:** Haiku

---

## Penetration Testing Workflow

**EXPLORE-PLAN-CODE-QA-COMMIT (5 Phases):**

### Phase 1: EXPLORE (No Testing)
- Read SCOPE.md, parse authorization + in-scope assets
- Validate credentials (.env lookup)
- Attack surface mapping
- Tool inventory check
- Methodology selection (auto-loaded based on domain)
- Passive reconnaissance (OSINT delegation)

**OSINT Delegation for Target Intelligence:**

```markdown
Load osint-research skill for pre-pentest reconnaissance.

**Caller:** security-testing
**Mode:** fast (quick recon) or deep (comprehensive profiling)

**Research Plan:**
- Target organization profile
- Technology stack identification
- Attack surface mapping
- Known vulnerabilities and incidents
- Public infrastructure details

**Output:** output/engagements/pentest/{target}/01-scope-and-reconnaissance/osint/

osint-research executes WebSearch + passive OSINT tools (NOT penetration testing).
```

**Note:** OSINT = passive only (no active scanning, no penetration testing)

**Gate:** ✅ Attack surface understood → Proceed to PLAN

---

### Phase 2: PLAN (Requires Approval)
- Generate scope-driven test plan
- Map test cases to methodology frameworks
- Tool assignment per test case
- Timeline estimation
- Risk assessment

**Template:** `templates/TEST-PLAN-TEMPLATE.md`

**Gate:** ⛔ **TEST PLAN APPROVAL REQUIRED** → Cannot proceed without approval

---

### Phase 3: CODE (Execute + Document)
- Execute approved test cases
- Document findings immediately (one file per vulnerability)
- Collect evidence (screenshots, requests, responses)
- Scope verification before EVERY test
- No testing if no vulnerability found

**Template:** `templates/FINDING-TEMPLATE.md`

**Gate:** ✅ All test cases executed → Proceed to QA

---

### Phase 4: QA (Findings Validation)
- Validate every finding for completeness
- Verify CVSS scores and CWE classifications
- Check evidence sufficiency
- Confirm scope compliance per finding
- Create qa-review.json

**Gate:** ✅ All findings validated → Proceed to COMMIT

---

### Phase 5: COMMIT (Close-Loop Toggle)

**Decision Point After Findings Discovered:**

| Choice | Mode | Activities | Deliverables |
|--------|------|------------|--------------|
| **A) YES - I own the infrastructure** | Close-Loop (Self-Hosted) | Handoff to remediation-engineer skill | Remediation tracker + verified fixes |
| **B) NO - External program** | Report-Only (Bug Bounty) | Generate bug bounty submission, format for HackerOne/Bugcrowd | Detachable findings ready to submit |

#### Close-Loop Handoff (Option A)

When user selects "YES - I own the infrastructure", generate structured handoff for `remediation-engineer` skill:

```json
{
  "finding_id": "VULN-YYYY-NNN",
  "cve": "CVE-XXXX-XXXXX",
  "severity": "CRITICAL|HIGH|MEDIUM|LOW",
  "targets": ["192.168.1.10", "192.168.1.11"],
  "detection_method": "pentest|vuln-scan|segmentation-test",
  "evidence": "output/engagements/.../evidence/",
  "engagement_dir": "output/engagements/..."
}
```

**Invoke remediation-engineer:**
```
The remediation-engineer skill will:
1. RESEARCH - CVE lookup, vendor advisories, patch availability
2. PROPOSAL - Generate fix proposal with approval gate
3. IMPLEMENTATION - Execute fix on PoC target (Wazuh API or SSH)
4. VALIDATION - Re-scan to verify fix
5. ROLLOUT - Apply to remaining targets
```

**Wazuh Integration:** If targets are Wazuh-managed, remediation uses Active Response API for automated patching.

**Templates:**
- Close-Loop: `templates/REMEDIATION-TRACKER-TEMPLATE.md`
- Report-Only: `templates/BUG-BOUNTY-SUBMISSION-TEMPLATE.md`

---

## Templates

**Professional templates in `templates/` directory:**

| Template | Purpose | Use Case |
|----------|---------|----------|
| `FINDING-TEMPLATE.md` | Self-contained vulnerability documentation | All findings |
| `TEST-PLAN-TEMPLATE.md` | Scope-driven test plan | Phase 2 PLAN |
| `PENTEST-REPORT-TEMPLATE.md` | PTES-compliant full report | Final deliverable |
| `BUG-BOUNTY-SUBMISSION-TEMPLATE.md` | Platform-ready submissions | Bug bounty programs |
| `REMEDIATION-TRACKER-TEMPLATE.md` | Lifecycle tracking (FIND → FIX → VERIFY → CLOSE) | Close-loop mode only |

---

## Reference Documentation

**Critical guides in `reference/` directory:**

| Document | Purpose |
|----------|---------|
| `SCOPE-COMPLIANCE-GUIDE.md` | Scope violation prevention (real HackerOne examples) |
| `PREREQUISITES.md` | Environment setup requirements |
| `PRE-ENGAGEMENT-CHECKLIST.md` | Pre-flight validation checklist |
| `AUDIT-MODE-DOCUMENTATION.md` | Compliance logging (SOC 2, ISO 27001, PCI DSS) |
| `CLEANUP-QUICKREF.md` | Post-engagement cleanup procedures |

---

## Tools

**Security tools available via VPS Docker wrappers (`servers/` directory):**

| Server | Domain | Status |
|--------|--------|--------|
| `kali-pentest` | Network, Web/API | ✅ Deployed |
| `mobile-security` | Mobile apps | ✅ Deployed |
| `web3-security` | Smart Contracts | ✅ Deployed |
| `cloud-security` | Cloud (AWS/GCP/Azure) | ✅ Deployed |
| `ai-security` | AI/LLM | ✅ Deployed |
| `ad-security` | Active Directory | ✅ Deployed |
| `playwright` | Web/API automation | ✅ Deployed |

**Tool discovery:** Agent verifies availability during EXPLORE phase via `servers/*/wrappers/index.py`

---

## Authorization Protocol

**MANDATORY before ANY testing:**

1. Verify written authorization exists (SCOPE.md, bug bounty program, contract)
2. Parse scope boundaries (in-scope assets, out-of-scope restrictions)
3. Document authorization in session file

**Authorization Sources:**
- ✅ HackerOne API (program active + scope accessible)
- ✅ SCOPE.md with authorization section
- ✅ Safe targets (HackTheBox, TryHackMe, scanme.nmap.org)

**SCOPE.md = Authorization** - If scope document exists with authorization details, testing is authorized. Follow scope EXPLICITLY.

---

## Common Scenarios (Quick Reference)

| Request | Mode | Domain | Workflow |
|---------|------|--------|----------|
| "Pentest web app" | Pentest | Web/API | `workflows/pentest-init.md` |
| "Quick network scan" | Vuln Scan | Network | `workflows/vuln-scan.md` |
| "Test firewall rules" | Segmentation | N/A | `workflows/segmentation-test.md` |
| "Audit smart contracts" | Pentest | Web3 | `workflows/pentest-init.md` |

**Version:** 1.0.0 | **Updated:** 2025-12-19 | **Status:** Decision tree + model escalation
