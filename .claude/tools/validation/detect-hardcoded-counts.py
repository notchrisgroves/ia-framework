#!/usr/bin/env python3
"""
Hardcoded Count Detection - Documentation Standards Enforcement

Detects hardcoded component counts in documentation files (e.g., "18 skills", "28 commands").
These create maintenance debt as components are added/removed.

**Why This Matters:**
Hardcoded counts appear in 120+ files and become stale immediately when components change.
Use qualifiers instead: "Multiple skills", "Specialized agents", categories without counts.

**Enforcement:**
- Pre-commit hook: Blocks commits with count violations
- /git-sync: Validates before allowing commits

**Exception:** Historical session reports documenting specific changes at a point in time.

See: docs/README-MAINTENANCE-DESIGN.md for complete policy
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple

# Patterns to detect hardcoded counts
COUNT_PATTERNS = [
    # "X tools" / "X containers" / "X skills" / "X agents" / "X commands"
    (r'\b(\d+)\s+(tools?|containers?|skills?|agents?|commands?|hooks?|workflows?|servers?)\b',
     'component count'),

    # "Category Name (X)" - counts in parentheses after category
    (r'\b(Security|Writing|Research|Utility|Career)\s+\w+\s*\((\d+)\)',
     'category count'),

    # "X/Y deployed" or "X of Y"
    (r'\b(\d+)/(\d+)\s+(deployed|containers?|tools?)',
     'ratio count'),

    # "Total: X" or "Total wrappers: X"
    (r'\b(Total|Deployed|Available|Missing)[\w\s]*:\s*(\d+)',
     'total count'),
]

# Directories to EXCLUDE (historical/temporary data)
EXCLUDE_DIRS = {
    'sessions',      # Historical session reports (allowed to have counts)
    'plans',         # Snapshot planning documents
    'output',        # Engagement deliverables
    '.git',
    'node_modules',
    '__pycache__',
}

# File extensions to CHECK (documentation only)
CHECK_EXTENSIONS = {
    '.md',      # Markdown documentation
    '.yml',     # Docker compose, manifests
    '.yaml',
}

# Files to ALWAYS EXCLUDE
EXCLUDE_FILES = {
    'CHANGELOG.md',  # Historical changes
    'detect-hardcoded-counts.py',  # This script (has examples)
}

def should_check_file(file_path: Path) -> bool:
    """Determine if file should be checked for hardcoded counts."""

    # Exclude specific files
    if file_path.name in EXCLUDE_FILES:
        return False

    # Exclude directories
    if any(excluded in file_path.parts for excluded in EXCLUDE_DIRS):
        return False

    # Check only documentation files
    if file_path.suffix not in CHECK_EXTENSIONS:
        return False

    return True

def detect_counts_in_file(file_path: Path) -> List[Tuple[int, str, str]]:
    """
    Detect hardcoded counts in a file.

    Returns:
        List of (line_number, matched_text, pattern_type) tuples
    """
    violations = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
        return violations

    for line_num, line in enumerate(lines, start=1):
        # Skip code blocks and comments in markdown
        if line.strip().startswith('```') or line.strip().startswith('#'):
            continue

        # Skip example lines in bullet lists (showing what NOT to do)
        # Example: - "18 skills" → "Multiple skills"
        if re.match(r'^\s*-\s+.*→', line):
            continue

        # Skip documentation of what gets blocked
        # Example: - Blocks hardcoded counts ("18 skills", "27 commands")
        if re.search(r'\b[Bb]locks?\b.*["\(]', line):
            continue

        # Check each pattern
        for pattern, pattern_type in COUNT_PATTERNS:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                violations.append((line_num, match.group(0), pattern_type))

    return violations

def scan_directory(root_path: Path, files: List[str] = None) -> dict:
    """
    Scan directory for hardcoded counts.

    Args:
        root_path: Root directory to scan
        files: Optional list of specific files to check (for pre-commit hook)

    Returns:
        Dictionary mapping file paths to violations
    """
    results = {}

    if files:
        # Check specific files (pre-commit mode)
        file_paths = [Path(f) for f in files if Path(f).exists()]
    else:
        # Scan all files in directory
        file_paths = root_path.rglob('*')

    for file_path in file_paths:
        if not file_path.is_file():
            continue

        if not should_check_file(file_path):
            continue

        violations = detect_counts_in_file(file_path)
        if violations:
            results[str(file_path)] = violations

    return results

def print_violations(results: dict) -> None:
    """Print violations in human-readable format."""
    if not results:
        print("[OK] No hardcoded counts detected")
        return

    print("[ERROR] HARDCODED COUNTS DETECTED\n")
    print("Documentation Standards Violation:")
    print("NEVER hardcode component counts (e.g., '18 skills', '28 commands')")
    print("Use qualifiers: 'Multiple skills', 'Specialized agents'\n")

    total_violations = sum(len(v) for v in results.values())
    print(f"Found {total_violations} violation(s) in {len(results)} file(s):\n")

    for file_path, violations in sorted(results.items()):
        print(f"FILE: {file_path}")
        for line_num, matched_text, pattern_type in violations:
            print(f"   Line {line_num}: '{matched_text}' ({pattern_type})")
        print()

    print("Fix: Replace with qualifiers or remove counts")
    print("See: docs/README-MAINTENANCE-DESIGN.md")

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Detect hardcoded component counts in documentation'
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
    sys.exit(1 if results else 0)

if __name__ == '__main__':
    main()
