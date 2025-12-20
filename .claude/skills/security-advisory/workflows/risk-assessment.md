# Risk Assessment Workflow

**Mode 1: Formal structured 22-question interview with comprehensive deliverables**

---

## Phase 1: Interview (22 Questions in 6 Categories)

**1. Organization Overview (3 questions)**
- Industry, size, business model
- Critical assets and data
- Regulatory requirements

**2. Current Security Posture (4 questions)**
- Existing security controls
- Security team structure
- Security tools in use
- Recent security incidents

**3. Technical Infrastructure (4 questions)**
- Network architecture
- Cloud vs on-premise
- Authentication mechanisms
- Data storage and backup

**4. Compliance & Governance (3 questions)**
- Compliance frameworks (HIPAA, PCI-DSS, GDPR, SOC 2)
- Security policies in place
- Audit history

**5. Incident Response & Recovery (4 questions)**
- Incident response plan
- Disaster recovery procedures
- Business continuity planning
- Backup and recovery testing

**6. Risk Priorities (4 questions)**
- Biggest security concerns
- Budget constraints
- Timeline expectations
- Success metrics

**Document answers in `01-intake/interview-responses.md` (MANDATORY):**
- Include: Organization name, date, contact person, title, industry
- Document all 22 answers with full context
- This is your primary engagement record (Critical Rule #2)
- Template: `../templates/interview-responses-template.md`

---

## Phase 2: OSINT Research & Framework Loading

**Step 1: Delegate OSINT Research**

```markdown
**DELEGATE to osint-research skill:**

**Caller:** security-advisory
**Mode:** fast (30-45 min for risk assessment)

**Research Plan:**
  - Industry threat landscape (recent breaches, attack trends, threat actors targeting this industry)
  - Regulatory requirements (HIPAA, PCI-DSS, GDPR, CCPA, SOX, industry-specific regulations)
  - Recent breach trends in client's industry (last 12-24 months)
  - Competitor security posture (public incidents, certifications, compliance disclosures)
  - Compliance framework documentation (NIST CSF, CIS Controls, ISO 27001)

**Output:** output/engagements/advisory/{client}/02-research/intelligence-summary.md

osint-research executes industry research using dual-source methodology (WebSearch + Grok).
```

**Step 2: Framework Loading**

**Multi-Location Reference Search Pattern:**
1. **Primary:** `../reference/` (bundled public frameworks)
2. **Secondary:** `../../resources/reference/` (user-added private materials)
3. **Fallback:** WebFetch for latest framework updates

**Load frameworks based on industry:**
- **Healthcare:** HIPAA Security Rule, NIST 800-66
- **Financial:** FFIEC, PCI-DSS, SOX IT controls
- **Retail/E-commerce:** PCI-DSS, GDPR/CCPA
- **General Business:** NIST CSF, CIS Controls, ISO 27001

**See:** `../reference/README.md` for complete framework inventory

**Step 3: Document Findings**

Update `02-research/intelligence-summary.md` with:
- Industry threat landscape findings (from osint-research)
- Regulatory requirements identified
- Framework selections and rationale
- Competitor security posture analysis

---

## Phase 3: Deliverable Generation

**3 Core Deliverables:**

1. **Security Assessment Report** (comprehensive)
   - Executive Summary
   - Current State Analysis
   - Risk Assessment Matrix
   - Gap Analysis (current vs desired state)
   - Compliance Mapping (NIST, CIS, ISO 27001)
   - Prioritized Recommendations

2. **120-Day Action Plan** (tactical roadmap)
   - **Days 1-30:** Quick wins (low-hanging fruit, immediate risk reduction)
   - **Days 31-60:** Foundation building (policies, processes, core controls)
   - **Days 61-90:** Advanced controls (monitoring, detection, response)
   - **Days 91-120:** Continuous improvement (optimization, automation)

3. **Implementation Checklist** (operational)
   - Prioritized action items
   - Resource requirements (people, budget, tools)
   - Budget estimates
   - Success metrics and KPIs
   - Timeline milestones

**Note:** All 3 deliverable templates include built-in Document Control revision tracking tables (added 2025-11-25) for tracking updates, annual assessments, and milestone adjustments. See `../templates/README.md` for details on revision tracking features.

**Deliverable Templates:** `../templates/deliverables/`

**Final deliverables output to `03-deliverables/`:**
- All 3 deliverables based on interview answers and OSINT research
- Document Control tables completed with engagement metadata
- Cross-reference interview-responses.md for answer traceability

---

## Risk Assessment Matrix

| Risk Level | Likelihood | Impact | Action Required |
|------------|------------|--------|-----------------|
| Critical | High | High | Immediate (0-7 days) |
| High | High | Medium | Urgent (1-30 days) |
| Medium | Medium | Medium | Planned (31-90 days) |
| Low | Low | Low | Monitored (90+ days) |

---

## Compliance Frameworks

**Primary Frameworks:**
- **NIST CSF** - Identify, Protect, Detect, Respond, Recover
- **CIS Controls** - Critical security controls
- **ISO 27001** - Information security management
- **NIST 800-53** - Security and privacy controls

**Industry-Specific:**
- **HIPAA** - Healthcare
- **PCI-DSS** - Payment processing
- **GDPR** - Data privacy (EU)
- **SOC 2** - Service organizations
- **FFIEC** - Financial institutions

---

## Output Structure

```
output/engagements/risk-assessments/[client-name]-[YYYY-MM]/
├── 01-intake/
│   └── interview-responses.md
├── 02-research/
│   └── intelligence-summary.md
├── 03-deliverables/
│   ├── Security-Assessment-Report.md
│   ├── 120-Day-Action-Plan.md
│   └── Implementation-Checklist.md
└── 04-presentation/
    └── executive-briefing.md
```

---

**See Also:**
- `../templates/deliverables/` - Deliverable templates
- `../reference/README.md` - Framework loading architecture
- `../templates/README.md` - Policy templates library
