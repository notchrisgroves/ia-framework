# Configuration Hardening Methodology

**Manual validation and remediation planning for infrastructure hardening**

---

## Control Validation Methodology

### 1. Baseline Selection

**CIS Benchmark Selection:**
- Identify exact platform and version (Ubuntu 22.04, Windows Server 2022, AWS Foundation)
- Select applicable benchmark version (CIS Ubuntu 22.04 v1.0.0)
- Determine level: Level 1 (essential, minimal disruption) or Level 2 (defense-in-depth)
- Review profile applicability (Server, Workstation, Cloud)

**DISA STIG Selection:**
- Identify system type (RHEL 8, Windows Server 2019, Oracle Database)
- Select applicable STIG and version (RHEL 8 STIG V1R12)
- Determine category focus: Cat I (critical), Cat II (medium), Cat III (low)
- Review DoD-specific requirements (CAC authentication, FIPS 140-2)

**Custom Baseline Creation:**
- Start with CIS or STIG as foundation
- Add organization-specific controls
- Document deviations from standard
- Maintain traceability to parent standard

### 2. Configuration Collection

**File-Based Collection:**
```bash
# Linux
cat /etc/ssh/sshd_config
cat /etc/pam.d/common-password
sysctl -a
iptables -L -n -v

# Windows
Get-ItemProperty "HKLM:\SOFTWARE\Policies\Microsoft\Windows\*"
Get-Service
Get-NetFirewallRule
```

**API-Based Collection:**
```bash
# AWS
aws s3api get-bucket-encryption --bucket example-bucket
aws ec2 describe-security-groups
aws iam get-account-password-policy

# Azure
az storage account show --name exampleaccount
az network nsg rule list --resource-group example-rg --nsg-name example-nsg
```

**Automated Scanning Tools:**
- OpenSCAP (Linux CIS/STIG scanning)
- Lynis (Linux security auditing)
- AWS Security Hub (CIS AWS Foundations)
- Microsoft Security Compliance Toolkit (Windows)
- Docker Bench (CIS Docker Benchmark)
- kube-bench (CIS Kubernetes Benchmark)

### 3. Control-by-Control Validation

**For Each Control:**

1. **Read Control Requirement**
   - Control ID (CIS 5.2.1, STIG V-230221)
   - Profile level (CIS L1/L2, STIG Cat I/II/III)
   - Description and rationale
   - Audit procedure (how to check)
   - Remediation procedure (how to fix)

2. **Execute Audit Command**
   - Run prescribed audit command from benchmark
   - Document actual configuration value
   - Compare against required value
   - Determine compliance status (Pass/Fail/Not Applicable)

3. **Document Finding**
   ```markdown
   **Control:** CIS 5.2.1 - Ensure permissions on /etc/ssh/sshd_config are configured
   **Level:** Level 1 Server
   **Status:** FAIL
   **Expected:** root:root 600
   **Actual:** root:ssh 644
   **Impact:** High - SSH configuration readable by non-root users
   **Remediation:** chown root:root /etc/ssh/sshd_config && chmod 600 /etc/ssh/sshd_config
   ```

4. **Assess Risk**
   - Exploitability (Can this be exploited remotely? With credentials?)
   - Impact (Confidentiality/Integrity/Availability)
   - Environment context (Production vs Development)
   - Compensating controls (Is risk mitigated elsewhere?)

---

## Compliance Checking Process

### Automated Scanning

**OpenSCAP (Linux):**
```bash
# Download CIS/STIG content
wget https://security-benchmarks.s3.amazonaws.com/cis-ubuntu-22.04-benchmark.xml

# Run scan
oscap xccdf eval --profile xccdf_org.cisecurity.benchmarks_profile_Level_1_Server \
  --results results.xml --report report.html cis-ubuntu-22.04-benchmark.xml

# Parse results
oscap xccdf generate report results.xml > compliance-report.html
```

**AWS Security Hub:**
```bash
# Enable CIS AWS Foundations Benchmark
aws securityhub batch-enable-standards \
  --standards-subscription-requests StandardsArn="arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0"

# Get findings
aws securityhub get-findings \
  --filters '{"ComplianceStatus":[{"Value":"FAILED","Comparison":"EQUALS"}]}' \
  --query 'Findings[*].[Title,Severity.Label,Compliance.Status]' \
  --output table
```

**Docker Bench:**
```bash
# Run CIS Docker Benchmark
docker run --rm --net host --pid host --cap-add audit_control \
  -v /var/lib:/var/lib -v /var/run/docker.sock:/var/run/docker.sock \
  -v /etc:/etc:ro docker/docker-bench-security

# Review output (Pass/Warn/Info/Note)
```

### Manual Validation

**When Automated Tools Cannot Check:**
- Organizational policies (password rotation frequency)
- Physical security controls (server room access)
- Complex architectural decisions (network segmentation design)
- Human processes (incident response procedures)

**Manual Validation Process:**
1. Review control requirement
2. Interview system administrators
3. Review documentation and policies
4. Inspect configurations manually
5. Document evidence (screenshots, command outputs, policy excerpts)
6. Determine compliance status with justification

---

## Remediation Planning

### Risk Prioritization

**Severity Matrix:**

| Category | Criteria | Example | Priority |
|----------|----------|---------|----------|
| **Critical** | Remote exploitation without authentication | Telnet enabled | P0 (Immediate) |
| **High** | Remote exploitation with low-privilege credentials | Weak SSH ciphers | P1 (1 week) |
| **Medium** | Local exploitation or information disclosure | Audit logging disabled | P2 (1 month) |
| **Low** | Best practice deviations, limited impact | Banner not configured | P3 (Next cycle) |

**CIS Level Prioritization:**
- **CIS Level 1:** Essential baseline, prioritize all findings
- **CIS Level 2:** Defense-in-depth, may defer based on risk

**STIG Category Prioritization:**
- **Cat I:** Critical, must remediate immediately
- **Cat II:** Medium, remediate within 30 days
- **Cat III:** Low, remediate within 90 days

### Environment-Specific Baselines

**Development Environment:**
- Apply CIS Level 1 controls (essential security)
- Skip controls that break development workflows (strict password policies, restrictive sudo)
- Allow looser logging retention (7 days vs 90 days)
- Permit local root access for troubleshooting

**Staging Environment:**
- Apply CIS Level 1 + selective Level 2 controls
- Mirror production security posture
- Test remediation scripts before production deployment
- Validate no service disruption

**Production Environment:**
- Apply full CIS Level 1 + Level 2 (or Level 1 + risk assessment)
- Implement all Cat I + Cat II STIG controls
- Require change approval for configuration changes
- Maintain strict audit logging (90+ days retention)

### Remediation Script Generation

**Bash (Linux):**
```bash
#!/bin/bash
# CIS 5.2.1 - SSH Config Permissions

# Backup
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup.$(date +%Y%m%d_%H%M%S)

# Remediate
chown root:root /etc/ssh/sshd_config
chmod 600 /etc/ssh/sshd_config

# Validate
echo "Verifying fix..."
stat -c '%U:%G %a' /etc/ssh/sshd_config

# Expected output: root:root 600
```

**PowerShell (Windows):**
```powershell
# CIS 18.9.39.2 - Application Log Size

# Backup registry
$backupPath = "C:\Backups\registry_$(Get-Date -Format 'yyyyMMdd_HHmmss').reg"
reg export "HKLM\SOFTWARE\Policies\Microsoft\Windows\EventLog" $backupPath /y

# Remediate
$regPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\EventLog\Application"
if (!(Test-Path $regPath)) {
    New-Item -Path $regPath -Force | Out-Null
}
Set-ItemProperty -Path $regPath -Name "MaxSize" -Value 32768

# Validate
Get-ItemProperty -Path $regPath -Name "MaxSize"

# Expected output: MaxSize : 32768
```

**Ansible (Multi-System):**
```yaml
---
- name: CIS 5.2.1 - SSH Config Permissions
  hosts: linux_servers
  become: yes
  tasks:
    - name: Backup SSH config
      copy:
        src: /etc/ssh/sshd_config
        dest: "/etc/ssh/sshd_config.backup.{{ ansible_date_time.iso8601_basic_short }}"
        remote_src: yes

    - name: Set SSH config ownership
      file:
        path: /etc/ssh/sshd_config
        owner: root
        group: root
        mode: '0600'

    - name: Validate SSH config permissions
      stat:
        path: /etc/ssh/sshd_config
      register: sshd_stat

    - name: Assert correct permissions
      assert:
        that:
          - sshd_stat.stat.pw_name == "root"
          - sshd_stat.stat.gr_name == "root"
          - sshd_stat.stat.mode == "0600"
```

---

## Rollback Procedures

### Rollback Strategy

**Every remediation MUST include rollback procedure**

**File-Based Rollback:**
```bash
# Restore backed-up file
cp /etc/ssh/sshd_config.backup.20250101_120000 /etc/ssh/sshd_config

# Restart service
systemctl restart sshd

# Verify service operational
systemctl status sshd
```

**Registry-Based Rollback (Windows):**
```powershell
# Restore registry from backup
reg import C:\Backups\registry_20250101_120000.reg

# Restart service if needed
Restart-Service EventLog
```

**Ansible Rollback:**
```yaml
---
- name: Rollback SSH Config
  hosts: linux_servers
  become: yes
  tasks:
    - name: Find latest backup
      find:
        paths: /etc/ssh
        patterns: "sshd_config.backup.*"
      register: backups

    - name: Restore latest backup
      copy:
        src: "{{ (backups.files | sort(attribute='mtime') | last).path }}"
        dest: /etc/ssh/sshd_config
        remote_src: yes

    - name: Restart SSH service
      service:
        name: sshd
        state: restarted
```

### Testing Rollback Procedures

**Pre-Production Testing:**
1. Apply remediation on non-production system
2. Verify configuration change
3. Execute rollback procedure
4. Verify system returns to original state
5. Confirm no service disruption

**Production Rollback Plan:**
1. Document current configuration state (pre-change baseline)
2. Schedule change during maintenance window
3. Apply remediation
4. Monitor for 15-30 minutes
5. If issues detected, execute rollback immediately
6. Document outcome (success or rollback reason)

---

## Gap Analysis Methodology

### Compliance Percentage Calculation

```
Compliance % = (Controls Passed / Total Applicable Controls) * 100
```

**Example:**
- Total controls: 230 (CIS Ubuntu 22.04 Level 1)
- Passed: 198
- Failed: 25
- Not Applicable: 7
- Compliance: (198 / (230-7)) * 100 = 88.8%

### Gap Categorization

**By Control Domain:**
- Access Control (15 failed controls)
- Audit & Logging (5 failed controls)
- Network Configuration (3 failed controls)
- File Permissions (2 failed controls)

**By Severity:**
- Critical: 3 controls (immediate remediation required)
- High: 8 controls (remediate within 1 week)
- Medium: 10 controls (remediate within 1 month)
- Low: 4 controls (remediate next cycle)

**By Remediation Effort:**
- Quick wins (< 1 hour): 12 controls
- Moderate (1-4 hours): 8 controls
- Complex (> 4 hours): 5 controls

### Compliance Roadmap

**Phase 1: Critical Fixes (Week 1)**
- Remediate all Cat I / Critical findings
- Focus on remote exploitation risks
- Test and validate in production

**Phase 2: High Priority (Weeks 2-4)**
- Remediate all Cat II / High findings
- Focus on authentication and access control
- Implement automated compliance monitoring

**Phase 3: Medium Priority (Months 2-3)**
- Remediate Cat III / Medium findings
- Focus on audit logging and monitoring
- Harden additional services

**Phase 4: Continuous Improvement (Ongoing)**
- Address low priority findings
- Regular compliance re-scans (monthly/quarterly)
- Update baselines for new CIS/STIG releases

---

## Validation & Verification

### Post-Remediation Validation

**Re-Run Automated Scans:**
```bash
# Re-scan with OpenSCAP
oscap xccdf eval --profile Level_1_Server \
  --results post-remediation-results.xml \
  --report post-remediation-report.html \
  cis-ubuntu-22.04-benchmark.xml

# Compare before/after
diff <(grep "result=\"fail\"" results.xml | wc -l) \
     <(grep "result=\"fail\"" post-remediation-results.xml | wc -l)
```

**Manual Spot Checks:**
- Verify high-risk controls manually
- Test service functionality (SSH login, web server access)
- Review logs for errors
- Confirm no unintended configuration changes

### Compliance Reporting

**Executive Summary:**
- Overall compliance percentage (before/after)
- Critical findings remediated
- Residual risks and exceptions
- Next steps and recommendations

**Technical Findings:**
- Control-by-control validation results
- Evidence for each finding (command outputs, screenshots)
- Remediation scripts provided
- Rollback procedures documented

**Compliance Dashboard:**
```
┌─────────────────────────────────────┐
│  CIS Ubuntu 22.04 L1 Compliance     │
├─────────────────────────────────────┤
│  Overall: 88.8% (198/223 controls)  │
│  Critical Gaps: 3                   │
│  High Priority: 8                   │
│  Medium Priority: 10                │
│  Low Priority: 4                    │
└─────────────────────────────────────┘

Top Gaps by Domain:
- Access Control: 15 controls
- Audit & Logging: 5 controls
- Network Config: 3 controls
- File Permissions: 2 controls
```

---

**Version:** 2.0
**Last Updated:** 2025-12-02
**Methodology:** Control validation, compliance checking, remediation planning, rollback procedures, gap analysis
