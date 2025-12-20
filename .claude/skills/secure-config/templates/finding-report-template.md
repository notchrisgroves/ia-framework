---
type: template
name: finding-report-template
category: CATEGORY_NAME
classification: public
version: 1.0
last_updated: 2025-12-02
---

# [Control ID]: [Control Title]

**Client:** [Client Name]
**Date Identified:** [YYYY-MM-DD]
**Auditor:** [Your Name]
**Finding ID:** [CIS-001 / STIG-001]

---

## Control Information

**Framework:** [CIS Ubuntu 22.04 Benchmark v1.0.0 / DISA RHEL 8 STIG V1R12]
**Control ID:** [CIS 5.2.1 / STIG V-230221]
**Control Title:** [Ensure permissions on /etc/ssh/sshd_config are configured]
**Level/Category:** [Level 1 Server / CAT II]
**Assessment Type:** [Automated / Manual]

---

## Status

**Status:** FAIL
**Severity:** [Critical / High / Medium / Low]
**Priority:** [P0 / P1 / P2 / P3]
**Risk Rating:** [Critical / High / Medium / Low]

---

## Current State

**Configuration File:** [/etc/ssh/sshd_config]
**Current Setting:**
```
Owner: root:ssh
Permissions: 644 (rw-r--r--)
```

**Evidence:**
```bash
$ stat /etc/ssh/sshd_config
  File: /etc/ssh/sshd_config
  Size: 3264      	Blocks: 8          IO Block: 4096   regular file
Device: 802h/2050d	Inode: 131097      Links: 1
Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (  113/     ssh)
Access: 2025-01-02 14:30:22.123456789 -0500
Modify: 2024-11-15 10:15:30.987654321 -0500
Change: 2024-11-15 10:15:30.987654321 -0500
 Birth: 2024-10-01 08:00:00.000000000 -0500
```

**Screenshot:** [evidence/screenshot-ssh-config-perms.png]

---

## Required State

**Expected Setting:**
```
Owner: root:root
Permissions: 600 (rw-------)
```

**Rationale:**
[The /etc/ssh/sshd_config file contains configuration specifications for sshd. Incorrect permissions could expose the file to unauthorized access, potentially revealing sensitive configuration details such as allowed authentication methods, enabled ciphers, and access control rules.]

**References:**
- [CIS Ubuntu 22.04 Benchmark v1.0.0, Section 5.2.1, Page 312]
- [NIST SP 800-53 Rev. 5: AC-3 (Access Enforcement)]
- [CIS Controls v8: 4.1 (Establish and Maintain a Secure Configuration Process)]

---

## Impact Assessment

### Security Impact

**Confidentiality:** MEDIUM
- SSH configuration details readable by non-root users
- Potential exposure of allowed cipher suites, authentication methods

**Integrity:** LOW
- File is not world-writable, integrity maintained

**Availability:** NONE
- No direct availability impact

### Operational Impact

**Service Disruption:** None
**User Impact:** None
**Downtime Required:** No (SSH service restart only, existing connections maintained)

### Exploitability

**Attack Vector:** Local
**Privileges Required:** Low (any local user can read file)
**User Interaction:** None
**Complexity:** Low

**CVSS v3.1 Score:** 3.3 (Low)
**CVSS Vector:** CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N

### Environment Context

**Environment:** [Production]
**System Role:** [Web Server]
**Compensating Controls:** [None]
**Mitigating Factors:** [SSH access restricted by IP whitelist + key-based auth + 2FA]

---

## Remediation

### Automated Remediation

**Script:**
```bash
#!/bin/bash
# Remediation for CIS 5.2.1

# Backup current configuration
BACKUP_DIR="/var/backups/compliance/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp /etc/ssh/sshd_config "$BACKUP_DIR/sshd_config.backup"

# Apply fix
chown root:root /etc/ssh/sshd_config
chmod 600 /etc/ssh/sshd_config

# Restart SSH service (existing connections maintained)
systemctl restart sshd

# Validate
echo "Validating fix..."
stat -c '%U:%G %a' /etc/ssh/sshd_config
# Expected: root:root 600

echo "Remediation complete. Backup saved to: $BACKUP_DIR"
```

**Execution:**
```bash
sudo bash remediate-cis-5-2-1.sh
```

### Manual Remediation

**Step-by-Step Procedure:**

1. **Backup current configuration:**
   ```bash
   sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup.$(date +%Y%m%d_%H%M%S)
   ```

2. **Change ownership to root:root:**
   ```bash
   sudo chown root:root /etc/ssh/sshd_config
   ```

3. **Change permissions to 600:**
   ```bash
   sudo chmod 600 /etc/ssh/sshd_config
   ```

4. **Verify changes:**
   ```bash
   sudo stat /etc/ssh/sshd_config
   # Expected: Access: (0600/-rw-------) Uid: (0/root) Gid: (0/root)
   ```

5. **Restart SSH service:**
   ```bash
   sudo systemctl restart sshd
   ```

6. **Test SSH connectivity:**
   ```bash
   ssh user@localhost
   # Verify successful authentication
   ```

---

## Rollback Procedure

**If remediation causes issues:**

1. **Stop SSH service:**
   ```bash
   sudo systemctl stop sshd
   ```

2. **Restore backup:**
   ```bash
   sudo cp /etc/ssh/sshd_config.backup.YYYYMMDD_HHMMSS /etc/ssh/sshd_config
   ```

3. **Restart SSH service:**
   ```bash
   sudo systemctl start sshd
   ```

4. **Verify service operational:**
   ```bash
   sudo systemctl status sshd
   ssh user@localhost
   ```

**Rollback Script:**
```bash
#!/bin/bash
# Rollback for CIS 5.2.1

BACKUP_FILE="$1"

if [ -z "$BACKUP_FILE" ] || [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file not found"
    echo "Usage: $0 /path/to/sshd_config.backup"
    exit 1
fi

# Restore configuration
cp "$BACKUP_FILE" /etc/ssh/sshd_config

# Restart SSH
systemctl restart sshd

echo "Rollback complete. SSH configuration restored from: $BACKUP_FILE"
```

---

## Validation

### Post-Remediation Validation

**Validation Commands:**
```bash
# Check file ownership
stat -c '%U:%G' /etc/ssh/sshd_config
# Expected: root:root

# Check file permissions
stat -c '%a' /etc/ssh/sshd_config
# Expected: 600

# Verify SSH service operational
systemctl status sshd
# Expected: active (running)

# Test SSH connectivity
ssh user@localhost
# Expected: Successful authentication
```

**Expected Results:**
- File owner: root:root
- File permissions: 600
- SSH service: active (running)
- SSH connectivity: operational

**Validation Checklist:**
- [ ] File ownership is root:root
- [ ] File permissions are 600
- [ ] SSH service is running
- [ ] SSH authentication works
- [ ] No errors in /var/log/auth.log

---

## Implementation Plan

**Recommended Timeline:**
- **Critical (P0):** Within 24 hours
- **High (P1):** Within 1 week
- **Medium (P2):** Within 30 days
- **Low (P3):** Next maintenance cycle

**This Finding Priority:** [P1 (High)]

**Implementation Schedule:**
1. **Preparation:** [2025-01-03] - Review remediation script, obtain change approval
2. **Staging Test:** [2025-01-04] - Apply remediation on staging server, validate
3. **Production:** [2025-01-05] - Apply remediation during maintenance window (20:00-21:00 EST)
4. **Validation:** [2025-01-05] - Post-remediation validation, update compliance tracking

**Change Management:**
- Change Request ID: [CHG-2025-001]
- Approval Required: [Yes / No]
- Maintenance Window: [2025-01-05 20:00-21:00 EST]
- Communication Plan: [Notify users of potential brief SSH disruption]

---

## Alternative Approaches

### Option 1: Automated Remediation (Recommended)
- **Pros:** Fast, consistent, repeatable across multiple systems
- **Cons:** Requires testing, potential for unintended consequences
- **Effort:** Low (15 minutes)

### Option 2: Manual Remediation
- **Pros:** Full control, step-by-step verification
- **Cons:** Time-consuming for multiple systems, potential for human error
- **Effort:** Medium (30 minutes per system)

### Option 3: Configuration Management (Ansible/Puppet)
- **Pros:** Automated, idempotent, scalable to entire fleet
- **Cons:** Requires configuration management infrastructure, initial setup time
- **Effort:** High (2-3 hours initial setup, 5 minutes per system thereafter)

**Recommended Approach:** [Option 1 - Automated Remediation Script]

---

## Dependencies

**Prerequisites:**
- Root/sudo access to target system
- SSH service installed and running
- Backup directory with sufficient disk space

**Related Findings:**
- [CIS-002: Ensure permissions on SSH public host key files are configured]
- [CIS-003: Ensure SSH access is limited]

**Dependent Controls:**
- None (standalone control)

---

## Risk Acceptance

**If remediation is deferred or declined:**

**Risk Statement:**
[By accepting this risk, [Client Name] acknowledges that SSH configuration details may be readable by non-root users, potentially exposing sensitive configuration information. This increases the risk of information disclosure and may aid attackers in reconnaissance activities.]

**Risk Owner:** [Name, Title]
**Acceptance Date:** [YYYY-MM-DD]
**Review Date:** [YYYY-MM-DD] (90 days)

**Justification:**
[Explain business reason for accepting risk, compensating controls, mitigation measures]

**Compensating Controls:**
- [SSH access restricted by IP whitelist]
- [Key-based authentication required (no passwords)]
- [Two-factor authentication enforced]

---

## Historical Information

**Date Identified:** [2025-01-02]
**Date Remediated:** [2025-01-05]
**Date Validated:** [2025-01-05]
**Status:** [Open / In Progress / Remediated / Risk Accepted / False Positive]

**Remediation History:**
| Date | Action | Performed By | Status |
|------|--------|--------------|--------|
| 2025-01-02 | Finding identified during CIS scan | Security Team | Open |
| 2025-01-03 | Remediation script created | Security Team | In Progress |
| 2025-01-04 | Tested on staging | Ops Team | In Progress |
| 2025-01-05 | Applied to production | Ops Team | Remediated |
| 2025-01-05 | Validation completed | Security Team | Closed |

---

## Notes

[Additional notes, observations, or context specific to this finding]

---

**Finding Template Version:** 2.0
**Last Updated:** 2025-12-02
**Template:** Security configuration finding report for non-compliant controls
