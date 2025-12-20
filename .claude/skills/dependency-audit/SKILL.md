---
name: dependency-audit
description: Supply chain security analysis with SBOM generation (SPDX/CycloneDX), CVE verification against NIST NVD, and SLSA maturity assessment. Use for dependency vulnerability scanning, transitive dependency analysis, license compliance, and third-party vendor security evaluation.
---

# Dependency Audit Skill

**Auto-loaded when `security` agent invoked for supply chain security**

Specialized in identifying dependency vulnerabilities, generating Software Bills of Materials (SBOMs), and assessing third-party component risks using NIST SP 800-161, SLSA framework, and NTIA minimum elements.

**Core Philosophy:** Verified vulnerabilities only. All CVE claims must be verified against NIST NVD. SBOM generation is mandatory for all audits (EO 14028 compliance).

---

## 🚀 Quick Access

**Slash Command:** `/dependency-audit`

Supply chain security analysis with dependency vulnerability scanning and SBOM generation.

**See:** `commands/dependency-audit.md` for complete workflow

---

## 🚨 Critical Rules

**Before starting any dependency audit:**

1. **Load Context First** - Read CLAUDE.md → SKILL.md → Load methodologies and references as needed
2. **SBOM Generation Required** - All audits must produce SPDX or CycloneDX SBOM with NTIA minimum elements (enables ongoing vulnerability tracking and EO 14028 compliance)
3. **Checkpoint After Each Phase** - Update session file after major phases (inventory, vulnerability scan, SBOM generation, risk assessment, remediation) with CVE IDs verified and SBOM location
4. **CVE Verification Mandatory** - All vulnerability claims must have verified CVE IDs from NIST NVD (prevents false positives, maintains audit credibility)
5. **SLSA Level Assessment** - All supply chain reviews must assess SLSA maturity level (L0-L4) for critical dependencies (provides actionable improvement path)

**Refresh Trigger:** If conversation exceeds 3 hours OR after 5+ dependency groups audited, refresh rules.

---

## Progressive Context Loading

**Core Context (Always Loaded):**
- This SKILL.md file
- When to use vs other skills

**Extended Context (Load as Needed):**
- `methodologies/supply-chain-analysis.md` - NIST SP 800-161, SLSA framework, CVE verification, dependency risk assessment, transitive dependency analysis
- `methodologies/sbom-generation.md` - SPDX vs CycloneDX, NTIA minimum elements, license identification, vulnerability mapping, SBOM validation
- `reference/standards.md` - NIST SP 800-161, SLSA, SPDX, CycloneDX, NTIA, NVD, GitHub Advisory Database, OSV, EPSS, license compliance, EO 14028
- `workflows/dependency-audit-workflow.md` - Complete 5-phase workflow (EXPLORE → PLAN → CODE → CODE → COMMIT)
- `templates/audit-report.md` - Comprehensive dependency audit report template

---

## Model Selection

**Reference:** `library/model-selection-matrix.md` for complete task-to-model mapping

**Default:** Latest Sonnet (dependency graph analysis, CVE research, risk prioritization, SBOM generation)
**Downgrade to Haiku:** Simple CVE lookup, SBOM format conversion, single package queries
**Upgrade to Opus:** Novel supply chain attack analysis, strategic dependency architecture decisions

**Dynamic Selection:** `tools/research/openrouter/fetch_models.py` for latest versions

---

## When to Use

✅ **Use dependency-audit for:**
- Identify CVEs in project dependencies (npm, pip, Maven, Go modules, etc.)
- Analyze transitive dependency vulnerabilities (dependencies of dependencies)
- Prioritize patching based on exploitability (EPSS scores)
- Verify CVE IDs against NIST NVD (prevent false positives)
- Generate SPDX 2.3 or CycloneDX 1.5 SBOMs
- Component inventory with version tracking
- License compliance analysis (GPL, MIT, Apache compatibility)
- NTIA minimum elements validation (EO 14028 compliance)
- SLSA maturity level assessment (L0-L4 build provenance)
- Third-party vendor security evaluation (maintainer trust)
- Dependency provenance validation
- Supply chain attack surface analysis (typosquatting, abandoned packages)
- Automated CVE scanning setup (Dependabot, Snyk, OWASP Dependency-Track)
- SBOM maintenance and updates
- Quarterly supply chain reviews

❌ **Don't use if:**
- Source code vulnerability analysis (SQL injection, XSS in YOUR code) → Use `/code-review` (code-review skill)
- System configuration hardening (CIS benchmarks, DISA STIGs) → Use `/secure-config` (secure-config skill)
- CVE research for systems (OS, services - not dependencies) → Use `/threat-intel` (threat-intel skill)
- Active penetration testing (exploitation, post-exploitation) → Use `/pentest` (security-testing skill)
- Architecture threat modeling (STRIDE, data flow diagrams) → Use `/arch-review` (architecture-review skill)

---

## Decision Helper

**"Should I use dependency-audit or another skill?"**

**Q1: What are you analyzing?**
- **Third-party libraries/packages** (package.json, requirements.txt, pom.xml) → dependency-audit ✅
- **Your own source code** → code-review ✅
- **System architecture** → architecture-review ✅
- **Server configuration** → secure-config ✅

**Q2: What are you looking for?**
- CVEs in dependencies (libraries, packages) → dependency-audit ✅
- Vulnerabilities in your code (SQL injection, XSS) → code-review ✅
- System CVEs (OS, Apache, nginx) → threat-intel ✅
- Configuration weaknesses (default passwords, open ports) → secure-config ✅

**Q3: What do you want to produce?**
- SBOM (Software Bill of Materials) → dependency-audit ✅
- Security code review report → code-review ✅
- Threat model (STRIDE, attack trees) → architecture-review ✅
- Configuration hardening report → secure-config ✅

**Examples:**
- "Scan npm dependencies for vulnerabilities" → dependency-audit ✅
- "Generate SBOM for this Python project" → dependency-audit ✅
- "Assess supply chain risk for vendor X" → dependency-audit ✅
- "Check if log4j vulnerability affects my dependencies" → dependency-audit ✅
- "Review authentication code for SQL injection" → code-review ✅
- "Research CVE-2024-1234" → threat-intel ✅
- "Harden Linux server configuration" → secure-config ✅
- "Test application for vulnerabilities" → security-testing ✅

---

## Workflow: EXPLORE → PLAN → CODE → CODE → COMMIT

**Total Duration:** 6-10 hours (depending on project size and dependency count)

### Phase 1: EXPLORE - Dependency Discovery (1-2 hours)

**Goal:** Build complete inventory of direct and transitive dependencies

**Actions:**
1. Identify dependency manifests (package.json, requirements.txt, pom.xml, Cargo.toml, go.mod)
2. Parse lock files (package-lock.json, Pipfile.lock, go.sum - preferred for exact versions)
3. Build dependency tree (direct + transitive, identify depth)
4. Catalog components (name, version, ecosystem, license, last updated)

**Tools:**
```bash
npm list --all > dependency-tree.txt  # JavaScript
pipdeptree > dependency-tree.txt      # Python
mvn dependency:tree                   # Maven
go mod graph                          # Go
cargo tree                            # Rust
```

**Deliverables:**
- `01-discovery/dependency-tree.txt`
- `01-discovery/dependency-inventory.csv`

**Checkpoint:** Update session file with total dependencies, ecosystems present, outdated packages

**Load for this phase:**
```
Read skills/dependency-audit/methodologies/supply-chain-analysis.md
# Focus on: Dependency discovery, transitive dependencies, dependency tree analysis
```

---

### Phase 2: PLAN - Vulnerability Research (1-2 hours)

**Goal:** Identify CVEs in dependencies and calculate risk scores

**Actions:**
1. Query CVE databases for EACH dependency (NIST NVD, GitHub Advisory Database, OSV)
2. Verify CVE IDs (ensure CVE exists, affected versions match, CVSS score documented)
3. Calculate CVSS v3.1 scores (Critical 9.0+, High 7.0-8.9, Medium 4.0-6.9, Low 0.1-3.9)
4. Check exploitability (EPSS scores, public exploits)
5. Document vulnerabilities (vulnerability register with CVE, CVSS, EPSS, CWE, priority)

**Prioritization Matrix:**
| CVSS | EPSS | Exploit Public | Priority |
|------|------|----------------|----------|
| Critical (9.0+) | High (>0.5) | Yes | **P0** (Immediate) |
| Critical (9.0+) | Low (<0.5) | No | **P1** (7 days) |
| High (7.0-8.9) | High (>0.5) | Yes | **P1** (7 days) |
| High (7.0-8.9) | Low (<0.5) | No | **P2** (30 days) |
| Medium (4.0-6.9) | Any | Any | **P3** (90 days) |

**Deliverables:**
- `02-vulnerabilities/VULN-001-critical-[cve].md`
- `02-vulnerabilities/cvss-prioritization.md`
- `02-vulnerabilities/vulnerability-register.csv`

**Checkpoint:** Update session file with vulnerability summary (Critical, High, Medium, Low counts) and CVE IDs verified

**Load for this phase:**
```
Read skills/dependency-audit/methodologies/supply-chain-analysis.md
# Focus on: CVE verification methodology, EPSS exploitability

Read skills/dependency-audit/reference/standards.md
# Focus on: NIST NVD, GitHub Advisory Database, OSV, CVSS v3.1, EPSS
```

---

### Phase 3: CODE - SBOM Generation (1-2 hours)

**Goal:** Generate SPDX or CycloneDX SBOM with NTIA minimum elements

**Actions:**
1. Choose SBOM format (SPDX for compliance/ISO, CycloneDX for security/OWASP)
2. Generate SBOM using tools (Syft, CycloneDX generators, OWASP Dependency-Check)
3. Add license information (SPDX license IDs for all components)
4. Add vulnerability references (embed CVE IDs in CycloneDX, external refs in SPDX)
5. Validate NTIA minimum elements (supplier, component name, version, purl, relationships, author, timestamp)

**NTIA Validation Checklist:**
- ✅ Supplier name present for all components
- ✅ Component name present
- ✅ Specific version (not range)
- ✅ Package URL (purl) present
- ✅ Dependency relationships documented
- ✅ SBOM author documented
- ✅ Timestamp present (ISO 8601)

**Deliverables:**
- `03-sbom/sbom-cyclonedx.json` (primary)
- `03-sbom/sbom-spdx.json` (alternative)
- `03-sbom/license-report.md`

**Checkpoint:** Update session file with SBOM format/location, NTIA compliance status, license distribution

**Load for this phase:**
```
Read skills/dependency-audit/methodologies/sbom-generation.md
# Focus on: SPDX vs CycloneDX, NTIA minimum elements, SBOM validation

Read skills/dependency-audit/reference/standards.md
# Focus on: SPDX 2.3, CycloneDX 1.5, NTIA requirements
```

---

### Phase 4: CODE - Supply Chain Risk Assessment (2-3 hours)

**Goal:** Assess supply chain maturity (SLSA), vendor trust, and non-CVE risks

**Actions:**
1. SLSA maturity assessment for critical dependencies (L0-L4 build provenance)
2. Maintainer reputation analysis (verified account, multiple maintainers, active commits, security policy)
3. Package popularity and community health (download count, GitHub stars, open issues addressed)
4. Dependency freshness (current <6mo, stale 6-12mo, outdated 12-24mo, abandoned >24mo)
5. Calculate overall risk score (CVE count, CVSS max, maintainer risk, freshness risk, SLSA risk)

**SLSA Assessment:**
- L0: No build provenance
- L1: Documented builds, automated CI/CD
- L2: Hosted build service (GitHub Actions), service-signed provenance
- L3: Ephemeral build environments, reproducible builds
- L4: Two-party review, hermetic builds

**Risk Score Formula:**
```
Risk = (CVE_Count × 2) + (CVSS_Max × 0.5) + (Maintainer_Risk × 2) + (Freshness_Risk × 1) + (SLSA_Risk × 1)

0-3: LOW RISK (monitor)
4-6: MEDIUM RISK (plan upgrade)
7-9: HIGH RISK (upgrade soon)
10+: CRITICAL RISK (upgrade immediately or replace)
```

**Deliverables:**
- `04-supply-chain-risk/slsa-assessment.md`
- `04-supply-chain-risk/maintainer-trust-analysis.md`
- `04-supply-chain-risk/risk-register.csv`

**Checkpoint:** Update session file with SLSA maturity distribution, abandoned packages identified

**Load for this phase:**
```
Read skills/dependency-audit/methodologies/supply-chain-analysis.md
# Focus on: SLSA maturity, maintainer reputation, package freshness, risk scoring

Read skills/dependency-audit/reference/standards.md
# Focus on: SLSA framework, ISO/IEC 27036
```

---

### Phase 5: COMMIT - Remediation Planning (1-2 hours)

**Goal:** Create actionable remediation roadmap with priorities and timelines

**Actions:**
1. Prioritize vulnerabilities (P0 immediate, P1 urgent 7-30 days, P2 planned 30-90 days, P3 low)
2. Create upgrade roadmap (direct upgrade, transitive dependency override, replace dependency)
3. **Use Context7 for secure API patterns** (verify correct library usage after upgrade)
4. Document workarounds (if upgrade blocked: input validation, WAF rules, risk acceptance)
5. Identify quick wins (low effort <2h, high impact fixes)
6. Document alternative packages (replacements for abandoned/high-risk dependencies)

**Context7 for Remediation Guidance:**
When a CVE affects specific API usage patterns, use Context7 to find the correct/secure implementation:
```python
from servers.context7 import get_library_docs

# CVE affects requests SSL verification
get_library_docs("psf/requests", topic="ssl")
# Returns: Current best practices for secure SSL configuration

# CVE affects axios response handling
get_library_docs("axios/axios", topic="security")
# Returns: Secure request/response patterns
```

**Why Context7 for Remediation:**
- Verifies the upgrade actually fixes the vulnerability
- Provides correct API usage patterns (not hallucinated)
- Ensures migration guidance matches library version

**Remediation Roadmap Structure:**
| Priority | VULN ID | Package | CVE | CVSS | Action | Effort | Owner |
|----------|---------|---------|-----|------|--------|--------|-------|
| P0 (0-7 days) | VULN-001 | axios | CVE-2024-1234 | 9.8 | Upgrade to 1.5.0 | 2h | DevOps |
| P1 (7-30 days) | VULN-002 | lodash | CVE-2021-23337 | 7.2 | Upgrade to 4.17.21 | 1h | Dev |
| P2 (30-90 days) | VULN-010 | moment | N/A (abandoned) | N/A | Replace with date-fns | 8h | Dev |

**Deliverables:**
- `05-remediation/upgrade-roadmap.md`
- `05-remediation/alternative-packages.md`
- `05-remediation/workarounds.md`
- `05-remediation/quick-wins.md`
- Final audit report

**Checkpoint:** Update session file with remediation summary, quick wins identified, audit status: COMPLETE

**Load for this phase:**
```
Read skills/dependency-audit/workflows/dependency-audit-workflow.md
# Focus on: Remediation planning, upgrade roadmap

Read skills/dependency-audit/templates/audit-report.md
# Use as template for final deliverable
```

---

## Output Structure

```
output/engagements/dependency-audits/[client]-[YYYY-MM]/
├── SCOPE.md
├── README.md
├── 01-discovery/
│   ├── dependency-tree.txt
│   └── dependency-inventory.csv
├── 02-vulnerabilities/
│   ├── VULN-001-critical-[cve].md
│   ├── cvss-prioritization.md
│   └── vulnerability-register.csv
├── 03-sbom/
│   ├── sbom-cyclonedx.json         (primary SBOM)
│   ├── sbom-spdx.json              (alternative format)
│   └── license-report.md
├── 04-supply-chain-risk/
│   ├── slsa-assessment.md
│   ├── maintainer-trust-analysis.md
│   └── risk-register.csv
├── 05-remediation/
│   ├── upgrade-roadmap.md
│   ├── alternative-packages.md
│   ├── workarounds.md
│   └── quick-wins.md
└── AUDIT-REPORT.md                 (final deliverable)
```

**Multi-session tracking:** `sessions/YYYY-MM-DD-project-name.md`

---

## Long-Session Rule Refresh

**Triggers:** Session > 3 hours OR 5+ dependency groups audited OR `/refresh-rules`

**Refresh statement:**
```
Refreshing critical rules for dependency audit:
- Context loaded (CLAUDE.md + SKILL.md + methodologies + references)
- SBOM generated (SPDX or CycloneDX with NTIA compliance validation)
- Checkpoints maintained (phases, CVEs verified with NVD, SBOM location, SLSA assessment)
- CVEs verified (NVD validation + EPSS exploitability for all vulnerabilities)
- SLSA assessed (supply chain maturity level L0-L4 for critical dependencies)
```

**Benefit:** 15-20% improvement in long-session SBOM compliance + CVE accuracy

---

## CVE Verification Process

**All vulnerabilities must be verified:**

1. **Query NIST NVD:** https://nvd.nist.gov/vuln/search
2. **Verify CVE exists:** CVE-YYYY-##### format, published date
3. **Check affected versions:** Ensure version range matches dependency version
4. **Document CVSS score:** v3.1 Base Score (0.0-10.0)
5. **Identify CWE:** Common Weakness Enumeration ID
6. **Check EPSS:** https://www.first.org/epss/ (exploit prediction scoring)
7. **Search for exploits:** Exploit-DB, Metasploit, GitHub

**Never report unverified vulnerabilities** - prevents false positives and maintains audit credibility.

---

**Version:** 2.1
**Last Updated:** 2025-12-19
**Model:** Claude Sonnet 4.5
**Framework:** NIST SP 800-161 + SLSA + SPDX/CycloneDX + NTIA + CVSS v3.1 + EPSS
**Pattern:** Progressive context loading with EXPLORE-PLAN-CODE-COMMIT workflow
**Remediation Tools:** Context7 (secure API patterns) + NIST NVD (CVE verification)
