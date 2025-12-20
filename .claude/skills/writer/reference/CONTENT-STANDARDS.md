# Content Standards & Quality Requirements

**Intelligence Adjacent content standards - Quality = Career Reputation**

---

## Core Philosophy

**Intelligence Adjacent builds systems that augment human intelligence, not replace it.**

Every published piece represents this mission and our professional reputation.

**Standard:** Professional, knowledgeable, humble, teaching-focused
**Quality Gate:** QA rating ≥4 (blog posts only)
**Mission:** Deep insights that upgrade human capabilities

---

## Writing Standards

### Voice & Tone

**Professional:**
- Clear, structured writing
- Technical accuracy
- Evidence-based claims
- Proper citations

**Knowledgeable:**
- Deep expertise evident
- Real-world experience
- Practical insights
- Not surface-level aggregation

**Humble:**
- "Measurements show" NOT "I claim"
- "Data indicates" NOT "I believe"
- Focus on findings, not ego
- Credit sources properly

**Teaching-Focused:**
- Readers learn something valuable
- Actionable takeaways
- Reproducible examples
- Practical application

---

## Content Quality Requirements

### Depth Standards

**Tier 1: Deep Dive (2000+ words)**
- Original research or exclusive insights
- 15+ sources with primary research
- Novel analysis or perspective
- Advanced technical detail

**Tier 2: Analysis (1000-2000 words)**
- Expert synthesis of multiple sources
- 10-12 sources with multi-model research
- Practical application focus
- Clear technical explanations

**Tier 3: Quick Guide (500-1000 words)**
- Focused how-to or tool overview
- 8-10 sources minimum
- Step-by-step instructions
- Beginner-friendly

**NO surface-level content** - Go deep or don't post

### Research Standards

**Minimum Sources:** 10+ for ANY published content

**Source Priority:**
1. **Primary sources** - Official docs, vendor advisories, CVE databases
2. **Code analysis** - GitHub repos, library documentation (Context7)
3. **Multi-model validation** - Grok (adversarial), GPT-4 (structured), Claude (technical)
4. **Industry sources** - Security blogs, academic papers, whitepapers

**Source Quality:**
- Authoritative (not random blogs)
- Current (within 6-12 months for security topics)
- Verifiable (reproducible claims)
- Diverse perspectives (not echo chamber)

### Evidence Requirements

**All claims must be:**
- Backed by sources (cited in Sources section)
- Reproducible by readers
- Based on evidence, not speculation
- Technically accurate

**Code examples must:**
- Actually work (tested)
- Include necessary context
- Show good practices
- Be safe to run

---

## Prohibited Content

### NEVER Publish

**Political content:**
- Hot takes on current events
- Partisan positions
- Social commentary unrelated to tech
- Controversial non-technical topics

**Clickbait:**
- Exaggerated titles
- Misleading headlines
- Engagement bait
- "You won't believe..." style

**Excessive self-promotion:**
- "Look how smart I am" framing
- Ego-driven language
- Self-congratulation
- Humble-bragging

**AI detection patterns:**
- "In the ever-evolving landscape..."
- "It's important to note that..."
- "Delve into"
- Excessive hedging

**Hardcoded counts:**
- "18 skills" (load content-guardian.md instead)
- "28 commands" (creates maintenance debt)
- Any specific component counts

### Allowed with Care

**Contrarian takes:**
- ✅ Evidence-based disagreement with common advice
- ❌ Contrarian for attention/engagement

**Strong opinions:**
- ✅ Backed by data and experience
- ❌ Unsubstantiated claims

**Personal stories:**
- ✅ Relevant to technical lesson
- ❌ Off-topic anecdotes

---

## Structural Standards

### Required Elements

**Every blog post must have:**
- [ ] Clear, professional title
- [ ] Hook/problem statement (first paragraph)
- [ ] Body with evidence and examples
- [ ] **Sources section** (at end, before CTAs)
- [ ] Optional CTA (problem-solution linking)

### NO H1 in Body

**Ghost renders title from frontmatter** - Do NOT include H1 in markdown body

**Correct:**
```yaml
---
title: "Post Title"
---

## First Section (H2)
Content...

## Second Section (H2)
Content...
```

**Wrong:**
```markdown
# Post Title  ← DUPLICATE H1, will break Ghost rendering
```

### Sources Section (MANDATORY)

**At end of every post:**
```markdown
## Sources

- [Source Title](https://example.com) - Description
- [Another Source](https://example.com) - Description
- [Third Source](https://example.com) - Description
```

**Sources must be:**
- Public URLs (no internal file references)
- Public repos (GitHub, GitLab with public access)
- Reproducible resources (readers can access)

**NOT allowed in Sources:**
- `sessions/YYYY-MM-DD-project.md` (internal)
- `~/.claude/skills/name/` (private paths)
- `C:/Users/Chris/...` (local paths)
- Paid content behind paywalls (unless noted)

---

## Infrastructure Content Special Rules

**For posts about infrastructure/deployment:**

### Safety Requirements

**NEVER expose:**
- ❌ Real IP addresses (use `X.X.X.X`, `Y.Y.Y.Y` placeholders)
- ❌ Real hostnames (use `example.com`, `service.example.com`)
- ❌ SSH key paths with usernames (use `~/.ssh/keyname`)
- ❌ Real VPS/cloud account IDs
- ❌ Actual credentials (even redacted keys)

### Consistency Requirements

**Validate:**
- [ ] Internal cross-references use actual slugs (no `(#)` placeholders)
- [ ] Access URLs match configured service names
- [ ] Docker port bindings correct for documented use case
- [ ] DNS aliases consistent (`.internal` vs `.twingate` - pick one)
- [ ] Multi-post series uses consistent terminology

---

## Problem-Solution Linking (MANDATORY)

**Rule:** Every problem mentioned MUST link to a solution

**Valid solutions:**
- Framework skill (with `/command` invocation)
- Documented process (in framework docs)
- External resource (tool, service, guide)

**CTA Pattern (opt-in, never forced):**
```markdown
**Ready to implement [solution]?**
→ Use /[command] for guided workflow
→ Multi-model research validates best approach
```

**Pre-Publishing Checklist:**
1. [ ] List all problems/pain points mentioned
2. [ ] Map each to solution (skill/process/resource)
3. [ ] Verify solution exists and accessible
4. [ ] Add "Ready to implement?" CTA before Sources
5. [ ] QA review validates solution mapping

**NEVER:**
- Complain about problems without solutions
- Force solutions (always opt-in pattern)
- Link to non-existent skills
- Claim to solve something we don't

**Enforcement:** If problem has no solution → Either create solution skill OR remove problem from post

---

## Quality Assurance

### QA Review (Blog Posts Only)

**Process:**
1. Complete draft
2. Invoke qa-review agent (advisor agent with QA mode)
3. Receive rating (1-5 scale)
4. If rating < 4: Apply corrections and re-review
5. If rating ≥4: Proceed to publishing

**Rating Requirements:**
- **Blog posts:** Rating ≥4 MANDATORY
- **Technical docs:** QA optional (accuracy via peer review)
- **Security reports:** Technical validation required

### Standards Validation Checklist

**Before publishing ANY content:**
- [ ] NO H1 in body
- [ ] Sources section present
- [ ] NO internal file references in Sources
- [ ] Humble framing throughout
- [ ] Teaching/practical focus evident
- [ ] Mission alignment verified
- [ ] Problem-solution linking validated
- [ ] Infrastructure content safety checked (if applicable)

---

## Enforcement Protocol

**Automated checks:**
- Content Guardian (no hardcoded counts)
- Path validator (no old framework paths)
- Standards validator (H1, Sources section)

**Manual checks:**
- QA review (rating ≥4 for blog posts)
- Peer review (technical docs)
- Security validation (reports)

**See:** `library/prompts/content-guardian.md` for complete enforcement rules

---

## Examples

### Good Example

```markdown
---
title: "How MCP Code API Wrappers Reduce Token Usage by 99%"
---

## The Problem with MCP Tool Verbosity

When using Model Context Protocol tools in security testing, token costs
become prohibitive. Measurements from our pentest engagements show that
raw MCP tool outputs consume 50,000+ tokens per reconnaissance phase.

## Two-Layer Wrapper Architecture

Our solution implements a two-layer pattern:
...

[Evidence-based explanation with code examples]
...

## Results

Testing across 5 engagements showed:
- Token usage: 50K → 500 (99% reduction)
- Response time: 8s → 1.2s (85% improvement)
- Cost per engagement: $15 → $0.15 (99% savings)

## Sources

- [MCP Documentation](https://modelcontextprotocol.io/docs)
- [Token Optimization Research](https://example.com)
- [Implementation Code](https://github.com/user/repo)
```

### Bad Example

```markdown
# How I Revolutionized Security Testing  ← Duplicate H1, ego-driven

In the ever-evolving landscape of cybersecurity... ← AI pattern

I believe that MCP tools are too verbose... ← Opinion, not evidence

My amazing framework has 18 skills and 28 commands... ← Hardcoded counts

[No sources section] ← Missing mandatory element
[No evidence] ← Claims without backing
[Self-promotional tone] ← Violates humble standard
```

---

## Mission Alignment

**Every piece of content should:**
- Upgrade human intelligence (teach something valuable)
- Build adjacent systems (augment, not replace)
- Focus on practical application (readers can use it)
- Maintain professional reputation (quality over quantity)

**Quality = Career Reputation**

**If in doubt:** Better to NOT publish than publish mediocre content

---

**See Also:**
- `library/prompts/content-guardian.md` - Automated enforcement
- `workflows/blog-content.md` - Complete blog workflow
- `workflows/technical-docs.md` - Diátaxis framework
