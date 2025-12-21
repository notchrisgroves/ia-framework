---
name: job-analysis
description: Job posting analysis and application strategy
---

# /job-analysis - Job Application Analysis & Strategy

Fast, comprehensive job application analysis with OSINT intelligence, match scoring, and tailored deliverables.

**Agent:** advisor
**Skill:** career (career advancement)
**Output:** `output/career/job-opportunities/{Company}-{Role}/`

---

## Quick Start

```
/job-analysis <job description or URL>
```

**Auto-loads:** Resume from `input/career/resume.md`

**Workflow:**
1. ✅ GO/NO-GO assessment (≥75% proceed, 60-74% explain, <60% stop)
2. 🕵️ OSINT intelligence gathering
3. 📝 Interview preparation
4. 📦 Deliverables (resume, cover letter, Q&A guide)

**Time:** 5-10 minutes

---

## When to Use

✅ **Use /job-analysis when:**
- Analyze job posting and make GO/NO-GO decision
- Research company intelligence before applying
- Optimize resume and cover letter for specific role
- Prepare interview talking points and questions
- Get strategic application guidance

❌ **Don't use if:**
- Need resume review without specific job → use `/job-analysis` (general resume review mode)
- Preparing for scheduled interview → use `/job-analysis` (interview prep mode)

---

## Prerequisites

### Resume Setup (Required)

**Place your resume at:** `input/career/resume.md`

```bash
# Create input directory if needed (mirrors output/career/)
mkdir -p input/career

# Copy/create your resume
# input/career/resume.md - Markdown format recommended
```

**If resume not found:** Command will prompt you to provide it or specify the path.

**Optional:** `input/career/cliftonstrengths-all34.pdf` - CliftonStrengths report for personality-role fit scoring

---

## Workflow

### Auto-Resource Detection (NO PROMPTS)

**Automatically loads:**
- ✅ Resume: `input/career/resume.md`
- ✅ CliftonStrengths: `input/career/cliftonstrengths-all34.pdf` (if applicable)
- ✅ Job source: Auto-detect (URL vs pasted text)

**Just provide:** Job description (URL or text)

---

### Phase 1: GO/NO-GO Assessment (≥75% = GO)

**Resume Match Score (75% weight):**
- Required skills alignment (60%)
- Experience level match (25%)
- Preferred qualifications (15%)

**CliftonStrengths Alignment (25% weight):**
- Strategic vs tactical fit
- Independent vs collaborative
- Stability vs change orientation
- Communication intensity needs

**Decision Logic:**
- **✅ ≥75%** → Proceed to Phase 2-4
- **⚠️ 60-74%** → Explain gaps, you decide
- **❌ <60%** → Stop, provide feedback on better-fit roles

**Visual Output:**
```
🔍 Phase 1: GO/NO-GO Assessment
   Resume Match: 82/100
   ├─ Required Skills: 52/60 ✅
   ├─ Experience Level: 20/25 ✅
   └─ Preferred Quals: 10/15 ✅

   CliftonStrengths: Strong Fit (23/25)

   ✅ DECISION: GO (82/100 - threshold ≥75%)
```

---

### Phase 2: OSINT Intelligence (Auto-executes if GO)

**Delegates to `osint-research` skill (FAST MODE):**

**Intelligence Gathering:**
1. Organization basics - Legal name, HQ, size, industry
2. Security posture - Breach history, regulatory actions, compliance
3. Culture & sentiment - Glassdoor/Indeed reviews, employee tenure
4. Job posting intel - 3-5 related roles for tech stack, pain points
5. Leadership research - CISO/CIO/CEO backgrounds, priorities

**Dual-Source Enhancement:**
- Claude WebSearch (primary) - Company info, news, public data
- Grok (when valuable) - X/Twitter sentiment, real-time news

---

### Phase 3: Interview Preparation

**A. Priority Areas (Top 5)**
- Evidence: Why this matters (from OSINT)
- Their needs: What they're seeking
- Your approach: How to position resume experience
- Resources: Framework/methodology links

**B. Interview Q&A (15-20 questions)**
- Categories: Technical, Behavioral, Scenario, Compliance, Cultural
- Why they're asking: OSINT context
- Answer framework: STAR method outline
- Key points: Resume highlights
- Avoid: Red flags

**C. Questions to Ask (10)**
- Strategic (demonstrate OSINT research)
- Role clarification
- Team/resources
- Culture/development
- Red flag investigation (if needed)

---

### Phase 4: Deliverables

**A. Optimized Resume**
- Rewrite Professional Summary ONLY
- Add Core Competencies/Skills with required terms
- **PROHIBITIONS:**
  - ❌ NEVER change job titles or role summaries
  - ❌ NEVER change job function
  - ❌ NEVER rewrite responsibilities
  - ❌ NEVER change occasional work into primary responsibilities
  - ✅ ONLY: Professional Summary, Core Competencies, bullet wording (SAME facts)

**B. Cover Letter**
4-paragraph structure:
1. Hook (organization-specific from OSINT)
2. Match (2-3 examples from resume aligned to priorities)
3. Value proposition (address pain point)
4. Close (enthusiasm + cultural fit)

---

## Agent Routing

```typescript
Task({
  subagent_type: "advisor",
  model: "sonnet",
  prompt: `
Mode: job-analysis
Skill: career
Workflow: career-advancement

Context:
- Resume: {auto-detected}
- CliftonStrengths: {auto-detected-or-none}
- Job: {url-or-text}

Instructions:
Execute career SKILL.md career-advancement workflow:
1. GO/NO-GO assessment (resume + CliftonStrengths)
2. OSINT intelligence (if GO)
3. Interview prep (priority areas, Q&A, questions)
4. Deliverables (resume, cover letter)

Output: output/career/job-opportunities/{Company}-{Role}/
`
})
```

---

## Output Structure

```
output/career/job-opportunities/{Company}-{Role}/
├── metadata.json             # Application tracking (phase, match_score, go_no_go)
├── 1-EXECUTIVE-SUMMARY.md    # GO/NO-GO + Intelligence + Priority Areas + Q&A (comprehensive)
├── 2-RESUME.md               # Optimized resume tailored to role
└── 3-COVER-LETTER.md         # 4-paragraph cover letter with OSINT insights
```

**Consolidated Output:** Executive Summary now contains all analysis (intelligence, priority areas, Q&A) in one comprehensive document with inline source citations per section.

---

## Metadata Tracking

**Create `metadata.json` at start of each analysis:**
```json
{
  "company": "{Company}",
  "role": "{Role}",
  "started_at": "YYYY-MM-DDTHH:MM:SS",
  "phase": "go_no_go|osint|interview_prep|deliverables|complete",
  "match_score": 0,
  "go_no_go": "pending|go|conditional|stop",
  "gates_passed": {
    "go_no_go": false,
    "osint": false,
    "deliverables": false
  },
  "job_url": "https://...",
  "application_status": "pending|applied|interviewing|rejected|offered"
}
```

**Update after each phase completes.**

---

## GO/NO-GO Gate (MANDATORY)

**This gate prevents wasted effort on poor-fit roles.**

| Score | Decision | Action |
|-------|----------|--------|
| >= 75% | GO | Proceed to OSINT + deliverables |
| 60-74% | CONDITIONAL | Explain gaps, user decides |
| < 60% | STOP | Provide feedback, suggest better-fit roles |

**STOP means STOP** - Do not proceed with OSINT or deliverables if score < 60%.

---

## Resume Modification Ethics

**NEVER FABRICATE EXPERIENCE:**
- ❌ Do NOT invent job responsibilities
- ❌ Do NOT add unused technologies/tools
- ❌ Do NOT fabricate achievements or metrics
- ✅ DO work with actual documented experience only

**When Major Gaps Exist:**
1. STOP and ASK USER before assumptions
2. Present gap: "Job requires X, but I don't see X in resume"
3. Explain career transition requirement
4. Adjust match score (deduct 10-15 points)
5. Wait for user input
6. Never guess undocumented experience
7. NEVER rewrite job functions to bridge gaps

**Resume Optimization Strategy:**
- Default resume = MAXIMUM length
- Goal: Make SHORTER and more focused per application
- Remove irrelevant positions
- Consolidate bullets
- Cut to 1-2 pages max
- Focus on relevant experience only

---

## Examples

### Strong Match (GO)

```
/job-analysis
→ Job: Senior Security Engineer (Fintech)

Result: ✅ GO (82/100) - Full OSINT, interview prep, 6 deliverables (~8 min)
```

### Poor Match (NO-GO)

```
/job-analysis
→ Job: Entry-level SOC Analyst

Result: ❌ NO-GO (45/100) - Overqualified, stopped (~2 min)
```

---

## Related Commands

- `/job-analysis` - Includes resume review and interview prep modes
- `/osint` - Standalone OSINT research

---

**Version:** 2.2
**Last Updated:** 2025-12-18
**Framework:** Intelligence Adjacent (IA)
**Changes:** Consolidated to 3 outputs, inline source citations, restored workflow files
