---
type: template
name: compliance-checklist-template
category: CATEGORY_NAME
classification: public
version: 1.0
last_updated: 2025-12-02
---

# [Framework] [Platform] [Level] - Compliance Validation Checklist

**Client:** [Client Name]
**Date:** [YYYY-MM-DD]
**Auditor:** [Your Name]
**Benchmark:** [CIS Ubuntu 22.04 v1.0.0 / DISA RHEL 8 STIG V1R12]
**Level/Category:** [Level 1 Server / Cat I+II / Custom Baseline]
**Environment:** [Production / Staging / Development]

---

## Instructions

1. For each control, execute the audit command provided
2. Compare actual output against expected output
3. Mark status as PASS, FAIL, or N/A (Not Applicable)
4. Document evidence (command output, screenshots, configuration snippets)
5. For FAIL findings, assess severity and priority
6. Create individual finding documents for all FAIL controls

---

## Summary Statistics

**Total Controls:** [230]
**Passed:** [198]
**Failed:** [25]
**Not Applicable:** [7]
**Compliance Percentage:** [(198 / 223) * 100 = 88.8%]

**By Severity:**
- Critical (P0): [3 controls]
- High (P1): [8 controls]
- Medium (P2): [10 controls]
- Low (P3): [4 controls]

---

## Section 1: Initial Setup

### 1.1 Filesystem Configuration

#### 1.1.1 Ensure mounting of cramfs filesystems is disabled (Automated)

**Level:** Level 1 Server
**Status:** [ ] PASS [ ] FAIL [ ] N/A

**Audit:**
```bash
lsmod | grep cramfs
modprobe -n -v cramfs
```

**Expected:** No output (cramfs not loaded, prevented from loading)

**Actual:**
```
[Paste command output here]
```

**Evidence:** [Screenshot filename or description]

**Notes:** [Any relevant notes]

---

#### 1.1.2 Ensure mounting of squashfs filesystems is disabled (Automated)

**Level:** Level 1 Server
**Status:** [ ] PASS [ ] FAIL [ ] N/A

**Audit:**
```bash
lsmod | grep squashfs
modprobe -n -v squashfs
```

**Expected:** No output (squashfs not loaded, prevented from loading)

**Actual:**
```
[Paste command output here]
```

**Evidence:** [Screenshot filename or description]

**Notes:** [Any relevant notes]

---

## Section 2: Services

### 2.1 Special Purpose Services

#### 2.1.1 Ensure xinetd is not installed (Automated)

**Level:** Level 1 Server
**Status:** [ ] PASS [ ] FAIL [ ] N/A

**Audit:**
```bash
dpkg -s xinetd 2>&1 | grep "package 'xinetd' is not installed"
```

**Expected:** package 'xinetd' is not installed

**Actual:**
```
[Paste command output here]
```

**Evidence:** [Screenshot filename or description]

**Notes:** [Any relevant notes]

---

## Section 3: Network Configuration

### 3.1 Network Parameters (Host Only)

#### 3.1.1 Ensure IP forwarding is disabled (Automated)

**Level:** Level 1 Server
**Status:** [ ] PASS [ ] FAIL [ ] N/A

**Audit:**
```bash
sysctl net.ipv4.ip_forward
sysctl net.ipv6.conf.all.forwarding
```

**Expected:**
```
net.ipv4.ip_forward = 0
net.ipv6.conf.all.forwarding = 0
```

**Actual:**
```
[Paste command output here]
```

**Evidence:** [Screenshot filename or description]

**Notes:** [Any relevant notes]

---

## Section 4: Logging and Auditing

### 4.1 Configure System Accounting (auditd)

#### 4.1.1 Ensure auditd is installed (Automated)

**Level:** Level 2 Server
**Status:** [ ] PASS [ ] FAIL [ ] N/A

**Audit:**
```bash
dpkg -s auditd 2>&1 | grep "Status: install ok installed"
```

**Expected:** Status: install ok installed

**Actual:**
```
[Paste command output here]
```

**Evidence:** [Screenshot filename or description]

**Notes:** [Any relevant notes]

---

## Section 5: Access, Authentication and Authorization

### 5.2 Configure SSH Server

#### 5.2.1 Ensure permissions on /etc/ssh/sshd_config are configured (Automated)

**Level:** Level 1 Server
**Status:** [ ] PASS [X] FAIL [ ] N/A

**Audit:**
```bash
stat /etc/ssh/sshd_config
```

**Expected:** Access: (0600/-rw-------) Uid: (0/root) Gid: (0/root)

**Actual:**
```
Access: (0644/-rw-r--r--) Uid: (0/root) Gid: (113/ssh)
```

**Evidence:** screenshot-ssh-config-perms.png

**Notes:** SSH config is world-readable, exposing configuration details. Priority: P1 (High)

**Finding Document:** CIS-001-ssh-config-permissions.md

---

#### 5.2.2 Ensure permissions on SSH private host key files are configured (Automated)

**Level:** Level 1 Server
**Status:** [ ] PASS [ ] FAIL [ ] N/A

**Audit:**
```bash
find /etc/ssh -xdev -type f -name 'ssh_host_*_key' -exec stat {} \;
```

**Expected:** Access: (0600/-rw-------) Uid: (0/root) Gid: (0/root) for all keys

**Actual:**
```
[Paste command output here]
```

**Evidence:** [Screenshot filename or description]

**Notes:** [Any relevant notes]

---

## Section 6: System Maintenance

### 6.1 System File Permissions

#### 6.1.1 Audit system file permissions (Manual)

**Level:** Level 2 Server
**Status:** [ ] PASS [ ] FAIL [ ] N/A

**Audit:**
```bash
dpkg --verify
rpm -Va  # For RPM-based systems
```

**Expected:** No unexpected file permission changes

**Actual:**
```
[Paste command output here]
```

**Evidence:** [Screenshot filename or description]

**Notes:** [Any relevant notes]

---

## Manual Controls (Organizational Policy)

### 1.3.1 Ensure sudo commands use pty (Scored)

**Level:** Level 1 Server
**Status:** [ ] PASS [ ] FAIL [ ] N/A

**Audit:**
```bash
grep -Ei '^\s*Defaults\s+([^#]+,\s*)?use_pty(,\s+\S+\s*)*(\s+#.*)?$' /etc/sudoers /etc/sudoers.d/*
```

**Expected:** Defaults use_pty

**Actual:**
```
[Paste command output here]
```

**Evidence:** [Screenshot filename or description]

**Notes:** [Requires organizational policy decision - impacts all sudo usage]

---

### 5.4.1.4 Ensure inactive password lock is 30 days or less (Scored)

**Level:** Level 1 Server
**Status:** [ ] PASS [ ] FAIL [ ] N/A

**Audit:**
```bash
useradd -D | grep INACTIVE
grep -E '^INACTIVE' /etc/default/useradd
```

**Expected:** INACTIVE=30 (or less)

**Actual:**
```
[Paste command output here]
```

**Evidence:** [Screenshot filename or description]

**Notes:** [Impacts user access - coordinate with user management team]

---

## Validation Summary

**Validation Date:** [YYYY-MM-DD]
**Validation Method:** [Automated (OpenSCAP) / Manual / Hybrid]
**Automated Scan Results:** [Pass: X, Fail: Y, N/A: Z]
**Manual Validation Results:** [Pass: X, Fail: Y, N/A: Z]

**Overall Assessment:**
- Baseline compliance: [88.8%]
- Critical gaps: [3 controls requiring immediate remediation]
- High priority gaps: [8 controls requiring remediation within 1 week]
- Medium priority gaps: [10 controls requiring remediation within 1 month]
- Low priority gaps: [4 controls for next maintenance cycle]

**Recommendations:**
1. [Apply critical remediations immediately (P0 controls)]
2. [Schedule high priority remediations within 1 week (P1 controls)]
3. [Plan medium priority remediations for next maintenance window (P2 controls)]
4. [Address low priority controls in next hardening cycle (P3 controls)]

---

## Appendix A: Not Applicable Controls

**List controls marked N/A with justification:**

- **1.1.5:** Ensure noexec option set on /var/tmp partition - N/A (no separate /var/tmp partition)
- **2.2.3:** Ensure Avahi Server is not installed - N/A (Avahi required for mDNS discovery in this environment)
- **3.3.1:** Ensure source routed packets are not accepted - N/A (this is a virtual machine, host controls routing)

---

## Appendix B: Compensating Controls

**List controls with compensating controls:**

- **5.2.10:** Ensure SSH root login is disabled
  - Current: PermitRootLogin yes
  - Compensating: Root login restricted by SSH key + 2FA + IP whitelist
  - Risk: LOW (compensating controls mitigate risk)

---

**Checklist Version:** 2.0
**Last Updated:** 2025-12-02
**Template:** Compliance checklist for CIS/STIG manual validation
