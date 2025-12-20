---
name: arch-review
description: Architecture security review with threat modeling
---

# /arch-review - Architecture Security Review

System design security analysis covering threat modeling, secure architecture patterns, and defense-in-depth validation.

**Agent:** security
**Skill:** architecture-review
**Output:** `output/engagements/arch-reviews/{project}-{YYYY-MM}/`

---

## Quick Start

```
/arch-review
```

Collects architecture documentation → Performs security analysis and threat modeling → Generates architecture security assessment

---

## When to Use

✅ **Use /arch-review when:**
- Review system architecture for security vulnerabilities
- Perform threat modeling (STRIDE, PASTA, attack trees)
- Validate defense-in-depth controls
- Assess security architecture patterns
- Review cloud architecture security (AWS, Azure, GCP)
- Prepare for security audits or compliance reviews
- Design review before implementation

❌ **Don't use if:**
- Need code-level review → use `/code-review`
- Need configuration hardening → use `/secure-config`
- Need runtime testing → use `/pentest` or `/vuln-scan`

---

## Workflow

1. **Context Collection** - Prompts gather architecture docs, system type, review focus
2. **Analysis** - Architecture decomposition, trust boundary identification, threat modeling
3. **Assessment** - Security control validation, defense-in-depth analysis, recommendations
4. **Output** - Generate review report in `output/engagements/arch-reviews/{project}-{YYYY-MM}/`

**Estimated time:** 60-180 minutes

---

## Context Prompts

### Architecture Documentation

**Question:** "How will you provide architecture documentation?"

**Options:**
- **Architecture Diagram** - Visio/Lucidchart/draw.io diagram file path
- **Written Documentation** - Markdown/PDF describing architecture
- **Code Repository** - Infrastructure-as-code (Terraform, CloudFormation, K8s)
- **Live System** - Describe running system (when formal docs don't exist)

**Multiple selection:** Yes

**Default:** Architecture Diagram

---

### System Type

**Question:** "What type of system are you reviewing?"

**Options:**
- **Web Application** - Multi-tier web app (frontend, API, database)
- **Cloud Infrastructure** - AWS/Azure/GCP architecture
- **Microservices** - Distributed microservices architecture
- **Mobile + Backend** - Mobile app with backend services
- **IoT/Embedded** - IoT devices with cloud backend
- **Enterprise Network** - Corporate network architecture

**Default:** Web Application

---

### Threat Modeling Methodology

**Question:** "Which threat modeling approach should be used?"

**Options:**
- **STRIDE** - Microsoft methodology (Spoofing, Tampering, Repudiation, Information Disclosure, DoS, Elevation of Privilege)
- **PASTA** - Process for Attack Simulation and Threat Analysis (risk-centric)
- **Attack Trees** - Visual representation of attack paths
- **All Methods** - Comprehensive threat modeling (recommended for critical systems)

**Default:** STRIDE

---

### Review Focus

**Question:** "What security aspects should the review emphasize?"

**Options:**
- **Trust Boundaries** - Validate trust boundaries, data flow across zones, boundary controls
- **Authentication/Authorization** - Identity management, access control, privilege models
- **Data Protection** - Encryption at rest/transit, key management, PII handling
- **Network Security** - Segmentation, firewall rules, DDoS protection
- **Resilience** - High availability, disaster recovery, fault tolerance
- **All Areas** - Comprehensive coverage (recommended)

**Multiple selection:** Yes

**Default:** All Areas

---

### Compliance Requirements

**Question:** "Are there specific compliance frameworks to assess against?"

**Options:**
- **None** - General security best practices only
- **PCI DSS** - Payment Card Industry Data Security Standard
- **HIPAA** - Health Insurance Portability and Accountability Act
- **SOC 2** - Service Organization Control 2
- **ISO 27001** - Information security management
- **NIST** - NIST Cybersecurity Framework or NIST 800-53

**Multiple selection:** Yes

**Default:** None

---

## Agent Routing

```typescript
// FLEXIBLE MODEL SELECTION (per library/model-selection-matrix.md):
//
// DEFAULT WORKFLOW: Sonnet executes, escalate strategically
//
// ULTRATHINK (Opus) - Strategic escalation points:
// ┌─────────────────────────────────────────────────────────────┐
// │ • Threat modeling methodology design (STRIDE/PASTA/Trees)   │
// │ • Complex attack path reasoning across trust boundaries     │
// │ • Defense-in-depth gap analysis                             │
// │ • When standard analysis misses something                   │
// └─────────────────────────────────────────────────────────────┘
//
// EXECUTION: Sonnet (decomposition, documentation, control mapping)
// QA/CHALLENGE: Grok (adversarial review of threat model completeness)
// VALIDATION: Haiku (compliance checklists, standards verification)

Task({
  subagent_type: "security",
  model: "sonnet",  // Default - escalate to opus/grok as needed
  prompt: `
Mode: architecture-review
Skill: architecture-review
Workflow: threat-modeling

Context:
- Documentation: {diagram|written|iac|live-system}
- System Type: {web-app|cloud|microservices|mobile|iot|enterprise-network}
- Threat Modeling: {stride|pasta|attack-trees|all}
- Focus Areas: {trust-boundaries|auth|data-protection|network|resilience|all}
- Compliance: {none|pci-dss|hipaa|soc2|iso27001|nist}

FLEXIBLE MODEL ESCALATION:
┌─────────────────────────────────────────────────────────────────┐
│ ULTRATHINK (Opus) - Invoke for:                                 │
│ • Designing threat modeling approach for complex architectures  │
│ • Multi-path attack chain reasoning (attacker thinks 3 steps)   │
│ • Novel threat identification beyond standard frameworks        │
│ • Defense-in-depth gap analysis (what's the weak link?)         │
│ • When initial analysis feels incomplete or surface-level       │
├─────────────────────────────────────────────────────────────────┤
│ EXECUTION (Sonnet) - Default for:                               │
│ • Architecture decomposition and component mapping              │
│ • Trust boundary identification                                 │
│ • Security control inventory                                    │
│ • Report writing and documentation                              │
│ • Standard STRIDE/PASTA application                             │
├─────────────────────────────────────────────────────────────────┤
│ QA/CHALLENGE (Grok) - Escalate for:                             │
│ • "Did I miss any attack paths?" adversarial review             │
│ • Challenge assumptions in threat model                         │
│ • Second opinion on defense-in-depth adequacy                   │
│ • Reasoning traces on why a control is/isn't sufficient         │
├─────────────────────────────────────────────────────────────────┤
│ VALIDATION (Haiku) - Use for:                                   │
│ • Compliance framework checklist (PCI, HIPAA, SOC2, etc.)       │
│ • Standards verification against CIS/NIST                       │
│ • Quick structural validation                                   │
└─────────────────────────────────────────────────────────────────┘

Instructions:
Execute architecture-review SKILL.md workflow:
1. Architecture decomposition
2. Trust boundary identification
3. Threat modeling
4. Security control validation
5. Defense-in-depth analysis

Output: output/engagements/arch-reviews/{project}-{YYYY-MM}/
`
})
```

---

## Output Structure

```
output/engagements/arch-reviews/{project}-{YYYY-MM}/
├── EXECUTIVE-SUMMARY.md
├── ARCHITECTURE-ANALYSIS.md
├── THREAT-MODEL.md
├── FINDINGS.md
├── RECOMMENDATIONS.md
├── COMPLIANCE-ASSESSMENT.md (if applicable)
├── diagrams/
│   ├── architecture-annotated.png
│   ├── trust-boundaries.png
│   ├── data-flow-diagram.png
│   └── attack-trees/
└── session-state.md
```

**Deliverables:**

1. **Executive Summary** - Overall security posture, critical risks (top 5), architecture strengths, key recommendations

2. **Architecture Analysis** - Component inventory, trust boundary identification, data flow mapping, entry/exit points, attack surface

3. **Threat Model** - Threats identified per methodology, threat scenarios with attack paths, likelihood/impact ratings, existing mitigations, residual risk

4. **Findings** - Architecture vulnerabilities by severity, missing security controls, insecure patterns, single points of failure, defense-in-depth gaps

5. **Recommendations** - Prioritized improvements (P0/P1/P2), secure architecture patterns, control implementations, design changes, cost/effort estimates

6. **Compliance Assessment** (if applicable) - Compliance gap analysis, control mapping, pass/fail status, remediation roadmap

---

## Examples

### Web Application STRIDE Review

```
/arch-review
→ Documentation: Architecture Diagram + Design Docs | Type: Web Application | Method: STRIDE

Result: Threat model with trust boundaries, 15 threats identified (~60-90 min)
Output: output/engagements/arch-reviews/webapp-2025-12/
```

### AWS Infrastructure Review (SOC 2)

```
/arch-review
→ Documentation: Terraform Code | Type: Cloud Infrastructure | Method: Attack Trees | Compliance: SOC 2

Result: Security architecture review with attack trees, SOC 2 gaps (~90-120 min)
Output: output/engagements/arch-reviews/aws-2025-12/
```

---

## Security Considerations

**Documentation Sensitivity:**
- Sanitize diagrams before external sharing
- Redact internal IP addresses, hostnames
- Remove proprietary technology details if needed
- Follow data classification policies

**Threat Disclosure:**
- Limit distribution to authorized personnel
- Use findings to improve security, not exploit
- Coordinate remediation timeline
- Document threats for security awareness

**Design Changes:**
- Involve stakeholders in remediation planning
- Assess cost/complexity of recommendations
- Balance security with business requirements
- Prioritize defense-in-depth

---

## Related Commands

- `/code-review` - Code-level security review
- `/secure-config` - Infrastructure hardening validation
- `/risk-assessment` - Formal cybersecurity risk assessment
- `/pentest` - Runtime security testing

---

## References

**Threat Modeling:**
- STRIDE: Microsoft threat modeling methodology
- PASTA: Process for Attack Simulation and Threat Analysis
- Attack Trees: Schneier's attack tree methodology

**Secure Architecture:**
- OWASP Application Security Architecture
- NIST 800-160 Systems Security Engineering
- Cloud Security Alliance (CSA) guidelines

**Compliance:**
- PCI DSS, HIPAA, SOC 2, ISO 27001

---

**Version:** 1.0
**Last Updated:** 2025-12-12
**Framework:** Intelligence Adjacent (IA)
