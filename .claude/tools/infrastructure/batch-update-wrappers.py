#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Update Code API Wrappers for VPS Deployment
Transforms local subprocess calls to SSH + docker exec pattern
"""

import sys
import io
from pathlib import Path
import re

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Container mappings
CONTAINER_MAP = {
    "kali-pentest": "kali-pentest",
    "web3-security": "web3-security",
    "mobile-security": "mobile-tools",
}

def detect_container(filepath: Path) -> str:
    """Detect which container this wrapper belongs to"""
    path_str = str(filepath)
    if "kali-pentest" in path_str or "kali_pentest" in path_str:
        return "kali-pentest"
    elif "web3-security" in path_str or "web3_security" in path_str:
        return "web3-security"
    elif "mobile-security" in path_str or "mobile_security" in path_str or "mobile-tools" in path_str:
        return "mobile-tools"
    return None

def already_updated(content: str) -> bool:
    """Check if wrapper already uses VPS pattern"""
    return "from vps_utils import docker_exec" in content

def update_wrapper(filepath: Path, dry_run: bool = False) -> dict:
    """
    Update wrapper to use VPS Docker execution pattern

    Returns:
        dict with status and changes
    """

    container = detect_container(filepath)
    if not container:
        return {
            "status": "skipped",
            "reason": "Could not determine container",
            "file": str(filepath)
        }

    content = filepath.read_text(encoding='utf-8')

    if already_updated(content):
        return {
            "status": "skipped",
            "reason": "Already uses VPS pattern",
            "file": str(filepath)
        }

    changes = []
    original_content = content

    # 1. Add vps_utils import after other imports
    if "import subprocess" in content:
        # Remove subprocess import
        content = re.sub(r'^import subprocess\n', '', content, flags=re.MULTILINE)
        changes.append("Removed subprocess import")

    # Find the position after imports to add vps_utils
    import_section_end = 0
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('from typing import') or line.startswith('import '):
            import_section_end = i

    if import_section_end > 0:
        # Insert vps_utils import after imports
        lines.insert(import_section_end + 1, "")
        lines.insert(import_section_end + 2, "# Add parent directory to path for vps_utils")
        lines.insert(import_section_end + 3, "sys.path.insert(0, str(Path(__file__).parent.parent))")
        lines.insert(import_section_end + 4, "from vps_utils import docker_exec")
        content = '\n'.join(lines)
        changes.append("Added vps_utils import")

    # 2. Replace subprocess.run pattern with docker_exec
    # Pattern: subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=X)
    # Replace with: docker_exec(container, cmd, timeout=X)

    # Find subprocess.run calls
    subprocess_pattern = r'result\s*=\s*subprocess\.run\s*\(\s*([^,]+),\s*shell=True,\s*capture_output=True,\s*text=True(?:,\s*timeout=(\d+))?\s*\)'

    def replace_subprocess(match):
        cmd_var = match.group(1).strip()
        timeout = match.group(2) if match.group(2) else "300"
        return f'result = docker_exec("{container}", {cmd_var}, timeout={timeout})'

    new_content = re.sub(subprocess_pattern, replace_subprocess, content)
    if new_content != content:
        content = new_content
        changes.append("Replaced subprocess.run with docker_exec")

    # 3. Update error handling - change result.returncode to result["returncode"]
    content = re.sub(r'result\.returncode', 'result["returncode"]', content)
    content = re.sub(r'result\.stdout', 'result["stdout"]', content)
    content = re.sub(r'result\.stderr', 'result["stderr"]', content)
    if "result[" in content and "result." in original_content:
        changes.append("Updated result access to dict notation")

    # 4. Update docstring to mention VPS
    content = re.sub(
        r'"""([^"]+)wrapper - MCP Code API Pattern',
        r'"""\1wrapper - MCP Code API Pattern (VPS Docker deployment)',
        content
    )

    if dry_run:
        return {
            "status": "would_update",
            "file": str(filepath),
            "container": container,
            "changes": changes
        }

    # Write updated content
    if content != original_content:
        filepath.write_text(content, encoding='utf-8')
        return {
            "status": "updated",
            "file": str(filepath),
            "container": container,
            "changes": changes
        }
    else:
        return {
            "status": "no_changes_needed",
            "file": str(filepath)
        }

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Batch update Code API wrappers for VPS deployment")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without modifying files")
    parser.add_argument("--category", help="Only update specific category (kali-pentest, web3-security, mobile-security)")
    args = parser.parse_args()

    print("[+] Batch Wrapper Update Tool")
    print(f"    Mode: {'DRY RUN' if args.dry_run else 'LIVE UPDATE'}")
    print()

    # Get all wrapper files
    servers_dir = Path.home() / ".claude" / "servers"

    categories = []
    if args.category:
        categories = [args.category]
    else:
        categories = ["kali-pentest", "web3-security", "mobile-security"]

    wrappers = []
    for cat in categories:
        cat_dir = servers_dir / cat
        if cat_dir.exists():
            for py_file in cat_dir.glob("*.py"):
                if py_file.name not in ["__init__.py", "index.py"]:
                    wrappers.append(py_file)

    print(f"[+] Found {len(wrappers)} wrapper files")
    print()

    results = {
        "updated": [],
        "would_update": [],
        "skipped": [],
        "no_changes_needed": [],
        "error": []
    }

    for wrapper in wrappers:
        try:
            result = update_wrapper(wrapper, dry_run=args.dry_run)
            status = result["status"]
            results[status].append(wrapper.name)

            if status in ["updated", "would_update"]:
                prefix = "[WOULD UPDATE]" if args.dry_run else "[UPDATED]"
                print(f"{prefix} {wrapper.name} -> {result.get('container', 'unknown')}")
                for change in result.get("changes", []):
                    print(f"           - {change}")
            elif status == "skipped":
                print(f"[SKIP] {wrapper.name} - {result.get('reason', 'Unknown')}")

        except Exception as e:
            results["error"].append(wrapper.name)
            print(f"[ERROR] {wrapper.name}: {str(e)}")

    # Summary
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    if args.dry_run:
        print(f"Would Update: {len(results['would_update'])}")
    else:
        print(f"Updated:      {len(results['updated'])}")
    print(f"Skipped:      {len(results['skipped'])}")
    print(f"No Changes:   {len(results['no_changes_needed'])}")
    print(f"Errors:       {len(results['error'])}")
    print()

    if args.dry_run:
        print("[!] This was a DRY RUN. No files were modified.")
        print("    Run without --dry-run to apply changes.")

if __name__ == "__main__":
    main()
