---
name: writer
description: Blog posts, technical documentation, and security reports with mandatory QA review. Use for content creation.
---

# Writer Skill

**Auto-loaded when `writer` agent invoked**

Unified content creation with 3 content types and mandatory QA review. This skill acts as a decision tree router that selects the appropriate workflow based on content type detection.

**Core Philosophy:** Quality over quantity. Deep insights only. No surface-level content. QA review rating ≥4 required before publishing.

**Merged Features:** technical-writing + report-generation consolidated into single skill

---

## 🚨 Critical Rules

**Before starting ANY content creation:**

1. **QA Review Mandatory** - Rating ≥4 required before publishing blog posts
2. **No Hardcoded Counts** - Load content-guardian.md, never write "18 skills", "28 commands"
3. **Deep Insights Only** - Go deep or don't post (no surface-level aggregation)
4. **Citations Required** - All claims backed by evidence (OSINT research)
5. **Tool Discovery** - Check Context7 for code examples, never improvise Ghost publishing

**Quality Standards = Career Reputation** - See `reference/CONTENT-STANDARDS.md`

---

## Model Selection

**Reference:** `library/model-selection-matrix.md` for complete task-to-model mapping

**Default:** Latest Sonnet (content drafting, technical writing, documentation)
**Upgrade to Opus:** Novel content requiring strategic thinking, complex technical explanations
**Research:** Perplexity Sonar-Pro for research phase (citations, current events)
**QA:** Latest Haiku (structured review) + Latest Grok 3 (adversarial review)

**Workflow Pattern:** Perplexity (research) → Sonnet (write) → Haiku + Grok (QA)

**Dynamic Selection:** `tools/research/openrouter/fetch_models.py` for latest versions

---

## Decision Tree: Content Type Selection

**Level 1: What TYPE of content?**

### Content Type 1: Blog Posts

**Detection Keywords:**
- User: "blog", "post", "article", "Intelligence Adjacent", "publish", "Ghost"

**Decision Path:** Blog Post → [Research Depth] → `workflows/blog-content.md`

**Research Depth:**
- Deep research: 4-6 hours (trending topics, original research)
- Project docs: 2-3 hours (framework features, tool documentation)
- Standard: 2-4 hours (quick posts, tool overviews)

**Characteristics:**
- OSINT research with 10+ sources (Context7 + OpenRouter + WebSearch)
- Hero image (90s anime aesthetic, cyberpunk, neon)
- QA review BEFORE staging (rating ≥4 MANDATORY)
- Ghost CMS publishing via `tools/ghost-admin.ts`
- No politics, clickbait, or excessive self-promotion

**Workflow:** `workflows/blog-content.md`

---

### Content Type 2: Technical Documentation

**Detection Keywords:**
- User: "docs", "documentation", "tutorial", "how-to", "reference", "guide", "explain"

**Decision Path:** Technical Docs → [Diátaxis Type] → `workflows/technical-docs.md`

**Diátaxis Framework (4 Types):**

| Intent | Type | Characteristics |
|--------|------|-----------------|
| "How to set up..." | Tutorial | Learning-oriented, step-by-step |
| "How do I..." | How-To | Task-oriented, problem-solving |
| "What is..." | Explanation | Understanding-oriented, clarification |
| "API reference for..." | Reference | Information-oriented, descriptions |

**Characteristics:**
- Diátaxis framework compliance
- Code examples via Context7 (library documentation)
- No hardcoded counts (content-guardian.md enforced)
- Clear structure with examples
- Accuracy over speed

**Workflow:** `workflows/technical-docs.md`

---

### Content Type 3: Security Reports

**Detection Keywords:**
- User: "report", "assessment", "findings", "pentest report", "vulnerability report"

**Decision Path:** Security Report → [Standard Detection] → `workflows/security-reports.md`

**Report Standards:**

| Purpose | Standard | Template |
|---------|----------|----------|
| Penetration test | PTES | `PENTEST-REPORT-TEMPLATE.md` |
| Web app assessment | OWASP | `WEB-APP-REPORT-TEMPLATE.md` |
| Infrastructure audit | NIST 800-115 | `PENTEST-REPORT-TEMPLATE.md` |
| Bug bounty | Platform-specific | `BUG-BOUNTY-REPORT-TEMPLATE.md` |

**Characteristics:**
- Executive summary + technical findings
- Evidence-based only (no speculation)
- CVSS 3.1 scoring with justification
- Remediation guidance included
- Templates from security-testing skill

**Workflow:** `workflows/security-reports.md`

---

### Content Type 4: Weekly Newsletter

**Detection Keywords:**
- User: "newsletter", "weekly digest", "send digest", "schedule newsletter"

**Decision Path:** Newsletter → [Week Detection] → `workflows/newsletter-digest.md`

**Purpose:**
- Automated weekly digest of published blog posts
- Email-only post (does NOT appear on site)
- Scheduled for Monday 8:00 AM delivery
- Curated summary prevents inbox fatigue

**Characteristics:**
- Collects posts from `blog/` with `status: "published"` in metadata.json for date range
- Featured article + additional articles with tier notation (*, **)
- Slug format: `weekly-digest-YYYY-MM-DD-DD` (week start-end)
- Ghost `emailOnly: true` + `sendEmailWhenPublished: true`
- No QA review (automated curation)

**Workflow:** `workflows/newsletter-digest.md`

---

## Routing Decision Matrix

| User Request | Content Type | Workflow | QA Required | Duration |
|--------------|-------------|----------|-------------|----------|
| "Write blog post about AI security" | Blog Post | `blog-content.md` | ✅ Yes | 4-6 hours |
| "Document framework installation" | Technical Docs | `technical-docs.md` | ❌ No | 2-3 hours |
| "Generate pentest report" | Security Report | `security-reports.md` | ❌ No | 1-2 hours |
| "Send weekly newsletter" | Weekly Newsletter | `newsletter-digest.md` | ❌ No | 15-30 min |
| "How to configure Ghost CMS" | Technical Docs | `technical-docs.md` | ❌ No | 1-2 hours |

---

## Workflow: Blog Content

**RESEARCH → WRITING → QA_REVIEW → PUBLISHING**

### Phase 1: RESEARCH

**Research Source Priority (use in order):**
1. **Context7 FIRST** → Code examples, library APIs (cheapest, prevents hallucination)
   - Example: `get_library_docs("vercel/next.js", topic="ssr")` for Next.js examples
   - Example: `get_library_docs("tiangolo/fastapi", topic="authentication")`
   - Use for: All code snippets, library usage patterns, API references
2. **WebSearch** → Current events, official announcements, recent developments
3. **Perplexity** → Deep OSINT research requiring citations
4. **OpenRouter** → Multi-model research (Grok for adversarial validation)

**Why Context7 First:**
- Prevents hallucinated code examples in blog posts
- 85-97% cheaper than WebSearch for documentation lookups
- Version-specific docs (e.g., Next.js 15 vs 14 patterns)

**Multi-Source (10+ sources minimum)**

**Output:** Research notes with sources inventory

**See:** `reference/RESEARCH-PROTOCOL.md` for complete methodology

---

### Phase 2: WRITING

**Content Tiers:**
- Tier 1: Deep dive (2000+ words, original research)
- Tier 2: Analysis (1000-2000 words, expert synthesis)
- Tier 3: Quick guide (500-1000 words, how-to)

**Structure:**
- Hero image prompt (90s anime, cyberpunk aesthetic)
- Compelling introduction
- Clear H2/H3 hierarchy
- Code examples (Context7)
- Practical takeaways
- Sources section (mandatory)

**Quality Checklist:**
- ✅ Adds unique insights
- ✅ Goes deep (not surface-level)
- ✅ Professional tone
- ✅ All claims cited
- ✅ No hardcoded counts

---

### Phase 3: QA_REVIEW (MANDATORY)

**⛔ CANNOT SKIP - Rating ≥4 required**

**Process:**
1. Save draft: `blog/drafts/{slug}/draft.md`
2. Delegate to qa-review skill (support skill) with caller context
3. Check `qa-review.json` for rating
4. If rating <4: Revise and re-review
5. If rating ≥4: Proceed to publishing

**QA Review Delegation:**
- Caller: writer
- Review Type: peer-review
- Depth Level: standard
- Output: `blog/{slug}/qa-review.json`

**See:** `reference/QA-REVIEW-PROTOCOL.md` for complete process

---

### Phase 4: PUBLISHING

**Ghost Integration (MANDATORY tool usage):**
- ✅ Use `tools/ghost-admin.ts` ONLY
- ❌ Never improvise markdown → HTML conversion

**Publishing:**
```bash
bun run tools/ghost-admin.ts publish \
  --draft draft.md \
  --hero-image hero.png \
  --tags "security,ai" \
  --featured
```

**See:** `reference/GHOST-PUBLISHING-GUIDE.md`

---

## Workflow: Technical Documentation

**PLAN → WRITE → REVIEW**

### Phase 1: PLAN

**Diátaxis Classification:**
- Tutorial: Learning-oriented (teach concepts)
- How-To: Task-oriented (solve problem)
- Reference: Information-oriented (describe accurately)
- Explanation: Understanding-oriented (clarify concepts)

**Structure Planning:**
- Outline sections
- Identify code examples (Context7)
- Determine depth and scope

---

### Phase 2: WRITE

**Format Compliance:**

**Tutorial:** Clear objectives → Step-by-step → Success criteria → Examples

**How-To:** Problem statement → Prerequisites → Steps → Outcome → Troubleshooting

**Reference:** Logical organization → Descriptions → Parameters → Returns → Examples

**Explanation:** Context → Why it works → Relationships → Alternatives → When to use

**Critical Standards:**
- ✅ No hardcoded counts (load content-guardian.md)
- ✅ Code examples via Context7
- ✅ Clear headings
- ✅ Examples for complex concepts

**See:** `reference/DIATAXIS-FRAMEWORK.md` for complete guidelines

---

### Phase 3: REVIEW

**Self-Review:**
- Technical accuracy verified
- Code examples tested
- Links functional
- No hardcoded counts

**Save:** `docs/{category}/{filename}.md`

---

## Workflow: Security Reports

**GATHER → STRUCTURE → WRITE → DELIVER**

### Phase 1: GATHER

**Source Materials:**
- Finding files: `FINDING-*.md` (from security-testing)
- Test plan, scope, evidence

**Inventory:**
- Count findings by severity
- CVSS scores
- Remediation recommendations

---

### Phase 2: STRUCTURE

**Report Sections (PTES/OWASP/NIST):**
1. Executive Summary (non-technical, business impact)
2. Methodology (testing approach, tools)
3. Scope (in-scope assets, testing window)
4. Findings Summary (statistics, severity distribution)
5. Technical Findings (detailed vulnerabilities)
6. Remediation Roadmap (prioritized fixes)
7. Appendices (evidence, tool output)

**Template Selection:** See `templates/` directory

---

### Phase 3: WRITE

**Executive Summary:**
- Business-level language (no jargon)
- Overall risk assessment
- Key findings (top 3-5)
- Recommended actions

**Technical Findings:**
- CVSS score + severity
- Description, Impact, PoC
- Remediation steps
- References (CWE, CVE, OWASP)

**Quality:** Evidence-based only, CVSS 3.1 calculator, professional tone

---

### Phase 4: DELIVER

**Deliverable:**
- PDF export (professional formatting)
- Markdown source (client editing)
- Evidence package (screenshots, logs)

**Save:** Report saved to requesting skill's output directory
- Security assessment → `output/engagements/{type}/{id}/report.md`
- Career guidance → `output/career/{Company}-{Role}/report.md`

---

## Templates

| Template | Purpose |
|----------|---------|
| `BLOG-POST-TEMPLATE.md` | Blog post structure |
| `TECHNICAL-DOC-TEMPLATE.md` | Documentation structure |
| `QA-REVIEW-TEMPLATE.json` | QA review format |
| `PENTEST-REPORT-TEMPLATE.md` | PTES-compliant reports |
| `WEB-APP-REPORT-TEMPLATE.md` | OWASP-compliant reports |
| `BUG-BOUNTY-REPORT-TEMPLATE.md` | HackerOne/Bugcrowd format |

---

## Tools

| Tool | Purpose | Location |
|------|---------|----------|
| `ghost-admin.ts` | Ghost CMS publishing | `tools/` |
| OpenRouter | QA review (Grok model) | `tools/openrouter/` |
| Context7 | Library documentation | `tools/context7/` |

---

## OSINT Research Delegation

**When to delegate to osint-research skill:**
- Blog posts requiring industry trends and emerging technologies
- Competitor analysis (what others have written, coverage gaps)
- Subject matter background (historical context, current state)
- Expert perspectives (security researchers, vendor insights)
- Real-world examples and case studies

**How to delegate:**

```markdown
Load osint-research skill for background research.

**Caller:** writer
**Mode:** deep (comprehensive research for original content)

**Research Plan:**
- Industry trends and emerging technologies
- Competitor analysis and coverage gaps
- Subject matter background and historical context
- Expert perspectives and thought leadership
- Real-world examples and case studies

**Output:** blog/{slug}/research-notes.md

osint-research executes dual-source methodology (WebSearch + Grok) for background intelligence.
```

**Result:** Research notes, source citations, and key insights ready for writing phase

**See:** `workflows/blog-content.md` Stage 1 for complete research protocol

---

## Reference Documentation

| Document | Purpose |
|----------|---------|
| `CONTENT-STANDARDS.md` | Quality standards, editorial guidelines |
| `RESEARCH-PROTOCOL.md` | Multi-source OSINT methodology |
| `QA-REVIEW-PROTOCOL.md` | QA review (rating ≥4) |
| `GHOST-PUBLISHING-GUIDE.md` | Ghost CMS integration |
| `DIATAXIS-FRAMEWORK.md` | Technical documentation framework |
| `CONTENT-GUARDIAN.md` | No hardcoded counts enforcement |

---

## QA Review Enforcement

**Why QA Review?**
- Prevents low-quality content publication
- Catches factual errors before publishing
- Ensures complete citations
- Maintains professional reputation

**Process:** `reference/QA-REVIEW-PROTOCOL.md`

**Tool:** OpenRouter with dynamic Grok model

**Gate:** Rating <4 = Cannot proceed to publishing

---

## File Organization

```
blog/
├── drafts/{slug}/              (Work in progress)
│   ├── draft.md
│   ├── hero.png
│   └── qa-review.json
└── published/{slug}/           (Archived)
    └── final.md

output/engagements/
└── {type}/{id}/                (Pentest, vuln-scan, etc.)
    ├── report.md
    └── findings/

docs/{category}/                (Framework docs)
└── {filename}.md
```

---

## Common Scenarios

**Blog Post:** "Write about hierarchical context loading"
→ Blog Post → Deep research → `blog-content.md` → QA ✅ → 4-6 hours

**Technical Docs:** "Document skill migration"
→ How-To → `technical-docs.md` → QA ❌ → 2-3 hours

**Security Report:** "Generate pentest report"
→ PTES → `security-reports.md` → QA ❌ → 1-2 hours

**Explanation:** "Explain decision tree architecture"
→ Explanation → `technical-docs.md` → QA ❌ → 1-2 hours

---

## Version History

**v1.0.0 (2025-12-19)** - Fresh framework rebuild
- Unified skill (merged technical-writing + report-generation)
- Decision tree router (3 content types)
- QA review enforcement (rating ≥4 for blog posts)
- Ghost CMS tool integration
- Diátaxis framework compliance
- PTES/OWASP/NIST standards

---

**Version:** 4.1
**Last Updated:** 2025-12-19
**Status:** Decision tree router with QA enforcement
**Research Tools:** Context7 (code examples) → WebSearch → Perplexity → OpenRouter
