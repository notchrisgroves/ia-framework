---
type: documentation
title: Blog Location Enforcement
classification: public
version: 1.0
last_updated: 2025-12-18
---

# Blog Location Enforcement - Automated Standards

**Purpose:** Prevent blog location drift through automated enforcement (hooks + validation)

**Problem Solved:** Documentation without enforcement becomes stale immediately. File-location standards documented but not enforced led to confusion between `/blog/` and `output/blog/` locations.

**Status:** ✅ Fully Enforced
**Created:** 2025-12-18
**Session:** Blog workflow testing and enforcement implementation

---

## The Problem

**Discovery (2025-12-18):**
- FILE-LOCATION-STANDARDS.md said: `output/blog/[drafts|published|docs]/` (WRONG)
- skills/writer/SKILL.md referenced: BOTH `blog/` and `output/blog/` (INCONSISTENT)
- /write command used: `blog/posts/YYYY-MM-DD-title/` (CORRECT)
- Only 1 location pattern enforced by hooks (INCOMPLETE)

**Root Cause:** Documentation created without enforcement = immediate staleness

**User Insight:** *"if its not part of a workflow/hook or other ENFORCED method, its likely WRONG"*

---

## The Solution

**Enforcement-First Approach:**

### 1. Documentation Standard (docs/FILE-LOCATION-STANDARDS.md)

**CORRECT Blog Locations:**
```
blog/YYYY-MM-DD-title/
├── draft.md              (user writes)
├── metadata.json         (status: "draft" → "published")
├── research-notes.md     (OSINT research if needed)
├── hero.png              (user uploads)
├── hero-prompt.txt       (generated)
└── tweet.txt             (generated)
```

**Key Principle:** Files NEVER move between folders. Status tracked in `metadata.json`, not folder location.

**DEPRECATED Locations:**
- ❌ `output/blog/drafts/{slug}/`
- ❌ `output/blog/published/{slug}/`
- ❌ `output/blog/research/{slug}/`
- ❌ `output/blog/docs/`
- ❌ `blog/drafts/` or `blog/published/` subfolders

### 2. Pre-Commit Hook Enforcement

**Hook 1: `validate-blog-structure.sh`**
- Validates blog post structure (slug format, required files, frontmatter)
- Enforces flat structure (all content in `blog/YYYY-MM-DD-title/`)
- Blocks commits with invalid blog posts

**Hook 2: `prevent-output-blog-references.sh`** (NEW)
- Blocks commits that reference deprecated `output/blog/` locations
- Scans: `.md`, `.ts`, `.js`, `.py`, `.sh`, `.yaml`, `.yml` files
- Skips: Historical files (`sessions/`, `plans/`, `output/`)
- Prevents documentation drift

### 3. Code References Updated

**Files Fixed:**
- `docs/FILE-LOCATION-STANDARDS.md` - Updated blog location rules
- `skills/writer/SKILL.md` - Fixed OSINT delegation output path, QA review path, newsletter collection
- `agents/writer.md` - Updated file organization reference
- `commands/write.md` - Already correct (reference implementation)

**Pattern:** Searched for ALL `output/blog` references, fixed active files, skipped historical sessions/plans

---

## Enforcement Mechanisms

### Pre-Commit Hooks

**Location:** `hooks/pre-commit/`

**Hook 1: validate-blog-structure.sh**
```bash
# Runs when blog/ files are being committed
# Validates:
# - Slug format: YYYY-MM-DD-title (lowercase, hyphens)
# - Required files: draft.md, metadata.json
# - Frontmatter fields: title, excerpt, tags, visibility, category
# - Visibility values: public, members, paid
# - JSON structure: metadata.json is valid JSON
```

**Hook 2: prevent-output-blog-references.sh**
```bash
# Runs on all staged .md/.ts/.js/.py/.sh/.yaml/.yml files
# Blocks if references:
# - output/blog/drafts
# - output/blog/published
# - output/blog/docs
# - output/blog/research
# - output/blog/[drafts|published]
```

**Installation:** See `hooks/pre-commit/README.md`

### Blog Workflow Tool

**Tool:** `skills/writer/scripts/blog-workflow.ts`

**Commands:**
```bash
# Initialize (creates blog/YYYY-MM-DD-title/)
bun run skills/writer/scripts/blog-workflow.ts init YYYY-MM-DD-title

# Generate image prompt (content-aware)
bun run skills/writer/scripts/blog-workflow.ts image-prompt YYYY-MM-DD-title

# Publish to Ghost (interactive)
bun run skills/writer/scripts/blog-workflow.ts publish YYYY-MM-DD-title

# Generate social summary
bun run skills/writer/scripts/blog-workflow.ts tweet YYYY-MM-DD-title

# Refresh STATUS.md
bun run skills/writer/scripts/blog-workflow.ts refresh
```

**Enforcement:** Tool ONLY operates on `blog/YYYY-MM-DD-title/` structure. Won't create old folder structure.

---

## Testing & Validation

### Test 1: Validate Correct Structure

```bash
# Create test post
mkdir blog/2025-12-18-test-post
cat > blog/2025-12-18-test-post/draft.md <<EOF
---
title: "Test Post"
excerpt: "Testing blog location enforcement"
tags: ["test"]
visibility: "members"
category: "framework"
---

Test content.
EOF

# Create metadata
cat > blog/2025-12-18-test-post/metadata.json <<EOF
{
  "status": "draft",
  "created": "2025-12-18"
}
EOF

# Stage and commit
git add blog/2025-12-18-test-post/
git commit -m "Test: Valid blog structure"

# RESULT: ✅ Should pass
```

### Test 2: Block Deprecated References

```bash
# Create file with deprecated reference
cat > test-file.md <<EOF
Blog posts are stored in output/blog/drafts/
EOF

# Stage and commit
git add test-file.md
git commit -m "Test: Deprecated reference"

# RESULT: ❌ Should be BLOCKED by prevent-output-blog-references.sh
```

### Test 3: Allow Historical References

```bash
# Create file in sessions/ (historical)
cat > sessions/2025-12-18-test.md <<EOF
Old workflow used output/blog/published/
EOF

# Stage and commit
git add sessions/2025-12-18-test.md
git commit -m "Test: Historical reference"

# RESULT: ✅ Should pass (sessions/ skipped)
```

---

## Migration Path

**For existing references to `output/blog/`:**

1. **Active Code/Docs:**
   - Update to `blog/YYYY-MM-DD-title/`
   - Pre-commit hook will block until fixed

2. **Historical Sessions/Plans:**
   - Leave as-is (historical record)
   - Hook automatically skips these files

3. **Old Blog Content:**
   - If you have posts in `output/blog/`, migrate them:
   ```bash
   # Move each post directory
   mv output/blog/drafts/YYYY-MM-DD-title blog/YYYY-MM-DD-title
   ```

---

## Key Decisions

### Decision 1: Flat Structure (No Folder Movement)

**Old Workflow (Deprecated):**
```
drafts/post/  →  staged/post/  →  published/123-post/
(FILES MOVE - DATA LOSS RISK)
```

**New Workflow (Enforced):**
```
blog/2025-12-17-post/  (files never move)
  └── metadata.json: { status: "draft" → "published" }
```

**Benefits:**
- ✅ Zero data loss (files never move)
- ✅ Clean git history (in-place edits)
- ✅ Easy to find (chronological folders)
- ✅ Central overview (STATUS.md)

### Decision 2: Root `/blog/` Not `output/blog/`

**Rationale:**
- Blog content is versioned framework content (not engagement output)
- `output/` is for client work and temporary results
- `/blog/` is permanent, published content
- Consistent with command structure (`/write`)

### Decision 3: Research in Same Directory

**Pattern:**
```
blog/2025-12-17-post-title/
├── draft.md
├── research-notes.md     (OSINT research notes)
└── metadata.json
```

**NOT:**
```
output/blog/research/post-title/research-notes.md  (DEPRECATED)
```

**Rationale:** Keep all blog-related files together. Easier to find, version, and manage.

---

## Rollback Procedure

**If enforcement causes issues:**

1. **Temporarily disable hooks:**
   ```bash
   # Rename hooks directory
   mv hooks/pre-commit hooks/pre-commit.disabled
   ```

2. **Make necessary commits**

3. **Re-enable and fix:**
   ```bash
   # Restore hooks
   mv hooks/pre-commit.disabled hooks/pre-commit

   # Fix violations
   # See: docs/FILE-LOCATION-STANDARDS.md
   ```

---

## Maintenance

**When to Update This Document:**
- New blog-related hooks added
- Blog workflow changes
- Enforcement mechanisms updated
- New edge cases discovered

**Testing Frequency:**
- Test hooks with each major blog workflow change
- Validate enforcement after framework updates
- Check for new `output/blog` references monthly

---

## Related Documentation

**Standards:**
- `docs/FILE-LOCATION-STANDARDS.md` - Complete file location rules
- `docs/ENFORCEMENT-METHODOLOGY.md` - General enforcement patterns
- `docs/README-MAINTENANCE-DESIGN.md` - Documentation standards

**Workflows:**
- `commands/write.md` - Complete blog workflow
- `skills/writer/SKILL.md` - Writer skill with blog content mode
- `hooks/pre-commit/README.md` - Hook documentation

**Tools:**
- `skills/writer/scripts/blog-workflow.ts` - Blog workflow automation
- `hooks/pre-commit/validate-blog-structure.sh` - Structure validation
- `hooks/pre-commit/prevent-output-blog-references.sh` - Location enforcement

---

## Success Metrics

**Enforcement is successful when:**
- ✅ Zero `output/blog/` references in active code/docs
- ✅ All blog posts follow `blog/YYYY-MM-DD-title/` structure
- ✅ Pre-commit hooks block violations before commit
- ✅ No manual fixes needed (automated enforcement works)
- ✅ Documentation stays current (hooks enforce the standard)

---

**Created:** 2025-12-18
**Problem:** Documentation drift (FILE-LOCATION-STANDARDS.md was wrong)
**Solution:** Automated enforcement via pre-commit hooks
**Status:** ✅ Fully enforced
**Framework:** Intelligence Adjacent (IA) v1.0.0
