# Policy Generation Workflow
## Intelligent Multi-Framework Policy Development

**Version:** 1.0
**Last Updated:** 2025-10-22
**Purpose:** Automated workflow for generating organization-specific security policies that satisfy multiple compliance frameworks with minimal duplication

---

## Workflow Overview

This workflow intelligently generates security policies by:
1. **Identifying** applicable compliance frameworks
2. **Determining** required policies based on framework mapping
3. **Prioritizing** high-overlap policies for maximum efficiency
4. **Generating** customized policies with multi-framework citations
5. **Validating** completeness against framework requirements

---

## Phase 1: Framework Identification & Scoping

### Inputs Required

**Organization Context:**
- Industry/sector (Financial Services, Healthcare, Technology, Retail, Government, etc.)
- Organization size (employees, revenue)
- Geographic operations (US only, EU, global)
- Data types handled (PII, ePHI, cardholder data, CUI, etc.)

**Compliance Requirements:**
- Regulatory mandates (HIPAA, GLBA, GDPR, etc.)
- Contractual obligations (SOC 2, ISO 27001, etc.)
- Customer requirements (PCI DSS for merchants, FedRAMP for gov contractors)
- Industry standards (NIST CSF, CIS Controls, etc.)

### Framework Selection Matrix

**Automatic Framework Selection Rules:**

```
IF industry = "Financial Services" OR handles_cardholder_data = TRUE:
    REQUIRED: PCI DSS v4.0.1

IF industry = "Financial Services" AND organization_type IN ["Bank", "Credit Union"]:
    REQUIRED: GLBA, FFIEC
    RECOMMENDED: NIST CSF, SOC 2

IF industry = "Healthcare" OR handles_ePHI = TRUE:
    REQUIRED: HIPAA Security Rule, HIPAA Privacy Rule
    RECOMMENDED: HITECH, SOC 2

IF provides_services_to_customers = TRUE AND customers_require_audit = TRUE:
    REQUIRED: SOC 2 Type II

IF operates_in_EU OR has_EU_customers = TRUE:
    REQUIRED: GDPR

IF operates_in_california OR has_california_customers = TRUE:
    REQUIRED: CCPA/CPRA

IF government_contractor = TRUE:
    REQUIRED: NIST SP 800-171 Rev. 2
    IF defense_contractor = TRUE:
        REQUIRED: CMMC (Level based on contract)

IF seeking_certification = TRUE:
    OPTIONAL: ISO 27001:2022

IF all_organizations = TRUE:
    RECOMMENDED: NIST CSF 2.0, CIS Controls v8.1
```

### Output: Framework List

**Example Output:**
```
Selected Frameworks:
✅ REQUIRED: PCI DSS v4.0.1 (Processes credit cards)
✅ REQUIRED: GLBA (Credit union)
✅ REQUIRED: NIST CSF 2.0 (Baseline security)
🟡 RECOMMENDED: SOC 2 Type II (Customer requirement)
🟡 RECOMMENDED: CIS Controls v8.1 (Implementation guide)
```

---

## Phase 2: Policy Requirement Analysis

### Required Policy Determination

Using `../reference/framework-mapping.md`, determine required policies:

**Algorithm:**
```
FOR EACH selected_framework:
    policies_required = GET_REQUIRED_POLICIES(framework)
    policies_recommended = GET_RECOMMENDED_POLICIES(framework)

combined_required = UNION(all_policies_required)
combined_recommended = UNION(all_policies_recommended)

prioritized_list = SORT_BY_OVERLAP_COUNT(combined_required)
```

### Priority Scoring

**Policy Priority Score = (Number of frameworks requiring) × 10 + (Number of frameworks recommending) × 5**

**Example for Access Control Policy:**
- Required by: NIST CSF, ISO 27001, CIS Controls, PCI DSS, HIPAA, GLBA, SOC 2, NIST 800-53, NIST 800-171, GDPR
- Recommended by: 0 frameworks
- **Priority Score: 100**

### Output: Prioritized Policy List

**Example Output:**
```
Priority 1 (Score 90-100): Core Governance
  1. Information Security Policy (100)
  2. Access Control / Identity Management (100)
  3. Incident Response Policy (100)
  4. Data Classification & Protection (100)
  5. Risk Management Policy (90)

Priority 2 (Score 70-89): Technical Security
  6. Third-Party Risk Management (100)
  7. Network Security Policy (90)
  8. Encryption Standard (90)
  9. Logging & Monitoring (90)
 10. Vulnerability Management (70)

Priority 3 (Score 50-69): Operational Security
 11. Configuration Management (80)
 12. Business Continuity & Disaster Recovery (70)
 13. Security Awareness Training (90)
 14. Password Standard (90)
 15. Privileged Access Management (90)

Priority 4 (Industry-Specific):
 16. Privacy Management Policy (GDPR/CCPA required)
 17. Physical Security Policy (HIPAA/PCI required)
 18. Database Security Policy (PCI/HIPAA specific)
```

---

## Phase 3: Policy Template Customization

### Information Gathering

**For EACH policy to be generated, collect:**

#### Universal Variables (All Policies)
```yaml
organization_name: "{{ORGANIZATION_NAME}}"
effective_date: "{{EFFECTIVE_DATE}}"
version: "{{VERSION}}"
policy_owner: "{{POLICY_OWNER}}"          # Role, e.g., "Chief Information Security Officer"
contact_email: "{{CONTACT_EMAIL}}"
next_review_date: "{{NEXT_REVIEW_DATE}}"  # Typically annual
compliance_frameworks: "{{COMPLIANCE_FRAMEWORKS}}"  # e.g., "PCI DSS v4.0.1, GLBA, NIST CSF 2.0"
```

#### Policy-Specific Variables

**Access Control Policy:**
```yaml
iam_director: "{{IAM_DIRECTOR}}"
password_min_length: "{{PASSWORD_MIN_LENGTH}}"      # e.g., 12
password_complexity_required: "{{PASSWORD_COMPLEXITY}}"  # true/false
mfa_required_for: "{{MFA_REQUIRED_FOR}}"           # e.g., "all privileged access, remote access, and access to sensitive data"
access_review_frequency: "{{ACCESS_REVIEW_FREQ}}"  # e.g., "quarterly"
privileged_account_tool: "{{PAM_TOOL}}"            # e.g., "CyberArk" or "vendor-agnostic PAM platform"
```

**Incident Response Policy:**
```yaml
incident_response_manager: "{{IR_MANAGER}}"
soc_hours: "{{SOC_HOURS}}"                         # e.g., "24/7" or "8am-5pm M-F"
siem_platform: "{{SIEM_PLATFORM}}"                 # e.g., "Splunk" or "centralized SIEM platform"
critical_notification_time: "{{CRITICAL_NOTIFY}}"  # e.g., "within 1 hour"
high_notification_time: "{{HIGH_NOTIFY}}"          # e.g., "within 4 hours"
breach_notification_required: "{{BREACH_NOTIFY}}"  # e.g., "GDPR (72 hours), HIPAA (60 days)"
```

**Data Classification Policy:**
```yaml
data_protection_officer: "{{DPO}}"
classification_levels: "{{CLASSIFICATION_LEVELS}}" # e.g., "Public, Internal, Confidential, Restricted"
sensitive_data_types: "{{SENSITIVE_DATA_TYPES}}"   # e.g., "SSN, credit card numbers, ePHI, account numbers"
encryption_required_for: "{{ENCRYPTION_REQUIRED}}" # e.g., "Confidential and Restricted data"
dlp_tool: "{{DLP_TOOL}}"                          # e.g., "Microsoft Purview" or "DLP platform"
data_retention_schedule: "{{RETENTION_SCHEDULE}}"  # e.g., "7 years for financial records, 6 years for medical records"
```

**Third-Party Risk Management:**
```yaml
vendor_risk_manager: "{{VENDOR_RISK_MANAGER}}"
vendor_assessment_frequency: "{{VENDOR_ASSESSMENT_FREQ}}"  # e.g., "Annual for critical vendors, biennial for others"
vendor_assessment_tool: "{{VENDOR_TOOL}}"                  # e.g., "SecurityScorecard" or "third-party risk platform"
minimum_vendor_requirements: "{{VENDOR_MIN_REQ}}"          # e.g., "SOC 2 Type II for cloud providers, annual security questionnaire for all others"
right_to_audit: "{{RIGHT_TO_AUDIT}}"                       # true/false
```

### Template Population Strategy

**Option 1: Guided Interview Mode**
- Ask user context-driven questions for each policy
- Provide intelligent defaults based on organization size and industry
- Offer examples and recommendations

**Option 2: Batch Input Mode**
- Provide YAML/JSON configuration file template
- User completes all variables at once
- Batch generate all policies

**Option 3: Hybrid Mode** (Recommended)
- Collect universal variables once (organization name, frameworks, etc.)
- For each policy, prompt only for policy-specific variables
- Use intelligent defaults where possible
- Allow "agnostic" option to keep vendor/tool references generic

---

## Phase 4: Multi-Framework Citation Integration

### Citation Strategy

For each policy control/requirement, determine which frameworks mandate it:

**Example: Multi-Factor Authentication (MFA) Requirement**

```markdown
**Multi-Factor Authentication:**
- MFA required for all privileged access, remote access, and access to {{SENSITIVE_SYSTEMS}}
- MFA shall use phishing-resistant authentication methods (FIDO2, WebAuthn, etc.)
- SMS-based MFA is prohibited for privileged access

**Framework Requirements Satisfied:**
- **NIST CSF 2.0:** PR.AA-6 (Physical and logical access to assets is managed based on the principle of least functionality)
- **ISO 27001:2022:** A.5.17 (Authentication information), A.5.18 (Access rights)
- **CIS Controls v8.1:** Control 6.3 (Require MFA for externally-exposed applications)
- **PCI DSS v4.0.1:** Requirement 8.4 (Multi-factor authentication implemented)
- **HIPAA Security Rule:** §164.312(a)(2)(i) (Unique user identification)
- **GLBA:** Interagency Guidelines Appendix B (Multi-factor authentication)
- **SOC 2:** CC6.1 (Logical and physical access controls)
- **NIST SP 800-53 Rev. 5:** IA-2(1) through IA-2(12) (Multi-factor authentication)
- **NIST SP 800-171 Rev. 2:** 3.5.3 (Use multifactor authentication)
```

### Intelligent Citation Consolidation

**Rule: If >6 frameworks require the same control, use summary format:**

```markdown
**Framework Requirements Satisfied:**
This control satisfies multi-factor authentication requirements across all selected frameworks:
- NIST CSF 2.0 (PR.AA-6)
- ISO 27001:2022 (A.5.17, A.5.18)
- CIS Controls v8.1 (6.3, 6.4, 6.5)
- PCI DSS v4.0.1 (Req 8.4, 8.5)
- HIPAA Security Rule (§164.312(a)(2)(i))
- GLBA (Interagency Guidelines Appendix B)
- SOC 2 (CC6.1, CC6.2)
- NIST 800-53 (IA-2)
- NIST 800-171 (3.5.3)

For detailed mapping, see Appendix: Framework Compliance Matrix.
```

---

## Phase 5: Policy Generation & Output

### Generation Process

**For Each Policy:**

1. **Load Base Template** from `../templates/policies/[policy_name].md`
2. **Replace Variables** with collected values
3. **Insert Framework Citations** based on selected frameworks
4. **Add Framework-Specific Requirements** if applicable
5. **Generate Appendix** with complete framework mapping table
6. **Validate Completeness** against all selected framework requirements

### Output Structure

**Output Location:** `output/engagements/policy-generation/[client-name]-[YYYY-MM]/`

```
output/engagements/policy-generation/[client-name]-[YYYY-MM]/
├── policies/
│   ├── 01_information_security_policy.md
│   ├── 02_risk_management_policy.md
│   ├── 03_access_control_policy.md
│   ├── 04_incident_response_policy.md
│   ├── 05_data_classification_policy.md
│   └── ...
├── framework_compliance_matrix.xlsx
└── policy_generation_report.md
```

### Policy Generation Report

```markdown
# Policy Generation Report
**Organization:** {{ORGANIZATION_NAME}}
**Date:** {{GENERATION_DATE}}
**Frameworks:** {{SELECTED_FRAMEWORKS}}

## Generation Summary
- Total Policies Generated: 15
- Framework Requirements Satisfied: 247 / 247 (100%)
- Policies with Multi-Framework Citations: 12
- Industry-Specific Policies: 3

## Framework Coverage Analysis

### PCI DSS v4.0.1
- Requirements Covered: 42 / 42 (100%)
- Policies Addressing PCI: 10
- Critical Controls Implemented: ✅ All

### GLBA Safeguards Rule
- Requirements Covered: 18 / 18 (100%)
- Policies Addressing GLBA: 8
- Critical Controls Implemented: ✅ All

### NIST CSF 2.0
- Functions Covered: 6 / 6 (100%)
- Categories Covered: 23 / 23 (100%)
- Subcategories Addressed: 108 / 108 (100%)

## Policy Review Schedule
| Policy | Owner | Next Review | Annual/Event-Driven |
|--------|-------|-------------|---------------------|
| Information Security Policy | CISO | 2026-10-22 | Annual |
| Risk Management Policy | CRO | 2026-10-22 | Annual |
| Incident Response Policy | IR Manager | 2026-04-22 | Semi-Annual |
...

## Recommended Next Steps
1. Executive review and approval of all policies
2. Legal review for regulatory compliance accuracy
3. Board approval of Information Security and Risk Management policies
4. Organization-wide policy distribution and acknowledgment
5. Training program development for policy awareness
6. Policy enforcement and monitoring procedures
7. Schedule first annual policy review
```

---

## Phase 6: Validation & Quality Assurance

### Completeness Checks

**For Each Selected Framework:**
```
✅ All required policies generated
✅ All framework requirements cited in at least one policy
✅ No orphaned requirements (not covered by any policy)
✅ No conflicting requirements between frameworks
✅ Framework-specific language accurately reflected
✅ Responsible parties assigned for all requirements
```

### Quality Criteria

**Policy-Level Checks:**
- [ ] Clear purpose and scope statement
- [ ] Specific, measurable requirements (not vague)
- [ ] Assigned roles and responsibilities
- [ ] Defined compliance monitoring and metrics
- [ ] Training requirements specified
- [ ] Enforcement and consequences documented
- [ ] Related policies cross-referenced
- [ ] Framework compliance mapping complete
- [ ] Review and approval workflow defined
- [ ] Version control and change management

**Organization-Level Checks:**
- [ ] No gaps in framework coverage
- [ ] No duplicate or conflicting policies
- [ ] Consistent terminology across policies
- [ ] Realistic for organization size and maturity
- [ ] Aligned with organizational risk appetite
- [ ] Scalable for organizational growth
- [ ] Integration with existing processes
- [ ] Achievable with available resources

---

## Workflow Execution Modes

### Mode 1: Full Automated Generation

**Use Case:** Greenfield implementation, no existing policies

**Process:**
1. Conduct framework identification interview (5-10 minutes)
2. Collect organization variables (YAML configuration file)
3. Auto-generate all required policies with intelligent defaults
4. Review and customize generated policies
5. Approve and distribute

**Timeline:** 2-4 hours for complete policy suite

---

### Mode 2: Incremental Policy Development

**Use Case:** Existing policies need enhancement for new framework

**Process:**
1. Load existing policy
2. Identify framework gaps using mapping matrix
3. Generate addendum or enhanced version with new framework citations
4. Merge with existing policy maintaining current customizations
5. Validate complete framework coverage

**Timeline:** 30-60 minutes per policy

---

### Mode 3: Framework-Specific Policy Pack

**Use Case:** Preparing for specific audit or certification

**Process:**
1. Select target framework (e.g., "SOC 2 Type II")
2. Generate only policies required for that framework
3. Focus on framework-specific language and evidence
4. Create audit-ready documentation package

**Timeline:** 3-6 hours for framework-specific pack

---

### Mode 4: Policy Refresh / Update

**Use Case:** Annual policy review or framework version update

**Process:**
1. Load existing policies
2. Check for framework updates (PCI DSS 4.0 → 4.0.1, etc.)
3. Identify new or changed requirements
4. Generate change summary and updated policy sections
5. Version control and approval process

**Timeline:** 1-2 hours for full policy suite review

---

## Context-Driven Prompts

### Intelligent Defaults by Organization Size

**Small Organization (<50 employees):**
```yaml
# Access Control Policy
access_review_frequency: "Semi-annually"
mfa_required_for: "All remote access and privileged access"
password_min_length: 12
privileged_account_tool: "Vendor-agnostic privileged access management platform or password vault"

# Incident Response Policy
soc_hours: "Business hours (8am-5pm M-F) with on-call rotation for after-hours critical incidents"
siem_platform: "Centralized log management and SIEM platform"
critical_notification_time: "Within 2 hours"

# Security Awareness Training
training_frequency: "Annual for all employees, new hire onboarding"
phishing_simulation_frequency: "Quarterly"
```

**Medium Organization (50-500 employees):**
```yaml
# Access Control Policy
access_review_frequency: "Quarterly"
mfa_required_for: "All user access (internal and external), with phishing-resistant MFA for privileged access"
password_min_length: 14
privileged_account_tool: "Enterprise PAM platform (CyberArk, BeyondTrust, or equivalent)"

# Incident Response Policy
soc_hours: "24/7 monitoring with dedicated SOC team or managed security service provider (MSSP)"
siem_platform: "Enterprise SIEM platform (Splunk, Sentinel, Chronicle, or equivalent)"
critical_notification_time: "Within 1 hour"

# Security Awareness Training
training_frequency: "Annual comprehensive training, quarterly micro-learning, role-based specialized training"
phishing_simulation_frequency: "Monthly"
```

**Large Organization (500+ employees):**
```yaml
# Access Control Policy
access_review_frequency: "Quarterly for all accounts, monthly for privileged accounts"
mfa_required_for: "All access (internal and external) with phishing-resistant MFA (FIDO2) required for all users"
password_min_length: 16
privileged_account_tool: "Enterprise PAM platform with session recording, JIT access, and automated credential rotation"

# Incident Response Policy
soc_hours: "24/7/365 dedicated SOC with tiered support (L1, L2, L3)"
siem_platform: "Enterprise SIEM with SOAR integration and threat intelligence feeds"
critical_notification_time: "Within 30 minutes"

# Security Awareness Training
training_frequency: "Continuous security awareness program with monthly micro-learning, quarterly phishing simulations, annual comprehensive training, role-based training"
phishing_simulation_frequency: "Bi-weekly with individualized remediation"
```

### Industry-Specific Customizations

**Financial Services:**
- Enhanced focus on PCI DSS and GLBA requirements
- Specific cardholder data environment (CDE) scoping
- FFIEC CAT alignment for credit unions/banks
- Regulatory examination preparedness language

**Healthcare:**
- HIPAA-specific ePHI protection measures
- Business Associate Agreement (BAA) requirements for vendors
- Breach notification within 60 days to HHS
- OCR audit readiness considerations

**Technology/SaaS:**
- SOC 2 trust services criteria language
- Customer data isolation and multi-tenancy security
- API security and developer-focused controls
- Continuous deployment and DevSecOps integration

**Government Contractors:**
- NIST 800-171 CUI protection requirements
- CMMC maturity level alignment
- Incident reporting to DoD/FBI within 72 hours
- Supply chain risk management for DFARS compliance

---

## Usage Instructions

### Step 1: Initiate Policy Generation

**Command:** `/generate-policies` or invoke policy-generator agent

**Initial Questions:**
```
1. What is your organization's primary industry?
   [Financial Services / Healthcare / Technology / Retail / Government / Manufacturing / Other]

2. What compliance frameworks are you required to follow?
   [Select all that apply: PCI DSS, HIPAA, GLBA, GDPR, CCPA, SOC 2, ISO 27001, NIST 800-171, FedRAMP, Other]

3. What is your organization size?
   [<50 employees / 50-500 employees / 500-2000 employees / 2000+ employees]

4. Do you currently have existing security policies?
   [No - Generate from scratch / Yes - Enhance existing / Yes - Update for new framework]

5. Do you prefer vendor-specific or vendor-agnostic policy language?
   [Agnostic (recommended) / Specific (will prompt for tool names)]
```

### Step 2: Framework-Based Policy Selection

Based on responses, system presents:
```
Based on your selections, the following policies are required:

CRITICAL (Must Have - Required by multiple frameworks):
✅ 1. Information Security Policy (Required by: ALL frameworks)
✅ 2. Access Control / Identity Management (Required by: PCI DSS, HIPAA, NIST CSF, SOC 2)
✅ 3. Incident Response Policy (Required by: PCI DSS, HIPAA, NIST CSF, SOC 2)
✅ 4. Data Classification & Protection (Required by: PCI DSS, HIPAA, NIST CSF, GDPR)
✅ 5. Risk Management Policy (Required by: PCI DSS, HIPAA, NIST CSF, SOC 2)

IMPORTANT (Recommended - Required by frameworks):
🟡 6. Third-Party Risk Management (Required by: PCI DSS, SOC 2)
🟡 7. Network Security Policy (Required by: PCI DSS, NIST CSF)
🟡 8. Encryption Standard (Required by: PCI DSS, HIPAA)
🟡 9. Logging & Monitoring (Required by: PCI DSS, HIPAA, SOC 2)
🟡 10. Vulnerability Management (Required by: PCI DSS, NIST CSF)

INDUSTRY-SPECIFIC:
🔵 11. Privacy Management Policy (Required by: GDPR)
🔵 12. Physical Security Policy (Required by: HIPAA)

Would you like to:
[A] Generate all recommended policies
[B] Generate only critical policies
[C] Customize selection

Selection: _
```

### Step 3: Organization Information Collection

```yaml
# Universal Organization Information
organization_name: "Acme Credit Union"
headquarters_location: "Seattle, WA"
effective_date: "2026-01-01"
policy_owner: "Chief Information Security Officer"
contact_email: "security@acmecreditunion.com"
next_review_date: "2027-01-01"
fiscal_year: "Calendar year"

# Compliance Scope
selected_frameworks:
  - "PCI DSS v4.0.1"
  - "GLBA Safeguards Rule"
  - "NIST Cybersecurity Framework 2.0"
  - "SOC 2 Type II"

# Organizational Context
employee_count: 250
annual_revenue: "$500M"
industry: "Financial Services - Credit Union"
data_types:
  - "Member PII"
  - "Account Information"
  - "Credit Card Data (as merchant)"
  - "Loan Application Data"
```

### Step 4: Policy-Specific Customization

**For each policy, prompted for specific details:**

**Example: Access Control Policy**
```
Access Control / Identity Management Policy Configuration:

1. Who is responsible for IAM?
   Default: "Identity & Access Management Director"
   Your answer: [Accept default / Custom role]

2. What is your minimum password length?
   Recommended for your frameworks: 12 characters (PCI DSS minimum)
   Your answer: [12 / 14 / 16 / Custom]

3. Where is MFA required?
   PCI DSS requires: Privileged access to CDE
   GLBA requires: Remote access and privileged access
   Your answer: [All access / Remote and privileged / Privileged only]

4. How often do you review user access?
   SOC 2 expects: Quarterly minimum
   Your answer: [Monthly / Quarterly / Semi-annually / Annually]

5. Do you use a PAM platform?
   Your answer: [Yes - specify vendor / Yes - keep agnostic / No - password vault only]

Generating Access Control Policy with your preferences...
✅ Generated: 03_access_control_policy.md
```

### Step 5: Multi-Framework Citation Generation

**Automatic process:**
- Analyzes each control requirement
- Identifies which frameworks mandate it
- Inserts appropriate citations
- Creates framework compliance matrix appendix

### Step 6: Review & Approval

**Output delivered:**
```
✅ Policy Generation Complete!

Generated policies in 15 minutes:
  - 01_information_security_policy.md
  - 02_risk_management_policy.md
  - 03_access_control_policy.md
  - ...
  - framework_compliance_matrix.xlsx
  - policy_generation_report.md

Framework Coverage: 100%
  ✅ PCI DSS v4.0.1: Requirements covered
  ✅ GLBA: Requirements covered
  ✅ NIST CSF 2.0: Subcategories addressed
  ✅ SOC 2: Criteria satisfied

Next Steps:
1. Review generated policies for accuracy
2. Customize any organization-specific details
3. Submit for executive approval
4. Distribute to organization
5. Track policy acknowledgments
6. Schedule annual review

Download All Policies: [Download ZIP]
```

---

## Error Handling & Edge Cases

### Conflicting Framework Requirements

**Example:** Password complexity vs. NIST 800-63B guidance

**Resolution Strategy:**
- Implement most stringent requirement
- Document exception or variance
- Note in policy why specific approach taken

```markdown
**Password Requirements:**
- Minimum length: 14 characters
- Complexity: Not required (per NIST SP 800-63B guidance favoring length over complexity)
- Note: While some frameworks traditionally required complexity rules, current NIST guidance
  prioritizes length and prohibits complexity requirements that lead to predictable patterns.
  This policy follows NIST 800-63B while maintaining compliance through enhanced length requirements.

**Framework Alignment:**
- NIST CSF 2.0: Satisfied via PR.AA-1 (length-based authentication)
- PCI DSS v4.0.1: Req 8.3.6 allows length-only if ≥12 characters
- GLBA: Satisfied via strong authentication requirement
```

### Missing Framework Data

**If framework not in mapping matrix:**
- Generate generic policy from closest framework match
- Flag for manual review
- Add framework to mapping matrix for future use

### Impossible Requirements

**If organization cannot meet framework requirement:**
- Document as "Compensating Control"
- Provide risk acceptance documentation template
- Flag for executive review and approval

---

## Maintenance & Updates

### Framework Updates

**When new framework version released:**
1. Update framework-mapping.md with new requirements
2. Identify changed or new requirements
3. Generate change impact report for existing policies
4. Offer policy update workflow for affected organizations

### Policy Template Improvements

**Continuous improvement:**
- Track user customizations and common patterns
- Refine intelligent defaults based on usage data
- Add new industry-specific templates
- Update citation accuracy

---

**End of Policy Generation Workflow**

**Related Files:**
- `../reference/framework-mapping.md` - Framework-to-policy requirement matrix
- `../templates/policies/*.md` - Policy templates
- `../reference/frameworks.md` - Framework documentation
