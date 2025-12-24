# Blog Content Workflow

**Complete workflow for Intelligence Adjacent blog posts with mandatory QA review**

**🚨 CRITICAL: QA rating ≥4 required before staging/publishing**

---

## Blog Structure

```
blog/
├── pages/                    # Static pages (about, contact, privacy, etc.)
│   ├── about.md
│   ├── contact.md
│   ├── privacy.md
│   ├── terms.md
│   ├── what-i-use.md
│   └── ia-setup-guide.md
├── posts/                    # Blog posts (date-prefixed folders)
│   └── YYYY-MM-DD-{slug}/
│       ├── draft.md          # Post content
│       ├── metadata.json     # Tracking data
│       ├── hero.png          # Hero image
│       ├── hero.txt          # Prompt used
│       ├── qa-review.json    # QA feedback
│       └── diagrams/         # Optional Mermaid diagrams
└── STATUS.md                 # Auto-generated status tracker
```

---

## Workflow Stages (SEQUENTIAL)

1. **RESEARCH** - Multi-source OSINT (10+ sources minimum)
2. **WRITING** - Deep insights, original analysis
3. **VISUAL_ASSETS** - Hero images (FLUX) + diagrams (Mermaid)
4. **QA_REVIEW** - Mandatory quality gate (rating ≥4)
5. **STANDARDS** - Validation against enforcement protocol
6. **PUBLISHING** - Ghost CMS staging + verification

---

## Stage 1: RESEARCH (Multi-Source OSINT)

**Minimum Sources:** 10+ (OSINT + Context7 + OpenRouter)

### Step 1: Delegate OSINT Background Research

```markdown
**DELEGATE to osint-research skill:**

**Caller:** writer
**Mode:** deep (comprehensive research for original content)

**Research Plan:**
  - Industry trends and emerging technologies (recent developments, market analysis)
  - Competitor analysis (what others have written, gaps in coverage)
  - Subject matter background (historical context, current state)
  - Expert perspectives (security researchers, vendor insights, thought leaders)
  - Real-world examples and case studies (breaches, implementations, lessons learned)

**Output:** blog/posts/{slug}/research-notes.md

osint-research executes dual-source methodology (WebSearch + Grok) for background intelligence.
```

### Step 2: Technical Depth Research (Writer-Specific Tools)

**Context7** (code examples, library documentation)
```typescript
// Use for technical implementations, code examples
// Official library docs, framework references
```

**OpenRouter** (multi-model technical analysis)
- Grok: Adversarial perspective, contrarian validation on technical claims
- GPT-4: Structured analysis, comprehensive technical research
- Claude: Technical accuracy, code review, security analysis

**Primary Sources** (direct technical investigation)
- CVE databases (MITRE, NVD) - vulnerability technical details
- GitHub repositories (code analysis, PoC review)
- Bug bounty disclosures (HackerOne, Bugcrowd) - exploitation details

### Research Output

**Save to:** `blog/posts/YYYY-MM-DD-{slug}/`
```
research-notes.md        # Complete research notes
sources.txt              # All sources with URLs
key-insights.md          # Original analysis points
```

**Update metadata.json:**
```json
{
  "stage": "research_complete",
  "sources_count": 12,
  "research_hours": 3.5,
  "files_created": ["research-notes.md", "sources.txt", "key-insights.md"]
}
```

---

## Stage 2: WRITING (Deep Insights Only)

**Content Tiers:**
- **Tier 1**: Deep dive (2000+ words, original research, exclusive insights)
- **Tier 2**: Analysis (1000-2000 words, expert synthesis, practical application)
- **Tier 3**: Quick guide (500-1000 words, how-to, tool overviews)

### Content Structure

**Title:** Clear, professional, no clickbait
**Hook:** Problem statement or question (first paragraph)
**Body:**
- Problem analysis with evidence
- Solution explanation with examples
- Implementation details (code/config)
- Results/outcomes (metrics, improvements)
**Sources:** At end of post (MANDATORY)

### Writing Standards

**DO:**
- Go deep or don't post (no surface-level content)
- Cite all claims with evidence
- Use humble framing ("measurements show" not "I claim")
- Teaching/practical focus
- Original insights and analysis
- Professional, knowledgeable tone

**DON'T:**
- Political content or hot takes
- Clickbait titles or excessive self-promotion
- AI detection patterns (see `reference/anti-ai-detection.md`)
- Hardcoded counts (load content-guardian.md)
- Speculation without evidence

### Save Draft

**Location:** `blog/posts/YYYY-MM-DD-{slug}/draft.md`

**Required Frontmatter:**
```yaml
---
title: "Post Title"
slug: "post-slug"
excerpt: "SEO description under 300 chars"
status: "draft"  # or "published"
visibility: "public"  # or "members", "paid"
tags: ["tag1", "tag2", "tag3"]
publishedAt: "2025-12-16T00:00:00.000Z"
---
```

**Update metadata.json:**
```json
{
  "stage": "writing_complete",
  "word_count": 1847,
  "tier": "analysis",
  "files_created": ["draft.md"]
}
```

---

## Stage 3: VISUAL ASSETS (Automatic Generation)

**Trigger:** After draft.md is complete

This stage generates all visual assets for the blog post:
1. **Hero image** - AI-generated via FLUX (automatic)
2. **Technical diagrams** - Mermaid export (convention-based)

### 3.1 Hero Image Generation (FLUX via OpenRouter)

**Tool:** `tools/image-generation/generate_image.py`
**API:** OpenRouter (FLUX model dynamically selected)

**Automatic process:**
```bash
# Generate hero from draft content analysis
python tools/image-generation/generate_image.py --hero blog/posts/YYYY-MM-DD-{slug}
```

**What happens:**
1. Reads `draft.md` and extracts title from frontmatter
2. Analyzes content for topic detection (security, AI, infrastructure, etc.)
3. Selects appropriate style from topic-specific pools:
   - **Security:** Red/black alerts, green matrix, command centers
   - **AI/ML:** Purple/blue neural, gold/white clean, collaboration
   - **Infrastructure:** Orange/teal industrial, server rooms
   - **Framework:** Multi-color modular, building blocks
   - **Career:** Professional blue/gold, workstations
4. Builds varied prompt with random selection from pools
5. Generates image via FLUX API (30-120 seconds)
6. Saves `hero.png` and `hero.txt` (prompt used)

**Topic detection keywords:** See `tools/image-generation/prompts.py`

**Output:**
```
blog/posts/YYYY-MM-DD-{slug}/
├── hero.png              # Generated hero image (~1.7-2MB PNG)
└── hero.txt              # Prompt used (for regeneration)
```

**Manual override:** If auto-generation fails or different style needed:
```bash
# Custom prompt
python tools/image-generation/generate_image.py "custom prompt" -o blog/posts/YYYY-MM-DD-{slug}/hero.png

# Check API connectivity
python tools/image-generation/generate_image.py --check

# Analyze title for topic detection (no generation)
python tools/image-generation/generate_image.py --analyze "Post Title"
```

### 3.2 Technical Diagrams (Mermaid Export)

**Tool:** `skills/diagram-generation/scripts/export-diagram.py`
**Convention:** `.mmd` files in `diagrams/` subfolder

**When to use:**
- Architecture explanations
- Process flows and workflows
- Sequence diagrams for API interactions
- Risk distribution charts
- Network topology diagrams

**File structure:**
```
blog/posts/YYYY-MM-DD-{slug}/
├── draft.md
├── diagrams/                    # Mermaid source files
│   ├── architecture.mmd         # System architecture
│   ├── workflow.mmd             # Process flow
│   └── risk-distribution.mmd    # Data visualization
```

**Export command:**
```bash
# Export all diagrams in folder
python skills/diagram-generation/scripts/export-diagram.py blog/posts/YYYY-MM-DD-{slug}/diagrams/*.mmd

# Exports to same location as source
# architecture.mmd → architecture.png
```

**Output:**
```
blog/posts/YYYY-MM-DD-{slug}/
├── diagrams/
│   ├── architecture.mmd
│   └── architecture.png          # Exported PNG
```

**Reference in draft:**
```markdown
![System Architecture](diagrams/architecture.png)
```

### 3.3 Inline Image Markers (Optional)

Add markers in draft.md for additional concept images:

```markdown
<!-- image: zero trust architecture with encrypted tunnels -->

The zero-trust model eliminates implicit trust...
```

**Processing:** Scan draft for `<!-- image: ... -->` markers and generate via FLUX.

**Output:** `blog/posts/YYYY-MM-DD-{slug}/inline-{concept-slug}.png`

### Visual Assets Checklist

**Automatic (always generated):**
- [ ] `hero.png` - Topic-aware hero image via FLUX
- [ ] `hero.txt` - Prompt used for regeneration

**Convention-based (if diagrams/ folder exists):**
- [ ] `diagrams/*.png` - Exported from `.mmd` sources

**Optional (if markers present):**
- [ ] `inline-*.png` - Concept images from markers

**Update metadata.json:**
```json
{
  "stage": "visual_assets_complete",
  "hero_generated": true,
  "hero_topic": "security",
  "diagrams_exported": 3,
  "files_created": ["hero.png", "hero.txt", "diagrams/architecture.png"]
}
```

---

## Stage 4: QA REVIEW (MANDATORY GATE)

**DELEGATE to qa-review skill (support skill):**

**Caller context:**
- **Calling skill:** writer
- **Review Type:** peer-review
- **Review Target:** `blog/posts/YYYY-MM-DD-{slug}/draft.md`
- **Depth Level:** standard
- **Requirements:**
  - Technical accuracy verification
  - Citation validation (all URLs working)
  - Evidence-to-claim alignment
  - SEO and readability checks
  - Intelligence Adjacent voice consistency
  - Rating requirement: ≥4 to publish
- **Output:** `blog/posts/YYYY-MM-DD-{slug}/qa-review.json`

**qa-review validates:**
- Technical accuracy (code examples work, methodology sound)
- Content quality (depth, insights, value)
- Style compliance (humble, teaching-focused, professional)
- Completeness (all claims backed by evidence)

**Rating Scale:**
- **5**: Exceptional (publish immediately)
- **4**: Strong (minor edits, publish)
- **3**: Needs work (major revision required)
- **2**: Weak (significant rewrite needed)
- **1**: Poor (start over)

**If rating < 4:**
1. Review QA feedback (saved to `qa-review.json`)
2. Apply corrections
3. Save corrected draft: `draft-v2.md`
4. Re-invoke QA if major changes

**QA Output:** `blog/posts/YYYY-MM-DD-{slug}/qa-review.json`

**Update metadata.json:**
```json
{
  "stage": "qa_complete",
  "qa_rating": 4.5,
  "corrections_applied": true,
  "files_created": ["qa-review.json", "draft-v2.md"]
}
```

**🚨 GATE: Cannot proceed to publishing if rating < 4**

---

## Stage 5: STANDARDS VALIDATION (MANDATORY)

**Checklist (EVERY post):**

### Content Standards
- [ ] **NO H1 in body** (Ghost renders title from frontmatter)
- [ ] **Sources section present** at end of post
- [ ] **NO internal file references** in Sources (only public URLs/repos)
- [ ] **Humble framing** throughout (no ego language)
- [ ] **Teaching/practical focus** evident
- [ ] **Mission alignment** verified

### Infrastructure Content (if applicable)
- [ ] **NO sensitive information:**
  - Real IP addresses (use `X.X.X.X` placeholders)
  - Real hostnames (use `example.com`)
  - SSH keys with usernames
  - VPS/cloud account IDs
- [ ] **Configuration consistency:**
  - Docker ports correct
  - DNS aliases consistent
  - Multi-post series uses same terminology

### Problem-Solution Linking
- [ ] **Every problem has solution link** (skill/process/resource)
- [ ] **Solutions verified** (actually exist and work)
- [ ] **Optional CTA before Sources:**
```markdown
**Ready to implement [solution]?**
→ Use /[command] for guided workflow
→ Multi-model research validates best approach
```

**See:** `library/prompts/content-guardian.md` for complete enforcement protocol

---

## Stage 6: PUBLISHING (Ghost CMS)

### 6.1 Verify Visual Assets

**Check from Stage 3:**
- `hero.png` exists (auto-generated via FLUX)
- `hero.txt` exists (prompt for regeneration if needed)
- `diagrams/*.png` exported (if `.mmd` sources exist)

**If hero.png missing:** Auto-generate on publish (fallback)
```bash
python tools/image-generation/generate_image.py --hero blog/posts/YYYY-MM-DD-{slug}
```

### 6.2 Create Ghost Draft

**Use Ghost publishing tool:**
```bash
cd skills/writer/scripts
bun run ghost-publish.ts ../../blog/posts/YYYY-MM-DD-{slug}/draft.md
```

**Script performs:**
- Parse frontmatter (title, slug, excerpt, tags, visibility)
- Create/update Ghost post via Admin API
- Upload hero image
- Set visibility tier (public/members/paid)
- Return Ghost post URL

**Save Ghost metadata to metadata.json:**
```json
{
  "ghost_id": "673a1b2c3d4e5f6a7b8c9d0e",
  "ghost_url": "https://intelligenceadjacent.com/p/post-slug/",
  "ghost_admin_url": "https://intelligenceadjacent.com/ghost/#/editor/post/673a1b2c3d4e5f6a7b8c9d0e",
  "status": "published",
  "visibility": "public"
}
```

### 6.3 Ghost Admin Verification

**Manual checks (CRITICAL):**
- [ ] NO duplicate H1 in rendered post
- [ ] Formatting renders correctly
- [ ] Code blocks have syntax highlighting
- [ ] Tables/charts display properly
- [ ] Hero image loads correctly
- [ ] Visibility tier set correctly (public/members/paid)
- [ ] Tags applied
- [ ] Excerpt displays on cards

**Return Ghost Admin URL to user for review**

### 6.4 Update Status

**After publishing in Ghost:**

1. Update frontmatter in `draft.md`:
```yaml
status: "published"
publishedAt: "2025-12-19T12:00:00.000Z"
```

2. Update `metadata.json` with Ghost IDs

3. `STATUS.md` auto-updates on next /write run

---

## Pages vs Posts

### Pages (`blog/pages/`)

**Static content** that rarely changes:
- About, Contact, Privacy, Terms
- Setup guides, What I Use

**Frontmatter:**
```yaml
---
title: "About"
slug: "about"
status: "published"
page: true
---
```

**Publishing:** Direct to Ghost as pages (not posts)

### Posts (`blog/posts/`)

**Date-prefixed folders** with full workflow:
- Each post is a folder: `YYYY-MM-DD-{slug}/`
- Contains draft.md, metadata.json, assets

**Naming:** Date prefix enables chronological sorting

---

## Files Created (Complete Workflow)

```
blog/posts/YYYY-MM-DD-{slug}/
├── research-notes.md           # Research phase
├── sources.txt                 # Sources inventory
├── key-insights.md             # Original analysis
├── draft.md                    # Post content
├── draft-v2.md                 # After QA corrections (if needed)
├── qa-review.json              # QA feedback
├── hero.png                    # Hero image (FLUX via OpenRouter)
├── hero.txt                    # Prompt used for hero
├── diagrams/                   # Technical diagrams (optional)
│   ├── architecture.mmd        # Mermaid source
│   └── architecture.png        # Exported PNG
└── metadata.json               # Complete tracking + Ghost IDs
```

---

## Research Depth Variations

### Deep Research (4-6 hours)
**Use for:** Trending topics, original research, exclusive insights
**Sources:** 15+ (deep OSINT, primary sources, multi-model validation)
**Output:** 2000+ words, Tier 1 content

### Project Documentation (2-3 hours)
**Use for:** Framework features, architecture explanations
**Sources:** Internal docs + 5-8 external validation sources
**Output:** 1000-2000 words, Tier 2 content

### Standard Post (2-4 hours)
**Use for:** Tool overviews, quick guides, how-tos
**Sources:** 10+ standard research
**Output:** 500-1000 words, Tier 3 content

---

## Quality Standards

**Remember:** Every post represents Intelligence Adjacent reputation
**Standard:** Professional, knowledgeable, humble, teaching-focused
**Gate:** QA rating ≥4 (non-negotiable)
**Mission:** Deep insights that upgrade human intelligence

**No shortcuts. Quality over quantity. Always.**

---

**See Also:**
- `reference/ghost-api.md` - Ghost CMS integration
- `reference/hero-images.md` - Hero image generation (manual fallback)
- `tools/image-generation/` - FLUX automatic hero generation
- `skills/diagram-generation/` - Mermaid diagram export
- `commands/generate-image.md` - Standalone image generation command
- `library/prompts/content-guardian.md` - Enforcement protocol
