---
type: workflow
name: secure-config-validation
classification: public
version: 1.0
last_updated: 2025-12-02
---

# Secure Configuration Validation Workflow

**Complete 3-phase workflow for infrastructure hardening validation**

---

## Workflow Overview

**Total Duration:** 4-8 hours (depending on system complexity and control count)

**Phases:**
1. **EXPLORE:** Baseline Assessment (1-2 hours)
2. **PLAN:** Compliance Validation (2-3 hours)
3. **CODE/COMMIT:** Remediation Generation + Documentation (1-3 hours)

---

## Phase 1: EXPLORE - Baseline Assessment

**Duration:** 1-2 hours

**Goal:** Understand system type, environment, and applicable security standards

### Step 1.1: Identify System Type and Environment

**System Specifications:**
- Platform: Linux (Ubuntu/RHEL/Debian) | Windows Server | Cloud (AWS/Azure/GCP) | Containers (Docker/Kubernetes)
- Version: Exact version (Ubuntu 22.04 LTS, Windows Server 2022, AWS Account, Kubernetes 1.28)
- Services: Installed applications (SSH, Apache, nginx, IIS, MySQL, PostgreSQL)
- Role: Web server, database server, domain controller, container host

**Environment Classification:**
- **Development:** Looser security, developer access, frequent changes
- **Staging:** Production-like, testing ground, tighter security
- **Production:** Strictest security, change control, audit requirements

### Step 1.2: Select Applicable Benchmark

**CIS Benchmark Selection:**
```
Platform: Ubuntu 22.04 LTS
Benchmark: CIS Ubuntu Linux 22.04 LTS Benchmark v1.0.0
Level: Level 1 - Server (essential baseline, 230 controls)
Profile: Server (not Workstation)
```

**DISA STIG Selection:**
```
Platform: Red Hat Enterprise Linux 8
STIG: Red Hat Enterprise Linux 8 STIG Version 1 Release 12 (V1R12)
Categories: Cat I (critical) + Cat II (medium) + Cat III (low)
Total Controls: 250+ findings
```

**Custom Requirements:**
- Compliance mandates: PCI DSS, HIPAA, SOC 2, ISO 27001
- Organization policies: Password complexity, MFA requirements, logging retention
- Industry standards: NIST SP 800-53, CIS Controls v8

### Step 1.3: Document Baseline State

**Configuration Collection:**

**Linux:**
```bash
# System information
uname -a > baseline/system-info.txt
cat /etc/os-release >> baseline/system-info.txt

# Installed packages
dpkg -l > baseline/installed-packages.txt  # Debian/Ubuntu
rpm -qa > baseline/installed-packages.txt  # RHEL/CentOS

# Running services
systemctl list-units --type=service --state=running > baseline/services.txt

# Network configuration
ip addr show > baseline/network-config.txt
iptables -L -n -v > baseline/firewall-rules.txt

# User accounts
cat /etc/passwd > baseline/users.txt
cat /etc/group > baseline/groups.txt

# Key configuration files
cp /etc/ssh/sshd_config baseline/
cp /etc/pam.d/common-password baseline/
cp /etc/login.defs baseline/
```

**Windows:**
```powershell
# System information
Get-ComputerInfo | Out-File baseline\system-info.txt

# Installed software
Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | Out-File baseline\installed-software.txt

# Running services
Get-Service | Where-Object {$_.Status -eq "Running"} | Out-File baseline\services.txt

# Network configuration
Get-NetIPConfiguration | Out-File baseline\network-config.txt
Get-NetFirewallRule | Out-File baseline\firewall-rules.txt

# User accounts
Get-LocalUser | Out-File baseline\users.txt
Get-LocalGroup | Out-File baseline\groups.txt

# Security policies
secedit /export /cfg baseline\security-policy.inf
```

**AWS:**
```bash
# S3 bucket encryption
aws s3api list-buckets --query 'Buckets[*].Name' --output text | \
while read bucket; do
  aws s3api get-bucket-encryption --bucket $bucket 2>/dev/null || echo "$bucket: No encryption"
done > baseline/s3-encryption.txt

# Security groups
aws ec2 describe-security-groups --output json > baseline/security-groups.json

# IAM password policy
aws iam get-account-password-policy > baseline/iam-password-policy.json

# CloudTrail status
aws cloudtrail describe-trails > baseline/cloudtrail.json
```

**Checkpoint:** Update session file with:
- Phase completion status + timestamp
- System type and environment documented
- Baseline standard selected (CIS Level 1/2 or STIG Cat I/II/III)
- Files created (baseline assessment directory)
- Next action: Begin compliance validation

**Load for this phase:**
```
Read skills/secure-config/reference/standards.md
# Focus on: Benchmark selection (CIS, STIG), platform coverage, control structure
```

---

## Phase 2: PLAN - Compliance Validation

**Duration:** 2-3 hours

**Goal:** Validate controls against CIS/STIG requirements and identify gaps

### Step 2.1: Run Automated Compliance Scans (if available)

**OpenSCAP (Linux):**
```bash
# Download CIS benchmark content
wget https://security-benchmarks.s3.amazonaws.com/cis-ubuntu-22.04-benchmark.xml

# Run scan
oscap xccdf eval \
  --profile xccdf_org.cisecurity.benchmarks_profile_Level_1_-_Server \
  --results results.xml \
  --report report.html \
  cis-ubuntu-22.04-benchmark.xml

# Generate report
oscap xccdf generate report results.xml > compliance-report.html

# Parse failed controls
grep "result=\"fail\"" results.xml | sed 's/.*idref=\"\(.*\)\" role.*/\1/' > failed-controls.txt
```

**AWS Security Hub:**
```bash
# Enable CIS AWS Foundations Benchmark
aws securityhub batch-enable-standards \
  --standards-subscription-requests \
  StandardsArn="arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0"

# Get failed findings
aws securityhub get-findings \
  --filters '{"ComplianceStatus":[{"Value":"FAILED","Comparison":"EQUALS"}]}' \
  --query 'Findings[*].[Title,Severity.Label,Compliance.Status,Resources[0].Id]' \
  --output table > findings/aws-security-hub-findings.txt
```

**Docker Bench (Containers):**
```bash
# Run CIS Docker Benchmark
docker run --rm --net host --pid host --cap-add audit_control \
  -v /var/lib:/var/lib \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /etc:/etc:ro \
  docker/docker-bench-security > findings/docker-bench-results.txt
```

### Step 2.2: Manual Control Validation

**For controls not covered by automated scans:**

**Create Validation Checklist:**
```markdown
# CIS Ubuntu 22.04 Level 1 - Manual Validation

## 1. Initial Setup

### 1.1.1 Ensure mounting of cramfs filesystems is disabled (Automated) ✅
**Status:** PASS
**Audit:** `lsmod | grep cramfs` (no output = disabled)
**Evidence:** [Screenshot or command output]

### 1.1.2 Ensure mounting of squashfs filesystems is disabled (Automated) ✅
**Status:** PASS
**Audit:** `lsmod | grep squashfs` (no output = disabled)
**Evidence:** [Screenshot or command output]

### 5.2.1 Ensure permissions on /etc/ssh/sshd_config are configured (Automated) ❌
**Status:** FAIL
**Expected:** root:root 600
**Actual:** root:ssh 644
**Evidence:**
```
$ stat /etc/ssh/sshd_config
Access: (0644/-rw-r--r--) Uid: (0/root) Gid: (113/ssh)
```
**Impact:** High - SSH configuration readable by ssh group
**Priority:** P1 (High)
```

### Step 2.3: Calculate Compliance Percentage

**Compliance Calculation:**
```
Total Controls: 230 (CIS Ubuntu 22.04 Level 1)
Passed: 198
Failed: 25
Not Applicable: 7

Applicable Controls: 230 - 7 = 223
Compliance %: (198 / 223) * 100 = 88.8%
```

**Compliance by Severity:**
```
Critical Gaps: 3 controls (immediate remediation)
High Priority: 8 controls (remediate within 1 week)
Medium Priority: 10 controls (remediate within 1 month)
Low Priority: 4 controls (remediate next cycle)
```

### Step 2.4: Document Non-Compliant Findings

**Finding Template (Markdown):**
```markdown
# CIS-001: SSH Config Permissions Incorrect

**Control ID:** CIS 5.2.1
**Title:** Ensure permissions on /etc/ssh/sshd_config are configured
**Level:** Level 1 - Server
**Status:** FAIL
**Severity:** High

## Current State
- **Owner:** root:ssh
- **Permissions:** 644 (rw-r--r--)

## Required State
- **Owner:** root:root
- **Permissions:** 600 (rw-------)

## Impact
SSH configuration file is readable by non-root users, potentially exposing
sensitive configuration details (allowed ciphers, authentication methods).

## Evidence
```
$ stat /etc/ssh/sshd_config
Access: (0644/-rw-r--r--) Uid: (0/root) Gid: (113/ssh)
```

## Remediation
```bash
chown root:root /etc/ssh/sshd_config
chmod 600 /etc/ssh/sshd_config
systemctl restart sshd
```

## Rollback
```bash
# Restore from backup
cp /etc/ssh/sshd_config.backup /etc/ssh/sshd_config
systemctl restart sshd
```

## Validation
```bash
stat /etc/ssh/sshd_config
# Expected: Access: (0600/-rw-------) Uid: (0/root) Gid: (0/root)
```

## References
- CIS Ubuntu 22.04 Benchmark v1.0.0, Section 5.2.1
- NIST SP 800-53 Rev. 5: AC-3 (Access Enforcement)
```

**Checkpoint:** Update session file with:
- Phase completion status + timestamp
- Compliance validation completed (88.8% compliant)
- Non-compliant settings identified (25 failed controls)
- Files created (compliance report, findings documents)
- Next action: Generate remediation guidance

**Load for this phase:**
```
Read skills/secure-config/methodologies/configuration-hardening.md
# Focus on: Control validation methodology, gap analysis, risk prioritization
```

---

## Phase 3: CODE/COMMIT - Remediation Generation + Documentation

**Duration:** 1-3 hours

**Goal:** Generate remediation scripts, rollback procedures, and final documentation

### Step 3.1: Prioritize Remediations

**Risk-Based Priority Matrix:**

| Priority | Criteria | Controls | Timeline |
|----------|----------|----------|----------|
| **P0 (Critical)** | Remote exploitation without auth | 3 | Immediate |
| **P1 (High)** | Remote exploitation with auth | 8 | 1 week |
| **P2 (Medium)** | Local exploitation / Info disclosure | 10 | 1 month |
| **P3 (Low)** | Best practice deviations | 4 | Next cycle |

**Environment-Specific Adjustments:**
- **Production:** Apply P0 + P1 immediately, P2 within 30 days
- **Staging:** Test all remediations before production
- **Development:** Apply P0 only, defer P1-P3 based on risk tolerance

### Step 3.2: Generate Remediation Scripts

**Bash Script (Linux):**
```bash
#!/bin/bash
# CIS Ubuntu 22.04 Level 1 - Remediation Script
# Generated: 2025-12-02
# Controls: P0 (Critical) + P1 (High) = 11 controls

set -e  # Exit on error

BACKUP_DIR="/var/backups/compliance/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "=== CIS Ubuntu 22.04 Level 1 Remediation ==="
echo "Backup directory: $BACKUP_DIR"
echo

# CIS 5.2.1 - SSH Config Permissions
echo "[1/11] Remediating CIS 5.2.1: SSH config permissions..."
cp /etc/ssh/sshd_config "$BACKUP_DIR/sshd_config.backup"
chown root:root /etc/ssh/sshd_config
chmod 600 /etc/ssh/sshd_config
echo "✓ CIS 5.2.1 complete"

# CIS 5.2.4 - SSH X11 Forwarding
echo "[2/11] Remediating CIS 5.2.4: Disable SSH X11 forwarding..."
sed -i 's/^X11Forwarding yes/X11Forwarding no/' /etc/ssh/sshd_config
echo "✓ CIS 5.2.4 complete"

# ... additional remediations ...

# Restart services
echo
echo "Restarting services..."
systemctl restart sshd
echo "✓ SSH service restarted"

echo
echo "=== Remediation Complete ==="
echo "Backups saved to: $BACKUP_DIR"
echo "Run validation script to verify fixes."
```

**PowerShell Script (Windows):**
```powershell
# CIS Windows Server 2022 Level 1 - Remediation Script
# Generated: 2025-12-02
# Controls: P0 (Critical) + P1 (High) = 15 controls

$BackupDir = "C:\ComplianceBackups\$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -Path $BackupDir -ItemType Directory -Force | Out-Null

Write-Host "=== CIS Windows Server 2022 Level 1 Remediation ===" -ForegroundColor Green
Write-Host "Backup directory: $BackupDir"
Write-Host

# CIS 18.9.39.2 - Application Log Size
Write-Host "[1/15] Remediating CIS 18.9.39.2: Application log size..." -ForegroundColor Yellow
$regPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\EventLog\Application"
reg export "HKLM\SOFTWARE\Policies\Microsoft\Windows\EventLog" "$BackupDir\eventlog.reg" /y | Out-Null
if (!(Test-Path $regPath)) {
    New-Item -Path $regPath -Force | Out-Null
}
Set-ItemProperty -Path $regPath -Name "MaxSize" -Value 32768
Write-Host "✓ CIS 18.9.39.2 complete" -ForegroundColor Green

# ... additional remediations ...

Write-Host
Write-Host "=== Remediation Complete ===" -ForegroundColor Green
Write-Host "Backups saved to: $BackupDir"
Write-Host "Run validation script to verify fixes."
```

### Step 3.3: Create Rollback Procedures

**Rollback Script (Bash):**
```bash
#!/bin/bash
# Rollback Script for CIS Ubuntu 22.04 Level 1 Remediation
# Usage: ./rollback.sh /var/backups/compliance/20250102_143000

BACKUP_DIR="$1"

if [ -z "$BACKUP_DIR" ] || [ ! -d "$BACKUP_DIR" ]; then
    echo "Error: Backup directory not found"
    echo "Usage: $0 <backup_directory>"
    exit 1
fi

echo "=== Rollback from $BACKUP_DIR ==="
echo

# Restore SSH config
if [ -f "$BACKUP_DIR/sshd_config.backup" ]; then
    echo "Restoring /etc/ssh/sshd_config..."
    cp "$BACKUP_DIR/sshd_config.backup" /etc/ssh/sshd_config
    systemctl restart sshd
    echo "✓ SSH config restored"
fi

# ... additional rollbacks ...

echo
echo "=== Rollback Complete ==="
echo "System restored to pre-remediation state"
```

### Step 3.4: Create Validation Checklist

**Post-Remediation Validation:**
```markdown
# CIS Ubuntu 22.04 Level 1 - Post-Remediation Validation

## Instructions
1. Run this checklist after applying remediation script
2. Verify each control manually
3. Document any remaining failures
4. Re-run automated scan for full compliance check

## Critical Controls (P0)

### CIS 5.2.1 - SSH Config Permissions
```bash
$ stat /etc/ssh/sshd_config
Expected: Access: (0600/-rw-------) Uid: (0/root) Gid: (0/root)
```
**Status:** [ ] PASS [ ] FAIL

### CIS 5.2.4 - SSH X11 Forwarding Disabled
```bash
$ grep "^X11Forwarding" /etc/ssh/sshd_config
Expected: X11Forwarding no
```
**Status:** [ ] PASS [ ] FAIL

## High Priority Controls (P1)

### CIS 5.3.1 - Password Creation Requirements
```bash
$ grep pam_pwquality /etc/pam.d/common-password
Expected: minlen=14, dcredit=-1, ucredit=-1, ocredit=-1, lcredit=-1
```
**Status:** [ ] PASS [ ] FAIL

## Service Functionality Verification

### SSH Access
```bash
$ ssh user@localhost
Expected: Successful authentication
```
**Status:** [ ] PASS [ ] FAIL

### Web Server (if applicable)
```bash
$ curl -I http://localhost
Expected: HTTP 200 OK
```
**Status:** [ ] PASS [ ] FAIL

## Compliance Re-Scan

```bash
# Re-run OpenSCAP scan
oscap xccdf eval --profile Level_1_Server \
  --results post-remediation-results.xml \
  --report post-remediation-report.html \
  cis-ubuntu-22.04-benchmark.xml

# Compare results
echo "Before: $(grep 'result=\"fail\"' results.xml | wc -l) failures"
echo "After: $(grep 'result=\"fail\"' post-remediation-results.xml | wc -l) failures"
```

**Expected Outcome:**
- Before: 25 failures
- After: ≤5 failures (some controls may require manual remediation)
- Compliance improvement: 88.8% → 97.8%
```

### Step 3.5: Create Final Documentation

**README.md:**
```markdown
# CIS Ubuntu 22.04 Level 1 Hardening - [Client Name]

**Date:** 2025-12-02
**Baseline:** CIS Ubuntu Linux 22.04 LTS Benchmark v1.0.0
**Environment:** Production
**Initial Compliance:** 88.8% (198/223 controls)
**Target Compliance:** 98% (218/223 controls)

## Directory Structure

```
secure-configs/example-client-2025-01/
├── README.md (this file)
├── baseline/ (initial configuration)
├── findings/ (non-compliant controls)
├── scripts/ (remediation + rollback)
├── validation/ (post-remediation checks)
└── reports/ (compliance reports)
```

## Remediation Summary

### Phase 1: Critical (P0) - 3 controls
- Applied: 2025-01-05
- Status: Complete
- Compliance: 88.8% → 90.1%

### Phase 2: High (P1) - 8 controls
- Applied: 2025-01-12
- Status: Complete
- Compliance: 90.1% → 93.7%

### Phase 3: Medium (P2) - 10 controls
- Scheduled: 2025-02-15
- Status: Pending
- Expected: 93.7% → 98.2%

## Manual Controls (Cannot Automate)

- 1.3.1: Ensure sudo commands use pty (organizational policy)
- 1.5.3: Ensure authentication required for single user mode (requires reboot)
- 5.4.1.4: Ensure inactive password lock is 30 days or less (user impact assessment)

## Usage

### Apply Remediation
```bash
sudo ./scripts/remediate-p0-p1.sh
```

### Rollback (if needed)
```bash
sudo ./scripts/rollback.sh /var/backups/compliance/20250105_140000
```

### Validate
```bash
./scripts/validate-post-remediation.sh
```

## Next Steps

1. Apply Phase 3 remediations (2025-02-15)
2. Schedule quarterly compliance re-scans
3. Update baseline for future comparisons
```

**Checkpoint:** Update session file with:
- Phase completion status + timestamp
- Remediation scripts generated (with rollback procedures)
- Validation checklist created
- Files created (remediation scripts, rollback script, validation checklist, README)
- Next action: N/A - secure config complete

**Load for this phase:**
```
Read skills/secure-config/templates/remediation-script-template.md
# Focus on: Script structure, rollback procedures, validation checklist
```

---

## Deliverables Checklist

**Phase 1: Baseline Assessment**
- ✅ System type and environment documented
- ✅ Applicable CIS Benchmark or DISA STIG selected
- ✅ Baseline configuration collected
- ✅ Compliance requirements documented

**Phase 2: Compliance Validation**
- ✅ Automated scans completed (OpenSCAP, AWS Security Hub, Docker Bench)
- ✅ Manual control validation performed
- ✅ Compliance percentage calculated
- ✅ Non-compliant findings documented with evidence

**Phase 3: Remediation Generation**
- ✅ Remediation priorities established (P0/P1/P2/P3)
- ✅ Remediation scripts generated (Bash, PowerShell, Ansible)
- ✅ Rollback procedures created
- ✅ Validation checklist created
- ✅ Final documentation (README, usage guide)

---

**Version:** 2.0
**Last Updated:** 2025-12-02
**Workflow:** EXPLORE (Baseline Assessment) → PLAN (Compliance Validation) → CODE/COMMIT (Remediation + Documentation)
**Duration:** 4-8 hours (standard system hardening)
