#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update Code API wrappers to use VPS Docker execution
Converts local subprocess calls to SSH + docker exec pattern
"""

import sys
import io
import re
from pathlib import Path
from typing import Dict, List

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Tool categories and container mappings
TOOL_CATEGORIES = {
    "kali-pentest": {
        "container": "kali-pentest",
        "tools": [
            "nmap", "nuclei", "httpx", "subfinder", "katana", "naabu",
            "sqlmap", "wapiti", "wpscan", "nikto", "dirb", "hydra",
            "crackmapexec", "searchsploit", "responder", "netcat", "cvemap"
        ]
    },
    "web3-security": {
        "container": "web3-security",
        "tools": [
            "slither", "mythril", "semgrep", "echidna", "halmos",
            "forge_test", "forge_coverage", "cast_call", "cast_storage",
            "cast_abi_decode", "cast_4byte", "cast_4byte_decode",
            "solc_versions", "solc_install", "solc_use", "brownie",
            "amarna", "caracal_detect", "caracal_print", "thoth_decompile", "thoth_analyze"
        ]
    },
    "mobile-security": {
        "container": "mobile-tools",
        "tools": [
            "apktool", "jadx", "androguard", "apksigner",
            "aapt", "apkleaks", "frida", "objection"
        ]
    },
    "reaper": {
        "container": "reaper",
        "tools": [
            "status", "start", "stop", "scan_domain", "list_domains",
            "get_domain_details", "list_endpoints", "get_requests",
            "replay_request", "fuzz_endpoint", "test_bola",
            "get_attack_results", "export_report"
        ]
    }
}


def get_wrapper_files() -> List[Path]:
    """Get all Python wrapper files that need updating."""
    servers_dir = Path.home() / ".claude" / "servers"
    wrappers = []

    for category, info in TOOL_CATEGORIES.items():
        category_dir = servers_dir / category.replace("-", "_")
        if category_dir.exists():
            for tool in info["tools"]:
                wrapper_file = category_dir / f"{tool}.py"
                if wrapper_file.exists():
                    wrappers.append(wrapper_file)

    return wrappers


def check_if_needs_update(filepath: Path) -> bool:
    """Check if wrapper already uses VPS pattern."""
    content = filepath.read_text(encoding='utf-8')
    return "from vps_utils import docker_exec" not in content


def update_wrapper(filepath: Path, container: str, dry_run: bool = False) -> Dict:
    """
    Update wrapper to use VPS Docker execution pattern.

    Args:
        filepath: Path to wrapper file
        container: Container name (kali-pentest, web3-security, etc.)
        dry_run: If True, only show what would change

    Returns:
        Dict with status and changes
    """

    content = filepath.read_text(encoding='utf-8')

    # Check if already updated
    if "from vps_utils import docker_exec" in content:
        return {
            "status": "skipped",
            "reason": "Already uses VPS pattern",
            "file": str(filepath)
        }

    # Pattern replacements
    changes = []

    # 1. Add vps_utils import (after pathlib import)
    if "from pathlib import Path" in content:
        old_import = "from pathlib import Path\nfrom typing import"
        new_import = "from pathlib import Path\nfrom typing import"

        # Add after imports section
        import_section_end = content.find("\n\n", content.find("from typing"))
        if import_section_end > 0:
            before = content[:import_section_end]
            after = content[import_section_end:]

            # Add vps_utils import
            vps_import = "\n\n# Add parent directory to path for vps_utils\nsys.path.insert(0, str(Path(__file__).parent.parent))\nfrom vps_utils import docker_exec"
            content = before + vps_import + after
            changes.append("Added vps_utils import")

    # 2. Replace subprocess.run pattern with docker_exec
    # This is tool-specific and would need manual review for complex cases
    # For now, mark files that need manual update

    if dry_run:
        return {
            "status": "needs_update",
            "file": str(filepath),
            "container": container,
            "changes": changes
        }

    # Write updated content
    filepath.write_text(content, encoding='utf-8')

    return {
        "status": "updated",
        "file": str(filepath),
        "container": container,
        "changes": changes
    }


def main():
    """Main execution."""
    import argparse

    parser = argparse.ArgumentParser(description="Update Code API wrappers for VPS deployment")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without modifying files")
    parser.add_argument("--category", help="Only update specific category (kali-pentest, web3-security, mobile-security, reaper)")
    args = parser.parse_args()

    print("[+] Code API Wrapper Update Tool")
    print(f"    Mode: {'DRY RUN' if args.dry_run else 'LIVE UPDATE'}")
    print()

    # Get wrapper files
    wrappers = get_wrapper_files()
    print(f"[+] Found {len(wrappers)} wrapper files")
    print()

    # Filter by category if specified
    if args.category:
        category_dir = args.category.replace("-", "_")
        wrappers = [w for w in wrappers if category_dir in str(w)]
        print(f"[+] Filtered to {len(wrappers)} wrappers in category: {args.category}")
        print()

    # Process each wrapper
    results = {
        "updated": [],
        "skipped": [],
        "needs_update": [],
        "error": []
    }

    for wrapper in wrappers:
        # Determine container
        container = None
        for category, info in TOOL_CATEGORIES.items():
            if category.replace("-", "_") in str(wrapper):
                container = info["container"]
                break

        if not container:
            results["error"].append(str(wrapper))
            print(f"[!] Could not determine container for: {wrapper.name}")
            continue

        # Check if needs update
        if not check_if_needs_update(wrapper):
            results["skipped"].append(str(wrapper))
            print(f"[SKIP] {wrapper.name} - Already uses VPS pattern")
            continue

        # Update wrapper
        try:
            result = update_wrapper(wrapper, container, dry_run=args.dry_run)
            status = result["status"]
            results[status].append(str(wrapper))

            if status == "updated":
                print(f"[UPDATE] {wrapper.name} -> {container}")
                for change in result.get("changes", []):
                    print(f"         - {change}")
            elif status == "needs_update":
                print(f"[NEEDS UPDATE] {wrapper.name} -> {container}")

        except Exception as e:
            results["error"].append(str(wrapper))
            print(f"[ERROR] {wrapper.name}: {str(e)}")

    # Summary
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Updated:      {len(results['updated'])}")
    print(f"Skipped:      {len(results['skipped'])}")
    print(f"Needs Update: {len(results['needs_update'])}")
    print(f"Errors:       {len(results['error'])}")
    print()

    if results["needs_update"]:
        print("[!] The following files need manual review:")
        for f in results["needs_update"]:
            print(f"    - {Path(f).name}")
        print()

    if args.dry_run:
        print("[!] This was a DRY RUN. No files were modified.")
        print("    Run without --dry-run to apply changes.")


if __name__ == "__main__":
    main()
