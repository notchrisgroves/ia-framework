# Supply Chain Security Analysis - Methodologies

**Core frameworks for dependency vulnerability assessment and third-party risk evaluation**

---

## NIST SP 800-161 Rev. 1 - Cybersecurity Supply Chain Risk Management

**Purpose:** Comprehensive framework for managing cybersecurity risks throughout the supply chain

**URL:** https://csrc.nist.gov/publications/detail/sp/800-161/rev-1/final

### Key Components

**1. Supply Chain Risk Identification**
- Third-party component analysis
- Vendor security assessment
- Dependency provenance validation
- Supply chain attack surface mapping

**2. Risk Assessment Process**
- Likelihood determination (supplier security posture, component criticality)
- Impact analysis (confidentiality, integrity, availability)
- Risk prioritization (NIST Risk Management Framework)

**3. Risk Response**
- Accept: Low-risk dependencies with monitoring
- Avoid: Replace high-risk dependencies
- Mitigate: Apply patches, workarounds, or compensating controls
- Transfer: Vendor indemnification or insurance

**4. Continuous Monitoring**
- CVE monitoring for dependencies
- SBOM maintenance and updates
- Vendor security posture tracking

### Implementation in Dependency Audits

**Phase 1: Identify Supply Chain Components**
```markdown
- Parse dependency manifests (package.json, requirements.txt, pom.xml)
- Build dependency tree (direct + transitive)
- Identify suppliers/vendors for each component
- Document component criticality (authentication, cryptography, data processing)
```

**Phase 2: Assess Component Risks**
```markdown
- Query CVE databases (NVD, GitHub Advisory, OSV)
- Calculate CVSS v3.1 scores for vulnerabilities
- Check exploitability (EPSS scores)
- Evaluate vendor security posture (GitHub stars, maintainer activity, security advisories)
```

**Phase 3: Prioritize Remediation**
```markdown
- Critical components with exploitable CVEs → Immediate action
- High-impact components with patches available → 7-30 days
- Low-impact components or no exploits → 30-90 days
```

---

## SLSA Framework - Supply-chain Levels for Software Artifacts

**Purpose:** Maturity model for build provenance and supply chain integrity

**URL:** https://slsa.dev/

### SLSA Levels (L0-L4)

**Level 0: No Guarantees**
- No build provenance
- No integrity verification
- Manual dependency management

**Level 1: Documentation**
- Build process documented
- Automated builds (CI/CD)
- Signed provenance metadata

**Level 2: Hosted Build Platform**
- Use hosted build service (GitHub Actions, GitLab CI)
- Signed provenance with source/build metadata
- Service-generated provenance (not self-signed)

**Level 3: Hardened Builds**
- Build platform isolation (ephemeral environments)
- Non-falsifiable provenance (cryptographic guarantees)
- Provenance includes all build dependencies

**Level 4: Two-party Review**
- All changes require two-party approval
- Hermetic, reproducible builds
- Complete build dependency provenance

### SLSA Assessment in Dependency Audits

**Question 1: Build Provenance** (L1 requirement)
- Does the project provide build provenance metadata?
- Are builds automated in CI/CD?
- Can you verify build process integrity?

**Question 2: Hosted Build Service** (L2 requirement)
- Does the project use a hosted build platform?
- Is provenance signed by the build service (not developer)?
- Can you verify the build service used?

**Question 3: Build Isolation** (L3 requirement)
- Are builds performed in ephemeral environments?
- Is the build process reproducible?
- Does provenance include all build dependencies?

**Question 4: Two-party Review** (L4 requirement)
- Do all changes require two-party approval?
- Are builds hermetic (no network access during build)?
- Can you reproduce the build from source?

**SLSA Score:**
- **L0:** No evidence of secure build practices (HIGH RISK)
- **L1:** Documented builds, automated CI/CD (MEDIUM RISK)
- **L2:** Hosted builds with signed provenance (LOW-MEDIUM RISK)
- **L3:** Hardened builds with isolation (LOW RISK)
- **L4:** Hermetic builds with two-party review (MINIMAL RISK)

---

## CVE Verification Methodology

**Purpose:** Ensure all vulnerability claims are backed by verified CVE IDs from authoritative sources

### Step 1: CVE Database Query

**Primary Source: NIST NVD (National Vulnerability Database)**
- URL: https://nvd.nist.gov/
- Search by: Package name, version, CVE ID
- Verification: CVE ID, CVSS score, affected versions, patch availability

**Secondary Sources:**
- GitHub Advisory Database: https://github.com/advisories
- OSV (Open Source Vulnerabilities): https://osv.dev/
- Snyk Vulnerability Database: https://security.snyk.io/
- npm Security Advisories: https://www.npmjs.com/advisories
- PyPI Advisory Database: https://github.com/pypa/advisory-database

### Step 2: CVE Validation Checklist

For EACH vulnerability, verify:
- ✅ CVE ID exists in NVD (e.g., CVE-2024-1234)
- ✅ Affected package name matches dependency
- ✅ Affected version range includes project's version
- ✅ CVSS v3.1 score is documented
- ✅ CWE ID is documented (e.g., CWE-79 for XSS)
- ✅ Patch version is available (or workaround documented)

### Step 3: False Positive Detection

**Common False Positives:**
- Vulnerability in unused code path (e.g., dev dependency not in production)
- Vulnerability requires specific configuration not present in project
- Vulnerability fixed by compensating controls (WAF, input validation)
- CVE applies to different package with similar name

**Validation:**
```markdown
1. Check if vulnerable code path is reachable in project
2. Verify configuration matches vulnerable scenario
3. Confirm no compensating controls exist
4. Double-check package name matches exactly
```

### Step 4: Exploitability Assessment

**EPSS Score (Exploit Prediction Scoring System)**
- URL: https://www.first.org/epss/
- Score: 0.0 (0% probability of exploitation) to 1.0 (100% probability)
- Threshold: EPSS > 0.10 (10% probability) = HIGH PRIORITY

**Exploit Availability:**
- Check Exploit-DB: https://www.exploit-db.com/
- Check Metasploit modules: https://www.rapid7.com/db/
- Check GitHub for POC exploits: Search "[CVE-ID] exploit"

**Prioritization Matrix:**
| CVSS Score | EPSS Score | Exploit Public | Priority |
|------------|------------|----------------|----------|
| Critical (9.0+) | High (>0.5) | Yes | **P0** (Immediate) |
| Critical (9.0+) | Low (<0.5) | No | **P1** (7 days) |
| High (7.0-8.9) | High (>0.5) | Yes | **P1** (7 days) |
| High (7.0-8.9) | Low (<0.5) | No | **P2** (30 days) |
| Medium (4.0-6.9) | Any | Any | **P3** (90 days) |
| Low (<4.0) | Any | Any | **P4** (When resources available) |

---

## Dependency Risk Assessment

**Purpose:** Evaluate supply chain risk beyond just CVE presence

### Risk Factor 1: Maintainer Reputation

**Indicators of Trustworthy Maintainers:**
- ✅ Verified GitHub account
- ✅ Multiple maintainers (bus factor > 1)
- ✅ Active commit history (last commit < 6 months)
- ✅ Responsive to security issues (median response time < 7 days)
- ✅ Security policy documented (SECURITY.md present)
- ✅ Known organization affiliation (Google, Microsoft, Apache, etc.)

**Red Flags:**
- ❌ Single maintainer with no backup
- ❌ Inactive project (no commits in 12+ months)
- ❌ No response to open security issues
- ❌ No security policy or vulnerability disclosure process
- ❌ Anonymous maintainer with no public identity

### Risk Factor 2: Package Popularity & Community Health

**Indicators of Healthy Package:**
- ✅ High download count (npm: >100K/week, PyPI: >10K/week)
- ✅ Active community (GitHub stars >1K, open issues being addressed)
- ✅ Regular releases (at least 1-2 releases per year)
- ✅ Comprehensive documentation
- ✅ Automated testing (CI/CD badges)

**Red Flags:**
- ❌ Very low download count (potential typosquatting)
- ❌ Abandoned project (no releases in 2+ years)
- ❌ Unaddressed security issues
- ❌ No documentation or tests

### Risk Factor 3: Typosquatting Detection

**Typosquatting Patterns:**
- Character substitution: `lodash` → `1odash` (L → 1)
- Character omission: `requests` → `reqeusts`
- Character insertion: `axios` → `axioss`
- Hyphenation: `express` → `express-js` (when legitimate is `express`)
- Scope confusion: `react` → `@fake/react`

**Detection:**
```markdown
1. Check package name against official repository
2. Verify package author matches official maintainer
3. Check creation date (typosquats often created recently)
4. Compare download counts (orders of magnitude lower than legitimate)
5. Review package description and homepage URL
```

### Risk Factor 4: Dependency Freshness

**Update Frequency:**
- ✅ **Current:** Last updated < 6 months
- ⚠️ **Stale:** Last updated 6-12 months
- ❌ **Outdated:** Last updated 12-24 months
- ❌ **Abandoned:** Last updated >24 months

**Security Implications:**
- Outdated dependencies may have unpatched CVEs
- Abandoned packages won't receive security fixes
- Stale dependencies may have compatibility issues

### Risk Assessment Score

**Calculate Risk Score (0-10):**
```
Risk Score = (CVE_Count × 2) + (CVSS_Max × 0.5) + (Maintainer_Risk × 2) + (Freshness_Risk × 1)

Where:
- CVE_Count = Number of known CVEs in dependency
- CVSS_Max = Highest CVSS score among CVEs (0-10)
- Maintainer_Risk = 0 (verified), 2 (unverified), 4 (anonymous), 6 (abandoned)
- Freshness_Risk = 0 (current), 1 (stale), 2 (outdated), 3 (abandoned)

Risk Score:
- 0-2: LOW RISK (monitor)
- 3-5: MEDIUM RISK (plan upgrade)
- 6-8: HIGH RISK (upgrade soon)
- 9-10: CRITICAL RISK (upgrade immediately or replace)
```

---

## Transitive Dependency Analysis

**Purpose:** Identify vulnerabilities in indirect dependencies (dependencies of dependencies)

### Challenge: Hidden Vulnerabilities

**Problem:**
- Your project depends on Package A
- Package A depends on Package B (transitive dependency)
- Package B has a critical CVE
- You may not be aware of Package B's existence

**Solution: Full Dependency Tree Analysis**

### Step 1: Build Dependency Tree

**Tools by Ecosystem:**
- **npm:** `npm list --all` (shows all transitive dependencies)
- **Python:** `pipdeptree` (visualizes dependency tree)
- **Maven:** `mvn dependency:tree` (shows all dependencies)
- **Go:** `go mod graph` (shows module dependencies)
- **Ruby:** `bundle viz` (generates dependency graph)

### Step 2: Identify Vulnerable Transitive Dependencies

**Process:**
```markdown
1. Parse lock file (package-lock.json, Pipfile.lock, go.sum)
2. Extract ALL dependencies (direct + transitive)
3. Query CVE databases for each transitive dependency
4. Map vulnerable transitive dependency back to direct dependency
5. Determine upgrade path (which direct dependency to upgrade)
```

### Step 3: Remediation Strategies

**Strategy 1: Upgrade Direct Dependency**
- Upgrade the direct dependency that pulls in vulnerable transitive
- Verify the new version of direct dependency uses patched transitive

**Strategy 2: Dependency Override**
- Force a specific version of transitive dependency (npm: `overrides`, Python: `constraints.txt`)
- **Risk:** May break direct dependency if it requires specific version

**Strategy 3: Replace Direct Dependency**
- Replace the direct dependency with an alternative that doesn't use vulnerable transitive
- **Example:** Switch from `packageA` (uses vulnerable `packageB`) to `packageC` (doesn't use `packageB`)

**Strategy 4: Workaround/Mitigation**
- If upgrade not possible, implement compensating controls (input validation, WAF rules)
- Document risk acceptance with expiration date

---

## Continuous Dependency Monitoring

**Purpose:** Ongoing vulnerability tracking for dependencies (not one-time audit)

### Monitoring Strategy

**Daily Checks:**
- New CVEs for dependencies (NVD, GitHub Security Advisories)
- Automated scanning (Dependabot, Snyk, GitHub Advanced Security)

**Weekly Reviews:**
- Review new CVEs flagged by scanners
- Prioritize patching based on CVSS + EPSS
- Update SBOM with new CVEs

**Monthly Audits:**
- Full dependency tree scan
- SBOM regeneration
- SLSA level reassessment

**Quarterly Reviews:**
- Supply chain risk assessment
- Vendor security posture evaluation
- Dependency replacement analysis

### Automation Tools

**Free Tools:**
- GitHub Dependabot (automatic PRs for dependency updates)
- OWASP Dependency-Check (CI/CD integration)
- npm audit / pip-audit (built-in scanners)

**Commercial Tools:**
- Snyk (developer-first security)
- WhiteSource/Mend (open source risk management)
- Veracode SCA (software composition analysis)

---

**Version:** 2.0
**Last Updated:** 2025-12-02
**Frameworks:** NIST SP 800-161 Rev. 1, SLSA, CVSS v3.1, EPSS
**Purpose:** Comprehensive supply chain security analysis methodology
