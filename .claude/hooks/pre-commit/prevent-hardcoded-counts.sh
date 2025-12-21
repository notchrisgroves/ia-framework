#!/usr/bin/env bash
# Hardcoded Count Prevention Pre-Commit Hook
# Blocks commits with hardcoded component counts (e.g., "18 skills", "28 commands")
# Enforces Documentation Standards (see docs/README-MAINTENANCE-DESIGN.md)

set -e

# Colors
RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
CYAN='\033[96m'
RESET='\033[0m'

echo -e "${CYAN}🔍 Checking for hardcoded counts...${RESET}"

# Get list of staged files (only check documentation files)
# Exclude blog/ directory - blog content may legitimately discuss counts (e.g., "50 tools" in MCP analysis)
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(md|yml|yaml)$' | grep -v '^blog/' || true)

if [ -z "$STAGED_FILES" ]; then
    echo -e "${GREEN}✓ No documentation files modified, skipping count validation${RESET}"
    exit 0
fi

# Run count detection on staged files
if python tools/validation/detect-hardcoded-counts.py $STAGED_FILES; then
    echo -e "${GREEN}✅ No hardcoded counts detected!${RESET}"
    exit 0
else
    echo ""
    echo -e "${RED}❌ HARDCODED COUNTS DETECTED!${RESET}"
    echo ""
    echo -e "${YELLOW}⚠️  Commit BLOCKED due to documentation standard violation${RESET}"
    echo ""
    echo -e "${CYAN}Why this matters:${RESET}"
    echo "  Hardcoded counts create maintenance debt across 120+ files"
    echo "  Counts become stale when components are added/removed"
    echo ""
    echo -e "${CYAN}Fix violations by replacing with:${RESET}"
    echo "  ❌ '18 skills' → ✅ 'Multiple skills'"
    echo "  ❌ '28 commands' → ✅ 'Specialized commands'"
    echo "  ❌ 'Security Commands (10)' → ✅ 'Security Commands'"
    echo ""
    echo -e "${CYAN}See documentation:${RESET}"
    echo "  docs/README-MAINTENANCE-DESIGN.md"
    echo "  CLAUDE.md (Documentation Standards section)"
    echo ""
    exit 1
fi
