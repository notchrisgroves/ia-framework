# Documentation Standards Enforcement

**Date:** 2025-12-17
**Purpose:** Comprehensive enforcement of all documentation standards
**Status:** Active enforcement + planned improvements

---

## Enforcement Hierarchy

### ✅ ENFORCED (Automated)

#### 1. Hardcoded Count Prevention ✅ COMPLETE (2025-12-17)

**What:** Blocks hardcoded component counts in all documentation

**Tool:** `tools/validation/detect-hardcoded-counts.py`
**Hook:** `hooks/pre-commit/prevent-hardcoded-counts.sh`

**Blocks:**
- Component counts: "18 skills", "27 commands", "5 containers"
- Category counts: "Security Commands (10)"
- Ratio counts: "5/8 deployed"
- Total counts: "Total: 43 tools"

**Scope:** All `.md`, `.yml`, `.yaml` files (excluding sessions/, plans/, output/)

**Skips:**
- Example lines showing before/after ("X tools" → "Multiple tools")
- Documentation describing what gets blocked

**Test:** `python tools/validation/detect-hardcoded-counts.py`
**Status:** ✅ Tested and working

---

#### 2. README.md Validation ✅ ACTIVE

**What:** Validates README.md against specific standards

**Tool:** `tools/validation/validate-readme.py`
**Hook:** `hooks/pre-commit/readme-validation.sh`

**Checks:**
- No hardcoded counts (overlaps with #1)
- No hardcoded file sizes ("7.4GB", "22GB")
- No percentage indicators ("95% complete")

**Test:** `python tools/validation/validate-readme.py`
**Status:** ✅ Tested and working

---

#### 3. Broken Internal Links ✅ COMPLETE (2025-12-17)

**What:** Detects broken links to framework files

**Tool:** `tools/validation/detect-broken-links.py`
**Hook:** `hooks/pre-commit/prevent-broken-links.sh`

**Detects:**
- Links to non-existent `.md` files
- Broken cross-references between components
- Invalid relative paths

**Skips:**
- External HTTP/HTTPS links
- Mailto links
- Anchor links (#section)

**Test:** `python tools/validation/detect-broken-links.py`
**Status:** ✅ Tested and working

---

#### 4. YAML Frontmatter Validation ✅ COMPLETE (2025-12-17)

**What:** Ensures commands and skills have required metadata

**Tool:** `tools/validation/validate-frontmatter.py`
**Hook:** `hooks/pre-commit/validate-component-metadata.sh`

**Checks:**
- Commands: Must have `name:` and `description:` in YAML frontmatter
- Skills: Must have valid `manifest.yaml` with required fields
- Detects deprecated frontmatter fields

**Test:** `python tools/validation/validate-frontmatter.py`
**Status:** ✅ Tested and working

---

#### 5. Stale Component References ⚠️ COMPLETE (Warning Only) (2025-12-17)

**What:** Detects references to deleted components

**Tool:** `tools/validation/detect-stale-references.py`
**Hook:** None (warning-level, not blocking)

**Detects:**
- References to non-existent commands (`/deleted-command`)
- References to removed skills (`skills/deleted-skill`)
- References to deleted agents (`agents/deleted-agent`)
- Tool references that are outdated

**Test:** `python tools/validation/detect-stale-references.py`
**Status:** ✅ Tested and working (found 2 real violations in README.md)

---

#### 6. Path Accuracy Validation ⚠️ COMPLETE (Warning Only) (2025-12-17)

**What:** Ensures documented paths actually exist

**Tool:** `tools/validation/validate-paths.py`
**Hook:** None (warning-level, not blocking)

**Checks:**
- Paths in backticks point to existing files
- Framework directory references are accurate
- Tool path claims are correct

**Skips:**
- External URLs
- Command examples (python, git, bash)
- Slash commands
- Environment variables

**Test:** `python tools/validation/validate-paths.py`
**Status:** ✅ Tested and working

---

### 🔄 PLANNED (Not Yet Automated)

#### 7. Required Section Validation (LOW PRIORITY)

**What:** Ensures standard files have required sections

**Need to check:**
- Agents must have: Quick Start, Core Identity, Operational Requirements
- Skills must have: Quick Start, Decision Tree, Workflows
- Commands must have: Quick Start, When to Use, Workflow, Examples

**Proposed tool:** `tools/validation/validate-structure.py`

**Detection strategy:**
```python
AGENT_REQUIRED_SECTIONS = [
    "Quick Start",
    "Core Identity",
    "Operational Requirements"
]

for agent in agents/*.md:
    sections = extract_sections(agent)
    for required in AGENT_REQUIRED_SECTIONS:
        if required not in sections:
            report_violation(f"Missing section: {required}")
```

**Implementation:** 2-3 hours

---

#### 8. Terminology Consistency (LOW PRIORITY)

**What:** Ensures consistent use of framework terms

**Need to check:**
- "subagent" vs "agent" (prefer "agent")
- "wrapper" vs "tool" (prefer "tool")
- "skill" vs "module" (prefer "skill")
- "slash command" vs "command" (both OK)

**Proposed tool:** `tools/validation/check-terminology.py`

**Detection strategy:**
```python
DEPRECATED_TERMS = {
    'subagent': 'agent',
    'module': 'skill',
}

for doc in all_markdown_files:
    for deprecated, preferred in DEPRECATED_TERMS.items():
        if deprecated in doc.lower():
            suggest_replacement(deprecated, preferred)
```

**Implementation:** 1 hour

---

## Implementation Priority

### Immediate (This Session)
- [x] Hardcoded count prevention - DONE
- [x] Broken link detection tool - DONE
- [ ] Add broken link pre-commit hook
- [ ] Test all enforcement tools

### Next Session (High Value)
- [ ] YAML frontmatter validation
- [ ] Stale component reference detection
- [ ] Path accuracy validation

### Future (Nice to Have)
- [ ] Required section validation
- [ ] Terminology consistency checker

---

## Testing Strategy

**Each enforcement tool MUST have:**

1. **Unit tests** - Test detection logic
   ```python
   def test_detects_hardcoded_counts():
       content = "This has 18 skills"
       violations = detect_counts(content)
       assert len(violations) > 0
   ```

2. **Integration tests** - Test on real files
   ```bash
   # Should pass on clean files
   python tools/validation/detect-broken-links.py README.md
   # Exit code 0

   # Should fail on violations
   echo "[bad](missing.md)" > test.md
   python tools/validation/detect-broken-links.py test.md
   # Exit code 1
   ```

3. **False positive tests** - Ensure it doesn't flag valid content
   ```python
   def test_skips_external_links():
       content = "[GitHub](https://github.com)"
       violations = detect_links(content)
       assert len(violations) == 0
   ```

---

## Pre-Commit Hook Integration

**Pattern for all validation tools:**

```bash
#!/usr/bin/env bash
# Pre-commit hook template

set -e

echo "🔍 Checking for <violation-type>..."

# Get staged files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.<ext>$' || true)

if [ -z "$STAGED_FILES" ]; then
    echo "✓ No relevant files modified, skipping validation"
    exit 0
fi

# Run validation
if python tools/validation/<tool-name>.py $STAGED_FILES; then
    echo "✅ No <violation-type> detected!"
    exit 0
else
    echo ""
    echo "❌ <VIOLATION> DETECTED!"
    echo ""
    echo "⚠️  Commit BLOCKED"
    echo ""
    echo "Fix violations and retry"
    exit 1
fi
```

---

## Documentation References

**For each enforcement mechanism, document:**

1. **What it enforces** - Clear description of the rule
2. **Why it matters** - Impact of violations
3. **How to fix** - Examples of corrections
4. **How to test** - Manual testing instructions
5. **Exceptions** - When rule doesn't apply

**Update these files when adding enforcement:**
- `docs/ENFORCEMENT-METHODOLOGY.md` - Add to "Already Implemented"
- `hooks/pre-commit/README.md` - Document new hook
- `commands/git-sync.md` - Update validation list
- This file - Mark as ✅ ENFORCED

---

## Enforcement Philosophy

**From ENFORCEMENT-METHODOLOGY.md:**

> "If it's important enough to document, it's important enough to enforce automatically."

**Every critical rule MUST have:**
1. Enforcement mechanism (hook, pre-commit, validation tool)
2. Test suite (proves it works)
3. Clear error messages (tells user how to fix)
4. Documentation (explains why it exists)

**Never rely on documentation alone** - Always combine with automated enforcement.

---

## Current Status

**Automated Enforcement Coverage:**
- ✅ Hardcoded counts - COMPLETE (blocking hook)
- ✅ README validation - COMPLETE (blocking hook)
- ✅ Broken links - COMPLETE (blocking hook)
- ✅ YAML frontmatter - COMPLETE (blocking hook)
- ⚠️ Stale references - COMPLETE (warning only, no hook)
- ⚠️ Path accuracy - COMPLETE (warning only, no hook)
- ❌ Required sections - Not started (LOW priority)
- ❌ Terminology - Not started (LOW priority)

**Implementation Status:** 6 of 8 standards enforced (75% complete)
**Time Invested:** ~5-6 hours (2025-12-17)
**Remaining Work:** Low-priority enforcers (~2-3 hours)

---

**Last Updated:** 2025-12-17
**Framework:** Intelligence Adjacent (IA) v4.0
**Status:** Active enforcement + roadmap for complete coverage
