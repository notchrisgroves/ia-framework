# Architecture Review - Output Structure

**Progressive context file - Load when organizing architecture review deliverables**

This document covers the directory organization, file naming, and output formats for architecture reviews.

---

## Directory Structure

### Standard Architecture Review Output

```
output/engagements/architecture-reviews/[client]-[YYYY-MM]/
├── SCOPE.md                          # Review scope and objectives
├── README.md                         # Engagement overview and quick links
├── # Multi-session tracking in `sessions/                  # Multi-session progress tracking
├── 01-discovery/
│   ├── architecture-diagrams/        # Logical, physical, network topology
│   ├── technical-specs/              # Tech stack, API specs, IaC
│   └── business-context.md           # Sensitivity, compliance, threat actors
├── 02-threat-modeling/
│   ├── threat-register.md            # Complete threat documentation
│   ├── threat-model-diagram.png      # Architecture with threat annotations
│   ├── STRIDE-analysis.md            # Detailed STRIDE analysis
│   └── attack-trees/                 # Attack tree diagrams (if applicable)
├── 03-findings/
│   ├── findings-register.md          # All security weaknesses
│   ├── design-review-notes.md        # Design validation notes
│   └── screenshots/                  # Supporting evidence
├── 04-compliance/
│   ├── NIST-800-160-compliance.md    # NIST SP 800-160 validation
│   ├── OWASP-ASVS-compliance.md      # OWASP ASVS validation
│   ├── PCI-DSS-compliance.md         # PCI DSS (if applicable)
│   └── HIPAA-compliance.md           # HIPAA (if applicable)
├── 05-reporting/
│   ├── defense-in-depth-report.md    # Complete architecture review
│   ├── recommendations-roadmap.md    # Prioritized improvements
│   ├── executive-summary.md          # High-level summary for stakeholders
│   └── presentation.pptx             # Executive presentation (optional)
└── COMPLETION-SUMMARY.md             # Final deliverable summary
```

---

## File Naming Conventions

### General Rules

- **Dates:** YYYY-MM-DD format (e.g., 2025-12-02)
- **Client names:** Lowercase, hyphens (e.g., acme-corp, example-inc)
- **Descriptive names:** Clear, concise, no spaces (use hyphens)
- **Versioning:** If multiple iterations, append v1, v2, v3

### Examples

**Good:**
- `acme-corp-2025-12/`
- `threat-register.md`
- `NIST-800-160-compliance.md`
- `architecture-diagram-v2.png`

**Bad:**
- `Acme Corp December/` (spaces, not ISO date)
- `threats.md` (not descriptive)
- `compliance.md` (which standard?)
- `diagram final FINAL v3 (1).png` (unclear versioning)

---

## Key Files Explained

### SCOPE.md

**Purpose:** Define review boundaries and objectives

**Contents:**
- Systems in scope (components, services, boundaries)
- Systems out of scope
- Objectives (threat modeling, compliance validation, etc.)
- Constraints (time, budget, access limitations)
- Assumptions (threat actors, risk tolerance)

**Template:**
```markdown
# Architecture Review Scope

**Client:** [Client Name]
**Date:** [YYYY-MM-DD]

## In Scope
- [System/Component 1]
- [System/Component 2]

## Out of Scope
- [System/Component]

## Objectives
1. [Objective 1]
2. [Objective 2]

## Constraints
- [Constraint 1]
- [Constraint 2]

## Assumptions
- [Assumption 1]
- [Assumption 2]
```

---

### README.md

**Purpose:** Engagement overview and navigation

**Contents:**
- Client and engagement details
- Review status (In Progress / Complete)
- Quick links to key deliverables
- Timeline and milestones
- Team members and roles

**Template:**
```markdown
# Architecture Review - [Client Name]

**Status:** ✅ Complete / 🚧 In Progress
**Start Date:** [YYYY-MM-DD]
**Completion Date:** [YYYY-MM-DD]

## Overview
[Brief description of architecture reviewed]

## Key Deliverables
- [Threat Model](02-threat-modeling/threat-register.md)
- [Findings Register](03-findings/findings-register.md)
- [Final Report](05-reporting/defense-in-depth-report.md)

## Timeline
- Discovery: [YYYY-MM-DD]
- Threat Modeling: [YYYY-MM-DD]
- Design Validation: [YYYY-MM-DD]
- Reporting: [YYYY-MM-DD]

## Team
- **Lead:** [Name]
- **Architect:** [Name]
```

---

### threat-register.md

**Purpose:** Complete threat documentation

**Format:** Markdown table with threat details

**Columns:**
- Threat ID (T-001, T-002, etc.)
- Category (STRIDE: Spoofing, Tampering, etc.)
- Severity (Critical/High/Medium/Low)
- Description (attack scenario)
- Affected Components
- Risk Score (1-10, if DREAD used)
- Existing Mitigations (current controls)
- Recommended Mitigations (improvements)

**See:** `templates/threat-model.md` for complete template

---

### findings-register.md

**Purpose:** All security weaknesses identified during design validation

**Format:** Markdown table with finding details

**Columns:**
- Finding ID (F-001, F-002, etc.)
- Category (Authentication, Authorization, Cryptography, etc.)
- Severity (Critical/High/Medium/Low)
- Description (what is the weakness)
- Affected Components
- Standard Reference (NIST, OWASP, CSA citation)
- Recommended Mitigation (how to fix)

**Template:**
```markdown
# Findings Register

| Finding ID | Category | Severity | Description | Components | Standard | Recommendation |
|---|---|---|---|---|---|---|
| F-001 | Authentication | High | No MFA | Auth service | OWASP ASVS V2.2.1 | Implement MFA |
```

---

### defense-in-depth-report.md

**Purpose:** Comprehensive architecture security review report

**Contents:**
- Executive summary
- Architecture overview
- Threat modeling analysis
- Design validation findings
- Defense-in-depth analysis
- Standards compliance
- Recommendations roadmap

**See:** `templates/review-report.md` for complete template

---

### recommendations-roadmap.md

**Purpose:** Prioritized list of security improvements

**Format:** Markdown tables organized by priority

**Priorities:**
- **Critical:** Immediate action required (days)
- **High:** Implement within 30 days
- **Medium:** Implement within 90 days
- **Low:** Implement when resources available
- **Quick Wins:** Low effort, high impact

**Columns:**
- Rec ID (R-001, R-002, etc.)
- Recommendation
- Impact (High/Medium/Low)
- Effort (Hours/Days/Weeks)
- Timeline
- Owner (team/person responsible)

---

### # Multi-session tracking in `sessions/

**Purpose:** Track progress in multi-session reviews

**Contents:**
- Current phase and status
- Completed phases with timestamps
- Files created
- Next actions
- Open questions

**Template:**
```markdown
# Session State - Architecture Review

**Last Updated:** [YYYY-MM-DD HH:MM]

## Current Phase

**Phase 2: Design Validation** - In Progress

## Completed Phases

### Phase 1: Threat Modeling - COMPLETE
**Completion:** 2025-12-02 14:30
**Threats Identified:** 15 threats (3 Critical, 5 High, 4 Medium, 3 Low)
**Files Created:**
- `02-threat-modeling/threat-register.md`
- `02-threat-modeling/threat-model-diagram.png`

## Next Actions
1. Complete design validation (authentication, authorization, cryptography)
2. Document findings in findings-register.md
3. Proceed to Phase 3 (Defense-in-Depth)

## Open Questions
- [Question 1]
- [Question 2]
```

---

## Diagram Formats

### Supported Formats

**Recommended:**
- PNG (architecture diagrams, threat models)
- SVG (scalable diagrams)
- PDF (multi-page diagrams, if necessary)

**Tools:**
- draw.io (free, supports PNG/SVG export)
- Lucidchart (professional, cloud-based)
- Microsoft Visio (enterprise standard)
- PlantUML (text-based, version-controlled)

### Diagram Types

**1. Logical Architecture Diagram**
- Components and their relationships
- Data flows
- Trust boundaries

**2. Physical Architecture Diagram**
- Servers, databases, load balancers
- Network topology
- Security controls (firewalls, WAF, IDS/IPS)

**3. Network Topology Diagram**
- VLANs, subnets, security groups
- Firewall rules (high-level)
- DMZ, internal, restricted zones

**4. Data Flow Diagram (DFD)**
- Data sources and destinations
- Processing locations
- Security controls per flow

**5. Threat Model Diagram**
- Architecture with threat annotations
- Attack vectors (arrows with threat IDs)
- Trust boundaries highlighted

---

## Export Formats

### Markdown Reports (Primary)

**Advantages:**
- Version-controlled (Git)
- Human-readable
- Easy to search and edit
- Platform-independent

**Use for:** All documentation (threat register, findings, reports)

---

### JSON Exports (Optional)

**Use for:** Automation and integration

**Examples:**
- ATT&CK Navigator layers (threat-model-attck.json)
- Findings export for bug tracking systems
- Compliance validation results

**Format:**
```json
{
  "findings": [
    {
      "id": "F-001",
      "category": "Authentication",
      "severity": "High",
      "description": "No MFA on admin accounts",
      "recommendation": "Implement MFA (TOTP, WebAuthn)"
    }
  ]
}
```

---

### PDF Reports (Client Deliverable)

**Use for:** Executive presentations, final client deliverable

**Generate from:** Markdown reports (using pandoc, Markdown PDF extension)

**Advantages:**
- Professional appearance
- Easy to share
- Preserves formatting

**Disadvantages:**
- Not version-controlled
- Difficult to edit
- Not searchable (without OCR)

---

### PowerPoint Presentations (Optional)

**Use for:** Executive briefings, stakeholder presentations

**Contents:**
- Executive summary (2-3 slides)
- Architecture overview (1 slide)
- Threat model highlights (2-3 slides)
- Key findings (3-5 slides)
- Recommendations (2-3 slides)

**Keep concise:** 10-15 slides maximum

---

## Compliance-Specific Outputs

### PCI DSS Architecture Review

**Additional files:**
- `04-compliance/PCI-DSS-compliance.md` - Requirement-by-requirement validation
- `04-compliance/cardholder-data-flow.png` - CDE boundary diagram
- `04-compliance/network-segmentation-validation.md` - Segmentation testing

---

### HIPAA Architecture Review

**Additional files:**
- `04-compliance/HIPAA-compliance.md` - Security Rule validation
- `04-compliance/PHI-data-flow.png` - PHI flow diagram
- `04-compliance/encryption-validation.md` - At-rest and in-transit validation

---

### SOC 2 Architecture Review

**Additional files:**
- `04-compliance/SOC2-compliance.md` - Trust Services Criteria validation
- `04-compliance/security-controls-mapping.md` - Control mapping to architecture

---

### GDPR Architecture Review

**Additional files:**
- `04-compliance/GDPR-compliance.md` - Data protection validation
- `04-compliance/data-subject-rights.md` - Right to access, erasure, portability
- `04-compliance/data-residency.md` - Data location and cross-border transfer

---

## Archive and Retention

### Archive After Completion

**Create archive:**
```bash
cd output/engagements/architecture-reviews/
tar -czf acme-corp-2025-12-ARCHIVE.tar.gz acme-corp-2025-12/
```

**Archive naming:** `[client]-[YYYY-MM]-ARCHIVE.tar.gz`

---

### Retention Policy

**Active engagements:** Keep in `output/engagements/architecture-reviews/`

**Completed engagements (< 1 year):** Keep for reference

**Completed engagements (> 1 year):** Archive to compressed format

**Completed engagements (> 3 years):** Review for deletion (check legal/contractual retention requirements)

---

## Quick Reference

| File | Purpose | Format |
|---|---|---|
| SCOPE.md | Review boundaries | Markdown |
| README.md | Engagement overview | Markdown |
| threat-register.md | Threat documentation | Markdown table |
| threat-model-diagram.png | Visual threat model | PNG/SVG |
| findings-register.md | Security weaknesses | Markdown table |
| defense-in-depth-report.md | Complete review report | Markdown |
| recommendations-roadmap.md | Prioritized improvements | Markdown table |
| executive-summary.md | High-level summary | Markdown |
| # Multi-session tracking in `sessions/ | Multi-session tracking | Markdown |
| *-compliance.md | Standards validation | Markdown |

---

**Version:** 2.0
**Last Updated:** 2025-12-02
