#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# Pre-Commit Hook: Documentation Validation
#
# Enforces 7 constitutional rules for documentation:
# 1. No session tracking (Phase checklists, progress markers)
# 2. No dated references (YYYY-MM-DD in paths)
# 3. No hardcoded counts ("18 skills", "4 agents")
# 4. No over-detailed architecture in README
# 5. No development guides in README
# 6. Folder structure: max 2 levels
# 7. No content duplication
#
# This hook BLOCKS commits that violate documentation standards.
#
# Installation:
#   cp hooks/pre-commit/validate-documentation.sh .git/hooks/pre-commit-documentation
#   chmod +x .git/hooks/pre-commit-documentation
#
# Author: Intelligence Adjacent Framework
# Date: 2025-12-14
# Version: 1.0

# Find framework root (where this script lives)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAMEWORK_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Path to validator
VALIDATOR="$FRAMEWORK_ROOT/tools/validation/validate-documentation.py"

# Colors
RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
CYAN='\033[96m'
BOLD='\033[1m'
RESET='\033[0m'

# Check if validator exists
if [ ! -f "$VALIDATOR" ]; then
    echo -e "${RED}Error: Documentation validator not found at $VALIDATOR${RESET}"
    exit 1
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required to run documentation validation${RESET}"
    echo -e "${YELLOW}Install Python 3 or skip validation with: git commit --no-verify${RESET}"
    exit 1
fi

# Determine Python command
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

echo -e "${CYAN}Running documentation validation...${RESET}"

# Run validator on staged files only, with strict mode
$PYTHON_CMD "$VALIDATOR" --staged --strict

# Capture exit code
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Documentation validation passed${RESET}"
    exit 0
else
    echo ""
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo -e "${RED}${BOLD}COMMIT BLOCKED: Documentation validation failed${RESET}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo ""
    echo -e "${YELLOW}Your commit contains documentation that violates framework standards.${RESET}"
    echo ""
    echo -e "${CYAN}To fix:${RESET}"
    echo -e "  1. Review the violations listed above"
    echo -e "  2. Fix the issues in the affected files"
    echo -e "  3. Stage the fixes: ${BOLD}git add [files]${RESET}"
    echo -e "  4. Try committing again: ${BOLD}git commit${RESET}"
    echo ""
    echo -e "${CYAN}For details on the rules:${RESET}"
    echo -e "  ${BOLD}cat docs/README-MAINTENANCE-RULES.md${RESET}"
    echo ""
    echo -e "${YELLOW}To bypass validation (NOT RECOMMENDED):${RESET}"
    echo -e "  ${BOLD}git commit --no-verify${RESET}"
    echo ""

    exit 1
fi
