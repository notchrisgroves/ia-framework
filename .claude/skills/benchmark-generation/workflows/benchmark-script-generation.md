---
type: workflow
name: benchmark-script-generation
classification: public
version: 1.0
last_updated: 2025-12-02
---

# Benchmark Script Generation Workflow

**Complete 4-phase workflow for compliance automation script creation**

---

## Workflow Overview

**Total Duration:** 4-6 hours (depending on benchmark complexity)

**Phases:**
1. **EXPLORE:** Requirements Analysis (1 hour)
2. **PLAN:** Control Mapping (1-2 hours)
3. **CODE:** Script Generation (1-2 hours)
4. **COMMIT:** Testing & Documentation (1 hour)

---

## Phase 1: EXPLORE - Requirements Analysis

**Duration:** 1 hour

**Goal:** Understand compliance framework, platform, and automation scope

### Step 1.1: Identify Compliance Framework

**Questions:**
- Which framework? (CIS, DISA STIG, PCI DSS, HIPAA, NIST SP 800-53)
- Which version? (CIS Ubuntu 22.04 v1.0.0, DISA RHEL 8 STIG V1R12, PCI DSS v4.0)
- Which level/category? (CIS L1/L2, STIG CAT I/II/III, PCI Scope)

### Step 1.2: Determine Target Platform

**Platform Specifications:**
- Operating System: Linux (Ubuntu/RHEL/Debian) or Windows Server
- Version: Specific version number (Ubuntu 22.04, Windows Server 2022)
- Services: Installed services (SSH, Apache, nginx, IIS, SQL Server)
- Cloud Provider: AWS, Azure, GCP (if applicable)

### Step 1.3: Define Automation Scope

**Scope Questions:**
- **Full Baseline:** All controls (230+ for CIS Level 1)
- **Targeted Controls:** Specific sections (SSH, users, file permissions)
- **Validation Only:** Check compliance without remediation
- **Full Automation:** Check + remediate + rollback

### Step 1.4: Select Script Format

**Format Options:**
- **Bash:** Linux/Unix systems
- **PowerShell:** Windows systems
- **Python:** Cross-platform, complex logic
- **Ansible:** Configuration management integration

**Checkpoint:** Update session file with requirements documented

---

## Phase 2: PLAN - Control Mapping

**Duration:** 1-2 hours

**Goal:** Map benchmark controls to platform-specific checks

### Step 2.1: Parse Benchmark Document

**Extract for EACH control:**
- Control ID (CIS 5.2.1, STIG V-230221)
- Title and description
- Audit commands (how to check compliance)
- Remediation commands (how to fix non-compliance)
- Severity/Level (CIS L1/L2, STIG CAT I/II/III)

### Step 2.2: Identify Automated vs Manual Controls

**Automated (Script-able):**
- File permissions: `chmod`, `chown`
- Service status: `systemctl`, `Get-Service`
- Kernel parameters: `sysctl`
- Registry settings: `Set-ItemProperty`

**Manual (Documentation Only):**
- Physical security controls
- Organizational policies
- Complex architectural decisions
- Human review required

### Step 2.3: Create Control-to-Function Mapping

**Mapping Document:**
```
CIS 5.2.1 → check_5_2_1(), remediate_5_2_1(), rollback_5_2_1()
CIS 5.2.2 → check_5_2_2(), remediate_5_2_2(), rollback_5_2_2()
...
```

### Step 2.4: Prioritize by Severity

**Priority Order:**
1. **CAT I / CIS L1 Critical:** Immediate exploitation risk
2. **CAT II / CIS L1 High:** Significant security gap
3. **CAT III / CIS L2 Medium:** Defense-in-depth
4. **CIS L2 Low:** Best practice enhancements

**Checkpoint:** Update session file with control mapping completed

---

## Phase 3: CODE - Script Generation

**Duration:** 1-2 hours

**Goal:** Generate platform-specific automation scripts

### Step 3.1: Create Script Structure

**Template Components:**
```bash
#!/bin/bash
# [Framework] [Platform] [Level] Benchmark Script
# Version: 1.0

# Configuration
DRY_RUN=false
VERBOSE=false
REPORT_FILE="compliance-report.json"

# Utility Functions
log() { ... }
backup_config() { ... }
restore_config() { ... }

# Check Functions (one per control)
check_X_Y_Z() { ... }

# Remediation Functions (one per control)
remediate_X_Y_Z() { ... }

# Rollback Functions (one per control)
rollback_X_Y_Z() { ... }

# Reporting
generate_report() { ... }

# Main Execution
main() { ... }
```

### Step 3.2: Generate Check Functions

**For EACH control, create check function:**
```bash
check_5_2_1() {
    local file="/etc/ssh/sshd_config"

    # Get current state
    local owner=$(stat -c '%U' "$file")
    local group=$(stat -c '%G' "$file")
    local perms=$(stat -c '%a' "$file")

    # Compare against requirement
    if [[ "$owner" == "root" && "$group" == "root" && "$perms" == "600" ]]; then
        log "PASS: CIS 5.2.1 - SSH config permissions correct"
        return 0
    else
        log "FAIL: CIS 5.2.1 - SSH config permissions incorrect (current: $owner:$group $perms, expected: root:root 600)"
        return 1
    fi
}
```

### Step 3.3: Generate Remediation Functions

**For EACH control, create remediation function:**
```bash
remediate_5_2_1() {
    local file="/etc/ssh/sshd_config"

    log "Remediating CIS 5.2.1: SSH config permissions"

    # Backup current state
    backup_config "$file"

    # Apply fix
    chown root:root "$file"
    chmod 600 "$file"

    # Verify remediation
    if check_5_2_1; then
        log "SUCCESS: CIS 5.2.1 remediated"
        return 0
    else
        log "FAILED: CIS 5.2.1 remediation unsuccessful"
        rollback_5_2_1
        return 1
    fi
}
```

### Step 3.4: Generate Rollback Functions

**For EACH control, create rollback function:**
```bash
rollback_5_2_1() {
    local file="/etc/ssh/sshd_config"

    log "Rolling back CIS 5.2.1: SSH config permissions"

    restore_config "$file"

    if [ $? -eq 0 ]; then
        log "SUCCESS: CIS 5.2.1 rolled back"
    else
        log "FAILED: CIS 5.2.1 rollback unsuccessful"
    fi
}
```

### Step 3.5: Implement Dry-Run Mode

```bash
DRY_RUN=false  # Set via --dry-run flag

apply_change() {
    local command="$1"

    if [ "$DRY_RUN" = true ]; then
        log "[DRY-RUN] Would execute: $command"
    else
        eval "$command"
    fi
}
```

### Step 3.6: Add Reporting

```bash
generate_report() {
    local total=$1
    local passed=$2
    local failed=$3
    local compliance_score=$(( passed * 100 / total ))

    cat > "$REPORT_FILE" <<EOF
{
  "framework": "CIS Ubuntu 22.04 LTS Benchmark",
  "version": "v1.0.0",
  "level": "Level 1 - Server",
  "scan_date": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "compliance_score": $compliance_score,
  "summary": {
    "total": $total,
    "passed": $passed,
    "failed": $failed
  },
  "findings": [...]
}
EOF
}
```

**Checkpoint:** Update session file with scripts generated

---

## Phase 4: COMMIT - Testing & Documentation

**Duration:** 1 hour

**Goal:** Validate scripts and create usage documentation

### Step 4.1: Test in Dry-Run Mode

```bash
# Test without making changes
./cis-ubuntu-22.04-l1.sh --dry-run

# Verify:
# - All check functions execute without errors
# - Dry-run mode prevents actual changes
# - Report generation works
```

### Step 4.2: Test on Non-Production System

```bash
# Test with actual execution
sudo ./cis-ubuntu-22.04-l1.sh

# Verify:
# - Remediation functions apply changes correctly
# - Check functions now return PASS
# - Report shows improved compliance score
```

### Step 4.3: Test Rollback Functionality

```bash
# Apply remediations
sudo ./cis-ubuntu-22.04-l1.sh --remediate

# Test rollback
sudo ./cis-ubuntu-22.04-l1.sh --rollback

# Verify:
# - Configuration restored to pre-remediation state
# - System functional
```

### Step 4.4: Create Usage Documentation

**Documentation Includes:**
- **Installation:** Prerequisites, permissions required
- **Usage:** Command-line flags, examples
- **Dry-Run:** Testing without changes
- **Remediation:** Applying fixes
- **Rollback:** Reverting changes
- **Reporting:** Understanding compliance reports
- **Troubleshooting:** Common issues, error messages

### Step 4.5: Document Limitations

**Known Limitations:**
- Controls requiring manual review
- Service disruption risks
- Platform version compatibility
- Reboot requirements

**Checkpoint:** Update session file with testing completed, script ready

---

## Deliverables Checklist

**Phase 1: Requirements**
- ✅ Compliance framework identified
- ✅ Platform specifications documented
- ✅ Automation scope defined
- ✅ Script format selected

**Phase 2: Planning**
- ✅ Control mapping completed (automated vs manual)
- ✅ Control-to-function mapping created
- ✅ Priority order established

**Phase 3: Script Generation**
- ✅ Script structure created
- ✅ Check functions generated (one per control)
- ✅ Remediation functions generated (one per control)
- ✅ Rollback functions generated (one per control)
- ✅ Dry-run mode implemented
- ✅ Reporting functions added

**Phase 4: Testing**
- ✅ Dry-run testing completed
- ✅ Non-production testing completed
- ✅ Rollback testing completed
- ✅ Usage documentation created
- ✅ Limitations documented

---

**Version:** 2.0
**Last Updated:** 2025-12-02
**Workflow:** EXPLORE → PLAN → CODE → COMMIT
**Duration:** 4-6 hours (standard automation)
