---
type: template
name: script-templates
category: CATEGORY_NAME
classification: public
version: 1.0
last_updated: 2025-12-02
---

# Benchmark Script Templates

**Platform-specific templates for compliance automation scripts**

---

## Linux (Bash) Template

```bash
#!/bin/bash
# CIS Benchmark Compliance Script
# Framework: [CIS Ubuntu 22.04 LTS Benchmark v1.0.0]
# Level: [Level 1 - Server]

# Configuration
DRY_RUN=false
VERBOSE=false
REPORT_FILE="compliance-report.json"
BACKUP_DIR="/var/backups/compliance"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'  # No Color

# Statistics
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

# Logging
log() {
    local level="$1"
    shift
    local message="$@"
    echo "$(date '+%Y-%m-%d %H:%M:%S') [$level] $message"
}

# Backup configuration
backup_config() {
    local file="$1"
    mkdir -p "$BACKUP_DIR"
    cp -p "$file" "$BACKUP_DIR/$(basename $file).$(date +%Y%m%d_%H%M%S)"
}

# Check Functions (one per control)
check_5_2_1() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    local file="/etc/ssh/sshd_config"
    local owner=$(stat -c '%U' "$file")
    local group=$(stat -c '%G' "$file")
    local perms=$(stat -c '%a' "$file")

    if [[ "$owner" == "root" && "$group" == "root" && "$perms" == "600" ]]; then
        log "INFO" "PASS: 5.2.1 - SSH config permissions"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        log "WARN" "FAIL: 5.2.1 - SSH config permissions (current: $owner:$group $perms)"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

# Remediation Functions
remediate_5_2_1() {
    local file="/etc/ssh/sshd_config"
    log "INFO" "Remediating 5.2.1: SSH config permissions"

    if [ "$DRY_RUN" = true ]; then
        log "INFO" "[DRY-RUN] Would execute: chown root:root $file && chmod 600 $file"
        return 0
    fi

    backup_config "$file"
    chown root:root "$file"
    chmod 600 "$file"

    if check_5_2_1; then
        log "INFO" "SUCCESS: 5.2.1 remediated"
    else
        log "ERROR" "FAILED: 5.2.1 remediation unsuccessful"
        return 1
    fi
}

# Reporting
generate_report() {
    local compliance_score=$(( PASSED_CHECKS * 100 / TOTAL_CHECKS ))

    cat > "$REPORT_FILE" <<EOF
{
  "framework": "CIS Ubuntu 22.04 LTS Benchmark",
  "version": "v1.0.0",
  "scan_date": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "compliance_score": $compliance_score,
  "summary": {
    "total": $TOTAL_CHECKS,
    "passed": $PASSED_CHECKS,
    "failed": $FAILED_CHECKS
  }
}
EOF

    echo -e "${GREEN}Compliance Score: $compliance_score%${NC}"
    echo "Report saved: $REPORT_FILE"
}

# Main execution
main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run) DRY_RUN=true ;;
            --verbose) VERBOSE=true ;;
            --remediate) MODE="remediate" ;;
            *) echo "Unknown option: $1"; exit 1 ;;
        esac
        shift
    done

    log "INFO" "Starting compliance check..."

    # Run all checks
    check_5_2_1
    # ... additional checks ...

    # Run remediations if requested
    if [[ "$MODE" == "remediate" ]]; then
        log "INFO" "Starting remediation..."
        remediate_5_2_1
        # ... additional remediations ...
    fi

    generate_report
}

main "$@"
```

---

## Windows (PowerShell) Template

```powershell
# CIS Benchmark Compliance Script
# Framework: CIS Windows Server 2022 Benchmark v1.0.0
# Level: Level 1 - Member Server

param(
    [switch]$DryRun,
    [switch]$Verbose,
    [switch]$Remediate
)

# Configuration
$ReportFile = "compliance-report.json"
$BackupDir = "C:\ComplianceBackups"

# Statistics
$TotalChecks = 0
$PassedChecks = 0
$FailedChecks = 0

# Logging
function Write-Log {
    param([string]$Level, [string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] [$Level] $Message"
}

# Backup registry key
function Backup-RegistryKey {
    param([string]$Path)

    if (!(Test-Path $BackupDir)) {
        New-Item -Path $BackupDir -ItemType Directory | Out-Null
    }

    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupFile = Join-Path $BackupDir "registry_backup_$timestamp.reg"

    reg export $Path $backupFile /y | Out-Null
}

# Check Functions
function Check-18_9_39_2 {
    $script:TotalChecks++
    $regPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\EventLog\Application"
    $regName = "MaxSize"
    $requiredValue = 32768

    try {
        $currentValue = (Get-ItemProperty -Path $regPath -Name $regName -ErrorAction Stop).$regName

        if ($currentValue -eq $requiredValue) {
            Write-Log "INFO" "PASS: 18.9.39.2 - Application log size"
            $script:PassedChecks++
            return $true
        } else {
            Write-Log "WARN" "FAIL: 18.9.39.2 - Application log size (current: $currentValue, required: $requiredValue)"
            $script:FailedChecks++
            return $false
        }
    } catch {
        Write-Log "WARN" "FAIL: 18.9.39.2 - Registry key not found"
        $script:FailedChecks++
        return $false
    }
}

# Remediation Functions
function Remediate-18_9_39_2 {
    Write-Log "INFO" "Remediating 18.9.39.2: Application log size"

    $regPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\EventLog\Application"
    $regName = "MaxSize"
    $requiredValue = 32768

    if ($DryRun) {
        Write-Log "INFO" "[DRY-RUN] Would set $regPath\$regName to $requiredValue"
        return
    }

    Backup-RegistryKey $regPath

    if (!(Test-Path $regPath)) {
        New-Item -Path $regPath -Force | Out-Null
    }

    Set-ItemProperty -Path $regPath -Name $regName -Value $requiredValue

    if (Check-18_9_39_2) {
        Write-Log "INFO" "SUCCESS: 18.9.39.2 remediated"
    } else {
        Write-Log "ERROR" "FAILED: 18.9.39.2 remediation unsuccessful"
    }
}

# Reporting
function Generate-Report {
    $complianceScore = [math]::Round(($PassedChecks / $TotalChecks) * 100, 1)

    $report = @{
        framework = "CIS Windows Server 2022 Benchmark"
        version = "v1.0.0"
        scan_date = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
        compliance_score = $complianceScore
        summary = @{
            total = $TotalChecks
            passed = $PassedChecks
            failed = $FailedChecks
        }
    }

    $report | ConvertTo-Json -Depth 10 | Out-File $ReportFile

    Write-Host "Compliance Score: $complianceScore%" -ForegroundColor Green
    Write-Host "Report saved: $ReportFile"
}

# Main execution
Write-Log "INFO" "Starting compliance check..."

# Run all checks
Check-18_9_39_2
# ... additional checks ...

# Run remediations if requested
if ($Remediate) {
    Write-Log "INFO" "Starting remediation..."
    Remediate-18_9_39_2
    # ... additional remediations ...
}

Generate-Report
```

---

## Ansible Playbook Template

```yaml
---
# CIS Benchmark Compliance Playbook
# Framework: CIS Ubuntu 22.04 LTS Benchmark v1.0.0
# Level: Level 1 - Server

- name: CIS Ubuntu 22.04 LTS Benchmark - Level 1
  hosts: all
  become: yes
  vars:
    dry_run: false
    report_file: "/tmp/compliance-report.json"

  tasks:
    # 5.2.1 Ensure permissions on /etc/ssh/sshd_config are configured
    - name: Check 5.2.1 - SSH config permissions
      stat:
        path: /etc/ssh/sshd_config
      register: sshd_config_stat

    - name: Assess 5.2.1 compliance
      set_fact:
        check_5_2_1_pass: "{{ sshd_config_stat.stat.pw_name == 'root' and sshd_config_stat.stat.gr_name == 'root' and sshd_config_stat.stat.mode == '0600' }}"

    - name: Remediate 5.2.1 - SSH config ownership
      file:
        path: /etc/ssh/sshd_config
        owner: root
        group: root
      when: not check_5_2_1_pass and not dry_run

    - name: Remediate 5.2.1 - SSH config permissions
      file:
        path: /etc/ssh/sshd_config
        mode: '0600'
      when: not check_5_2_1_pass and not dry_run

    # Generate report
    - name: Generate compliance report
      template:
        src: compliance-report.json.j2
        dest: "{{ report_file }}"
      delegate_to: localhost
```

---

**Version:** 2.0
**Last Updated:** 2025-12-02
**Templates:** Bash (Linux), PowerShell (Windows), Ansible (cross-platform)
