---
name: secure-config
description: Infrastructure hardening validation using CIS Benchmarks, DISA STIGs, and vendor security guides
---

# Secure Config Skill Context

**Auto-loaded for infrastructure hardening validation**

Specialized in validating system configurations against CIS Benchmarks, DISA STIGs, and vendor security guides for compliance and hardening with manual validation and remediation planning.

**Version:** 2.0 (Progressive context loading with EXPLORE-PLAN-CODE/COMMIT workflow)

---

## 🚀 Quick Access - Slash Command

**Slash Command:** `/secure-config`

Infrastructure hardening validation using CIS Benchmarks, DISA STIGs, and vendor security guides.

**Command Documentation:** `../commands/secure-config.md`

**What it provides:**
- Guided workflow with context collection (system type, benchmark, access method, remediation approach)
- CIS Benchmark Level 1/Level 2 validation
- DISA STIG compliance checking (Cat I/II/III)
- Manual validation checklists for controls
- Remediation scripts (Bash, PowerShell, Ansible)
- Rollback procedures for safe changes
- Compliance reporting with evidence
- Examples and troubleshooting guidance

**Direct Agent Invocation:** Advanced users can invoke the security agent directly with the secure-config skill for custom workflows.

---

## 🚨 CRITICAL RULES SUMMARY

**Reference if context drift suspected (after 3+ hours or 5+ major tasks)**

This skill has 5 non-negotiable rules. If conversation exceeds 3 hours, review this section and restate it in your response.

**Rule 1: Load Context First**
Always begin with: `Read ../CLAUDE.md` → `Read skills/secure-config/SKILL.md` → Load methodologies and references as needed from:
- `methodologies/configuration-hardening.md` (Control validation, compliance checking, remediation planning, rollback procedures, gap analysis)
- `reference/standards.md` (CIS Benchmarks, DISA STIGs, NSA/CISA guides, Mozilla SSL config, NIST standards)
- `workflows/secure-config-validation.md` (Complete 3-phase process: EXPLORE → PLAN → CODE/COMMIT)
- `templates/` (Compliance checklist, finding report templates)

**Rule 2: CIS/STIG Standards Required**
All hardening must follow CIS Benchmarks or DISA STIGs. Never create custom baselines without standard reference. This ensures recognized compliance and audit acceptance.
- Parse control requirements exactly (audit commands, expected values)
- Map findings to specific control IDs (CIS 5.2.1, STIG V-230221)
- Document deviations with justification

**Rule 3: Checkpoint After System Type**
After completing each system type (Linux, Windows, AWS, Kubernetes), update session file in `../../sessions/` with:
- System completion status + timestamp
- Controls validated (CIS Level 1/2 or STIG Cat I/II/III)
- Non-compliant settings found (count and severity)
- Remediation scripts generated (file locations)
- Compliance percentage (before/after)
- Next action

**Rule 4: Test Before Production**
All hardening recommendations must include rollback procedures. Never recommend irreversible changes. This prevents system breakage and service disruption.
- Test remediation in staging/non-production first
- Provide backup commands before all changes
- Document rollback procedure for each remediation
- Verify service functionality after changes

**Rule 5: Environment-Specific Baselines**
Always specify environment (dev/staging/prod) and risk tolerance. Never apply max-security settings to development. This ensures operational compatibility.
- Development: CIS Level 1 (essential security only)
- Staging: CIS Level 1 + selective Level 2 (production-like)
- Production: Full CIS Level 1 + Level 2 or Level 1 + risk-based Level 2

**Refresh Trigger:**
If conversation exceeds 3 hours OR after 5+ systems validated, restate briefly:
```
Refreshing critical rules for secure config:
- Context loaded (CLAUDE.md + SKILL.md + methodologies + references + workflows + templates)
- Standards followed (CIS/STIG required, exact control mapping)
- Checkpoints maintained (systems, controls, remediations documented)
- Rollback procedures (included for all changes, tested in staging)
- Environment-specific (dev/staging/prod baselines differentiated)
```

---

## Model Selection

**Reference:** `library/model-selection-matrix.md` for complete task-to-model mapping

**Default:** Latest Haiku (checklist execution, standards validation)
**Upgrade to Sonnet:** Complex hardening analysis, remediation script generation
**Upgrade to Opus:** Novel security architecture, risk-based control selection

**Dynamic Selection:** `tools/research/openrouter/fetch_models.py` for latest versions

---

## Progressive Context Loading

**This skill uses progressive context loading to minimize token usage while maintaining comprehensive capability.**

### Core Skill Context (Always Loaded)
- This SKILL.md file (skill overview, critical rules, workflow phases)
- When to use secure-config vs other skills (benchmark-generation, code-review)

### Extended Context (Load as Needed)
**Load for methodology guidance:**
- `methodologies/configuration-hardening.md` - Control validation methodology (baseline selection, configuration collection, control-by-control validation, risk assessment), compliance checking process (automated scanning with OpenSCAP/AWS Security Hub/Docker Bench, manual validation), remediation planning (risk prioritization, environment-specific baselines, script generation), rollback procedures, gap analysis methodology, validation & verification

**Load for standards reference:**
- `reference/standards.md` - CIS Benchmarks (platforms, Level 1/2, control format, automation tools), DISA STIGs (DoD configurations, CAT I/II/III, control format), NSA/CISA Security Guides (Kubernetes, VMware, Active Directory, network devices), Mozilla SSL Configuration Generator (Modern/Intermediate/Old profiles), NIST standards (SP 800-123, SP 800-70, SP 800-53), ISO/IEC 27001/27002, PCI DSS v4.0, HIPAA Security Rule, vendor-specific guides

**Load for workflow execution:**
- `workflows/secure-config-validation.md` - Complete 3-phase workflow (EXPLORE baseline assessment, PLAN compliance validation, CODE/COMMIT remediation + documentation) with time estimates, checkpoints, deliverables

**Load for templates:**
- `templates/compliance-checklist-template.md` - Manual control validation checklist with evidence tracking
- `templates/finding-report-template.md` - Non-compliant control finding documentation

### How to Load Extended Context

**During EXPLORE phase:**
```
Read skills/secure-config/reference/standards.md
# Focus on: Benchmark selection (CIS, STIG), platform coverage, control structure
```

**During PLAN phase:**
```
Read skills/secure-config/methodologies/configuration-hardening.md
# Focus on: Control validation methodology, compliance checking, gap analysis
```

**During CODE/COMMIT phase:**
```
Read skills/secure-config/methodologies/configuration-hardening.md
# Focus on: Remediation planning, rollback procedures, script generation

Read skills/secure-config/templates/finding-report-template.md
# Focus on: Finding documentation format, validation procedures
```

---

## Model Preference

**Recommended Model:** Claude Haiku 4.5

**Rationale:** Efficient pattern matching for configuration validation, fast checklist processing, sufficient for rule-based compliance checks, cost-effective for repetitive control validation

**Use Sonnet for:** Complex remediation planning requiring architectural decisions, multi-system orchestration, custom baseline creation with risk analysis

---

## ✅ When to Use secure-config

Use this skill when you need:

**✅ Manual Infrastructure Validation**
- Validate system configurations against CIS Benchmarks
- Apply DISA STIGs for government/defense compliance
- Manual review of configuration files
- Gap analysis against security baselines
- Compliance reporting with evidence

**✅ Platform Hardening**
- Linux servers (Ubuntu, RHEL, Debian, CentOS)
- Windows Server (2016, 2019, 2022)
- Cloud infrastructure (AWS, Azure, GCP)
- Containers and Kubernetes
- Databases, web servers, network devices

**✅ Remediation Planning**
- Generate remediation scripts for non-compliant settings
- Provide rollback procedures for changes
- Environment-specific baselines (dev/staging/prod)
- Risk-prioritized remediation roadmaps

---

## ❌ When to Use Other Skills Instead

**Don't use secure-config for:**
- **Automated compliance script generation** (executable automation) → Use `/benchmark-gen` (benchmark-generation skill for automated scripts)
- **Source code vulnerability analysis** → Use `/code-review` (code-review skill for code security)
- **Application security design** → Use `/arch-review` (architecture-review skill for threat modeling)
- **Active penetration testing** → Use `/pentest` (security-testing skill for exploitation)
- **Dependency vulnerability scanning** → Use `/dependency-audit` (dependency-audit skill for SBOM/CVE analysis)

---

## 🔀 Decision Helper

**"Should I use secure-config or benchmark-generation?"**

**Q1: Do you need MANUAL VALIDATION or AUTOMATED SCRIPTS?**
- **Manual validation** (review configs, assess settings, create reports) → secure-config ✅
- **Automated scripts** (executable PowerShell, bash, Ansible for automated checking) → benchmark-generation ✅

**Q2: What deliverable do you expect?**
- **Compliance report** (findings, remediation guidance, checklists) → secure-config ✅
- **Executable scripts** (automated compliance checking and remediation) → benchmark-generation ✅

**Examples:**
- "Validate Ubuntu 22.04 server against CIS Benchmark" → secure-config ✅
- "Review AWS configuration for security compliance" → secure-config ✅
- "Apply DISA STIG to Windows server" (manual validation) → secure-config ✅
- "Assess Kubernetes cluster hardening" → secure-config ✅
- "Generate CIS Benchmark automation script for Ubuntu" → benchmark-generation ✅
- "Create DISA STIG remediation PowerShell script" → benchmark-generation ✅
- "Build automated PCI DSS compliance checker" → benchmark-generation ✅

**Still unsure?** If you need MANUAL VALIDATION and REPORTS, use secure-config. If you need EXECUTABLE AUTOMATION SCRIPTS, use benchmark-generation.

**See:** `../benchmark-generation/SKILL.md`

---

## Workflow: EXPLORE → PLAN → CODE/COMMIT

**Total Duration:** 4-8 hours (depending on system complexity and control count)

### Phase 1: EXPLORE - Baseline Assessment (1-2 hours)

**Goal:** Understand system type, environment, and applicable security standards

**Actions:**
1. Identify system type and environment (dev/staging/prod)
2. Select applicable CIS Benchmark or DISA STIG
3. Document baseline state (configuration files, services, network)
4. Define compliance requirements (PCI DSS, HIPAA, SOC 2)

**Deliverables:**
- System specifications (OS, version, services)
- Benchmark selection (CIS Level 1/2, STIG Cat I/II/III)
- Baseline configuration snapshot

**Checkpoint:** Update session file with requirements documented

**Load for this phase:**
```
Read skills/secure-config/reference/standards.md
# Focus on: Benchmark selection, platform coverage, control structure
```

---

### Phase 2: PLAN - Compliance Validation (2-3 hours)

**Goal:** Validate controls against CIS/STIG requirements and identify gaps

**Actions:**
1. Run automated compliance scans (OpenSCAP, AWS Security Hub, Docker Bench)
2. Perform manual control validation for non-automated controls
3. Calculate compliance percentage and gap categorization
4. Document non-compliant findings with evidence

**Deliverables:**
- Automated scan results
- Manual validation checklist
- Compliance report (% compliant, findings by severity)
- Finding documents for each non-compliant control

**Checkpoint:** Update session file with compliance validation completed

**Load for this phase:**
```
Read skills/secure-config/methodologies/configuration-hardening.md
# Focus on: Control validation, compliance checking, gap analysis
```

---

### Phase 3: CODE/COMMIT - Remediation Generation + Documentation (1-3 hours)

**Goal:** Generate remediation scripts, rollback procedures, and final documentation

**Actions:**
1. Prioritize remediations (P0/P1/P2/P3 based on risk)
2. Generate remediation scripts (Bash, PowerShell, Ansible)
3. Create rollback procedures for all changes
4. Create validation checklist for post-remediation testing
5. Document implementation plan and timeline

**Deliverables:**
- Remediation scripts with rollback procedures
- Validation checklist
- README with usage instructions
- Implementation roadmap

**Checkpoint:** Update session file with remediation generation completed

**Load for this phase:**
```
Read skills/secure-config/methodologies/configuration-hardening.md
# Focus on: Remediation planning, script generation, rollback procedures

Read skills/secure-config/templates/finding-report-template.md
# Focus on: Finding documentation, validation procedures
```

---

## Output Structure

```
output/engagements/secure-config/{client}-{YYYY-MM}/
   README.md                          (Usage guide, compliance summary)
   #  Multi-session tracking in ../../sessions/                   (Checkpoint tracking)
   baseline/                          (Initial configuration)
      system-info.txt
      services.txt
      network-config.txt
      firewall-rules.txt
   findings/                          (Non-compliant controls)
      CIS-001-high-ssh-config-perms.md
      CIS-002-high-ssh-public-keys.md
      STIG-001-critical-root-login.md
      compliance-gaps.md              (Summary)
   scripts/                           (Remediation + rollback)
      remediate-p0-critical.sh        (Critical fixes)
      remediate-p1-high.sh            (High priority)
      remediate-p2-medium.sh          (Medium priority)
      rollback.sh                     (Restore from backup)
      validate-post-remediation.sh    (Verification)
   reports/                           (Compliance reports)
      compliance-report-before.html   (OpenSCAP initial scan)
      compliance-report-after.html    (OpenSCAP post-remediation)
      compliance-checklist.md         (Manual validation)
   docs/
      remediation-roadmap.md          (Implementation timeline)
      risk-assessment.md              (Risk analysis for findings)
```

---

## Long-Session Rule Refresh Protocol

**Use if session exceeds 3 hours or 5+ systems**

**What triggers:** Session > 3 hours OR 5+ systems validated OR `/refresh-rules`

**How to refresh:**
```
Refreshing critical rules for secure config:
- Context loaded (CLAUDE.md + SKILL.md + methodologies + references + workflows + templates)
- Standards exact (CIS/STIG required, control IDs mapped, no custom baselines)
- Checkpoints maintained (systems documented, controls listed, compliance tracked)
- Rollback procedures (included for all changes, tested before production)
- Environment-specific (dev/staging/prod baselines differentiated, risk-appropriate)
```

**Why refresh:**
- Maintains standards compliance (15-20% better control mapping accuracy)
- Ensures rollback procedures not forgotten
- Prevents environment drift (correct baselines for dev/staging/prod)

**Benefit:** 15-20% improvement in long-session compliance + safety + operational compatibility

---

**Version:** 2.0
**Last Updated:** 2025-12-02
**Model:** Claude Haiku 4.5 (primary), Sonnet 4.5 (complex)
**Framework:** CIS Benchmarks + DISA STIGs + NSA/CISA Guides + NIST Standards
**Pattern:** Progressive context loading with EXPLORE-PLAN-CODE/COMMIT workflow
