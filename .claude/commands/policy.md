---
name: policy
description: Multi-framework security policy generation with intelligent defaults and compliance citations
---

# /policy - Security Policy Generation

Generate organization-specific security policies that satisfy multiple compliance frameworks with multi-framework citations.

**Agent:** security
**Skill:** security-advisory (policy-generation mode)
**Output:** `output/engagements/policy-generation/{client}-{YYYY-MM}/`

---

## Quick Start

```
/policy
```

**Or with context:**
```
/policy generate policies for healthcare organization (HIPAA, SOC 2)
/policy PCI DSS and GLBA policies for credit union
/policy create security policy suite for SaaS startup
```

---

## When to Use

**Use /policy when:**
- Need complete security policy suite for organization
- Preparing for compliance audit (SOC 2, ISO 27001, PCI DSS)
- Building policies that satisfy multiple frameworks
- Starting from scratch or enhancing existing policies
- Need framework-specific citations in policies

**Don't use if:**
- Need risk assessment first → `/risk-assessment`
- Quick security question → `/security-advice`
- Need legal review of policies → `/compliance`

---

## Supported Frameworks

| Framework | Industry |
|-----------|----------|
| NIST CSF 2.0 | All organizations |
| ISO 27001:2022 | Certification-seeking |
| CIS Controls v8.1 | Implementation guide |
| SOC 2 Type II | Service providers |
| PCI DSS v4.0.1 | Payment card processing |
| HIPAA Security Rule | Healthcare |
| GLBA Safeguards | Financial services |
| GDPR | EU data processing |
| CCPA/CPRA | California consumers |
| NIST SP 800-171 | Government contractors |
| CMMC | Defense contractors |

---

## Policy Templates (25)

**Core Governance:**
- Information Security Policy
- Risk Management Policy
- Access Control / Identity Management
- Data Classification & Protection
- Incident Response Policy

**Technical Security:**
- Network Security Policy
- Encryption Standard
- Vulnerability Management
- Configuration Management
- Logging & Monitoring

**Operational:**
- Third-Party Risk Management
- Business Continuity & Disaster Recovery
- Security Awareness Training
- Password Standard
- Privileged Access Management

**Industry-Specific:**
- Privacy Management (GDPR/CCPA)
- Physical Security (HIPAA/PCI)
- Database Security
- Mobile Device Management
- Cloud Security

See `skills/security-advisory/templates/policies/` for complete list.

---

## Workflow Phases

### Phase 1: Framework Identification
- Industry and regulatory requirements
- Organization size and structure
- Data types handled
- Compliance mandates

### Phase 2: Policy Requirement Analysis
- Determine required policies per framework
- Priority scoring by framework overlap
- Identify high-impact policies first

### Phase 3: Customization
- Collect organization variables
- Apply intelligent defaults by org size
- Industry-specific customizations

### Phase 4: Generation
- Load base templates
- Insert framework citations
- Apply organization customizations
- Generate compliance matrix

### Phase 5: Validation
- Verify all framework requirements covered
- No orphaned requirements
- Consistent terminology

---

## Web Search Integration

**For current information:**
- Latest framework version updates
- Recent regulatory changes
- Industry-specific requirements
- Best practice updates
- Audit trends and focus areas

**Search sources:**
- NIST publications
- PCI Security Standards Council
- HHS (HIPAA)
- ISO standards updates
- Industry compliance guides

---

## Agent Routing

```typescript
Task({
  subagent_type: "security",
  model: "sonnet",
  prompt: `
Mode: policy
Skill: security-advisory
Workflow: policy-generation

Instructions:
1. Identify applicable frameworks
2. Determine required policies
3. Collect organization variables
4. Generate policies with citations
5. Validate completeness

Output: output/engagements/policy-generation/{client}-{YYYY-MM}/
`
})
```

---

## Output Structure

```
output/engagements/policy-generation/{client}-{YYYY-MM}/
├── policies/
│   ├── 01_information_security_policy.md
│   ├── 02_risk_management_policy.md
│   ├── 03_access_control_policy.md
│   └── ... (15-25 policies)
├── framework_compliance_matrix.xlsx
└── policy_generation_report.md
```

---

## Execution Modes

### Mode 1: Full Generation (Greenfield)
- No existing policies
- Generate complete suite
- 2-4 hours

### Mode 2: Incremental Enhancement
- Existing policies need framework additions
- Add citations and requirements
- 30-60 min per policy

### Mode 3: Framework-Specific Pack
- Preparing for specific audit
- Generate only required policies
- 3-6 hours

### Mode 4: Policy Refresh
- Annual review or framework update
- Generate change summary
- 1-2 hours

---

## Examples

### Healthcare Organization
```
/policy HIPAA and SOC 2 policies for 200-person healthcare SaaS

→ Framework Selection: HIPAA Security Rule, SOC 2 Type II, NIST CSF
→ Required Policies: 18
→ Industry-specific: ePHI handling, BAA requirements
→ Output: Complete policy suite with framework citations
```

### Financial Services
```
/policy PCI DSS and GLBA for credit union

→ Framework Selection: PCI DSS v4.0.1, GLBA, NIST CSF, FFIEC
→ Required Policies: 20
→ Industry-specific: Cardholder data, member information
→ Output: Audit-ready policy package
```

---

## Related Commands

- `/risk-assessment` - Formal security assessment (do first if unsure of gaps)
- `/security-advice` - Quick security guidance
- `/compliance` - Legal compliance review
- `/secure-config` - Technical hardening (CIS/STIG)

---

**Version:** 1.0
**Last Updated:** 2025-12-19
**Framework:** Intelligence Adjacent (IA)
