---
name: benchmark-generation
description: Automated generation of CIS compliance scripts, DISA STIG remediations, and custom security baseline validators with validation, remediation, and rollback capabilities. Use for compliance automation across Windows, Linux, cloud platforms, and container environments.
---

# Benchmark Generation Skill

**Auto-loaded when `security` agent invoked for compliance automation**

Specialized in generating automated compliance scripts for CIS Benchmarks, DISA STIGs, PCI DSS, and HIPAA requirements with validation, remediation, and rollback capabilities.

**Core Philosophy:** Standards-based automation. Scripts implement CIS/STIG/PCI/HIPAA controls exactly as documented. No custom interpretations.

---

## 🚀 Quick Access

**Slash Command:** `/benchmark-gen`

Generate CIS/STIG compliance automation scripts with validation and remediation capabilities.

**See:** `commands/benchmark-gen.md` for complete workflow

---

## 🚨 Critical Rules

**Before generating any compliance script:**

1. **Load Context First** - Read CLAUDE.md → SKILL.md → Load methodologies and references as needed
2. **Standards-Based Generation** - Implement CIS/STIG/PCI/HIPAA controls exactly as documented (1:1 mapping, no custom interpretations)
3. **Checkpoint After Script Type** - Update session file after completing each script type with controls implemented and test results
4. **Test Scripts Before Delivery** - All scripts must include dry-run mode and validation logic (test on non-production first)
5. **Platform-Specific Implementation** - Generate platform-specific scripts (PowerShell for Windows, bash for Linux, cloud CLI for AWS/Azure) - no pseudo-code

**Refresh Trigger:** If conversation exceeds 3 hours OR after 5+ scripts generated, refresh rules.

---

## Progressive Context Loading

**Core Context (Always Loaded):**
- This SKILL.md file
- When to use vs other skills

**Extended Context (Load as Needed):**
- `methodologies/compliance-automation.md` - Control mapping, script generation patterns, platform-specific implementations
- `reference/standards.md` - CIS Benchmarks, DISA STIGs, PCI DSS, HIPAA, NIST SP 800-53, CIS Controls
- `workflows/benchmark-script-generation.md` - Complete 4-phase process (EXPLORE → PLAN → CODE → COMMIT)
- `templates/script-templates.md` - Bash, PowerShell, Ansible templates

---

## Model Selection

**Reference:** `library/model-selection-matrix.md` for complete task-to-model mapping

**Default:** Latest Haiku (code generation, pattern-based scripts, rule-to-script translation)
**Upgrade to Sonnet:** Complex remediation logic, multi-system orchestration, custom baseline creation
**Upgrade to Opus:** Novel automation architecture, strategic baseline decisions

**Dynamic Selection:** `tools/research/openrouter/fetch_models.py` for latest versions

---

## When to Use

✅ **Use benchmark-generation for:**
- Generate CIS Benchmark compliance checking scripts
- Create DISA STIG remediation automation
- Build PCI DSS validation scripts
- Develop HIPAA compliance validators
- PowerShell scripts for Windows compliance
- Bash scripts for Linux/Unix hardening
- Cloud CLI automation (AWS/Azure/GCP)
- Ansible/Puppet/Chef compliance playbooks
- Automated compliance reporting scripts
- Dry-run mode for safe testing
- Rollback procedures for remediations
- Continuous compliance monitoring automation

❌ **Don't use if:**
- Manual compliance validation (not automation) → Use `/secure-config` (secure-config skill)
- Architecture security design → Use `/arch-review` (architecture-review skill)
- Source code vulnerability analysis → Use `/code-review` (code-review skill)
- Active penetration testing → Use `/pentest` (security-testing skill)
- Dependency vulnerability scanning → Use `/dependency-audit` (dependency-audit skill)

---

## Decision Helper

**"Should I use benchmark-generation or secure-config?"**

**Q1: Do you need AUTOMATION SCRIPTS or MANUAL VALIDATION?**
- **Automation scripts** (PowerShell, bash, Ansible) → benchmark-generation ✅
- **Manual validation guidance** (read configs, assess settings) → secure-config ✅

**Q2: What deliverable do you expect?**
- **Executable scripts** → benchmark-generation ✅
- **Report or guidance** → secure-config ✅

**Examples:**
- "Generate CIS Benchmark script for Ubuntu 22.04" → benchmark-generation ✅
- "Create DISA STIG remediation PowerShell script" → benchmark-generation ✅
- "Build PCI DSS compliance checker for Windows" → benchmark-generation ✅
- "Automate HIPAA technical safeguard validation" → benchmark-generation ✅
- "Manually validate AWS configuration against CIS" → secure-config ✅
- "Review server hardening posture" → secure-config ✅

**Still unsure?** If you need EXECUTABLE AUTOMATION SCRIPTS for compliance, use benchmark-generation. If you need MANUAL VALIDATION or GUIDANCE, use secure-config.

---

## Workflow: EXPLORE → PLAN → CODE → COMMIT

**Total Duration:** 4-6 hours (depending on benchmark complexity and control count)

### Phase 1: EXPLORE - Requirements Analysis (1 hour)

**Goal:** Understand compliance framework, platform, and automation scope

**Actions:**
1. Identify compliance framework (CIS, DISA STIG, PCI DSS, HIPAA, NIST SP 800-53)
2. Determine version (CIS Ubuntu 22.04 v1.0.0, DISA RHEL 8 STIG V1R12)
3. Select level/category (CIS L1/L2, STIG CAT I/II/III)
4. Identify target platform (OS type, version, services)
5. Define automation scope (full baseline vs targeted controls, validation only vs full automation)
6. Select script format (Bash, PowerShell, Python, Ansible)

**Deliverables:**
- Requirements document (framework, platform, scope, format)

**Checkpoint:** Update session file with requirements documented

**Load for this phase:**
```
Read skills/benchmark-generation/reference/standards.md
# Focus on: Compliance framework selection, control requirements
```

---

### Phase 2: PLAN - Control Mapping (1-2 hours)

**Goal:** Map benchmark controls to platform-specific checks

**Actions:**
1. Parse benchmark document (extract control IDs, titles, audit commands, remediation commands)
2. Identify automated vs manual controls (scriptable vs documentation-only)
3. Create control-to-function mapping (CIS 5.2.1 → check_5_2_1(), remediate_5_2_1(), rollback_5_2_1())
4. Prioritize by severity (CAT I/CIS L1 Critical → CAT III/CIS L2 Low)

**Deliverables:**
- Control mapping document (control ID to function name)
- Automation scope (X automated controls, Y manual controls)

**Checkpoint:** Update session file with control mapping completed

**Load for this phase:**
```
Read skills/benchmark-generation/methodologies/compliance-automation.md
# Focus on: Control mapping process, automated vs manual determination
```

---

### Phase 3: CODE - Script Generation (1-2 hours)

**Goal:** Generate platform-specific automation scripts

**Actions:**
1. Create script structure (configuration, utilities, check/remediate/rollback functions, reporting, main execution)
2. Generate check functions (one per control: read current state, compare against requirement, return pass/fail)
3. Generate remediation functions (one per control: backup, apply fix, verify, log)
4. Generate rollback functions (one per control: restore backup, verify, log)
5. Implement dry-run mode (`--dry-run` flag prevents actual changes)
6. Add reporting (JSON/CSV compliance reports)

**Deliverables:**
- Platform-specific script(s) (e.g., `cis-ubuntu-22.04-l1.sh`)

**Checkpoint:** Update session file with scripts generated, controls implemented

**Load for this phase:**
```
Read skills/benchmark-generation/methodologies/compliance-automation.md
# Focus on: Script generation patterns, platform-specific implementations

Read skills/benchmark-generation/templates/script-templates.md
# Focus on: Platform-specific templates (Bash, PowerShell, Ansible)
```

---

### Phase 4: COMMIT - Testing & Documentation (1 hour)

**Goal:** Validate scripts and create usage documentation

**Actions:**
1. Test in dry-run mode (verify script executes without errors, no actual changes)
2. Test on non-production system (apply remediations, verify improved compliance)
3. Test rollback functionality (restore configuration, verify system functional)
4. Create usage documentation (installation, usage, flags, examples, troubleshooting)
5. Document limitations (manual controls, service disruption risks, reboot requirements)

**Deliverables:**
- Tested scripts with validated functionality
- Usage documentation (README.md)
- Limitations documentation

**Checkpoint:** Update session file with testing completed, script ready

**Load for this phase:**
```
Read skills/benchmark-generation/workflows/benchmark-script-generation.md
# Focus on: Testing procedures, documentation requirements
```

---

## Output Structure

```
output/engagements/benchmark-gen/{client}-{YYYY-MM}/
├── README.md                       (Usage guide)
├── scripts/
│   ├── cis-ubuntu-22.04-l1.sh     (CIS Level 1 script)
│   ├── cis-ubuntu-22.04-l2.sh     (CIS Level 2 script)
│   ├── disa-stig-rhel8.sh         (DISA STIG script)
│   ├── pci-dss-validator.py       (PCI DSS checks)
│   └── hipaa-compliance.ps1       (HIPAA validation)
├── playbooks/                      (Ansible automation)
│   ├── cis-hardening.yml
│   └── stig-remediation.yml
├── reports/                        (Sample outputs)
│   ├── compliance-report.json
│   └── findings-summary.csv
└── docs/
    ├── control-mapping.md          (Framework to script mapping)
    └── remediation-impact.md       (Change impact analysis)
```

**Multi-session tracking:** `../../sessions/YYYY-MM-DD-project-name.md`

---

## Long-Session Rule Refresh

**Triggers:** Session > 3 hours OR 5+ scripts generated OR `/refresh-rules`

**Refresh statement:**
```
Refreshing critical rules for benchmark generation:
- Context loaded (CLAUDE.md + SKILL.md + methodologies + references + workflows + templates)
- Standards exact (CIS/STIG/PCI/HIPAA controls, 1:1 mapping, no custom interpretations)
- Checkpoints maintained (scripts documented, controls listed, tests recorded)
- Scripts tested (dry-run mode, non-production validation, rollback verified)
- Platform-specific (Bash/PowerShell/Ansible correctly targeted, no pseudo-code)
```

**Benefit:** 15-20% improvement in long-session script quality + testing compliance

---

## Script Safety Features

**All generated scripts must include:**

**1. Dry-Run Mode:**
```bash
if [ "$DRY_RUN" = "true" ]; then
    echo "[DRY-RUN] Would execute: $command"
else
    eval "$command"
fi
```

**2. Backup Before Changes:**
```bash
backup_file() {
    cp "$1" "$1.backup.$(date +%Y%m%d-%H%M%S)"
}
```

**3. Idempotent Execution:**
- Scripts safe to run multiple times
- Check current state before applying changes
- Skip already-compliant controls

**4. Rollback Procedures:**
- Restore from backups
- Selective rollback (per control)
- Verify system functional after rollback

**5. Comprehensive Logging:**
- Timestamp all actions
- Log pass/fail for each control
- Record changes made

---

## Platform-Specific Implementations

**Bash (Linux):**
- Use `stat`, `systemctl`, `sysctl`, `chmod`, `chown`
- File permissions: `chmod 0600 /etc/shadow`
- Service management: `systemctl disable telnet.socket`

**PowerShell (Windows):**
- Use `Get-ItemProperty`, `Set-ItemProperty`, `Get-Service`, `Set-Service`
- Registry: `Set-ItemProperty -Path "HKLM:\..." -Name "..." -Value "..."`
- Services: `Set-Service -Name "Telnet" -StartupType Disabled`

**Ansible (Cross-platform):**
- Use `file`, `service`, `sysctl`, `template` modules
- Declarative state management
- Built-in idempotence

---

## Compliance Frameworks Supported

**CIS Benchmarks:**
- Level 1 (basic hardening, minimal functionality impact)
- Level 2 (strict hardening for high-security environments)
- 100+ platforms (Ubuntu, RHEL, Windows, AWS, Azure, Kubernetes)

**DISA STIGs:**
- CAT I (Critical) - Immediate remediation
- CAT II (High) - Priority remediation
- CAT III (Medium) - Standard remediation

**PCI DSS v4.0:**
- 12 requirements, 300+ controls
- Focus on payment card data protection

**HIPAA Security Rule:**
- 164.308 (Administrative Safeguards)
- 164.310 (Physical Safeguards)
- 164.312 (Technical Safeguards)
- 164.316 (Policies and Procedures)

**NIST SP 800-53 Rev. 5:**
- 20 control families (AC, AU, CM, etc.)
- Low/Moderate/High baselines

**CIS Controls v8:**
- IG1 (Implementation Group 1 - Essential)
- IG2 (Implementation Group 2 - Foundational)
- IG3 (Implementation Group 3 - Organizational)

---

**Version:** 2.0
**Last Updated:** 2025-12-12
**Model:** Claude Haiku 4.5 (primary), Sonnet 4.5 (complex logic)
**Framework:** CIS Benchmarks + DISA STIGs + PCI DSS + HIPAA + NIST SP 800-53 + CIS Controls v8
**Pattern:** Progressive context loading with EXPLORE-PLAN-CODE-COMMIT workflow
