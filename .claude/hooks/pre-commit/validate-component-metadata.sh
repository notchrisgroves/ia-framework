#!/usr/bin/env bash
# Component Metadata Validation Pre-Commit Hook
# Validates YAML frontmatter in commands and skill manifests
# Enforces Documentation Standards (see docs/DOCUMENTATION-STANDARDS-ENFORCEMENT.md)

set -e

# Colors
RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
CYAN='\033[96m'
RESET='\033[0m'

echo -e "${CYAN}🔍 Validating component metadata...${RESET}"

# Get list of staged command files and skill manifests
STAGED_COMMANDS=$(git diff --cached --name-only --diff-filter=ACM | grep -E '^commands/.*\.md$' || true)
STAGED_MANIFESTS=$(git diff --cached --name-only --diff-filter=ACM | grep -E '^skills/.*/manifest\.yaml$' || true)

if [ -z "$STAGED_COMMANDS" ] && [ -z "$STAGED_MANIFESTS" ]; then
    echo -e "${GREEN}✓ No command or skill files modified, skipping metadata validation${RESET}"
    exit 0
fi

# Combine all staged files
STAGED_FILES="$STAGED_COMMANDS $STAGED_MANIFESTS"

# Run frontmatter validation
if python tools/validation/validate-frontmatter.py $STAGED_FILES; then
    echo -e "${GREEN}✅ All component metadata valid!${RESET}"
    exit 0
else
    echo ""
    echo -e "${RED}❌ INVALID COMPONENT METADATA DETECTED!${RESET}"
    echo ""
    echo -e "${YELLOW}⚠️  Commit BLOCKED due to missing or invalid frontmatter${RESET}"
    echo ""
    echo -e "${CYAN}Required fields:${RESET}"
    echo "  Commands: name, description (in YAML frontmatter)"
    echo "  Skills: name, type, description (in manifest.yaml)"
    echo ""
    echo -e "${CYAN}Fix violations by:${RESET}"
    echo "  - Adding required YAML frontmatter to command files"
    echo "  - Ensuring skill manifests have all required fields"
    echo "  - Removing deprecated fields from frontmatter"
    echo ""
    echo -e "${CYAN}See templates:${RESET}"
    echo "  library/templates/COMMAND-TEMPLATE.md"
    echo "  library/templates/SKILL-MANIFEST-TEMPLATE.yaml"
    echo ""
    exit 1
fi
