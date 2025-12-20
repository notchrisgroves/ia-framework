---
name: vuln-scan
description: Automated vulnerability scanning with Director/Demo modes
---

# /vuln-scan - Automated Vulnerability Scanning

Execute automated vulnerability scans for web applications, networks, APIs, and cloud infrastructure.

**Agent:** security
**Skill:** security-testing
**Output:** `output/engagements/vuln-scans/{target}-{YYYY-MM}/`

---

## Quick Start

```
/vuln-scan
```

Collects scan parameters → Validates authorization → Routes to security agent

---

## When to Use

✅ **Use /vuln-scan when:**
- Automated vulnerability detection needed
- Quick security assessment required
- Compliance scanning for audit evidence
- Testing web apps, networks, APIs, or cloud infrastructure
- Unauthenticated or authenticated scanning

❌ **Don't use if:** Need manual exploitation → use `/pentest`

---

## Workflow

1. **Context Collection** - Prompts gather scan mode, target type, depth, authentication
2. **Validation** - Verify authorization, target reachability, tool availability
3. **Agent Execution** - Route to security agent with security-testing skill
4. **Deliverables** - Generate reports in `output/engagements/vuln-scans/{target}-{YYYY-MM}/`

**Estimated time:**
- Demo: 5-15 minutes
- Director: 30 minutes - 4 hours

---

## Context Prompts

### Scan Mode

**Question:** "What type of scan engagement is this?"

**Options:**
- **Director (Production)** - Full automated scan, complete deliverables
- **Demo (Testing)** - Quick validation without full coverage

**Default:** Director

---

### Target Type

**Question:** "What type of target are you scanning?"

**Options:**
- **Web Application** - OWASP Top 10, web vulnerabilities (Nuclei, ZAP, Nikto)
- **Network Infrastructure** - Ports, services, network vulns (Nmap, OpenVAS)
- **API Endpoints** - REST/GraphQL/SOAP security (auth, injection, access control)
- **Cloud Infrastructure** - AWS/Azure/GCP misconfigurations

**Default:** Web Application

---

### Scan Depth

**Question:** "How thorough should the scan be?"

**Options:**
- **Quick** - Essential checks (10-30 min), minimal false positives
- **Standard** - Common vulns (1-2 hours), critical/high severity focus
- **Thorough** - All signatures (3-6 hours), maximum coverage

**Default:** Standard

---

### Authentication

**Question:** "Will you provide authenticated access?"

**Options:**
- **Unauthenticated** - External perspective, no credentials
- **Authenticated** - Valid credentials for deeper coverage

**Default:** Unauthenticated

---

### Credentials Source (Conditional)

**Show if:** Authentication = Authenticated

**Question:** "How will you provide credentials?"

**Options:**
- **File Path** - JSON/YAML with credentials (secure format)
- **Manual Input** - Paste credentials directly

**Default:** File Path

---

## Validation

Before agent execution:

- [x] Scan mode selected
- [x] Target type selected
- [x] Scan depth selected
- [x] Authorization verified
- [x] Target reachable (ping/HTTP check)
- [x] Tools available (Nuclei, Nmap, etc.)
- [x] Credentials valid (if authenticated)
- [x] Output directory writable

**Error Handling:**

```
Target not reachable:
  → Display: "Cannot reach target at {target}"
  → Suggest: "Check DNS resolution and network connectivity"
  → Options: [Retry] [Abort]

Tools missing:
  → Display: "Required scanning tools not available"
  → Suggest: "Connect to VPS via Twingate for tool access"
  → Options: [Connect and Retry] [Abort]

No authorization:
  → Display: "⚠️ AUTHORIZATION REQUIRED for vulnerability scanning"
  → Ask: "Do you have written authorization to scan?" [Yes/No]
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
Workflow: vulnerability-scan
Skill: security-testing

Context:
- Scan Mode: {Director/Demo}
- Target Type: {web|network|api|cloud}
- Scan Depth: {quick|standard|thorough}
- Authentication: {unauthenticated|authenticated}
- Credentials: {file-path-or-manual}

Files:
- Output: output/engagements/vuln-scans/{target}-{YYYY-MM}/

Instructions:
{mode-specific instructions}

Execute security-testing SKILL.md vulnerability-scan workflow.
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
output/engagements/vuln-scans/{target}-{YYYY-MM}/
├── SCOPE.md
├── FINDINGS.md
├── STATUS.md
├── results/
│   ├── nuclei-output.json
│   ├── nmap-scan.xml
│   ├── vulnerability-report.pdf
│   └── screenshots/
└── session-state.md
```

**Demo Mode:**
```
output/engagements/vuln-scans/{target}-{YYYY-MM}/
├── demo-results.txt
└── tool-validation.log
```

---

## Examples

### Web Application (Director)

```
/vuln-scan
→ Mode: Director | Target: Web Application | Depth: Standard

Result: Full vulnerability scan (1-2 hours)
Output: output/engagements/vuln-scans/example-com-2025-12/
```

### Quick Network Check (Demo)

```
/vuln-scan
→ Mode: Demo | Target: Network Infrastructure | Depth: Quick

Result: Quick port scan (~5-10 min), confirms tool connectivity
```

---

## Related Commands

- `/pentest` - Full penetration testing with manual exploitation
- `/segmentation-test` - Network segmentation validation
- `/code-review` - Source code security review
- `/risk-assessment` - Formal cybersecurity risk assessment

---

## Security

**Authorization:**
- Custom targets require explicit written authorization
- SCOPE.md validated
- Targets must be: own infrastructure, authorized bug bounty, or safe test environments
- Never scan without authorization

**Credentials Security:**
- Store outside git (.gitignore)
- Encrypt at rest if possible
- Delete after scan completion

**Legal Compliance:**
- Written authorization required
- CFAA compliance enforced
- Safe targets inherently authorized

---

**Version:** 1.0
**Last Updated:** 2025-12-12
**Framework:** Intelligence Adjacent (IA)
