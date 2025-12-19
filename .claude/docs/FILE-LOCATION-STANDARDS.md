---
type: documentation
title: File Location Standards
classification: public
version: 1.2
last_updated: 2025-12-17
---

# File Location Standards - MANDATORY ROUTING RULES

**Purpose:** Single source of truth for where different document types belong in the Intelligence Adjacent framework.

**Status:** ✅ Active Enforcement
**Version:** 1.0
**Last Updated:** 2025-11-23

---

## Overview

This document solves the recurring problem: **"Why is this permanent doc in scratchpad/"**

The framework has clear locations for different document types. Following these rules ensures:
- ✅ Permanent docs survive long-term
- ✅ Version control includes important files
- ✅ Easy to find documentation
- ✅ No accidental deletion of critical work

---

## Document Type Matrix

| Document Type | Location | When Created | Lifespan | Example |
|---|---|---|---|---|
| **User Input Files** | `input/` | User provides | Indefinite | resume.md, cliftonstrengths.pdf |
| **Design Plans** | `plans/YYYY-MM-DD-description.md` | Before implementation | Task duration | 2025-12-14-subdirectory-claude-md-design.md |
| **Permanent Analysis** | `docs/[category]/` | Infrastructure decisions | Indefinite | gap-analysis.md, audit.md |
| **Skill Methodology** | `skills/[skill]/SKILL.md` | Methodology updates | Indefinite | SKILL.md sections, PRINCIPLES.md |
| **Session Checkpoints** | `sessions/YYYY-MM-DD-project-name.md` | Multi-session projects | Project duration | sessions/2025-12-11-blog-post.md |
| **Engagement Data** | `output/engagements/[type]/[id]/` | Client work | Per contract | SCOPE.md, FINDINGS.md |
| **Blog Content** | `blog/YYYY-MM-DD-title/` | Blog work | Indefinite | blog/2025-12-17-post-title/ |
| **Temporary Analysis** | `scratchpad/YYYYMMDD-HHMMSS/` | Session iteration | Session only | Quick notes, explorations |

---

## Decision Rules

### Rule 0: Plans vs Sessions vs Docs (Critical Distinction)

**Three similar-looking locations with DIFFERENT purposes:**

| Directory | Purpose | When to Use | Lifecycle |
|---|---|---|---|
| `plans/` | **Design BEFORE execution** | Plan mode, research, analysis | Delete after task complete |
| `sessions/` | **Progress DURING execution** | Multi-session tracking, resume context | Keep until project complete |
| `docs/` | **Permanent architecture decisions** | Framework changes, standards | Keep indefinitely |

**Example workflow:**
1. **Plan mode:** Create `plans/2025-12-14-feature-design.md` with research and design decisions
2. **Implementation:** Create `sessions/2025-12-14-feature-name.md` to track progress across sessions
3. **After completion:** If it changed architecture, add section to `docs/architecture/[topic].md`, then delete plan and session files

**Key insight:** Plans and sessions are WORKING FILES (gitignored). Docs are PERMANENT (version controlled).

### Rule 0.5: User Input Files

**User-provided files that skills/commands consume.**

**CRITICAL: Input mirrors Output structure.** If a skill outputs to `output/{category}/`, its inputs come from `input/{category}/`.

| Category | Input Location | Output Location | Used By |
|---|---|---|---|
| Career | `input/career/` | `output/career/` | /job-analysis, career skill |

**Career input files:**

| File | Path | Purpose |
|---|---|---|
| Resume | `input/career/resume.md` | Master resume (Markdown) |
| CliftonStrengths | `input/career/cliftonstrengths-all34.pdf` | Full 34 themes (optional) |

**Key principles:**
- `input/` mirrors `output/` directory structure
- `input/` is for files the USER provides (not generated)
- `output/` is for files the FRAMEWORK generates
- When creating a new skill that needs input files, create `input/{category}/` matching `output/{category}/`
- Input files are version controlled (private repo)

---

### Rule 1: Permanent vs Temporary Test

**Ask this question before creating ANY file:**

> "If I delete this file tomorrow, would the project be damaged?"

- **YES (damaged)** → Permanent document → Use `docs/`, `skills/`, or project location
- **NO (not damaged)** → Temporary work → Use `scratchpad/`

**Examples:**
- ✅ Permanent: "Public migration gap analysis" (project plan)
- ✅ Permanent: "Server deployment audit" (infrastructure docs)
- ✅ Permanent: "Blog content roadmap" (strategic planning)
- ❌ Temporary: "Quick test of OpenRouter models" (one-off exploration)
- ❌ Temporary: "Session notes 2025-11-23" (throwaway)

### Rule 2: Analysis Document Locations

**System Infrastructure Analysis** → `docs/[category]/`
- Framework architecture decisions
- Migration planning
- System audits
- Standards and best practices

**Categories:**
- `docs/public-migration/` - Public repo preparation
- `docs/architecture/` - System design docs
- `docs/best-practices/` - Framework standards
- `docs/troubleshooting/` - How-to documentation

**Skill Methodology Updates** → `skills/[skill]/SKILL.md`
- Add as new section in existing SKILL.md
- Updates to workflows or methodologies
- Don't create separate methodology files

**Design Plans** → `plans/YYYY-MM-DD-description.md`
- Analysis and planning BEFORE implementation starts
- Research findings and design decisions
- Multiple implementation approaches considered
- Used in plan mode, referenced during execution

**Session Decisions** → `sessions/YYYY-MM-DD-project-name.md`
- Multi-session project tracking DURING implementation
- Current phase and blockers
- Resume context for next session
- Progress updates across multiple sessions

**Engagement Findings** → `output/engagements/[type]/[id]/`
- Client scope documentation
- Testing results
- Reports and findings

### Rule 3: Blog-Specific Rules (Most Common Case)

**Blog content uses FLAT STRUCTURE (no folder movement):**

| Content Type | Location | Examples |
|---|---|---|
| **All Blog Files** | `blog/YYYY-MM-DD-title/` | Posts, research, images, metadata |

**Key Principle:** Files NEVER move between folders. Status tracked in `metadata.json`, not folder location.

**Structure:**
```
blog/2025-12-17-post-title/
├── draft.md              (user writes)
├── metadata.json         (status: "draft" → "published")
├── research-notes.md     (OSINT research if needed)
├── hero.png              (user uploads)
├── hero-prompt.txt       (generated)
└── tweet.txt             (generated)
```

**❌ NEVER:**
- Put blog content in `scratchpad/` (files may be deleted, won't be version controlled)
- Put blog content in `output/blog/` (deprecated location)
- Create `blog/drafts/` or `blog/published/` subfolders (old workflow, deprecated)
- Move files between folders to change status (use metadata.json instead)

### Rule 4: When to Move From Scratchpad

Files should be moved from `scratchpad/` to permanent location if:

1. **Referenced in next session** - You'll need it again
2. **Contains decisions** - Documents choices made
3. **Project planning** - Roadmaps, gap analysis, audits
4. **Infrastructure docs** - Standards, architecture, guides
5. **Session lasted >2 hours** - Significant work product

**Move BEFORE committing to git.**

### Rule 5: Scratchpad-Only Content

**Only these belong in scratchpad/:**
- Quick experiments and tests
- One-off analysis that won't be referenced
- Session working notes (not checkpoints)
- Temporary outputs from tools
- Draft explorations before permanent docs

**Scratchpad files should be:**
- Dated (YYYYMMDD-HHMMSS)
- Disposable (can be deleted)
- Not referenced by other docs

---

## Agent Responsibilities

### All Agents MUST

**1. Load this file at startup:**
```markdown
## SESSION STARTUP REQUIREMENT
1. Read CLAUDE.md (bootloader)
2. Read docs/FILE-LOCATION-STANDARDS.md (file location routing) ← THIS FILE
3. Read sessions/YYYY-MM-DD-project.md (if exists)
4. Read skills/[skill]/SKILL.md (skill context)
```

**2. Classify documents before creation:**
- Determine: Permanent or Temporary?
- Select correct location based on document type
- Create file in proper location FIRST TIME (don't move later)

**3. Before session end:**
- Review files created in `scratchpad/`
- Move any permanent docs to correct location
- Update session file with file references

---

## Common Mistakes & Fixes

### Mistake 1: "Gap Analysis" in Scratchpad

**❌ Wrong:**
```
scratchpad/PUBLIC-REPO-GAP-ANALYSIS-2025-11-23.md
```

**✅ Correct:**
```
docs/public-migration/gap-analysis.md
```

**Why:** Gap analysis is permanent project planning, not temporary work.

### Mistake 2: "Audit" Documentation in Scratchpad

**❌ Wrong:**
```
scratchpad/SERVERS-DEPLOYMENT-AUDIT-2025-11-23.md
```

**✅ Correct:**
```
docs/public-migration/servers-audit.md
```

**Why:** Audit documentation is infrastructure analysis, belongs in docs/.

### Mistake 3: Updating CLAUDE.md for Engagement Setup

**❌ Wrong:**
```
Updating CLAUDE.md when creating new pentest/audit engagement
```

**✅ Correct:**
```
output/engagements/[type]/[client-name]-YYYY-MM/
```

**Why:** Engagements are DATA (client work), not infrastructure. CLAUDE.md is for system-level changes only (new skills, agents, workflows). Create engagement directories and copy templates from skills - never update CLAUDE.md for individual engagements.

### Mistake 4: Blog Roadmap in Scratchpad

**❌ Wrong:**
```
scratchpad/BLOG-CONTENT-ROADMAP-2025-11-23.md
```

**✅ Correct:**
```
docs/blog/content-roadmap.md
```

**Why:** Blog planning is permanent project documentation, not blog content itself.

### Mistake 5: Timestamped Permanent Docs

**❌ Wrong pattern:**
```
ANY-PERMANENT-DOC-2025-11-23.md
```

**✅ Correct pattern:**
```
descriptive-name.md  (no timestamp)
```

**Why:** Timestamps signal "temporary". Permanent docs use descriptive names.

---

## Quick Reference Decision Tree

```
Creating a file?
  │
  ├─ Is it a USER-PROVIDED input file (resume, credentials)?
  │   └─ YES → input/{category}/ (mirrors output/{category}/)
  │
  ├─ Is it design/planning BEFORE implementation?
  │   └─ YES → plans/YYYY-MM-DD-description.md
  │
  ├─ Is it blog content (posts, research, images)?
  │   └─ YES → blog/YYYY-MM-DD-title/
  │
  ├─ Is it client engagement work?
  │   └─ YES → output/engagements/[type]/[id]/
  │
  ├─ Is it infrastructure analysis (gap, audit, roadmap)?
  │   └─ YES → docs/[category]/
  │
  ├─ Is it skill methodology update?
  │   └─ YES → skills/[skill]/SKILL.md (add section)
  │
  ├─ Is it multi-session project tracking DURING work?
  │   └─ YES → sessions/YYYY-MM-DD-project-name.md
  │
  └─ Is it temporary exploration/notes?
      └─ YES → scratchpad/YYYYMMDD-HHMMSS/
```

---

## Related Documentation

- `docs/session-checkpoint-enforcement.md` - Session state rules
- `docs/hierarchical-context-loading.md` - Context architecture
- `docs/directory-structure.md` - Framework organization

---

**This is a MANDATORY document.** All agents must load and follow these rules.

**Questions?** These rules are authoritative. If unclear, ask user before creating files.

**Version:** 1.0
**Status:** ✅ Active Enforcement
**Framework:** Intelligence Adjacent (IA)
