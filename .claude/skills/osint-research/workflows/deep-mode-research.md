---
type: workflow
name: deep-mode-research
classification: public
version: 1.0
last_updated: 2025-12-02
---

# DEEP MODE Research Workflow

**Multi-phase comprehensive investigation with checkpoints (30-60+ minutes)**

---

## Overview

**Purpose:** Thorough intelligence gathering for high-stakes investigations

**Duration:** 30-60+ minutes (may span multiple sessions)

**Use Cases:**
- Penetration test reconnaissance
- Comprehensive threat actor profiling
- M&A due diligence
- Complex investigations
- Competitive intelligence (detailed)

**Checkpoints:** Multi-session tracking in `sessions/` required for multi-session work

**Dual-Source:** Mandatory (Claude WebSearch + Grok verification)

---

## Workflow Phases

### Phase 1: Scope Definition (5-10 minutes)

**Objectives:**
1. Define research target and objectives
2. Identify information requirements
3. Establish scope boundaries (ethical, legal)
4. Determine research depth (Standard/Megathink/Ultrathink)

**Activities:**
- Document target details (name, domain, industry, size)
- Clarify intelligence requirements (technical, operational, strategic)
- Identify ethical boundaries (public sources only, no unauthorized access)
- Estimate research timeline and depth

**Deliverable:** Research plan documented

**CHECKPOINT:** Update session file with:
- Research target and objectives
- Scope boundaries and ethical constraints
- Research depth tier selected
- Estimated timeline
- Next action: Proceed to Phase 2

---

### Phase 2: Claude Native Search (15-25 minutes)

**Objectives:**
Execute comprehensive WebSearch queries across all intelligence areas

**Activities:**

**1. Company/Organization Research (5-7 queries)**
```
"[Target]" size OR employees OR revenue
"[Target]" headquarters OR offices OR locations
"[Target]" products OR services OR offerings
"[Target]" funding OR investors OR acquisitions
"[Target]" leadership OR executives OR board
```

**2. Technology Stack (4-6 queries)**
```
"[Target]" AWS OR Azure OR GCP
"[Target]" tech stack site:builtwith.com OR site:wappalyzer.com
"[Target]" engineering blog OR developer docs
site:github.com "[Target]" OR "[Target]" repositories
"[Target]" job postings site:linkedin.com/jobs
```

**3. Security Posture (4-6 queries)**
```
"[Target]" security incident OR breach OR vulnerability
"[Target]" SOC 2 OR ISO 27001 OR PCI DSS OR compliance
"[Target]" CVE OR exploit OR disclosure
"[Target]" site:have been pwned OR site:breachdirectory.com
"[Target]" bug bounty site:hackerone.com OR site:bugcrowd.com
```

**4. Digital Footprint (3-5 queries)**
```
site:crt.sh "[Target]" OR site:censys.io "[Target]"
"[Target]" email format OR naming convention
"[Target]" site:linkedin.com employees OR people
"[Target]" site:twitter.com OR site:reddit.com
```

**5. Public Perception (2-4 queries)**
```
"[Target]" glassdoor OR reviews OR ratings
"[Target]" news OR press release OR announcement
"[Target]" lawsuit OR legal OR complaint
"[Target]" customer reviews site:g2.com OR site:trustpilot.com
```

**Expected Sources:** 25-40 primary sources (depending on depth tier)

**Deliverable:** Claude intelligence report with citations

**CHECKPOINT:** Update session file with:
- WebSearch queries executed (count)
- Primary sources collected (count)
- Key findings summary
- Intelligence gaps identified
- Next action: Proceed to Phase 3

---

### Phase 3: Grok Social Intelligence (10-15 minutes)

**Objectives:**
Gather social media intelligence and real-time events

**Activities:**

**1. Corporate Social Media**
```python
grok_api.search(
    query="[Target] OR @[TargetHandle]",
    max_results=50,
    time_range="30d"
)
```

**2. Employee Mentions**
```python
grok_api.search(
    query="working at [Target] OR employee [Target]",
    max_results=30,
    time_range="90d"
)
```

**3. Security Discussions**
```python
grok_api.search(
    query="[Target] security OR breach OR incident",
    max_results=40,
    time_range="180d"
)
```

**4. Customer Sentiment**
```python
grok_api.search(
    query="[Target] customer OR user experience",
    max_results=30,
    time_range="60d",
    filter="engagement>50"
)
```

**5. Industry Analysis**
```python
grok_api.search(
    query="[Industry] threat OR vulnerability OR attack",
    max_results=25,
    time_range="30d"
)
```

**Expected Sources:** 30-50 social intelligence sources

**Deliverable:** Grok intelligence report with tweet URLs and engagement metrics

**CHECKPOINT:** Update session file with:
- Grok queries executed (count)
- Social sources collected (count)
- Sentiment analysis (positive/negative/neutral percentages)
- Key social findings
- Next action: Proceed to Phase 4

---

### Phase 4: Cross-Validation (5-10 minutes)

**Objectives:**
Compare findings from Claude and Grok, resolve discrepancies

**Activities:**

**1. Compare Findings**
- Match facts from both sources
- Identify unique findings from single source
- Flag contradictions or conflicts

**2. Confidence Scoring**
- High: Confirmed by both Claude and Grok
- Medium: One authoritative source (official press release, verified account)
- Low: Single unverified source or social media rumor
- Unverified: Contradictory information or no corroboration

**3. Resolve Discrepancies**
- Research conflicting data points
- Assess source credibility
- Seek third source if critical

**4. Document Provenance**
- Attribute findings to Claude or Grok
- Preserve original citations
- Note cross-validation status

**Deliverable:** Cross-validation report with confidence levels

**CHECKPOINT:** Update session file with:
- High-confidence findings (count)
- Medium-confidence findings (count)
- Low-confidence findings (count)
- Unresolved discrepancies (count)
- Next action: Proceed to Phase 5

---

### Phase 5: Synthesis and Reporting (10-15 minutes)

**Objectives:**
Consolidate findings into comprehensive OSINT report

**Activities:**

**1. Organize by Category**
- Target Profiling (organization, personnel, technology)
- Digital Footprint (domains, emails, social media, repositories)
- Security Posture (incidents, certifications, vulnerabilities)
- Threat Intelligence (threat actors, campaigns, industry threats)
- Competitive Intelligence (market position, sentiment)

**2. Add Citations for All Claims**
- Every fact must have source URL
- Include access dates for ephemeral content
- Document confidence levels
- Preserve source provenance (Claude vs Grok)

**3. Create Executive Summary**
- Key findings (top 5-10)
- Risk assessment
- Strategic recommendations
- Intelligence gaps

**4. Generate Detailed Report**
- All findings organized by category
- Complete citations
- Confidence levels
- Cross-validation notes

**Deliverable:** Comprehensive OSINT intelligence report

**FINAL CHECKPOINT:** Update session file with:
- Phase 5 completion status + timestamp
- Total sources (Claude + Grok combined)
- Report files created
- Intelligence gaps documented
- Next action: N/A (research complete)

---

## Output Structure (DEEP MODE)

**Multi-file deliverable:**
```
output/engagements/osint/{client}-{YYYY-MM}/
├── README.md                          (Research objectives, scope)
├── SESSION-STATE.md                   (Checkpoint tracking)
├── 01-target-profiling/
│   ├── organization-overview.md
│   ├── key-personnel.md
│   └── technology-stack.md
├── 02-digital-footprint/
│   ├── domains-subdomains.md
│   ├── email-patterns.md
│   └── social-media-presence.md
├── 03-security-posture/
│   ├── security-certifications.md
│   ├── security-incidents.md
│   └── known-vulnerabilities.md
├── 04-threat-intelligence/
│   └── industry-threats.md
├── 05-competitive-intel/
│   └── market-analysis.md
└── 06-synthesis-report/
    ├── executive-summary.md           (Key findings, high confidence)
    ├── detailed-findings.md           (All intelligence with citations)
    └── intelligence-gaps.md           (Areas requiring further research)
```

---

## Research Depth Tiers

**DEEP MODE supports three depth levels:**

### Standard Tier (Default)
- **Duration:** 30-45 minutes
- **WebSearch Queries:** 15-25 queries
- **Grok Queries:** 3-5 queries
- **Sources:** 25-40 primary sources
- **Use For:** Typical pentest scoping, standard investigations

### Megathink Tier (Complex Targets)
- **Duration:** 60-90 minutes
- **WebSearch Queries:** 30-50 queries with follow-up
- **Grok Queries:** 5-8 queries with deep analysis
- **Sources:** 50-75 primary sources
- **Use For:** High-value targets, complex organizations, M&A

### Ultrathink Tier (High-Stakes)
- **Duration:** 2-4 hours (multi-session)
- **WebSearch Queries:** 50+ queries with iterative refinement
- **Grok Queries:** 10+ queries with network mapping
- **Sources:** 100+ primary sources
- **Use For:** Nation-state research, major investigations, strategic intelligence

**See:** `reference/research-depth.md` for complete tier descriptions

---

## Multi-Session Protocol

**For Ultrathink tier or interrupted research:**

**Session 1:**
- Complete Phases 1-2 (Scope + Claude Search)
- CHECKPOINT SESSION-STATE.md
- Note: "Continue with Phase 3 (Grok Intelligence)"

**Session 2:**
- Resume from SESSION-STATE.md
- Complete Phases 3-4 (Grok + Cross-Validation)
- CHECKPOINT SESSION-STATE.md
- Note: "Continue with Phase 5 (Synthesis)"

**Session 3:**
- Resume from SESSION-STATE.md
- Complete Phase 5 (Synthesis and Reporting)
- FINAL CHECKPOINT SESSION-STATE.md
- Close research engagement

---

## When to Use DEEP MODE

**Automatic Triggers:**
- User mentions "pentest" or "penetration test"
- Request for "comprehensive" or "thorough" research
- M&A due diligence explicitly requested
- User provides `--deep` flag
- Multi-session investigation

**Manual Triggers:**
- FAST MODE reveals critical intelligence gaps
- Time-sensitive decision with high stakes
- Conflicting information requires validation
- Target has complex footprint

---

**Related:**
- `workflows/fast-mode-research.md` - Quick intelligence gathering
- `methodologies/dual-source-research.md` - Claude + Grok methodology
- `reference/research-depth.md` - Standard, Megathink, Ultrathink tiers
- `reference/output-structure.md` - Directory organization details
- `docs/session-checkpoint-enforcement.md` - Multi-session protocol
