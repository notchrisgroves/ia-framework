# README Validation - Usage Guide

**Date:** 2025-12-12
**Purpose:** How to use the README validation system
**Status:** ✅ Active

---

## Quick Start

### Run Validation

```bash
# Basic validation (shows violations)
python tools/validation/validate-readme.py

# With fix suggestions
python tools/validation/validate-readme.py --explain

# Strict mode (exits with code 1 if violations - for CI/CD)
python tools/validation/validate-readme.py --strict
```

### Example Output

**When validation passes:**
```
README.md Validation Tool
Checking: C:\ia-framework\README.md

======================================================================
README Validation Results
======================================================================

✅ All validations passed!

Checked: 401 lines
✓ No hardcoded counts
✓ No hardcoded sizes
✓ No broken documentation links
```

**When violations found:**
```
README.md Validation Tool
Checking: C:\ia-framework\README.md

======================================================================
README Validation Results
======================================================================

❌ Found 2 violation(s):

Line 168: hardcoded_counts
  Pattern: 672 resources
  Line: - **672 resources** automatically discovered and cataloged...

Line 213: hardcoded_sizes
  Pattern: 7.4GB
  Line: - Space-efficient: 7.4GB working directory (vs 22GB before migration)...

Violations by type:
  • hardcoded_counts: 1
  • hardcoded_sizes: 1

💡 Run with --explain for fix suggestions
```

---

## What Gets Validated

### 1. No Hardcoded Component Counts

**Detects:**
- "18 skills", "28 commands", "4 agents"
- "672 resources", "17 frameworks"
- Any number + component word pattern

**Exceptions (allowed):**
- Version numbers: "v1.0", "v4.0"
- File size limits: "<250 lines", "<500 lines"
- Phase indicators: "Phase 1:", "Step 2:"
- Examples in quotes: (e.g., "18 skills")

### 2. No Hardcoded Sizes

**Detects:**
- "7.4GB", "22GB", "1.5MB"
- Any size with GB/MB/KB/TB

**Why:** Sizes change as resources grow/shrink

### 3. No Percentage Indicators

**Detects:**
- "85% complete", "100% migrated"
- Any percentage + status word

**Use instead:** "Phase X complete", "Migration finished"

### 4. No Hardcoded Dates in Status

**Detects:**
- "Status: 2025-12-11"
- "Last Updated: 2025-12-12"

**Use instead:** Git history provides dates automatically

### 5. No Broken Documentation Links

**Validates:**
- All markdown links to docs/ files exist
- Reports broken links with line numbers

**Skips:**
- External links (http/https)
- Anchors (#sections)

---

## Pre-Commit Hook

**What it does:**
- Runs automatically when you commit changes to README.md
- Blocks commit if violations found
- Shows violations and suggestions

**Location:**
- Windows: `hooks/pre-commit/readme-validation.ps1`
- Linux/Mac: `hooks/pre-commit/readme-validation.sh`

**How to enable:**
- Hook runs automatically if README.md is in staged files
- No manual activation needed (framework handles this)

**Example when blocked:**
```bash
$ git commit -m "Update README"

🔍 Validating README.md...

❌ README.md validation FAILED!

[Violations shown here]

⚠️  Commit blocked due to README violations
Fix violations and try again, or run:
  python tools/validation/validate-readme.py --explain
```

---

## Content Guardian

**What it is:**
- Documentation standards file for writer agent
- Loaded automatically when writer agent starts
- Enforces "no counts" rule during content creation

**Location:** `library/prompts/content-guardian.md`

**What it contains:**
- Forbidden patterns (what NOT to write)
- Approved alternatives (what TO write)
- Examples of good vs bad content
- Self-check questions before writing

**When it applies:**
- README.md updates
- Blog posts
- Technical documentation
- ANY written content

---

## Fixing Violations

### Strategy 1: Use Qualifiers

**Before:**
```markdown
The framework has 18 skills, 28 commands, and 4 agents.
```

**After:**
```markdown
The framework has multiple modular skills, specialized commands,
and dedicated agents for different domains.
```

### Strategy 2: Use Descriptive Language

**Before:**
```markdown
With 672 resources (7.4GB), the library includes...
```

**After:**
```markdown
With a comprehensive resource library, the framework includes...
```

### Strategy 3: Point to Catalogs

**Before:**
```markdown
The system includes 655 CIS Benchmarks and 17 frameworks.
```

**After:**
```markdown
The system includes CIS Benchmarks and security frameworks.
See `library/catalogs/RESOURCES-CATALOG.md` for complete inventory.
```

### Strategy 4: Use Categories

**Before:**
```markdown
Available: 28 commands across 5 categories
```

**After:**
```markdown
Available commands: Security, Writing, Research, Career, Utilities
```

---

## Common Scenarios

### Scenario 1: Updating README with new feature

```bash
# 1. Edit README.md (use qualifiers, not counts)
vim README.md

# 2. Validate before committing
python tools/validation/validate-readme.py

# 3. Fix any violations

# 4. Commit (pre-commit hook validates automatically)
git add README.md
git commit -m "Add new feature to README"
```

### Scenario 2: CI/CD Pipeline

```yaml
# .github/workflows/validate.yml
- name: Validate README
  run: python tools/validation/validate-readme.py --strict
```

### Scenario 3: Writer Agent Creating Documentation

```markdown
# Writer agent startup sequence:
1. Load CLAUDE.md
2. Load library/prompts/content-guardian.md  ← Enforces no-counts rule
3. Load skills/writer/SKILL.md
4. Create content (following content-guardian rules)
```

---

## Reference Documents

**Design Documentation:**
- `docs/README-MAINTENANCE-DESIGN.md` - Complete design and rationale
- `docs/PERSONAL-PROFESSIONAL-INTEGRATION.md` - Output directory design

**Enforcement Files:**
- `tools/validation/validate-readme.py` - Validation tool
- `library/prompts/content-guardian.md` - Writer agent enforcement
- `hooks/pre-commit/readme-validation.{ps1,sh}` - Pre-commit hooks

**Framework Standards:**
- `CLAUDE.md` - Documentation Standards section
- `README.md` - Documentation Standards section

---

## Testing

**Test the validation tool:**
```bash
# Should pass (current README is clean)
python tools/validation/validate-readme.py

# Test with violations (modify README temporarily)
echo "The framework has 18 skills" >> README.md
python tools/validation/validate-readme.py
# Should show violation

# Restore README
git checkout README.md
```

**Test pre-commit hook:**
```bash
# Add violation to README
echo "The framework has 18 skills" >> README.md

# Try to commit
git add README.md
git commit -m "Test"
# Should be blocked

# Restore
git checkout README.md
```

---

## Troubleshooting

### Issue: Validation tool not found

```bash
# Ensure you're in framework root
cd C:\ia-framework

# Check tool exists
ls tools/validation/validate-readme.py
```

### Issue: Pre-commit hook not running

```bash
# Check hook exists
ls hooks/pre-commit/readme-validation.*

# Verify README is staged
git diff --cached --name-only | grep README.md
```

### Issue: False positive (legitimate number flagged)

**Allowed contexts:**
- Version numbers: v1.0 ✅
- Phase indicators: Phase 1: ✅
- File size limits: <250 lines ✅
- Examples in documentation: (e.g., "18 skills") ✅

If legitimately flagged, update `ALLOWED_CONTEXTS` in `validate-readme.py`

---

**Version:** 1.0
**Status:** ✅ Production Ready
**Framework:** Intelligence Adjacent (IA)
