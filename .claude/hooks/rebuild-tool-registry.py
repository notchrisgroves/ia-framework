#!/usr/bin/env python3
"""
Rebuild Tool Registry Hook

Trigger: SessionStart (every new session) OR /refresh-tools command
Purpose: Auto-scan tools/ and servers/ folders, rebuild TOOL-REGISTRY.yaml
Output: Updated registry + validation report
"""

import json
import sys
import io
import yaml
from pathlib import Path
from datetime import datetime

# Ensure UTF-8 encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def scan_for_manifests(base_dir: str) -> list:
    """Scan directory for manifest.yaml files."""
    manifests = []
    base_path = Path(base_dir)

    if not base_path.exists():
        return manifests

    for manifest_path in base_path.rglob("manifest.yaml"):
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest_data = yaml.safe_load(f)
                manifests.append((manifest_path, manifest_data))
        except Exception as e:
            print(f"WARNING: Failed to load {manifest_path}: {e}", file=sys.stderr)

    return manifests


def find_rogue_files(base_dir: str, valid_tool_dirs: set) -> list:
    """Find executable files (.py, .ts, .sh) NOT in valid tool directories."""
    rogue_files = []
    base_path = Path(base_dir)

    if not base_path.exists():
        return rogue_files

    # Find all executable files
    for ext in ['*.py', '*.ts', '*.sh', '*.ps1']:
        for file_path in base_path.rglob(ext):
            # Skip if in valid tool directory
            if any(str(file_path).startswith(str(tool_dir)) for tool_dir in valid_tool_dirs):
                continue

            # Skip if it's a test file
            if '/tests/' in str(file_path) or 'test_' in file_path.name.lower():
                continue

            # Skip if it's in node_modules or __pycache__
            if 'node_modules' in str(file_path) or '__pycache__' in str(file_path):
                continue

            # Skip manifest files themselves
            if file_path.name == 'manifest.yaml':
                continue

            rogue_files.append(file_path)

    return rogue_files


def build_registry_entry(manifest_path: Path, manifest_data: dict) -> dict:
    """Convert manifest to registry entry."""

    tool_type = manifest_data.get('type', 'tool')

    entry = {
        'name': manifest_data['name'],
        'path': str(manifest_path.parent).replace('\\', '/'),
        'type': tool_type,
        'category': manifest_data['category'],
        'subcategory': manifest_data.get('subcategory', ''),
        'description': manifest_data['description'],
        'version': manifest_data.get('version', '1.0'),
        'capabilities': manifest_data.get('capabilities', []),
        'keywords': manifest_data.get('keywords', []),
        'usage': manifest_data.get('usage', ''),
        'vps_required': manifest_data.get('vps_required', False),
        'language': manifest_data.get('language', 'unknown'),
        'last_updated': manifest_data.get('last_updated', 'unknown')
    }

    # Add executable path (relative to tool directory)
    if tool_type == 'tool':
        executable = manifest_data.get('executable', f"{manifest_data['name']}.py")
        entry['executable'] = str(manifest_path.parent / executable).replace('\\', '/')

    # Add endpoints for servers
    if tool_type == 'server':
        entry['endpoints'] = manifest_data.get('endpoints', [])
        entry['vps_location'] = manifest_data.get('vps_location', 'unknown')

    return entry


def rebuild_registry():
    """Rebuild TOOL-REGISTRY.yaml from manifests."""

    print("🔄 Scanning for tools and servers...", file=sys.stderr)

    # Scan both directories
    tool_manifests = scan_for_manifests("tools")
    server_manifests = scan_for_manifests("servers")

    all_manifests = tool_manifests + server_manifests

    print(f"✅ Found {len(tool_manifests)} tools and {len(server_manifests)} servers", file=sys.stderr)

    # Build registry entries
    registry_entries = []
    valid_tool_dirs = set()

    for manifest_path, manifest_data in all_manifests:
        try:
            entry = build_registry_entry(manifest_path, manifest_data)
            registry_entries.append(entry)
            valid_tool_dirs.add(manifest_path.parent)
        except Exception as e:
            print(f"WARNING: Failed to process {manifest_path}: {e}", file=sys.stderr)

    # Sort by category, then name
    registry_entries.sort(key=lambda x: (x['category'], x['name']))

    # Find rogue files
    rogue_files_tools = find_rogue_files("tools", valid_tool_dirs)
    rogue_files_servers = find_rogue_files("servers", valid_tool_dirs)
    all_rogue_files = rogue_files_tools + rogue_files_servers

    # Build registry YAML
    registry = {
        'version': '1.0',
        'generated': datetime.now().isoformat(),
        'total_tools': len(tool_manifests),
        'total_servers': len(server_manifests),
        'tools': registry_entries
    }

    # Write to file
    registry_path = Path("library/catalogs/TOOL-REGISTRY.yaml")
    registry_path.parent.mkdir(parents=True, exist_ok=True)

    with open(registry_path, 'w', encoding='utf-8') as f:
        yaml.dump(registry, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"✅ Registry updated: {registry_path}", file=sys.stderr)

    # Report rogue files
    if all_rogue_files:
        print(f"\n⚠️  WARNING: Found {len(all_rogue_files)} rogue files (no manifest):", file=sys.stderr)
        for rogue in all_rogue_files[:10]:  # Show first 10
            print(f"   - {rogue}", file=sys.stderr)
        if len(all_rogue_files) > 10:
            print(f"   ... and {len(all_rogue_files) - 10} more", file=sys.stderr)

    # Output system-reminder for user
    output = f"""<system-reminder type="registry-update">
✅ Tool Registry Rebuilt

**Stats:**
- Tools found: {len(tool_manifests)}
- Servers found: {len(server_manifests)}
- Registry updated: library/catalogs/TOOL-REGISTRY.yaml

**Validation:**
- Rogue files detected: {len(all_rogue_files)}
</system-reminder>"""

    print(output)


def main():
    """Main hook execution."""
    try:
        # Read hook data from stdin (if provided)
        try:
            data = json.load(sys.stdin)
        except:
            data = {}  # Manual execution

        rebuild_registry()
        sys.exit(0)
    except Exception as e:
        # Fail gracefully - registry rebuild is non-critical
        print(f"WARNING: Registry rebuild failed: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
