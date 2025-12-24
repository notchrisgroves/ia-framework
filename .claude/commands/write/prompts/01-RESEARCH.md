# Phase 1: RESEARCH

## 🚨 CRITICAL RULES

**Before starting this phase:**
1. **Create folder if not exists** - `blog/YYYY-MM-DD-{slug}/`
2. **Initialize metadata.json** - With slug, created timestamp, phase: "research"

**You MUST:**
- Gather 10+ sources MINIMUM (not optional)
- Use WebSearch for current information
- Use Context7 for technical documentation
- Verify ALL sources are accessible URLs

**NEVER:**
- ❌ Proceed with fewer than 10 sources
- ❌ Use sources you haven't verified
- ❌ Skip OSINT background research
- ❌ Cite internal framework files as sources

---

## Required Output Files

You MUST create these files in `blog/YYYY-MM-DD-{slug}/`:

- [ ] `sources.txt` - ALL sources with URLs (10+ entries MANDATORY)
- [ ] `research-notes.md` - Complete research notes organized by topic
- [ ] `key-insights.md` - Original analysis points (what's NEW, not rehashed)
- [ ] `metadata.json` - Updated with phase: "research", sources_count

---

## Step 1: Background OSINT Research

**Delegate to osint-research skill:**
```
Caller: writer
Mode: deep (comprehensive research)

Research Plan:
- Industry trends and recent developments
- Competitor analysis (existing coverage, gaps)
- Subject matter background (history, current state)
- Expert perspectives (researchers, thought leaders)
- Real-world examples and case studies
```

**Save to:** `research-notes.md`

---

## Step 2: Technical Depth Research

**Use these tools:**

1. **WebSearch** - Current articles, news, expert opinions
2. **Context7** - Library docs, code examples, API references
3. **Primary Sources** - CVE databases, GitHub repos, official docs

**For security topics:**
- MITRE CVE database
- NVD vulnerability details
- HackerOne/Bugcrowd disclosures

**For framework/tool topics:**
- Official documentation
- GitHub repositories
- Changelog/release notes

---

## Step 3: Source Verification

**EVERY source in sources.txt MUST:**
1. Be a valid, accessible URL
2. Be relevant to the topic
3. Be from a credible source
4. Be cited in the final draft

**Format for sources.txt:**
```
1. [Title] - URL
   Key insight: [What you learned]

2. [Title] - URL
   Key insight: [What you learned]

... (10+ entries required)
```

---

## Step 4: Extract Key Insights

**In key-insights.md, document:**
- What's NEW that others haven't covered
- Unique angles or perspectives
- Practical applications
- Connections between sources

**This drives the draft content** - Not just a summary, but original analysis.

---

## ⛔ GATE (MANDATORY)

**Cannot proceed to Phase 2 (DRAFT) unless:**
- [ ] `sources.txt` exists with 10+ entries
- [ ] `research-notes.md` exists
- [ ] `key-insights.md` exists with original analysis
- [ ] `metadata.json` updated with sources_count ≥ 10

🚨 **If gate fails:** Gather more sources. Do not proceed.

---

## Checkpoint Output

**Show user:**
```
✅ PHASE 1 COMPLETE: Research
Folder: blog/YYYY-MM-DD-{slug}/
Sources gathered: [X] (minimum 10)
Research notes: [X] words
Key insights: [X] original points
Files created: sources.txt, research-notes.md, key-insights.md, metadata.json

Gate: PASSED ✓
→ Ready for Phase 2: DRAFT
```

---

**Next Phase:** Load `prompts/02-DRAFT.md`
