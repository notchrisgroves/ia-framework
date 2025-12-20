# Audit Mode Integration Guide

**Purpose**: Integrate audit logging into security tool wrappers for compliance and legal defense.

**Version**: 1.0
**Created**: 2025-11-23
**Status**: Production Ready

---

## Overview

Audit mode provides comprehensive command and output logging for penetration testing engagements. This guide shows how to integrate audit logging into:

1. Code API wrappers (`servers/*/*`)
2. Security agent workflows
3. Engagement initialization

---

## Architecture

### Components

```
tools/security/
├── audit_logger.py          # Core audit logging module
├── audit_wrapper.py          # Decorator/wrapper for tool integration
├── audit_viewer.py           # CLI viewer and compliance report generator
└── AUDIT-INTEGRATION-GUIDE.md (This file)
```

### Data Flow

```
Security Tool Call
     ↓
Audit Wrapper (if enabled)
     ↓
Execute Tool → Capture Output
     ↓
Audit Logger (async write)
     ↓
Files: .jsonl (structured) + .txt (human-readable) + outputs/
```

---

## Integration Step 1: Initialize Audit Logging at Engagement Start

### In Security Agent Workflow

When starting a new penetration testing session:

```python
from tools.security.audit_wrapper import initialize_audit_logging, shutdown_audit_logging, AuditSession

# Method 1: Initialize at session start (manual control)
def start_pentest_session(engagement_dir: str, audit_enabled: bool):
    # Initialize audit logging
    initialize_audit_logging(
        engagement_dir=engagement_dir,
        enabled=audit_enabled
    )

    # ... rest of testing workflow ...

    # At end of session
    shutdown_audit_logging()

# Method 2: Use context manager (automatic cleanup)
def start_pentest_session(engagement_dir: str, audit_enabled: bool):
    with AuditSession(engagement_dir=engagement_dir, enabled=audit_enabled):
        # All tool executions within this block are audited
        result = nmap.nmap(target="192.168.1.1", options="-sV", engagement_dir=engagement_dir)
        # ... rest of testing ...
    # Audit logs automatically closed and reports generated
```

### Mode Selection Integration

Add audit mode to the Director/Mentor/Demo mode selection:

```python
# In security agent or /pentest command

# Show mode selection dialog
print("""
🎯 ENGAGEMENT CONFIGURATION:

1. ENGAGEMENT MODE:
   A) DIRECTOR MODE (Production)
   B) MENTOR MODE (Learning)
   C) DEMO MODE (Testing/Quick Validation)

2. AUDIT LOGGING:
   A) ENABLED - Full command and output logging (compliance/legal defense)
   B) DISABLED - No audit trail (faster, less storage)

Select engagement mode [A/B/C]: """)

engagement_mode = input().strip().upper()

print("\nEnable audit logging? [Y/N]: ")
audit_enabled = input().strip().upper() == 'Y'

# Store in README.md
readme_content = f"""
engagement_mode: {engagement_mode.lower()}
audit_logging: {"enabled" if audit_enabled else "disabled"}
"""
```

Store configuration in `README.md`:

```yaml
# Engagement Configuration
engagement_mode: director       # director | mentor | demo
audit_logging: enabled          # enabled | disabled
audit_verbosity: full           # full | commands
```

---

## Integration Step 2: Wrap Security Tools

### Method 1: Using Decorator (Recommended)

**For new tools or refactoring:**

```python
# Example: servers/kali_pentest/nmap.py

from tools.security.audit_wrapper import with_audit_logging

@with_audit_logging(tool="nmap", category="kali_pentest")
def nmap(target: str, options: str, engagement_dir: str) -> dict:
    """
    Run nmap scan with audit logging

    Args:
        target: Target to scan
        options: Nmap options
        engagement_dir: Path to engagement directory

    Returns:
        Dict with summary, outputFile, message, success
    """
    # Original tool implementation
    command = f"nmap {options} {target}"

    # Execute via SSH/Docker
    result = subprocess.run(...)

    # Parse and return
    return {
        "summary": parsed_summary,
        "output": full_output,
        "outputFile": output_file_path,
        "message": "Scan complete",
        "success": True
    }
```

**That's it!** The decorator automatically:
- Logs command with timestamp
- Captures full output
- Records exit code
- Writes to audit log (if enabled)
- Returns original result unchanged

### Method 2: Using execute_with_audit (Manual Control)

**For complex tool logic:**

```python
from tools.security.audit_wrapper import execute_with_audit

def nuclei(target: str, severity: str, engagement_dir: str, scope_verified: bool = False) -> dict:
    """Run nuclei scan with manual audit control"""

    command = f"nuclei -u {target} -severity {severity}"

    def run_nuclei():
        # Actual execution logic
        result = subprocess.run(...)
        return {
            "summary": {...},
            "output": result.stdout,
            "success": result.returncode == 0
        }

    # Execute with audit logging
    return execute_with_audit(
        tool="nuclei",
        category="kali_pentest",
        command=command,
        target=target,
        engagement_dir=engagement_dir,
        execution_func=run_nuclei,
        scope_verified=scope_verified  # Log scope verification status
    )
```

---

## Integration Step 3: Log Scope Verifications

**CRITICAL**: Log scope verification checks for compliance:

```python
from tools.security.audit_wrapper import log_scope_verification

# Before testing a target
def verify_and_test_target(target: str, scope_file: str):
    # Read SCOPE.md
    with open(scope_file, 'r') as f:
        scope_content = f.readlines()

    # Check if target in scope
    in_scope = False
    scope_line = None

    for i, line in enumerate(scope_content, start=1):
        if target in line:
            in_scope = True
            scope_line = i
            break

    # LOG SCOPE VERIFICATION
    log_scope_verification(
        target=target,
        verified=in_scope,
        scope_line=scope_line
    )

    if not in_scope:
        raise ValueError(f"Target {target} NOT IN SCOPE")

    # Proceed with testing
    result = nmap.nmap(target=target, options="-sV", engagement_dir="...")
```

This creates audit trail entries like:

```
[14:30:22.123] SCOPE VERIFICATION
────────────────────────────────────────────────────────────────────────────────
Target:      192.168.1.100
Status:      ✅ IN SCOPE
Reference:   SCOPE.md line 45
────────────────────────────────────────────────────────────────────────────────
```

---

## Integration Step 4: Update Engagement Templates

### Update SCOPE-TEMPLATE.md

Add audit logging configuration section:

```markdown
## Audit Logging Configuration

**Audit Mode**: [ENABLED / DISABLED]
**Verbosity**: [FULL / COMMANDS]
**Retention**: 7 years (compliance requirement)

Audit logs location: `audit-logs/sessions/`
```

### Update README-TEMPLATE.md

Add audit configuration:

```markdown
## Session Configuration

- **Engagement Mode**: Director / Mentor / Demo
- **Audit Logging**: Enabled / Disabled
- **Audit Verbosity**: Full (command + output) / Commands (command only)

## Audit Logs

📊 **Audit logging is ENABLED for this engagement**

View logs:
```bash
# View latest session
python tools/security/audit_viewer.py --engagement .

# View specific session
python tools/security/audit_viewer.py --engagement . --session session-20251123-143022

# Export compliance report
python tools/security/audit_viewer.py --engagement . --export-compliance compliance-report.md
```

Audit logs stored in: `audit-logs/sessions/`
```

---

## Usage Examples

### Example 1: Start Engagement with Audit Logging

```python
from tools.security.audit_wrapper import AuditSession
from servers.kali_pentest import nmap, nuclei

# Start audited session
engagement_dir = "output/engagements/pentest/acme-2025-11"

with AuditSession(engagement_dir=engagement_dir, enabled=True):
    # All tools are automatically audited

    # Run nmap
    nmap_result = nmap.nmap(
        target="192.168.1.100",
        options="-sV -sC",
        engagement_dir=engagement_dir
    )

    # Run nuclei
    nuclei_result = nuclei.nuclei(
        target="https://example.com",
        severity="critical,high",
        engagement_dir=engagement_dir
    )

    # ... more testing ...

# Session automatically closed, compliance reports generated
```

Result:
```
✅ Audit logging ENABLED for acme-2025-11
   Logs: output/engagements/pentest/acme-2025-11/audit-logs/sessions

[Testing happens here...]

📊 Generating audit compliance reports...
✅ Audit logging session closed
```

### Example 2: View Audit Logs

```bash
# View latest session as table
python tools/security/audit_viewer.py \
    --engagement output/engagements/pentest/acme-2025-11

# View human-readable transcript
python tools/security/audit_viewer.py \
    --engagement output/engagements/pentest/acme-2025-11 \
    --format transcript

# Search for commands against specific target
python tools/security/audit_viewer.py \
    --engagement output/engagements/pentest/acme-2025-11 \
    --search-target 192.168.1.100

# Verify output integrity
python tools/security/audit_viewer.py \
    --engagement output/engagements/pentest/acme-2025-11 \
    --verify-integrity

# Export compliance report
python tools/security/audit_viewer.py \
    --engagement output/engagements/pentest/acme-2025-11 \
    --export-compliance audit-logs/compliance/report.md
```

### Example 3: Disable Audit Logging (Demo Mode)

```python
# For quick tests where audit trail is not needed
with AuditSession(engagement_dir=engagement_dir, enabled=False):
    # Tools execute normally without audit overhead
    result = nmap.nmap(...)
```

---

## File Structure After Integration

```
output/engagements/pentest/acme-2025-11/
├── SCOPE.md
├── README.md
├── creds.txt
├── 00-scope/
├── 01-planning/
├── 02-reconnaissance/
├── 03-vulnerability-assessment/
├── 04-exploitation/
├── 05-findings/
├── 06-reporting/
└── audit-logs/                              # NEW
    ├── README.md                           # Audit documentation
    ├── audit-config.json                   # Configuration
    ├── audit-index.json                    # Quick lookup index
    ├── sessions/
    │   ├── session-20251123-143022.jsonl   # Structured logs
    │   ├── session-20251123-143022.txt     # Human-readable transcript
    │   ├── session-20251123-143022-outputs/
    │   │   ├── cmd-001-nmap-output.txt
    │   │   ├── cmd-002-nuclei-output.txt
    │   │   └── ...
    │   ├── session-20251123-180945.jsonl   # Session 2
    │   └── session-20251123-180945.txt
    └── compliance/
        └── timeline-20251123-143022.md     # Compliance report
```

---

## Compliance Use Cases

### Use Case 1: Client Requests Timeline of Testing

**Scenario**: Client asks "What were you testing at 14:45 UTC when we saw unusual traffic?"

**Solution**:
```bash
# Export timeline report
python tools/security/audit_viewer.py \
    --engagement output/engagements/pentest/client-2025-11 \
    --export-compliance timeline-report.md

# Send timeline-report.md to client
```

Timeline shows:
```
| 14:45:10 | nmap | 192.168.1.100 | `nmap -sV -p- 192.168.1.100` | 15.2s | ✅ Success |
```

### Use Case 2: Legal Defense - Prove What You Didn't Do

**Scenario**: Client claims you tested out-of-scope target. You need proof you didn't.

**Solution**:
```bash
# Search for target
python tools/security/audit_viewer.py \
    --engagement output/engagements/pentest/client-2025-11 \
    --search-target 10.0.0.50

# Result: "❌ No commands found for target: 10.0.0.50"
```

Provide JSONL file to legal counsel as proof.

### Use Case 3: SOC 2 Compliance Audit

**Scenario**: Auditor requests proof of scope verification before testing.

**Solution**:
```bash
# View transcript showing scope verifications
python tools/security/audit_viewer.py \
    --engagement output/engagements/pentest/client-2025-11 \
    --format transcript | grep "SCOPE VERIFICATION"
```

Shows all scope checks:
```
[14:30:22.123] SCOPE VERIFICATION
Target:      192.168.1.100
Status:      ✅ IN SCOPE
Reference:   SCOPE.md line 45
```

### Use Case 4: Verify No Tampering

**Scenario**: Need to prove audit logs haven't been altered.

**Solution**:
```bash
# Verify integrity
python tools/security/audit_viewer.py \
    --engagement output/engagements/pentest/client-2025-11 \
    --verify-integrity

# Result:
# ✅ All files passed integrity verification
# Results: 42 verified | 0 mismatches | 0 missing
```

---

## Performance Considerations

### Storage Impact

**Typical engagement (4 hours, 100 commands):**
- Structured logs (.jsonl): ~50-100 KB
- Transcripts (.txt): ~200-500 KB
- Tool outputs: ~10-50 MB (depends on scan size)
- **Total**: ~10-50 MB per session

**Recommendation**: Enable for production engagements, disable for quick tests.

### Performance Impact

- **Audit enabled (full)**: ~5-10ms overhead per command (async writes)
- **Audit enabled (commands only)**: ~2-3ms overhead (no output capture)
- **Audit disabled**: 0ms overhead

**Recommendation**: Use "full" verbosity for compliance engagements, "commands" for speed-sensitive testing.

---

## Security & Privacy

### Sensitive Data Handling

⚠️ **WARNING**: Audit logs contain:
- Full command outputs (may include credentials, tokens, session IDs)
- Target information (IPs, domains, internal hostnames)
- Vulnerability details (exploits, payloads)

**Best Practices**:
1. Encrypt audit logs before transmitting to client
2. Redact credentials/tokens before sharing
3. Follow client data handling requirements
4. Delete logs after retention period (7 years default)

### Access Control

Audit logs stored in engagement directory:
```
output/engagements/pentest/client-2025-11/audit-logs/
```

**Recommendation**:
- Keep engagement directories in `.gitignore`
- Restrict filesystem permissions (owner-only read/write)
- Use encrypted backups

---

## Troubleshooting

### Issue 1: Audit logs not being created

**Symptom**: No files in `audit-logs/sessions/`

**Cause**: Audit logging not initialized

**Solution**:
```python
# Add at start of testing session
from tools.security.audit_wrapper import initialize_audit_logging

initialize_audit_logging(engagement_dir="path/to/engagement", enabled=True)
```

### Issue 2: Tools not being logged

**Symptom**: Some tool calls missing from audit log

**Cause**: Tool wrapper not using audit integration

**Solution**: Wrap tool with decorator or execute_with_audit (see Integration Step 2)

### Issue 3: Large output files

**Symptom**: Audit logs consuming too much disk space

**Cause**: Full output capture for verbose tools (nmap -p-, nuclei)

**Solution**:
```python
# Use "commands" verbosity instead of "full"
initialize_audit_logging(
    engagement_dir="...",
    enabled=True,
    verbosity="commands"  # Only log commands, not outputs
)
```

Or compress old sessions:
```bash
# Compress session outputs
tar -czf audit-logs/archive/session-20251123-143022.tar.gz \
    audit-logs/sessions/session-20251123-143022-outputs/
rm -rf audit-logs/sessions/session-20251123-143022-outputs/
```

---

## Testing the Integration

### Quick Test

```python
# test_audit.py
from tools.security.audit_wrapper import AuditSession, log_scope_verification

engagement_dir = "scratchpad/test-engagement"

with AuditSession(engagement_dir=engagement_dir, enabled=True):
    # Log scope verification
    log_scope_verification(target="192.168.1.1", verified=True, scope_line=10)

    # Simulate tool execution
    from servers.kali_pentest import nmap
    result = nmap.nmap(
        target="scanme.nmap.org",
        options="-sV -p80,443",
        engagement_dir=engagement_dir
    )

    print(f"Result: {result}")

# View logs
import subprocess
subprocess.run([
    "python", "tools/security/audit_viewer.py",
    "--engagement", engagement_dir
])
```

**Expected output**:
```
✅ Audit logging ENABLED for test-engagement
   Logs: scratchpad/test-engagement/audit-logs/sessions

[Tool execution...]

📊 Generating audit compliance reports...
✅ Audit logging session closed

AUDIT LOG: session-20251123-143022
────────────────────────────────────────────────────────────────────────────────
#    Time         Tool            Target                    Status   Duration
---- ------------ --------------- ------------------------- -------- ----------
1    14:30:22     nmap            scanme.nmap.org          ✅ OK     15.23s

1 total commands
```

---

## Maintenance

### Regular Tasks

**Weekly** (active engagement):
- Verify log integrity: `audit_viewer.py --verify-integrity`
- Archive old sessions: Compress `session-*-outputs/` directories

**Post-engagement**:
- Export compliance report: `audit_viewer.py --export-compliance`
- Archive entire engagement: `tar -czf engagement-archive.tar.gz audit-logs/`
- Verify backup integrity

**Yearly** (retention):
- Review 7-year retention policy
- Delete engagements older than 7 years
- Verify encrypted backups

---

## Version History

**v1.0** (2025-11-23)
- Initial release
- Core audit logger with async writes
- Decorator-based tool integration
- CLI viewer and compliance reports
- SHA256 integrity verification

**Planned Features** (v1.1+):
- Real-time log streaming for long scans
- Audit log compression (gzip)
- Redaction tool for sensitive data
- Integration with SIEM systems (Splunk, ELK)

---

**This integration provides complete audit trail capabilities for professional penetration testing engagements with minimal performance overhead and maximum compliance value.**
