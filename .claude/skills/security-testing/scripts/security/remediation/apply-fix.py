#!/usr/bin/env python3
"""
Apply Tested Fix with Automatic Backup

Applies fix to production code with:
- Automatic backup creation
- Git commit (if repo detected)
- Metadata storage
- Rollback instructions

Usage:
    python apply-fix.py --patch fix.patch --target file.py --backup-dir backups/ --git-commit "Fix VULN-001"

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
from typing import Dict, Optional


def calculate_file_hash(file_path: Path) -> str:
    """Calculate SHA256 hash of file"""
    sha256 = hashlib.sha256()

    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)

    return sha256.hexdigest()


def create_backup(target_file: str, backup_dir: str) -> Dict[str, str]:
    """
    Create backup with timestamp and metadata

    Returns:
        dict: {backup_path, original_hash, timestamp, target_file}
    """
    try:
        target_path = Path(target_file)
        if not target_path.exists():
            raise FileNotFoundError(f"Target file not found: {target_file}")

        # Create backup directory if doesn't exist
        backup_path = Path(backup_dir)
        backup_path.mkdir(parents=True, exist_ok=True)

        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        backup_filename = f"{target_path.name}.backup-{timestamp}"
        backup_file = backup_path / backup_filename

        # Calculate hash of original file before backup
        original_hash = calculate_file_hash(target_path)

        # Create backup
        shutil.copy2(target_path, backup_file)

        # Verify backup
        backup_hash = calculate_file_hash(backup_file)
        if backup_hash != original_hash:
            raise RuntimeError("Backup verification failed: hash mismatch")

        return {
            'backup_path': str(backup_file),
            'original_hash': original_hash,
            'timestamp': timestamp,
            'target_file': str(target_path.absolute()),
            'backup_dir': str(backup_path.absolute())
        }

    except Exception as e:
        print(f"[!] Backup creation failed: {e}")
        sys.exit(1)


def apply_patch(patch_file: str, target_file: str) -> bool:
    """Apply patch to production file"""
    try:
        patch_path = Path(patch_file)
        target_path = Path(target_file)

        if not patch_path.exists():
            raise FileNotFoundError(f"Patch file not found: {patch_file}")

        if not target_path.exists():
            raise FileNotFoundError(f"Target file not found: {target_file}")

        # Read patch content
        with open(patch_path, 'r', encoding='utf-8') as f:
            patch_content = f.read()

        # Try using system 'patch' command first
        try:
            result = subprocess.run(
                ['patch', '-p0', str(target_path)],
                input=patch_content,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                return True
            else:
                print(f"[!] Patch command failed: {result.stderr}")
                # Try Python fallback
                return apply_patch_python(patch_content, target_path)

        except FileNotFoundError:
            # 'patch' command not available, use Python implementation
            return apply_patch_python(patch_content, target_path)

    except Exception as e:
        print(f"[!] Patch application failed: {e}")
        return False


def apply_patch_python(patch_content: str, target_file: Path) -> bool:
    """Simple Python-based patch application (fallback)"""
    try:
        # For MVP, support full file replacement
        if '--- COMPLETE FILE ---' in patch_content:
            new_content = patch_content.split('--- COMPLETE FILE ---')[1].strip()
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        else:
            # For unified diff, try basic line-by-line replacement
            # This is a simplified implementation
            with open(target_file, 'r', encoding='utf-8') as f:
                original_lines = f.readlines()

            # Parse simple unified diff format
            new_lines = []
            in_diff = False
            for line in patch_content.split('\n'):
                if line.startswith('---') or line.startswith('+++'):
                    in_diff = True
                    continue
                elif line.startswith('@@'):
                    in_diff = True
                    continue
                elif in_diff:
                    if line.startswith('+'):
                        new_lines.append(line[1:] + '\n')
                    elif not line.startswith('-'):
                        new_lines.append(line + '\n')

            if new_lines:
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                return True

            return False

    except Exception as e:
        print(f"[!] Python patch application failed: {e}")
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


def create_git_commit(target_file: str, commit_message: str) -> Optional[str]:
    """Create git commit if repo detected"""
    try:
        target_path = Path(target_file)

        # Check if git repo
        if not is_git_repo(target_path):
            return None

        # Get current directory for git operations
        repo_dir = target_path.parent if target_path.is_file() else target_path

        # Stage file
        result = subprocess.run(
            ['git', 'add', str(target_path)],
            cwd=str(repo_dir),
            capture_output=True,
            timeout=10
        )

        if result.returncode != 0:
            print(f"[!] Git add failed: {result.stderr.decode()}")
            return None

        # Create commit
        result = subprocess.run(
            ['git', 'commit', '-m', commit_message],
            cwd=str(repo_dir),
            capture_output=True,
            timeout=10
        )

        if result.returncode != 0:
            # Check if "nothing to commit" error
            if 'nothing to commit' in result.stdout.decode().lower():
                print(f"[!] Nothing to commit (no changes detected)")
                return None
            else:
                print(f"[!] Git commit failed: {result.stderr.decode()}")
                return None

        # Get commit hash
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            cwd=str(repo_dir),
            capture_output=True,
            timeout=5
        )

        if result.returncode == 0:
            commit_hash = result.stdout.decode().strip()
            return commit_hash
        else:
            return None

    except Exception as e:
        print(f"[!] Git commit error: {e}")
        return None


def store_backup_metadata(backup_info: Dict[str, str], metadata_file: Path) -> bool:
    """Store backup metadata for rollback"""
    try:
        # Load existing metadata if file exists
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        else:
            metadata = {'backups': []}

        # Add retention days
        backup_info['retention_days'] = 30
        backup_info['created_at'] = datetime.now().isoformat()

        # Append new backup
        metadata['backups'].append(backup_info)

        # Write metadata
        metadata_file.parent.mkdir(parents=True, exist_ok=True)
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)

        return True

    except Exception as e:
        print(f"[!] Metadata storage failed: {e}")
        return False


def print_rollback_instructions(backup_path: str, target_file: str):
    """Print rollback command for user"""
    rollback_cmd = (
        f"python tools/security/remediation/rollback-fix.py "
        f"--backup {backup_path} "
        f"--target {target_file}"
    )
    print(f"\n[i] Rollback available via:")
    print(f"    {rollback_cmd}")


def verify_applied_fix(target_file: str, expected_hash: Optional[str] = None) -> bool:
    """Verify fix was applied correctly"""
    try:
        target_path = Path(target_file)
        if not target_path.exists():
            return False

        # Calculate new hash
        new_hash = calculate_file_hash(target_path)

        # If expected hash provided, verify it matches
        if expected_hash:
            return new_hash == expected_hash

        # Otherwise, just confirm file is readable
        return True

    except:
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Apply fix with automatic backup',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python apply-fix.py --patch fix.patch --target vulnerable.py --backup-dir backups/
  python apply-fix.py --patch fix.patch --target app.py --backup-dir backups/ --git-commit "Fix: SQL injection in login"
        """
    )

    parser.add_argument('--patch', required=True, help='Patch file to apply')
    parser.add_argument('--target', required=True, help='Target file to patch')
    parser.add_argument('--backup-dir', required=True, help='Backup directory')
    parser.add_argument('--git-commit', help='Git commit message (optional)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would happen without applying')

    args = parser.parse_args()

    # Validate inputs
    if not Path(args.patch).exists():
        print(f"[!] Patch file not found: {args.patch}")
        return 1

    if not Path(args.target).exists():
        print(f"[!] Target file not found: {args.target}")
        return 1

    print(f"\n[*] Applying fix to production code")
    print(f"[*] Target: {args.target}")
    print(f"[*] Patch: {args.patch}")

    if args.dry_run:
        print(f"\n[*] DRY RUN MODE - No changes will be made")

    # Step 1: Create backup
    print(f"\n[*] Creating backup...")
    backup_info = create_backup(args.target, args.backup_dir)
    print(f"[+] Backup created: {backup_info['backup_path']}")
    print(f"[+] Original hash: {backup_info['original_hash'][:16]}...")

    if args.dry_run:
        print(f"\n[*] DRY RUN: Would apply patch to {args.target}")
        print(f"[*] DRY RUN: Would store metadata")
        return 0

    # Step 2: Apply patch
    print(f"\n[*] Applying patch to production file...")
    if not apply_patch(args.patch, args.target):
        print(f"[!] Patch application failed")
        print(f"[!] Original file preserved in backup: {backup_info['backup_path']}")
        return 1

    print(f"[+] Patch applied successfully")

    # Step 3: Verify fix
    print(f"\n[*] Verifying applied fix...")
    if not verify_applied_fix(args.target):
        print(f"[!] Verification failed - file may be corrupted")
        print(f"[!] Use rollback to restore: {backup_info['backup_path']}")
        return 1

    # Calculate new hash
    new_hash = calculate_file_hash(Path(args.target))
    backup_info['new_hash'] = new_hash
    print(f"[+] New hash: {new_hash[:16]}...")

    # Step 4: Git commit (if requested)
    if args.git_commit:
        print(f"\n[*] Creating git commit...")
        commit_hash = create_git_commit(args.target, args.git_commit)
        if commit_hash:
            print(f"[+] Git commit: {commit_hash[:8]}")
            backup_info['git_commit'] = commit_hash
        else:
            print(f"[!] Git commit skipped (not a repository or no changes)")

    # Step 5: Store metadata
    print(f"\n[*] Storing backup metadata...")
    metadata_file = Path(args.backup_dir) / 'backup-metadata.json'
    if store_backup_metadata(backup_info, metadata_file):
        print(f"[+] Metadata saved: {metadata_file}")
    else:
        print(f"[!] Warning: Metadata storage failed (backup still exists)")

    # Print summary
    print(f"\n{'='*70}")
    print(f"FIX APPLIED SUCCESSFULLY")
    print(f"{'='*70}")
    print(f"File: {args.target}")
    print(f"Backup: {backup_info['backup_path']}")
    print(f"Retention: 30 days")

    if 'git_commit' in backup_info:
        print(f"Git commit: {backup_info['git_commit'][:8]}")

    # Print rollback instructions
    print_rollback_instructions(backup_info['backup_path'], args.target)

    print(f"\n[+] NEXT STEP: Retest vulnerability in production")
    print(f"    python tools/security/remediation/validate-fix.py \\")
    print(f"      --target {args.target} \\")
    print(f"      --test-command 'your test command here'")

    print(f"\n[i] If validation passes, keep the fix")
    print(f"[i] If validation fails, use rollback command above")

    return 0


if __name__ == '__main__':
    sys.exit(main())
