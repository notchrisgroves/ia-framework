# Phase 2: DRAFT

## 🚨 CRITICAL RULES

**Before starting this phase:**
1. **Verify Phase 1 Complete** - `sources.txt` MUST exist with 10+ sources
2. **Read research files** - Load research-notes.md and key-insights.md

**You MUST:**
- Write deep, original content (not surface-level summaries)
- Cite ALL claims with evidence from sources.txt
- Include Sources section at end of post
- Use humble framing ("measurements show" not "I claim")
- Focus on teaching and practical application

**NEVER:**
- ❌ Skip reading the research files first
- ❌ Write without citing sources
- ❌ Use H1 (`#`) in the body (Ghost renders title from frontmatter)
- ❌ Add clickbait titles or excessive self-promotion
- ❌ Hardcode counts (e.g., "18 skills")
- ❌ Reference internal framework files in Sources section

---

## Required Output Files

You MUST create in `blog/YYYY-MM-DD-{slug}/`:

- [ ] `draft.md` - Complete post with valid frontmatter
- [ ] `metadata.json` - Updated with phase: "draft", word_count

---

## Step 1: Read Research Files

**MANDATORY - Load these first:**
```
Read: blog/YYYY-MM-DD-{slug}/sources.txt
Read: blog/YYYY-MM-DD-{slug}/research-notes.md
Read: blog/YYYY-MM-DD-{slug}/key-insights.md
```

**Do NOT write without reading research first.**

---

## Step 2: Write Draft with Valid Frontmatter

**Required Frontmatter (MANDATORY):**
```yaml
---
title: "Post Title Here"
slug: "post-slug"
excerpt: "SEO description 150-160 chars - compelling hook"
status: "draft"
visibility: "public"  # public | members | paid
tags: ["Tag1", "Tag2", "Tag3"]
category: "framework"  # framework | security | research | tools
---
```

**Visibility Classification (AUTOMATED):**

Apply this decision tree to determine visibility:

```
IF title contains ["Deep Dive", "Building", "Creating", "Implementing",
                   "Extending", "Custom", "Internals", "Tutorial"]
   OR category == "implementation"
   → visibility: "paid"

ELSE IF title contains ["Guide", "Setup", "Hardening", "Methodology",
                        "Foundations", "Lab", "Professional", "Infrastructure"]
   OR category in ["security", "infrastructure"]
   → visibility: "members"

ELSE IF title contains ["Architecture", "Overview", "Introduction", "Analysis",
                        "Comparison", "Announcement", "Reality Check", "Companion"]
   OR category in ["commentary", "announcement", "framework", "tools"]
   → visibility: "public"

ELSE → visibility: "members" (safe default)
```

**Tier Definitions:**
| Tier | Purpose | Who Sees It |
|------|---------|-------------|
| `public` | What & Why (concepts, analysis, announcements) | Everyone |
| `members` | How to Use (methodology, setup guides) | Free subscribers |
| `paid` | How to Build/Extend (implementation, customization) | Paid members |

**Override (when classification doesn't fit):**
```yaml
visibility: "public"
visibility_override: true
visibility_reason: "Launch promotion - temporary free access"
```

---

## Step 2b: Add Membership CTA Footer

**MANDATORY - Add before Sources section:**

```markdown
---

*The Intelligence Adjacent framework is free and open source. If this helped you, consider [joining as a Lurker](https://yourblog.ghost.io/#/portal/signup) (free) for methodology guides, or [becoming a Contributor](https://yourblog.ghost.io/#/portal/signup) ($5/mo) for implementation deep dives and to support continued development.*

---
```

**This CTA is REQUIRED on all posts.** Do not skip.

**CTA Variations (choose based on post type):**

For PUBLIC posts (concepts/analysis):
> *Want to put this into practice? Lurkers get methodology guides. Contributors get implementation deep dives.*

For MEMBERS posts (methodology):
> *Ready to customize the framework? Contributors get deep dives on building custom skills and extending workflows.*

For PAID posts (implementation):
> *Thanks for supporting the mission. Your contribution funds continued development of the framework.*

---

## Step 3: Content Structure

**Post Structure:**
1. **Hook** - Problem statement or question (first paragraph)
2. **Problem Analysis** - Evidence-backed problem description
3. **Solution Explanation** - Clear, practical solution
4. **Implementation** - Code/config examples
5. **Results/Outcomes** - Metrics, improvements, lessons
6. **Sources** - ALL citations (MANDATORY section)

**Content Tiers:**
- **Tier 1**: 2000+ words, deep dive, original research
- **Tier 2**: 1000-2000 words, analysis, expert synthesis
- **Tier 3**: 500-1000 words, how-to, quick guides

---

## Step 4: Writing Standards

**DO:**
- ✅ Go deep or don't post (no surface-level content)
- ✅ Cite all claims with evidence
- ✅ Use humble framing
- ✅ Focus on teaching/practical application
- ✅ Include original insights from key-insights.md
- ✅ Professional, knowledgeable tone

**DON'T:**
- ❌ Political content or hot takes
- ❌ Clickbait titles
- ❌ AI detection patterns (see anti-ai-detection.md)
- ❌ Speculation without evidence
- ❌ H1 headers in body

---

## Step 5: Citation Style (Hybrid Approach)

**Use BOTH inline links AND a Sources section:**

### Inline Citations (For Key Claims)

**Link inline when citing:**
- Specific statistics ("reduces accuracy by [9.5%](url)")
- CVE numbers ("[CVE-2025-49596](url)")
- Research study titles ("[arXiv: Help or Hurdle?](url)")
- Direct quotes or paraphrases
- Tool/product announcements

**Example:**
```markdown
Research shows MCP [reduces accuracy by 9.5%](https://arxiv.org/...) across six LLMs.
```

**DON'T over-link:**
- General statements don't need inline links
- One link per claim is sufficient
- Avoid linking every sentence

### Sources Section (Comprehensive Reference)

**At end of draft.md:**
```markdown
## Sources

### Category Name
- [Source Title](URL)
- [Source Title](URL)

### Another Category
- [Source Title](URL)
...
```

**EVERY source from sources.txt MUST appear here, categorized.**

**Purpose:** Gives readers a comprehensive reference list while inline links provide immediate credibility for key claims.

---

## ⛔ GATE (MANDATORY)

**Cannot proceed to Phase 3 (QA) unless:**
- [ ] `draft.md` exists
- [ ] Frontmatter is valid (title, slug, excerpt, visibility, tags)
- [ ] Sources section present at end (categorized)
- [ ] Inline links for key statistics and CVEs
- [ ] Word count ≥ 500 (Tier 3 minimum)
- [ ] NO H1 headers in body
- [ ] `metadata.json` updated with word_count

🚨 **If gate fails:** Fix issues. Do not proceed.

---

## Checkpoint Output

**Show user:**
```
✅ PHASE 2 COMPLETE: Draft
File: blog/YYYY-MM-DD-{slug}/draft.md
Word count: [X] words
Tier: [1|2|3]
Visibility: [public|members|paid]
Sources cited: [X]
Frontmatter: Valid ✓

Gate: PASSED ✓
→ Ready for Phase 3: QA Review
```

---

**Next Phase:** Load `prompts/03-QA.md`
