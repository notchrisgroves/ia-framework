---
name: dependency-audit
description: Supply chain security analysis and dependency vulnerabilities
---

# /dependency-audit - Dependency Security Audit

Supply chain security analysis including dependency vulnerabilities, SBOM generation, and third-party risk assessment.

**Agent:** security
**Skill:** dependency-audit
**Output:** `output/engagements/dependency-audits/{project}-{YYYY-MM}/`

---

## Quick Start

```
/dependency-audit
```

Collects project info → Analyzes dependencies for vulnerabilities → Generates SBOM → Assesses supply chain risk

---

## When to Use

✅ **Use /dependency-audit when:**
- Identify vulnerable dependencies in your project
- Generate Software Bill of Materials (SBOM) for compliance
- Assess third-party library security risks
- Prepare for security audits or vendor assessments
- Review supply chain security posture
- Comply with SBOM requirements (Executive Order 14028, etc.)
- Evaluate open-source license risks

❌ **Don't use if:**
- Need code security review → use `/code-review`
- Need configuration hardening → use `/secure-config`
- Need runtime vulnerability scanning → use `/vuln-scan`

---

## Workflow

1. **Context Collection** - Prompts gather project info, audit scope, output format
2. **Dependency Analysis** - Scan dependencies, identify vulnerabilities, map supply chain
3. **Risk Assessment** - Evaluate vulnerability severity, exploitability, license risks
4. **Output** - Generate audit report in `output/engagements/dependency-audits/{project}-{YYYY-MM}/`

**Estimated time:** 20-60 minutes

---

## Context Prompts

### Project Type

**Question:** "What type of project are you auditing?"

**Options:**
- **Node.js/JavaScript** - NPM or Yarn (package.json, package-lock.json)
- **Python** - Python (requirements.txt, Pipfile, pyproject.toml)
- **Java/Maven** - Maven project (pom.xml)
- **Java/Gradle** - Gradle project (build.gradle)
- **Go** - Go project (go.mod)
- **Rust** - Rust project (Cargo.toml)
- **Ruby** - Ruby project (Gemfile)
- **Multiple/Other** - Multiple languages or other ecosystem

**Default:** Node.js/JavaScript

---

### Audit Scope

**Question:** "What should the audit focus on?"

**Options:**
- **Vulnerabilities Only** - Focus on known CVEs and security vulnerabilities
- **Vulnerabilities + Licenses** - Include open-source license analysis
- **Full Supply Chain** - Comprehensive analysis (transitive deps, maintainer trust, typosquatting)

**Default:** Vulnerabilities Only

---

### Dependency Depth

**Question:** "Which dependencies should be analyzed?"

**Options:**
- **Direct Dependencies** - Only top-level dependencies (faster)
- **All Dependencies** - Direct + transitive (recommended)

**Default:** All Dependencies

---

### Severity Threshold

**Question:** "What severity level should trigger findings?"

**Options:**
- **Critical Only** - CVSS 9.0-10.0, urgent issues only
- **High and Above** - CVSS 7.0+ (recommended for production)
- **Medium and Above** - CVSS 4.0+, comprehensive
- **All Severities** - All vulnerabilities including low/informational

**Default:** High and Above

---

### Output Format

**Question:** "What output format do you need?"

**Options:**
- **Markdown Report** - Human-readable report with vulnerability details
- **SBOM (CycloneDX)** - Software Bill of Materials in CycloneDX JSON format
- **SBOM (SPDX)** - Software Bill of Materials in SPDX format
- **All Formats** - Markdown report + both SBOM formats (recommended)

**Default:** All Formats

---

## Agent Routing

```typescript
Task({
  subagent_type: "security",
  model: "sonnet",
  prompt: `
Mode: dependency-audit
Skill: dependency-audit
Workflow: supply-chain-analysis

Context:
- Project Type: {nodejs|python|java-maven|java-gradle|go|rust|ruby|multiple}
- Audit Scope: {vulnerabilities|vulnerabilities-licenses|full-supply-chain}
- Dependency Depth: {direct|all}
- Severity Threshold: {critical|high-above|medium-above|all}
- Output Format: {markdown|cyclonedx|spdx|all}

Instructions:
Execute dependency-audit SKILL.md workflow:
1. Scan dependencies for vulnerabilities
2. Identify license risks (if scope includes licenses)
3. Assess supply chain (if full scope)
4. Generate SBOM
5. Create remediation guide

Output: output/engagements/dependency-audits/{project}-{YYYY-MM}/
`
})
```

---

## Output Structure

```
output/engagements/dependency-audits/{project}-{YYYY-MM}/
├── AUDIT-SUMMARY.md
├── VULNERABILITY-REPORT.md
├── LICENSE-REPORT.md (if scope includes licenses)
├── SUPPLY-CHAIN-ANALYSIS.md (if full scope)
├── REMEDIATION-GUIDE.md
├── sbom/
│   ├── sbom-cyclonedx.json
│   └── sbom-spdx.json
├── dependency-tree/
│   └── dependency-graph.txt
└── evidence/
    └── raw-audit-logs/
```

**Deliverables:**

1. **Audit Summary** - Total dependencies, vulnerability counts by severity, critical findings, overall risk rating

2. **Vulnerability Report** - Each vulnerability with CVE ID, CVSS score, affected dependency, description, exploitability, available fixes, dependency path

3. **License Report** (if applicable) - License distribution, compliance risks, incompatible combinations, dependencies requiring legal review

4. **Supply Chain Analysis** (if full scope) - Maintainer trust, deprecated/unmaintained deps, typosquatting risks, update frequency, single points of failure

5. **Remediation Guide** - Prioritized upgrades, version-specific commands, breaking change warnings, alternative dependencies, compensating controls

6. **SBOM** (if requested) - Component inventory, version/license info, dependency relationships, vulnerability references, compliance-ready format

---

## Examples

### Node.js Vulnerability Audit

```
/dependency-audit
→ Project: Node.js | Scope: Vulnerabilities Only | Severity: High+

Result: 8 vulnerabilities (2 Critical, 6 High) with upgrade commands, SBOMs (~25-35 min)
Output: output/engagements/dependency-audits/webapp-2025-12/
```

### Python Supply Chain Analysis

```
/dependency-audit
→ Project: Python | Scope: Full Supply Chain | Severity: Medium+

Result: 5 vulns, license analysis (2 LGPL concerns), unmaintained deps report (~45-60 min)
Output: output/engagements/dependency-audits/ml-service-2025-12/
```

---

## Security Considerations

**Supply Chain:**
- Vet new dependencies (popularity, maintainers)
- Use lock files
- Enable automated vulnerability alerts (Dependabot/Snyk)

**SBOM Sensitivity:**
- Limit distribution to authorized parties
- Sanitize before external sharing

**Continuous Monitoring:**
- Integrate audits into CI/CD
- Schedule periodic re-audits (monthly/quarterly)

---

## Related Commands

- `/code-review` - Source code security analysis
- `/vuln-scan` - Runtime vulnerability scanning
- `/secure-config` - Infrastructure hardening validation

---

## References

**Standards:**
- CycloneDX: cyclonedx.org
- SPDX: spdx.dev
- NTIA SBOM: ntia.gov/sbom

**Regulations:**
- Executive Order 14028 (Federal SBOM requirement)
- EU Cyber Resilience Act
- NIST Secure Software Development Framework (SSDF)

**Vulnerability Databases:**
- National Vulnerability Database (NVD)
- GitHub Advisory Database
- Snyk Vulnerability Database

---

**Version:** 1.0
**Last Updated:** 2025-12-12
**Framework:** Intelligence Adjacent (IA)
