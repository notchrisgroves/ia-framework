---
name: compliance
description: Legal compliance review with mandatory citation verification (HIPAA, PCI DSS, GDPR, SOC 2)
---

# /compliance - Legal Compliance Review

Legal information and compliance review with mandatory citation verification. All legal claims verified via dual-model approach.

**Agent:** legal
**Skill:** legal
**Output:** `output/compliance/{regulation}-{topic}-{YYYY-MM-DD}.md`

---

## CRITICAL DISCLAIMER

> **THIS IS NOT LEGAL ADVICE. THIS IS LEGAL INFORMATION ONLY.**
>
> This provides general legal information based on publicly available sources. It does NOT create an attorney-client relationship, provide legal advice for your specific situation, or guarantee compliance. **For legal advice, consult a licensed attorney.**

---

## Quick Start

```
/compliance review for HIPAA security requirements
```

**Examples:**
```
/compliance PCI DSS assessment for e-commerce
/compliance GDPR data processing requirements
/compliance SOC 2 Type II preparation
/compliance penetration test authorization requirements
```

---

## When to Use

**Use /compliance when:**
- Reviewing regulatory compliance requirements
- Understanding HIPAA, PCI DSS, GDPR, SOC 2 obligations
- Assessing compliance gaps
- Preparing authorization documentation
- Jurisdictional research for security testing

**Don't use if:**
- Need legal advice for specific situation (consult attorney)
- Active litigation or legal dispute
- Contract negotiation

---

## Supported Regulations

| Regulation | Focus Area |
|------------|------------|
| **HIPAA** | Healthcare data protection |
| **PCI DSS** | Payment card security |
| **GDPR** | EU data protection |
| **CCPA** | California privacy |
| **SOC 2** | Service organization controls |
| **FERPA** | Educational records |
| **GLBA** | Financial privacy |
| **CFAA** | Computer fraud (security testing) |

---

## Workflow

### Phase 1: Identify Requirements
- Determine applicable laws and regulations
- Identify jurisdiction(s)
- Scope assessment

### Phase 2: Gap Analysis
- Compare current state to legal requirements
- Identify specific requirement gaps
- Map to regulation sections

### Phase 3: Risk Assessment
- Identify compliance gaps
- Assess legal and operational risks
- Prioritize remediation

### Phase 4: Recommendations
- Remediation guidance with **verified citations**
- Implementation priorities
- Documentation requirements

### Phase 5: Deliverables
- Compliance checklist with citations
- Gap analysis report
- Remediation recommendations

---

## Citation Verification

**All legal claims verified via dual-model approach:**
1. Claude provides initial analysis with citations
2. Grok AI verifies citations exist and are accurate
3. Non-existent cases/statutes flagged and removed

**This prevents:**
- Hallucinated court cases
- Non-existent regulations
- Incorrect statute citations
- Fabricated legal precedents

---

## Web Search Integration

**For current information:**
- Latest regulatory updates and amendments
- Recent enforcement actions
- Current guidance documents
- Industry interpretation updates
- Case law developments

**Search sources:**
- Official regulatory websites (HHS, PCI SSC, ICO)
- Federal/state register updates
- Legal databases (public access)
- Industry compliance guides

---

## Agent Routing

```typescript
Task({
  subagent_type: "legal",
  model: "sonnet",
  prompt: `
Mode: compliance
Skill: legal
Workflow: compliance-review

Regulation: {regulation}
Scope: {topic or assessment area}

Instructions:
1. Include MANDATORY disclaimer
2. Identify applicable requirements
3. Conduct gap analysis
4. Verify ALL citations via Grok AI
5. Provide recommendations with sources

Output: output/compliance/{regulation}-{topic}-{YYYY-MM-DD}.md
`
})
```

---

## Output Structure

```
output/compliance/{regulation}-{topic}-{YYYY-MM-DD}/
├── COMPLIANCE-REVIEW.md      # Full analysis with citations
├── GAP-ANALYSIS.md           # Requirements vs current state
└── REMEDIATION-PLAN.md       # Prioritized recommendations
```

---

## Examples

### HIPAA Security
```
/compliance HIPAA security rule requirements for cloud storage

→ Administrative, Physical, Technical safeguards
→ Gap analysis against requirements
→ Verified citations to 45 CFR 164
→ Remediation priorities
```

### PCI DSS
```
/compliance PCI DSS v4.0 requirements for e-commerce

→ 12 requirements analysis
→ SAQ type determination
→ Gap identification
→ Implementation guidance
```

### Security Testing Authorization
```
/compliance legal requirements for penetration testing

→ CFAA considerations
→ Authorization documentation requirements
→ State law variations
→ Template authorization language
```

---

## Related Commands

- `/risk-assessment` - Cybersecurity risk assessment
- `/secure-config` - Technical hardening (CIS/STIG)
- `/pentest` - Authorized security testing

---

**Version:** 1.0
**Last Updated:** 2025-12-19
**Framework:** Intelligence Adjacent (IA)
