#!/usr/bin/env bash
# Broken Link Prevention Pre-Commit Hook
# Blocks commits with broken internal documentation links
# Enforces Documentation Standards (see docs/DOCUMENTATION-STANDARDS-ENFORCEMENT.md)

set -e

# Colors
RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
CYAN='\033[96m'
RESET='\033[0m'

echo -e "${CYAN}🔍 Checking for broken internal links...${RESET}"

# Get list of staged markdown files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.md$' || true)

if [ -z "$STAGED_FILES" ]; then
    echo -e "${GREEN}✓ No markdown files modified, skipping link validation${RESET}"
    exit 0
fi

# Run broken link detection on staged files
if python tools/validation/detect-broken-links.py $STAGED_FILES; then
    echo -e "${GREEN}✅ No broken internal links detected!${RESET}"
    exit 0
else
    echo ""
    echo -e "${RED}❌ BROKEN INTERNAL LINKS DETECTED!${RESET}"
    echo ""
    echo -e "${YELLOW}⚠️  Commit BLOCKED due to documentation integrity violation${RESET}"
    echo ""
    echo -e "${CYAN}Why this matters:${RESET}"
    echo "  Broken links create dead-ends for users navigating documentation"
    echo ""
    echo -e "${CYAN}Fix violations by:${RESET}"
    echo "  - Updating links to point to existing files"
    echo "  - Creating missing files referenced by links"
    echo "  - Removing references to deleted components"
    echo ""
    echo -e "${CYAN}See documentation:${RESET}"
    echo "  docs/DOCUMENTATION-STANDARDS-ENFORCEMENT.md"
    echo "  docs/README-MAINTENANCE-DESIGN.md"
    echo ""
    exit 1
fi
