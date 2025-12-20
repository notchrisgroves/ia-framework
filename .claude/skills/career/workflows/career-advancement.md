---
name: career-advancement
description: Job application workflow with GO/NO-GO assessment, OSINT intelligence, and tailored deliverables
---

# Career Advancement Workflow

**Complete job application optimization in 5-10 minutes**

---

## Overview

5-phase workflow producing 3 comprehensive deliverables.

**Output:** `output/career/job-opportunities/{Company}-{Role}/`

**Deliverables:**
1. `1-EXECUTIVE-SUMMARY.md` - GO/NO-GO + Intelligence + Priority Areas + Q&A (comprehensive)
2. `2-RESUME.md` - Optimized resume tailored to role
3. `3-COVER-LETTER.md` - 4-paragraph cover letter with OSINT insights

**Auto-Resource Detection:**
- Resume: `input/career/resume.md`
- CliftonStrengths: `input/career/cliftonstrengths-all34.pdf` (optional)

---

## Phase 1: GO/NO-GO Assessment

**Threshold: ≥75% = GO, 60-74% = explain gaps, <60% = STOP**

### Scoring Methodology

**Resume Match Score (75% of total):**
| Category | Points | Criteria |
|----------|--------|----------|
| Required Skills | 40 | Direct match to job requirements |
| Nice-to-Have Skills | 20 | Preferred qualifications |
| Experience Level | 20 | Years and seniority match |
| Industry Match | 10 | Sector familiarity |

**CliftonStrengths Alignment (25% of total):**
- Theme-role fit analysis
- Domain balance for role type
- Leadership themes for management roles

**Decision Gates:**
- **≥75% = GO** - Proceed with full workflow
- **60-74% = Conditional** - Explain gaps, user decides
- **<60% = NO-GO** - Stop, recommend better-fit roles

**Red Flags (Auto NO-GO):**
- Required certification not held (and can't obtain quickly)
- Experience 5+ years below requirement
- Technology stack 0% overlap
- Location requires unwanted relocation

---

## Phase 2: Intelligence Gathering (OSINT)

**Use WebSearch for 90% of research. Cite sources inline per section.**

### Research Categories

**1. Organization Basics**
- Legal name, HQ, size, industry, type
- Revenue and financial health (if public)
- Recent news (funding, acquisitions, leadership changes)

**2. Security/Compliance Posture**
- Breach history and regulatory actions
- Compliance certifications (SOC 2, ISO 27001, CMMC)
- Industry-specific requirements

**3. Culture & Sentiment**
- Glassdoor rating and review themes
- Work-life balance indicators
- Management style feedback

**4. Leadership Research**
- CISO/CIO/CEO backgrounds
- Recent initiatives and priorities
- Strategic direction indicators

**5. Role Intelligence**
- Similar roles at 3-5 other companies
- Tech stack from job postings
- Team structure indicators

### Source Citation Format (MANDATORY)

**Cite sources inline after each section:**
```markdown
### Leadership

**CISO:** Jane Smith (since 2022)
- Background: 15 years security, former CISO at Acme Corp
- Priorities: Zero trust architecture, cloud security

**Source:** [Company Leadership Page](https://example.com/leadership), [LinkedIn](https://linkedin.com/in/janesmith)
```

**NOT at bottom in bulk. Sources per section for verification.**

---

## Phase 3: Priority Areas & Interview Prep

### Top 5 Priority Areas

For each priority area, include:
1. **Why It Matters** - Evidence from OSINT
2. **Their Need** - What they're seeking
3. **Your Position** - How to leverage resume experience
4. **Talking Points** - 2-3 key points to emphasize

### Interview Q&A (10-12 Questions)

**Categories:** Technical (3-4), Behavioral (3-4), Strategic (3-4)

**Format per question:**
```markdown
**Q: [Question]**
- **Why they're asking:** [OSINT context]
- **Your answer:** [STAR framework - Situation, Task, Action, Result]
- **Key evidence:** [Resume highlight]
```

**Quality over quantity. 10-12 strong questions > 20 generic ones.**

### Questions to Ask (5-7)

Strategic questions that demonstrate OSINT research:
- Role clarification
- Team structure and resources
- Growth and development
- Red flag investigation (if needed)

---

## Phase 4: Document Generation

### File 1: 1-EXECUTIVE-SUMMARY.md

**Comprehensive analysis document combining GO/NO-GO, intelligence, and interview prep.**

**Template Structure:**

```markdown
# Executive Summary: {Company} - {Role}

**Candidate:** {Name}
**Position:** {Title}
**Organization:** {Company}
**Analysis Date:** {YYYY-MM-DD}

---

## Match Assessment

### Score Summary

| Category | Score | Notes |
|----------|-------|-------|
| Resume Match | XX/75 | [Key strengths/gaps] |
| CliftonStrengths | XX/25 | [Fit assessment] |
| **TOTAL** | **XX/100** | **[GO/CONDITIONAL/NO-GO]** |

### Decision: [GO/CONDITIONAL/NO-GO]

[1-2 sentence recommendation with rationale]

---

## Why This Is a [XX]% Match

### Key Strengths
- [Strength 1 with evidence]
- [Strength 2 with evidence]
- [Strength 3 with evidence]

### Gaps to Address
- [Gap 1 with mitigation strategy]
- [Gap 2 with mitigation strategy]

---

## Organization Intelligence

### Company Overview
[Size, industry, mission, recent news]

**Source:** [URL]

### Security/Leadership
[CISO/CIO background, team size, priorities]

**Source:** [URL]

### Culture & Sentiment
[Glassdoor rating, pros/cons, work-life balance]

**Source:** [URL]

### Financial Context (if relevant)
[Revenue, growth, constraints that affect the role]

**Source:** [URL]

---

## Strategic Positioning

### Your Narrative
[2-3 sentence positioning statement]

### Competitive Advantages

| Their Need | Your Differentiator |
|------------|---------------------|
| [Need 1] | [Your strength] |
| [Need 2] | [Your strength] |
| [Need 3] | [Your strength] |

---

## Interview Preparation

### Priority Area 1: [Topic]
**Why it matters:** [OSINT evidence]
**Their need:** [What they're seeking]
**Your position:** [Resume evidence]
**Talking points:**
- [Point 1]
- [Point 2]

### Priority Area 2: [Topic]
[Same structure]

### Priority Area 3: [Topic]
[Same structure]

---

## Interview Q&A

### Technical Questions

**Q: [Question 1]**
- Why asking: [Context]
- Your answer: [STAR response]
- Key evidence: [Resume highlight]

**Q: [Question 2]**
[Same structure]

### Behavioral Questions

**Q: [Question 1]**
[Same structure]

### Scenario Questions

**Q: [Question 1]**
[Same structure]

---

## Questions to Ask

1. [Strategic question demonstrating OSINT research]
2. [Role clarification question]
3. [Team/resources question]
4. [Culture/development question]
5. [Red flag investigation if needed]

---

## Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| [Risk 1] | Low/Med/High | [Strategy] |
| [Risk 2] | Low/Med/High | [Strategy] |

---

## Recommendation

[Final 2-3 sentence recommendation with next steps]

**Analysis Completed:** {Date}
**Confidence Level:** [High/Medium/Low]
```

### File 2: 2-RESUME.md

**Tailored resume optimized for this specific role.**

**Optimization Rules:**
- Rewrite Professional Summary for this role
- Add Core Competencies with job keywords
- Reorder bullets to emphasize relevant experience
- Remove irrelevant positions entirely
- Target: 1-2 pages MAX

**NEVER:**
- Change job titles or role summaries
- Fabricate experience, skills, or achievements
- Add technologies not actually used
- Rewrite job functions (pentesting ≠ governance)

**ALWAYS:**
- Work with actual documented experience only
- STOP and ASK if major gaps exist
- Optimize = removal and reframing, not addition

### File 3: 3-COVER-LETTER.md

**4-paragraph structure, <350 words, today's date**

```markdown
[Today's Date]

[Hiring Manager Name or "Hiring Manager"]
[Company Name]
[Address if known]

Dear [Name/Hiring Manager],

**Paragraph 1 - Hook (OSINT insight):**
[Organization-specific opening that demonstrates research]

**Paragraph 2 - Match:**
[2-3 examples from resume aligned to job priorities]

**Paragraph 3 - Value Proposition:**
[Address specific pain point using your experience]

**Paragraph 4 - Close:**
[Enthusiasm + cultural fit + call to action]

Sincerely,
[Name]
[Contact info]
```

---

## Phase 5: Submission Strategy

### Application Timing
- Best days: Tuesday-Thursday
- Best time: 7-9 AM in company timezone
- Avoid: Friday afternoon, weekends, holidays

### Follow-Up Timeline
- **Day 3-5:** LinkedIn connection to hiring manager
- **Week 2:** Follow-up email if no response
- **Week 4:** Final check-in, then move on

---

## Resume Ethics (MANDATORY)

### Honest Assessment Protocol

**If career transition detected:**
1. Subtract 10-15 points from match score
2. Note in Executive Summary: "Career transition required"
3. Do NOT rewrite job functions to bridge gaps
4. Highlight transferable skills honestly

**When gaps exist:**
1. STOP and ASK USER before assumptions
2. Present gap: "Job requires X, but I don't see X in resume"
3. Wait for user input
4. Never guess undocumented experience

**The Critical Rule:**
> Optimization = Highlighting relevant parts of what you ACTUALLY DID
> Fabrication = Changing WHAT YOUR JOB WAS to fit better

---

## CliftonStrengths Usage

**Use in:**
- GO/NO-GO assessment (25% of match score)
- Executive Summary (personality-role fit)

**NOT in:**
- Interview Q&A (focus on experience, not personality)
- Resume (never mention CliftonStrengths)
- Cover letter (focus on achievements)

**Rationale:** Interviews evaluate demonstrated competence through evidence, not personality assessments.

---

## Fast Mode (Default)

- No session tracking
- Direct execution → 3 deliverable files
- Complete in 5-10 minutes
- Single session

---

**Related:**
- `workflows/strengths-development.md` - CliftonStrengths coaching
- `workflows/skill-building.md` - Mentorship and learning
