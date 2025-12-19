#!/usr/bin/env python3
"""
YAML Frontmatter Validation - Component Metadata Enforcement

Validates that commands and skills have required YAML frontmatter fields.
Ensures components are properly structured and discoverable.

**Why This Matters:**
Missing frontmatter breaks component discovery and command detection.

**Enforcement:**
- Pre-commit hook: Blocks commits with invalid frontmatter
- Manual validation: Run before releases

See: docs/DOCUMENTATION-STANDARDS-ENFORCEMENT.md
"""

import re
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Required fields for each component type
COMMAND_REQUIRED_FIELDS = ['name', 'description']
SKILL_MANIFEST_REQUIRED_FIELDS = ['name', 'type', 'description']

# Deprecated fields that should NOT be in frontmatter
COMMAND_DEPRECATED_FIELDS = ['agent', 'skill', 'complexity', 'version']

def extract_yaml_frontmatter(file_path: Path) -> Optional[Dict]:
    """
    Extract YAML frontmatter from markdown file.

    Frontmatter format:
    ---
    name: command-name
    description: Brief description
    ---

    Returns:
        Dictionary of frontmatter fields, or None if no frontmatter found
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
        return None

    # Match YAML frontmatter between --- delimiters
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return None

    frontmatter_text = match.group(1)

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        return frontmatter if frontmatter else {}
    except yaml.YAMLError as e:
        print(f"Warning: Invalid YAML in {file_path}: {e}", file=sys.stderr)
        return None

def validate_command_frontmatter(file_path: Path) -> List[str]:
    """
    Validate command file frontmatter.

    Returns:
        List of violation messages (empty if valid)
    """
    violations = []

    frontmatter = extract_yaml_frontmatter(file_path)

    # Check if frontmatter exists
    if frontmatter is None:
        violations.append("Missing YAML frontmatter (must have --- delimiters)")
        return violations

    # Check required fields
    for field in COMMAND_REQUIRED_FIELDS:
        if field not in frontmatter:
            violations.append(f"Missing required field: {field}")
        elif not frontmatter[field]:
            violations.append(f"Empty required field: {field}")

    # Check for deprecated fields
    for field in COMMAND_DEPRECATED_FIELDS:
        if field in frontmatter:
            violations.append(f"Deprecated field: {field} (remove from frontmatter, use body instead)")

    return violations

def validate_skill_manifest(file_path: Path) -> List[str]:
    """
    Validate skill manifest.yaml file.

    Returns:
        List of violation messages (empty if valid)
    """
    violations = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            manifest = yaml.safe_load(f)
    except FileNotFoundError:
        violations.append("Skill missing manifest.yaml file")
        return violations
    except yaml.YAMLError as e:
        violations.append(f"Invalid YAML syntax: {e}")
        return violations
    except Exception as e:
        violations.append(f"Could not read manifest: {e}")
        return violations

    if not manifest:
        violations.append("Empty manifest.yaml file")
        return violations

    # Check required fields
    for field in SKILL_MANIFEST_REQUIRED_FIELDS:
        if field not in manifest:
            violations.append(f"Missing required field: {field}")
        elif not manifest[field]:
            violations.append(f"Empty required field: {field}")

    return violations

def scan_commands(root_path: Path, files: List[str] = None) -> Dict[str, List[str]]:
    """
    Scan command files for frontmatter violations.

    Args:
        root_path: Framework root directory
        files: Optional list of specific files to check

    Returns:
        Dictionary mapping file paths to violations
    """
    results = {}
    commands_dir = root_path / 'commands'

    if not commands_dir.exists():
        return results

    if files:
        # Check specific files
        command_files = [Path(f) for f in files if Path(f).suffix == '.md' and 'commands' in Path(f).parts]
    else:
        # Scan all command files
        command_files = list(commands_dir.glob('*.md'))

    for file_path in command_files:
        # Skip README and CLAUDE.md
        if file_path.name in ['README.md', 'CLAUDE.md']:
            continue

        violations = validate_command_frontmatter(file_path)
        if violations:
            results[str(file_path)] = violations

    return results

def scan_skills(root_path: Path, files: List[str] = None) -> Dict[str, List[str]]:
    """
    Scan skill manifest files for violations.

    Args:
        root_path: Framework root directory
        files: Optional list of specific files to check

    Returns:
        Dictionary mapping file paths to violations
    """
    results = {}
    skills_dir = root_path / 'skills'

    if not skills_dir.exists():
        return results

    if files:
        # Check specific manifest files
        manifest_files = [Path(f) for f in files if Path(f).name == 'manifest.yaml' and 'skills' in Path(f).parts]
    else:
        # Scan all skill manifests
        manifest_files = list(skills_dir.glob('*/manifest.yaml'))

    for file_path in manifest_files:
        violations = validate_skill_manifest(file_path)
        if violations:
            results[str(file_path)] = violations

    return results

def print_violations(command_results: Dict, skill_results: Dict) -> None:
    """Print violations in human-readable format."""
    total_files = len(command_results) + len(skill_results)

    if total_files == 0:
        print("[OK] All frontmatter valid")
        return

    print("[ERROR] INVALID FRONTMATTER DETECTED\n")
    print("Component Metadata Violation:")
    print("Commands must have 'name' and 'description' in YAML frontmatter")
    print("Skills must have valid manifest.yaml with required fields\n")

    if command_results:
        print(f"=== COMMAND VIOLATIONS ({len(command_results)} files) ===\n")
        for file_path, violations in sorted(command_results.items()):
            print(f"FILE: {file_path}")
            for violation in violations:
                print(f"   - {violation}")
            print()

    if skill_results:
        print(f"=== SKILL VIOLATIONS ({len(skill_results)} files) ===\n")
        for file_path, violations in sorted(skill_results.items()):
            print(f"FILE: {file_path}")
            for violation in violations:
                print(f"   - {violation}")
            print()

    print("Fix: Add required YAML frontmatter fields")
    print("See: library/templates/COMMAND-TEMPLATE.md")
    print("See: library/templates/SKILL-MANIFEST-TEMPLATE.yaml")

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Validate YAML frontmatter in commands and skill manifests'
    )
    parser.add_argument(
        'files',
        nargs='*',
        help='Specific files to check (default: scan all commands and skills)'
    )
    parser.add_argument(
        '--root',
        type=Path,
        default=Path.cwd(),
        help='Root directory to scan (default: current directory)'
    )
    parser.add_argument(
        '--commands-only',
        action='store_true',
        help='Check only command files'
    )
    parser.add_argument(
        '--skills-only',
        action='store_true',
        help='Check only skill manifests'
    )

    args = parser.parse_args()

    # Scan for violations
    command_results = {}
    skill_results = {}

    if not args.skills_only:
        command_results = scan_commands(args.root, args.files if args.files else None)

    if not args.commands_only:
        skill_results = scan_skills(args.root, args.files if args.files else None)

    # Print results
    print_violations(command_results, skill_results)

    # Exit with error code if violations found
    sys.exit(1 if (command_results or skill_results) else 0)

if __name__ == '__main__':
    main()
