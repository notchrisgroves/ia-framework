---
name: benchmark-gen
description: Generate CIS/STIG compliance automation scripts
---

# /benchmark-gen - Compliance Benchmark Script Generation

Automated generation of CIS compliance scripts, DISA STIG remediations, and custom security baseline validators.

**Agent:** security
**Skill:** benchmark-generation
**Output:** `output/tools/compliance-scripts/{benchmark}-{system}-{YYYY-MM}/`

---

## Quick Start

```
/benchmark-gen
```

Collects benchmark and system requirements → Generates automated compliance validation and remediation scripts with testing framework

---

## When to Use

✅ **Use /benchmark-gen when:**
- Generate automated CIS Benchmark compliance scripts
- Create DISA STIG remediation automation
- Build custom security baseline validators
- Automate compliance checking across multiple systems
- Generate CI/CD pipeline compliance gates
- Create reusable hardening scripts for standardization

❌ **Don't use if:**
- Need one-time configuration review → use `/secure-config`
- Need architecture review → use `/arch-review`
- Need to assess current compliance → use `/secure-config` first, then generate scripts

---

## Workflow

1. **Context Collection** - Prompts gather benchmark, system type, script requirements
2. **Script Generation** - Create validation and remediation scripts based on benchmark
3. **Testing Framework** - Generate test harness to validate script safety
4. **Output** - Create script package in `output/tools/compliance-scripts/{benchmark}-{system}-{YYYY-MM}/`

**Estimated time:** 30-60 minutes

---

## Context Prompts

### Benchmark Type

**Question:** "Which security benchmark should the scripts implement?"

**Options:**
- **CIS Benchmark** - Center for Internet Security Benchmarks
- **DISA STIG** - Defense Information Systems Agency STIGs
- **Custom Baseline** - Organization-specific security baseline

**Default:** CIS Benchmark

---

### System Type

**Question:** "What system type are the scripts for?"

**Options:**
- **Linux (RHEL/CentOS)** - Red Hat Enterprise Linux or CentOS
- **Linux (Ubuntu/Debian)** - Ubuntu or Debian
- **Windows Server** - Windows Server (2016, 2019, 2022)
- **Docker/Containers** - Docker container hardening
- **Kubernetes** - Kubernetes cluster hardening
- **AWS** - AWS infrastructure
- **Azure** - Azure infrastructure

**Default:** Linux (Ubuntu/Debian)

---

### CIS Benchmark Level (Conditional: CIS Only)

**Conditional:** Only if Benchmark = CIS Benchmark

**Question:** "Which CIS profile level should be implemented?"

**Options:**
- **Level 1** - Basic hardening, minimal functionality impact
- **Level 2** - Strict hardening for high-security environments
- **Both (Modular)** - Separate scripts for Level 1 and Level 2 (recommended)

**Default:** Both (Modular)

---

### Script Purpose

**Question:** "What should the scripts do?"

**Options:**
- **Validation Only** - Check compliance without making changes (safe for production)
- **Remediation Only** - Apply hardening configurations (modifies system)
- **Both (Separate Scripts)** - Generate both validation and remediation scripts (recommended)

**Default:** Both (Separate Scripts)

---

### Execution Environment

**Question:** "Where will the scripts run?"

**Options:**
- **Manual Execution** - Scripts run manually by administrators (interactive prompts)
- **Automated/CI-CD** - Scripts run in automation pipelines (non-interactive, JSON output)
- **Configuration Management** - Integration with Ansible, Puppet, Chef, or SaltStack

**Default:** Manual Execution

---

## Agent Routing

```typescript
Task({
  subagent_type: "security",
  model: "sonnet",
  prompt: `
Mode: benchmark-generation
Skill: benchmark-generation
Workflow: compliance-script-generation

Context:
- Benchmark: {cis|stig|custom}
- System: {rhel|ubuntu|windows|docker|kubernetes|aws|azure}
- Level: {level-1|level-2|both} (if CIS)
- Purpose: {validation|remediation|both}
- Environment: {manual|automated|config-mgmt}

Instructions:
Execute benchmark-generation SKILL.md workflow:
1. Generate validation scripts (if requested)
2. Generate remediation scripts (if requested)
3. Create rollback scripts
4. Build testing framework
5. Generate configuration management templates (if requested)

Output: output/tools/compliance-scripts/{benchmark}-{system}-{YYYY-MM}/
`
})
```

---

## Output Structure

```
output/tools/compliance-scripts/{benchmark}-{system}-{YYYY-MM}/
├── README.md
├── validate-compliance.sh
├── remediate-compliance.sh
├── rollback.sh
├── config/
│   ├── benchmark-requirements.txt
│   └── exclusions.txt
├── modules/
│   ├── section-1-filesystem.sh
│   ├── section-2-services.sh
│   ├── section-3-network.sh
│   ├── section-4-logging.sh
│   └── section-5-access.sh
├── tests/
│   ├── test-validation.sh
│   ├── test-remediation.sh
│   └── test-rollback.sh
├── output/
│   └── .gitkeep
└── ansible/ (if config-mgmt selected)
    └── compliance-playbook.yml
```

**Deliverables:**

1. **README** - Installation instructions, usage examples, prerequisites, configuration options, safety warnings

2. **Validation Script** (if requested) - Check compliance, non-destructive, report format (JSON, HTML, plain text), exit codes, compliance scoring

3. **Remediation Script** (if requested) - Apply hardening, pre-flight checks, dry-run mode, backup critical files, logging, idempotent

4. **Rollback Script** - Undo remediation, restore from backups, selective rollback, safety checks

5. **Modular Scripts** - Separate scripts by benchmark section, can run individually or together, easier maintenance, enables phased implementation

6. **Testing Framework** - Unit tests, integration tests, safety validation, performance testing

7. **Configuration Management** (if selected) - Ansible playbooks, Puppet manifests, Chef recipes, SaltStack states

---

## Metadata Tracking

**Create `metadata.json` at engagement start:**

```json
{
  "benchmark": "{cis|stig|custom}",
  "system": "{system}",
  "started_at": "YYYY-MM-DDTHH:MM:SS",
  "benchmark_level": "level-1|level-2|both",
  "script_purpose": "validation|remediation|both",
  "environment": "manual|automated|config-mgmt",
  "phase": "context|generation|testing|packaging|complete",
  "scripts_generated": {
    "validation": 0,
    "remediation": 0,
    "rollback": 0
  }
}
```

---

## Examples

### CIS Ubuntu Automation

```
/benchmark-gen
→ Benchmark: CIS | System: Ubuntu 22.04 | Level: Both (Modular) | Purpose: Validation + Remediation

Result: Validation + remediation scripts, Level 1+2 scripts, rollback, tests (~45-60 min)
Output: output/tools/compliance-scripts/cis-ubuntu-22-04-2025-12/
```

### DISA STIG Windows CI/CD

```
/benchmark-gen
→ Benchmark: STIG | System: Windows Server 2019 | Purpose: Validation Only | Environment: CI/CD

Result: PowerShell validation script, JSON output, CI/CD pipeline examples (~35-45 min)
Output: output/tools/compliance-scripts/stig-windows-2019-2025-12/
```

---

## Security Considerations

**Generated scripts have safety features, but:**
- Always review before execution
- Test in non-production first
- Use secure credential storage (Ansible Vault, etc.)
- Follow change management process (schedule maintenance windows)

---

## Related Commands

- `/secure-config` - One-time compliance assessment (use this first)
- `/risk-assessment` - Risk assessment to justify compliance requirements
- `/vuln-scan` - Runtime vulnerability validation

---

## References

**Benchmarks:**
- CIS Benchmarks: cisecurity.org/cis-benchmarks
- DISA STIGs: cyber.mil/stigs
- CIS-CAT Pro: cisecurity.org/cybersecurity-tools/cis-cat-pro

**Automation Frameworks:**
- Ansible: docs.ansible.com
- OpenSCAP: open-scap.org
- InSpec: inspec.io

---

**Version:** 1.0
**Last Updated:** 2025-12-12
**Framework:** Intelligence Adjacent (IA)
