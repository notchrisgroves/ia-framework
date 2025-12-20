# Dependency Audit Standards & Frameworks

**Authoritative standards for supply chain security, SBOM generation, and vulnerability management**

---

## Primary Standards

### NIST SP 800-161 Rev. 1 - Cybersecurity Supply Chain Risk Management

**URL:** https://csrc.nist.gov/publications/detail/sp/800-161/rev-1/final

**Published:** May 2022 (NIST)

**Scope:** Comprehensive supply chain risk management practices

**Key Controls:**
- C-SCRM-1: Supply chain cybersecurity risk identification
- C-SCRM-2: Criticality and prioritization (asset classification)
- C-SCRM-3: Threat and vulnerability assessment
- C-SCRM-4: Risk response and mitigation
- C-SCRM-5: Continuous monitoring and improvement

**Application:**
- Dependency risk assessment (identify third-party component risks)
- Vendor security evaluation (supplier trust assessment)
- Supply chain attack surface analysis
- Risk prioritization framework

---

### SLSA - Supply-chain Levels for Software Artifacts

**URL:** https://slsa.dev/

**Version:** 1.0 (Released 2023)

**Published by:** OpenSSF (Open Source Security Foundation), Google

**Purpose:** End-to-end framework for supply chain integrity

**Maturity Levels:**
- **Level 0:** No guarantees (manual, ad-hoc builds)
- **Level 1:** Documentation (automated builds with provenance)
- **Level 2:** Hosted build platform (service-generated provenance)
- **Level 3:** Hardened builds (isolated, ephemeral environments)
- **Level 4:** Two-party review (hermetic, reproducible builds)

**Build Requirements:**
- Provenance generation (signed metadata about build process)
- Source integrity (commit hash, repository URL)
- Build isolation (ephemeral environments for L3+)
- Two-party review (multi-person approval for L4)

**Application:**
- Assess build provenance maturity for dependencies
- Evaluate reproducibility of builds
- Verify supplier security practices
- Prioritize high-SLSA dependencies

---

### SPDX - Software Package Data Exchange

**URL:** https://spdx.dev/

**Version:** SPDX 2.3 (Current), SPDX 3.0 (In development)

**Status:** ISO/IEC 5962:2021 (International Standard)

**Published by:** Linux Foundation

**Purpose:** Standard format for communicating software component information

**SBOM Elements:**
- Package information (name, version, supplier, download location)
- File information (file-level SBOM with hashes)
- Licensing information (SPDX license identifiers)
- Relationships (DEPENDS_ON, CONTAINS, BUILD_TOOL_OF)
- External references (CPE, purl, security advisories)

**License List:**
- 500+ standardized license identifiers
- URL: https://spdx.org/licenses/
- Examples: MIT, Apache-2.0, GPL-3.0-only, BSD-3-Clause

**Application:**
- Generate SPDX SBOMs for compliance-driven environments
- License compliance analysis (GPL, MIT, Apache compatibility)
- File-level component tracking
- Government/ISO standard requirements

---

### CycloneDX

**URL:** https://cyclonedx.org/

**Version:** 1.5 (Current)

**Published by:** OWASP (Open Web Application Security Project)

**Purpose:** Lightweight SBOM standard for security use cases

**SBOM Elements:**
- Component inventory (libraries, frameworks, applications, containers, services)
- Dependency graph (parent-child relationships)
- Vulnerability references (CVE IDs embedded in SBOM)
- License information (SPDX license IDs)
- Hashes and identifiers (SHA-256, purl, CPE)
- Properties and evidence (build metadata, provenance)

**Formats:**
- JSON (most common)
- XML
- Protobuf (high-performance)

**Application:**
- Generate SBOMs for vulnerability management (security-first use case)
- Embed CVE IDs directly in SBOM
- Dependency-Track integration (continuous monitoring)
- OWASP ecosystem compatibility

---

### NTIA Minimum Elements for SBOM

**URL:** https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom

**Published:** July 2021 (U.S. Department of Commerce, NTIA)

**Mandated by:** Executive Order 14028 (Improving the Nation's Cybersecurity, May 2021)

**7 Minimum Elements:**
1. **Supplier Name** - Provider of the component
2. **Component Name** - Unique identifier for the software component
3. **Version of Component** - Specific version (not range)
4. **Other Unique Identifiers** - purl, CPE, SWID tag
5. **Dependency Relationship** - Direct vs transitive, parent-child mapping
6. **Author of SBOM Data** - Who generated the SBOM
7. **Timestamp** - When SBOM was generated

**Validation:**
- All SBOMs (SPDX, CycloneDX) must include these 7 elements
- Federal software procurement requires NTIA-compliant SBOMs
- Industry standard for SBOM completeness

**Application:**
- Validate SBOM completeness before delivery
- Ensure compliance with U.S. federal requirements
- Baseline for SBOM quality

---

## Supporting Standards

### NIST SP 800-218 - Secure Software Development Framework (SSDF)

**URL:** https://csrc.nist.gov/publications/detail/sp/800-218/final

**Published:** February 2022 (NIST)

**Purpose:** Secure development lifecycle practices

**Practices:**
- **PO (Prepare the Organization):** Security culture, training, tools
- **PS (Protect the Software):** Secure dependencies, build provenance
- **PW (Produce Well-Secured Software):** Code review, testing, SBOM generation
- **RV (Respond to Vulnerabilities):** Vulnerability disclosure, patch management

**Dependency-Specific Practices:**
- PO.3.2: Establish and maintain provenance of software components
- PS.1.1: Store and secure all software dependencies
- PS.3.1: Verify software component integrity (hashes, signatures)
- PS.3.2: Analyze software components for known vulnerabilities
- RV.1.1: Identify and track vulnerabilities in software components

**Application:**
- Secure SDLC integration for dependency management
- Provenance and integrity verification
- Vulnerability response procedures

---

### ISO/IEC 27036 - Security in Supplier Relationships

**URL:** https://www.iso.org/standard/59648.html

**Published:** ISO/IEC (International Organization for Standardization)

**Parts:**
- Part 1: Overview and concepts
- Part 2: Requirements (security in supply chain)
- Part 3: ICT supply chain security guidelines
- Part 4: Security of cloud services

**Key Requirements:**
- Supplier security assessment before procurement
- Contractual security requirements (SLAs, security controls)
- Ongoing supplier monitoring (security posture, incident disclosure)
- Supply chain incident response

**Application:**
- Vendor security evaluation (trust assessment before adopting dependency)
- Third-party risk management
- Supplier agreements (security requirements for dependencies)

---

### OWASP Dependency-Check

**URL:** https://owasp.org/www-project-dependency-check/

**Type:** Tool + Methodology

**Purpose:** Automated CVE detection in project dependencies

**Supported Ecosystems:**
- Java/Maven/Gradle
- .NET (NuGet)
- JavaScript/npm
- Python/pip
- Ruby/Bundler
- PHP/Composer
- Go modules
- Rust/Cargo

**Detection Method:**
- Parses dependency manifests and lock files
- Queries NIST NVD for CVE IDs
- Matches components using CPE (Common Platform Enumeration)
- Generates report with CVE IDs, CVSS scores, references

**Application:**
- CI/CD integration (automated vulnerability scanning)
- Dependency audit methodology (CVE identification)
- Baseline for vulnerability detection

---

## Vulnerability Databases

### NIST NVD - National Vulnerability Database

**URL:** https://nvd.nist.gov/

**Authority:** U.S. National Institute of Standards and Technology

**Coverage:** All CVEs (Common Vulnerabilities and Exposures)

**Data Provided:**
- CVE ID (e.g., CVE-2024-1234)
- CVSS v2.0, v3.0, v3.1 scores
- CWE ID (Common Weakness Enumeration)
- Affected product configurations (CPE strings)
- Vendor advisories and patches
- References (exploit POCs, vendor advisories)

**API Access:**
- NVD API 2.0: https://nvd.nist.gov/developers/vulnerabilities
- Rate limit: 5 requests per 30 seconds (with API key: 50 requests per 30 seconds)

**Application:**
- Primary source for CVE verification
- CVSS scoring for vulnerability prioritization
- Patch availability verification

---

### GitHub Advisory Database

**URL:** https://github.com/advisories

**Coverage:** Open source package vulnerabilities (npm, PyPI, Maven, NuGet, RubyGems, Go, Rust, Composer, Erlang)

**Data Provided:**
- GHSA ID (GitHub Security Advisory ID)
- CVE ID (if assigned)
- CVSS score
- Affected package versions
- Patched versions
- Workarounds

**Features:**
- Dependabot integration (automatic PRs for vulnerable dependencies)
- Security advisories from package maintainers
- Faster updates than NVD (community-driven)

**Application:**
- Ecosystem-specific vulnerability research
- Faster CVE detection (often updated before NVD)
- Dependabot workflow integration

---

### OSV - Open Source Vulnerabilities

**URL:** https://osv.dev/

**Published by:** Google (Open Source Security Team)

**Coverage:** 30+ open source ecosystems (PyPI, npm, Go, Rust, Maven, etc.)

**Data Provided:**
- OSV ID (ecosystem-specific)
- CVE ID (if mapped)
- Affected versions (precise version ranges)
- Severity (CVSS score when available)
- Ecosystem metadata (purl, package manager)

**API:**
- REST API: https://osv.dev/docs/api.html
- Query by package name + version
- Bulk query support

**Application:**
- Cross-ecosystem vulnerability lookup
- Precise version range matching (better than NVD CPE)
- Integration with vulnerability scanning tools

---

### EPSS - Exploit Prediction Scoring System

**URL:** https://www.first.org/epss/

**Published by:** FIRST (Forum of Incident Response and Security Teams)

**Purpose:** Predict probability of exploitation in the next 30 days

**Scoring:**
- 0.0 (0% probability) to 1.0 (100% probability)
- Updated daily with new data
- Machine learning model based on:
  - Exploit availability (Exploit-DB, Metasploit)
  - Social media mentions (Twitter, security blogs)
  - Vulnerability age
  - Vendor information

**Application:**
- Prioritize patching (high EPSS = likely to be exploited)
- Combine with CVSS (High CVSS + High EPSS = Critical priority)
- Resource allocation (focus on exploitable vulnerabilities)

**Example:**
- CVE-2021-44228 (Log4Shell): EPSS = 0.97 (97% probability) → Immediate patching
- CVE-2024-1234 (Obscure library): EPSS = 0.001 (0.1% probability) → Lower priority

---

## License Compliance Standards

### SPDX License List

**URL:** https://spdx.org/licenses/

**Coverage:** 500+ standardized license identifiers

**Common Licenses:**
- **Permissive:** MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC
- **Copyleft (Weak):** LGPL-2.1, LGPL-3.0, MPL-2.0
- **Copyleft (Strong):** GPL-2.0, GPL-3.0, AGPL-3.0
- **Restrictive:** SSPL (Server Side Public License), BSL (Business Source License)

**License Compatibility:**
- MIT + Apache-2.0 = ✅ Compatible (both permissive)
- Apache-2.0 + GPL-2.0 = ❌ Incompatible (patent clause conflict)
- MIT + GPL-3.0 = ⚠️ Compatible but project becomes GPL-3.0

**Application:**
- License compliance auditing
- Open source policy enforcement
- Risk assessment (GPL in proprietary software)

---

## Compliance Frameworks

### Executive Order 14028 - Improving the Nation's Cybersecurity

**URL:** https://www.whitehouse.gov/briefing-room/presidential-actions/2021/05/12/executive-order-on-improving-the-nations-cybersecurity/

**Section 4(e):** Software supply chain security

**Requirements:**
- **SBOMs:** Provide SBOM for all software sold to federal government
- **Provenance:** Cryptographically signed attestation of build process
- **Known vulnerabilities:** Disclose known vulnerabilities at delivery
- **Secure development:** Follow NIST SSDF practices

**Timeline:**
- May 2021: EO signed
- February 2022: NIST SP 800-218 (SSDF) published
- July 2021: NTIA minimum elements for SBOM published
- Ongoing: Federal agencies requiring SBOMs in contracts

**Application:**
- SBOM generation for government software
- SLSA compliance (provenance requirements)
- Vulnerability disclosure process

---

### PCI DSS 4.0 - Payment Card Industry Data Security Standard

**URL:** https://www.pcisecuritystandards.org/

**Requirement 6.3:** Software Development Lifecycle Security

**Sub-requirements:**
- 6.3.2: Review of custom code prior to production (code review, vulnerability testing)
- 6.3.3: Secure coding practices (OWASP, CWE/SANS Top 25)

**Requirement 11.3:** External and Internal Penetration Testing

**Application:**
- Dependency vulnerability scanning (external/internal testing)
- SBOM for compliance audits
- License compliance (GPL in PCI-regulated software)

---

**Version:** 2.0
**Last Updated:** 2025-12-02
**Primary Standards:** NIST SP 800-161, SLSA, SPDX, CycloneDX, NTIA, NIST SP 800-218
**Compliance:** EO 14028, ISO/IEC 27036, PCI DSS 4.0
