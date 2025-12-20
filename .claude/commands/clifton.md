---
name: clifton
description: CliftonStrengths coaching with theme analysis, blindspot identification, and development recommendations
---

# /clifton - CliftonStrengths Coaching

Deep analysis of your CliftonStrengths themes with brutally honest blindspot identification and development recommendations.

**Agent:** advisor
**Skill:** career (strengths-development mode)
**Output:** `output/career/strengths-analysis/{YYYY-MM-DD}/`

---

## Quick Start

```
/clifton
```

**Prerequisites:** CliftonStrengths report at `input/career/cliftonstrengths-all34.pdf`

**Or provide themes directly:**
```
/clifton My top 5: Strategic, Learner, Analytical, Achiever, Ideation
```

---

## When to Use

**Use /clifton when:**
- Want deep analysis of CliftonStrengths themes
- Need honest blindspot identification
- Exploring theme tensions and contradictions
- Want development recommendations (Name it, Claim it, Aim it)
- Understanding domain gaps

**Don't use if:**
- Need job application help → `/job-analysis`
- Want learning roadmap → `/mentorship`
- Don't have CliftonStrengths report

---

## What CliftonStrengths Measures

**Four Domains:**
- **Executing** - Get things done (Achiever, Responsibility, Focus)
- **Influencing** - Take charge, speak up (Command, Communication, Woo)
- **Relationship Building** - Hold teams together (Empathy, Harmony, Includer)
- **Strategic Thinking** - Focus on possibilities (Strategic, Analytical, Ideation)

**34 Talent Themes** ranked from dominant (#1) to lesser (#34)

---

## Workflow Phases

### Phase 1: Parse Strengths Data
- Top 5 or Full 34 themes
- Domain distribution analysis
- Signature theme identification

### Phase 2: Dominant Pattern Analysis
- #1 + #2 theme interaction
- How they amplify each other
- Natural behavior patterns

### Phase 3: Theme Tensions
- Contradicting themes (e.g., Deliberative + Activator)
- Overuse patterns (when strength becomes weakness)
- Situational conflicts

### Phase 4: Blindspot Analysis (Brutally Honest)
- Bottom 5 themes (if Full 34)
- Domain gaps (missing areas)
- Limitations to acknowledge
- Blind spots others see

### Phase 5: Development Recommendations
- **Name it** - Understand your themes
- **Claim it** - Own your natural talents
- **Aim it** - Apply intentionally

---

## Web Search Integration

**For current information:**
- Latest Gallup research on themes
- Career applications by strength
- Theme combination insights
- Industry fit analysis
- Leadership development resources

**Search sources:**
- Gallup Strengths Center
- CliftonStrengths community insights
- Theme-specific development resources
- Career fit research

---

## Agent Routing

```typescript
Task({
  subagent_type: "advisor",
  model: "sonnet",
  prompt: `
Mode: strengths
Skill: career
Workflow: strengths-development

CliftonStrengths Report: {auto-detected or provided}

Instructions:
1. Parse themes (Top 5 or Full 34)
2. Analyze dominant pattern (#1 + #2)
3. Identify theme tensions
4. Provide BRUTALLY HONEST blindspot analysis
5. Development recommendations

Output: output/career/strengths-analysis/{YYYY-MM-DD}/
`
})
```

---

## Output Structure

```
output/career/strengths-analysis/{YYYY-MM-DD}/
├── STRENGTHS-ANALYSIS.md     # Full theme analysis
├── BLINDSPOT-REPORT.md       # Honest limitations
└── DEVELOPMENT-PLAN.md       # Name/Claim/Aim recommendations
```

---

## Examples

### Top 5 Analysis
```
/clifton Strategic, Learner, Analytical, Achiever, Ideation

→ Domain: Heavy Strategic Thinking (4/5)
→ Pattern: Analysis paralysis risk (Analytical + Strategic)
→ Blindspot: Relationship Building domain gap
→ Development: Partner with Relator/Harmony types
```

### Full 34 Analysis
```
/clifton [Full report provided]

→ Top 5 deep dive
→ Bottom 5 limitations (e.g., #34 Woo = networking challenge)
→ Theme tensions (Deliberative vs Activator)
→ Domain gaps with mitigation strategies
```

---

## Honest Feedback Principle

This analysis is intentionally **brutally honest**:
- We identify real limitations, not just strengths
- Bottom themes matter - they're natural weaknesses
- Theme tensions create real friction
- Overused strengths become liabilities
- Domain gaps affect team dynamics

**The goal:** Self-awareness, not validation.

---

## Related Commands

- `/job-analysis` - Uses strengths for role fit (NOT interview prep)
- `/mentorship` - Skill development planning

---

**Version:** 1.0
**Last Updated:** 2025-12-19
**Framework:** Intelligence Adjacent (IA)
