#!/usr/bin/env bash
# README Validation Pre-Commit Hook (Bash)
# Validates README.md before allowing commits
# Enforces "no hardcoded counts" rule

set -e

# Colors
RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
CYAN='\033[96m'
RESET='\033[0m'

echo -e "${CYAN}🔍 Validating README.md...${RESET}"

# Check if README.md is being committed
if ! git diff --cached --name-only | grep -q "README.md"; then
    echo -e "${GREEN}✓ README.md not modified, skipping validation${RESET}"
    exit 0
fi

# Run validation
if python tools/validation/validate-readme.py --strict; then
    echo -e "${GREEN}✅ README.md validation passed!${RESET}"
    exit 0
else
    echo ""
    echo -e "${RED}❌ README.md validation FAILED!${RESET}"
    echo ""
    echo -e "${YELLOW}⚠️  Commit blocked due to README violations${RESET}"
    echo -e "${CYAN}Fix violations and try again, or run:${RESET}"
    echo "  python tools/validation/validate-readme.py --explain"
    echo ""
    echo -e "${CYAN}See also:${RESET}"
    echo "  docs/README-MAINTENANCE-DESIGN.md"
    echo "  library/prompts/content-guardian.md"
    echo ""
    exit 1
fi
