# Compliance Automation - Methodologies

**Core patterns for generating automated compliance scripts from security benchmarks**

---

## Script Generation Pattern

### Three-Phase Script Structure

**Phase 1: VALIDATION (Check Compliance)**
- Read current configuration
- Compare against benchmark requirement
- Return pass/fail status
- No system changes

**Phase 2: REMEDIATION (Apply Fixes)**
- Backup current configuration
- Apply benchmark-compliant settings
- Verify successful application
- Log all changes

**Phase 3: ROLLBACK (Revert Changes)**
- Restore backup configuration
- Verify restoration
- Log rollback actions
- Return to pre-remediation state

### Idempotent Design

**Key Principle:** Script can run multiple times safely without unintended effects

**Implementation:**
```bash
# Check before change
if [ "$current_value" != "$required_value" ]; then
    apply_change
else
    log "Already compliant"
fi
```

**Benefits:**
- Safe re-execution
- No duplicate changes
- Continuous compliance checking

---

## Control Mapping Process

### Step 1: Parse Benchmark Control

**CIS Control Example:**
```
Control ID: 5.2.1
Title: Ensure permissions on /etc/ssh/sshd_config are configured
Level: 1
Description: The /etc/ssh/sshd_config file contains configuration...
Audit: Run the following command and verify Uid and Gid are both 0/root and Access is 600:
    # stat /etc/ssh/sshd_config
Remediation: Run the following commands to set ownership and permissions:
    # chown root:root /etc/ssh/sshd_config
    # chmod 600 /etc/ssh/sshd_config
```

### Step 2: Extract Automation Components

**From Control, Identify:**
1. **Check Command:** `stat /etc/ssh/sshd_config`
2. **Expected Result:** Owner=root, Group=root, Permissions=600
3. **Remediation Command:** `chown root:root` + `chmod 600`
4. **Rollback:** Store original permissions, restore if needed

### Step 3: Generate Script Functions

```bash
# CIS 5.2.1: SSH Config Permissions
check_5_2_1() {
    local file="/etc/ssh/sshd_config"
    local owner=$(stat -c '%U' "$file")
    local group=$(stat -c '%G' "$file")
    local perms=$(stat -c '%a' "$file")

    if [[ "$owner" == "root" && "$group" == "root" && "$perms" == "600" ]]; then
        return 0  # Compliant
    else
        return 1  # Non-compliant
    fi
}

remediate_5_2_1() {
    local file="/etc/ssh/sshd_config"

    # Backup current state
    backup_permissions "$file"

    # Apply fix
    chown root:root "$file"
    chmod 600 "$file"

    # Verify
    if check_5_2_1; then
        log "SUCCESS: CIS 5.2.1 remediated"
    else
        log "FAILED: CIS 5.2.1 remediation unsuccessful"
        rollback_5_2_1
    fi
}

rollback_5_2_1() {
    local file="/etc/ssh/sshd_config"
    restore_permissions "$file"
}
```

---

## Platform-Specific Implementations

### Linux (Bash)

**File Permissions:**
```bash
# Check
stat -c '%U:%G %a' /path/to/file

# Remediate
chown user:group /path/to/file
chmod 644 /path/to/file
```

**Service Configuration:**
```bash
# Check if service enabled
systemctl is-enabled sshd

# Remediate
systemctl enable sshd
systemctl restart sshd
```

**Kernel Parameters:**
```bash
# Check
sysctl net.ipv4.ip_forward

# Remediate (persistent)
echo "net.ipv4.ip_forward = 0" >> /etc/sysctl.conf
sysctl -p
```

---

### Windows (PowerShell)

**Registry Settings:**
```powershell
# Check
Get-ItemProperty -Path "HKLM:\SOFTWARE\Policies\..." -Name "Setting"

# Remediate
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\..." -Name "Setting" -Value 1

# Rollback
Remove-ItemProperty -Path "HKLM:\SOFTWARE\Policies\..." -Name "Setting"
```

**File Permissions:**
```powershell
# Check
Get-Acl C:\Path\To\File | Format-List

# Remediate
$acl = Get-Acl C:\Path\To\File
$acl.SetAccessRuleProtection($true, $false)  # Disable inheritance
Set-Acl C:\Path\To\File $acl
```

**Service Configuration:**
```powershell
# Check
Get-Service -Name "ServiceName" | Select-Object Status, StartType

# Remediate
Set-Service -Name "ServiceName" -StartupType Disabled
Stop-Service -Name "ServiceName"
```

---

### Cloud (AWS CLI)

**S3 Bucket Encryption:**
```bash
# Check
aws s3api get-bucket-encryption --bucket my-bucket

# Remediate
aws s3api put-bucket-encryption --bucket my-bucket \
    --server-side-encryption-configuration '{
        "Rules": [{
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "AES256"
            }
        }]
    }'
```

**IAM Password Policy:**
```bash
# Check
aws iam get-account-password-policy

# Remediate
aws iam update-account-password-policy \
    --minimum-password-length 14 \
    --require-symbols \
    --require-numbers \
    --require-uppercase-characters \
    --require-lowercase-characters
```

---

## Dry-Run Mode Implementation

**Purpose:** Allow validation without making changes (safe testing)

**Implementation Pattern:**
```bash
DRY_RUN=false  # Set via command-line flag

apply_change() {
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY-RUN] Would execute: $1"
    else
        eval "$1"
    fi
}

# Usage
apply_change "chown root:root /etc/ssh/sshd_config"
```

**Benefits:**
- Test script logic without system changes
- Preview remediation actions
- Identify potential issues before execution
- Safe for production validation

---

## Reporting Format

### Compliance Score Calculation

```
Compliance Score = (Passed Controls / Total Controls) × 100%

Example:
- Total Controls: 230
- Passed: 195
- Failed: 35
- Compliance Score: (195 / 230) × 100% = 84.8%
```

### JSON Report Format

```json
{
  "framework": "CIS Ubuntu 22.04 LTS Benchmark",
  "version": "v1.0.0",
  "level": "Level 1 - Server",
  "scan_date": "2025-12-02T10:00:00Z",
  "compliance_score": 84.8,
  "summary": {
    "total": 230,
    "passed": 195,
    "failed": 35,
    "manual": 15
  },
  "findings": [
    {
      "control_id": "5.2.1",
      "title": "Ensure permissions on /etc/ssh/sshd_config are configured",
      "status": "FAIL",
      "severity": "Medium",
      "current_value": "644",
      "expected_value": "600",
      "remediation": "chown root:root /etc/ssh/sshd_config && chmod 600 /etc/ssh/sshd_config"
    }
  ]
}
```

### CSV Report Format

```csv
Control ID,Title,Status,Severity,Current Value,Expected Value,Remediation
5.2.1,Ensure permissions on /etc/ssh/sshd_config are configured,FAIL,Medium,644,600,chmod 600 /etc/ssh/sshd_config
```

---

## Backup and Rollback Strategy

### Configuration Backup

**Before Remediation:**
```bash
backup_config() {
    local file="$1"
    local backup_dir="/var/backups/compliance"
    local timestamp=$(date +%Y%m%d_%H%M%S)

    mkdir -p "$backup_dir"
    cp "$file" "$backup_dir/$(basename $file).$timestamp"

    # Store permissions
    stat -c '%U:%G %a' "$file" > "$backup_dir/$(basename $file).$timestamp.perms"
}
```

### Rollback Execution

```bash
rollback_config() {
    local file="$1"
    local backup_dir="/var/backups/compliance"

    # Find most recent backup
    local latest_backup=$(ls -t "$backup_dir/$(basename $file)."* | grep -v '.perms$' | head -1)

    if [ -f "$latest_backup" ]; then
        cp "$latest_backup" "$file"

        # Restore permissions
        local perms_file="$latest_backup.perms"
        if [ -f "$perms_file" ]; then
            local owner_group=$(cut -d' ' -f1 "$perms_file")
            local permissions=$(cut -d' ' -f2 "$perms_file")

            chown "$owner_group" "$file"
            chmod "$permissions" "$file"
        fi

        log "Rollback successful: $file"
    else
        log "ERROR: No backup found for $file"
    fi
}
```

---

## Error Handling

### Graceful Failure

```bash
safe_execute() {
    local command="$1"
    local error_msg="$2"

    if eval "$command"; then
        return 0
    else
        log "ERROR: $error_msg"
        log "Command failed: $command"
        return 1
    fi
}

# Usage
safe_execute "systemctl restart sshd" "Failed to restart SSH service"
```

### Remediation Verification

```bash
remediate_with_verification() {
    local control_id="$1"

    # Check before remediation
    if check_${control_id}; then
        log "Already compliant: $control_id"
        return 0
    fi

    # Apply remediation
    remediate_${control_id}

    # Verify successful remediation
    if check_${control_id}; then
        log "SUCCESS: $control_id remediated"
        return 0
    else
        log "FAILED: $control_id remediation unsuccessful"
        rollback_${control_id}
        return 1
    fi
}
```

---

## Testing Framework

### Unit Testing Pattern

```bash
test_check_function() {
    # Setup: Create non-compliant configuration
    setup_non_compliant_config

    # Execute: Run check function
    if check_5_2_1; then
        echo "TEST FAILED: Should detect non-compliance"
        return 1
    else
        echo "TEST PASSED: Non-compliance detected"
    fi

    # Cleanup
    teardown_config
}

test_remediate_function() {
    # Setup: Create non-compliant configuration
    setup_non_compliant_config

    # Execute: Run remediation
    remediate_5_2_1

    # Verify: Check now passes
    if check_5_2_1; then
        echo "TEST PASSED: Remediation successful"
    else
        echo "TEST FAILED: Remediation did not fix issue"
        return 1
    fi

    # Cleanup
    teardown_config
}
```

### Integration Testing

```bash
integration_test() {
    echo "Running integration test for $1"

    # Test dry-run mode
    DRY_RUN=true
    run_compliance_script

    # Test actual execution
    DRY_RUN=false
    run_compliance_script

    # Test rollback
    rollback_all_changes

    # Verify rollback successful
    verify_original_state
}
```

---

**Version:** 2.0
**Last Updated:** 2025-12-02
**Purpose:** Core patterns for compliance automation script generation
