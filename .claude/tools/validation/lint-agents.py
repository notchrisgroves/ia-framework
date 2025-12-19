#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lint Agents - Validate agent format and structure

Checks:
1. Agent files are under 150 lines
2. YAML frontmatter present
3. Required sections exist
4. No inline skill content (should reference SKILL.md)
5. Proper template adherence

Usage:
    python lint-agents.py              # Lint all agents
    python lint-agents.py security     # Lint specific agent
    python lint-agents.py --fix        # Auto-fix simple issues

Exit Codes:
    0 - All agents valid
    1 - Issues found
    2 - Critical error

Author: Intelligence Adjacent Framework
Date: 2025-12-18
Version: 1.0
"""

import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stdin.reconfigure(encoding='utf-8')

# Paths
FRAMEWORK_ROOT = Path(__file__).parent.parent.parent
AGENTS_DIR = FRAMEWORK_ROOT / "agents"

# Limits
MAX_AGENT_LINES = 150

# Required sections in agent files (with variations)
REQUIRED_SECTIONS = {
    "Identity": ["identity", "core identity", "agent identity"],
    "Startup": ["startup", "mandatory startup", "quick start"],
}

# ANSI colors
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


def print_header(title: str):
    print(f"\n{Colors.BOLD}{title}{Colors.RESET}")
    print("=" * 60)


def print_pass(msg: str):
    print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")


def print_fail(msg: str):
    print(f"{Colors.RED}✗{Colors.RESET} {msg}")


def print_warn(msg: str):
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {msg}")


def check_line_count(content: str, agent_name: str) -> List[str]:
    """Check agent is under line limit."""
    issues = []
    line_count = len(content.splitlines())
    if line_count > MAX_AGENT_LINES:
        issues.append(f"{line_count} lines exceeds {MAX_AGENT_LINES} max")
    return issues


def check_frontmatter(content: str, agent_name: str) -> List[str]:
    """Check YAML frontmatter exists and has required fields."""
    issues = []

    if not content.startswith("---"):
        issues.append("Missing YAML frontmatter")
        return issues

    # Find end of frontmatter
    end_match = re.search(r'^---\s*$', content[3:], re.MULTILINE)
    if not end_match:
        issues.append("Malformed YAML frontmatter (no closing ---)")
        return issues

    frontmatter = content[3:end_match.start() + 3]

    # Check required fields
    if "name:" not in frontmatter:
        issues.append("Frontmatter missing 'name' field")
    if "description:" not in frontmatter:
        issues.append("Frontmatter missing 'description' field")

    return issues


def check_required_sections(content: str, agent_name: str) -> List[str]:
    """Check required sections exist."""
    issues = []
    content_lower = content.lower()

    for section_name, variations in REQUIRED_SECTIONS.items():
        found = False
        for variation in variations:
            # Look for ## Section or # Section headers
            pattern = rf'^#{{1,2}}\s*{re.escape(variation)}'
            if re.search(pattern, content_lower, re.MULTILINE):
                found = True
                break
        if not found:
            issues.append(f"Missing required section: {section_name} (variants: {', '.join(variations)})")

    return issues


def check_no_inline_content(content: str, agent_name: str) -> List[str]:
    """Check for overly detailed inline content that should be in SKILL.md."""
    issues = []

    # Check for inline code blocks >20 lines (should be in scripts/)
    code_blocks = re.findall(r'```[\w]*\n(.*?)```', content, re.DOTALL)
    for block in code_blocks:
        if len(block.splitlines()) > 20:
            issues.append("Large code block (>20 lines) should be in scripts/")

    # Check for inline tables >10 rows (may need to be in reference/)
    table_rows = re.findall(r'^\|.*\|$', content, re.MULTILINE)
    if len(table_rows) > 15:
        issues.append(f"Large table ({len(table_rows)} rows) may belong in reference/")

    return issues


def check_skill_references(content: str, agent_name: str) -> List[str]:
    """Check that skill references point to valid skills."""
    issues = []
    skills_dir = FRAMEWORK_ROOT / "skills"

    # Find skill references like "skills/security-testing/SKILL.md"
    skill_refs = re.findall(r'skills/([a-z-]+)/SKILL\.md', content)

    for skill_name in skill_refs:
        skill_path = skills_dir / skill_name / "SKILL.md"
        if not skill_path.exists():
            issues.append(f"References non-existent skill: {skill_name}")

    return issues


def lint_agent(agent_path: Path) -> Tuple[str, List[str], List[str]]:
    """
    Lint a single agent file.

    Returns:
        Tuple of (agent_name, errors, warnings)
    """
    agent_name = agent_path.stem
    errors = []
    warnings = []

    try:
        content = agent_path.read_text(encoding='utf-8')
    except Exception as e:
        return agent_name, [f"Could not read file: {e}"], []

    # Run checks
    errors.extend(check_line_count(content, agent_name))
    errors.extend(check_frontmatter(content, agent_name))
    errors.extend(check_required_sections(content, agent_name))
    errors.extend(check_skill_references(content, agent_name))

    # Warnings (non-blocking)
    warnings.extend(check_no_inline_content(content, agent_name))

    return agent_name, errors, warnings


def lint_all_agents() -> Dict[str, Tuple[List[str], List[str]]]:
    """Lint all agent files."""
    results = {}

    if not AGENTS_DIR.exists():
        print_fail("agents/ directory not found")
        return results

    for agent_file in AGENTS_DIR.glob("*.md"):
        if agent_file.name == "CLAUDE.md":
            continue  # Skip the agents CLAUDE.md

        agent_name, errors, warnings = lint_agent(agent_file)
        results[agent_name] = (errors, warnings)

    return results


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Lint agent files")
    parser.add_argument("agent", nargs="?", help="Specific agent to lint")
    parser.add_argument("--fix", action="store_true", help="Auto-fix issues (not implemented)")
    args = parser.parse_args()

    print(f"{Colors.BOLD}Agent Linter{Colors.RESET}")
    print(f"{Colors.BLUE}Checking: {AGENTS_DIR}{Colors.RESET}")

    total_errors = 0
    total_warnings = 0

    if args.agent:
        # Lint specific agent
        agent_path = AGENTS_DIR / f"{args.agent}.md"
        if not agent_path.exists():
            print_fail(f"Agent not found: {args.agent}")
            sys.exit(2)

        agent_name, errors, warnings = lint_agent(agent_path)
        results = {agent_name: (errors, warnings)}
    else:
        # Lint all agents
        results = lint_all_agents()

    # Display results
    for agent_name, (errors, warnings) in results.items():
        print_header(f"Agent: {agent_name}")

        if errors:
            for error in errors:
                print_fail(error)
            total_errors += len(errors)

        if warnings:
            for warning in warnings:
                print_warn(warning)
            total_warnings += len(warnings)

        if not errors and not warnings:
            print_pass("All checks passed")

    # Summary
    print_header("Summary")
    if total_errors > 0:
        print(f"{Colors.RED}Errors: {total_errors}{Colors.RESET}")
    if total_warnings > 0:
        print(f"{Colors.YELLOW}Warnings: {total_warnings}{Colors.RESET}")

    if total_errors == 0:
        print(f"{Colors.GREEN}All agents valid!{Colors.RESET}")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
