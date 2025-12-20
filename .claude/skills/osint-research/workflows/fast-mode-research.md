---
type: workflow
name: fast-mode-research
classification: public
version: 1.0
last_updated: 2025-12-02
---

# FAST MODE Research Workflow

**Single-pass intelligence gathering for career research and quick investigations (5-10 minutes)**

---

## Overview

**Purpose:** Rapid intelligence gathering for time-sensitive or lightweight research needs

**Duration:** 5-10 minutes

**Use Cases:**
- Career research (job applications, company background)
- Quick company intelligence
- Pre-application due diligence
- Simple person/organization lookups
- Social media sentiment checks

**Checkpoints:** None (single-pass execution to output)

---

## Workflow Steps

### 1. Execute Targeted WebSearch Queries (5-10 queries)

**Company Basics:**
```
"[Company Name]" size OR employees
"[Company Name]" industry OR market
"[Company Name]" headquarters OR offices
"[Company Name]" funding OR revenue
```

**Security Posture:**
```
"[Company Name]" security incident OR breach
"[Company Name]" SOC 2 OR ISO 27001 OR compliance
"[Company Name]" vulnerability OR CVE
```

**Culture Research:**
```
"[Company Name]" glassdoor reviews
"[Company Name]" employee sentiment
"[Company Name]" work culture OR remote
```

**Job Posting Intelligence (if career research):**
```
"[Company Name]" [job title] site:linkedin.com/jobs
"[Company Name]" [job title] requirements
"[Company Name]" engineering blog OR tech stack
```

**Leadership Research:**
```
"[Company Name]" CISO OR "Chief Information Security Officer"
"[Company Name]" CIO OR "Chief Information Officer"
"[Company Name]" CTO blog OR interviews
```

**Expected Sources:** 10-15 URLs with citations

---

### 2. Grok Enhancement (When Valuable)

**Use Grok for culture/sentiment ONLY when it adds value:**

**Company Culture:**
```python
grok_api.search(
    query="[Company Name] employee OR working",
    max_results=20,
    time_range="30d"
)
```

**Real-Time News:**
```python
grok_api.search(
    query="[Company Name]",
    max_results=10,
    time_range="7d"
)
```

**Social Sentiment:**
```python
grok_api.search(
    query="[Company Name] culture OR layoffs OR hiring",
    max_results=15,
    time_range="30d"
)
```

**Skip Grok when:**
- Target has minimal social media presence
- Historical data only (pre-2020)
- Time-critical quick lookup
- Technical/CVE research (use threat-intel instead)

**Expected Sources (if used):** 5-10 tweet URLs

---

### 3. Synthesize and Output

**Single Intelligence Report:**

```markdown
# OSINT Quick Brief: [Target Name]

**Research Date:** YYYY-MM-DD
**Research Mode:** FAST MODE
**Duration:** X minutes

## Company Overview
[Size, industry, locations, key products]

## Security Posture
[Known incidents, certifications, compliance]

## Technology Stack
[Languages, frameworks, cloud providers from job postings]

## Culture & Sentiment
[Glassdoor ratings, employee reviews, social media sentiment]

## Leadership
[CISO/CIO background, recent statements, priorities]

## Key Findings
1. [High-priority finding with citation]
2. [High-priority finding with citation]
3. [High-priority finding with citation]

## Citations

### Claude WebSearch
1. [URL] - [Title] (Accessed: YYYY-MM-DD)
2. ...

### Grok Social Intelligence (if used)
1. [Tweet URL] - [@Username] (Posted: YYYY-MM-DD)
2. ...

## Intelligence Gaps
[Quick list of unknowns for future research]
```

---

## Example: Career Research (Job Application)

**Research Request:** "Research Acme Corp for Senior Security Engineer role"

**FAST MODE Execution (8 minutes):**

**Step 1: WebSearch (6 queries, 5 minutes)**
1. "Acme Corp" size OR employees
   → 500-1000 employees, San Francisco HQ
2. "Acme Corp" security incident OR breach
   → Q3 2024 S3 misconfiguration, 10K records exposed
3. "Acme Corp" SOC 2 OR ISO 27001
   → SOC 2 Type II (2024-06), ISO 27001 (2023-11)
4. "Acme Corp" Senior Security Engineer site:linkedin.com/jobs
   → Posted 2024-11-20, req mentions AWS security, Kubernetes
5. "Acme Corp" glassdoor reviews
   → 3.8/5 rating, 65% approve of CEO, work-life balance praised
6. "Acme Corp" CISO
   → Jane Doe, hired 2024-10 after incident, ex-FAANG security leader

**Step 2: Grok Enhancement (2 queries, 2 minutes)**
1. X search: "Acme Corp working OR employee" (30d)
   → Mix of positive culture mentions, some concern about post-incident changes
2. X search: "Acme Corp" (7d)
   → Recent news: Secured $50M Series B, hiring surge announced

**Step 3: Synthesize (1 minute)**
Output intelligence brief with 8 Claude sources + 2 Grok sources

**Total Time:** 8 minutes
**No Checkpoint:** Direct execution to output

---

## Fast Mode Best Practices

**1. Targeted Queries**
- Use specific, focused queries (not broad exploration)
- 5-10 queries maximum (resist scope creep)
- Prioritize high-value intelligence categories

**2. Selective Grok Use**
- Only use when it adds value (culture, sentiment, real-time)
- Skip for technical/historical research
- 2-3 queries maximum

**3. Single-Pass Output**
- No iterative refinement (save for DEEP MODE)
- Synthesize findings immediately
- Accept intelligence gaps (document for future)

**4. Time Management**
- Set 10-minute hard limit
- If exceeded, incomplete is acceptable
- Note what's missing in "Intelligence Gaps"

---

## When to Switch to DEEP MODE

**Triggers for upgrading to DEEP MODE:**
- Intelligence gaps are critical to decision
- Multi-source conflicts requiring validation
- Pentest scoping (need comprehensive footprint)
- High-stakes investigation (M&A due diligence)
- User explicitly requests comprehensive research

**Indicators:**
- "I need everything you can find on..."
- "Comprehensive OSINT for..."
- "This is for a pentest engagement"
- Explicit `--deep` flag

**Action:** Escalate to DEEP MODE workflow with checkpoints

---

## Output Structure (FAST MODE)

**Single File:**
```
output/engagements/osint/{client}-{YYYY-MM}/
└── quick-brief-[target-name].md
```

**No Directory Structure:** FAST MODE produces single-file output

**No SESSION-STATE.md:** Not required for single-pass research

---

**Related:**
- `workflows/deep-mode-research.md` - Multi-phase comprehensive research
- `methodologies/dual-source-research.md` - Dual-source methodology
- `reference/mode-detection.md` - Automatic FAST vs DEEP mode detection
- `reference/research-depth.md` - Standard, Megathink, Ultrathink tiers
