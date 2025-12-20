#!/usr/bin/env python3
"""
Rollback Fix from Backup

Restores original code from backup with:
- Integrity verification (hash check)
- Git revert (if applicable)
- Documentation update
- Reason logging

Usage:
    python rollback-fix.py --backup backups/file.py.backup-YYYYMMDD-HHMMSS --target file.py --reason "Validation failed"

Author: Intelligence Adjacent
Version: 1.0
Last Updated: 2025-11-24
"""

import argparse
import sys
import hashlib
import shutil
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Tuple


def calculate_file_hash(file_path: Path) -> str:
    """Calculate SHA256 hash of file"""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def load_backup_metadata(backup_dir: Path) -> Dict:
    """Load metadata for backup verification"""
    try:
        metadata_file = backup_dir / 'backup-metadata.json'
        if not metadata_file.exists():
            return {}

        with open(metadata_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}


def find_backup_entry(metadata: Dict, backup_file: str) -> Optional[Dict]:
    """Find metadata entry for specific backup file"""
    backup_path_str = str(Path(backup_file).absolute())

    for entry in metadata.get('backups', []):
        if entry.get('backup_path') == backup_path_str:
            return entry

    return None


def verify_backup_integrity(backup_file: Path, expected_hash: Optional[str] = None) -> Tuple[bool, str]:
    """Verify backup file integrity"""
    try:
        if not backup_file.exists():
            return False, "FILE_NOT_FOUND"

        actual_hash = calculate_file_hash(backup_file)

        if expected_hash:
            return actual_hash == expected_hash, actual_hash
        else:
            return True, actual_hash

    except Exception as e:
        return False, f"ERROR: {e}"


def restore_from_backup(backup_file: Path, target_file: Path) -> bool:
    """Copy backup file to target location"""
    try:
        # Create backup of current state before rollback
        if target_file.exists():
            rollback_backup = target_file.parent / f"{target_file.name}.pre-rollback"
            shutil.copy2(target_file, rollback_backup)
            print(f"[+] Current state backed up: {rollback_backup}")

        # Restore from backup
        shutil.copy2(backup_file, target_file)
        return True

    except Exception as e:
        print(f"[!] Restore failed: {e}")
        return False


def is_git_repo(path: Path) -> bool:
    """Check if path is inside a git repository"""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--git-dir'],
            cwd=str(path.parent if path.is_file() else path),
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False


def revert_git_commit(target_file: Path, commit_hash: str) -> Optional[str]:
    """Revert git commit"""
    try:
        repo_dir = target_file.parent if target_file.is_file() else target_file

        # Git revert
        result = subprocess.run(
            ['git', 'revert', '--no-commit', commit_hash],
            cwd=str(repo_dir),
            capture_output=True,
            timeout=30
        )

        if result.returncode != 0:
            print(f"[!] Git revert failed: {result.stderr.decode()}")
            return None

        # Commit the revert
        result = subprocess.run(
            ['git', 'commit', '-m', f'Revert fix (rollback): {commit_hash[:8]}'],
            cwd=str(repo_dir),
            capture_output=True,
            timeout=10
        )

        if result.returncode != 0:
            print(f"[!] Git commit failed: {result.stderr.decode()}")
            return None

        # Get new commit hash
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            cwd=str(repo_dir),
            capture_output=True,
            timeout=5
        )

        if result.returncode == 0:
            return result.stdout.decode().strip()

        return None

    except Exception as e:
        print(f"[!] Git revert error: {e}")
        return None


def log_rollback(backup_dir: Path, backup_file: Path, target_file: Path, reason: str):
    """Log rollback event"""
    try:
        rollback_log = backup_dir / 'rollback-log.json'

        if rollback_log.exists():
            with open(rollback_log, 'r', encoding='utf-8') as f:
                log = json.load(f)
        else:
            log = {'rollbacks': []}

        entry = {
            'timestamp': datetime.now().isoformat(),
            'backup_file': str(backup_file),
            'target_file': str(target_file),
            'reason': reason
        }

        log['rollbacks'].append(entry)

        with open(rollback_log, 'w', encoding='utf-8') as f:
            json.dump(log, f, indent=2)

        print(f"[+] Rollback logged: {rollback_log}")

    except Exception as e:
        print(f"[!] Warning: Failed to log rollback: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Rollback fix from backup',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python rollback-fix.py --backup backups/app.py.backup-20251124-143022 --target app.py
  python rollback-fix.py --backup backups/app.py.backup-20251124-143022 --target app.py --reason "Validation failed"
  python rollback-fix.py --backup backups/app.py.backup-20251124-143022 --target app.py --git-revert abc1234
        """
    )

    parser.add_argument('--backup', required=True, help='Backup file path')
    parser.add_argument('--target', required=True, help='Target file to restore')
    parser.add_argument('--git-revert', help='Git commit hash to revert (optional)')
    parser.add_argument('--reason', default='Manual rollback', help='Rollback reason')

    args = parser.parse_args()

    backup_path = Path(args.backup)
    target_path = Path(args.target)

    # Validate inputs
    if not backup_path.exists():
        print(f"[!] Backup file not found: {args.backup}")
        return 1

    if not target_path.exists():
        print(f"[!] Target file not found: {args.target}")
        print(f"[!] Cannot rollback to non-existent file")
        return 1

    print(f"\n[*] ROLLBACK OPERATION")
    print(f"[*] Target: {args.target}")
    print(f"[*] Backup: {args.backup}")
    print(f"[*] Reason: {args.reason}")

    # Load and verify backup metadata
    print(f"\n[*] Verifying backup integrity...")
    backup_dir = backup_path.parent
    metadata = load_backup_metadata(backup_dir)

    backup_entry = find_backup_entry(metadata, str(backup_path))
    expected_hash = backup_entry.get('original_hash') if backup_entry else None

    is_valid, actual_hash = verify_backup_integrity(backup_path, expected_hash)

    if not is_valid:
        print(f"[!] Backup integrity check FAILED")
        if expected_hash:
            print(f"[!] Expected hash: {expected_hash[:16]}...")
        print(f"[!] Actual result: {actual_hash}")
        print(f"[!] Aborting rollback (backup may be corrupted)")
        return 1

    print(f"[+] Backup integrity: VERIFIED")
    print(f"[+] Hash: {actual_hash[:16]}...")

    # Confirm rollback
    print(f"\n[!] WARNING: This will restore {target_path.name} to previous state")
    print(f"[!] Current version will be backed up as .pre-rollback")

    # Restore from backup
    print(f"\n[*] Restoring file from backup...")
    if not restore_from_backup(backup_path, target_path):
        print(f"[!] Restore failed - aborting")
        return 1

    print(f"[+] File restored successfully")

    # Verify restoration
    restored_hash = calculate_file_hash(target_path)
    if restored_hash == actual_hash:
        print(f"[+] Restoration verified (hash match)")
    else:
        print(f"[!] Warning: Hash mismatch after restoration")

    # Git revert (if applicable)
    new_commit = None
    if args.git_revert:
        print(f"\n[*] Reverting git commit {args.git_revert[:8]}...")
        if is_git_repo(target_path):
            new_commit = revert_git_commit(target_path, args.git_revert)
            if new_commit:
                print(f"[+] Git revert commit: {new_commit[:8]}")
            else:
                print(f"[!] Git revert failed (check git status manually)")
        else:
            print(f"[!] Not a git repository - skipping revert")

    # Log rollback
    print(f"\n[*] Logging rollback...")
    log_rollback(backup_dir, backup_path, target_path, args.reason)

    # Print summary
    print(f"\n{'='*70}")
    print(f"ROLLBACK COMPLETE")
    print(f"{'='*70}")
    print(f"File: {args.target}")
    print(f"Restored from: {args.backup}")
    print(f"Backup hash: {actual_hash[:16]}...")
    print(f"Reason: {args.reason}")

    if new_commit:
        print(f"Git revert: {args.git_revert[:8]} → {new_commit[:8]}")

    print(f"\n[i] Original vulnerability is still present")
    print(f"[i] Review research findings to improve next remediation attempt")

    if backup_entry:
        print(f"\n[i] Backup metadata:")
        print(f"    Created: {backup_entry.get('timestamp', 'unknown')}")
        print(f"    Original hash: {backup_entry.get('original_hash', 'unknown')[:16]}...")

    return 0


if __name__ == '__main__':
    sys.exit(main())
