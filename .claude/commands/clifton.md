---
name: clifton
description: CliftonStrengths coaching with individual analysis, team comparison, and development recommendations
---

# /clifton - CliftonStrengths Coaching

Deep analysis of CliftonStrengths themes with brutally honest blindspot identification, team comparison, and development recommendations.

**Agent:** advisor
**Skill:** career (strengths-development mode)
**Output:** `output/career/strengths-analysis/{YYYY-MM-DD}/`

---

## Quick Start

**Individual Analysis:**
```
/clifton
```

**Team Comparison:**
```
/clifton compare our team strengths
```

---

## Two Modes

### Individual Mode (Default)

Analyze a single person's CliftonStrengths profile.

**Prerequisites:** CliftonStrengths report at `input/career/cliftonstrengths-all34.pdf`

**Or provide themes directly:**
```
/clifton My top 5: Strategic, Learner, Analytical, Achiever, Ideation
```

**Output:**
- `STRENGTHS-ANALYSIS.md` - Full theme breakdown
- `BLINDSPOT-REPORT.md` - Brutally honest limitations
- `DEVELOPMENT-PLAN.md` - Name/Claim/Aim recommendations

---

### Team Mode

Compare multiple profiles and identify partnerships and gaps.

**Provide multiple profiles:**
```
/clifton compare team:
- Alice: Strategic, Learner, Achiever, Input, Ideation
- Bob: Connectedness, Achiever, Belief, Responsibility, Developer
- Carol: Command, Activator, Woo, Competition, Self-Assurance
```

**Or use team folder:**
Place multiple PDF reports in `input/career/team/`

**Output:**
- `TEAM-GRID.md` - Visual team composition by domain
- `DOMAIN-ANALYSIS.md` - Coverage gaps and balance
- `PARTNERSHIP-MAP.md` - Complementary partnerships
- `TEAM-DEVELOPMENT.md` - Collective recommendations

---

## When to Use

**Use /clifton when:**
- Want deep analysis of CliftonStrengths themes (individual or team)
- Need honest blindspot identification
- Exploring theme tensions and contradictions
- Understanding domain gaps
- Building team composition strategy
- Finding complementary partnerships

**Don't use if:**
- Need job application help (use `/job-analysis`)
- Want learning roadmap (use `/mentorship`)
- Don't have CliftonStrengths data

---

## The Four Domains

| Domain | Color | Themes | Question Answered |
|--------|-------|--------|-------------------|
| **Executing** | Purple | Achiever, Arranger, Belief, Consistency, Deliberative, Discipline, Focus, Responsibility, Restorative | How do you make things happen? |
| **Influencing** | Orange | Activator, Command, Communication, Competition, Maximizer, Self-Assurance, Significance, Woo | How do you influence others? |
| **Relationship** | Blue | Adaptability, Connectedness, Developer, Empathy, Harmony, Includer, Individualization, Positivity, Relator | How do you build relationships? |
| **Strategic** | Green | Analytical, Context, Futuristic, Ideation, Input, Intellection, Learner, Strategic | How do you analyze information? |

**Note:** Influencing is statistically the RAREST domain (appears in only 15% of Top 5s)

---

## Individual Workflow

### Phase 1: Parse Strengths Data
- Theme rankings (Top 5 or Full 34)
- Domain distribution
- Signature theme identification

### Phase 2: Dominant Pattern Analysis
- #1 + #2 theme interaction
- Unique behavioral signature
- Career implications

### Phase 3: Theme Tensions
- Contradicting themes (e.g., Deliberative + Activator)
- Overuse patterns
- Missing domains

### Phase 4: Blindspot Analysis (Brutally Honest)
- Bottom 5 themes (if Full 34)
- Domain gaps
- Limitations to acknowledge

### Phase 5: Development Recommendations
- **Name it** - Understand your themes
- **Claim it** - Own your natural talents
- **Aim it** - Apply intentionally

---

## Team Workflow

### Phase T1: Collect Team Profiles
- Gather all team members' Top 5 or Full 34
- Create master theme list

### Phase T2: Generate Team Grid
- Visual representation by domain
- Who has what themes

### Phase T3: Domain Distribution
- Coverage analysis
- Gap identification
- Balance assessment

### Phase T4: Theme Frequency
- Most common themes on team
- Missing themes across team

### Phase T5: Partnership Recommendations
- Complementary pairs
- Who should work together
- Tension points to watch

### Phase T6: Team Development
- Gap mitigation strategies
- Hiring recommendations
- Team rituals for balance

---

## Examples

### Individual - Top 5 Only
```
/clifton My top 5: Strategic, Learner, Analytical, Achiever, Ideation

→ Domain: Heavy Strategic Thinking (4/5)
→ Pattern: Analysis paralysis risk (Analytical + Strategic)
→ Blindspot: Relationship Building domain gap
→ Development: Partner with Relator/Harmony types
```

### Individual - Full 34
```
/clifton (with PDF report provided)

→ Top 5 deep dive with personalized insights
→ Bottom 5 limitations (e.g., #34 Woo = networking challenge)
→ Theme tensions identified
→ Domain gaps with mitigation strategies
```

### Team Comparison
```
/clifton compare team:
- Product Manager: Strategic, Ideation, Learner, Futuristic, Input
- Tech Lead: Achiever, Responsibility, Analytical, Discipline, Focus
- Designer: Empathy, Individualization, Developer, Positivity, Adaptability

→ Team Grid generated
→ Strong: Strategic (PM), Executing (Tech), Relationship (Designer)
→ Gap: Zero Influencing themes across team
→ Recommendation: Add someone with Communication/Woo for stakeholder management
```

---

## Output Format

All outputs are clean professional Markdown:
- Tables for structured data
- Horizontal rules between sections
- Clear visual hierarchy
- ASCII charts for domain distribution
- Resource links included

---

## Honest Feedback Principle

This analysis is intentionally **brutally honest**:
- Real limitations identified, not just strengths
- Bottom themes matter (natural weaknesses)
- Theme tensions create real friction
- Overused strengths become liabilities
- Domain gaps affect team dynamics

**The goal:** Self-awareness, not validation.

---

## Additional Resources

### Official Gallup
- [CliftonStrengths Assessment](https://www.gallup.com/cliftonstrengths/)
- [34 Theme Definitions](https://www.gallup.com/cliftonstrengths/en/253715/34-cliftonstrengths-themes.aspx)
- [Find a Certified Coach](https://www.gallupstrengthscenter.com/)

### Team Resources
- [Team Strengths](https://www.gallup.com/cliftonstrengths/en/254039/team.aspx)
- [Strengths-Based Leadership](https://www.gallup.com/workplace/266822/strengths-based-leadership.aspx)

---

## Related Commands

- `/job-analysis` - Uses strengths for role fit assessment
- `/mentorship` - Skill development planning

---

**Version:** 2.0
**Last Updated:** 2025-12-23
**Framework:** Intelligence Adjacent (IA)
