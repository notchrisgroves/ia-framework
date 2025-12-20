# SBOM Generation - Software Bill of Materials

**Comprehensive guide to generating, validating, and maintaining SBOMs in SPDX and CycloneDX formats**

---

## What is an SBOM?

**Software Bill of Materials (SBOM):** Complete inventory of components used to build software, including:
- Direct dependencies (explicitly declared)
- Transitive dependencies (pulled in by direct dependencies)
- Component versions
- Licenses
- Suppliers/manufacturers
- Vulnerability status
- Relationships between components

**Purpose:**
- **Vulnerability Management:** Track which components have CVEs
- **License Compliance:** Identify GPL, MIT, Apache licenses
- **Supply Chain Transparency:** Know what's in your software
- **Incident Response:** Quickly identify affected systems when new CVE announced

---

## SBOM Standards

### SPDX (Software Package Data Exchange)

**URL:** https://spdx.dev/

**Status:** ISO/IEC 5962:2021 international standard

**Format:** JSON, YAML, XML, RDF, Tag-Value

**Key Features:**
- License identification (SPDX License List)
- Component relationships (DEPENDS_ON, CONTAINS, etc.)
- File-level granularity (individual files within packages)
- Cryptographic hashes (SHA-256, SHA-1)
- Originator and supplier metadata

**When to Use SPDX:**
- Compliance-driven environments (government, ISO standards)
- Need file-level SBOM (not just package-level)
- License compliance primary concern

**Example SPDX (JSON):**
```json
{
  "spdxVersion": "SPDX-2.3",
  "dataLicense": "CC0-1.0",
  "SPDXID": "SPDXRef-DOCUMENT",
  "name": "MyProject-1.0",
  "documentNamespace": "https://example.com/myproject-1.0",
  "creationInfo": {
    "created": "2025-12-02T10:00:00Z",
    "creators": ["Tool: dependency-audit-agent"]
  },
  "packages": [
    {
      "SPDXID": "SPDXRef-Package-lodash",
      "name": "lodash",
      "versionInfo": "4.17.21",
      "downloadLocation": "https://registry.npmjs.org/lodash/-/lodash-4.17.21.tgz",
      "licenseConcluded": "MIT",
      "externalRefs": [
        {
          "referenceCategory": "PACKAGE-MANAGER",
          "referenceType": "purl",
          "referenceLocator": "pkg:npm/lodash@4.17.21"
        }
      ]
    }
  ],
  "relationships": [
    {
      "spdxElementId": "SPDXRef-DOCUMENT",
      "relationshipType": "DESCRIBES",
      "relatedSpdxElement": "SPDXRef-Package-lodash"
    }
  ]
}
```

---

### CycloneDX

**URL:** https://cyclonedx.org/

**Status:** OWASP project, de facto standard for security use cases

**Format:** JSON, XML, Protobuf

**Key Features:**
- Vulnerability references (CVE IDs directly in SBOM)
- Component properties (hashes, licenses, suppliers)
- Dependency graph (parent-child relationships)
- Services and API inventory (beyond just packages)
- Security-focused (designed for vulnerability tracking)

**When to Use CycloneDX:**
- Security-driven environments (vulnerability management primary goal)
- Need to embed CVE IDs in SBOM
- Prefer simpler format than SPDX
- OWASP ecosystem (used by Dependency-Track, etc.)

**Example CycloneDX (JSON):**
```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.5",
  "version": 1,
  "metadata": {
    "timestamp": "2025-12-02T10:00:00Z",
    "component": {
      "type": "application",
      "name": "MyProject",
      "version": "1.0"
    }
  },
  "components": [
    {
      "type": "library",
      "name": "lodash",
      "version": "4.17.21",
      "purl": "pkg:npm/lodash@4.17.21",
      "licenses": [
        {
          "license": {
            "id": "MIT"
          }
        }
      ],
      "hashes": [
        {
          "alg": "SHA-256",
          "content": "f6a1a7dbb5f0d0f6e6f4a7e8..."
        }
      ]
    }
  ],
  "dependencies": [
    {
      "ref": "pkg:npm/lodash@4.17.21",
      "dependsOn": []
    }
  ]
}
```

---

## NTIA Minimum Elements for SBOM

**URL:** https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom

**Required by:** U.S. Executive Order 14028 (Cybersecurity, May 2021)

### The 7 Minimum Elements

**1. Supplier Name**
- Who provides the component (npm registry, PyPI, GitHub, company name)
- Example: "npm", "Python Software Foundation", "Lodash Authors"

**2. Component Name**
- Exact name of the component
- Example: "lodash", "requests", "log4j-core"

**3. Version of Component**
- Specific version number (not "latest" or ranges)
- Example: "4.17.21", "2.28.1", "2.17.1"

**4. Other Unique Identifiers**
- Package URL (purl): `pkg:npm/lodash@4.17.21`
- CPE (Common Platform Enumeration): `cpe:2.3:a:lodash:lodash:4.17.21`
- SWID tag (Software Identification Tag)

**5. Dependency Relationship**
- Is this a direct or transitive dependency?
- What depends on this component?
- What does this component depend on?

**6. Author of SBOM Data**
- Who generated the SBOM?
- Example: "dependency-audit-agent", "Syft", "OWASP Dependency-Check"

**7. Timestamp**
- When was the SBOM generated?
- Example: "2025-12-02T10:00:00Z"

### NTIA Validation Checklist

For EACH component in SBOM, verify:
- ✅ Supplier name present
- ✅ Component name present
- ✅ Version present (specific version, not range)
- ✅ Package URL (purl) present
- ✅ Dependency relationships documented
- ✅ SBOM author documented
- ✅ Timestamp present

**Invalid SBOM Examples:**
- ❌ Version: "^4.17.0" (range, not specific version)
- ❌ Supplier: "Unknown" (not identified)
- ❌ Component: "core" (too generic, need full name)

---

## SBOM Generation Process

### Phase 1: Dependency Inventory

**Step 1: Identify Dependency Manifests**

**Common Manifest Files:**
- **JavaScript/Node.js:** package.json, package-lock.json, yarn.lock
- **Python:** requirements.txt, Pipfile.lock, poetry.lock
- **Java/Maven:** pom.xml, dependency-reduced-pom.xml
- **Java/Gradle:** build.gradle, gradle.lockfile
- **Ruby:** Gemfile, Gemfile.lock
- **Go:** go.mod, go.sum
- **Rust:** Cargo.toml, Cargo.lock
- **C#/.NET:** packages.config, *.csproj, packages.lock.json
- **PHP:** composer.json, composer.lock

**Step 2: Parse Lock Files (Preferred)**
- Lock files contain exact versions (manifest files may have ranges)
- Lock files include transitive dependencies
- Lock files include cryptographic hashes

**Example (package-lock.json):**
```json
{
  "name": "myproject",
  "version": "1.0.0",
  "dependencies": {
    "lodash": {
      "version": "4.17.21",
      "resolved": "https://registry.npmjs.org/lodash/-/lodash-4.17.21.tgz",
      "integrity": "sha512-v2kDEe57lecTulaDIuNTPy3Ry4gLGJ6Z1O3vE1krgXZNrsQ+..."
    }
  }
}
```

**Step 3: Build Dependency Tree**
```
myproject@1.0.0
├── express@4.18.2
│   ├── accepts@1.3.8
│   │   ├── mime-types@2.1.35
│   │   │   └── mime-db@1.52.0
│   │   └── negotiator@0.6.3
│   ├── body-parser@1.20.1
│   └── ...
└── lodash@4.17.21
```

---

### Phase 2: License Identification

**Step 1: Detect License Type**

**Common Licenses:**
- **Permissive:** MIT, Apache-2.0, BSD-3-Clause (allow commercial use, modification)
- **Copyleft:** GPL-2.0, GPL-3.0, LGPL (require derived works to be open source)
- **Restrictive:** SSPL, BSL, Commons Clause (restrict commercial use)

**License Detection Methods:**
1. Check package manifest (package.json: "license" field)
2. Read LICENSE file in package repository
3. Use SPDX License List identifiers
4. Scan code for license headers

**Step 2: SPDX License IDs**
- Use standardized SPDX license identifiers
- Example: "MIT", "Apache-2.0", "GPL-3.0-only"
- Full list: https://spdx.org/licenses/

**Step 3: License Compliance Checks**
```markdown
✅ SAFE COMBINATIONS:
- MIT + Apache-2.0 (both permissive)
- BSD + MIT (both permissive)
- Apache-2.0 + LGPL-3.0 (permissive + weak copyleft)

⚠️ RISKY COMBINATIONS:
- MIT + GPL-3.0 (permissive + strong copyleft → project becomes GPL-3.0)
- Apache-2.0 + AGPL-3.0 (permissive + network copyleft → project becomes AGPL-3.0)

❌ INCOMPATIBLE:
- Apache-2.0 + GPL-2.0 (patent clause conflict)
- Proprietary + GPL-3.0 (copyleft conflict)
```

---

### Phase 3: Vulnerability Mapping

**Step 1: Query CVE Databases**

**For EACH component, query:**
- NIST NVD: https://nvd.nist.gov/
- GitHub Advisory Database: https://github.com/advisories
- OSV: https://osv.dev/

**Example Query:**
```
Package: lodash
Version: 4.17.21
CVE Query: "lodash 4.17.21 vulnerability"
```

**Step 2: Map CVEs to Components**

**CycloneDX Format (includes CVEs in SBOM):**
```json
{
  "components": [
    {
      "name": "lodash",
      "version": "4.17.21",
      "vulnerabilities": [
        {
          "id": "CVE-2021-23337",
          "source": {
            "name": "NVD",
            "url": "https://nvd.nist.gov/vuln/detail/CVE-2021-23337"
          },
          "ratings": [
            {
              "score": 7.4,
              "severity": "high",
              "method": "CVSSv31"
            }
          ]
        }
      ]
    }
  ]
}
```

**SPDX Format (external references):**
```json
{
  "packages": [
    {
      "name": "lodash",
      "versionInfo": "4.17.21",
      "externalRefs": [
        {
          "referenceCategory": "SECURITY",
          "referenceType": "cpe23Type",
          "referenceLocator": "cpe:2.3:a:lodash:lodash:4.17.21:*:*:*:*:*:*:*"
        },
        {
          "referenceCategory": "SECURITY",
          "referenceType": "advisory",
          "referenceLocator": "https://nvd.nist.gov/vuln/detail/CVE-2021-23337"
        }
      ]
    }
  ]
}
```

---

### Phase 4: SBOM Validation

**NTIA Minimum Elements Check:**
```markdown
For EACH component, verify:
✅ Supplier name present
✅ Component name present
✅ Specific version (not range)
✅ Package URL (purl) present
✅ Dependency relationships documented
✅ SBOM author documented
✅ Timestamp present
```

**Additional Quality Checks:**
```markdown
✅ All transitive dependencies included (not just direct)
✅ License identified for all components
✅ CVE mapping completed (vulnerabilities documented)
✅ Hashes present (SHA-256 for integrity verification)
✅ Valid JSON/XML (syntax check)
```

---

## SBOM Generation Tools

### Free/Open Source Tools

**Syft (Anchore)**
- URL: https://github.com/anchore/syft
- Formats: SPDX, CycloneDX, Syft JSON
- Features: Container image scanning, multi-language support
- Usage: `syft packages dir:/path/to/project -o cyclonedx-json`

**CycloneDX Generator**
- URL: https://github.com/CycloneDX
- Formats: CycloneDX (JSON, XML)
- Ecosystem-specific: npm, Maven, Python, .NET, Go, Ruby
- Usage: `cyclonedx-npm --output-file sbom.json`

**SPDX Tools**
- URL: https://github.com/spdx/tools
- Formats: SPDX (JSON, YAML, XML, RDF, Tag-Value)
- Features: SBOM validation, format conversion
- Usage: SPDX libraries for Java, Python, Go

**OWASP Dependency-Check**
- URL: https://owasp.org/www-project-dependency-check/
- Formats: HTML, JSON, CSV, XML
- Features: CVE detection + SBOM generation
- Usage: `dependency-check --project myproject --scan . --format JSON`

### Commercial Tools

**Snyk**
- SBOM export from vulnerability scan results
- CycloneDX format

**WhiteSource/Mend**
- Automated SBOM generation for all projects
- SPDX and CycloneDX formats

**JFrog Xray**
- SBOM generation from artifact analysis
- Integration with JFrog Artifactory

---

## SBOM Maintenance

### When to Regenerate SBOM

**Trigger 1: Dependency Updates**
- Regenerate SBOM after `npm update`, `pip install --upgrade`, etc.
- SBOM must reflect current dependency versions

**Trigger 2: New CVE Discovered**
- Update SBOM vulnerability section when new CVE affects dependency
- Add CVE reference to affected component

**Trigger 3: Release/Deployment**
- Regenerate SBOM for each release (1.0, 1.1, 2.0)
- Include SBOM in release artifacts

**Trigger 4: Periodic Review**
- Monthly: Regenerate SBOM to catch any drift
- Quarterly: Full audit + SBOM validation

### SBOM Versioning

**Best Practice: Version SBOMs**
```
sbom-myproject-1.0.0-20251202.json
sbom-myproject-1.0.1-20251210.json
sbom-myproject-1.1.0-20260115.json
```

**Track Changes:**
- Which dependencies were added/removed?
- Which vulnerabilities were fixed?
- Which licenses changed?

---

## SBOM Distribution

### Who Needs Access to SBOM?

**Internal:**
- Security team (vulnerability tracking)
- Compliance team (license auditing)
- DevOps team (deployment decisions)
- Incident response team (rapid CVE assessment)

**External:**
- Customers (enterprise buyers often request SBOMs)
- Auditors (SOC 2, ISO 27001 compliance)
- Government agencies (EO 14028 requirement for federal software)
- Open source communities (transparency)

### SBOM Storage

**Options:**
1. **Git repository** (alongside source code)
   - `sbom/sbom-1.0.0.json`
2. **Artifact repository** (with release artifacts)
   - Nexus, Artifactory, GitHub Releases
3. **SBOM registry** (centralized SBOM management)
   - OWASP Dependency-Track
4. **Public transparency** (published on website)
   - `https://example.com/security/sbom/myproject-1.0.0.json`

---

## Example SBOM Generation Workflow

### JavaScript/Node.js Project

**Step 1: Install CycloneDX Generator**
```bash
npm install -g @cyclonedx/cyclonedx-npm
```

**Step 2: Generate SBOM**
```bash
cyclonedx-npm --output-file sbom.json
```

**Step 3: Validate NTIA Minimum Elements**
```bash
# Check that sbom.json includes:
# - component names
# - specific versions
# - purls (pkg:npm/...)
# - timestamp
# - author (tool)
```

**Step 4: Add Vulnerability Data**
```bash
# Query NVD for each component
# Add CVE IDs to sbom.json (CycloneDX "vulnerabilities" field)
```

**Step 5: Store SBOM**
```bash
# Commit to git
git add sbom.json
git commit -m "Add SBOM for v1.0.0"

# Or publish to artifact repository
```

---

## SBOM Analysis & Consumption

### Reading SBOMs

**Tools for SBOM Analysis:**
- **OWASP Dependency-Track:** SBOM ingestion, continuous vulnerability monitoring
- **Grype (Anchore):** Scan SBOM for vulnerabilities
- **OSS Review Toolkit (ORT):** License compliance, policy checks

### Continuous Monitoring with SBOMs

**Workflow:**
1. Generate SBOM during build
2. Upload SBOM to Dependency-Track
3. Dependency-Track monitors NVD for new CVEs
4. Alerts triggered when new CVE affects component in SBOM
5. Create ticket for patching

**Benefits:**
- Don't need to re-scan code (just check SBOM against CVE databases)
- Rapid response to new CVEs (know immediately if you're affected)
- Historical tracking (how long was vulnerable component in production?)

---

**Version:** 2.0
**Last Updated:** 2025-12-02
**Standards:** SPDX 2.3, CycloneDX 1.5, NTIA Minimum Elements
**Purpose:** Complete guide to SBOM generation, validation, and maintenance
