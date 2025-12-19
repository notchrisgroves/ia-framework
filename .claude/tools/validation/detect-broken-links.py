#!/usr/bin/env python3
"""
Broken Internal Link Detection - Documentation Integrity Enforcement

Detects broken internal links in documentation files (markdown links to other framework files).
Ensures all documentation cross-references are valid.

**Why This Matters:**
Broken links create dead-ends for users trying to navigate documentation.

**Enforcement:**
- Pre-commit hook: Blocks commits with broken links
- Manual validation: Run before releases

See: docs/README-MAINTENANCE-DESIGN.md for validation strategy
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Set

# Pattern to detect markdown links: [text](path)
LINK_PATTERN = r'\[([^\]]+)\]\(([^)]+)\)'

# Directories to EXCLUDE from link checking
EXCLUDE_DIRS = {
    '.git',
    'node_modules',
    '__pycache__',
    'output',  # Engagement deliverables
}

# File extensions to CHECK
CHECK_EXTENSIONS = {
    '.md',
}

# External link patterns to SKIP
EXTERNAL_PATTERNS = [
    r'^https?://',  # HTTP/HTTPS URLs
    r'^mailto:',    # Email links
    r'^#',          # Anchor links within same file
]

def is_external_link(link: str) -> bool:
    """Check if link is external (should be skipped)."""
    for pattern in EXTERNAL_PATTERNS:
        if re.match(pattern, link):
            return True
    return False

def resolve_link_path(source_file: Path, link: str, root_path: Path) -> Path:
    """
    Resolve a relative link path to absolute path.

    Args:
        source_file: File containing the link
        link: The link path from markdown
        root_path: Framework root directory

    Returns:
        Absolute path to the linked file
    """
    # Remove anchor fragments (#section-name)
    link = link.split('#')[0]

    if not link:  # Pure anchor link
        return source_file

    # Handle absolute paths from root
    if link.startswith('~/.claude/'):
        # Convert ~/.claude/ to framework root
        link = link.replace('~/.claude/', '')
        return root_path / link

    # Handle relative paths
    if not link.startswith('/'):
        # Relative to source file's directory
        return (source_file.parent / link).resolve()
    else:
        # Absolute path from root
        return (root_path / link.lstrip('/')).resolve()

def detect_broken_links_in_file(file_path: Path, root_path: Path) -> List[Tuple[int, str, str, str]]:
    """
    Detect broken links in a file.

    Returns:
        List of (line_number, link_text, link_path, reason) tuples
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

        # Find all markdown links in line
        matches = re.finditer(LINK_PATTERN, line)
        for match in matches:
            link_text = match.group(1)
            link_path = match.group(2)

            # Skip external links
            if is_external_link(link_path):
                continue

            # Resolve link to absolute path
            try:
                resolved_path = resolve_link_path(file_path, link_path, root_path)
            except Exception as e:
                violations.append((line_num, link_text, link_path, f"Invalid path: {e}"))
                continue

            # Check if linked file exists
            if not resolved_path.exists():
                violations.append((line_num, link_text, link_path, "File not found"))

    return violations

def scan_directory(root_path: Path, files: List[str] = None) -> dict:
    """
    Scan directory for broken links.

    Args:
        root_path: Root directory to scan
        files: Optional list of specific files to check

    Returns:
        Dictionary mapping file paths to violations
    """
    results = {}

    if files:
        # Check specific files (pre-commit mode)
        file_paths = [Path(f) for f in files if Path(f).exists() and Path(f).suffix in CHECK_EXTENSIONS]
    else:
        # Scan all markdown files
        file_paths = []
        for ext in CHECK_EXTENSIONS:
            file_paths.extend(root_path.rglob(f'*{ext}'))

    for file_path in file_paths:
        # Skip excluded directories
        if any(excluded in file_path.parts for excluded in EXCLUDE_DIRS):
            continue

        violations = detect_broken_links_in_file(file_path, root_path)
        if violations:
            results[str(file_path)] = violations

    return results

def print_violations(results: dict) -> None:
    """Print violations in human-readable format."""
    if not results:
        print("[OK] No broken internal links detected")
        return

    print("[ERROR] BROKEN INTERNAL LINKS DETECTED\n")
    print("Documentation Integrity Violation:")
    print("Internal links must point to existing files within the framework.\n")

    total_violations = sum(len(v) for v in results.values())
    print(f"Found {total_violations} broken link(s) in {len(results)} file(s):\n")

    for file_path, violations in sorted(results.items()):
        print(f"FILE: {file_path}")
        for line_num, link_text, link_path, reason in violations:
            print(f"   Line {line_num}: [{link_text}]({link_path})")
            print(f"            Reason: {reason}")
        print()

    print("Fix: Update links to point to existing files or create missing files")
    print("See: docs/README-MAINTENANCE-DESIGN.md")

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Detect broken internal links in documentation'
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
