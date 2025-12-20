---
type: workflow
name: dependency-audit-workflow
classification: public
version: 1.0
last_updated: 2025-12-02
---

# Dependency Audit Workflow

**Complete 5-phase workflow for supply chain security analysis with SBOM generation**

---

## Workflow Overview

**Total Duration:** 6-10 hours (depending on project size and complexity)

**Phases:**
1. **EXPLORE:** Dependency Discovery (1-2 hours)
2. **PLAN:** Vulnerability Research (1-2 hours)
3. **CODE:** SBOM Generation (1-2 hours)
4. **CODE:** Risk Assessment (2-3 hours)
5. **COMMIT:** Remediation Planning (1-2 hours)

**Prerequisites:**
- Dependency manifests (package.json, requirements.txt, pom.xml, etc.)
- Lock files (package-lock.json, Pipfile.lock, go.sum, etc.)
- Access to NVD, GitHub Advisory Database, OSV

---

## Phase 1: EXPLORE - Dependency Discovery

**Duration:** 1-2 hours

**Goal:** Build complete inventory of direct and transitive dependencies

### Step 1.1: Identify Dependency Manifests

**Locate manifest files by ecosystem:**
- **JavaScript/Node.js:** package.json, package-lock.json, yarn.lock, pnpm-lock.yaml
- **Python:** requirements.txt, Pipfile.lock, poetry.lock, setup.py
- **Java/Maven:** pom.xml, dependency-reduced-pom.xml
- **Java/Gradle:** build.gradle, gradle.lockfile
- **Ruby:** Gemfile, Gemfile.lock
- **Go:** go.mod, go.sum
- **Rust:** Cargo.toml, Cargo.lock
- **C#/.NET:** packages.config, *.csproj, packages.lock.json
- **PHP:** composer.json, composer.lock

**Tools:**
```bash
# Find all manifest files
find . -name "package.json" -o -name "requirements.txt" -o -name "pom.xml" -o -name "Cargo.toml" -o -name "go.mod"
```

### Step 1.2: Parse Lock Files (Preferred)

**Why lock files?**
- Exact versions (manifest files may have version ranges like `^4.17.0`)
- Transitive dependencies included
- Cryptographic hashes for integrity verification

**Examples:**
```json
// package-lock.json (npm)
{
  "name": "myproject",
  "dependencies": {
    "lodash": {
      "version": "4.17.21",  // Exact version
      "resolved": "https://registry.npmjs.org/lodash/-/lodash-4.17.21.tgz",
      "integrity": "sha512-v2kDEe57lecTulaDIuNTPy3Ry4gLGJ6Z1O3vE1krgXZNrsQ+..."
    }
  }
}
```

```toml
# Cargo.lock (Rust)
[[package]]
name = "serde"
version = "1.0.152"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "bb7d1f0d3021d347a83e556fc4683dea2ea09d87bccdf88ff5c12545d89d5efb"
```

### Step 1.3: Build Dependency Tree

**Command examples by ecosystem:**
```bash
# npm (JavaScript)
npm list --all > dependency-tree.txt

# pip (Python)
pipdeptree --warn silence > dependency-tree.txt

# Maven (Java)
mvn dependency:tree > dependency-tree.txt

# Gradle (Java)
gradle dependencies > dependency-tree.txt

# Go
go mod graph > dependency-tree.txt

# Rust
cargo tree > dependency-tree.txt

# Ruby
bundle viz --file=dependency-graph.png
```

**Analyze tree:**
- Count direct dependencies (explicitly declared)
- Count transitive dependencies (pulled in by direct dependencies)
- Identify depth of dependency tree (potential supply chain risk)

**Example tree:**
```
myproject@1.0.0
├── express@4.18.2 (DIRECT)
│   ├── accepts@1.3.8 (TRANSITIVE)
│   │   ├── mime-types@2.1.35 (TRANSITIVE)
│   │   │   └── mime-db@1.52.0 (TRANSITIVE - depth 4)
│   │   └── negotiator@0.6.3 (TRANSITIVE)
│   ├── body-parser@1.20.1 (TRANSITIVE)
│   └── ...
└── lodash@4.17.21 (DIRECT)
```

**Red flags:**
- ⚠️ Depth > 5 (deep dependency chains increase supply chain risk)
- ⚠️ Hundreds of transitive dependencies (large attack surface)
- ⚠️ Unmaintained packages (last updated > 24 months ago)

### Step 1.4: Catalog Components

**Create dependency inventory (Excel/CSV/Markdown):**
| Package Name | Version | Type | Ecosystem | License | Last Updated |
|---|---|---|---|---|---|
| lodash | 4.17.21 | direct | npm | MIT | 2021-02-20 |
| express | 4.18.2 | direct | npm | MIT | 2022-10-08 |
| accepts | 1.3.8 | transitive | npm | MIT | 2021-04-27 |

**Document:**
- Total dependencies: X direct + Y transitive = Z total
- Ecosystems present (npm, PyPI, Maven, etc.)
- License types (MIT, Apache, GPL, etc.)
- Outdated packages (last updated > 12 months)

### **CHECKPOINT AFTER PHASE 1**

**Update #  Multi-session tracking in `../../sessions/:**
```markdown
## Phase 1: Dependency Discovery - COMPLETE

**Completed:** 2025-12-02 10:30:00

**Inventory Summary:**
- Direct dependencies: 15
- Transitive dependencies: 127
- Total dependencies: 142
- Ecosystems: npm (120), PyPI (22)
- Deepest dependency chain: 6 levels

**Files Created:**
- `01-discovery/dependency-tree.txt`
- `01-discovery/dependency-inventory.csv`

**Outdated Packages Identified:**
- lodash: 4.17.21 (last updated 2021-02-20, 47 months old)
- moment: 2.29.1 (last updated 2020-12-16, 60 months old)

**Next Action:** Phase 2 - Vulnerability Analysis (CVE research)
```

---

## Phase 2: PLAN - Vulnerability Research

**Duration:** 1-2 hours

**Goal:** Identify CVEs in dependencies and calculate risk scores

### Step 2.1: Query CVE Databases

**For EACH dependency, query:**

**Primary: NIST NVD**
- API: https://services.nvd.nist.gov/rest/json/cves/2.0
- Query: `https://services.nvd.nist.gov/rest/json/cves/2.0?keyword=lodash+4.17.21`
- Verify: CVE ID exists, affected versions match, CVSS score present

**Secondary: GitHub Advisory Database**
- URL: https://github.com/advisories?query=lodash+4.17.21
- Check: GHSA ID, CVE mapping, patch availability

**Tertiary: OSV**
- API: https://api.osv.dev/v1/query
- Query: `{"package": {"name": "lodash", "ecosystem": "npm"}, "version": "4.17.21"}`
- Precise version matching

**Tools:**
```bash
# OWASP Dependency-Check (automated)
dependency-check --project myproject --scan . --format JSON

# npm audit (npm only)
npm audit --json > npm-audit.json

# pip-audit (Python only)
pip-audit --format json > pip-audit.json

# cargo-audit (Rust only)
cargo audit --json > cargo-audit.json
```

### Step 2.2: Verify CVE IDs

**For EACH vulnerability found, verify:**
- ✅ CVE ID exists in NVD (e.g., CVE-2021-23337)
- ✅ Package name matches exactly (lodash, not loadash)
- ✅ Version range includes project's version
- ✅ CVSS v3.1 score documented
- ✅ CWE ID documented (e.g., CWE-78 Command Injection)

**Example verification:**
```markdown
### CVE-2021-23337 - Command Injection in lodash

**NVD URL:** https://nvd.nist.gov/vuln/detail/CVE-2021-23337

**Verified:**
- ✅ CVE-2021-23337 exists in NVD
- ✅ Affects lodash < 4.17.21 (our version: 4.17.20 - VULNERABLE)
- ✅ CVSS 3.1: 7.2 HIGH
- ✅ CWE-78: OS Command Injection
- ✅ Patch available: lodash 4.17.21+

**False Positive Check:**
- Code path reachable? YES (using lodash.template)
- Compensating controls? NO
- Confirmed: REAL VULNERABILITY
```

### Step 2.3: Calculate CVSS Scores

**CVSS v3.1 Severity Ranges:**
- **Critical:** 9.0 - 10.0
- **High:** 7.0 - 8.9
- **Medium:** 4.0 - 6.9
- **Low:** 0.1 - 3.9

**CVSS Calculator:** https://www.first.org/cvss/calculator/3.1

### Step 2.4: Check Exploitability (EPSS)

**Query EPSS scores:**
- URL: https://api.first.org/data/v1/epss?cve=CVE-2021-23337
- Score: 0.0 (0% probability) to 1.0 (100% probability)

**Prioritization Matrix:**
| CVSS | EPSS | Exploit Public | Priority |
|------|------|----------------|----------|
| Critical (9.0+) | High (>0.5) | Yes | **P0** (Immediate) |
| Critical (9.0+) | Low (<0.5) | No | **P1** (7 days) |
| High (7.0-8.9) | High (>0.5) | Yes | **P1** (7 days) |
| High (7.0-8.9) | Low (<0.5) | No | **P2** (30 days) |
| Medium (4.0-6.9) | Any | Any | **P3** (90 days) |

**Check for public exploits:**
- Exploit-DB: https://www.exploit-db.com/search?cve=CVE-2021-23337
- Metasploit: Search modules
- GitHub: Search "CVE-2021-23337 exploit"

### Step 2.5: Document Vulnerabilities

**Create vulnerability register (Markdown):**
```markdown
# Vulnerability Register

## VULN-001: Command Injection in lodash

**CVE:** CVE-2021-23337
**Package:** lodash@4.17.20
**CVSS:** 7.2 HIGH
**EPSS:** 0.15 (15% probability)
**CWE:** CWE-78 (OS Command Injection)
**Priority:** P2 (30 days)

**Description:**
lodash versions before 4.17.21 are vulnerable to command injection via the template function.

**Affected Code:**
- `src/utils.js:42` uses lodash.template with user input

**Patch Available:**
- Upgrade to lodash@4.17.21 or later

**Workaround:**
- Sanitize user input before passing to lodash.template
- Use allowlist for template variables

**References:**
- NVD: https://nvd.nist.gov/vuln/detail/CVE-2021-23337
- GitHub Advisory: https://github.com/advisories/GHSA-...
```

### **CHECKPOINT AFTER PHASE 2**

**Update #  Multi-session tracking in `../../sessions/:**
```markdown
## Phase 2: Vulnerability Analysis - COMPLETE

**Completed:** 2025-12-02 12:00:00

**Vulnerability Summary:**
- Critical: 2 (CVE-2024-1234, CVE-2024-5678)
- High: 5 (CVE-2021-23337, ...)
- Medium: 12
- Low: 8
- Total: 27 vulnerabilities

**High-Risk Dependencies:**
- lodash@4.17.20 (CVE-2021-23337 - High)
- axios@0.21.1 (CVE-2021-3749 - Critical)

**Files Created:**
- `02-vulnerabilities/VULN-001-critical-cve-2024-1234.md`
- `02-vulnerabilities/VULN-002-critical-cve-2024-5678.md`
- `02-vulnerabilities/cvss-prioritization.md`
- `02-vulnerabilities/vulnerability-register.csv`

**Next Action:** Phase 3 - SBOM Generation
```

---

## Phase 3: CODE - SBOM Generation

**Duration:** 1-2 hours

**Goal:** Generate SPDX or CycloneDX SBOM with NTIA minimum elements

### Step 3.1: Choose SBOM Format

**SPDX (ISO/IEC 5962:2021):**
- ✅ Use for: Compliance-driven environments (government, ISO requirements)
- ✅ Use for: File-level SBOM (individual files, not just packages)
- ✅ Use for: License compliance primary concern

**CycloneDX (OWASP):**
- ✅ Use for: Security-driven environments (vulnerability management)
- ✅ Use for: Embedding CVE IDs directly in SBOM
- ✅ Use for: OWASP ecosystem (Dependency-Track integration)

**Decision:** If unsure, generate BOTH formats

### Step 3.2: Generate SBOM

**Tools by ecosystem:**

**Syft (multi-ecosystem):**
```bash
# CycloneDX format
syft packages dir:. -o cyclonedx-json > sbom-cyclonedx.json

# SPDX format
syft packages dir:. -o spdx-json > sbom-spdx.json
```

**CycloneDX generators:**
```bash
# npm
cyclonedx-npm --output-file sbom-cyclonedx.json

# Maven
mvn cyclonedx:makeBom

# Python
cyclonedx-py --output sbom-cyclonedx.json
```

**SPDX tools:**
```bash
# Java SPDX tool
java -jar spdx-tools.jar Convert dir:. spdx-json sbom-spdx.json
```

### Step 3.3: Add License Information

**Verify each component has license:**
```json
{
  "components": [
    {
      "name": "lodash",
      "version": "4.17.21",
      "licenses": [
        {
          "license": {
            "id": "MIT",  // SPDX license ID
            "url": "https://opensource.org/licenses/MIT"
          }
        }
      ]
    }
  ]
}
```

**License detection:**
- Check package manifest (package.json: "license" field)
- Read LICENSE file from GitHub repository
- Use SPDX License List: https://spdx.org/licenses/

### Step 3.4: Add Vulnerability References

**CycloneDX format (embed CVEs):**
```json
{
  "components": [
    {
      "name": "lodash",
      "version": "4.17.20",
      "vulnerabilities": [
        {
          "id": "CVE-2021-23337",
          "source": {
            "name": "NVD",
            "url": "https://nvd.nist.gov/vuln/detail/CVE-2021-23337"
          },
          "ratings": [
            {
              "score": 7.2,
              "severity": "high",
              "method": "CVSSv31",
              "vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L"
            }
          ]
        }
      ]
    }
  ]
}
```

### Step 3.5: Validate NTIA Minimum Elements

**Checklist for EACH component:**
- ✅ Supplier name present (npm registry, Python Software Foundation, etc.)
- ✅ Component name present (lodash, requests, etc.)
- ✅ Specific version (4.17.21, not ^4.17.0)
- ✅ Package URL (purl) present: `pkg:npm/lodash@4.17.21`
- ✅ Dependency relationships documented (direct vs transitive)
- ✅ SBOM author documented (tool name: dependency-audit-agent)
- ✅ Timestamp present (ISO 8601: 2025-12-02T12:00:00Z)

**Validation tools:**
```bash
# Validate SBOM with sbom-tool
sbom-tool validate --input sbom-cyclonedx.json

# Manual validation
jq '.components[] | {name: .name, version: .version, purl: .purl}' sbom-cyclonedx.json
```

### **CHECKPOINT AFTER PHASE 3**

**Update #  Multi-session tracking in `../../sessions/:**
```markdown
## Phase 3: SBOM Generation - COMPLETE

**Completed:** 2025-12-02 14:00:00

**SBOM Summary:**
- Format: CycloneDX 1.5 JSON
- Components: 142 (15 direct, 127 transitive)
- Licenses identified: 100% (142/142)
- Vulnerabilities mapped: 27 CVEs embedded
- NTIA compliance: ✅ PASS (all 7 elements present)

**Files Created:**
- `03-sbom/sbom-cyclonedx.json` (primary SBOM)
- `03-sbom/sbom-spdx.json` (alternative format)
- `03-sbom/license-report.md` (license compliance summary)

**License Distribution:**
- MIT: 105 components
- Apache-2.0: 22 components
- BSD-3-Clause: 10 components
- ISC: 5 components

**Next Action:** Phase 4 - Supply Chain Risk Assessment (SLSA maturity, vendor trust)
```

---

## Phase 4: CODE - Supply Chain Risk Assessment

**Duration:** 2-3 hours

**Goal:** Assess supply chain maturity (SLSA), vendor trust, and non-CVE risks

### Step 4.1: SLSA Maturity Assessment

**For critical dependencies (authentication, cryptography, data processing):**

**Question 1: Build Provenance (L1)?**
- Does the project provide build provenance metadata?
- Are builds automated in CI/CD?
- Score: L0 (none), L1 (documented)

**Question 2: Hosted Build Service (L2)?**
- Builds performed on hosted platform (GitHub Actions, GitLab CI)?
- Provenance signed by service (not developer self-signed)?
- Score: L2 (service-signed provenance)

**Question 3: Build Isolation (L3)?**
- Ephemeral build environments (destroyed after build)?
- Reproducible builds?
- Score: L3 (hardened builds)

**Question 4: Two-party Review (L4)?**
- All changes require two-party approval?
- Hermetic builds (no network access during build)?
- Score: L4 (maximum supply chain integrity)

**SLSA Risk Matrix:**
| SLSA Level | Risk Rating | Recommendation |
|------------|-------------|----------------|
| L0 | HIGH RISK | Replace if possible, monitor closely |
| L1 | MEDIUM-HIGH RISK | Monitor, plan upgrade path |
| L2 | MEDIUM RISK | Acceptable for non-critical components |
| L3 | LOW RISK | Acceptable for all components |
| L4 | MINIMAL RISK | Preferred for critical components |

### Step 4.2: Maintainer Reputation Assessment

**For EACH dependency, evaluate:**

**Maintainer Trust Indicators:**
- ✅ Verified GitHub account
- ✅ Multiple maintainers (bus factor > 1)
- ✅ Active commit history (last commit < 6 months)
- ✅ Responsive to security issues (median response < 7 days)
- ✅ Security policy documented (SECURITY.md present)
- ✅ Known organization (Google, Microsoft, Apache, etc.)

**Red Flags:**
- ❌ Single maintainer with no backup
- ❌ Inactive project (no commits in 12+ months)
- ❌ No response to open security issues
- ❌ Anonymous maintainer

**Maintainer Risk Score (0-10):**
```
Risk = (Single maintainer: 2) + (Inactive: 3) + (No security policy: 2) + (Anonymous: 3)

0-2: LOW RISK (verified, active, multiple maintainers)
3-5: MEDIUM RISK (some concerns, monitor)
6-8: HIGH RISK (serious concerns, plan replacement)
9-10: CRITICAL RISK (replace immediately)
```

### Step 4.3: Package Popularity & Community Health

**Indicators:**
- Download count (npm: >100K/week = popular, PyPI: >10K/week = popular)
- GitHub stars (>1K = healthy community)
- Open issues being addressed (median response < 7 days)
- Regular releases (at least 1-2 per year)
- Comprehensive documentation
- Automated testing (CI/CD badges)

**Red flags for typosquatting:**
- Very low download count (potential typosquat)
- Package name similar to popular package (lodash vs 1odash)
- Recently created (< 6 months old) but claims to be mature
- No documentation or homepage

### Step 4.4: Dependency Freshness

**Update frequency:**
- ✅ **Current:** Last updated < 6 months
- ⚠️ **Stale:** Last updated 6-12 months
- ❌ **Outdated:** Last updated 12-24 months
- ❌ **Abandoned:** Last updated > 24 months

**Document abandoned packages:**
- Identify replacement packages
- Plan migration strategy
- Document risk acceptance if no replacement

### Step 4.5: Calculate Overall Risk Score

**Risk Score Formula:**
```
Risk Score = (CVE_Count × 2) + (CVSS_Max × 0.5) + (Maintainer_Risk × 2) + (Freshness_Risk × 1) + (SLSA_Risk × 1)

Where:
- CVE_Count = Number of known CVEs
- CVSS_Max = Highest CVSS score among CVEs (0-10)
- Maintainer_Risk = 0 (verified), 2 (unverified), 4 (anonymous), 6 (abandoned)
- Freshness_Risk = 0 (current), 1 (stale), 2 (outdated), 3 (abandoned)
- SLSA_Risk = 3 (L0), 2 (L1), 1 (L2), 0 (L3/L4)

Risk Score:
- 0-3: LOW RISK (monitor)
- 4-6: MEDIUM RISK (plan upgrade)
- 7-9: HIGH RISK (upgrade soon)
- 10+: CRITICAL RISK (upgrade immediately or replace)
```

### **CHECKPOINT AFTER PHASE 4**

**Update #  Multi-session tracking in `../../sessions/:**
```markdown
## Phase 4: Supply Chain Risk Assessment - COMPLETE

**Completed:** 2025-12-02 16:30:00

**Risk Assessment Summary:**
- Critical risk dependencies: 3 (lodash@4.17.20, axios@0.21.1, moment@2.29.1)
- High risk dependencies: 8
- Medium risk dependencies: 25
- Low risk dependencies: 106

**SLSA Maturity:**
- L0 (no guarantees): 45 packages
- L1 (documented): 62 packages
- L2 (hosted builds): 28 packages
- L3 (hardened): 7 packages
- L4 (two-party review): 0 packages

**Abandoned Packages:**
- moment@2.29.1 (last updated 60 months ago) → Replace with date-fns or dayjs

**Typosquatting Detected:**
- None found

**Files Created:**
- `04-supply-chain-risk/slsa-assessment.md`
- `04-supply-chain-risk/maintainer-trust-analysis.md`
- `04-supply-chain-risk/risk-register.csv`

**Next Action:** Phase 5 - Remediation Planning (upgrade roadmap, alternative packages)
```

---

## Phase 5: COMMIT - Remediation Planning

**Duration:** 1-2 hours

**Goal:** Create actionable remediation roadmap with priorities and timelines

### Step 5.1: Prioritize Vulnerabilities

**Prioritization matrix:**
| Priority | Criteria | Timeline |
|----------|----------|----------|
| **P0 (Immediate)** | CVSS ≥ 9.0 + EPSS > 0.5 + Public exploit | 0-7 days |
| **P1 (Urgent)** | CVSS ≥ 7.0 + EPSS > 0.1 OR Critical component | 7-30 days |
| **P2 (Planned)** | CVSS 4.0-6.9 + Patch available | 30-90 days |
| **P3 (Low)** | CVSS < 4.0 OR Workaround sufficient | When resources available |

### Step 5.2: Create Upgrade Roadmap

**For EACH high-priority vulnerability:**

**Option 1: Direct Upgrade**
```markdown
### VULN-001: CVE-2021-23337 (lodash)

**Current Version:** lodash@4.17.20
**Patched Version:** lodash@4.17.21+
**Upgrade Command:** `npm update lodash`
**Breaking Changes:** None (patch release)
**Effort:** 1 hour (upgrade + test)
**Priority:** P1 (7-30 days)
```

**Option 2: Transitive Dependency Override**
```markdown
### VULN-005: CVE-2024-5678 (vulnerable transitive dependency)

**Vulnerable Package:** mime@1.6.0 (transitive via express)
**Patched Version:** mime@2.0.0
**Direct Dependency:** express@4.18.2 (not yet updated to mime@2.0.0)

**Solution: Override in package.json**
```json
{
  "overrides": {
    "mime": "2.0.0"
  }
}
```

**Risk:** May break express if incompatible
**Test Plan:** Full regression testing
```

**Option 3: Replace Dependency**
```markdown
### VULN-010: moment (abandoned project)

**Current:** moment@2.29.1 (60 months old, no security updates)
**Replacement Options:**
1. date-fns@2.29.3 (actively maintained, tree-shakeable, MIT)
2. dayjs@1.11.7 (lightweight, moment.js-compatible API, MIT)

**Recommendation:** Migrate to date-fns
**Effort:** 8 hours (code refactoring + testing)
**Priority:** P2 (30-90 days)
```

### Step 5.3: Document Workarounds (If Upgrade Blocked)

**For vulnerabilities without patches:**
```markdown
### VULN-015: CVE-2024-9999 (no patch available)

**Package:** vulnerable-lib@3.2.1
**Issue:** No patch available (vendor unresponsive)

**Workarounds:**
1. **Input Validation:** Sanitize all user input before passing to vulnerable-lib
2. **WAF Rules:** Block requests matching exploit pattern
3. **Network Segmentation:** Isolate vulnerable service
4. **Monitoring:** Alert on suspicious activity

**Risk Acceptance:**
- Accepted by: Security Team
- Expiration: 2026-01-15 (re-evaluate in 30 days)
- Compensating Controls: Input validation + WAF + monitoring
```

### Step 5.4: Create Remediation Roadmap

**Sprint 1 (0-7 days) - Critical/Immediate:**
| Vuln ID | Package | CVE | CVSS | Action | Effort | Owner |
|---------|---------|-----|------|--------|--------|-------|
| VULN-001 | axios | CVE-2024-1234 | 9.8 | Upgrade to 1.5.0 | 2h | DevOps |
| VULN-002 | lodash | CVE-2021-23337 | 7.2 | Upgrade to 4.17.21 | 1h | Dev Team |

**Sprint 2 (7-30 days) - High Priority:**
| Vuln ID | Package | CVE | CVSS | Action | Effort | Owner |
|---------|---------|-----|------|--------|--------|-------|
| VULN-005 | express | CVE-2024-5678 | 7.5 | Override transitive | 4h | Dev Team |

**Sprint 3 (30-90 days) - Planned:**
| Vuln ID | Package | CVE | CVSS | Action | Effort | Owner |
|---------|---------|-----|------|--------|--------|-------|
| VULN-010 | moment | N/A (abandoned) | N/A | Replace with date-fns | 8h | Dev Team |

### Step 5.5: Quick Wins Analysis

**Identify low-effort, high-impact fixes:**
```markdown
### Quick Wins (< 2 hours effort each)

1. **lodash@4.17.20 → 4.17.21** (1 hour)
   - Impact: Fixes CVE-2021-23337 (CVSS 7.2 HIGH)
   - Effort: `npm update lodash` + regression test

2. **axios@1.4.0 → 1.5.0** (1 hour)
   - Impact: Fixes CVE-2024-1234 (CVSS 9.8 CRITICAL)
   - Effort: `npm update axios` + test

3. **express@4.17.0 → 4.18.2** (2 hours)
   - Impact: Fixes 3 CVEs (CVSS 7.5, 6.1, 5.3)
   - Effort: `npm update express` + full test suite
```

### **FINAL CHECKPOINT**

**Update #  Multi-session tracking in `../../sessions/:**
```markdown
## Phase 5: Remediation Planning - COMPLETE

**Completed:** 2025-12-02 18:00:00

**Remediation Summary:**
- P0 (Immediate): 2 vulnerabilities (upgrade axios, lodash)
- P1 (Urgent): 5 vulnerabilities
- P2 (Planned): 12 vulnerabilities
- P3 (Low): 8 vulnerabilities

**Quick Wins:** 3 fixes (< 2 hours each, high impact)

**Files Created:**
- `05-remediation/upgrade-roadmap.md`
- `05-remediation/alternative-packages.md`
- `05-remediation/workarounds.md`
- `05-remediation/quick-wins.md`

**Audit Status:** COMPLETE
**Next Steps:** Implement P0 fixes (0-7 days), schedule P1 fixes (7-30 days)
```

---

## Deliverables Checklist

**Phase 1: Discovery**
- ✅ dependency-tree.txt
- ✅ dependency-inventory.csv

**Phase 2: Vulnerability Analysis**
- ✅ vulnerability-register.csv
- ✅ VULN-XXX-[severity]-[cve].md files
- ✅ cvss-prioritization.md

**Phase 3: SBOM Generation**
- ✅ sbom-cyclonedx.json (primary)
- ✅ sbom-spdx.json (alternative)
- ✅ license-report.md
- ✅ NTIA validation report

**Phase 4: Risk Assessment**
- ✅ slsa-assessment.md
- ✅ maintainer-trust-analysis.md
- ✅ risk-register.csv

**Phase 5: Remediation**
- ✅ upgrade-roadmap.md
- ✅ alternative-packages.md
- ✅ workarounds.md
- ✅ quick-wins.md

**Final Report**
- ✅ Executive summary
- ✅ Methodology and scope
- ✅ Findings summary
- ✅ SBOM (attached)
- ✅ Remediation roadmap
- ✅ Appendices (detailed findings)

---

**Version:** 2.0
**Last Updated:** 2025-12-02
**Workflow:** EXPLORE → PLAN → CODE → CODE → COMMIT
**Duration:** 6-10 hours (standard audit)
