---
name: career
description: Career development with 3 modes - career advancement (job applications with GO/NO-GO assessment and OSINT research), strengths development (CliftonStrengths coaching and blindspot analysis), and skill building (mentorship and learning roadmaps). Resume ethics mandatory.
---

# Career Development Skill

**Auto-loaded when `advisor` agent invoked with career development task**

Unified career development with 3 modes: Career Advancement (job applications with OSINT), Strengths Development (CliftonStrengths coaching), and Skill Building (mentorship and learning roadmaps).

**Core Philosophy:** Evidence-based career strategy. GO/NO-GO assessment prevents wasted effort. OSINT-powered company research. Resume ethics mandatory (never fabricate). CliftonStrengths for blindspot analysis.

---

## 🚨 Critical Rules

**Before starting ANY career development work:**

1. **Auto-Resource Detection** - Resume auto-detect at `input/career/resume.md`, CliftonStrengths at `input/career/cliftonstrengths-all34.pdf`
2. **Mode Detection Required** - Analyze request to determine mode (Career/Strengths/Mentorship), never mix workflows
3. **Resume Ethics MANDATORY** - NEVER fabricate experience, skills, certifications, or achievements
4. **Fast Mode Default** - No checkpoints, no session files, direct output (90% of use cases)
5. **CliftonStrengths Usage Scope** - Use in GO/NO-GO and personality-role fit ONLY (NOT in interviews, resume, cover letter)

**Quality Standards = Career Reputation** - See `reference/ethics-standards.md`

---

## Model Selection

**Reference:** `library/model-selection-matrix.md` for complete task-to-model mapping

**Default:** Latest Sonnet (career analysis, resume optimization, interview prep)
**Upgrade to Opus:** Strategic career decisions, complex career pivots, strengths integration
**Research:** Perplexity Sonar-Pro for company research, job market analysis
**Advisory:** Latest Haiku (GO/NO-GO filtering) + Latest Sonnet (detailed analysis)

**Dynamic Selection:** `tools/research/openrouter/fetch_models.py` for latest versions

---

## Decision Tree: Mode Selection

**Level 1: What TYPE of career development?**

### Mode 1: Career Advancement (Jobs)

**Detection Keywords:**
- User: "job application", "apply to job", "resume", "interview prep", "cover letter"
- "job opportunity", "career opportunity", "position at"
- "optimize resume", "salary negotiation"
- Request includes job description or company name

**Decision Path:** Career Advancement → [Phase] → `workflows/career-advancement.md`

**Workflow Phases:**
1. GO/NO-GO Assessment (match score ≥75% = GO, <60% = STOP)
2. Intelligence Gathering (OSINT company research with inline citations)
3. Priority Areas & Interview Prep (Top 5 areas, 10-12 Q&A)
4. Document Generation (3 comprehensive files)
5. Submission Strategy (timing, follow-up, networking)

**Characteristics:**
- GO/NO-GO prevents wasted effort on poor-fit roles
- OSINT research with 10+ sources, cited inline per section
- Resume optimization = removal (not fabrication)
- CliftonStrengths for personality-role fit (NOT interview prep)
- 3 deliverables in 5-10 minutes
- Fast Mode (no checkpoints)

**Workflow:** `workflows/career-advancement.md`

**Output:** `output/career/job-opportunities/{Company}-{Role}/`

---

### Mode 2: Strengths Development (CliftonStrengths)

**Detection Keywords:**
- User: "CliftonStrengths", "strengths coaching", "Gallup assessment"
- "theme analysis", "strengths analysis", "theme interaction"
- "blindspots", "strengths development", "talent themes"
- Request includes CliftonStrengths report or Top 5 themes

**Decision Path:** Strengths Development → [Phase] → `workflows/strengths-development.md`

**Workflow Phases:**
1. Parse Strengths Data (Top 5 or Full 34, domain distribution)
2. Analyze Dominant Pattern (#1 + #2 theme interaction)
3. Identify Tensions (contradicting themes, overuse patterns)
4. Blindspot Analysis (Bottom 5, domain gaps, limitations)
5. Development Recommendations (Name it, Claim it, Aim it)

**Characteristics:**
- Brutally honest blindspot analysis
- Bottom 5 identification (if Full 34)
- Theme tension analysis (contradicting patterns)
- Domain gap identification (Executing, Influencing, Relationship Building, Strategic Thinking)
- 3 deliverables in 15-20 minutes
- Fast Mode (no checkpoints)

**Workflow:** `workflows/strengths-development.md`

**Output:** `output/career/strengths-analysis/{YYYY-MM-DD}/`

---

### Mode 3: Skill Building (Mentorship)

**Detection Keywords:**
- User: "mentorship", "learning roadmap", "skill development"
- "30/60/90-day plan", "certifications", "learning path"
- "portfolio development", "career development", "skill building"
- Request about cybersecurity learning or career progression

**Decision Path:** Skill Building → [Phase] → `workflows/skill-building.md`

**Workflow Phases:**
1. Assessment (current skills, gap analysis, objectives, timeline)
2. Planning (30/60/90-day action plans: Foundation → Building → Application)
3. Resources (free platforms prioritized, certification ROI analysis)
4. Tracking (session notes, milestone tracking, portfolio projects)

**Characteristics:**
- 30/60/90-day structured plans
- Free platforms prioritized (TryHackMe, HackTheBox)
- Certification ROI analysis
- Portfolio project ideas
- 3 deliverables in 15-30 minutes
- Fast Mode (no checkpoints)

**Workflow:** `workflows/skill-building.md`

**Output:** `output/career/learning-progress/{YYYY-MM-DD}/`

---

## Routing Decision Matrix

| User Request | Mode | Workflow | Deliverables | Duration |
|--------------|------|----------|--------------|----------|
| "Analyze this job posting for me" | Career Advancement | `career-advancement.md` | 3 files | 5-10 min |
| "Review my CliftonStrengths themes" | Strengths Development | `strengths-development.md` | 3 files | 15-20 min |
| "Create learning roadmap for cybersecurity" | Skill Building | `skill-building.md` | 3 files | 15-30 min |
| "Optimize resume for job X" | Career Advancement | `career-advancement.md` | 3 files | 5-10 min |

---

## Workflow: Career Advancement (5 Phases)

**GO_NO_GO → OSINT → SWOT → DELIVERABLES → STRATEGY**

### Phase 1: GO/NO-GO ASSESSMENT

**Match Score Calculation:**
- Technical skills match (40%)
- Experience match (30%)
- CliftonStrengths personality-role fit (20%)
- Location/compensation fit (10%)

**Decision Gates:**
- ≥75% = GO (proceed with application)
- 60-74% = CONDITIONAL (explain gaps, upskilling plan)
- <60% = STOP (poor fit, recommend alternative roles)

**Prevents wasted effort on poor-fit roles**

---

### Phase 2: INTELLIGENCE GATHERING (OSINT)

**Delegate to osint-research skill for company intelligence:**

```markdown
Load osint-research skill for company research.

**Caller:** career
**Mode:** fast (5-10 min)

**Research Plan:**
- Company culture and values
- Leadership team and backgrounds
- Technology stack and tools
- Recent news and developments
- Interview intel (team structure, priorities)

**Output:** output/career/job-opportunities/{Company}-{Role}/01-company-intelligence.md

osint-research executes dual-source methodology (WebSearch + Grok for culture/sentiment).
```

**Research should include (10+ sources):**
- Company basics (size, industry, funding, leadership)
- Recent news and business updates
- Glassdoor reviews and employee sentiment
- Job postings for tech stack intel
- Leadership background (CISO/CIO priorities)
- Market positioning and competitors

**Result:** Comprehensive company intelligence ready for SWOT analysis

---

### Phase 3: SWOT ANALYSIS

**Four Quadrants:**
- Strengths: Your advantages for this role
- Weaknesses: Skill gaps or experience mismatches
- Opportunities: Company growth, emerging tech, career path
- Threats: Competitors, market conditions, role risks

---

### Phase 4: DOCUMENT GENERATION (3 Files)

**Deliverables:**
1. `1-EXECUTIVE-SUMMARY.md` - Comprehensive analysis (GO/NO-GO + Intelligence + Priority Areas + Q&A)
2. `2-RESUME.md` - Optimized resume tailored to role (1-2 pages MAX)
3. `3-COVER-LETTER.md` - 4-paragraph cover letter (<350 words, today's date)

**Source Citation Format (MANDATORY):**
- Cite sources inline after each section, NOT at bottom
- Format: `**Source:** [Title](URL)`
- Enables per-section verification

**Resume Ethics (MANDATORY):**
- NEVER fabricate experience, skills, certifications, achievements
- Default resume = MAXIMUM length (optimization = removal, not addition)
- When gaps exist → STOP and ASK USER (never guess undocumented experience)

**See:** `workflows/career-advancement.md` for complete ethics protocol and templates

---

### Phase 5: SUBMISSION STRATEGY

**Timing and Follow-Up:**
- Application timing (Tuesday-Thursday, 6-10am optimal)
- Follow-up timeline (1 week, 2 weeks, 3 weeks)
- Networking strategy (LinkedIn connections, informational interviews)

**See:** `workflows/career-advancement.md` for complete process

---

## Workflow: Strengths Development (5 Phases)

**PARSE → ANALYZE → TENSIONS → BLINDSPOTS → RECOMMENDATIONS**

### Phase 1: PARSE STRENGTHS DATA

**Extract Themes:**
- Top 5 (or Full 34 if provided)
- Domain distribution (Executing, Influencing, Relationship Building, Strategic Thinking)
- Theme ranking order

---

### Phase 2: ANALYZE DOMINANT PATTERN

**#1 + #2 Theme Interaction:**
- How do top 2 themes interact?
- Unique behavioral patterns created
- Strengths amplification or conflicts

---

### Phase 3: IDENTIFY TENSIONS

**Contradictions:**
- Contradicting themes (e.g., Achiever vs. Adaptability)
- Overuse patterns (too much of one domain)
- Missing domains (zero themes in Strategic Thinking)

---

### Phase 4: BLINDSPOT ANALYSIS

**Brutally Honest Assessment:**
- Bottom 5 themes (if Full 34 provided)
- Domain gaps (missing domains = blind spots)
- Unintended consequences of top themes
- Honest limitations

---

### Phase 5: DEVELOPMENT RECOMMENDATIONS

**Name it, Claim it, Aim it Framework:**
- Name it: Recognize patterns and tensions
- Claim it: Own strengths AND limitations
- Aim it: Action plan for development

**See:** `workflows/strengths-development.md` for complete process

---

## Workflow: Skill Building (4 Phases)

**ASSESSMENT → PLANNING → RESOURCES → TRACKING**

### Phase 1: ASSESSMENT

**Current State Analysis:**
- Current skills (technical, soft, certifications)
- Gap analysis (what's missing for target role)
- Objectives (career goals, timeline)
- Constraints (time, budget, access)

---

### Phase 2: PLANNING (30/60/90-Day)

**Structured Roadmap:**
- 30 days: Foundation (concepts, basic skills, free platforms)
- 60 days: Building (intermediate skills, certifications, projects)
- 90 days: Application (portfolio, labs, job applications)

---

### Phase 3: RESOURCES

**Prioritized Resources:**
- Free platforms (TryHackMe, HackTheBox, OverTheWire)
- Certification ROI analysis (OSCP, CEH, CISSP)
- Books, courses, communities
- Lab environments

---

### Phase 4: TRACKING

**Progress Management:**
- Session notes
- Milestone tracking
- Portfolio projects
- Skill assessments

**See:** `workflows/skill-building.md` for complete process

---

## CliftonStrengths Usage Scope (CRITICAL)

**✅ Use CliftonStrengths in:**
- GO/NO-GO assessment (personality-role fit scoring)
- Executive Summary in 1-EXECUTIVE-SUMMARY.md (cultural fit analysis)
- Strengths Development mode (complete theme analysis)

**❌ Do NOT use CliftonStrengths in:**
- Interview prep (interviews showcase experience, not personality traits)
- Q&A answers (use STAR method with concrete examples)
- Cover letter (focus on achievements, not personality)
- Resume (skills and experience only)
- Tactical interview guidance (behavioral questions need evidence)

**Rationale:** Interviews evaluate demonstrated competence through evidence (STAR method), not personality assessments. CliftonStrengths informs role fit decision-making, not interview performance.

---

## Resource Auto-Detection

**Automatic File Discovery:**
- Resume: `input/career/resume.md`
- CliftonStrengths: `input/career/cliftonstrengths-all34.pdf`

**No prompts, direct execution (Fast Mode)**

**If resources not found:**
- Resume missing: Ask user to provide or specify path
- CliftonStrengths missing: Skip personality-role fit in GO/NO-GO

---

## Fast Mode vs Deep Mode

**Fast Mode (Default - 90% of use cases):**
- No checkpoints, no session files
- Direct output in single session
- Progress tracked in deliverable files (Application-Tracker.md, development-plan.md, progress-tracker.md)
- Complete in 5-30 minutes

**Deep Mode (Opt-in for multi-week projects):**
- SESSION-STATE.md for session-to-session continuity
- Update after each major milestone
- Track long-term job search campaigns or learning programs
- User explicitly requests "--deep" flag

**See:** `docs/streamlining-methodology.md` for complete guidance

---

## Output Structure

**Career Advancement:**
```
output/career/job-opportunities/{Company}-{Role}/
   metadata.json             # Application tracking (phase, match_score, go_no_go)
   1-EXECUTIVE-SUMMARY.md    # GO/NO-GO + Intelligence + Priority Areas + Q&A
   2-RESUME.md               # Optimized resume
   3-COVER-LETTER.md         # 4-paragraph cover letter
```

**Strengths Development:**
```
output/career/strengths-analysis/{YYYY-MM-DD}/
   metadata.json             # Session tracking
   strengths-analysis.md     # Complete theme breakdown
   blindspots-identified.md  # Brutally honest limitations
   development-plan.md       # Actionable recommendations
```

**Skill Building:**
```
output/career/learning-progress/{YYYY-MM-DD}/
   metadata.json             # Learning progress tracking
   learning-roadmap.md       # 30/60/90-day action plan
   skills-assessment.md      # Current state and gaps
   progress-tracker.md       # Milestone tracking
```

---

## Privacy Protection

**Sanitization Rules:**
- Never include real names, contact info, or identifying details in examples
- Sanitize all examples unless explicitly requested
- PII protection for resume data

---

## Tools

| Tool | Purpose | Location |
|------|---------|----------|
| WebSearch | Company research (primary) | Native |
| WebFetch | Deep content extraction | Native |
| osint-research | Deep company intel | `skills/osint-research/` |

---

## Reference Documentation

| Document | Purpose |
|----------|---------|
| `ethics-standards.md` | Resume ethics, fabrication prevention |
| `resource-locations.md` | File paths for resume, CliftonStrengths, outputs |
| `shared-resources.md` | Shared resources from resources/library/ |

---

## Integration Points

**OSINT Research Integration:**
- Delegates to osint-research skill for company intelligence
- Uses WebSearch for 90% of research
- Sources cited with URLs and dates

**Legal Integration:**
- Employment contract review before accepting offers
- Non-compete enforceability analysis (state-specific)
- IP assignment clause review

**Writer Integration:**
- Portfolio project documentation
- Technical writing for blog/GitHub
- Resume and cover letter formatting

---

## Common Scenarios

**Job Application:** "Analyze this job posting at Acme Corp"
→ Career Advancement → GO/NO-GO → OSINT → 3 files → 5-10 min

**Strengths Coaching:** "Review my CliftonStrengths Top 5"
→ Strengths Development → Theme analysis → Blindspots → 3 files → 15-20 min

**Learning Roadmap:** "Create 30/60/90 plan for cybersecurity"
→ Skill Building → Assessment → 30/60/90 plan → Resources → 3 files → 15-30 min

**Resume Optimization:** "Optimize resume for CISO role"
→ Career Advancement → Resume ethics check → Tailoring → 3 files → 5 min

---

**Version:** 2.1 | **Updated:** 2025-12-18 | **Status:** Decision tree router with workflow files restored
