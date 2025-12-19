#!/bin/bash
# Pre-commit Hook: Prevent Duplicate Tracking Documents
# Enforces single source of truth for skill migration tracking

set -e

# ANSI colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Blocked patterns - files that conflict with session tracking
BLOCKED_PATTERNS=(
  "docs/SKILL-MIGRATION-RESULTS.md"
  "docs/MIGRATION-STATUS.md"
  "docs/SKILL-STATUS.md"
  "SKILL-MIGRATION.md"
  "MIGRATION-RESULTS.md"
)

# Check staged files
STAGED_FILES=$(git diff --cached --name-only)

# Check for blocked tracking documents
for pattern in "${BLOCKED_PATTERNS[@]}"; do
  if echo "$STAGED_FILES" | grep -q "$pattern"; then
    echo -e "${RED}❌ COMMIT BLOCKED${NC}"
    echo ""
    echo -e "${YELLOW}Attempted to commit duplicate tracking document:${NC}"
    echo "  $pattern"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "SINGLE SOURCE OF TRUTH ENFORCEMENT"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Skill migration is tracked in ONE location ONLY:"
    echo "  sessions/2025-12-15-skill-migration.md"
    echo ""
    echo "Blocked files (duplicate tracking):"
    for blocked in "${BLOCKED_PATTERNS[@]}"; do
      echo "  - $blocked"
    done
    echo ""
    echo "Allowed files (reference, not tracking):"
    echo "  - docs/SKILL-MIGRATION-AUDIT-YYYY-MM-DD.md (audit snapshots)"
    echo "  - plans/{skill}-migration-plan.md (per-skill planning)"
    echo ""
    echo "To fix:"
    echo "  1. Remove the duplicate tracking file"
    echo "  2. Update sessions/2025-12-15-skill-migration.md instead"
    echo "  3. git reset HEAD $pattern"
    echo ""
    exit 1
  fi
done

# Allow audit snapshots (dated, not live tracking)
if echo "$STAGED_FILES" | grep -q "docs/SKILL-MIGRATION-AUDIT-"; then
  # This is OK - audit snapshots are reference docs, not live tracking
  exit 0
fi

# If we get here, commit is allowed
exit 0
