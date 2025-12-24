# Phase 5: PUBLISH

## 🚨 CRITICAL RULES

**Before starting this phase:**
1. **Verify Phase 4 Complete** - `hero.png` MUST exist
2. **Verify ALL previous phases** - sources.txt, draft.md, qa-review.json (rating ≥4), hero.png

**You MUST:**
- Publish to Ghost CMS
- Generate tweet.md
- Update metadata.json with Ghost URLs
- Show user the published URL

**NEVER:**
- ❌ Publish without hero image
- ❌ Publish without QA approval (rating ≥4)
- ❌ Skip tweet generation
- ❌ Mark complete without Ghost URL returned
- ❌ Set wrong visibility (check frontmatter)

---

## Required Output Files

You MUST create in `blog/YYYY-MM-DD-{slug}/`:

- [ ] `tweet.md` - Social summary for X (MANDATORY)
- [ ] `metadata.json` - Updated with Ghost URLs, phase: "published"

---

## Step 1: Final Verification Checklist

**ALL must be true before publishing:**
- [ ] `sources.txt` exists (10+ sources)
- [ ] `draft.md` exists with valid frontmatter
- [ ] `qa-review.json` exists with rating ≥ 4
- [ ] `hero.png` exists
- [ ] Visibility in frontmatter is correct:
  - `public` for framework announcements, general content
  - `members` for in-depth analysis
  - `paid` for premium (rare)

**If ANY check fails: STOP. Fix the issue first.**

---

## Step 2: Publish to Ghost

**EXACT COMMAND:**
```bash
bun run skills/writer/scripts/blog-workflow.ts publish YYYY-MM-DD-{slug}
```

**What happens:**
1. Verifies hero.png exists
2. Parses frontmatter from draft.md
3. Converts markdown to HTML
4. Creates draft post in Ghost
5. Returns Ghost editor URL
6. **User uploads hero.png in Ghost editor**
7. User presses Enter to confirm
8. Script publishes post
9. Returns published URL

**Save Ghost metadata:**
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

## Step 3: Generate Tweet (MANDATORY)

**EXACT COMMAND (AI-Powered via Grok):**
```bash
python tools/openrouter/generate_tweet.py blog/YYYY-MM-DD-{slug}/draft.md "https://yourblog.ghost.io/{slug}/"
```

**Creates:** `blog/YYYY-MM-DD-{slug}/tweet.md`

**Tweet Structure (HOOK → VALUE → CTA):**
```
[HOOK - Pattern interrupt, contrarian take, surprising data, or bold claim]

[TENSION - The problem/pain point. What's broken? What do people get wrong?]

[INSIGHT - What you discovered/built. The non-obvious finding.]

[PROOF - Specific numbers, concrete outcomes (optional)]

[CTA - Link + engagement question]

---
THREAD POTENTIAL:
1. [Topic for thread expansion if post performs]
2. [Another angle]
...

ALTERNATIVE HOOKS:
1. [Different hook formula - contrarian, data, question]
...
```

**Hook Formulas:**
- Contrarian: "Most people think [X]. They're wrong."
- Data drop: "[Surprising stat]. Here's what that means."
- Question: "[Provocative question]?"
- Story: "I spent [time] doing [thing]. Here's what I learned."

**NO character limit** - User truncates for X as needed.

🚨 **You MUST create tweet.md. Workflow is NOT complete without it.**

---

## Step 4: Update Metadata

**Final metadata.json:**
```json
{
  "slug": "YYYY-MM-DD-{slug}",
  "phase": "published",
  "created": "2025-12-20T...",
  "updated": "2025-12-20T...",
  "sources_count": 12,
  "word_count": 1847,
  "qa_rating": 4.5,
  "ghost": {
    "id": "abc123xyz",
    "status": "published",
    "url": "https://...",
    "editor_url": "https://..."
  }
}
```

---

## ⛔ GATE (MANDATORY)

**Workflow NOT complete unless:**
- [ ] Ghost URL returned and saved to metadata.json
- [ ] `tweet.md` exists
- [ ] `metadata.json` phase is "published"

🚨 **If Ghost publish fails:** Debug and retry. Do not skip.
🚨 **If tweet not generated:** Generate it. Workflow incomplete without it.

---

## Checkpoint Output (FINAL)

**Show user:**
```
✅ WORKFLOW COMPLETE: Blog Post Published

📝 Post: [Title]
🔗 URL: [Ghost published URL]
👁️ Visibility: [public|members|paid]
📊 Stats: [X] words, [Y] sources, QA rating [Z]/5

📁 Files in blog/YYYY-MM-DD-{slug}/:
  - sources.txt (research)
  - research-notes.md
  - key-insights.md
  - draft.md (content)
  - qa-review.json (QA feedback)
  - hero.png (visual)
  - hero.txt (prompt)
  - tweet.md (social)
  - metadata.json (tracking)

🐦 Tweet auto-posted to X
   URL: {tweet_url from metadata}

✅ ALL PHASES COMPLETE
```

---

## Troubleshooting

**"GHOST_ADMIN_API_KEY not set"**
- Add to `.env`: `GHOST_ADMIN_API_KEY=your_key_here`

**"Invalid slug format"**
- Must be: YYYY-MM-DD-title
- Example: 2025-12-20-post-title

**Ghost publish timeout**
- Retry: `bun run skills/writer/scripts/blog-workflow.ts publish {slug}`
- Check Ghost admin panel for draft

---

**Workflow Complete. No more phases.**
