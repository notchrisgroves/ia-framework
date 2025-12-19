# Output Directory Standard

**Version:** 1.1
**Date:** 2025-12-18
**Status:** ✅ Active Enforcement

---

## Overview

All engagement deliverables MUST use the `output/` directory structure. Blog content uses a separate `blog/` directory with flat structure.

**Why this matters:**
- Consistent location across all skills
- Proper gitignore handling (structure versioned, client data blocked)
- Clear separation between framework code and generated outputs

**Note:** Blog content uses `blog/YYYY-MM-DD-title/` (flat structure at root). See `docs/FILE-LOCATION-STANDARDS.md` Rule 3 for blog-specific standards.

---

## Standard Pattern

### Engagements

**Pattern:** `output/engagements/[type]/[id]/`

**Examples:**
```
output/engagements/pentest/acme-corp-2025-12/
output/engagements/vuln-scan/startup-2025-11/
output/engagements/secure-config/client-2025-10/
output/engagements/code-review/project-2025-09/
```

**Type Values:**
- `pentest` - Penetration testing engagements
- `vuln-scan` - Vulnerability scanning assessments
- `segmentation-test` - Network segmentation validation
- `secure-config` - Configuration hardening validation
- `code-review` - Source code security review
- `arch-review` - Architecture security assessment
- `risk-assessment` - Security risk assessments

**ID Format:** `{client-name}-{YYYY-MM}`

### Blog Content (Separate Directory)

**Pattern:** `blog/YYYY-MM-DD-title/` (flat structure at root, NOT in output/)

**Examples:**
```
blog/2025-12-17-security-testing-automation/
blog/2025-12-18-vps-api-wrappers/
blog/2025-12-19-intelligence-adjacent-intro/
```

**Key principle:** Files NEVER move between folders. Status tracked in `metadata.json`, not folder location.

**See:** `docs/FILE-LOCATION-STANDARDS.md` (Rule 3) for complete blog standards.

---

## Git Ignore Strategy

**Strategy:** Allow structure directories, block client data

**Pattern in .gitignore:**
```gitignore
# Block all output by default
output/

# Allow top-level output structure
!output/
!output/.gitkeep

# Allow engagements directory structure
!output/engagements/
!output/engagements/README.md

# Allow engagement type directories (second level - structure only)
!output/engagements/*/
!output/engagements/*/README.md

# Block actual engagement directories (third level - contain client data)
output/engagements/*/*/

# Note: Blog content uses blog/ directory (not output/blog/)
# See: docs/FILE-LOCATION-STANDARDS.md (Rule 3)
```

**What gets versioned:**
- ✅ `output/` directory itself
- ✅ `output/engagements/` directory
- ✅ `output/engagements/pentest/` directory
- ✅ `output/engagements/*/README.md` files
- ❌ `output/engagements/pentest/acme-corp-2025-12/` (client data)

---

## Enforcement

### Pre-Commit Hook

**Hook:** `hooks/pre-commit/enforce-output-directory.sh`

**What it checks:**
- Detects old `professional/engagements/` pattern
- Blocks commits with deprecated paths
- Enforces `output/engagements/` standard

**When it runs:** Automatically on `git commit`

**How to bypass:** DON'T - Fix the violation instead

### Manual Verification

**Check your skill files:**
```bash
# Search for old pattern
grep -r "professional/engagements/" skills/*/SKILL.md

# Should return nothing (0 matches)
```

**Check your workflow files:**
```bash
# Search for old pattern
grep -r "professional/engagements/" skills/*/workflows/*.md

# Should return nothing (0 matches)
```

---

## Migration Guide

### Old Pattern → New Pattern

**Old (deprecated):**
```
professional/engagements/pentests/acme-corp-2025-12/
professional/engagements/vuln-scans/startup-2025-11/
professional/engagements/secure-configs/client-2025-10/
```

**New (standard):**
```
output/engagements/pentest/acme-corp-2025-12/
output/engagements/vuln-scan/startup-2025-11/
output/engagements/secure-config/client-2025-10/
```

**Changes:**
1. `professional/` → `output/`
2. Plural type names → Singular (`pentests` → `pentest`, `secure-configs` → `secure-config`)
3. Structure: `output/engagements/[type]/[id]/` (consistent pattern)

### Updating Skill Files

**In SKILL.md:**
```markdown
OLD:
professional/engagements/pentests/{client}-{YYYY-MM}/

NEW:
output/engagements/pentest/{client}-{YYYY-MM}/
```

**In Workflows:**
```markdown
OLD:
1. Create engagement directory: professional/engagements/pentests/acme-2025-12/

NEW:
1. Create engagement directory: output/engagements/pentest/acme-2025-12/
```

---

## Documentation References

**Where output/ is documented:**
1. `docs/FILE-LOCATION-STANDARDS.md` - Document Type Matrix (line 39-40)
2. `CLAUDE.md` - Directory Structure (lines 93-95)
3. `.gitignore` - Output patterns (lines 207-229)
4. Individual `skills/*/SKILL.md` - Output Structure sections
5. This file - Complete standard documentation

**Enforcement:**
- `hooks/pre-commit/enforce-output-directory.sh` - Automatic detection
- `docs/FILE-LOCATION-STANDARDS.md` - Manual reference
- Skills SKILL.md files - Skill-specific examples

---

## Skills Using Output Standard

**All skills migrated to output/ standard (2025-12-17):**
- ✅ security-testing → `output/engagements/pentest/`
- ✅ security-advisory → `output/engagements/risk-assessment/`
- ✅ code-review → `output/engagements/code-review/`
- ✅ architecture-review → `output/engagements/arch-review/`
- ✅ secure-config → `output/engagements/secure-config/`
- ✅ benchmark-generation → `output/engagements/benchmark/`
- ✅ dependency-audit → `output/engagements/dependency-audit/`
- ✅ threat-intel → `output/engagements/threat-intel/`
- ✅ infrastructure-ops → Uses engagement-specific paths
- ✅ career → `output/career/`
- ✅ legal → `output/engagements/legal/`

**Skills using separate directories (not output/):**
- ✅ writer → `blog/YYYY-MM-DD-title/` (flat structure)
- ✅ osint-research → Support skill (no direct output)
- ✅ qa-review → Support skill (no direct output)
- ✅ create-skill → Creates in `skills/` directory
- ✅ gitingest-repo → Creates in `resources/` directory

---

## Common Issues

### Issue 1: Hook Blocks Commit

**Error:**
```
❌ COMMIT BLOCKED: Old output/ pattern detected
Found old pattern in: skills/my-skill/SKILL.md
```

**Solution:**
```bash
# Find all occurrences
grep -n "professional/engagements/" skills/my-skill/SKILL.md

# Replace with output/ pattern
sed -i 's|professional/engagements/|output/engagements/|g' skills/my-skill/SKILL.md

# Also update plural types to singular
sed -i 's|output/engagements/pentests/|output/engagements/pentest/|g' skills/my-skill/SKILL.md
```

### Issue 2: Unsure Which Type to Use

**Question:** "Is my engagement 'pentest' or 'security-test' or 'penetration-testing'?"

**Answer:** Use the skill name (singular form):
- `/pentest` command → `output/engagements/pentest/`
- `/vuln-scan` command → `output/engagements/vuln-scan/`
- `/secure-config` command → `output/engagements/secure-config/`

**Pattern:** `output/engagements/{skill-name}/{client}-{YYYY-MM}/`

### Issue 3: Directory Doesn't Exist

**Error:** `mkdir: cannot create directory 'output/engagements/pentest': No such file or directory`

**Solution:**
```bash
# Create output structure
mkdir -p output/engagements/pentest
mkdir -p output/engagements/vuln-scan
mkdir -p output/engagements/secure-config

# Or create on-demand
mkdir -p output/engagements/[type]
```

---

## Testing the Standard

**Verify enforcement works:**
```bash
# 1. Create test file with old pattern
echo "professional/engagements/test/" > test.md
git add test.md

# 2. Try to commit (should be blocked)
git commit -m "Test commit"

# Expected: ❌ COMMIT BLOCKED

# 3. Fix and try again
sed -i 's|professional/engagements/|output/engagements/|g' test.md
git add test.md
git commit -m "Test commit"

# Expected: ✅ Commit succeeds

# 4. Cleanup
git reset HEAD~1
rm test.md
```

---

## Future Considerations

**Potential Enhancements:**
1. Automatic migration script (scan all skills, replace patterns)
2. output/README.md with examples for each engagement type
3. Template engagement directories with boilerplate
4. Hook to auto-create output/engagements/[type]/ on first use

**Status:** Current implementation sufficient for framework needs

---

**Version:** 1.1
**Framework:** Intelligence Adjacent (IA)
**Enforcement:** Active (pre-commit hook + manual verification)
**Documentation:** Complete (5 file references)
**Last Updated:** 2025-12-18
