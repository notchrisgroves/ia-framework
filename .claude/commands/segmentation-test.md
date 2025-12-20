---
name: segmentation-test
description: Network segmentation validation with Director/Demo modes
---

# /segmentation-test - Network Segmentation Validation

Validate network segmentation controls and isolation between security zones.

**Agent:** security
**Skill:** security-testing
**Output:** `output/engagements/segmentation-tests/{client}-{YYYY-MM}/`

---

## Quick Start

```
/segmentation-test
```

Collects network topology → Validates segmentation → Routes to security agent

---

## When to Use

✅ **Use /segmentation-test when:**
- Validate network segmentation between zones (DMZ, internal, management)
- Test firewall rules and ACLs
- Verify VLAN isolation and trunk security
- Assess zero-trust network architecture
- PCI DSS, HIPAA, or compliance segmentation validation

❌ **Don't use if:** Need full network vulnerability scanning → use `/vuln-scan`

---

## Workflow

1. **Context Collection** - Prompts gather test mode, network topology, methodology
2. **Validation** - Check diagrams, access to systems, tool availability
3. **Agent Execution** - Route to security agent with security-testing skill
4. **Deliverables** - Generate reports in `output/engagements/segmentation-tests/{client}-{YYYY-MM}/`

**Estimated time:**
- Demo: 10-20 minutes
- Director: 2-8 hours

---

## Context Prompts

### Test Mode

**Question:** "What type of segmentation test is this?"

**Options:**
- **Director (Production)** - Comprehensive validation, all zones, compliance report
- **Demo (Testing)** - Quick connectivity validation, minimal documentation

**Default:** Director

---

### Network Topology Source

**Question:** "How will you provide network topology information?"

**Options:**
- **Network Diagram File** - Visio/PDF/PNG showing VLANs, zones, rules
- **Manual Description** - Text description of zones and isolation rules
- **Auto-Discovery** - Scan-based topology discovery (Nmap, traceroute, SNMP)

**Default:** Network Diagram File

---

### Test Methodology

**Question:** "What testing approach should be used?"

**Options:**
- **Manual Testing** - Human-driven tests, custom scripts, higher accuracy
- **Automated Testing** - Tool-based scanning, faster coverage
- **Hybrid** - Automated discovery + manual validation (recommended)

**Default:** Hybrid

---

### Security Zones to Test

**Question:** "Which security zones should be tested?"

**Options:**
- **DMZ → Internal** - Test DMZ/internal boundary
- **Internal → Management** - Test user/management boundary
- **VLAN Isolation** - Test VLAN-to-VLAN isolation
- **All Zones** - Comprehensive testing (recommended)

**Multiple selection:** Yes

**Default:** All Zones

---

### Access Credentials

**Question:** "Do you have network device credentials?"

**Options:**
- **Yes - Authenticated** - Credentials for switches/routers/firewalls, config review
- **No - Unauthenticated** - External testing, attacker perspective

**Default:** No - Unauthenticated

---

## Validation

Before agent execution:

- [x] Test mode selected
- [x] Topology source selected
- [x] Test methodology selected
- [x] Security zones selected
- [x] Network diagram exists (if File option)
- [x] Connectivity to test systems
- [x] Tools available (Nmap, segmentation scripts)
- [x] Credentials valid (if authenticated)
- [x] Output directory writable

**Error Handling:**

```
Diagram missing:
  → Display: "Network diagram not found at {path}"
  → Suggest: "Provide diagram file or use Manual/Auto-Discovery"
  → Options: [Specify Path] [Switch to Manual] [Abort]

Cannot access test systems:
  → Display: "No connectivity to test systems in target zones"
  → Suggest: "Connect via Twingate/VPN and verify network access"
  → Options: [Retry] [Abort]

No authorization:
  → Display: "⚠️ AUTHORIZATION REQUIRED for segmentation testing"
  → Ask: "Do you have written authorization?" [Yes/No]
  → If No: ABORT immediately
  → If Yes: Document source, proceed
```

---

## Agent Routing

```typescript
Task({
  subagent_type: "security",
  model: "sonnet",
  prompt: `
Mode: {mode} (director/demo)
Workflow: segmentation-test
Skill: security-testing

Context:
- Test Mode: {Director/Demo}
- Topology Source: {diagram|manual|auto-discovery}
- Test Methodology: {manual|automated|hybrid}
- Security Zones: {zones-list}
- Authentication: {authenticated|unauthenticated}
- Credentials: {file-path-or-none}

Files:
- Output: output/engagements/segmentation-tests/{client}-{YYYY-MM}/

Instructions:
{mode-specific instructions}

Execute security-testing SKILL.md segmentation-test workflow.
`
})
```

**Agent loads:**
1. `agents/security.md` (via PreToolUse hook)
2. `skills/security-testing/SKILL.md` (via load-agent-skill-context hook)
3. Tools referenced in skill workflows (via tool awareness system)

---

## Output Structure

**Director Mode:**
```
output/engagements/segmentation-tests/{client}-{YYYY-MM}/
├── SCOPE.md
├── FINDINGS.md
├── STATUS.md
├── network-topology/
│   ├── provided-diagram.pdf
│   ├── discovered-topology.png
│   └── zone-matrix.csv
├── results/
│   ├── connectivity-tests.txt
│   ├── firewall-rule-analysis.md
│   ├── bypass-attempts.log
│   └── compliance-report.pdf
└── session-state.md
```

**Demo Mode:**
```
output/engagements/segmentation-tests/{client}-{YYYY-MM}/
├── demo-results.txt
└── zone-checks.log
```

---

## Examples

### PCI DSS Compliance Test (Director)

```
/segmentation-test
→ Mode: Director | Topology: Diagram | Test: Hybrid | Auth: Yes

Result: Full PCI DSS segmentation test (4-8 hours)
Output: output/engagements/segmentation-tests/client-pci-2025-12/
```

### Quick VLAN Check (Demo)

```
/segmentation-test
→ Mode: Demo | Topology: Manual (3 VLANs) | Test: Automated

Result: Quick VLAN isolation check (~10-15 min)
```

---

## Related Commands

- `/pentest` - Full penetration testing (may include segmentation)
- `/vuln-scan` - Network vulnerability scanning
- `/secure-config` - Network device configuration hardening
- `/risk-assessment` - Compliance risk assessment

---

## Security

**Authorization:**
- Written authorization required
- Confirm scope includes all VLANs/subnets
- Document in SCOPE.md

**Production Impact:**
- Schedule during maintenance windows
- Start with passive discovery
- Test non-production zones first
- Monitor for network impact

**Compliance Validation:**
- PCI DSS Requirement 1 (Network Segmentation)
- HIPAA Security Rule (Network Controls)
- NIST 800-53 SC-7 (Boundary Protection)
- ISO 27001 A.13.1 (Network Security)
- SOC 2 CC6.6 (Logical Access Controls)

---

**Version:** 1.0
**Last Updated:** 2025-12-12
**Framework:** Intelligence Adjacent (IA)
