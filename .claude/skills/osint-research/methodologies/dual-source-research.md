# Dual-Source OSINT Methodology

**Claude native search + Grok integration for comprehensive intelligence gathering**

---

## Overview

**Dual-source approach combines:**
- **Claude WebSearch:** General web intelligence (news, blogs, company sites, technical docs)
- **Grok Integration:** Social media intelligence (X/Twitter data, real-time events, sentiment)

**Benefits:**
- Cross-validation of findings from multiple angles
- Comprehensive coverage (web + social media)
- Increased confidence with multi-source confirmation
- Real-time intelligence + historical context

---

## Phase 1: Claude Native Search (Primary)

**Purpose:** General intelligence gathering from web sources

### Coverage Areas
- News articles and press releases
- Company websites and blogs
- Technical documentation and whitepapers
- GitHub repositories and code
- Job postings and career pages
- Public filings and regulatory documents
- Academic papers and research

### Strengths
- Comprehensive web coverage across all major sources
- 74% token savings compared to traditional methods
- Deep synthesis and reasoning capabilities
- Automatic source URL citations
- Historical data and archived content

### Process
1. **Execute WebSearch queries** (5-30+ queries depending on depth)
   - Targeted queries by intelligence category
   - Iterative refinement based on initial findings
   - Follow-up queries for deep dives

2. **Extract and synthesize findings**
   - Identify key facts and patterns
   - Note contradictions or inconsistencies
   - Document confidence levels

3. **Collect citations**
   - Source URLs with titles
   - Access dates
   - Relevant quotes

### Example Queries
- Company research: `"Acme Corp" security OR cybersecurity`
- Technical stack: `"Acme Corp" AWS OR Azure OR GCP`
- Personnel: `"Acme Corp" CISO OR "Chief Information Security Officer"`
- Incidents: `"Acme Corp" breach OR incident OR vulnerability`

---

## Phase 2: Grok Integration (Social/Real-Time)

**Purpose:** Social media intelligence and real-time event monitoring

### Coverage Areas
- X/Twitter posts and discussions
- Real-time breaking news
- Public discourse and sentiment
- Employee social media activity
- Customer complaints and feedback
- Industry analyst commentary
- Trending topics and hashtags

### Strengths
- Direct access to X/Twitter data (Grok's native platform)
- Real-time event monitoring
- Sentiment analysis from public discourse
- Employee perspectives and insights
- Unfiltered customer feedback

### Process
1. **Execute Grok API queries** (10-50+ results depending on depth)
   - Target-specific search terms
   - Time-range filtering (24h, 7d, 30d, all)
   - Engagement filtering (retweets, likes)

2. **Analyze social intelligence**
   - Sentiment trends (positive, negative, neutral)
   - Key influencers and thought leaders
   - Crisis events or controversies
   - Employee morale signals

3. **Collect social citations**
   - Tweet URLs with timestamps
   - Engagement metrics (retweets, likes, replies)
   - User credibility assessment

### Example Grok Queries
```python
grok_api.search(
    query="Acme Corp security OR cybersecurity",
    max_results=50,
    time_range="7d",
    filter="engagement>100"
)
```

---

## Phase 3: Cross-Validation

**Purpose:** Increase confidence through multi-source confirmation

### Validation Process

1. **Compare findings from both sources**
   - Identify facts confirmed by both Claude and Grok
   - Note unique findings from single source
   - Flag contradictions for manual review

2. **Confidence Scoring**
   - **High confidence:** Confirmed by both sources with consistent details
   - **Medium confidence:** One authoritative source (official press release, verified account)
   - **Low confidence:** Single unverified source or social media rumor
   - **Unverified:** Contradictory information or no corroboration

3. **Flag discrepancies**
   - Document conflicting information
   - Investigate source credibility
   - Seek additional verification if critical

4. **Document source provenance**
   - Clearly attribute findings to Claude or Grok
   - Preserve original citations
   - Note cross-validation status

### Example Cross-Validation

**Finding:** "Acme Corp uses AWS for infrastructure"

**Claude Source:** Press release (2024-06-15) announcing AWS partnership
**Grok Source:** CTO tweet (2024-07-20) mentioning AWS deployment
**Confidence:** **High** (official press release + executive confirmation)

**Finding:** "Acme Corp had a security incident in Q3 2024"

**Claude Source:** News article (2024-09-01) reporting potential breach
**Grok Source:** Customer complaints on X (2024-09-02) about service disruption
**Confidence:** **Medium** (news report + customer reports, no official confirmation)

---

## When to Use Dual-Source

### FAST MODE (Career Research, Quick Intel)
**Use dual-source selectively:**
- **Always use Claude WebSearch** (primary source)
- **Use Grok when valuable** for:
  - Company culture and employee sentiment
  - Real-time news and recent events
  - Customer perception and feedback
  - Social media presence assessment

**Skip Grok when:**
- Target has minimal social media presence
- Time-sensitive quick lookups
- Historical data only (pre-Twitter era)

### DEEP MODE (Pentesting, Investigations)
**Use dual-source mandatorily:**
- All intelligence gathering uses both sources
- Cross-validation required for all critical findings
- Comprehensive social media mapping
- Real-time + historical intelligence

---

## Output Format

**Synthesis Report Structure:**

```markdown
# OSINT Intelligence Report: [Target Name]

## Executive Summary
[Key findings with confidence levels]

## Intelligence Findings

### 1. [Category Name]

**Finding:** [Specific claim]

**Sources:**
- Claude: [URL] - [Title] (Accessed: YYYY-MM-DD)
- Grok: [Tweet URL] - [Username] (Posted: YYYY-MM-DD, Engagement: X retweets, Y likes)

**Confidence:** High/Medium/Low

**Analysis:** [Cross-validation notes]

---

## Intelligence Gaps

[Areas requiring further research]

## Citations

### Claude WebSearch Sources
1. [URL] - [Title] (Accessed: YYYY-MM-DD)
2. ...

### Grok Social Intelligence
1. [Tweet URL] - [@Username] (Posted: YYYY-MM-DD)
2. ...
```

---

## Best Practices

1. **Always cite sources** - Every claim must have attribution
2. **Document confidence levels** - Be transparent about verification status
3. **Preserve provenance** - Clearly mark which source provided which data
4. **Seek corroboration** - Don't rely on single-source for critical findings
5. **Time-stamp everything** - Intelligence degrades over time
6. **Flag unverified** - Clearly mark speculation or unconfirmed intelligence

---

**Related:**
- `reference/standards.md` - OSINT frameworks and methodologies
- `workflows/fast-mode-research.md` - Single-pass workflow
- `workflows/deep-mode-research.md` - Multi-phase workflow with checkpoints
- `reference/grok-integration.md` - Grok API details and examples
