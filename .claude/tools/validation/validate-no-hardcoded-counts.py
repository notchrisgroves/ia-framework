#!/usr/bin/env python3
"""
Hardcoded Counts Validation - ALL Content

Validates ALL markdown files for hardcoded counts (not just README.md).
This is a BLOCKING rule per CLAUDE.md Critical Requirements.

Checks for patterns like:
- "N tools" (e.g., "43 tools", "17 tools")
- "N skills" (e.g., "18 skills", "7 skills")
- "N agents" (e.g., "4 agents", "8 agents")
- "N commands" (e.g., "15 commands")
- "Total: N"

Usage:
    python validate-no-hardcoded-counts.py              # Check all staged .md files
    python validate-no-hardcoded-counts.py --all        # Check all .md files
    python validate-no-hardcoded-counts.py file.md      # Check specific file
    python validate-no-hardcoded-counts.py --strict     # Exit code 1 if violations

Exit Codes:
    0 - No violations found
    1 - Violations found (with --strict)

Author: Intelligence Adjacent Framework
Version: 1.0
"""

import re
import sys
import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

FRAMEWORK_ROOT = Path(__file__).parent.parent.parent

# ANSI colors
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

@dataclass
class Violation:
    file_path: str
    line_num: int
    line_content: str
    pattern_matched: str

# Patterns that indicate hardcoded counts (BLOCKING)
HARDCODED_COUNT_PATTERNS = [
    (r'\b(\d+)\s+tools?\b', 'tools'),
    (r'\b(\d+)\s+skills?\b', 'skills'),
    (r'\b(\d+)\s+agents?\b', 'agents'),
    (r'\b(\d+)\s+commands?\b', 'commands'),
    (r'\b(\d+)\s+servers?\b', 'servers'),
    (r'\b(\d+)\s+hooks?\b', 'hooks'),
    (r'\b(\d+)\s+workflows?\b', 'workflows'),
    (r'\bTotal:\s*\d+\b', 'total'),
]

# Contexts where numbers are allowed (don't flag these)
ALLOWED_CONTEXTS = [
    r'Level \d+:',          # "Level 1:", "Level 2:"
    r'Phase \d+:',          # "Phase 1:", "Phase 2:"
    r'Step \d+:',           # "Step 1:", "Step 2:"
    r'v\d+\.\d+',           # Version numbers "v1.0"
    r'port \d+',            # Port numbers
    r'<\d+ lines',          # File size limits "<150 lines"
    r'\d+-page',            # "10-page chunks"
    r'\(e\.g\.',            # Examples "(e.g., "18 skills", ...)"
    r'\".*\"',              # Quoted text as example
    r"'.*'",                # Single quoted
    r'example:',            # Examples section
    r'NEVER.*counts',       # Documentation about NOT using counts
    r'hardcode.*count',     # Documentation about rule
    r'❌.*\d+',              # Examples of what NOT to do
    r'search.*pattern',     # Regex pattern documentation
    r'Rating.*\d+',         # "Rating: 5/5" etc.
    r'rating.*\d+',         # QA ratings
    r'≥\s*\d+',             # Thresholds "≥4"
    r'>\s*\d+',             # Comparisons "> 0"
    r'<\s*\d+',             # Comparisons "< 5"
    r'\d+\s*sources',       # "10+ sources" in research requirements
    r'\d+\s*words',         # Word counts in content tiers
    r'\d+\s*hours',         # Time estimates
    r'\d+\s*minutes',       # Time estimates
    r'\d+\s*seconds',       # Timeout values
    r'\d+\s*bytes',         # File sizes
    r'\d+\s*lines',         # Line counts for limits
    r'Port.*\d+',           # Port specifications
    r'Line.*\d+',           # Line number references
    r'\d+\s*questions',     # "22 questions" in risk-assessment (methodology)
]

def is_allowed_context(line: str, match_start: int, match_end: int) -> bool:
    """Check if match appears in an allowed context."""
    start = max(0, match_start - 50)
    end = min(len(line), match_end + 50)
    context = line[start:end]

    for pattern in ALLOWED_CONTEXTS:
        if re.search(pattern, context, re.IGNORECASE):
            return True
    return False

def validate_file(file_path: Path) -> List[Violation]:
    """Validate a single file for hardcoded counts."""
    violations = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"{Colors.YELLOW}Warning: Could not read {file_path}: {e}{Colors.RESET}")
        return violations

    in_code_block = False

    for line_num, line in enumerate(lines, 1):
        # Track code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue

        # Skip code blocks
        if in_code_block:
            continue

        # Skip HTML comments
        if '<!--' in line and '-->' in line:
            continue

        # Check each pattern
        for pattern, pattern_name in HARDCODED_COUNT_PATTERNS:
            matches = re.finditer(pattern, line, re.IGNORECASE)

            for match in matches:
                if not is_allowed_context(line, match.start(), match.end()):
                    violations.append(Violation(
                        file_path=str(file_path.relative_to(FRAMEWORK_ROOT)),
                        line_num=line_num,
                        line_content=line.strip()[:80],
                        pattern_matched=match.group()
                    ))

    return violations

def get_staged_files() -> List[Path]:
    """Get list of staged markdown files."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            capture_output=True,
            text=True,
            cwd=FRAMEWORK_ROOT
        )
        files = [
            FRAMEWORK_ROOT / f.strip()
            for f in result.stdout.strip().split('\n')
            if f.strip().endswith('.md')
        ]
        return [f for f in files if f.exists()]
    except Exception:
        return []

def get_all_md_files() -> List[Path]:
    """Get all markdown files in framework."""
    exclude_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv'}
    files = []

    for md_file in FRAMEWORK_ROOT.rglob('*.md'):
        if not any(ex in str(md_file) for ex in exclude_dirs):
            files.append(md_file)

    return files

def main():
    strict = '--strict' in sys.argv
    check_all = '--all' in sys.argv

    # Determine files to check
    specific_files = [arg for arg in sys.argv[1:] if not arg.startswith('--') and arg.endswith('.md')]

    if specific_files:
        files = [FRAMEWORK_ROOT / f for f in specific_files]
    elif check_all:
        files = get_all_md_files()
    else:
        files = get_staged_files()

    if not files:
        print(f"{Colors.CYAN}No markdown files to check{Colors.RESET}")
        sys.exit(0)

    print(f"{Colors.BOLD}Checking {len(files)} file(s) for hardcoded counts...{Colors.RESET}")

    all_violations = []

    for file_path in files:
        violations = validate_file(file_path)
        all_violations.extend(violations)

    if not all_violations:
        print(f"{Colors.GREEN}✅ No hardcoded counts found{Colors.RESET}")
        sys.exit(0)

    # Print violations
    print(f"\n{Colors.RED}❌ Found {len(all_violations)} hardcoded count(s):{Colors.RESET}\n")

    for v in all_violations:
        print(f"{Colors.YELLOW}{v.file_path}:{v.line_num}{Colors.RESET}")
        print(f"  {Colors.RED}Pattern:{Colors.RESET} {v.pattern_matched}")
        print(f"  {Colors.CYAN}Line:{Colors.RESET} {v.line_content}...")
        print()

    print(f"{Colors.BOLD}Fix:{Colors.RESET} Replace with qualifiers:")
    print(f"  ❌ '43 tools' → ✅ 'Multiple tools'")
    print(f"  ❌ '17 skills' → ✅ 'Various skills'")
    print(f"  ❌ '8 agents' → ✅ 'Specialized agents'")
    print()

    if strict:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
