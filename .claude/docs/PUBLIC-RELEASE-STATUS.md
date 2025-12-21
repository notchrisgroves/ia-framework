# Public Release Status

**Purpose:** Track which framework components are ready for public release
**Used by:** `/public-sync`, ia-setup-guide page, `.framework-manifest.yaml`

---

## Release Status Legend

| Status | Meaning |
|--------|---------|
| ✅ Public | Validated and included in public repo |
| 🧪 Testing | Internal testing before public release |
| 🔒 Private | Will remain private (personal/infrastructure-specific) |

---

## Skills

| Skill | Agent | Status | Notes |
|-------|-------|--------|-------|
| create-skill | meta | ✅ Public | Template system for creating new skills |
| career | advisor | ✅ Public | Job analysis, mentorship, CliftonStrengths |
| osint-research | advisor | ✅ Public | Dual-source research (support skill) |
| qa-review | advisor | ✅ Public | Multi-model review (support skill) |
| code-review | security | ✅ Public | Security-focused code analysis |
| architecture-review | security | ✅ Public | Threat modeling, STRIDE/PASTA |
| security-testing | security | ✅ Public | Pentest, vuln-scan, segmentation |
| security-advisory | security | ✅ Public | Risk assessments, security guidance |
| threat-intel | security | ✅ Public | CVE research, MITRE ATT&CK |
| dependency-audit | security | ✅ Public | SBOM, supply chain security |
| secure-config | security | ✅ Public | CIS/STIG hardening validation |
| benchmark-generation | security | ✅ Public | Compliance script generation |
| legal | legal | ✅ Public | Compliance with citation verification |
| writer | writer | ✅ Public | Blog, docs, reports |
| diagram-generation | writer | ✅ Public | Mermaid diagram export |
| gitingest-repo | meta | ✅ Public | GitHub repo ingestion |
| personal-training | advisor | ✅ Public | Fitness programming |
| health-wellness | advisor | ✅ Public | Alternative health reference |
| remediation-engineer | security | 🧪 Testing | Wazuh integration, fix proposals |
| infrastructure-ops | infra | 🔒 Private | VPS management, personal infra |

---

## Commands

| Command | Skill | Status | Notes |
|---------|-------|--------|-------|
| /job-analysis | career | ✅ Public | Job application workflow |
| /mentorship | career | ✅ Public | Skill building and learning roadmaps |
| /clifton | career | ✅ Public | CliftonStrengths coaching |
| /code-review | code-review | ✅ Public | Security code analysis |
| /arch-review | architecture-review | ✅ Public | Architecture security review |
| /threat-intel | threat-intel | ✅ Public | CVE and threat research |
| /dependency-audit | dependency-audit | ✅ Public | Supply chain analysis |
| /secure-config | secure-config | ✅ Public | Hardening validation |
| /benchmark-gen | benchmark-generation | ✅ Public | Compliance scripts |
| /pentest | security-testing | ✅ Public | Penetration testing |
| /vuln-scan | security-testing | ✅ Public | Vulnerability scanning |
| /segmentation-test | security-testing | ✅ Public | Network segmentation |
| /risk-assessment | security-advisory | ✅ Public | Formal risk assessment |
| /security-advice | security-advisory | ✅ Public | Ad-hoc security guidance |
| /compliance | legal | ✅ Public | Legal compliance review |
| /policy | security-advisory | ✅ Public | Multi-framework policy generation |
| /blog-post | writer | ✅ Public | Blog content creation |
| /newsletter | writer | ✅ Public | Weekly digest |
| /generate-image | writer | ✅ Public | FLUX hero images |
| /diagram | diagram-generation | ✅ Public | Diagram generation and export |
| /training | personal-training | ✅ Public | Fitness program design |
| /wellness | health-wellness | ✅ Public | Alternative health reference |
| /ingest-repo | gitingest-repo | ✅ Public | GitHub repository ingestion |
| /git-sync | infra | 🔒 Private | Private repo workflow |
| /public-sync | infra | 🔒 Private | Public repo publishing |

---

## Agents

| Agent | Status | Notes |
|-------|--------|-------|
| security | ✅ Public | Routes to security skills |
| writer | ✅ Public | Routes to content skills |
| advisor | ✅ Public | Routes to career/research/wellness skills |
| legal | ✅ Public | Routes to legal skill |

---

## Server Wrappers

| Server Category | Status | Notes |
|-----------------|--------|-------|
| servers/utils/vps_utils.py | ✅ Public | Core SSH/Docker utilities, configurable via .env |
| servers/SETUP-GUIDE.md | ✅ Public | Agent-driven deployment instructions |
| servers/ARCHITECTURE.md | ✅ Public | Architecture documentation (IPs transformed) |
| servers/kali-pentest/ | ✅ Public | Network/web pentest tool wrappers |
| servers/web3-security/ | ✅ Public | Smart contract security wrappers |
| servers/mobile-security/ | ✅ Public | Mobile app analysis wrappers |
| servers/metasploit/ | ✅ Public | Exploitation framework wrapper |
| tools/openrouter/ | ✅ Public | Multi-model AI access |
| tools/context7/ | ✅ Public | Documentation context tool |
| servers/ghost-blog/ | 🔒 Private | Blog-specific integration |
| servers/n8n/ | 🔒 Private | Automation-specific |
| servers/wazuh/ | 🔒 Private | Security monitoring |
| servers/reaper/ | 🔒 Private | Traffic analysis (complex setup) |

---

## Resources Library

| Resource Category | Status | Notes |
|-------------------|--------|-------|
| resources/library/README.md | ✅ Public | Library structure documentation |
| resources/library/repositories/ | ✅ Public | OWASP, MITRE gitingest text files |
| resources/library/threat-intelligence/ | ✅ Public | CVE, CWE, CISA KEV data |
| resources/library/benchmarks/ | ✅ Public | CIS Benchmarks (public downloads) |
| resources/library/frameworks/ | ✅ Public | NIST, PCI-DSS, OWASP frameworks |
| resources/library/books/ | ✅ Public | Placeholder with README (users add their own copies) |

**Note:** Users can use `/ingest-repo` command to fetch additional content.

---

## Release Criteria

**To move from 🧪 Testing → ✅ Public:**
1. Skill decision tree validated
2. All workflows tested end-to-end
3. No hardcoded paths or personal references
4. Reference materials reviewed for public appropriateness
5. Scripts tested without private infrastructure
6. Added to `.framework-manifest.yaml` include list
7. `/public-sync` executed successfully

**Server-specific criteria:**
1. Uses configurable .env variables (no hardcoded IPs)
2. Works with any VPS provider
3. SETUP-GUIDE.md explains agent-driven deployment
4. Transformations remove personal paths on public-sync

---

**Last Updated:** 2025-12-19
**Maintained by:** /public-sync command
