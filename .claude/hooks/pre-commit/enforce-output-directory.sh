#!/usr/bin/env bash
# ==============================================================================
# Pre-Commit Hook: Enforce output/ Directory Standard
# ==============================================================================
# Purpose: Prevent commits with professional/engagements/ paths (old standard)
#          Enforce output/engagements/ pattern (new standard)
# Location: hooks/pre-commit/enforce-output-directory.sh
# Version: 1.0
# ==============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Header
echo "🔍 Checking for output/ directory standard compliance..."

# Get staged files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

if [ -z "$STAGED_FILES" ]; then
    echo "${GREEN}✓${NC} No files to check"
    exit 0
fi

# Track violations
VIOLATIONS_FOUND=0

# Pattern to detect: professional/engagements/ (old standard)
OLD_PATTERN="professional/engagements/"

# Files to check (skills, docs, workflows)
CHECK_PATTERNS=(
    "skills/.*\.md$"
    "docs/.*\.md$"
    "workflows/.*\.md$"
    "commands/.*\.md$"
)

echo "Checking for old professional/engagements/ pattern..."

for FILE in $STAGED_FILES; do
    # Skip if file doesn't exist (deleted files)
    if [ ! -f "$FILE" ]; then
        continue
    fi

    # Check if file matches patterns we care about
    SHOULD_CHECK=0
    for PATTERN in "${CHECK_PATTERNS[@]}"; do
        if echo "$FILE" | grep -qE "$PATTERN"; then
            SHOULD_CHECK=1
            break
        fi
    done

    if [ $SHOULD_CHECK -eq 0 ]; then
        continue
    fi

    # Check for old pattern
    if grep -n "$OLD_PATTERN" "$FILE" > /dev/null 2>&1; then
        echo "${RED}✗${NC} Found old pattern in: $FILE"
        echo "   ${YELLOW}Lines with 'professional/engagements/':${NC}"
        grep -n "$OLD_PATTERN" "$FILE" | head -5 | sed 's/^/   /'
        VIOLATIONS_FOUND=1
    fi
done

# If violations found, block commit
if [ $VIOLATIONS_FOUND -eq 1 ]; then
    echo ""
    echo "${RED}════════════════════════════════════════════════════════════════${NC}"
    echo "${RED}❌ COMMIT BLOCKED: Old output/ pattern detected${NC}"
    echo "${RED}════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "${YELLOW}Problem:${NC} Files contain old 'professional/engagements/' pattern"
    echo "${YELLOW}Standard:${NC} Use 'output/engagements/[type]/[id]/' instead"
    echo ""
    echo "${YELLOW}Fix:${NC}"
    echo "1. Replace 'professional/engagements/' with 'output/engagements/'"
    echo "2. Update engagement type structure: output/engagements/[type]/[id]/"
    echo "3. See docs/FILE-LOCATION-STANDARDS.md for complete pattern"
    echo ""
    echo "${YELLOW}Reference:${NC} docs/FILE-LOCATION-STANDARDS.md (Document Type Matrix)"
    echo ""
    exit 1
fi

echo "${GREEN}✓${NC} Output directory standard compliance verified"
exit 0
