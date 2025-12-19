#!/bin/bash
# Pre-commit hook: Validate support-skill pattern compliance
# Ensures support skills follow architectural standards

set -e

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Validating Support Skill Pattern Compliance...${NC}"

VIOLATIONS=0

# Get list of support skills (skills with "support skill" in description)
SUPPORT_SKILLS=$(grep -r "description:.*[Ss]upport skill" skills/*/SKILL.md | cut -d: -f1 | xargs dirname | xargs -n1 basename)

if [ -z "$SUPPORT_SKILLS" ]; then
    echo -e "${GREEN}✓${NC} No support skills found (nothing to validate)"
    exit 0
fi

echo -e "${BLUE}Found support skills:${NC} $SUPPORT_SKILLS"
echo ""

# Check 1: Support skills must NOT have slash commands
echo -e "${BLUE}Check 1: Support skills must NOT have slash commands${NC}"
for skill in $SUPPORT_SKILLS; do
    # Convert skill name to command name (e.g., osint-research → osint)
    # Try common patterns: exact match, without "-research", without "-skill"
    cmd_exact="commands/${skill}.md"
    cmd_short=$(echo "$skill" | sed 's/-research$//' | sed 's/-skill$//')
    cmd_file="commands/${cmd_short}.md"

    if [ -f "$cmd_exact" ]; then
        echo -e "${RED}✗ VIOLATION:${NC} Support skill '$skill' has slash command: $cmd_exact"
        echo "  Support skills should not be standalone (no slash commands)"
        echo "  Fix: Delete $cmd_exact"
        VIOLATIONS=$((VIOLATIONS + 1))
    elif [ -f "$cmd_file" ] && [ "$cmd_short" != "$skill" ]; then
        # Check if command file references this skill
        if grep -q "skills/${skill}" "$cmd_file" 2>/dev/null; then
            echo -e "${RED}✗ VIOLATION:${NC} Support skill '$skill' has slash command: $cmd_file"
            echo "  Support skills should not be standalone (no slash commands)"
            echo "  Fix: Delete $cmd_file"
            VIOLATIONS=$((VIOLATIONS + 1))
        fi
    fi
done

if [ $VIOLATIONS -eq 0 ]; then
    echo -e "${GREEN}✓${NC} No support skills have slash commands"
fi

echo ""

# Check 2: Support skills must have "Support skill" in frontmatter description
echo -e "${BLUE}Check 2: Support skills must identify as support skills${NC}"
for skill in $SUPPORT_SKILLS; do
    skill_file="skills/${skill}/SKILL.md"

    if [ ! -f "$skill_file" ]; then
        echo -e "${RED}✗ VIOLATION:${NC} Support skill file not found: $skill_file"
        VIOLATIONS=$((VIOLATIONS + 1))
        continue
    fi

    # Check if description mentions "support skill" or "Support skill"
    if ! grep -q "description:.*[Ss]upport skill" "$skill_file"; then
        echo -e "${RED}✗ VIOLATION:${NC} Support skill '$skill' missing 'Support skill' in description"
        echo "  Fix: Add 'Support skill' to frontmatter description in $skill_file"
        VIOLATIONS=$((VIOLATIONS + 1))
    fi
done

if [ $VIOLATIONS -eq 0 ]; then
    echo -e "${GREEN}✓${NC} All support skills properly identified"
fi

echo ""

# Check 3: Support skills must have "Support skill loaded by:" header
echo -e "${BLUE}Check 3: Support skills must document calling skills${NC}"
for skill in $SUPPORT_SKILLS; do
    skill_file="skills/${skill}/SKILL.md"

    if [ ! -f "$skill_file" ]; then
        continue
    fi

    # Check for "Support skill loaded by:" or "Support skill used by:" pattern
    if ! grep -q "Support skill.*by:" "$skill_file"; then
        echo -e "${YELLOW}⚠ WARNING:${NC} Support skill '$skill' should document calling skills"
        echo "  Recommendation: Add 'Support skill loaded by: skill-a, skill-b' near top of $skill_file"
        # Don't increment violations for warnings
    fi
done

echo ""

# Check 4: Calling skills should have delegation blocks (soft check - too complex for pre-commit)
echo -e "${BLUE}Check 4: Delegation blocks (soft check)${NC}"
for skill in $SUPPORT_SKILLS; do
    # Find potential calling skills by searching for skill name in other SKILL.md files
    POTENTIAL_CALLERS=$(grep -r "skills/${skill}\|${skill} skill" skills/*/SKILL.md skills/*/workflows/*.md 2>/dev/null | cut -d: -f1 | xargs dirname | xargs -n1 basename | sort -u | grep -v "^${skill}$" || true)

    if [ -n "$POTENTIAL_CALLERS" ]; then
        echo -e "${BLUE}  Support skill '${skill}' potentially used by:${NC}"
        for caller in $POTENTIAL_CALLERS; do
            # Check if caller has delegation block
            CALLER_FILES="skills/${caller}/SKILL.md skills/${caller}/workflows/*.md"

            HAS_DELEGATION=$(grep -l "DELEGATE.*${skill}" $CALLER_FILES 2>/dev/null || true)

            if [ -n "$HAS_DELEGATION" ]; then
                echo -e "${GREEN}    ✓${NC} $caller has delegation block"
            else
                echo -e "${YELLOW}    ⚠${NC} $caller references '${skill}' but may not have delegation block"
                echo "      Check: skills/${caller}/workflows/ for 'DELEGATE to ${skill}' blocks"
            fi
        done
    fi
done

echo ""

# Summary
if [ $VIOLATIONS -eq 0 ]; then
    echo -e "${GREEN}═══════════════════════════════════════════${NC}"
    echo -e "${GREEN}✓ Support Skill Pattern Validation PASSED${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════${NC}"
    exit 0
else
    echo -e "${RED}═══════════════════════════════════════════${NC}"
    echo -e "${RED}✗ Support Skill Pattern Validation FAILED${NC}"
    echo -e "${RED}  Found $VIOLATIONS violation(s)${NC}"
    echo -e "${RED}═══════════════════════════════════════════${NC}"
    echo ""
    echo -e "${YELLOW}Fix violations and commit again${NC}"
    echo -e "${YELLOW}See: docs/SUPPORT-SKILL-PATTERN.md${NC}"
    exit 1
fi
