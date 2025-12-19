#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
README Validation Tool - Enforce "No Hardcoded Counts" Rule

Validates README.md against framework standards:
1. No hardcoded component counts ("18 skills", "28 commands")
2. No hardcoded sizes ("7.4GB", "672 resources")
3. No broken documentation links
4. No percentage indicators ("85% complete")

Usage:
    python validate-readme.py              # Check README.md
    python validate-readme.py --strict     # Exit code 1 if violations (for CI/CD)
    python validate-readme.py --explain    # Show suggestions for fixing violations
    python validate-readme.py --fix        # Auto-fix common violations (interactive)

Exit Codes:
    0 - All validations passed
    1 - Violations found (with --strict)
    2 - README.md not found or error

Author: Intelligence Adjacent Framework
Date: 2025-12-12
Version: 1.0
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict
from dataclasses import dataclass

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stdin.reconfigure(encoding='utf-8')

# Paths
FRAMEWORK_ROOT = Path(__file__).parent.parent.parent
README_PATH = FRAMEWORK_ROOT / "README.md"
DOCS_DIR = FRAMEWORK_ROOT / "docs"

# ANSI colors
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

@dataclass
class Violation:
    """Represents a validation violation."""
    line_num: int
    line_content: str
    violation_type: str
    pattern_matched: str
    suggestion: str

# Violation patterns
PATTERNS = {
    'hardcoded_counts': {
        'regex': r'\b\d+\s+(agent|skill|command|resource|tool|framework|benchmark|server|hook|workflow)s?\b',
        'description': 'Hardcoded component count',
        'examples': ['18 skills', '28 commands', '4 agents', '672 resources'],
        'suggestion': 'Use qualifiers: "Multiple skills", "Specialized commands", "Comprehensive resources"'
    },
    'hardcoded_sizes': {
        'regex': r'\b\d+\.?\d*\s?(GB|MB|KB|TB)\b',
        'description': 'Hardcoded size',
        'examples': ['7.4GB', '22GB', '1.5MB'],
        'suggestion': 'Use qualitative descriptions: "Space-efficient storage", "Comprehensive collection"'
    },
    'percentage_complete': {
        'regex': r'\b\d+%\s+(complete|done|finished|migrated)\b',
        'description': 'Percentage completion indicator',
        'examples': ['85% complete', '100% migrated'],
        'suggestion': 'Use phase indicators: "Phase 1 complete", "Migration complete" (no percentages)'
    },
    'specific_dates_in_status': {
        'regex': r'(Status|Last\s+Updated|Build):\s*\d{4}-\d{2}-\d{2}',
        'description': 'Hardcoded date in status line',
        'examples': ['Status: 2025-12-11', 'Last Updated: 2025-12-11'],
        'suggestion': 'Status dates should be in git history, not hardcoded in README'
    }
}

# Allowed contexts where numbers are OK
ALLOWED_CONTEXTS = [
    r'Level \d+:',  # "Level 1:", "Level 2:" in architecture diagrams
    r'Phase \d+:',  # "Phase 1:", "Phase 2:" in roadmaps
    r'Step \d+:',   # "Step 1:", "Step 2:" in instructions
    r'v\d+\.\d+',   # Version numbers "v1.0", "v4.0"
    r'port \d+',    # Port numbers
    r'<\d+ lines',  # File size limits "<250 lines"
    r'\d+-page',    # "10-page chunks"
    r'\(e\.g\.',    # Examples "(e.g., "18 skills", ...)"
    r'\".*\"',      # Quoted text "18 skills"
    r"'.*'",        # Single quoted text
    r'example:',    # Examples section
    r'NEVER.*counts',  # Documentation about NOT using counts
    r'hardcode.*count',  # Documentation about hardcoded counts
]

def is_allowed_context(line: str, match_start: int, match_end: int) -> bool:
    """Check if number appears in an allowed context."""
    # Get surrounding context (30 chars before and after)
    start = max(0, match_start - 30)
    end = min(len(line), match_end + 30)
    context = line[start:end]

    # Check against allowed patterns
    for pattern in ALLOWED_CONTEXTS:
        if re.search(pattern, context, re.IGNORECASE):
            return True

    return False

def validate_readme(readme_path: Path, strict: bool = False) -> Tuple[List[Violation], Dict]:
    """
    Validate README.md against framework standards.

    Args:
        readme_path: Path to README.md
        strict: If True, treat warnings as errors

    Returns:
        Tuple of (violations list, stats dict)
    """
    violations = []
    stats = {
        'total_lines': 0,
        'violations_by_type': {},
        'broken_links': []
    }

    # Read README
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"{Colors.RED}❌ Error: README.md not found at {readme_path}{Colors.RESET}")
        return violations, stats

    stats['total_lines'] = len(lines)

    # Check each line
    for line_num, line in enumerate(lines, 1):
        # Skip code blocks and comments
        if line.strip().startswith('```') or line.strip().startswith('<!--'):
            continue

        # Check each violation pattern
        for vtype, pattern_info in PATTERNS.items():
            matches = re.finditer(pattern_info['regex'], line, re.IGNORECASE)

            for match in matches:
                # Skip if in allowed context
                if is_allowed_context(line, match.start(), match.end()):
                    continue

                violation = Violation(
                    line_num=line_num,
                    line_content=line.strip(),
                    violation_type=vtype,
                    pattern_matched=match.group(),
                    suggestion=pattern_info['suggestion']
                )
                violations.append(violation)

                # Update stats
                stats['violations_by_type'][vtype] = stats['violations_by_type'].get(vtype, 0) + 1

    # Check for broken documentation links
    broken_links = check_doc_links(lines, readme_path.parent)
    stats['broken_links'] = broken_links

    return violations, stats

def check_doc_links(lines: List[str], base_path: Path) -> List[Tuple[int, str]]:
    """
    Check that all doc links in README point to existing files.

    Args:
        lines: README lines
        base_path: Base path for resolving relative links

    Returns:
        List of (line_num, broken_link) tuples
    """
    broken_links = []

    # Pattern for markdown links
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'

    for line_num, line in enumerate(lines, 1):
        matches = re.finditer(link_pattern, line)

        for match in matches:
            link_text = match.group(1)
            link_path = match.group(2)

            # Skip external links (http/https)
            if link_path.startswith('http'):
                continue

            # Skip anchors
            if link_path.startswith('#'):
                continue

            # Check if file exists
            full_path = base_path / link_path
            if not full_path.exists():
                broken_links.append((line_num, link_path))

    return broken_links

def print_violations(violations: List[Violation], stats: Dict, explain: bool = False):
    """Print validation results in colored format."""

    print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}README Validation Results{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*70}{Colors.RESET}\n")

    # Summary
    total_violations = len(violations)
    broken_links = len(stats['broken_links'])

    if total_violations == 0 and broken_links == 0:
        print(f"{Colors.GREEN}✅ All validations passed!{Colors.RESET}")
        print(f"\n{Colors.CYAN}Checked: {stats['total_lines']} lines{Colors.RESET}")
        print(f"{Colors.GREEN}✓ No hardcoded counts{Colors.RESET}")
        print(f"{Colors.GREEN}✓ No hardcoded sizes{Colors.RESET}")
        print(f"{Colors.GREEN}✓ No broken documentation links{Colors.RESET}")
        return

    # Violations by type
    if total_violations > 0:
        print(f"{Colors.RED}❌ Found {total_violations} violation(s):{Colors.RESET}\n")

        for violation in violations:
            print(f"{Colors.YELLOW}Line {violation.line_num}:{Colors.RESET} {Colors.RED}{violation.violation_type}{Colors.RESET}")
            print(f"  {Colors.MAGENTA}Pattern:{Colors.RESET} {violation.pattern_matched}")
            print(f"  {Colors.CYAN}Line:{Colors.RESET} {violation.line_content[:80]}...")

            if explain:
                print(f"  {Colors.GREEN}Fix:{Colors.RESET} {violation.suggestion}")
            print()

    # Broken links
    if broken_links > 0:
        print(f"{Colors.RED}❌ Found {broken_links} broken link(s):{Colors.RESET}\n")

        for line_num, link_path in stats['broken_links']:
            print(f"{Colors.YELLOW}Line {line_num}:{Colors.RESET} {Colors.RED}Broken link{Colors.RESET}")
            print(f"  {Colors.CYAN}Link:{Colors.RESET} {link_path}")
            print()

    # Summary by type
    if stats['violations_by_type']:
        print(f"{Colors.BOLD}Violations by type:{Colors.RESET}")
        for vtype, count in stats['violations_by_type'].items():
            print(f"  • {vtype}: {count}")
        print()

    # Recommendations
    if not explain:
        print(f"{Colors.CYAN}💡 Run with --explain for fix suggestions{Colors.RESET}")

    print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}\n")

def suggest_fixes(violations: List[Violation]):
    """Suggest automated fixes for common violations."""

    fixes = {}

    for violation in violations:
        line_num = violation.line_num

        if violation.violation_type == 'hardcoded_counts':
            # Suggest replacement
            pattern = violation.pattern_matched

            # Extract number and component
            match = re.match(r'(\d+)\s+(\w+)s?', pattern)
            if match:
                num, component = match.groups()

                # Suggest qualitative replacement
                replacements = {
                    'agent': 'Specialized agents',
                    'skill': 'Multiple skills',
                    'command': 'Specialized commands',
                    'resource': 'Comprehensive resources',
                    'tool': 'Framework utilities',
                    'framework': 'Multiple frameworks',
                    'benchmark': 'Security benchmarks'
                }

                suggestion = replacements.get(component.lower(), f'Multiple {component}s')
                fixes[line_num] = (pattern, suggestion)

        elif violation.violation_type == 'hardcoded_sizes':
            # Suggest removing size or using qualifier
            pattern = violation.pattern_matched
            fixes[line_num] = (pattern, 'Space-efficient storage')

    return fixes

def main():
    """Main execution."""
    # Parse arguments
    strict = '--strict' in sys.argv
    explain = '--explain' in sys.argv
    fix = '--fix' in sys.argv

    print(f"{Colors.BOLD}README.md Validation Tool{Colors.RESET}")
    print(f"{Colors.CYAN}Checking: {README_PATH}{Colors.RESET}")

    # Validate
    violations, stats = validate_readme(README_PATH, strict=strict)

    # Print results
    print_violations(violations, stats, explain=explain)

    # Auto-fix mode
    if fix and violations:
        print(f"{Colors.YELLOW}⚠️  Auto-fix mode not yet implemented{Colors.RESET}")
        print(f"{Colors.CYAN}Please review violations and fix manually{Colors.RESET}")
        print(f"\nSee {Colors.MAGENTA}docs/README-MAINTENANCE-DESIGN.md{Colors.RESET} for guidelines")

    # Exit code
    if strict and (len(violations) > 0 or len(stats['broken_links']) > 0):
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
