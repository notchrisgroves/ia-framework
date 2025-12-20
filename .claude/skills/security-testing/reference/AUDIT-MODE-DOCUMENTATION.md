# Audit Mode Documentation

**Comprehensive command and output logging for compliance requirements and legal defense.**

---

## 📊 Audit Mode: Compliance & Legal Defense Logging

### Purpose

Audit mode provides complete audit trail for:
- **Compliance**: SOC 2, ISO 27001, PCI DSS, client SLA requirements
- **Legal Defense**: Prove what you did/didn't do during testing
- **Incident Correlation**: Map testing activities to client-observed events
- **Quality Assurance**: Post-engagement methodology review

### When to Enable Audit Mode

**✅ ENABLE for:**
- Client pentests (contractual audit trail requirement)
- Bug bounties on high-value programs (legal protection)
- Compliance-driven assessments (SOC 2, ISO 27001, etc.)
- Any engagement where client may question your activities

**⚠️ OPTIONAL for:**
- Personal training/practice on safe targets
- Quick tool connectivity tests (Demo mode)
- Internal security assessments with no compliance requirement

### How Audit Mode Works

**Automatic Logging:**
1. Every command executed (timestamp, tool, target, options)
2. Full command output (raw unfiltered)
3. Scope verification checkpoints
4. Exit codes and execution duration
5. SHA256 hashes for integrity verification

**File Structure:**
```
[engagement]/
└── audit-logs/
    ├── README.md                    # Audit documentation
    ├── audit-config.json            # Configuration
    ├── audit-index.json             # Quick lookup
    ├── sessions/
    │   ├── session-*.jsonl          # Structured (machine-readable)
    │   ├── session-*.txt            # Human-readable transcript
    │   └── session-*-outputs/       # Raw tool outputs
    └── compliance/
        └── timeline-*.md            # Client-facing report
```

**Performance Impact:**
- Enabled (full): ~5-10ms overhead per command (async writes)
- Enabled (commands only): ~2-3ms overhead
- Disabled: 0ms overhead

**Storage Impact:**
- Typical 4-hour engagement: ~10-50 MB (depends on scan output size)
- Retention: 7 years (standard compliance requirement)

### Mode Selection Integration

**Prompt shown during engagement setup:**

```
🎯 ENGAGEMENT CONFIGURATION:

1. ENGAGEMENT MODE:
   A) DIRECTOR MODE (Production)
   B) MENTOR MODE (Learning)
   C) DEMO MODE (Testing/Quick Validation)

2. AUDIT LOGGING: (Compliance & Legal Defense)
   A) ENABLED - Full command and output logging
      └─ Use for: Client pentests, bug bounties, compliance assessments
      └─ Impact: ~10-50 MB storage, ~5-10ms per command
      └─ Benefit: Complete audit trail, legal protection, compliance

   B) DISABLED - No audit trail
      └─ Use for: Personal practice, quick tests, non-compliance work
      └─ Impact: No overhead, no audit trail
      └─ Benefit: Faster execution, less storage

Select engagement mode [A/B/C]:
Enable audit logging? [Y/N]:
```

**Store configuration in README.md:**
```yaml
engagement_mode: director
audit_logging: enabled       # enabled | disabled
audit_verbosity: full        # full | commands
```

### Usage

**Initialize at engagement start:**

```python
from scripts.security.audit_wrapper import AuditSession

# Context manager (automatic cleanup)
with AuditSession(engagement_dir="output/engagements/pentest/client-2025-11", enabled=True):
    # All tool executions are audited
    result = nmap.nmap(target="192.168.1.100", options="-sV", engagement_dir="...")
    # ... rest of testing ...
# Reports generated automatically
```

**Log scope verification:**

```python
from scripts.security.audit_wrapper import log_scope_verification

# Before testing each target
log_scope_verification(
    target="192.168.1.100",
    verified=True,          # Whether target is in scope
    scope_line=45           # Line in SCOPE.md where target appears
)
```

### Viewing Audit Logs

```bash
# View latest session
python scripts/security/audit_viewer.py --engagement output/engagements/pentest/client-2025-11

# View transcript
python scripts/security/audit_viewer.py --engagement ... --format transcript

# Search for target
python scripts/security/audit_viewer.py --engagement ... --search-target 192.168.1.100

# Verify integrity
python scripts/security/audit_viewer.py --engagement ... --verify-integrity

# Export compliance report
python scripts/security/audit_viewer.py --engagement ... --export-compliance report.md
```

### Use Cases

**Client Questions Your Activities:**
```bash
# Export timeline showing exactly what was done at specific time
audit_viewer.py --export-compliance timeline.md
```

**Legal Defense - Prove What You Didn't Do:**
```bash
# Search for allegedly-tested target (shows "not found")
audit_viewer.py --search-target out-of-scope-server.com
```

**Compliance Audit:**
```bash
# Show scope verification checkpoints before each test
audit_viewer.py --format transcript | grep "SCOPE VERIFICATION"
```

**Verify No Tampering:**
```bash
# Cryptographic integrity verification
audit_viewer.py --verify-integrity
# Result: "✅ All files passed integrity verification (SHA256)"
```

### Implementation Details

**Complete documentation:**
- **Core Logger**: `scripts/security/audit_logger.py` (async logging engine)
- **Wrapper Module**: `scripts/security/audit_wrapper.py` (decorator/wrapper for tools)
- **Viewer CLI**: `scripts/security/audit_viewer.py` (view, search, verify, export)

**Security & Privacy:**

⚠️ Audit logs contain sensitive data (credentials, tokens, vulnerabilities)

**Best Practices:**
1. Encrypt logs before transmitting to client
2. Redact credentials/tokens before sharing
3. Follow client data handling requirements
4. Delete after retention period (7 years)
5. Restrict filesystem permissions
6. Use encrypted backups

---

**Referenced from:** `SKILL.md` - Audit mode configuration and usage
