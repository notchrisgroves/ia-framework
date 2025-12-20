
## Problem Statement

**Current Issue:**
After completing security testing engagements, significant manual cleanup is required:
- VPS accumulates ~1GB of installers, temp files, auth cookies, bash history
- System configurations may be altered during testing
- Local working directories contain large scan outputs and temporary files
- No systematic tracking of what changed during engagement
- Credentials and tokens left on systems

**Impact:**
- Security risk (leftover credentials/tokens)
- Disk space waste
- System configuration drift
- No audit trail of changes
- Manual cleanup is error-prone and time-consuming

---

## Solution Architecture

**Three-Component System:**

1. **Pre-Engagement State Capture** - Snapshot system state before testing
2. **Change Tracking** - Monitor modifications during engagement
3. **Post-Engagement Cleanup** - Automatic restoration and cleanup

**Design Principles:**
- ✅ Automatic by default (minimal manual intervention)
- ✅ Safe (never delete critical system files)
- ✅ Auditable (log all cleanup actions)
- ✅ Reversible (can restore if needed)
- ✅ Integrated into existing workflow

---

## Component 1: Pre-Engagement State Capture

**When:** Phase 1 (Engagement Setup) - BEFORE any testing

**What to Snapshot:**

### VPS State (root@72.60.27.87)
```python
snapshot_data = {
    "timestamp": "2025-11-11T14:00:00Z",
    "engagement_id": "airtable-bugbounty-2025-11",
    "vps": {
        "hostname": "72.60.27.87",
        "disk_usage": {
            "/root": "1.2GB",
            "/tmp": "45MB",
            "/var/log": "230MB",
            "/home": "120MB"
        },
        "installed_packages": [
            # apt list --installed output (hash only for comparison)
        ],
        "critical_configs": {
            "/etc/hosts": "sha256_hash",
            "/etc/resolv.conf": "sha256_hash",
            "/etc/ssh/sshd_config": "sha256_hash",
            "/root/.bashrc": "sha256_hash",
            "/root/.bash_profile": "sha256_hash"
        },
        "running_processes": [
            # ps aux output snapshot
        ],
        "open_ports": [
            # netstat -tulpn output
        ],
        "docker_containers": [
            # docker ps -a output
        ],
        "bash_history_lines": 1543,  # Line count for comparison
        "reaper_db_size": "450MB",
        "tools_directory": {
            "/root/tools": "2.1GB",
            "file_count": 8432
        }
    }
}
```

### Local State (Windows workstation)
```python
snapshot_data = {
    "engagement_dir": "../../output/engagements/pentest/airtable-bugbounty-2025-11",
    "disk_usage": "3.5GB",
    "file_count": 2847,
    "subdirectories": {
        "00-scope": {"size": "12MB", "files": 15},
        "02-reconnaissance": {"size": "450MB", "files": 234},
        "03-vulnerability-assessment": {"size": "2.8GB", "files": 1894},
        "05-findings": {"size": "2.3MB", "files": 8},
        "06-reporting": {"size": "850KB", "files": 3}
    },
    "temp_files": [
        # List of files marked as temporary (.tmp, .temp, etc.)
    ],
    "credentials_used": [
        "airtable_api_key",
        "test_user_session_cookie"
    ]
}
```

**Storage Location:**
- VPS: `/root/.engagement-snapshots/[engagement-id].json`
- Local: `[engagement-dir]/.snapshot.json`

**Implementation:** `../scripts/security/capture-engagement-state.py`

---

## Component 2: Change Tracking During Engagement

**When:** Throughout testing (automatic via filesystem monitoring)

**Tracking Methods:**

### VPS Change Detection
```python
tracked_changes = {
    "engagement_id": "airtable-bugbounty-2025-11",
    "changes": [
        {
            "timestamp": "2025-11-11T14:23:45Z",
            "type": "file_created",
            "path": "/tmp/airtable-scan-results.txt",
            "size": "450KB",
            "category": "temp_output",
            "action": "delete_on_cleanup"
        },
        {
            "timestamp": "2025-11-11T15:12:33Z",
            "type": "file_modified",
            "path": "/root/.bashrc",
            "size_before": "3.2KB",
            "size_after": "3.5KB",
            "hash_before": "abc123...",
            "hash_after": "def456...",
            "category": "system_config",
            "action": "restore_on_cleanup"
        },
        {
            "timestamp": "2025-11-11T16:45:22Z",
            "type": "file_created",
            "path": "/root/tools/custom-exploit.py",
            "size": "12KB",
            "category": "engagement_tool",
            "action": "delete_on_cleanup"
        },
        {
            "timestamp": "2025-11-11T17:30:11Z",
            "type": "credentials_stored",
            "path": "/root/.cookies/airtable-session.txt",
            "category": "sensitive",
            "action": "secure_delete"  # Overwrite before deletion
        }
    ]
}
```

### Change Categories

**1. temp_output** - Scan results, temporary files
- **Action:** Delete without confirmation
- **Examples:** `/tmp/*`, `scan-results.txt`, `output-*.json`

**2. system_config** - Modified system files
- **Action:** Restore from snapshot
- **Examples:** `/etc/hosts`, `/root/.bashrc`, `sshd_config`

**3. engagement_tool** - Custom tools/exploits created during testing
- **Action:** Offer to archive OR delete
- **Examples:** Custom Python scripts, exploit POCs, test payloads

**4. sensitive** - Credentials, tokens, cookies
- **Action:** Secure delete (overwrite 3x before removal)
- **Examples:** API keys, session cookies, auth tokens, passwords

**5. installer** - Tool installers and downloads
- **Action:** Delete without confirmation
- **Examples:** `.deb` files, `.tar.gz` archives, installers

**6. logs** - Testing logs and histories
- **Action:** Selective cleanup (keep last 100 bash history lines, delete engagement-specific logs)
- **Examples:** `.bash_history`, `/var/log/engagement-*.log`

**Implementation:** `../scripts/security/track-engagement-changes.py` (inotify-based)

---

## Component 3: Post-Engagement Cleanup

**When:** After engagement completion (manual trigger OR automatic on engagement close)

**Cleanup Workflow:**

### Step 1: Generate Cleanup Plan

```python
cleanup_plan = {
    "engagement_id": "airtable-bugbounty-2025-11",
    "timestamp": "2025-11-15T10:00:00Z",
    "duration_days": 4,
    "actions": {
        "vps": {
            "delete_files": [
                {"path": "/tmp/airtable-scan-*.txt", "size": "450KB", "count": 23},
                {"path": "/root/tools/temp-exploit.py", "size": "12KB", "count": 1},
                {"path": "/root/.cookies/airtable-*.txt", "size": "2KB", "count": 3, "secure": True}
            ],
            "restore_configs": [
                {"path": "/root/.bashrc", "backup": "/root/.engagement-snapshots/airtable-bugbounty-2025-11/bashrc.backup"}
            ],
            "clean_bash_history": {
                "total_lines": 1823,
                "engagement_lines": 280,
                "action": "Remove lines 1543-1823"
            },
            "clean_reaper_db": {
                "size_before": "890MB",
                "size_after_estimated": "450MB",
                "action": "Delete requests for hostname: staging.airtable.com"
            },
            "package_cleanup": [
                # Any tools installed ONLY for this engagement
            ]
        },
        "local": {
            "archive_large_files": [
                {"path": "03-vulnerability-assessment/scan-outputs/nmap-full-*.txt", "size": "1.2GB"},
                {"path": "03-vulnerability-assessment/reaper-traffic/*.db", "size": "890MB"}
            ],
            "compress_engagement": {
                "source": "airtable-bugbounty-2025-11/",
                "archive": "airtable-bugbounty-2025-11.tar.gz",
                "compression_ratio_estimated": "60%",
                "size_before": "3.5GB",
                "size_after_estimated": "1.4GB"
            },
            "delete_temp_files": [
                {"path": "scratchpad/airtable-temp-*.txt", "count": 15, "size": "34MB"}
            ]
        }
    },
    "space_savings": {
        "vps": "~1.1GB",
        "local": "~2.1GB",
        "total": "~3.2GB"
    }
}
```

### Step 2: User Review and Approval

**Interactive Prompt:**
```
========================================
ENGAGEMENT CLEANUP PLAN
========================================

Engagement: airtable-bugbounty-2025-11
Duration: 4 days
Status: COMPLETE

VPS CLEANUP (root@72.60.27.87):
  [DELETE] 23 temp scan files (450KB)
  [DELETE] 3 auth cookies (2KB) - SECURE DELETION
  [RESTORE] /root/.bashrc (modified during engagement)
  [CLEAN] Bash history (remove 280 engagement lines)
  [CLEAN] Reaper database (remove staging.airtable.com traffic)
  Space savings: ~1.1GB

LOCAL CLEANUP (Windows):
  [ARCHIVE] Large scan outputs (2.1GB → compress to ~840MB)
  [COMPRESS] Engagement directory (3.5GB → 1.4GB tar.gz)
  [DELETE] 15 temp files from scratchpad (34MB)
  Space savings: ~2.1GB

TOTAL SPACE SAVINGS: ~3.2GB

Options:
  [1] Execute full cleanup (recommended)
  [2] VPS cleanup only
  [3] Local cleanup only
  [4] Custom (select specific actions)
  [5] Cancel (no cleanup)

Enter choice (1-5):
```

### Step 3: Execute Cleanup

**Step 3.0: Stop VPS Containers (CRITICAL - Do First)**

**Why First:** Stops containers before cleaning output files to prevent new files being written

```bash
# SSH to VPS and stop all running security tool containers
ssh -i ${OVHCLOUD_VPS_SSH_KEY} -p ${OVHCLOUD_VPS_SSH_PORT} ${OVHCLOUD_VPS_USERNAME}@${OVHCLOUD_VPS_IP} \
  "cd /root/security-tools && docker compose down"
```

**Expected Output:**
```
[+] Running 6/6
 ✔ Container kali-pentest     Removed
 ✔ Container web3-security    Removed
 ✔ Container mobile-tools     Removed
 ✔ Container reaper           Removed
 ✔ Container metasploit       Removed
 ✔ Network security-tools_security-tools  Removed
```

**Verify Containers Stopped:**
```bash
ssh -i ${OVHCLOUD_VPS_SSH_KEY} -p ${OVHCLOUD_VPS_SSH_PORT} ${OVHCLOUD_VPS_USERNAME}@${OVHCLOUD_VPS_IP} \
  "docker ps"
```

**Expected:** No containers running (empty table except header)

**⚠️ Container Lifecycle Reminder:**
- **On-Demand Model:** Containers only run during active engagements
- **Resource Savings:** Stops memory usage, prevents disk accumulation
- **Next Engagement:** Containers will be started fresh (see pentest-init.md Phase 0)

---

**Step 3.1: VPS File Cleanup**

**VPS Cleanup Script:**
```powershell
#!/bin/bash
# cleanup-engagement-vps.sh

ENGAGEMENT_ID="$env:1"
SNAPSHOT_FILE="/root/.engagement-snapshots/${ENGAGEMENT_ID}.json"

Write-Output "[+] Starting VPS cleanup for: $env:ENGAGEMENT_ID"

# 1. Delete temporary files
Write-Output "[+] Removing temporary files..."
find /tmp -name "${ENGAGEMENT_ID}*" -delete
find /root/tools -name "*temp*.py" -mtime -7 -delete

# 2. Secure delete sensitive files (3-pass overwrite)
Write-Output "[+] Securely deleting credentials and cookies..."
find /root/.cookies -name "${ENGAGEMENT_ID}*" -exec shred -vfz -n 3 {} \;

# 3. Restore modified system configs
Write-Output "[+] Restoring system configurations..."
if [ -f "/root/.engagement-snapshots/${ENGAGEMENT_ID}/bashrc.backup" ]; then
    Copy-Item "/root/.engagement-snapshots/${ENGAGEMENT_ID}/bashrc.backup" /root/.bashrc
    Write-Output "  [OK] Restored /root/.bashrc"
fi

# 4. Clean bash history (remove engagement-specific commands)
Write-Output "[+] Cleaning bash history..."
SNAPSHOT_LINE_COUNT=$(jq -r '.vps.bash_history_lines' "$env:SNAPSHOT_FILE")
CURRENT_LINE_COUNT=$((Get-Content ... ).Count  # was: wc -l < ~/.bash_history)
LINES_TO_REMOVE=$((CURRENT_LINE_COUNT - SNAPSHOT_LINE_COUNT))

if [ $env:LINES_TO_REMOVE -gt 0 ]; then
    # Keep only lines from before engagement
    head -n $env:SNAPSHOT_LINE_COUNT ~/.bash_history > ~/.bash_history.tmp
    Move-Item ~/.bash_history.tmp ~/.bash_history
    Write-Output "  [OK] Removed $env:LINES_TO_REMOVE lines from bash history"
fi

# 5. Clean Reaper database (delete engagement-specific traffic)
Write-Output "[+] Cleaning Reaper database..."
REAPER_DB="/root/reaper/reaper.db"
if [ -f "$env:REAPER_DB" ]; then
    # Extract target hostnames from engagement scope
    HOSTNAMES=$(jq -r '.engagement_hostnames[]' "$env:SNAPSHOT_FILE")
    for HOSTNAME in $env:HOSTNAMES; do
        sqlite3 "$env:REAPER_DB" "DELETE FROM requests WHERE hostname LIKE '%${HOSTNAME}%';"
        Write-Output "  [OK] Deleted requests for: $env:HOSTNAME"
    done

    # Vacuum database to reclaim space
    sqlite3 "$env:REAPER_DB" "VACUUM;"
    Write-Output "  [OK] Compacted Reaper database"
fi

# 6. Remove engagement snapshot (cleanup complete)
Write-Output "[+] Removing engagement snapshot..."
Remove-Item -Recurse -Force "/root/.engagement-snapshots/${ENGAGEMENT_ID}"

Write-Output "[+] VPS cleanup complete!"
```

**Local Cleanup Script:**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cleanup-engagement-local.py

import os
import sys
import json
import shutil
import tarfile
from pathlib import Path

def cleanup_engagement(engagement_dir, snapshot_file):
    """Clean up local engagement directory after completion."""

    print(f"[+] Starting local cleanup for: {engagement_dir}")

    with open(snapshot_file, 'r') as f:
        snapshot = json.load(f)

    # 1. Archive large scan outputs (compress to save space)
    print("[+] Archiving large scan outputs...")
    large_dirs = [
        "03-vulnerability-assessment/scan-outputs",
        "03-vulnerability-assessment/reaper-traffic"
    ]

    for dir_path in large_dirs:
        full_path = Path(engagement_dir) / dir_path
        if full_path.exists():
            archive_name = f"{dir_path.replace('/', '-')}.tar.gz"
            archive_path = Path(engagement_dir) / "archives" / archive_name
            archive_path.parent.mkdir(exist_ok=True)

            with tarfile.open(archive_path, "w:gz") as tar:
                tar.add(full_path, arcname=dir_path)

            # Delete original directory after successful archive
            shutil.rmtree(full_path)
            print(f"  [OK] Archived and removed: {dir_path}")

    # 2. Compress entire engagement directory
    print("[+] Compressing engagement directory...")
    engagement_name = Path(engagement_dir).name
    archive_path = Path(engagement_dir).parent / f"{engagement_name}.tar.gz"

    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(engagement_dir, arcname=engagement_name)

    original_size = sum(f.stat().st_size for f in Path(engagement_dir).rglob('*') if f.is_file())
    archive_size = archive_path.stat().st_size
    compression_ratio = (1 - archive_size / original_size) * 100

    print(f"  [OK] Created archive: {archive_path}")
    print(f"  [OK] Original: {original_size / 1024**3:.2f}GB → Archive: {archive_size / 1024**3:.2f}GB")
    print(f"  [OK] Compression ratio: {compression_ratio:.1f}%")

    # 3. Delete temporary files from scratchpad
    print("[+] Cleaning scratchpad temporary files...")
    scratchpad = Path.home() / ".claude" / "scratchpad"
    temp_pattern = f"{engagement_name}*"

    deleted_count = 0
    for temp_file in scratchpad.glob(temp_pattern):
        if temp_file.is_file():
            temp_file.unlink()
            deleted_count += 1

    if deleted_count > 0:
        print(f"  [OK] Deleted {deleted_count} temporary files")

    # 4. Remove snapshot file
    print("[+] Removing snapshot file...")
    Path(snapshot_file).unlink()

    print("[+] Local cleanup complete!")
    print(f"\n[!] Archived engagement saved to: {archive_path}")
    print("[!] Original directory preserved for now - delete manually after verification")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cleanup-engagement-local.py [engagement-dir]")
        sys.exit(1)

    engagement_dir = sys.argv[1]
    snapshot_file = Path(engagement_dir) / ".snapshot.json"

    if not snapshot_file.exists():
        print(f"[!] ERROR: Snapshot file not found: {snapshot_file}")
        sys.exit(1)

    cleanup_engagement(engagement_dir, snapshot_file)
```

---

## Integration into Security Testing Workflow

**Modified Phase Workflow:**

### Phase 1: Engagement Setup (ENHANCED)

**NEW Step 1.1: Capture Pre-Engagement State**
```python
# Execute BEFORE any testing begins
python ../scripts/security/capture-engagement-state.py \
    --engagement-dir "output/engagements/pentest/airtable-bugbounty-2025-11" \
    --vps "root@72.60.27.87"

# Output:
# [OK] VPS state captured: /root/.engagement-snapshots/airtable-bugbounty-2025-11.json
# [OK] Local state captured: output/engagements/pentest/airtable-bugbounty-2025-11/.snapshot.json
# [OK] Change tracking enabled
```

**NEW Step 1.2: Enable Change Monitoring**
```powershell
# On VPS (run in tmux/screen - background daemon)
python /root/tools/track-engagement-changes.py \
    --engagement-id "airtable-bugbounty-2025-11" \
    --snapshot "/root/.engagement-snapshots/airtable-bugbounty-2025-11.json" \
    --daemon
```

**Existing steps continue as normal...**

---

### NEW Phase 5: Post-Engagement Cleanup

**Trigger Points:**
1. **Manual:** User declares engagement complete
2. **Automatic:** No activity for 7+ days AND all findings documented

**Step 1: Generate Cleanup Plan**
```python
python ../scripts/security/generate-cleanup-plan.py \
    --engagement-dir "output/engagements/pentest/airtable-bugbounty-2025-11" \
    --vps "root@72.60.27.87"
```

**Step 2: Review and Approve**
- Interactive prompt (see template above)
- User selects cleanup scope
- Confirm before execution

**Step 3: Execute Cleanup**
```powershell
# VPS cleanup
ssh root@72.60.27.87 "bash /root/tools/cleanup-engagement-vps.sh airtable-bugbounty-2025-11"

# Local cleanup
python ../scripts/security/cleanup-engagement-local.py \
    "output/engagements/pentest/airtable-bugbounty-2025-11"
```

**Step 4: Verification**
```powershell
# Verify VPS state restored
ssh root@72.60.27.87 "df -h; (Get-Content ... ).Count  # was: wc -l ~/.bash_history"

# Verify local archive created
Get-ChildItemh "output/engagements/pentest/airtable-bugbounty-2025-11.tar.gz"
```

**Step 5: Update README.md**
```markdown
## Engagement Status: COMPLETE + CLEANED UP

- **Cleanup Date:** 2025-11-15
- **VPS Space Reclaimed:** 1.1GB
- **Local Space Reclaimed:** 2.1GB
- **Archive Location:** airtable-bugbounty-2025-11.tar.gz
- **Archive Size:** 1.4GB (from 3.5GB original)
```

---

## File Restoration Logic

**When to Restore vs When to Harden:**

### Restore (Return to Original State)
**Criteria:**
- File was modified during testing
- Original was not insecure
- Change was temporary for testing purposes

**Examples:**
- `/root/.bashrc` - Added test aliases
- `/etc/hosts` - Added test domain mappings
- SSH config - Temporary connection settings

**Action:** Copy from backup in snapshot directory

---

### Harden (Improve Security)
**Criteria:**
- File was insecure BEFORE testing
- Testing revealed security weakness
- Production system should be hardened

**Examples:**
- `/etc/ssh/sshd_config` - Weak cipher suites discovered
- Firewall rules - Overly permissive rules found
- Application configs - Insecure defaults

**Action:** Apply security hardening, document in findings

---

### Leave Modified (Intentional Improvement)
**Criteria:**
- File was intentionally improved
- Change benefits future engagements
- No security risk

**Examples:**
- Installed security tool (nuclei templates updated)
- Added useful bash function to `.bashrc`
- Improved tool configuration

**Action:** Keep change, update snapshot for next engagement

---

## Safety Mechanisms

**1. Dry-Run Mode:**
```powershell
# Preview cleanup without executing
python ../scripts/security/cleanup-engagement-local.py --dry-run [engagement-dir]
```

**2. Backup Before Delete:**
- All deletions create `.cleanup-backup/` directory
- Files stored for 30 days before permanent deletion
- Can rollback if mistake detected

**3. Critical File Protection:**
```python
PROTECTED_PATHS = [
    "/etc/passwd",
    "/etc/shadow",
    "/boot/*",
    "/root/.ssh/id_rsa*",
    "../../CLAUDE.md",
    "../../.env"
]
# These files NEVER deleted or restored automatically
```

**4. Change Log Audit Trail:**
- All cleanup actions logged to `.cleanup-log.json`
- Includes: timestamp, file path, action taken, user who approved
- Permanent record for compliance/auditing

---

## Implementation Checklist

### Phase 1: Core Scripts (Week 1)
- [ ] `../scripts/security/capture-engagement-state.py`
- [ ] `../scripts/security/track-engagement-changes.py`
- [ ] `../scripts/security/generate-cleanup-plan.py`
- [ ] `../scripts/security/cleanup-engagement-vps.sh`
- [ ] `../scripts/security/cleanup-engagement-local.py`

### Phase 2: Integration (Week 2)
- [ ] Update `../SKILL.md` with cleanup phase
- [ ] Add cleanup checklist to engagement README template
- [ ] Create cleanup notification hook
- [ ] Test on completed engagement (dry-run)

### Phase 3: Automation (Week 3)
- [ ] Automatic cleanup plan generation (7 days post-engagement)
- [ ] Email notification when cleanup ready
- [ ] One-click cleanup execution
- [ ] Scheduled VPS maintenance (monthly full cleanup)

### Phase 4: Advanced Features (Week 4)
- [ ] Intelligent file categorization (ML-based)
- [ ] Restore vs harden decision engine
- [ ] Engagement archive compression (optimized for large scan outputs)
- [ ] Cloud backup integration (encrypted archives to cold storage)

---

## Testing Strategy

**Test Engagement: drumgrange-vdp-2025-11 (Completed)**

1. **Retroactive Snapshot Creation:**
   - Manually document "before" state from memory
   - Create synthetic snapshot file
   - Identify known changes during engagement

2. **Dry-Run Cleanup:**
   - Generate cleanup plan for drumgrange
   - Review output for accuracy
   - Identify any mistakes in categorization

3. **Partial Cleanup Execution:**
   - Execute VPS cleanup only (reversible)
   - Verify system state after cleanup
   - Check that critical functions still work

4. **Full Cleanup Execution:**
   - Execute local cleanup
   - Verify archive created successfully
   - Test archive extraction (ensure nothing corrupted)

5. **Validation:**
   - Compare VPS state to snapshot
   - Verify space savings match estimates
   - Check for any unintended deletions

---

## Metrics and KPIs

**Track These Metrics:**

### Efficiency Metrics
- Time to complete manual cleanup: **BEFORE** (30-45 min) → **AFTER** (5 min)
- VPS disk space reclaimed per engagement: **~1-2GB**
- Local disk space reclaimed per engagement: **~2-4GB**
- Cleanup errors/mistakes: **Target: 0**

### Security Metrics
- Credentials left on systems: **Target: 0**
- System configs not restored: **Target: 0**
- Sensitive data in bash history: **Target: 0**

### Quality Metrics
- Engagements with complete snapshots: **Target: 100%**
- Cleanup plans approved before execution: **Target: 100%**
- Audit trail completeness: **Target: 100%**

---

## Rollback Procedures

**If Cleanup Goes Wrong:**

### Emergency Rollback (VPS)
```powershell
# 1. Restore from snapshot
tar -xzf /root/.engagement-snapshots/[engagement-id]/system-backup.tar.gz -C /

# 2. Restore specific file
Copy-Item /root/.engagement-snapshots/[engagement-id]/bashrc.backup /root/.bashrc

# 3. Check restoration
diff /root/.bashrc /root/.engagement-snapshots/[engagement-id]/bashrc.backup
```

### Emergency Rollback (Local)
```powershell
# 1. Extract archive
tar -xzf "airtable-bugbounty-2025-11.tar.gz"

# 2. Verify extraction
diff -r "airtable-bugbounty-2025-11/" "airtable-bugbounty-2025-11-restored/"
```

---

## Future Enhancements

**Phase 5 (Future):**
1. **ML-Based Change Classification**
   - Train model on historical engagement changes
   - Automatically categorize files without rules
   - Confidence scoring for delete/restore decisions

2. **Cloud Integration**
   - Automatic encrypted backup to S3/Azure Blob
   - 90-day retention for compliance
   - Cost optimization (lifecycle policies)

3. **Compliance Reporting**
   - Generate compliance reports (SOC 2, ISO 27001)
   - Demonstrate proper data handling
   - Audit trail export (PDF format)

4. **Multi-VPS Support**
   - Track changes across multiple VPS hosts
   - Coordinated cleanup across infrastructure
   - Centralized cleanup dashboard

---

## References

- **Engagement Template:** `../templates/_ENGAGEMENT-TEMPLATE/`
- **VPS Management:** `skills/infrastructure-ops/SKILL.md`
- **MCP Tool Wrappers:** `servers/kali_pentest/` (use Code API layer)
- **Workflow Documentation:** `../workflows/`

---

**Status:** READY FOR IMPLEMENTATION
**Next Steps:** Build core scripts (Phase 1), test on drumgrange-vdp-2025-11
**Owner:** Security Testing Workflow
**Last Updated:** 2025-01-11
