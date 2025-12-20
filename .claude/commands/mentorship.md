---
name: mentorship
description: Skill building with learning roadmaps, 30/60/90-day plans, certifications, and career progression guidance
---

# /mentorship - Skill Building & Career Development

Structured skill development with personalized learning roadmaps, certification guidance, and portfolio development.

**Agent:** advisor
**Skill:** career (skill-building mode)
**Output:** `output/career/learning-progress/{YYYY-MM-DD}/`

---

## Quick Start

```
/mentorship
```

**Or with context:**
```
/mentorship create a cybersecurity learning roadmap for cloud security
/mentorship 90-day plan for OSCP preparation
/mentorship portfolio projects for security engineering role
```

---

## When to Use

**Use /mentorship when:**
- Need structured learning roadmap for new skills
- Want 30/60/90-day development plans
- Researching certification paths and ROI
- Building portfolio with practical projects
- Career progression guidance

**Don't use if:**
- Need job application help → `/job-analysis`
- Want CliftonStrengths coaching → `/strengths`

---

## Workflow Phases

### Phase 1: Assessment
- Current skills inventory
- Gap analysis (where you are vs where you want to be)
- Clear objectives definition
- Timeline and constraints

### Phase 2: Planning (30/60/90-Day)

**Days 1-30: Foundation**
- Core concepts and fundamentals
- Platform onboarding
- Initial certifications (if applicable)

**Days 31-60: Building**
- Hands-on labs and practice
- Intermediate projects
- Community engagement

**Days 61-90: Application**
- Portfolio projects
- Advanced certifications
- Real-world application

### Phase 3: Resources

**Free Platforms Prioritized:**
- TryHackMe (hands-on security)
- HackTheBox (advanced challenges)
- PortSwigger Web Security Academy
- SANS Cyber Aces
- Coursera/edX (audit mode)

**Certification ROI Analysis:**
- Cost vs market value
- Time investment
- Prerequisites
- Career impact

### Phase 4: Tracking
- Milestone tracking template
- Session notes format
- Portfolio project ideas
- Progress metrics

---

## Web Search Integration

**For current information:**
- Latest certification requirements and costs
- Current job market demands
- Updated learning platform content
- Industry trends and in-demand skills
- Conference and networking opportunities

**Search sources:**
- Certification body websites (ISC2, ISACA, CompTIA, OffSec)
- Job boards for skill demand analysis
- Industry reports (SANS, Gartner)
- Community forums (Reddit, Discord)

---

## Agent Routing

```typescript
Task({
  subagent_type: "advisor",
  model: "sonnet",
  prompt: `
Mode: mentorship
Skill: career
Workflow: skill-building

Instructions:
1. Run assessment (current skills, goals, timeline)
2. Create 30/60/90-day structured plan
3. Research current certification requirements
4. Provide free platform recommendations
5. Generate portfolio project ideas

Output: output/career/learning-progress/{YYYY-MM-DD}/
`
})
```

---

## Output Structure

```
output/career/learning-progress/{YYYY-MM-DD}/
├── LEARNING-ROADMAP.md       # Full 30/60/90 plan
├── RESOURCES.md              # Platforms, courses, certifications
└── PROGRESS-TRACKER.md       # Milestones and tracking
```

---

## Examples

### Cybersecurity Entry
```
/mentorship I want to break into cybersecurity, currently a sysadmin

→ Assessment: Current IT skills, security gaps
→ 30/60/90 plan: Network+ → Security+ → hands-on labs
→ Resources: TryHackMe path, CompTIA prep
→ Portfolio: Home lab setup, CTF writeups
```

### Advanced Specialization
```
/mentorship preparing for OSCP, have Security+ and 2 years SOC experience

→ Assessment: Current pentest skills
→ 30/60/90 plan: Focused OSCP prep
→ Resources: TryHackMe Offensive path, HackTheBox, PG Practice
→ Portfolio: CTF writeups, vulnerability research
```

---

## Related Commands

- `/job-analysis` - Job application workflow
- `/clifton` - CliftonStrengths coaching

---

**Version:** 1.0
**Last Updated:** 2025-12-19
**Framework:** Intelligence Adjacent (IA)
