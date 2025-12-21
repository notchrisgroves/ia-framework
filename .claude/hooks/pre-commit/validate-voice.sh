#!/bin/bash
# Pre-commit hook: Validate blog post voice
# BLOCKS commit if voice rules violated
# Enforcement: Automated + Blocking

set -e

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if any blog draft files are being ADDED or MODIFIED
BLOG_FILES=$(git diff --cached --name-only --diff-filter=AM | grep '^blog/.*draft\.md$' || true)

if [ -z "$BLOG_FILES" ]; then
    # No blog draft files in commit, skip validation
    exit 0
fi

echo -e "${BLUE}Validating Blog Post Voice...${NC}"
echo ""

VIOLATIONS=0

for file in $BLOG_FILES; do
    echo -e "${BLUE}Checking: $file${NC}"

    # Skip frontmatter (between --- markers) and empty lines to get first content line
    FIRST_CONTENT=$(awk '
        /^---$/ { in_frontmatter = !in_frontmatter; next }
        in_frontmatter { next }
        /^$/ { next }
        /^#/ { next }
        { print; exit }
    ' "$file")

    # Rule 1: Opening must NOT start with narrative pattern
    if echo "$FIRST_CONTENT" | grep -qiE '^In (January|February|March|April|May|June|July|August|September|October|November|December|20[0-9]{2})|^For the past|^Over the past|^When I (started|first|began)|^I (started|began|built|created) '; then
        echo -e "${RED}VOICE VIOLATION:${NC} Opening starts with narrative, not hook"
        echo "   Found: ${FIRST_CONTENT:0:80}..."
        echo "   Required: Bold question or statement"
        echo "   Example: **What if [powerful question]?**"
        VIOLATIONS=$((VIOLATIONS + 1))
    else
        echo -e "${GREEN}✓${NC} Opening is not narrative"
    fi

    # Rule 2: First code block must be under 15 lines
    FIRST_CODE_LINES=$(awk '
        /^```/ {
            if (in_block) {
                print NR - start_line
                exit
            } else {
                in_block = 1
                start_line = NR
            }
        }
    ' "$file")

    if [ -n "$FIRST_CODE_LINES" ] && [ "$FIRST_CODE_LINES" -gt 15 ]; then
        echo -e "${RED}VOICE VIOLATION:${NC} First code block too long ($FIRST_CODE_LINES lines)"
        echo "   Required: Under 15 lines (code is seasoning, not the meal)"
        echo "   Fix: Trim code, link to full implementation"
        VIOLATIONS=$((VIOLATIONS + 1))
    elif [ -n "$FIRST_CODE_LINES" ]; then
        echo -e "${GREEN}✓${NC} First code block is $FIRST_CODE_LINES lines (under 15)"
    else
        echo -e "${GREEN}✓${NC} No code blocks found (OK)"
    fi

    # Rule 3: Check for diagram before analogy (ASCII art or mermaid)
    DIAGRAM_LINE=$(grep -n "^[│┌└├┬┼┤┴┘┐]\|^\`\`\`ascii\|^\`\`\`mermaid" "$file" 2>/dev/null | head -1 | cut -d: -f1 || true)
    ANALOGY_LINE=$(grep -ni "like a \|think of it\|imagine \|similar to \|just as \|much like " "$file" 2>/dev/null | head -1 | cut -d: -f1 || true)

    if [ -n "$DIAGRAM_LINE" ] && [ -n "$ANALOGY_LINE" ]; then
        if [ "$DIAGRAM_LINE" -lt "$ANALOGY_LINE" ]; then
            echo -e "${YELLOW}WARNING:${NC} Diagram appears before analogy"
            echo "   Diagram at line $DIAGRAM_LINE, first analogy at line $ANALOGY_LINE"
            echo "   Recommended: Explain with analogy BEFORE showing diagram"
            # This is a warning, not a blocking violation
        else
            echo -e "${GREEN}✓${NC} Analogy appears before diagram (good warmth)"
        fi
    elif [ -n "$DIAGRAM_LINE" ] && [ -z "$ANALOGY_LINE" ]; then
        echo -e "${YELLOW}WARNING:${NC} Diagram found but no analogy language detected"
        echo "   Consider adding 'think of it like...' before diagrams"
        # This is a warning, not a blocking violation
    else
        echo -e "${GREEN}✓${NC} Diagram/analogy ordering OK"
    fi

    echo ""
done

# Summary
if [ $VIOLATIONS -eq 0 ]; then
    echo -e "${GREEN}═══════════════════════════════════════════${NC}"
    echo -e "${GREEN}✓ Voice Validation PASSED${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════${NC}"
    exit 0
else
    echo -e "${RED}═══════════════════════════════════════════${NC}"
    echo -e "${RED}VOICE VALIDATION FAILED${NC}"
    echo -e "${RED}  Found $VIOLATIONS violation(s)${NC}"
    echo -e "${RED}═══════════════════════════════════════════${NC}"
    echo ""
    echo -e "${YELLOW}Fix violations and commit again${NC}"
    echo -e "${YELLOW}Reference: archive/blog-v3/published/20251203-ia-intro/final.md${NC}"
    echo ""
    echo -e "${BLUE}Voice Rules:${NC}"
    echo -e "  1. Opening MUST be bold question or statement (not narrative)"
    echo -e "  2. First code block MUST be under 15 lines"
    echo -e "  3. Analogies SHOULD appear before diagrams"
    echo ""
    exit 1
fi
