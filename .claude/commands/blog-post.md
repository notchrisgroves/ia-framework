---
name: blog-post
description: Create blog post with flat structure, content-aware prompts, and Ghost publishing
---

# /blog-post - Blog Content Creation

Create Intelligence Adjacent blog posts with prompt-chained workflow enforcement.

**Agent:** writer
**Skill:** writer
**Output:** `blog/YYYY-MM-DD-title/`

---

## 🚨 WORKFLOW ENFORCEMENT

**This command uses prompt chaining with mandatory gates.**

**You MUST:**
1. Load `commands/blog-post/00-WORKFLOW.md` to determine current phase
2. Execute ONLY the current phase prompt
3. Verify gate before proceeding to next phase
4. Show checkpoint output to user after each phase

**NEVER skip phases. NEVER proceed without gate verification.**

---

## Phase Overview

```
Phase 1: RESEARCH → Gate: sources.txt (10+ sources)
Phase 2: DRAFT → Gate: draft.md (valid frontmatter)
Phase 3: QA → Gate: rating = 5/5 (HARD GATE, may take multiple iterations)
Phase 4: VISUALS → Gate: hero.png exists
Phase 5: PUBLISH → Gate: Ghost URL + tweet.txt
```

**Prompts:** `commands/blog-post/prompts/01-05-*.md`

---

## Quick Start

```
/blog-post [topic]
```

**To start:**
1. Read `00-WORKFLOW.md` for phase detection logic
2. Check blog folder for existing files to determine phase
3. Load appropriate phase prompt from `prompts/`
4. Execute phase, verify gate, proceed

---

## When to Use

✅ **Use /blog-post when:**
- Creating Intelligence Adjacent blog content
- Documenting IA system building, tools, architecture
- Writing security testing methodology content
- Sharing practical implementation guides

❌ **Don't use if:** Writing technical documentation → use writer skill directly

---

## Prompt Files

| Phase | Prompt | Gate |
|-------|--------|------|
| 1 | `prompts/01-RESEARCH.md` | sources.txt ≥10 |
| 2 | `prompts/02-DRAFT.md` | draft.md valid |
| 3 | `prompts/03-QA.md` | rating = 5/5 |
| 4 | `prompts/04-VISUALS.md` | hero.png exists |
| 5 | `prompts/05-PUBLISH.md` | Ghost URL + tweet |

---

## Workflow

### Step 1: Initialize New Post

```bash
bun run skills/writer/scripts/blog-workflow.ts init YYYY-MM-DD-title
```

**Creates:**
- `blog/YYYY-MM-DD-title/` directory
- `draft.md` with template and frontmatter
- `metadata.json` with initial status
- Updates `blog/STATUS.md`

**Example:**
```bash
bun run skills/writer/scripts/blog-workflow.ts init 2025-12-17-blog-workflow-automation
```

---

### Step 2: Write Draft

**Edit:** `blog/YYYY-MM-DD-title/draft.md`

**Frontmatter (MANDATORY):**
```yaml
---
title: "Post Title Here"
excerpt: "SEO description 150-160 chars"
tags: ["Tag1", "Tag2", "Tag3"]
visibility: "members"  # public | members | paid
category: "framework"  # framework | security | research | tools
---
```

**Body Rules:**
- NO H1 (`#`) in body (Ghost renders title from frontmatter)
- Start with paragraph or H2 (`##`)
- Include "Sources" section with all citations
- Problem → Solution → Implementation structure
- Teaching/practical focus
- Mission-aligned (Intelligence Adjacent)

**Voice Principles:**
- First person, direct, security-professional
- "Why" before "How"
- Concrete examples over abstract theory
- Forward-thinking with SOLUTIONS

---

### Step 3: Generate Visual Assets (Automatic)

**Hero image generation (FLUX via OpenRouter):**
```bash
python tools/image-generation/generate_image.py --hero blog/YYYY-MM-DD-title
```

**What happens:**
1. Reads draft.md and extracts title from frontmatter
2. Analyzes content for topic detection (security, AI, infrastructure, etc.)
3. Selects appropriate style from topic-specific pools:
   - **Security:** Red/black alerts, green matrix, command centers
   - **AI/ML:** Purple/blue neural, gold/white clean, collaboration
   - **Infrastructure:** Orange/teal industrial, server rooms
   - **Framework:** Multi-color modular, building blocks
4. Generates image via FLUX API (30-120 seconds)
5. Saves `hero.png` and `hero.txt` (prompt used)

**Creates:**
- `blog/YYYY-MM-DD-title/hero.png` - Generated hero image
- `blog/YYYY-MM-DD-title/hero.txt` - Prompt used (for regeneration)

**Diagram export (if diagrams/ folder exists):**
```bash
python skills/diagram-generation/scripts/export-diagram.py blog/YYYY-MM-DD-title/diagrams/*.mmd
```

**Check API connectivity:**
```bash
python tools/image-generation/generate_image.py --check
```

**Manual override (custom prompt):**
```bash
python tools/image-generation/generate_image.py "custom prompt here" -o blog/YYYY-MM-DD-title/hero.png
```

---

### Step 4: Publish to Ghost

```bash
bun run skills/writer/scripts/blog-workflow.ts publish YYYY-MM-DD-title
```

**What happens:**

1. **Verifies visual assets:**
   - Checks `hero.png` exists (auto-generates if missing via FLUX)
   - Checks for exported diagrams in `diagrams/` folder

2. **Creates Ghost Draft:**
   - Parses frontmatter and converts markdown to HTML
   - Creates draft post in Ghost
   - Returns Ghost editor URL

3. **User uploads hero:**
   - Opens Ghost editor
   - Uploads `hero.png` from local folder
   - Adds alt-text from `hero.txt`
   - Reviews content
   - **Press Enter when ready**

4. **Publishes post:**
   - Updates Ghost status to 'published'
   - Updates metadata.json with Ghost URLs
   - Sets status to 'published' in metadata
   - Updates blog/STATUS.md

**Files stay in same location** - No folder moves!

**Output URLs in metadata.json:**
```json
{
  "ghost": {
    "id": "abc123xyz",
    "status": "published",
    "url": "https://yourblog.ghost.io/post-slug/",
    "editor_url": "https://yourblog.ghost.io/ghost/#/editor/post/abc123xyz"
  }
}
```

---

### Step 5: Generate Social Summary

```bash
bun run skills/writer/scripts/blog-workflow.ts tweet YYYY-MM-DD-title
```

**Creates:** `blog/YYYY-MM-DD-title/tweet.txt`

**Format:**
```
[Hook - What you built/discovered]

[Key insight - Why it matters]

[Outcome - What it enables]

[URL]

[Optional: Thread suggestions]
```

**NO character limit** - User truncates for X as needed.

User manually posts to X.

---

## File Structure

### Before Visual Assets:
```
blog/2025-12-17-post-title/
├── draft.md              (user writes)
├── metadata.json         (status: "draft")
└── diagrams/             (optional Mermaid sources)
    └── architecture.mmd
```

### After Visual Assets:
```
blog/2025-12-17-post-title/
├── draft.md
├── metadata.json         (status: "visual_assets_complete")
├── hero.png              (auto-generated via FLUX)
├── hero.txt              (prompt used)
└── diagrams/
    ├── architecture.mmd
    └── architecture.png  (exported)
```

### After Publishing:
```
blog/2025-12-17-post-title/
├── draft.md              (preserved)
├── metadata.json         (status: "published", Ghost URLs)
├── hero.png              (FLUX generated)
├── hero.txt              (prompt archive)
├── diagrams/             (preserved)
└── tweet.txt             (generated)
```

**Central tracking:**
```
blog/STATUS.md            (auto-updated table)
```

---

## STATUS.md Format

```markdown
# Blog Post Status

**Summary:**
- Total Posts: 3
- Published: 1
- Drafts: 2

## All Posts (Chronological - Newest First)

| Date | Title | Status | Visibility | Category | Ghost | Updated |
|------|-------|--------|------------|----------|-------|---------|
| 2025-12-19 | OSINT Patterns | draft | members | research | - | 2025-12-19 09:15 |
| 2025-12-17 | Security Testing | published | members | security | [View](url) | 2025-12-17 14:30 |
```

---

## Key Differences from Old Workflow

### Old (Folder-Based Status):
```
drafts/post/       → staged/post/       → published/123-post/
(FILES MOVE - DATA LOSS RISK)
```

### New (Metadata-Based Status):
```
blog/2025-12-17-post/  (files never move)
  └── metadata.json: { status: "draft" → "published" }
```

**Benefits:**
- ✅ Zero data loss (files never move)
- ✅ Clean git history (in-place edits)
- ✅ Easy to find (chronological folders)
- ✅ Central overview (STATUS.md)

---

## Agent Routing

```typescript
Task({
  subagent_type: "writer",
  model: "sonnet",
  prompt: `
Mode: blog-content
Skill: writer
Workflow: blog-post

Instructions:
1. Use blog-workflow.ts for all operations
2. Content-aware image prompts (themes from post)
3. Voice validation (first-person, IA mission)
4. Files stay in blog/YYYY-MM-DD-title/
5. STATUS.md auto-updates

Output: blog/YYYY-MM-DD-title/
`
})
```

**Agent loads:**
1. `agents/writer.md` (via PreToolUse hook)
2. `skills/writer/SKILL.md` (via load-agent-skill-context hook)
3. Tools: blog-workflow.ts, ghost-admin.ts

---

## Tools Used

**TypeScript:**
- `skills/writer/scripts/blog-workflow.ts` - Unified workflow (init, publish, tweet)
- `skills/writer/scripts/ghost-admin.ts` - Ghost Admin API wrapper

**Python:**
- `tools/image-generation/generate_image.py` - FLUX hero image generation
- `tools/image-generation/prompts.py` - Topic detection and prompt building
- `skills/diagram-generation/scripts/export-diagram.py` - Mermaid diagram export

**API Requirements:**
- `GHOST_ADMIN_API_KEY` - Ghost CMS authentication (in `.env`)
- `OPENROUTER_API_KEY` - FLUX image generation (in `.env`)

---

## Commands Reference

```bash
# Initialize new post
bun run skills/writer/scripts/blog-workflow.ts init 2025-12-17-title

# Generate hero image (automatic topic detection)
python tools/image-generation/generate_image.py --hero blog/2025-12-17-title

# Generate hero with custom prompt
python tools/image-generation/generate_image.py "custom prompt" -o blog/2025-12-17-title/hero.png

# Check image generation API
python tools/image-generation/generate_image.py --check

# Analyze title for topic detection (no generation)
python tools/image-generation/generate_image.py --analyze "Post Title Here"

# Export diagrams (if diagrams/ folder exists)
python skills/diagram-generation/scripts/export-diagram.py blog/2025-12-17-title/diagrams/*.mmd

# Publish to Ghost (interactive)
bun run skills/writer/scripts/blog-workflow.ts publish 2025-12-17-title

# Generate social summary
bun run skills/writer/scripts/blog-workflow.ts tweet 2025-12-17-title

# Refresh STATUS.md manually
bun run skills/writer/scripts/blog-workflow.ts refresh
```

**Always run from framework root** to ensure .env loads correctly.

---

## Critical Rules

1. **Flat structure** - Files NEVER move between folders
2. **Status in metadata** - Not folder location
3. **NO H1 in body** - Ghost renders title from frontmatter
4. **Sources section** - All citations required
5. **Automatic visuals** - Hero images auto-generated via FLUX (topic-aware)
6. **Diagrams convention** - Place `.mmd` files in `diagrams/` for auto-export
7. **PUBLISH ONLY** - No individual emails (weekly digest via `/newsletter`)

---

## Examples

### IA System Documentation

```
/blog-post
→ init 2025-12-17-vps-api-wrappers
→ Write draft (1,847 words)
→ Auto-generate hero (detected: infrastructure topic → orange/teal, server room)
→ Export diagrams (if diagrams/*.mmd exist)
→ Publish (files stay in blog/2025-12-17-vps-api-wrappers/)
→ Generate tweet
```

### Security Testing Methodology

```
/blog-post
→ init 2025-12-18-pentest-automation
→ Write draft (security focus)
→ Auto-generate hero (detected: security topic → red/black, command center)
→ Add architecture diagram (diagrams/attack-flow.mmd → exported)
→ Publish
→ Tweet generated
```

### AI Framework Post

```
/blog-post
→ init 2025-12-19-agent-orchestration
→ Write draft (AI/framework focus)
→ Auto-generate hero (detected: AI topic → purple/blue neural, collaboration)
→ Publish
→ Tweet generated
```

---

## Related Commands

- `/newsletter` - Weekly digest generation (collects published posts)
- `/generate-image` - Standalone image generation (non-blog use)
- Writer skill handles technical documentation directly

---

## Troubleshooting

**Issue: "GHOST_ADMIN_API_KEY not set"**
- Add to `.env`: `GHOST_ADMIN_API_KEY=your_key_here`
- Affects: publish command

**Issue: "OPENROUTER_API_KEY not found"**
- Add to `.env`: `OPENROUTER_API_KEY=sk-or-v1-...`
- Affects: hero image generation

**Issue: "No allowed providers available" (image generation)**
- Check OpenRouter dashboard for provider status
- Run `python tools/image-generation/generate_image.py --check`

**Issue: Image generation timeout**
- FLUX generation takes 30-120 seconds
- Use `--timeout 300` for extended timeout

**Issue: "Invalid slug format"**
- Must be: YYYY-MM-DD-title
- Example: 2025-12-17-post-title

**Issue: Diagrams not exporting**
- Ensure `.mmd` files are in `diagrams/` subfolder
- Check Mermaid syntax is valid
- Run `python skills/diagram-generation/scripts/export-diagram.py --check`

---

**Version:** 3.0 (Automatic visual assets)
**Last Updated:** 2025-12-19
**Framework:** Intelligence Adjacent (IA)
