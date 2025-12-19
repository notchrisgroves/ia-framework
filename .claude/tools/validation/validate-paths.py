#!/usr/bin/env python3
"""
Path Accuracy Validation - Documentation Path Verification

Validates that file paths mentioned in documentation actually exist.
Prevents users from searching for non-existent files.

**Why This Matters:**
Documentation says "See: ~/.claude/docs/missing-file.md" but file doesn't exist.
Users waste time looking for files that aren't there.

**Enforcement:**
- Manual validation: Run before releases
- Warning-level: Suggests fixes but doesn't block commits

See: docs/DOCUMENTATION-STANDARDS-ENFORCEMENT.md
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Set

# Directories to EXCLUDE from path checking
EXCLUDE_DIRS = {
    '.git',
    'node_modules',
    '__pycache__',
    'output',  # Engagement deliverables
    'sessions',  # Historical session reports (may reference old paths)
}

# File extensions to CHECK
CHECK_EXTENSIONS = {
    '.md',
}

# Pattern to detect paths in backticks: `path/to/file`
PATH_PATTERN = r'`([^`]+)`'

# Patterns that indicate framework paths
FRAMEWORK_PATH_INDICATORS = [
    r'^~/.claude/',  # Home directory notation
    r'^\./',  # Relative to current directory
    r'^\.\./',  # Parent directory
    r'^/',  # Absolute path (less common)
    r'^tools/',  # Framework directory
    r'^docs/',
    r'^skills/',
    r'^agents/',
    r'^commands/',
    r'^library/',
    r'^hooks/',
    r'^servers/',
]

# Patterns to SKIP (not file paths)
SKIP_PATTERNS = [
    r'^https?://',  # URLs
    r'^git@',  # Git SSH URLs
    r'^[A-Z_]+$',  # Environment variables (e.g., `AWS_KEY`)
    r'^[a-z]+:',  # Commands with flags (e.g., `docker-compose:`)
    r'^\$',  # Shell variables
    r'^\.env$',  # Special files that shouldn't exist in repo
    r'^\*\.',  # Glob patterns (e.g., `*.md`)
    r'^--',  # Command flags
    r'^-[a-z]$',  # Short flags
    r'^/[a-z][-a-z0-9]*$',  # Slash commands (e.g., `/public-sync`, `/git-sync`)
    r'^python\s',  # Command examples starting with python
    r'^bash\s',  # Command examples starting with bash
    r'^git\s',  # Command examples starting with git
    r'^docker\s',  # Command examples starting with docker
]

def looks_like_framework_path(path: str) -> bool:
    """Check if string looks like a framework file path."""
    # Skip obviously non-path patterns
    for pattern in SKIP_PATTERNS:
        if re.match(pattern, path):
            return False

    # Check if it matches framework path indicators
    for pattern in FRAMEWORK_PATH_INDICATORS:
        if re.match(pattern, path):
            return True

    # Also match paths with file extensions
    if re.search(r'\.(md|py|sh|yaml|yml|json|txt)$', path):
        return True

    return False

def resolve_path(path: str, source_file: Path, root_path: Path) -> Path:
    """
    Resolve a path string to absolute path.

    Args:
        path: Path string from documentation
        source_file: File containing the path reference
        root_path: Framework root directory

    Returns:
        Absolute path to the referenced file
    """
    # Handle ~/.claude/ notation
    if path.startswith('~/.claude/'):
        path = path.replace('~/.claude/', '')
        return root_path / path

    # Handle absolute paths from root
    if path.startswith('/'):
        return root_path / path.lstrip('/')

    # Handle relative paths
    if path.startswith('./') or path.startswith('../'):
        return (source_file.parent / path).resolve()

    # Assume path is relative to framework root
    return root_path / path

def detect_invalid_paths_in_file(file_path: Path, root_path: Path) -> List[Tuple[int, str, str]]:
    """
    Detect invalid file path references in a file.

    Returns:
        List of (line_number, path, reason) tuples
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

        # Find all paths in backticks
        matches = re.finditer(PATH_PATTERN, line)
        for match in matches:
            path_str = match.group(1)

            # Check if it looks like a framework path
            if not looks_like_framework_path(path_str):
                continue

            # Try to resolve and check existence
            try:
                resolved_path = resolve_path(path_str, file_path, root_path)

                # Check if path exists
                if not resolved_path.exists():
                    violations.append((line_num, path_str, f"Path not found: {resolved_path}"))

            except Exception as e:
                # Path resolution failed
                violations.append((line_num, path_str, f"Invalid path: {e}"))

    return violations

def scan_directory(root_path: Path, files: List[str] = None) -> dict:
    """
    Scan directory for invalid path references.

    Args:
        root_path: Root directory to scan
        files: Optional list of specific files to check

    Returns:
        Dictionary mapping file paths to violations
    """
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

        violations = detect_invalid_paths_in_file(file_path, root_path)
        if violations:
            results[str(file_path)] = violations

    return results

def print_violations(results: dict) -> None:
    """Print violations in human-readable format."""
    if not results:
        print("[OK] All documented paths exist")
        return

    print("[WARNING] INVALID PATH REFERENCES DETECTED\n")
    print("Documentation Path Accuracy Warning:")
    print("File paths mentioned in documentation do not exist.\n")

    total_violations = sum(len(v) for v in results.values())
    print(f"Found {total_violations} invalid path(s) in {len(results)} file(s):\n")

    for file_path, violations in sorted(results.items()):
        print(f"FILE: {file_path}")
        for line_num, path_str, reason in violations:
            print(f"   Line {line_num}: `{path_str}`")
            print(f"            Reason: {reason}")
        print()

    print("Fix: Update paths to point to existing files or create missing files")
    print("Note: This check may have false positives for example paths")
    print("See: docs/DOCUMENTATION-STANDARDS-ENFORCEMENT.md")

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Validate file path references in documentation'
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

    # Exit with warning (exit 0) since false positives are likely
    # In production, consider exit 1 for stricter enforcement
    sys.exit(0 if not results else 1)

if __name__ == '__main__':
    main()
