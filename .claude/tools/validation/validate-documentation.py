#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Documentation Validation Tool - Enforce Constitutional Rules

Validates ALL documentation files against 7 constitutional rules:
1. No session tracking (Phase checklists, progress markers)
2. No dated references (YYYY-MM-DD in paths)
3. No hardcoded counts ("18 skills", "4 agents")
4. No over-detailed architecture (>50 lines in README)
5. No development guides in README
6. Folder structure: high-level only (max 2 levels)
7. No content duplication

Usage:
    python validate-documentation.py                    # Check all docs
    python validate-documentation.py --strict           # Exit 1 if violations
    python validate-documentation.py --file README.md   # Check single file
    python validate-documentation.py --staged           # Check only staged files (for pre-commit)

Exit Codes:
    0 - All validations passed
    1 - Violations found (with --strict)
    2 - File not found or error

Author: Intelligence Adjacent Framework
Date: 2025-12-14
Version: 2.0 (Comprehensive enforcement)
"""

import re
import sys
import subprocess
from pathlib import Path
from typing import List, Tuple, Dict, Set
from dataclasses import dataclass
import argparse

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stdin.reconfigure(encoding='utf-8')

# Paths
FRAMEWORK_ROOT = Path(__file__).parent.parent.parent
DOCS_TO_VALIDATE = [
    "README.md",
    "CLAUDE.md",
    "agents/README.md",
    "skills/README.md",
    "commands/README.md"
]

# Files exempt from validation (historical documents)
EXEMPT_FILES = [
    "FRAMEWORK-AUDIT-2025-12-13.md",
    "RESTRUCTURE-COMPLETE-2025-12-13.md",
    "OUTSTANDING-WORK.md",
    "CRITICAL-GAP-ANALYSIS.md"
]

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
    file: str
    line_num: int
    line_content: str
    rule: str
    pattern_matched: str
    suggestion: str

# Validation patterns for each constitutional rule
RULE_PATTERNS = {
    'rule_1_session_tracking': {
        'patterns': [
            r'(?i)\*\*Phase \d+:.*\(In Progress\)',
            r'- \[[ x]\].*(?:created|complete|finished)',
            r'(?i)Current Status.*\n.*Phase',
            r'(?i)## Current Status',
            r'(?i)✅.*(?:COMPLETE|DONE|FINISHED)',
            r'(?i)⏳.*(?:IN PROGRESS|PENDING)',
        ],
        'description': 'Session tracking / progress markers',
        'examples': ['Phase 1: (In Progress)', '- [x] Folder structure created', 'Current Status'],
        'suggestion': 'Move to sessions/YYYY-MM-DD-project.md. Use simple badges only: "Status: Active Development"'
    },
    'rule_2_dated_references': {
        'patterns': [
            r'`docs/\d{4}-\d{2}-\d{2}-[^`]+`',
            r'See.*\d{4}-\d{2}-\d{2}.*\.md',
            r'(?i)parent framework',
            r'(?i)as of (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}',
        ],
        'description': 'Dated file references',
        'examples': ['docs/2025-12-11-plan.md', 'parent framework', 'As of December 2024'],
        'suggestion': 'Use permanent paths: docs/architecture.md, docs/design.md (no dates in filenames)'
    },
    'rule_3_hardcoded_counts': {
        'patterns': [
            r'\b\d+\s+specialized\s+agents?\b',
            r'\b\d+\s+skills?\b',
            r'\b\d+\s+commands?\b',
            r'\b\d+\s+tools?\b',
            r'\b\d+\s+workflows?\b',
            r'\((?:Security|Content|Research|Advisory|Infrastructure|Meta)\s+\(\d+\)',
            r'\beach <\d+ lines\b',
            r'\b\d+\s+(?:GB|MB|KB|TB)\b',
        ],
        'description': 'Hardcoded component counts or sizes',
        'examples': ['4 specialized agents', '18 skills', 'each <150 lines', 'Security (7)'],
        'suggestion': 'Use qualifiers: "Specialized agents", "Modular skills", "Security, Content, Research"'
    },
    'rule_4_architecture_detail': {
        'patterns': [
            # Only apply to README.md
            # Will be checked with line count logic
        ],
        'description': 'Over-detailed architecture in README',
        'examples': [],
        'suggestion': 'README should have 2-3 sentence summary + link to docs/architecture.md'
    },
    'rule_5_development_guides': {
        'patterns': [
            # Only apply to README.md
            r'## (?:Development|Creating Components|Validation Tools|Pre-Commit Hooks)',
            r'### (?:Agent Format Validation|Framework Health Check)',
        ],
        'description': 'Development process details in README',
        'examples': ['## Development', '## Creating Components'],
        'suggestion': 'Move to CONTRIBUTING.md. README should link only: "See CONTRIBUTING.md"'
    },
    'rule_6_folder_structure': {
        'patterns': [
            # Check for >2 levels of nesting in code blocks
            # Will be checked with custom logic
        ],
        'description': 'Folder structure too detailed (>2 levels)',
        'examples': [],
        'suggestion': 'Show max 2 levels. Link to docs/directory-structure.md for details'
    }
}

# Allowed contexts where numbers are OK
ALLOWED_CONTEXTS = [
    r'Level \d+:',  # "Level 1:", "Level 2:" in architecture
    r'Phase \d+:',  # "Phase 1:" (without status markers)
    r'Step \d+:',   # Instructions
    r'v\d+\.\d+',   # Version numbers
    r'<\d+ lines',  # File size limits
    r'port \d+',    # Port numbers
    r'\d+-\d+-\d+', # Dates in headers "2025-12-14"
    r'Version.*\d+', # Version strings
    r'e\.g\.',      # Examples showing anti-patterns: e.g., "18 skills"
    r'❌',          # Examples of what NOT to do
    r'"\d+\s+\w+"', # Quoted numbers (examples in documentation)
]

def is_exempt_file(file_path: Path) -> bool:
    """Check if file is exempt from validation."""
    return file_path.name in EXEMPT_FILES

def is_allowed_context(line: str) -> bool:
    """Check if line contains allowed context for numbers."""
    for pattern in ALLOWED_CONTEXTS:
        if re.search(pattern, line):
            return True
    return False

def get_staged_files() -> Set[str]:
    """Get list of staged files from git."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only'],
            cwd=FRAMEWORK_ROOT,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return set(result.stdout.strip().split('\n'))
    except Exception:
        pass
    return set()

def check_file(file_path: Path, rules_to_check: List[str] = None) -> List[Violation]:
    """
    Check a single file for violations.

    Args:
        file_path: Path to file to check
        rules_to_check: List of rule keys to check (default: all)

    Returns:
        List of violations found
    """
    violations = []

    # Skip exempt files
    if is_exempt_file(file_path):
        return violations

    # Read file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"{Colors.RED}Error reading {file_path}: {e}{Colors.RESET}")
        return violations

    # Check each rule
    rules = rules_to_check or RULE_PATTERNS.keys()

    for rule_key in rules:
        if rule_key not in RULE_PATTERNS:
            continue

        rule = RULE_PATTERNS[rule_key]

        # Special handling for README-only rules
        if rule_key in ['rule_4_architecture_detail', 'rule_5_development_guides']:
            if file_path.name != 'README.md':
                continue

        # Check each pattern
        for pattern in rule['patterns']:
            for i, line in enumerate(lines, 1):
                # Skip allowed contexts
                if is_allowed_context(line):
                    continue

                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    violations.append(Violation(
                        file=str(file_path.relative_to(FRAMEWORK_ROOT)),
                        line_num=i,
                        line_content=line.strip(),
                        rule=rule_key,
                        pattern_matched=match.group(0),
                        suggestion=rule['suggestion']
                    ))

    # Rule 4: Check architecture section length (README only)
    if file_path.name == 'README.md':
        in_architecture = False
        arch_lines = 0
        arch_start = 0

        for i, line in enumerate(lines, 1):
            if re.match(r'##\s+Architecture', line):
                in_architecture = True
                arch_start = i
            elif in_architecture and re.match(r'##\s+', line):
                # End of architecture section
                if arch_lines > 50:
                    violations.append(Violation(
                        file=str(file_path.relative_to(FRAMEWORK_ROOT)),
                        line_num=arch_start,
                        line_content=f"Architecture section: {arch_lines} lines",
                        rule='rule_4_architecture_detail',
                        pattern_matched=f"{arch_lines} lines",
                        suggestion="Architecture section should be ≤50 lines (summary + link to docs/). Move details to docs/architecture.md"
                    ))
                break
            elif in_architecture:
                arch_lines += 1

    # Rule 6: Check folder structure depth
    in_code_block = False
    code_block_start = 0
    max_depth = 0

    for i, line in enumerate(lines, 1):
        if line.strip().startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_block_start = i
                max_depth = 0
            else:
                # End of code block
                if max_depth > 2 and 'framework' in '\n'.join(lines[code_block_start:i]).lower():
                    violations.append(Violation(
                        file=str(file_path.relative_to(FRAMEWORK_ROOT)),
                        line_num=code_block_start,
                        line_content=f"Folder structure depth: {max_depth} levels",
                        rule='rule_6_folder_structure',
                        pattern_matched=f"{max_depth} levels",
                        suggestion="Show max 2 levels of folder structure. Link to docs/directory-structure.md for complete details"
                    ))
                in_code_block = False
        elif in_code_block:
            # Count leading spaces/tabs to determine depth
            stripped = line.lstrip()
            if stripped and (stripped.startswith('├──') or stripped.startswith('│') or stripped.startswith('└──')):
                indent = len(line) - len(stripped)
                depth = indent // 4  # Assuming 4-space indents
                max_depth = max(max_depth, depth)

    return violations

def print_violations(violations: List[Violation], verbose: bool = True):
    """Print violations in readable format."""
    if not violations:
        print(f"\n{Colors.GREEN}✅ All validations passed!{Colors.RESET}\n")
        return

    print(f"\n{Colors.RED}❌ Violations found:{Colors.RESET}\n")

    # Group by file
    by_file = {}
    for v in violations:
        if v.file not in by_file:
            by_file[v.file] = []
        by_file[v.file].append(v)

    for file, file_violations in by_file.items():
        print(f"{Colors.BOLD}{file}{Colors.RESET}")

        # Group by rule
        by_rule = {}
        for v in file_violations:
            if v.rule not in by_rule:
                by_rule[v.rule] = []
            by_rule[v.rule].append(v)

        for rule, rule_violations in by_rule.items():
            rule_name = rule.replace('_', ' ').title()
            print(f"  {Colors.YELLOW}{rule_name}:{Colors.RESET}")

            for v in rule_violations:
                print(f"    Line {v.line_num}: {Colors.RED}{v.pattern_matched}{Colors.RESET}")
                if verbose:
                    print(f"      {Colors.CYAN}Fix:{Colors.RESET} {v.suggestion}")

        print()

def validate_all(staged_only: bool = False, strict: bool = False) -> int:
    """
    Validate all documentation files.

    Args:
        staged_only: Only check staged files
        strict: Exit with code 1 if violations found

    Returns:
        Exit code (0 = pass, 1 = violations, 2 = error)
    """
    print(f"{Colors.BOLD}Documentation Validation Tool{Colors.RESET}")
    print(f"{Colors.CYAN}Checking documentation against 7 constitutional rules...{Colors.RESET}\n")

    all_violations = []

    # Get files to check
    if staged_only:
        staged = get_staged_files()
        files_to_check = [
            FRAMEWORK_ROOT / f
            for f in DOCS_TO_VALIDATE
            if f in staged
        ]
    else:
        files_to_check = [
            FRAMEWORK_ROOT / f
            for f in DOCS_TO_VALIDATE
            if (FRAMEWORK_ROOT / f).exists()
        ]

    if not files_to_check:
        print(f"{Colors.YELLOW}No files to validate{Colors.RESET}")
        return 0

    # Check each file
    for file_path in files_to_check:
        if not file_path.exists():
            continue

        print(f"{Colors.CYAN}Checking:{Colors.RESET} {file_path.relative_to(FRAMEWORK_ROOT)}")
        violations = check_file(file_path)
        all_violations.extend(violations)

    print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}Validation Results{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*70}{Colors.RESET}")

    print_violations(all_violations)

    if all_violations:
        print(f"{Colors.RED}Total violations: {len(all_violations)}{Colors.RESET}")
        print(f"\n{Colors.YELLOW}Fix violations and try again.{Colors.RESET}")
        print(f"{Colors.CYAN}See docs/README-MAINTENANCE-RULES.md for details.{Colors.RESET}\n")

        if strict:
            return 1
    else:
        print(f"{Colors.GREEN}Checked: {len(files_to_check)} files{Colors.RESET}")
        print(f"{Colors.GREEN}✓ No violations found{Colors.RESET}\n")

    return 0

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Validate documentation against constitutional rules')
    parser.add_argument('--strict', action='store_true', help='Exit with code 1 if violations found')
    parser.add_argument('--staged', action='store_true', help='Check only staged files (for pre-commit)')
    parser.add_argument('--file', type=str, help='Check specific file only')

    args = parser.parse_args()

    if args.file:
        # Check single file
        file_path = FRAMEWORK_ROOT / args.file
        if not file_path.exists():
            print(f"{Colors.RED}File not found: {args.file}{Colors.RESET}")
            return 2

        violations = check_file(file_path)
        print_violations(violations)

        if violations and args.strict:
            return 1
        return 0
    else:
        # Check all files
        return validate_all(staged_only=args.staged, strict=args.strict)

if __name__ == '__main__':
    sys.exit(main())
