#!/usr/bin/env python3
"""
Stale Component Reference Detection - Documentation Accuracy Enforcement

Detects references to deleted or non-existent framework components in documentation.
Prevents documentation rot and broken workflow instructions.

**Why This Matters:**
Users follow documentation instructions and try to use components that don't exist.

**Enforcement:**
- Pre-commit hook: Warns about stale references
- Manual validation: Run before releases

See: docs/DOCUMENTATION-STANDARDS-ENFORCEMENT.md
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Set

# Directories to EXCLUDE from reference checking
EXCLUDE_DIRS = {
    '.git',
    'node_modules',
    '__pycache__',
    'output',  # Engagement deliverables (may reference old components)
    'sessions',  # Historical session reports (allowed to reference old components)
}

# File extensions to CHECK
CHECK_EXTENSIONS = {
    '.md',
}

# Reference patterns to detect
COMMAND_PATTERN = r'/([a-z][-a-z0-9]*)'  # /command-name
SKILL_PATTERN = r'skills/([a-z][-a-z0-9]+)'  # skills/skill-name
AGENT_PATTERN = r'agents/([a-z][-a-z0-9]+)'  # agents/agent-name
TOOL_PATTERN = r'tools/([a-z][-a-z0-9_/]+\.py)'  # tools/category/script.py

def get_valid_components(root_path: Path) -> Dict[str, Set[str]]:
    """
    Get lists of all valid framework components.

    Returns:
        Dictionary with component types as keys, sets of valid names as values
    """
    components = {
        'commands': set(),
        'skills': set(),
        'agents': set(),
        'tools': set(),
    }

    # Get commands
    commands_dir = root_path / 'commands'
    if commands_dir.exists():
        for cmd_file in commands_dir.glob('*.md'):
            if cmd_file.name not in ['README.md', 'CLAUDE.md']:
                # Command name is filename without .md
                components['commands'].add(cmd_file.stem)

    # Get skills
    skills_dir = root_path / 'skills'
    if skills_dir.exists():
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
                components['skills'].add(skill_dir.name)

    # Get agents
    agents_dir = root_path / 'agents'
    if agents_dir.exists():
        for agent_file in agents_dir.glob('*.md'):
            # Agent name is filename without .md
            components['agents'].add(agent_file.stem)

    # Get tools (Python scripts)
    tools_dir = root_path / 'tools'
    if tools_dir.exists():
        for tool_file in tools_dir.rglob('*.py'):
            # Tool name is relative path from tools/ (forward slashes)
            rel_path = tool_file.relative_to(tools_dir)
            components['tools'].add(str(rel_path).replace('\\', '/'))

    return components

def detect_stale_references_in_file(
    file_path: Path,
    valid_components: Dict[str, Set[str]]
) -> List[Tuple[int, str, str, str]]:
    """
    Detect stale component references in a file.

    Returns:
        List of (line_number, reference_type, reference_name, context) tuples
    """
    violations = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
        return violations

    for line_num, line in enumerate(lines, start=1):
        # Skip code blocks
        if line.strip().startswith('```'):
            continue

        # Check for command references (/command-name)
        command_matches = re.finditer(COMMAND_PATTERN, line)
        for match in command_matches:
            command_name = match.group(1)
            # Skip if it's not actually a command reference (e.g., /path/to/file)
            # Commands are usually at start of word or after whitespace
            if command_name and command_name not in valid_components['commands']:
                # Additional validation: command references are usually standalone
                # Check if it looks like a slash command
                context_start = max(0, match.start() - 10)
                context_end = min(len(line), match.end() + 10)
                context = line[context_start:context_end].strip()

                # Only flag if it looks like a command (starts line or after space)
                if match.start() == 0 or line[match.start() - 1].isspace():
                    violations.append((line_num, 'command', command_name, context))

        # Check for skill references (skills/skill-name)
        skill_matches = re.finditer(SKILL_PATTERN, line)
        for match in skill_matches:
            skill_name = match.group(1)
            if skill_name and skill_name not in valid_components['skills']:
                context_start = max(0, match.start() - 10)
                context_end = min(len(line), match.end() + 10)
                context = line[context_start:context_end].strip()
                violations.append((line_num, 'skill', skill_name, context))

        # Check for agent references (agents/agent-name)
        agent_matches = re.finditer(AGENT_PATTERN, line)
        for match in agent_matches:
            agent_name = match.group(1)
            if agent_name and agent_name not in valid_components['agents']:
                context_start = max(0, match.start() - 10)
                context_end = min(len(line), match.end() + 10)
                context = line[context_start:context_end].strip()
                violations.append((line_num, 'agent', agent_name, context))

        # Check for tool references (tools/category/script.py)
        tool_matches = re.finditer(TOOL_PATTERN, line)
        for match in tool_matches:
            tool_path = match.group(1)  # Path after 'tools/'
            if tool_path and tool_path not in valid_components['tools']:
                context_start = max(0, match.start() - 10)
                context_end = min(len(line), match.end() + 10)
                context = line[context_start:context_end].strip()
                violations.append((line_num, 'tool', tool_path, context))

    return violations

def scan_directory(root_path: Path, files: List[str] = None) -> Dict[str, List]:
    """
    Scan directory for stale component references.

    Args:
        root_path: Root directory to scan
        files: Optional list of specific files to check

    Returns:
        Dictionary mapping file paths to violations
    """
    # Get list of valid components
    valid_components = get_valid_components(root_path)

    results = {}

    if files:
        # Check specific files
        file_paths = [Path(f) for f in files if Path(f).exists() and Path(f).suffix in CHECK_EXTENSIONS]
    else:
        # Scan all markdown files
        file_paths = list(root_path.rglob('*.md'))

    for file_path in file_paths:
        # Skip excluded directories
        if any(excluded in file_path.parts for excluded in EXCLUDE_DIRS):
            continue

        violations = detect_stale_references_in_file(file_path, valid_components)
        if violations:
            results[str(file_path)] = violations

    return results

def print_violations(results: Dict) -> None:
    """Print violations in human-readable format."""
    if not results:
        print("[OK] No stale component references detected")
        return

    print("[WARNING] STALE COMPONENT REFERENCES DETECTED\n")
    print("Documentation Accuracy Warning:")
    print("References to non-existent commands, skills, agents, or tools found.\n")

    total_violations = sum(len(v) for v in results.values())
    print(f"Found {total_violations} stale reference(s) in {len(results)} file(s):\n")

    for file_path, violations in sorted(results.items()):
        print(f"FILE: {file_path}")
        for line_num, ref_type, ref_name, context in violations:
            print(f"   Line {line_num}: {ref_type.upper()} '{ref_name}' not found")
            print(f"            Context: ...{context}...")
        print()

    print("Fix: Update references to existing components or create missing components")
    print("Note: This check may have false positives for external references")
    print("See: docs/DOCUMENTATION-STANDARDS-ENFORCEMENT.md")

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Detect references to non-existent framework components'
    )
    parser.add_argument(
        'files',
        nargs='*',
        help='Specific files to check (default: scan entire framework)'
    )
    parser.add_argument(
        '--root',
        type=Path,
        default=Path.cwd(),
        help='Root directory to scan (default: current directory)'
    )

    args = parser.parse_args()

    # Scan for violations
    results = scan_directory(args.root, args.files if args.files else None)

    # Print results
    print_violations(results)

    # Exit with error code if violations found
    # Note: Using warning (exit 0) since false positives are likely
    # In production, consider exit 1 for stricter enforcement
    sys.exit(0 if not results else 1)

if __name__ == '__main__':
    main()
