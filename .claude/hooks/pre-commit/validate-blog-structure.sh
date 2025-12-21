#!/bin/bash
# Pre-commit hook: Validate blog post structure
# Ensures blog posts follow flat structure standards before allowing commits

set -e

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if any blog files are being ADDED or MODIFIED (not deleted)
BLOG_FILES=$(git diff --cached --name-only --diff-filter=AM | grep '^blog/' || true)

if [ -z "$BLOG_FILES" ]; then
    # No blog files being added/modified in commit, skip validation
    exit 0
fi

echo -e "${BLUE}Validating Blog Post Structure...${NC}"
echo ""

VIOLATIONS=0

# Extract unique blog post directories from changed files
# Structure: blog/YYYY-MM-DD-slug/ for posts (top-level), blog/pages/ for static pages
# For a file like blog/2025-12-20-title/draft.md, we want blog/2025-12-20-title
BLOG_DIRS=$(echo "$BLOG_FILES" | while read f; do dirname "$f"; done | sort -u)

for dir in $BLOG_DIRS; do
    # Skip blog/ root directory, STATUS.md, and pages/ directory (static pages, not blog posts)
    if [ "$dir" = "blog" ] || [ "$dir" = "blog/STATUS.md" ] || [[ "$dir" == blog/pages* ]]; then
        continue
    fi

    echo -e "${BLUE}Checking: $dir${NC}"

    # Extract slug from directory path (blog/YYYY-MM-DD-title → YYYY-MM-DD-title)
    slug=$(basename "$dir")

    # Check 1: Slug format validation (YYYY-MM-DD-title pattern)
    if ! echo "$slug" | grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+$'; then
        echo -e "${RED}✗ VIOLATION:${NC} Invalid slug format: $slug"
        echo "  Expected: YYYY-MM-DD-title (lowercase, hyphens only)"
        echo "  Example: 2025-12-17-blog-workflow-test"
        VIOLATIONS=$((VIOLATIONS + 1))
    else
        echo -e "${GREEN}✓${NC} Slug format valid"
    fi

    # Check 2: Required files exist
    draft_file="${dir}/draft.md"
    metadata_file="${dir}/metadata.json"

    if [ ! -f "$draft_file" ]; then
        echo -e "${RED}✗ VIOLATION:${NC} Missing draft.md in $dir"
        echo "  All blog posts must have draft.md"
        VIOLATIONS=$((VIOLATIONS + 1))
    else
        echo -e "${GREEN}✓${NC} draft.md exists"

        # Check 3: Validate frontmatter in draft.md
        # Extract frontmatter (between --- markers)
        frontmatter=$(awk '/^---$/{flag=!flag;next}flag' "$draft_file")

        # Check required fields
        required_fields=("title" "excerpt" "tags" "visibility" "category")

        for field in "${required_fields[@]}"; do
            if ! echo "$frontmatter" | grep -q "^${field}:"; then
                echo -e "${RED}✗ VIOLATION:${NC} Missing required frontmatter field: $field"
                echo "  File: $draft_file"
                VIOLATIONS=$((VIOLATIONS + 1))
            fi
        done

        if [ $VIOLATIONS -eq 0 ]; then
            echo -e "${GREEN}✓${NC} All required frontmatter fields present"
        fi

        # Check 4: Validate visibility value
        visibility=$(echo "$frontmatter" | grep "^visibility:" | sed 's/visibility: *//' | tr -d '"' | tr -d "'" | xargs)

        if [ -n "$visibility" ]; then
            if [[ "$visibility" != "public" && "$visibility" != "members" && "$visibility" != "paid" ]]; then
                echo -e "${RED}✗ VIOLATION:${NC} Invalid visibility value: $visibility"
                echo "  Allowed: public, members, paid"
                echo "  File: $draft_file"
                VIOLATIONS=$((VIOLATIONS + 1))
            else
                echo -e "${GREEN}✓${NC} Visibility valid: $visibility"
            fi
        fi
    fi

    if [ ! -f "$metadata_file" ]; then
        echo -e "${YELLOW}⚠ WARNING:${NC} Missing metadata.json in $dir"
        echo "  This file is auto-generated on first publish"
        echo "  No action needed if this is a new draft"
    else
        echo -e "${GREEN}✓${NC} metadata.json exists"

        # Check 5: Validate JSON structure
        if ! python -m json.tool "$metadata_file" > /dev/null 2>&1; then
            echo -e "${RED}✗ VIOLATION:${NC} Invalid JSON in $metadata_file"
            echo "  Run: python -m json.tool $metadata_file to see errors"
            VIOLATIONS=$((VIOLATIONS + 1))
        else
            echo -e "${GREEN}✓${NC} metadata.json is valid JSON"
        fi
    fi

    echo ""
done

# Summary
if [ $VIOLATIONS -eq 0 ]; then
    echo -e "${GREEN}═══════════════════════════════════════════${NC}"
    echo -e "${GREEN}✓ Blog Structure Validation PASSED${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════${NC}"
    exit 0
else
    echo -e "${RED}═══════════════════════════════════════════${NC}"
    echo -e "${RED}✗ Blog Structure Validation FAILED${NC}"
    echo -e "${RED}  Found $VIOLATIONS violation(s)${NC}"
    echo -e "${RED}═══════════════════════════════════════════${NC}"
    echo ""
    echo -e "${YELLOW}Fix violations and commit again${NC}"
    echo -e "${YELLOW}See: skills/writer/SKILL.md (Blog Post Workflow)${NC}"
    echo ""
    echo -e "${BLUE}Quick fixes:${NC}"
    echo -e "  1. Ensure slug format: YYYY-MM-DD-title (lowercase, hyphens)"
    echo -e "  2. Add missing frontmatter fields to draft.md:"
    echo -e "     title, excerpt, tags, visibility, category"
    echo -e "  3. Set visibility to: public, members, or paid"
    echo -e "  4. Create draft.md if missing"
    echo ""
    exit 1
fi
