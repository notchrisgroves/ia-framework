#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Engagement State Capture Tool
Captures VPS and local system state BEFORE engagement testing begins.
Creates snapshots for later cleanup and restoration.

Usage:
    python tools/security/capture-engagement-state.py \\
        --engagement-dir "output/engagements/pentest/client-2025-11" \\
        --vps "root@72.60.27.87"

Author: Chris Groves
Created: 2025-01-11
"""

import sys
import io
import os
import json
import subprocess
import hashlib
from pathlib import Path
from datetime import datetime
import argparse

# Force UTF-8 encoding for Windows console output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def get_file_hash(file_path):
    """Calculate SHA256 hash of file."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        return f"ERROR: {str(e)}"


def get_directory_size(path):
    """Calculate total size of directory in bytes."""
    total = 0
    try:
        for entry in Path(path).rglob('*'):
            if entry.is_file():
                total += entry.stat().st_size
    except Exception as e:
        return 0
    return total


def format_size(bytes_size):
    """Format bytes to human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f}{unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f}PB"


def capture_vps_state(vps_host, engagement_id, ssh_key=None):
    """Capture current state of VPS before engagement."""
    print(f"[+] Capturing VPS state: {vps_host}")

    # Build SSH command prefix with key if provided
    ssh_cmd = ["ssh"]
    if ssh_key:
        ssh_cmd.extend(["-i", ssh_key])

    vps_data = {
        "hostname": vps_host,
        "timestamp": datetime.now().isoformat(),
        "engagement_id": engagement_id
    }

    # 1. Disk usage
    print("  [*] Capturing disk usage...")
    try:
        result = subprocess.run(
            ssh_cmd + [vps_host, "du -sh /root /tmp /var/log /home 2>/dev/null"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            disk_usage = {}
            for line in result.stdout.strip().split('\n'):
                if line:
                    size, path = line.split('\t')
                    disk_usage[path] = size
            vps_data["disk_usage"] = disk_usage
            print(f"    [OK] Disk usage captured")
    except Exception as e:
        print(f"    [!] WARNING: Could not capture disk usage: {e}")
        vps_data["disk_usage"] = {}

    # 2. Bash history line count
    print("  [*] Capturing bash history...")
    try:
        result = subprocess.run(
            ssh_cmd + [vps_host, "wc -l ~/.bash_history"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            line_count = int(result.stdout.strip().split()[0])
            vps_data["bash_history_lines"] = line_count
            print(f"    [OK] Bash history: {line_count} lines")
    except Exception as e:
        print(f"    [!] WARNING: Could not capture bash history: {e}")
        vps_data["bash_history_lines"] = 0

    # 3. Critical config file hashes
    print("  [*] Capturing config file hashes...")
    critical_configs = [
        "/root/.bashrc",
        "/root/.bash_profile",
        "/etc/hosts",
        "/etc/resolv.conf",
        "/etc/ssh/sshd_config"
    ]

    config_hashes = {}
    for config_path in critical_configs:
        try:
            result = subprocess.run(
                ssh_cmd + [vps_host, f"sha256sum {config_path} 2>/dev/null"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                hash_value = result.stdout.strip().split()[0]
                config_hashes[config_path] = hash_value
                print(f"    [OK] {config_path}: {hash_value[:16]}...")
        except Exception as e:
            print(f"    [!] WARNING: Could not hash {config_path}: {e}")

    vps_data["critical_configs"] = config_hashes

    # 4. Docker containers
    print("  [*] Capturing Docker container state...")
    try:
        result = subprocess.run(
            ssh_cmd + [vps_host, "docker ps -a --format '{{.Names}}:{{.Status}}'"],
            capture_output=True,
            text=True,
            timeout=15
        )
        if result.returncode == 0:
            containers = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    name, status = line.split(':', 1)
                    containers.append({"name": name, "status": status})
            vps_data["docker_containers"] = containers
            print(f"    [OK] Docker containers: {len(containers)} found")
    except Exception as e:
        print(f"    [!] WARNING: Could not capture Docker state: {e}")
        vps_data["docker_containers"] = []

    # 5. Reaper database size (if exists)
    print("  [*] Checking Reaper database...")
    try:
        result = subprocess.run(
            ssh_cmd + [vps_host, "stat -c%s /root/reaper/reaper.db 2>/dev/null || echo 0"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            db_size = int(result.stdout.strip())
            vps_data["reaper_db_size"] = format_size(db_size)
            print(f"    [OK] Reaper DB size: {vps_data['reaper_db_size']}")
    except Exception as e:
        print(f"    [!] WARNING: Could not check Reaper database: {e}")
        vps_data["reaper_db_size"] = "0B"

    # 6. Open ports
    print("  [*] Capturing open ports...")
    try:
        result = subprocess.run(
            ssh_cmd + [vps_host, "netstat -tuln | grep LISTEN"],
            capture_output=True,
            text=True,
            timeout=15
        )
        if result.returncode == 0:
            open_ports = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split()
                    if len(parts) >= 4:
                        port = parts[3].split(':')[-1]
                        open_ports.append(port)
            vps_data["open_ports"] = sorted(set(open_ports))
            print(f"    [OK] Open ports: {len(vps_data['open_ports'])} found")
    except Exception as e:
        print(f"    [!] WARNING: Could not capture open ports: {e}")
        vps_data["open_ports"] = []

    # 7. Create backup of critical configs
    print("  [*] Creating config backups...")
    snapshot_dir = f"/root/.engagement-snapshots/{engagement_id}"
    try:
        # Create snapshot directory on VPS
        subprocess.run(
            ssh_cmd + [vps_host, f"mkdir -p {snapshot_dir}"],
            check=True,
            timeout=10
        )

        # Backup each critical config
        for config_path in critical_configs:
            filename = config_path.replace('/', '_')
            backup_cmd = f"cp {config_path} {snapshot_dir}/{filename}.backup 2>/dev/null || true"
            subprocess.run(
                ssh_cmd + [vps_host, backup_cmd],
                timeout=10
            )

        print(f"    [OK] Config backups saved to: {snapshot_dir}")
    except Exception as e:
        print(f"    [!] WARNING: Could not create config backups: {e}")

    # 8. Save snapshot JSON to VPS
    try:
        snapshot_json = json.dumps(vps_data, indent=2)
        snapshot_file = f"{snapshot_dir}/snapshot.json"

        # Write JSON via SSH
        subprocess.run(
            ssh_cmd + [vps_host, f"cat > {snapshot_file}"],
            input=snapshot_json,
            text=True,
            check=True,
            timeout=10
        )

        print(f"[+] VPS state captured successfully!")
        print(f"    Snapshot: {snapshot_file}")
    except Exception as e:
        print(f"[!] ERROR: Could not save VPS snapshot: {e}")
        return None

    return vps_data


def capture_local_state(engagement_dir, engagement_id):
    """Capture current state of local engagement directory."""
    print(f"\n[+] Capturing local state: {engagement_dir}")

    engagement_path = Path(engagement_dir)
    if not engagement_path.exists():
        print(f"[!] ERROR: Engagement directory does not exist: {engagement_dir}")
        return None

    local_data = {
        "engagement_dir": str(engagement_path.absolute()),
        "engagement_id": engagement_id,
        "timestamp": datetime.now().isoformat()
    }

    # 1. Total disk usage and file count
    print("  [*] Calculating disk usage...")
    total_size = get_directory_size(engagement_path)
    file_count = sum(1 for _ in engagement_path.rglob('*') if _.is_file())

    local_data["disk_usage"] = format_size(total_size)
    local_data["file_count"] = file_count
    print(f"    [OK] Size: {local_data['disk_usage']}, Files: {file_count}")

    # 2. Subdirectory breakdown
    print("  [*] Analyzing subdirectories...")
    subdirs = {}
    for subdir in engagement_path.iterdir():
        if subdir.is_dir() and not subdir.name.startswith('.'):
            size = get_directory_size(subdir)
            files = sum(1 for _ in subdir.rglob('*') if _.is_file())
            subdirs[subdir.name] = {
                "size": format_size(size),
                "files": files
            }
            print(f"    [OK] {subdir.name}: {format_size(size)} ({files} files)")

    local_data["subdirectories"] = subdirs

    # 3. Identify temporary files
    print("  [*] Identifying temporary files...")
    temp_patterns = ['*.tmp', '*.temp', '*-temp-*', '*.log']
    temp_files = []

    for pattern in temp_patterns:
        for temp_file in engagement_path.rglob(pattern):
            if temp_file.is_file():
                temp_files.append({
                    "path": str(temp_file.relative_to(engagement_path)),
                    "size": format_size(temp_file.stat().st_size)
                })

    local_data["temp_files"] = temp_files
    print(f"    [OK] Found {len(temp_files)} temporary files")

    # 4. Check for credentials file
    print("  [*] Checking for credentials...")
    creds_file = engagement_path / "creds.txt"
    if creds_file.exists():
        with open(creds_file, 'r', encoding='utf-8') as f:
            creds_lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        local_data["credentials_count"] = len(creds_lines)
        print(f"    [OK] Credentials file found: {len(creds_lines)} entries")
    else:
        local_data["credentials_count"] = 0
        print(f"    [!] WARNING: No credentials file found")

    # 5. Save snapshot to engagement directory
    snapshot_file = engagement_path / ".snapshot.json"
    try:
        with open(snapshot_file, 'w') as f:
            json.dump(local_data, f, indent=2)
        print(f"[+] Local state captured successfully!")
        print(f"    Snapshot: {snapshot_file}")
    except Exception as e:
        print(f"[!] ERROR: Could not save local snapshot: {e}")
        return None

    return local_data


def main():
    parser = argparse.ArgumentParser(
        description='Capture engagement state before testing begins'
    )
    parser.add_argument(
        '--engagement-dir',
        required=True,
        help='Path to engagement directory (local)'
    )
    parser.add_argument(
        '--vps',
        required=False,
        help='VPS SSH hostname (e.g., root@72.60.27.87)'
    )
    parser.add_argument(
        '--ssh-key',
        required=False,
        default=r"C:\Users\Chris\.ssh\gro_256",
        help='Path to SSH private key (default: C:\\Users\\Chris\\.ssh\\gro_256)'
    )
    parser.add_argument(
        '--local-only',
        action='store_true',
        help='Only capture local state (skip VPS)'
    )

    args = parser.parse_args()

    # Extract engagement ID from directory name
    engagement_id = Path(args.engagement_dir).name

    print("=" * 60)
    print("ENGAGEMENT STATE CAPTURE")
    print("=" * 60)
    print(f"Engagement: {engagement_id}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Capture VPS state (if requested)
    vps_success = True
    if not args.local_only and args.vps:
        vps_data = capture_vps_state(args.vps, engagement_id, args.ssh_key)
        if not vps_data:
            vps_success = False
            print("\n[!] WARNING: VPS state capture failed")

    # Capture local state
    local_data = capture_local_state(args.engagement_dir, engagement_id)
    if not local_data:
        print("\n[!] ERROR: Local state capture failed")
        sys.exit(1)

    # Summary
    print("\n" + "=" * 60)
    print("CAPTURE COMPLETE")
    print("=" * 60)

    if vps_success and args.vps:
        print("[OK] VPS state captured")
    if local_data:
        print("[OK] Local state captured")

    print("\nNext steps:")
    print("  1. Begin engagement testing")
    print("  2. After completion, generate cleanup plan:")
    print(f"     python skills/security-testing/scripts/security/generate-cleanup-plan.py {args.engagement_dir}")

    print("\n[!] IMPORTANT: Do NOT delete snapshot files during engagement!")


if __name__ == "__main__":
    main()
