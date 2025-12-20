---
name: secure-config
description: Infrastructure hardening validation with CIS/STIG benchmarks
---

# /secure-config - Infrastructure Hardening Validation

Infrastructure hardening validation using CIS Benchmarks, DISA STIGs, and vendor security guides.

**Agent:** security
**Skill:** secure-config
**Output:** `output/engagements/secure-config/{system}-{YYYY-MM}/`

---

## Quick Start

```
/secure-config
```

Collects system info → Validates hardening against security benchmarks → Generates compliance report with remediation

---

## When to Use

✅ **Use /secure-config when:**
- Validate system hardening against CIS Benchmarks or DISA STIGs
- Assess server, network device, or cloud service configurations
- Prepare for compliance audits (PCI DSS, HIPAA, FedRAMP)
- Review baseline security configurations
- Identify configuration drift from security standards
- Generate compliance evidence for auditors

❌ **Don't use if:**
- Need vulnerability scanning → use `/vuln-scan`
- Need architecture review → use `/arch-review`
- Need compliance benchmark script generation → use `/benchmark-gen`

---

## Workflow

1. **Context Collection** - Prompts gather system type, benchmark, access method
2. **Configuration Review** - Analyze configuration files or system settings
3. **Compliance Assessment** - Compare against benchmark requirements
4. **Output** - Generate compliance report in `output/engagements/secure-config/{system}-{YYYY-MM}/`

**Estimated time:** 30-90 minutes

---

## Context Prompts

### System Type

**Question:** "What type of system are you hardening?"

**Options:**
- **Linux Server** - Linux distributions (Ubuntu, RHEL, CentOS, Debian)
- **Windows Server** - Windows Server (2016, 2019, 2022)
- **Network Device** - Cisco, Juniper, Palo Alto firewalls/routers/switches
- **Cloud Service** - AWS, Azure, GCP services
- **Kubernetes** - Kubernetes cluster configuration
- **Database** - PostgreSQL, MySQL, MongoDB, etc.
- **Application** - Web servers (Apache, Nginx), Docker, etc.

**Default:** Linux Server

---

### Hardening Benchmark

**Question:** "Which security benchmark should be used?"

**Options:**
- **CIS Benchmark** - Center for Internet Security Benchmarks (industry-standard)
- **DISA STIG** - Defense Information Systems Agency STIGs (government/military)
- **Vendor Security Guide** - Official vendor hardening guides
- **Custom Baseline** - Organization-specific security baseline

**Default:** CIS Benchmark

---

### Benchmark Level (Conditional: CIS Only)

**Conditional:** Only if Benchmark = CIS Benchmark

**Question:** "Which CIS Benchmark profile level?"

**Options:**
- **Level 1** - Basic hardening, minimal functionality impact (recommended)
- **Level 2** - Strict hardening for high-security environments

**Default:** Level 1

---

### Configuration Access

**Question:** "How will you provide system configuration?"

**Options:**
- **SSH/Remote Access** - Direct access via SSH (Linux) or RDP (Windows)
- **Configuration Files** - Provide configuration file paths or exports
- **Configuration Paste** - Paste configuration text directly
- **Describe Manually** - Manually answer configuration questions

**Default:** Configuration Files

---

### Remediation Approach

**Question:** "What remediation approach do you prefer?"

**Options:**
- **Manual Guidance** - Step-by-step manual remediation instructions
- **Automated Scripts** - Generate remediation scripts (Bash, PowerShell, Ansible)
- **Both** - Both manual instructions and automated scripts (recommended)

**Default:** Both

---

## Agent Routing

```typescript
Task({
  subagent_type: "security",
  model: "sonnet",
  prompt: `
Mode: secure-config
Skill: secure-config
Workflow: infrastructure-hardening

Context:
- System Type: {linux|windows|network|cloud|kubernetes|database|application}
- Benchmark: {cis|stig|vendor|custom}
- Level: {level-1|level-2} (if CIS)
- Access: {ssh|files|paste|manual}
- Remediation: {manual|scripts|both}

Instructions:
Execute secure-config SKILL.md workflow:
1. Analyze configuration against benchmark
2. Generate compliance report
3. Create remediation guidance
4. Generate scripts (if requested)

Output: output/engagements/secure-config/{system}-{YYYY-MM}/
`
})
```

---

## Output Structure

```
output/engagements/secure-config/{system}-{YYYY-MM}/
├── COMPLIANCE-SUMMARY.md
├── COMPLIANCE-REPORT.md
├── CONFIGURATION-REVIEW.md
├── REMEDIATION-GUIDE.md
├── remediation-scripts/
│   ├── remediate-all.sh
│   ├── section-1-remediate.sh
│   ├── section-2-remediate.sh
│   └── rollback.sh
├── evidence/
│   ├── config-backup/
│   └── compliance-proof/
└── session-state.md
```

**Deliverables:**

1. **Compliance Summary** - Overall compliance score (%), pass/fail/NA count, critical findings, compliance level achieved

2. **Compliance Report** - Benchmark requirement-by-requirement analysis, current status, evidence, severity, remediation guidance

3. **Configuration Review** - Current configuration analysis, security posture, notable misconfigurations, configuration drift

4. **Remediation Guide** - Prioritized remediation steps (P0/P1/P2), manual instructions, expected outcomes, testing/validation steps, rollback procedures

5. **Remediation Scripts** (if requested) - Automated remediation, modular scripts by section, pre-flight checks, backup and rollback capabilities, audit logging

---

## Examples

### CIS Level 1 - Ubuntu Server

```
/secure-config
→ System: Linux (Ubuntu 22.04) | Benchmark: CIS Level 1 | Access: SSH | Remediation: Scripts + Manual

Result: Compliance report with 200+ controls, remediation scripts (~60-75 min)
Output: output/engagements/secure-config/ubuntu-22-04-2025-12/
```

### AWS CIS Benchmark

```
/secure-config
→ System: AWS | Benchmark: CIS Level 1 | Access: AWS Config Export | Remediation: Terraform

Result: AWS hardening report with Terraform scripts (~45-60 min)
Output: output/engagements/secure-config/aws-account-2025-12/
```

---

## Security Considerations

**Production Impact:**
- Test remediation in non-production first
- Schedule changes during maintenance windows
- Have rollback plan ready
- Monitor systems after changes
- Document all changes for audit trail

**Risk Acceptance:**
- Document risk acceptance for non-compliant items
- Justify business or technical reasons
- Implement compensating controls where possible
- Review risk acceptances periodically

**Continuous Compliance:**
- Implement automated compliance monitoring
- Set up configuration drift detection
- Schedule periodic re-assessments
- Integrate compliance into CI/CD

---

## Related Commands

- `/benchmark-gen` - Generate compliance automation scripts
- `/vuln-scan` - Runtime vulnerability scanning
- `/risk-assessment` - Formal risk assessment with compliance focus
- `/arch-review` - Architecture security review

---

## References

**Benchmarks:**
- CIS Benchmarks: cisecurity.org/cis-benchmarks
- DISA STIGs: cyber.mil/stigs
- NIST 800-53: nvd.nist.gov/800-53

---

**Version:** 1.0
**Last Updated:** 2025-12-12
**Framework:** Intelligence Adjacent (IA)
