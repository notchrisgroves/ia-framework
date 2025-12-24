---
name: osint-research
description: Support skill providing dual-source OSINT research methodology (Claude WebSearch + Grok) for other skills. Not standalone - always invoked with caller context and research plan.
---

# OSINT Research Skill (Support Skill)

**Support skill loaded by: career, security-testing, security-advisory, writer**

Provides OSINT research methodology (dual-source, citations, fast/deep modes) for skills that need intelligence gathering.

**Core Philosophy:** Evidence-based research with mandatory citations. Every claim needs source URL + access date. This skill provides HOW to research - calling skills define WHAT to research.

---

## 🚨 Critical Rules

**This is a SUPPORT SKILL - not standalone:**

1. **Always Called with Context** - Caller provides: research plan, output location, mode
2. **Citations Mandatory** - Every claim needs source URL + access date, no speculation
3. **Dual-Source When Valuable** - Fast mode: Grok for culture/sentiment; Deep mode: Cross-validate
4. **Public Sources Only** - Ethical OSINT boundaries (no unauthorized access, social engineering)
5. **Caller-Specific Output** - Return findings to caller's specified directory

**Quality Standards = Research Credibility** - See `reference/standards.md`

---

## Support Skill Architecture

**How delegation works:**

```
Calling Skill → Defines WHAT to research → osint-research executes HOW

Example:
  security-testing needs: "Target org profile, tech stack, known vulns"
  osint-research executes: Dual-source methodology, returns findings
```

**Caller Context Required:**
- **Calling skill:** Who invoked osint-research (security-testing, career, etc.)
- **Research plan:** Specific requirements (what to find)
- **Mode:** fast (5-10 min) or deep (30-60+ min)
- **Output location:** Where to save findings

---

## Model Selection

**Reference:** `library/model-selection-matrix.md` | **Dynamic:** `tools/research/openrouter/fetch_models.py`

**Primary:** Perplexity Sonar-Pro (citations) | **Deep:** + Grok 4.1 (cross-validation) | **Synthesis:** Sonnet

---

## Decision Tree: Caller Detection

**Level 1: Who is calling this skill?**

### Caller 1: career

**Context:** Job application company research

**Research Plan (from caller):**
- Company culture and values
- Leadership team and backgrounds
- Technology stack and tools
- Recent news and developments
- Interview intel (team structure, priorities)

**Mode:** Fast (5-10 min)

**Output:** `output/career/job-opportunities/{Company}-{Role}/01-company-intelligence.md`

**Methodology:** WebSearch (primary) + Grok (culture/sentiment)

---

### Caller 2: security-testing

**Context:** Pre-pentest reconnaissance

**Research Plan (from caller):**
- Target organization profile
- Technology stack identification
- Attack surface mapping
- Known vulnerabilities and incidents
- Public infrastructure details

**Mode:** Fast (quick recon) or Deep (comprehensive profiling)

**Output:** `output/engagements/pentest/{target}/01-scope-and-reconnaissance/osint/`

**Methodology:** WebSearch + passive OSINT tools (not penetration testing)

---

### Caller 3: security-advisory

**Context:** Risk assessment industry research

**Research Plan (from caller):**
- Industry threat landscape
- Regulatory requirements
- Recent breach trends in industry
- Competitor security posture
- Compliance framework documentation

**Mode:** Fast (30-45 min for risk assessment Phase 2)

**Output:** `output/engagements/advisory/{client}/02-research/intelligence-summary.md`

**Methodology:** WebSearch + industry reports

---

### Caller 4: writer

**Context:** Blog post background research

**Research Plan (from caller):**
- Industry trends and developments
- Competitor analysis
- Subject matter depth (technical concepts)
- Expert perspectives
- Real-world examples and case studies

**Mode:** Deep (comprehensive research for original content)

**Output:** `blog/posts/{slug}/research-notes.md`

**Methodology:** WebSearch + Grok (adversarial validation) + multi-model research

---

## Research Modes

### Fast Mode (5-10 minutes)

**Characteristics:**
- Single-pass research
- 5-10 WebSearch queries per topic
- Grok for culture/sentiment only (when valuable)
- No checkpoints
- 10-15 primary sources
- Direct synthesis and delivery

**Use when:**
- Time-sensitive (job applications, quick intel)
- Caller needs overview, not deep dive
- Reconnaissance phase (not comprehensive profiling)

**Workflow:** `workflows/fast-mode-research.md`

---

### Deep Mode (30-60+ minutes)

**Characteristics:**
- Multi-phase research across 5 intelligence domains
- 15-30+ WebSearch queries with follow-up
- Mandatory dual-source verification (Claude + Grok)
- Session checkpoints after each phase
- 25-50+ primary sources
- Cross-validation emphasis
- Confidence assessment (high: both sources, medium: one source)
- Intelligence gaps identified

**Use when:**
- Comprehensive profiling needed
- Pentesting reconnaissance
- Original blog content
- Multi-session investigations

**Workflow:** `workflows/deep-mode-research.md`

---

## Delegation Examples

### Example 1: career → osint-research

**Caller context:**
```markdown
# From career/workflows/career-advancement.md

### Phase 2: Intelligence Gathering

**DELEGATE to osint-research skill:**

**Caller:** career
**Mode:** fast
**Research Plan:**
  - Company culture and values (Grok for X/Twitter sentiment)
  - Leadership backgrounds (C-suite, hiring manager if known)
  - Technology stack (job postings, engineering blog)
  - Recent news (funding, product launches, press releases)

**Output:** output/career/job-opportunities/{Company}-{Role}/01-company-intelligence.md

osint-research executes dual-source methodology and returns findings.
```

---

### Example 2: security-testing → osint-research

**Caller context:**
```markdown
# From security-testing/workflows/pentest-init.md

### Phase 1: Intelligence Gathering

**DELEGATE to osint-research skill:**

**Caller:** security-testing
**Mode:** fast (quick recon) OR deep (comprehensive profiling)
**Research Plan:**
  - Organization profile (industry, size, locations)
  - Technology stack (web tech, cloud providers, third-party services)
  - Attack surface mapping (domains, subdomains, IP ranges)
  - Known vulnerabilities (CVEs, breach history)
  - Public infrastructure (DNS, WHOIS, certificate transparency)

**Output:** output/engagements/pentest/{target}/01-scope-and-reconnaissance/osint/

osint-research executes reconnaissance using passive OSINT only (no active scanning).
```

---

### Example 3: security-advisory → osint-research

**Caller context:**
```markdown
# From security-advisory/workflows/risk-assessment.md

### Phase 2: OSINT Research

**DELEGATE to osint-research skill:**

**Caller:** security-advisory
**Mode:** fast (30-45 min)
**Research Plan:**
  - Industry threat landscape (WebSearch for trends)
  - Regulatory requirements (HIPAA, PCI-DSS, GDPR, etc.)
  - Recent breach trends in client's industry
  - Competitor security posture (public incidents, certifications)
  - Compliance framework documentation

**Output:** output/engagements/advisory/{client}/02-research/intelligence-summary.md

osint-research executes industry research and compliance framework loading.
```

---

### Example 4: writer → osint-research

**Caller context:**
```markdown
# From writer/workflows/blog-content.md

### Phase 1: Research

**DELEGATE to osint-research skill:**

**Caller:** writer
**Mode:** deep (comprehensive research)
**Research Plan:**
  - Industry trends and emerging technologies
  - Competitor analysis (what others have written)
  - Technical depth (understand concepts thoroughly)
  - Expert perspectives (security researchers, vendors)
  - Real-world examples and case studies

**Output:** blog/posts/{slug}/research-notes.md

osint-research executes multi-source methodology (WebSearch + Grok + Context7).
```

---

## Intelligence Gathering Areas (5 Domains)

**Used in deep mode for comprehensive profiling:**

1. **Target Profiling** - Organization structure, key personnel, technology stack, business relationships
2. **Digital Footprint** - Domains, subdomains, email patterns, social media presence, code repositories
3. **Security Posture** - Exposed credentials, known vulnerabilities, security incidents, compliance
4. **Threat Intelligence** - Known threat actors, attack campaigns, industry vulnerabilities, emerging threats
5. **Competitive Intelligence** - Market positioning, product offerings, customer base, public sentiment

**See:** `reference/intelligence-areas.md` for detailed coverage

---

## Dual-Source OSINT Methodology

**Claude Native Search (Primary):**
- General intelligence gathering
- News articles, blogs, company sites, technical docs
- Comprehensive web coverage
- Automatic citation URLs

**Grok Integration (Social/Real-Time):**
- X/Twitter intelligence
- Social media trends and sentiment
- Breaking news and real-time events
- Tweet URLs with engagement metrics

**Cross-Validation:**
- Compare findings from both sources
- Flag discrepancies for manual review
- Increase confidence with multi-source confirmation
- Document source provenance

**See:** `methodologies/dual-source-research.md` for complete process

---

## Standards and Frameworks

**Primary Standards:**
- **OSINT Framework** - Comprehensive OSINT tool taxonomy
- **Bellingcat's Open Source Investigation Toolkit** - Advanced OSINT techniques
- **NIST SP 800-115** - Security testing information gathering
- **PTES Intelligence Gathering Phase** - Penetration testing reconnaissance

**Supporting Standards:**
- **MITRE ATT&CK - Reconnaissance Tactics** - Adversarial perspective
- **OWASP Testing Guide - Information Gathering** - Web application reconnaissance

**See:** `reference/standards.md` for complete standards documentation

---

## When to Use OSINT Research vs Threat Intel

**✅ Use osint-research for:**
- General intelligence gathering (non-security context)
- Competitive intelligence and market analysis
- Pre-engagement reconnaissance (background)
- Threat actor CONTEXTUAL information (who they are, history, motivations)
- Narrative reports with synthesis and storytelling

**❌ Use threat-intel instead for:**
- CVE lookups and vulnerability research
- MITRE ATT&CK mapping
- Exploit availability research
- IOC enrichment and threat data
- CISA KEV tracking
- Threat actor TACTICAL TTPs (what they do, how they do it, detection methods)

**Decision Helper:** `reference/scope-decision-helper.md`

---

## Output Structure

**Caller-specific output locations:**

```
# career
output/career/job-opportunities/{Company}-{Role}/
   01-company-intelligence.md

# security-testing
output/engagements/pentest/{target}/
   01-scope-and-reconnaissance/osint/
      organization-profile.md
      technology-stack.md
      attack-surface.md
      known-vulnerabilities.md

# security-advisory
output/engagements/advisory/{client}/
   02-research/
      intelligence-summary.md

# writer
blog/posts/{slug}/
   research-notes.md
   sources.txt
   key-insights.md
```

**See:** `templates/osint-report-example.md` for complete template

---

## Safety Guardrails

**Ethical Boundaries:**
- Only use publicly available information
- No social engineering or deception
- Respect privacy and confidentiality
- Follow responsible disclosure for vulnerabilities
- Obtain authorization for target-specific research

**Citation Requirements:**
- Mandatory source URLs for ALL claims
- Include access dates for ephemeral content
- Document confidence levels (verified, probable, possible)
- Flag unverified information clearly
- Preserve source provenance (Claude vs Grok)

**Scope Limits:**
- No illegal access (hacking, unauthorized access)
- No dark web research without explicit authorization
- No personal harassment or doxxing
- Respect platform terms of service
- Follow client engagement scope strictly

---

## Session Checkpoint Protocol

**Checkpoint triggers (Deep Mode only):**
- After each research phase completion
- Every 2 hours during long investigations
- When switching between different research targets
- User explicitly requests checkpoint

**SESSION-STATE.md format:**
```yaml
skill: osint-research
calling_skill: [career|security-testing|security-advisory|writer]
session_number: [N]
mode: [fast/deep]
phase: [scope-definition/claude-search/grok-intel/cross-validation/synthesis]
status: [in-progress/completed]

# Caller context
caller_research_plan: [requirements from calling skill]
caller_output_location: [where to save findings]

# Phase-specific tracking
claude_queries_executed: [count]
grok_queries_executed: [count]
sources_collected: [count]
cross_validation_complete: [yes/no]

# Files created
files_created:
  - [list of intelligence reports generated]

# Next actions
next_action: [what to do next]
timestamp: [YYYY-MM-DD HH:MM]
```

**See:** `docs/session-checkpoint-enforcement.md` for complete protocol

---

## Tools

| Tool | Purpose | Location |
|------|---------|----------|
| Claude WebSearch | Primary intelligence gathering | Native |
| WebFetch | Deep content extraction | Native |
| Grok API | Social media + real-time intel | `tools/openrouter/` |

---

## Reference Documentation

| Document | Purpose |
|----------|---------|
| `standards.md` | OSINT Framework, Bellingcat, NIST SP 800-115 |
| `intelligence-areas.md` | 5 domain coverage details |
| `scope-decision-helper.md` | OSINT vs threat-intel routing |
| `dual-source-research.md` | Claude + Grok methodology |

---

## Common Scenarios

**Fast Mode (career):** "Research Acme Corp for job application"
→ Fast Mode → Company intel → Grok for culture → 5-10 min

**Fast Mode (security-testing):** "Quick recon on target before pentest"
→ Fast Mode → Org profile + tech stack → Passive OSINT → 10 min

**Deep Mode (security-testing):** "Comprehensive OSINT for pentest scoping"
→ Deep Mode → 5 intelligence domains → Dual-source → 30-60 min

**Deep Mode (writer):** "Research AI security trends for blog post"
→ Deep Mode → Industry analysis → Multi-source → 60+ min

---

## Version History

**v3.0** (2025-12-16): Support skill (delegated by other skills, caller context detection)
**v2.0** (2025-12-11): Dual-source methodology (Claude + Grok), progressive disclosure
