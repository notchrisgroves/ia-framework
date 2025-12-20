#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Engagement Cleanup Plan Generator
Analyzes engagement state changes and generates cleanup recommendations.

Usage:
    python tools/security/generate-cleanup-plan.py \\
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
from pathlib import Path
from datetime import datetime
import argparse

# Force UTF-8 encoding for Windows console output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def format_size(bytes_size):
    """Format bytes to human-readable size."""
    if isinstance(bytes_size, str):
        return bytes_size

    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f}{unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f}PB"


def parse_size(size_str):
    """Convert human-readable size to bytes."""
    if isinstance(size_str, int):
        return size_str

    units = {'B': 1, 'KB': 1024, 'MB': 1024**2, 'GB': 1024**3, 'TB': 1024**4}
    size_str = size_str.strip().upper()

    for unit, multiplier in units.items():
        if size_str.endswith(unit):
            try:
                number = float(size_str[:-len(unit)])
                return int(number * multiplier)
            except:
                return 0
    return 0


def analyze_vps_changes(vps_host, engagement_id, snapshot, ssh_key=None):
    """Analyze VPS changes since snapshot."""
    print(f"[+] Analyzing VPS changes: {vps_host}")

    # Build SSH command prefix with key if provided
    ssh_cmd = ["ssh"]
    if ssh_key:
        ssh_cmd.extend(["-i", ssh_key])

    changes = {
        "delete_files": [],
        "restore_configs": [],
        "clean_bash_history": {},
        "clean_reaper_db": {},
        "space_savings": 0
    }

    # 1. Check bash history growth
    print("  [*] Checking bash history...")
    try:
        result = subprocess.run(
            ssh_cmd + [vps_host, "wc -l ~/.bash_history"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            current_lines = int(result.stdout.strip().split()[0])
            snapshot_lines = snapshot.get("bash_history_lines", 0)
            new_lines = current_lines - snapshot_lines

            if new_lines > 0:
                changes["clean_bash_history"] = {
                    "total_lines": current_lines,
                    "engagement_lines": new_lines,
                    "action": f"Remove lines {snapshot_lines + 1}-{current_lines}"
                }
                print(f"    [!] {new_lines} new bash history lines to remove")
    except Exception as e:
        print(f"    [!] WARNING: Could not check bash history: {e}")

    # 2. Check for modified configs
    print("  [*] Checking config file changes...")
    critical_configs = snapshot.get("critical_configs", {})

    for config_path, original_hash in critical_configs.items():
        try:
            result = subprocess.run(
                ssh_cmd + [vps_host, f"sha256sum {config_path} 2>/dev/null"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                current_hash = result.stdout.strip().split()[0]
                if current_hash != original_hash:
                    snapshot_dir = f"/root/.engagement-snapshots/{engagement_id}"
                    filename = config_path.replace('/', '_')
                    backup_path = f"{snapshot_dir}/{filename}.backup"

                    changes["restore_configs"].append({
                        "path": config_path,
                        "backup": backup_path,
                        "changed": True
                    })
                    print(f"    [!] {config_path} was modified - will restore")
        except Exception as e:
            print(f"    [!] WARNING: Could not check {config_path}: {e}")

    # 3. Find temporary files (heuristic-based)
    print("  [*] Searching for temporary files...")
    temp_patterns = [
        "/tmp/*scan*",
        "/tmp/*temp*",
        "/root/tools/*exploit*.py",
        "/root/.cookies/*",
        "*.tmp"
    ]

    for pattern in temp_patterns:
        try:
            result = subprocess.run(
                ssh_cmd + [vps_host, f"find /root /tmp -type f -name '{pattern.split('/')[-1]}' 2>/dev/null | head -20"],
                capture_output=True,
                text=True,
                timeout=15
            )
            if result.returncode == 0:
                for file_path in result.stdout.strip().split('\n'):
                    if file_path:
                        # Get file size
                        size_result = subprocess.run(
                            ssh_cmd + [vps_host, f"stat -c%s {file_path} 2>/dev/null"],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        if size_result.returncode == 0:
                            size = int(size_result.stdout.strip())
                            changes["delete_files"].append({
                                "path": file_path,
                                "size": format_size(size),
                                "secure": ".cookie" in file_path or "cred" in file_path.lower()
                            })
                            changes["space_savings"] += size
        except Exception as e:
            print(f"    [!] WARNING: Error searching for {pattern}: {e}")

    # 4. Check Reaper database growth
    print("  [*] Checking Reaper database...")
    try:
        result = subprocess.run(
            ssh_cmd + [vps_host, "stat -c%s /root/reaper/reaper.db 2>/dev/null || echo 0"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            current_size = int(result.stdout.strip())
            snapshot_size = parse_size(snapshot.get("reaper_db_size", "0B"))

            if current_size > snapshot_size:
                growth = current_size - snapshot_size
                changes["clean_reaper_db"] = {
                    "size_before": format_size(current_size),
                    "size_after_estimated": format_size(snapshot_size),
                    "growth": format_size(growth),
                    "action": f"Delete requests for engagement hostnames"
                }
                changes["space_savings"] += growth
                print(f"    [!] Reaper DB grew by {format_size(growth)}")
    except Exception as e:
        print(f"    [!] WARNING: Could not check Reaper database: {e}")

    print(f"  [OK] VPS analysis complete - {format_size(changes['space_savings'])} can be reclaimed")
    return changes


def analyze_local_changes(engagement_dir, snapshot):
    """Analyze local engagement directory changes."""
    print(f"\n[+] Analyzing local changes: {engagement_dir}")

    engagement_path = Path(engagement_dir)
    changes = {
        "archive_large_files": [],
        "compress_engagement": {},
        "delete_temp_files": [],
        "space_savings": 0
    }

    # 1. Find large scan output directories
    print("  [*] Identifying large directories...")
    large_dirs = [
        "03-vulnerability-assessment/scan-outputs",
        "03-vulnerability-assessment/reaper-traffic",
        "02-reconnaissance/subdomain-scans"
    ]

    for dir_name in large_dirs:
        dir_path = engagement_path / dir_name
        if dir_path.exists():
            total_size = sum(f.stat().st_size for f in dir_path.rglob('*') if f.is_file())
            if total_size > 10 * 1024 * 1024:  # > 10MB
                changes["archive_large_files"].append({
                    "path": dir_name,
                    "size": format_size(total_size)
                })
                # Assume 60% compression ratio
                changes["space_savings"] += int(total_size * 0.6)
                print(f"    [!] {dir_name}: {format_size(total_size)} (will archive)")

    # 2. Calculate engagement compression
    print("  [*] Calculating compression potential...")
    total_size = sum(f.stat().st_size for f in engagement_path.rglob('*') if f.is_file())
    estimated_archive_size = int(total_size * 0.4)  # 60% compression ratio

    changes["compress_engagement"] = {
        "source": engagement_path.name,
        "archive": f"{engagement_path.name}.tar.gz",
        "compression_ratio_estimated": "60%",
        "size_before": format_size(total_size),
        "size_after_estimated": format_size(estimated_archive_size)
    }
    changes["space_savings"] += (total_size - estimated_archive_size)

    # 3. Find temporary files
    print("  [*] Finding temporary files...")
    temp_patterns = ['*.tmp', '*.temp', '*-temp-*']
    temp_size = 0
    temp_count = 0

    for pattern in temp_patterns:
        for temp_file in engagement_path.rglob(pattern):
            if temp_file.is_file():
                size = temp_file.stat().st_size
                temp_size += size
                temp_count += 1

    if temp_count > 0:
        changes["delete_temp_files"] = [{
            "pattern": "*.tmp, *.temp, *-temp-*",
            "count": temp_count,
            "size": format_size(temp_size)
        }]
        print(f"    [!] {temp_count} temporary files: {format_size(temp_size)}")

    print(f"  [OK] Local analysis complete - {format_size(changes['space_savings'])} can be reclaimed")
    return changes


def print_cleanup_plan(engagement_id, vps_changes, local_changes):
    """Print interactive cleanup plan."""
    total_savings = vps_changes["space_savings"] + local_changes["space_savings"]

    print("\n" + "=" * 70)
    print("ENGAGEMENT CLEANUP PLAN".center(70))
    print("=" * 70)
    print(f"\nEngagement: {engagement_id}")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # VPS Cleanup
    print("\n" + "-" * 70)
    print("VPS CLEANUP")
    print("-" * 70)

    if vps_changes["delete_files"]:
        print(f"\n[DELETE] {len(vps_changes['delete_files'])} temporary files:")
        for item in vps_changes["delete_files"][:5]:  # Show first 5
            secure_flag = " (SECURE DELETE)" if item["secure"] else ""
            print(f"  - {item['path']} ({item['size']}){secure_flag}")
        if len(vps_changes["delete_files"]) > 5:
            print(f"  ... and {len(vps_changes['delete_files']) - 5} more files")

    if vps_changes["restore_configs"]:
        print(f"\n[RESTORE] {len(vps_changes['restore_configs'])} modified config files:")
        for item in vps_changes["restore_configs"]:
            print(f"  - {item['path']}")

    if vps_changes["clean_bash_history"]:
        hist = vps_changes["clean_bash_history"]
        print(f"\n[CLEAN] Bash history:")
        print(f"  - Remove {hist['engagement_lines']} lines (lines {hist['action'].split()[-1]})")

    if vps_changes["clean_reaper_db"]:
        reaper = vps_changes["clean_reaper_db"]
        print(f"\n[CLEAN] Reaper database:")
        print(f"  - Size: {reaper['size_before']} → {reaper['size_after_estimated']}")
        print(f"  - Growth: {reaper['growth']}")

    print(f"\nVPS Space Savings: ~{format_size(vps_changes['space_savings'])}")

    # Local Cleanup
    print("\n" + "-" * 70)
    print("LOCAL CLEANUP")
    print("-" * 70)

    if local_changes["archive_large_files"]:
        print(f"\n[ARCHIVE] {len(local_changes['archive_large_files'])} large directories:")
        for item in local_changes["archive_large_files"]:
            print(f"  - {item['path']} ({item['size']})")

    if local_changes["compress_engagement"]:
        comp = local_changes["compress_engagement"]
        print(f"\n[COMPRESS] Engagement directory:")
        print(f"  - {comp['size_before']} → {comp['size_after_estimated']} ({comp['compression_ratio_estimated']} reduction)")
        print(f"  - Archive: {comp['archive']}")

    if local_changes["delete_temp_files"]:
        for item in local_changes["delete_temp_files"]:
            print(f"\n[DELETE] Temporary files:")
            print(f"  - {item['count']} files ({item['size']})")

    print(f"\nLocal Space Savings: ~{format_size(local_changes['space_savings'])}")

    # Total Summary
    print("\n" + "=" * 70)
    print(f"TOTAL SPACE SAVINGS: ~{format_size(total_savings)}")
    print("=" * 70)

    print("\nOptions:")
    print("  [1] Execute full cleanup (recommended)")
    print("  [2] VPS cleanup only")
    print("  [3] Local cleanup only")
    print("  [4] Save plan and exit (manual execution later)")
    print("  [5] Cancel (no cleanup)")


def save_cleanup_plan(engagement_dir, engagement_id, vps_changes, local_changes):
    """Save cleanup plan to JSON file."""
    plan = {
        "engagement_id": engagement_id,
        "generated": datetime.now().isoformat(),
        "vps": vps_changes,
        "local": local_changes,
        "total_savings_bytes": vps_changes["space_savings"] + local_changes["space_savings"]
    }

    plan_file = Path(engagement_dir) / ".cleanup-plan.json"
    with open(plan_file, 'w') as f:
        json.dump(plan, f, indent=2)

    print(f"\n[OK] Cleanup plan saved to: {plan_file}")
    return plan_file


def main():
    parser = argparse.ArgumentParser(
        description='Generate engagement cleanup plan'
    )
    parser.add_argument(
        '--engagement-dir',
        required=True,
        help='Path to engagement directory'
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
        help='Only analyze local changes (skip VPS)'
    )

    args = parser.parse_args()

    engagement_path = Path(args.engagement_dir)
    engagement_id = engagement_path.name

    # Load local snapshot
    snapshot_file = engagement_path / ".snapshot.json"
    if not snapshot_file.exists():
        print(f"[!] ERROR: Snapshot file not found: {snapshot_file}")
        print("    Run capture-engagement-state.py before cleanup")
        sys.exit(1)

    with open(snapshot_file, 'r') as f:
        local_snapshot = json.load(f)

    # Load VPS snapshot
    vps_snapshot = {}
    if not args.local_only and args.vps:
        # Build SSH command with key
        ssh_cmd = ["ssh"]
        if args.ssh_key:
            ssh_cmd.extend(["-i", args.ssh_key])

        snapshot_dir = f"/root/.engagement-snapshots/{engagement_id}"
        try:
            result = subprocess.run(
                ssh_cmd + [args.vps, f"cat {snapshot_dir}/snapshot.json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                vps_snapshot = json.loads(result.stdout)
        except Exception as e:
            print(f"[!] WARNING: Could not load VPS snapshot: {e}")

    # Analyze changes
    vps_changes = {"space_savings": 0}
    if vps_snapshot and args.vps:
        vps_changes = analyze_vps_changes(args.vps, engagement_id, vps_snapshot, args.ssh_key)

    local_changes = analyze_local_changes(args.engagement_dir, local_snapshot)

    # Print plan
    print_cleanup_plan(engagement_id, vps_changes, local_changes)

    # Save plan
    plan_file = save_cleanup_plan(args.engagement_dir, engagement_id, vps_changes, local_changes)

    print("\nNext steps:")
    print("  1. Review cleanup plan above")
    print("  2. Execute cleanup manually using the plan file:")
    print(f"     Plan saved to: {plan_file}")
    print("  3. Follow VPS and local cleanup commands in the plan")


if __name__ == "__main__":
    main()
