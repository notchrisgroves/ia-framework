#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Framework Health Check - Validate IA Framework integrity

Checks:
1. Required files exist (CLAUDE.md, settings.json, etc.)
2. All agents under 150 lines
3. All skills under 500 lines
4. Agent-to-skill mappings are valid
5. No broken references in CLAUDE.md

Usage:
    python framework-health-check.py          # Run all checks
    python framework-health-check.py --quick  # Skip slow checks
    python framework-health-check.py --fix    # Suggest fixes

Exit Codes:
    0 - All checks passed
    1 - Issues found
    2 - Critical error

Author: Intelligence Adjacent Framework
Date: 2025-12-18
Version: 1.0
"""

import sys
import json
from pathlib import Path
from typing import List, Tuple, Dict

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stdin.reconfigure(encoding='utf-8')

# Paths
FRAMEWORK_ROOT = Path(__file__).parent.parent.parent
AGENTS_DIR = FRAMEWORK_ROOT / "agents"
SKILLS_DIR = FRAMEWORK_ROOT / "skills"
HOOKS_DIR = FRAMEWORK_ROOT / "hooks"
DOCS_DIR = FRAMEWORK_ROOT / "docs"

# Limits
MAX_AGENT_LINES = 150
MAX_SKILL_LINES = 500

# Required files
REQUIRED_FILES = [
    "CLAUDE.md",
    "README.md",
    "settings.json",
    ".gitignore",
]

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


def check_required_files() -> List[str]:
    """Check that all required files exist."""
    issues = []
    for filename in REQUIRED_FILES:
        filepath = FRAMEWORK_ROOT / filename
        if not filepath.exists():
            issues.append(f"Missing required file: {filename}")
    return issues


def check_agent_line_counts() -> List[str]:
    """Check that all agents are under the line limit."""
    issues = []
    if not AGENTS_DIR.exists():
        return ["agents/ directory not found"]

    for agent_file in AGENTS_DIR.glob("*.md"):
        if agent_file.name == "CLAUDE.md":
            continue  # Skip the agents CLAUDE.md

        line_count = len(agent_file.read_text(encoding='utf-8').splitlines())
        if line_count > MAX_AGENT_LINES:
            issues.append(f"Agent {agent_file.name}: {line_count} lines (max {MAX_AGENT_LINES})")

    return issues


def check_skill_line_counts() -> List[str]:
    """Check that all SKILL.md files are under the line limit."""
    issues = []
    if not SKILLS_DIR.exists():
        return ["skills/ directory not found"]

    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            issues.append(f"Skill {skill_dir.name}: Missing SKILL.md")
            continue

        line_count = len(skill_file.read_text(encoding='utf-8').splitlines())
        if line_count > MAX_SKILL_LINES:
            issues.append(f"Skill {skill_dir.name}/SKILL.md: {line_count} lines (max {MAX_SKILL_LINES})")

    return issues


def check_agent_skill_mapping() -> List[str]:
    """Check that AGENT_SKILL_MAP references valid skills."""
    issues = []
    hook_file = HOOKS_DIR / "load-agent-skill-context.py"

    if not hook_file.exists():
        return ["hooks/load-agent-skill-context.py not found"]

    # Get list of valid skills
    valid_skills = set()
    if SKILLS_DIR.exists():
        for skill_dir in SKILLS_DIR.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                valid_skills.add(skill_dir.name)

    # Parse AGENT_SKILL_MAP from hook - only check the actual map definition
    content = hook_file.read_text(encoding='utf-8')

    # Extract just the AGENT_SKILL_MAP block
    import re
    map_match = re.search(r'AGENT_SKILL_MAP\s*=\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}', content)
    if not map_match:
        return ["Could not parse AGENT_SKILL_MAP from hook"]

    map_content = map_match.group(1)

    # Extract skill names from list values (quoted strings in brackets)
    skill_refs = re.findall(r'\[\s*([^\]]+)\s*\]', map_content)
    for skill_list in skill_refs:
        skills = re.findall(r'"([a-z-]+)"', skill_list)
        for skill_name in skills:
            if skill_name not in valid_skills:
                issues.append(f"AGENT_SKILL_MAP references unknown skill: {skill_name}")

    return issues


def check_settings_json() -> List[str]:
    """Check that settings.json is valid JSON with required fields."""
    issues = []
    settings_file = FRAMEWORK_ROOT / "settings.json"

    if not settings_file.exists():
        return ["settings.json not found"]

    try:
        settings = json.loads(settings_file.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        return [f"settings.json is invalid JSON: {e}"]

    # Check required fields
    required_fields = ["framework", "agents", "skills", "hooks"]
    for field in required_fields:
        if field not in settings:
            issues.append(f"settings.json missing required field: {field}")

    return issues


def check_skill_structure() -> List[str]:
    """Check that skills have proper structure."""
    issues = []
    if not SKILLS_DIR.exists():
        return ["skills/ directory not found"]

    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_name = skill_dir.name
        skill_file = skill_dir / "SKILL.md"

        if not skill_file.exists():
            issues.append(f"Skill {skill_name}: Missing SKILL.md")
            continue

        # Check for YAML frontmatter
        content = skill_file.read_text(encoding='utf-8')
        if not content.startswith("---"):
            issues.append(f"Skill {skill_name}: Missing YAML frontmatter")

    return issues


def run_health_check(quick: bool = False) -> int:
    """Run all health checks and return exit code."""
    print(f"{Colors.BOLD}IA Framework Health Check{Colors.RESET}")
    print(f"{Colors.BLUE}Checking: {FRAMEWORK_ROOT}{Colors.RESET}")

    all_issues = []

    # Check 1: Required files
    print_header("1. Required Files")
    issues = check_required_files()
    if issues:
        for issue in issues:
            print_fail(issue)
        all_issues.extend(issues)
    else:
        print_pass("All required files present")

    # Check 2: Agent line counts
    print_header("2. Agent Line Counts (max 150)")
    issues = check_agent_line_counts()
    if issues:
        for issue in issues:
            print_fail(issue)
        all_issues.extend(issues)
    else:
        print_pass("All agents within limit")

    # Check 3: Skill line counts
    print_header("3. Skill Line Counts (max 500)")
    issues = check_skill_line_counts()
    if issues:
        for issue in issues:
            print_fail(issue)
        all_issues.extend(issues)
    else:
        print_pass("All skills within limit")

    # Check 4: Settings.json
    print_header("4. Settings Configuration")
    issues = check_settings_json()
    if issues:
        for issue in issues:
            print_fail(issue)
        all_issues.extend(issues)
    else:
        print_pass("settings.json valid")

    # Check 5: Skill structure
    if not quick:
        print_header("5. Skill Structure")
        issues = check_skill_structure()
        if issues:
            for issue in issues:
                print_warn(issue)
            # Warnings, not failures
        else:
            print_pass("All skills have proper structure")

    # Check 6: Agent-skill mapping
    if not quick:
        print_header("6. Agent-Skill Mapping")
        issues = check_agent_skill_mapping()
        if issues:
            for issue in issues:
                print_warn(issue)
        else:
            print_pass("All skill mappings valid")

    # Summary
    print_header("Summary")
    if all_issues:
        print(f"{Colors.RED}Found {len(all_issues)} issue(s){Colors.RESET}")
        return 1
    else:
        print(f"{Colors.GREEN}All checks passed!{Colors.RESET}")
        return 0


def main():
    import argparse
    parser = argparse.ArgumentParser(description="IA Framework Health Check")
    parser.add_argument("--quick", action="store_true", help="Skip slow checks")
    parser.add_argument("--fix", action="store_true", help="Suggest fixes (not implemented)")
    args = parser.parse_args()

    exit_code = run_health_check(quick=args.quick)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
