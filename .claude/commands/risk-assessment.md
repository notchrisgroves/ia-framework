---
name: risk-assessment
description: Formal cybersecurity risk assessment with 22-question structured methodology
---

# /risk-assessment - Cybersecurity Risk Assessment

Formal cybersecurity risk assessment with 22-question structured analysis, compliance framework mapping, and deliverables.

**Agent:** security
**Skill:** security-advisory
**Output:** `output/engagements/risk-assessments/{client}-{YYYY-MM}/`

---

## Quick Start

```
/risk-assessment
```

Collects organization context → Explores library for frameworks → Performs 22-question analysis → Generates deliverables

---

## When to Use

**Use /risk-assessment when:**
- Conduct formal cybersecurity risk assessments
- Evaluate security posture against industry frameworks
- Prepare for compliance audits (SOC 2, ISO 27001, NIST)
- Identify and prioritize security risks
- Develop security roadmaps and remediation plans
- Board-level or executive security reporting

**Don't use if:**
- Quick security question → use `/security-advice`
- Technical vulnerability scanning → use `/vuln-scan`
- Architecture threat modeling → use `/arch-review`
- Code security review → use `/code-review`

---

## Workflow

1. **Context Collection** - Organization info, compliance requirements
2. **Library Research** - Explore `resources/library/` for relevant frameworks
3. **Assessment** - 22-question structured questionnaire
4. **Analysis** - Risk identification, likelihood/impact scoring, gap analysis
5. **Deliverables** - Generate assessment reports

**Estimated time:** 90-180 minutes

---

## Context Prompts

### Organization Context

**Question:** "Provide organization details for context?"

**Options:**
- **Company Name + Industry** - Agent researches context and tailors to industry-specific risks
- **Manual Description** - Describe org size, industry, tech stack manually
- **Anonymous** - No specific org details, generic assessment

**Default:** Company Name + Industry

---

### Assessment Focus

**Question:** "What security domains should the assessment emphasize?"

**Options:**
- **All Domains** - Comprehensive coverage (all 22 questions) - Recommended
- **Governance & Policy** - Questions 1-8 (security program, policies, governance, training)
- **Technical Controls** - Questions 9-16 (access control, encryption, monitoring, vulnerability management)
- **Compliance & Incident Response** - Questions 17-22 (compliance, DR/BC, incident response)

**Default:** All Domains

---

### Compliance Framework

**Question:** "Are there specific compliance frameworks to assess against?"

**Options:**
- **None** - General security best practices
- **SOC 2 Type II** - Service Organization Control 2
- **ISO 27001** - International information security management
- **NIST CSF** - NIST Cybersecurity Framework
- **PCI DSS** - Payment Card Industry Data Security Standard
- **HIPAA** - Health Insurance Portability and Accountability Act

**Multiple selection:** Yes

**Default:** None

---

## Agent Routing

```typescript
Task({
  subagent_type: "security",
  model: "sonnet",
  prompt: `
Skill: security-advisory
Mode: formal-risk-assessment
Workflow: risk-assessment

Context:
- Organization: {company-name|manual|anonymous}
- Focus: {all|governance|technical|compliance}
- Compliance: {none|soc2|iso27001|nist|pci|hipaa}

CRITICAL - LIBRARY EXPLORATION:
┌─────────────────────────────────────────────────────────────────┐
│ BEFORE and DURING assessment, explore resources/library/ for   │
│ relevant frameworks based on compliance requirements:          │
│                                                                 │
│ resources/library/                                              │
│ ├── benchmarks/     (CIS controls for technical questions)     │
│ ├── frameworks/     (NIST, PCI-DSS, HIPAA, GDPR, ISO, etc.)   │
│ │   ├── nist/sp800/ (NIST SP 800-53, 800-61, 800-207, etc.)   │
│ │   ├── pci-dss/    (PCI DSS v4.0.1)                          │
│ │   ├── hipaa/      (HIPAA Simplification)                     │
│ │   ├── gdpr/       (GDPR full text)                          │
│ │   └── owasp/      (ASVS, etc.)                              │
│ ├── repositories/   (OWASP cheatsheets, OSCAL mappings)        │
│ └── methodologies/  (assessment approaches)                    │
│                                                                 │
│ Use Glob/Read to find and load relevant materials.             │
│ Map findings to specific framework control requirements.       │
└─────────────────────────────────────────────────────────────────┘

FLEXIBLE MODEL ESCALATION:
┌─────────────────────────────────────────────────────────────────┐
│ ULTRATHINK (Opus) - Invoke for:                                 │
│ • Designing assessment methodology for unique organizations     │
│ • Complex risk scoring (when factors interact non-linearly)     │
│ • Strategic roadmap design (resource constraints vs risk)       │
│ • Residual risk calculation with control dependencies           │
├─────────────────────────────────────────────────────────────────┤
│ EXECUTION (Sonnet) - Default for:                               │
│ • 22-question questionnaire administration                      │
│ • Standard risk register population                             │
│ • Compliance gap analysis against frameworks                    │
│ • Report writing and documentation                              │
├─────────────────────────────────────────────────────────────────┤
│ QA/CHALLENGE (Grok) - Escalate for:                             │
│ • "What risks am I underestimating?" adversarial review         │
│ • Challenge likelihood/impact assumptions                       │
├─────────────────────────────────────────────────────────────────┤
│ RESEARCH (Perplexity) - Use for:                                │
│ • Industry-specific threat landscape research                   │
│ • Organization context and public incident history              │
└─────────────────────────────────────────────────────────────────┘

Instructions:
Execute security-advisory SKILL.md workflow:
22-question analysis, risk register, roadmap

Output: output/engagements/risk-assessments/{client}-{YYYY-MM}/
`
})
```

---

## Output Structure

```
output/engagements/risk-assessments/{client}-{YYYY-MM}/
├── EXECUTIVE-SUMMARY.md
├── RISK-ASSESSMENT-REPORT.md
├── QUESTIONNAIRE-RESPONSES.md
├── RISK-REGISTER.md
├── REMEDIATION-ROADMAP.md
├── COMPLIANCE-MATRIX.md (if applicable)
└── session-state.md
```

**Deliverables:**

1. **Executive Summary** - Overall risk level, top 5 risks, security program maturity, key recommendations

2. **Risk Assessment Report** - Detailed findings by domain, strengths/weaknesses, industry benchmarking

3. **Questionnaire Responses** - All 22 questions with answers, supporting evidence, gaps, scoring

4. **Risk Register** - Identified risks, likelihood/impact scores, risk level, current mitigations, residual risk

5. **Remediation Roadmap** - Prioritized action items (P0/P1/P2), resource requirements, success metrics

6. **Compliance Matrix** (if applicable) - Control mapping, pass/fail/partial status, gap analysis

---

## Examples

### SOC 2 Assessment

```
/risk-assessment
→ Organization: CloudApp Inc (SaaS)
→ Focus: All Domains
→ Compliance: SOC 2

Result: 22-question assessment, SOC 2 gap analysis, remediation roadmap (~120-150 min)
Output: output/engagements/risk-assessments/cloudapp-inc-2025-12/
```

### Healthcare Compliance

```
/risk-assessment
→ Organization: Regional Health Network
→ Focus: All Domains
→ Compliance: HIPAA, NIST CSF

Result: HIPAA-focused assessment with NIST CSF mapping (~150 min)
Output: output/engagements/risk-assessments/regional-health-2025-12/
```

---

## Security Considerations

**Confidentiality:**
- Limit distribution to authorized personnel
- Mark reports as confidential/privileged
- Consider attorney-client privilege
- Sanitize before external sharing

**Honest Assessment:**
- Don't downplay risks to look better
- Document gaps even if embarrassing
- Assessment informs improvement, not blame

---

## Related Commands

- `/security-advice` - Quick security guidance (no formal deliverables)
- `/arch-review` - Architecture threat modeling
- `/secure-config` - Infrastructure hardening validation
- `/pentest` - Technical security testing
- `/vuln-scan` - Automated vulnerability scanning

---

## References

**Library Resources:**
- `resources/library/frameworks/nist/` - NIST SP 800 series
- `resources/library/frameworks/pci-dss/` - PCI DSS v4.0.1
- `resources/library/frameworks/hipaa/` - HIPAA requirements
- `resources/library/benchmarks/cis/` - CIS Controls

**External:**
- NIST Cybersecurity Framework: nist.gov/cyberframework
- ISO 27001: iso.org/iso-27001-information-security.html
- SOC 2: aicpa.org/soc2
- PCI DSS: pcisecuritystandards.org
- HIPAA Security Rule: hhs.gov/hipaa

---

**Version:** 2.0
**Last Updated:** 2025-12-19
**Framework:** Intelligence Adjacent (IA)
