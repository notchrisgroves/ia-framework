#!/usr/bin/env python3
"""
Tool Structure Validation Hook

Trigger: Pre-commit OR /validate-tools command
Purpose: Enforce tool structure rules, block commits with violations
Exit: 0 = valid, 1 = violations found (blocks commit)
"""

import sys
import io
import yaml
from pathlib import Path

# Ensure UTF-8 encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

REQUIRED_MANIFEST_FIELDS = [
    'type', 'name', 'description', 'category', 'capabilities', 'keywords'
]


def validate_manifest(manifest_path: Path) -> list:
    """Validate manifest.yaml structure. Returns list of errors."""
    errors = []

    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = yaml.safe_load(f)
    except Exception as e:
        return [f"Invalid YAML: {e}"]

    # Check required fields
    for field in REQUIRED_MANIFEST_FIELDS:
        if field not in manifest:
            errors.append(f"Missing required field: {field}")

    # Validate type
    if manifest.get('type') not in ['tool', 'server']:
        errors.append(f"Invalid type: {manifest.get('type')} (must be 'tool' or 'server')")

    # Check capabilities is list
    if not isinstance(manifest.get('capabilities', []), list):
        errors.append("capabilities must be a list")

    # Check keywords is list
    if not isinstance(manifest.get('keywords', []), list):
        errors.append("keywords must be a list")

    return errors


def validate_tool_structure(tool_dir: Path) -> list:
    """Validate tool directory structure. Returns list of violations."""
    violations = []

    # Check manifest exists
    manifest_path = tool_dir / "manifest.yaml"
    if not manifest_path.exists():
        violations.append(f"Missing manifest.yaml in {tool_dir}")
        return violations  # Can't validate further

    # Validate manifest content
    manifest_errors = validate_manifest(manifest_path)
    violations.extend([f"{tool_dir.name}: {err}" for err in manifest_errors])

    # Check README exists
    readme_path = tool_dir / "README.md"
    if not readme_path.exists():
        violations.append(f"Missing README.md in {tool_dir}")

    # Load manifest to check executable
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = yaml.safe_load(f)

        if manifest.get('type') == 'tool':
            # Check executable exists
            executable = manifest.get('executable', f"{manifest['name']}.py")
            exec_path = tool_dir / executable

            if not exec_path.exists():
                violations.append(f"Executable not found: {exec_path}")
    except:
        pass  # Already reported manifest errors

    return violations


def find_and_validate_all_tools():
    """Find and validate all tools and servers."""

    all_violations = []

    # Validate tools/
    tools_dir = Path("tools")
    if tools_dir.exists():
        for category_dir in tools_dir.iterdir():
            if not category_dir.is_dir():
                continue

            for tool_dir in category_dir.iterdir():
                if not tool_dir.is_dir():
                    all_violations.append(f"Rogue file in tools/{category_dir.name}/: {tool_dir.name}")
                    continue

                violations = validate_tool_structure(tool_dir)
                all_violations.extend(violations)

    # Validate servers/
    servers_dir = Path("servers")
    if servers_dir.exists():
        for server_dir in servers_dir.iterdir():
            if not server_dir.is_dir():
                all_violations.append(f"Rogue file in servers/: {server_dir.name}")
                continue

            violations = validate_tool_structure(server_dir)
            all_violations.extend(violations)

    return all_violations


def main():
    """Main validation execution."""

    print("🔍 Validating tool structure...", file=sys.stderr)

    violations = find_and_validate_all_tools()

    if violations:
        print(f"\n❌ VALIDATION FAILED - {len(violations)} violations found:\n", file=sys.stderr)
        for v in violations:
            print(f"  - {v}", file=sys.stderr)
        print("\n💡 Fix these issues before committing", file=sys.stderr)
        sys.exit(1)
    else:
        print("✅ All tools valid - structure compliance verified", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
