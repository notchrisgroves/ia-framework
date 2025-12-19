#!/bin/bash
# Pre-commit hook: Prevent output/blog/ references
# Blocks deprecated blog location references before allowing commits

set -e

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get list of staged files (added or modified, not deleted)
STAGED_FILES=$(git diff --cached --name-only --diff-filter=AM || true)

if [ -z "$STAGED_FILES" ]; then
    # No files staged
    exit 0
fi

# File types to check (code and documentation)
CHECK_FILES=$(echo "$STAGED_FILES" | grep -E '\.(md|ts|js|py|sh|yaml|yml)$' || true)

if [ -z "$CHECK_FILES" ]; then
    # No relevant files being committed
    exit 0
fi

echo -e "${BLUE}Checking for deprecated blog location references...${NC}"
echo ""

VIOLATIONS=0
VIOLATION_FILES=()

# Patterns to detect
DEPRECATED_PATTERNS=(
    "output/blog/drafts"
    "output/blog/published"
    "output/blog/docs"
    "output/blog/\[drafts\|published\]"
)

# Files to skip (historical documentation)
SKIP_PATTERNS=(
    "^sessions/"          # Historical session reports
    "^plans/"             # Historical planning docs
    "^output/"            # Actual output files (not code/docs)
)

for file in $CHECK_FILES; do
    # Skip historical files
    should_skip=false
    for pattern in "${SKIP_PATTERNS[@]}"; do
        if echo "$file" | grep -qE "$pattern"; then
            should_skip=true
            break
        fi
    done

    if [ "$should_skip" = true ]; then
        continue
    fi

    # Check for deprecated patterns
    for pattern in "${DEPRECATED_PATTERNS[@]}"; do
        if grep -qF "$pattern" "$file" 2>/dev/null; then
            if [ $VIOLATIONS -eq 0 ]; then
                echo -e "${RED}✗ DEPRECATED BLOG LOCATION DETECTED${NC}"
                echo ""
            fi

            echo -e "${YELLOW}File: $file${NC}"
            grep -nF "$pattern" "$file" | head -3 | while read line; do
                echo "  $line"
            done
            echo ""

            VIOLATIONS=$((VIOLATIONS + 1))
            VIOLATION_FILES+=("$file")
            break  # Only report once per file
        fi
    done
done

# Also check for the research pattern exception
# output/blog/research/ is ALSO deprecated - should be blog/{slug}/research-notes.md
for file in $CHECK_FILES; do
    # Skip historical files
    should_skip=false
    for pattern in "${SKIP_PATTERNS[@]}"; do
        if echo "$file" | grep -qE "$pattern"; then
            should_skip=true
            break
        fi
    done

    if [ "$should_skip" = true ]; then
        continue
    fi

    if grep -qE "output/blog/research" "$file" 2>/dev/null; then
        # Check if file already counted
        already_counted=false
        for counted_file in "${VIOLATION_FILES[@]}"; do
            if [ "$counted_file" = "$file" ]; then
                already_counted=true
                break
            fi
        done

        if [ "$already_counted" = false ]; then
            if [ $VIOLATIONS -eq 0 ]; then
                echo -e "${RED}✗ DEPRECATED BLOG LOCATION DETECTED${NC}"
                echo ""
            fi

            echo -e "${YELLOW}File: $file${NC}"
            grep -nE "output/blog/research" "$file" | head -3 | while read line; do
                echo "  $line"
            done
            echo ""

            VIOLATIONS=$((VIOLATIONS + 1))
        fi
    fi
done

# Summary
if [ $VIOLATIONS -eq 0 ]; then
    echo -e "${GREEN}✓ No deprecated blog location references${NC}"
    exit 0
else
    echo -e "${RED}═══════════════════════════════════════════${NC}"
    echo -e "${RED}✗ DEPRECATED BLOG LOCATIONS DETECTED${NC}"
    echo -e "${RED}  Found $VIOLATIONS violation(s)${NC}"
    echo -e "${RED}═══════════════════════════════════════════${NC}"
    echo ""
    echo -e "${YELLOW}Blog content MUST use flat structure:${NC}"
    echo ""
    echo -e "  ${GREEN}✓ CORRECT:${NC}"
    echo -e "    blog/YYYY-MM-DD-title/draft.md"
    echo -e "    blog/YYYY-MM-DD-title/research-notes.md"
    echo -e "    blog/YYYY-MM-DD-title/metadata.json"
    echo ""
    echo -e "  ${RED}✗ DEPRECATED:${NC}"
    echo -e "    output/blog/drafts/{slug}/"
    echo -e "    output/blog/published/{slug}/"
    echo -e "    output/blog/research/{slug}/"
    echo -e "    output/blog/docs/"
    echo ""
    echo -e "${BLUE}Why:${NC} Files NEVER move. Status tracked in metadata.json, not folder location."
    echo ""
    echo -e "${BLUE}See:${NC} docs/FILE-LOCATION-STANDARDS.md (Rule 3)"
    echo -e "${BLUE}See:${NC} commands/blog-post.md (Workflow)"
    echo ""
    exit 1
fi
