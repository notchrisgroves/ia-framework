---
name: skill-building
description: Career mentorship with 30/60/90-day learning roadmaps and ROI-focused certification guidance
---

# Skill Building Workflow

**Career development with progressive mentorship and learning tracking**

---

## Overview

Complete mentorship workflow for skill development and career progression.

**Output:** `output/career/learning-progress/{YYYY-MM-DD}/`

**Deliverables:**
1. `learning-roadmap.md` - 30/60/90-day action plan with resources
2. `skills-assessment.md` - Current state and gap analysis
3. `progress-tracker.md` - Milestone and session tracking

**Auto-Resource Detection:**
- Resume: `input/career/resume.md` (for current skills assessment)
- Learning history: `output/career/learning-progress/` (if exists)

**Time:** 15-30 minutes

---

## Philosophy

- **Free resources first** - Prioritize open-source over expensive certifications
- **Hands-on over theory** - Labs and practice > lectures
- **Portfolio visible** - Build publicly (GitHub, blog, CTFs)
- **ROI-focused** - Certifications only if proven job market value
- **Network strategically** - Communities, conferences, mentors

---

## Workflow Phases

### Phase 1: Assessment

**Current State Analysis:**

1. **Skills Inventory:**
   - Technical skills (from resume)
   - Certifications held
   - Tools and platforms experience
   - Domain knowledge

2. **Gap Analysis:**
   - Target role requirements
   - Missing skills or certifications
   - Experience level gaps
   - Knowledge areas to develop

3. **Define Objectives:**
   - Career goal (role, timeline)
   - Skill targets
   - Certification goals (if ROI-positive)
   - Portfolio projects needed

---

### Phase 2: Planning (30/60/90-Day Framework)

#### Month 1: Foundation
**Goals: Assess, Learn Basics, Start Portfolio**

| Week | Focus | Deliverable |
|------|-------|-------------|
| 1-2 | Complete skills inventory, research target roles | Skills assessment |
| 3-4 | Core concepts, tools setup, first labs | Foundation completed |

**Activities:**
- Core concepts and fundamentals
- Tools and platforms setup
- Basic hands-on labs
- Join relevant communities
- GitHub profile setup

#### Month 2: Building
**Goals: Deep Dive, Practice, Network**

| Week | Focus | Deliverable |
|------|-------|-------------|
| 5-6 | Specialized learning, advanced labs | Deeper knowledge |
| 7-8 | Practice projects, networking | Portfolio projects |

**Activities:**
- Specialized learning in target area
- TryHackMe/HackTheBox (if security)
- Open-source contributions
- Join Discord/Slack communities
- 2-3 portfolio projects

#### Month 3: Application
**Goals: Apply Skills, Certify (if valuable), Job Prep**

| Week | Focus | Deliverable |
|------|-------|-------------|
| 9-10 | Real projects, certification prep | Capstone project |
| 11-12 | Job prep, applications | Updated resume |

**Activities:**
- Capstone portfolio project
- Certification (if ROI-positive)
- Resume update with new skills
- Job applications begin
- Blog posts about projects

---

### Phase 3: Resources

#### Free/Low-Cost Platforms (Prioritized)

**Security:**
| Platform | Cost | Focus |
|----------|------|-------|
| TryHackMe | Free/$10/mo | Guided learning paths |
| HackTheBox | Free tier | Challenge-based |
| PentesterLab | Free exercises | Web security |
| OverTheWire | Free | Wargames |
| picoCTF | Free | CTF practice |

**General Tech:**
| Platform | Cost | Focus |
|----------|------|-------|
| freeCodeCamp | Free | Web development |
| Codecademy | Free tier | Multiple languages |
| Coursera | Audit free | University courses |
| YouTube | Free | Conference talks, tutorials |

**Communities:**
- Discord servers (InfoSec, DevSec)
- Reddit (r/cybersecurity, r/netsec)
- Twitter/X (follow practitioners)
- Local meetups

#### Certification ROI Analysis

**Before recommending ANY certification:**

| Factor | Question |
|--------|----------|
| Job posting frequency | How often required/preferred? |
| Salary differential | With cert vs without? |
| Cost | Exam + training + time? |
| Difficulty | Pass rate, prep time? |
| Market recognition | Do employers know it? |

**Rule:** Only recommend if expected salary increase > cost within 6-12 months.

**De-Prioritize:**
- Expensive bootcamps ($10K+) without job guarantees
- Certifications without market demand
- Theory-heavy courses without labs
- Outdated training materials

---

### Phase 4: Tracking

#### Session-Based Tracking

**For each learning session:**
- Date and duration
- Objectives for session
- Skills practiced
- Resources used
- Challenges completed
- Next session goals

#### Milestone Tracking

**Long-term progress:**
- Skills mastered (learning → proficient → expert)
- Projects completed
- Certifications earned
- Job applications submitted
- Interviews completed
- Network connections made

---

## Skill Development Tracks

### Defensive Security Track
**SOC Analyst → Incident Response → Threat Intel → Security Architect**

| Phase | Skills | Certifications |
|-------|--------|----------------|
| Entry | SIEM, log analysis | Security+ |
| Mid | Threat hunting, IR | CySA+, GCIH |
| Senior | Architecture, strategy | CISSP |

### Offensive Security Track
**Pentester → Red Team → Bug Bounty → Security Researcher**

| Phase | Skills | Certifications |
|-------|--------|----------------|
| Entry | Web app testing, OWASP | eJPT |
| Mid | Network pentest, AD attacks | OSCP |
| Senior | Exploit dev, tool dev | OSWE, OSCE |

### Specialized Tracks

**Cloud Security:**
- AWS/Azure/GCP security services
- IAM and identity
- Compliance (SOC 2, ISO 27001)
- Infrastructure as Code

**Application Security:**
- Secure coding practices
- Code review and SAST
- DevSecOps pipelines
- Container security

---

## Output Templates

### learning-roadmap.md

```markdown
# Learning Roadmap

**Created:** {YYYY-MM-DD}
**Target Role:** {Role}
**Timeline:** 90 days

---

## Month 1: Foundation (Weeks 1-4)

### Objectives
- [ ] Complete skills assessment
- [ ] Set up learning environment
- [ ] Complete foundational labs
- [ ] Join 2+ communities

### Resources
| Resource | Type | Link |
|----------|------|------|
| [Platform] | Labs | [URL] |
| [Course] | Theory | [URL] |
| [Community] | Network | [URL] |

### Deliverables
- [ ] Skills assessment document
- [ ] GitHub profile setup
- [ ] First project outline

---

## Month 2: Building (Weeks 5-8)

### Objectives
- [ ] Complete intermediate labs
- [ ] Build 2-3 portfolio projects
- [ ] Make 5+ network connections
- [ ] Contribute to open source

### Resources
[Same format]

### Deliverables
- [ ] 2-3 portfolio projects
- [ ] Network connections made
- [ ] Progress documented

---

## Month 3: Application (Weeks 9-12)

### Objectives
- [ ] Complete capstone project
- [ ] Certification (if pursuing)
- [ ] Update resume
- [ ] Begin applications

### Resources
[Same format]

### Deliverables
- [ ] Capstone project complete
- [ ] Updated resume
- [ ] Job applications started
```

### skills-assessment.md

```markdown
# Skills Assessment

**Assessment Date:** {YYYY-MM-DD}
**Target Role:** {Role}

---

## Current Skills

### Technical Skills
| Skill | Level | Evidence |
|-------|-------|----------|
| [Skill] | Beginner/Intermediate/Expert | [Where demonstrated] |

### Certifications
| Certification | Status | Expiry |
|--------------|--------|--------|
| [Cert] | Active/Expired/Pursuing | [Date] |

### Tools & Platforms
- [Tool 1]
- [Tool 2]

---

## Gap Analysis

### Required for Target Role
| Requirement | Current Level | Gap |
|-------------|---------------|-----|
| [Skill] | [Level] | [What's missing] |

### Priority Learning Areas
1. [Highest priority skill]
2. [Second priority]
3. [Third priority]

---

## Certification ROI Analysis

### Considered: [Certification Name]

| Factor | Assessment |
|--------|------------|
| Job posting frequency | X% of target roles require |
| Salary differential | +$X,XXX average |
| Cost | $X,XXX (exam + prep) |
| Prep time | X months |
| Market recognition | High/Medium/Low |

**Recommendation:** [Pursue/Skip/Defer]
```

### progress-tracker.md

```markdown
# Progress Tracker

**Started:** {YYYY-MM-DD}
**Target Role:** {Role}

---

## Milestone Progress

### Skills Development
| Skill | Start Level | Current | Target |
|-------|-------------|---------|--------|
| [Skill] | Beginner | Intermediate | Expert |

### Projects
| Project | Status | Link |
|---------|--------|------|
| [Project] | Complete/In Progress | [URL] |

### Certifications
| Certification | Status | Date |
|--------------|--------|------|
| [Cert] | Pursuing/Earned | [Date] |

---

## Session Log

### {YYYY-MM-DD} - Session X
**Duration:** X hours
**Focus:** [Topic]
**Completed:**
- [Task 1]
- [Task 2]

**Next Session:**
- [Goal 1]
- [Goal 2]
```

---

## Fast Mode (Default)

- No session tracking
- Direct execution → 3 deliverable files
- Complete in 15-30 minutes
- Single session plan creation

---

**Related:**
- `workflows/career-advancement.md` - Job application workflow
- `workflows/strengths-development.md` - CliftonStrengths coaching
