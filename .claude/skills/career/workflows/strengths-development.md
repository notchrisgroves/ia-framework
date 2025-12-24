---
name: strengths-development
description: CliftonStrengths coaching with brutally honest blindspot analysis and team comparison using Gallup methodology
---

# Strengths Development Workflow

**CliftonStrengths coaching with brutally honest assessment and team analysis**

---

## Overview

Complete CliftonStrengths coaching workflow supporting both individual analysis and team comparison.

**Modes:**
- **Individual Mode** - Deep dive into one person's profile
- **Team Mode** - Compare multiple profiles, identify gaps and partnerships

**Output:** `output/career/strengths-analysis/{YYYY-MM-DD}/`

**Auto-Resource Detection:**
- Individual: `input/career/cliftonstrengths-all34.pdf`
- Team: `input/career/team/*.pdf` or provided in conversation

---

## Mode Detection

**Individual Mode (Default):**
- Single person's CliftonStrengths report provided
- Keywords: "my strengths", "analyze my themes", "clifton coaching"

**Team Mode:**
- Multiple profiles provided (PDFs or theme lists)
- Keywords: "compare team", "team strengths", "our team", "team analysis", "partnership"

---

## The Four Domains

| Domain | Themes | Description |
|--------|--------|-------------|
| **EXECUTING** (Purple) | Achiever, Arranger, Belief, Consistency, Deliberative, Discipline, Focus, Responsibility, Restorative | Get things done |
| **INFLUENCING** (Orange) | Activator, Command, Communication, Competition, Maximizer, Self-Assurance, Significance, Woo | Lead and persuade |
| **RELATIONSHIP** (Blue) | Adaptability, Connectedness, Developer, Empathy, Harmony, Includer, Individualization, Positivity, Relator | Connect and unite |
| **STRATEGIC** (Green) | Analytical, Context, Futuristic, Ideation, Input, Intellection, Learner, Strategic | Analyze and plan |

**Note:** Influencing is statistically the RAREST domain (appears in only 15% of Top 5s)

---

## Individual Mode: 5 Phases

### Phase 1: Parse Strengths Data

**Extract from CliftonStrengths Report:**

1. **Theme Rankings** - All 34 themes in order (or Top 5)
2. **Domain Distribution** - Count themes per domain
3. **Identify Signature Themes** - Top 5 as core identity

**Create Table:**
```markdown
| Rank | Theme | Domain |
|------|-------|--------|
| 1 | [Theme] | [Domain] |
| 2 | [Theme] | [Domain] |
...
```

---

### Phase 2: Dominant Pattern Analysis

**Focus on #1 + #2 Theme Interaction**

The top two themes create a unique behavioral signature.

**Analysis Framework:**
- How do these amplify each other?
- What unique behavior does this combination create?
- What's the "signature move"?
- Career/role implications?
- Risk patterns?

**Example Pattern:**
```
Connectedness (#1) + Achiever (#2) = "The Purposeful Workhorse"
- Meaning drives execution (Connectedness provides "why")
- Tireless effort when work matters (Achiever provides stamina)
- Struggles with meaningless busywork
- Risk: Burnout when purpose unclear
```

---

### Phase 3: Theme Tensions

**Identify Contradictions:**

| Tension Type | Example | Impact |
|--------------|---------|--------|
| Contradicting themes | Deliberative vs Activator | Decision paralysis vs action bias |
| Overuse patterns | Achiever → burnout | Never satisfied, work addiction |
| Missing domains | 0 Influencing themes | Leadership visibility challenges |

**Common Tension Pairs:**
- Discipline (structure) vs Ideation (exploration)
- Harmony (consensus) vs Command (decisive action)
- Deliberative (caution) vs Activator (urgency)
- Maximizer (excellence) vs Restorative (fixing)

---

### Phase 4: Blindspot Analysis

**Most Important Part - Brutally Honest Assessment**

#### Bottom 5 Themes (if Full 34)

These are natural non-talents. Gallup research shows you CANNOT effectively develop these.

**Strategy:** Partner with someone strong here, don't try to fix.

**Bottom 5 Table:**
```markdown
| Rank | Theme | What This Means |
|------|-------|-----------------|
| 30 | [Theme] | [Practical implication] |
| 31 | [Theme] | [Practical implication] |
| 32 | [Theme] | [Practical implication] |
| 33 | [Theme] | [Practical implication] |
| 34 | [Theme] | [Practical implication] |
```

#### Domain Gaps

Zero themes in a domain = significant structural blindspot.

#### Overuse Patterns

| Theme | Overuse Risk | Warning Signs |
|-------|--------------|---------------|
| Achiever | Workaholism | Never celebrating, always more |
| Responsibility | Overcommitment | Can't say no, martyr complex |
| Empathy | Emotional exhaustion | Absorbing others' emotions |
| Command | Intimidation | Bulldozing, not listening |
| Maximizer | Perfectionism paralysis | Never good enough |

---

### Phase 5: Development Recommendations

**"Name It, Claim It, Aim It" Framework**

#### Name It
- Recognize your specific patterns
- Understand theme interactions
- Know your situational triggers

#### Claim It
- Accept these as natural patterns
- Stop fighting your nature
- Embrace what you're NOT good at
- Find partners who complement weaknesses

#### Aim It
1. **Role/Environment Fit** - Where do you thrive vs drain?
2. **Team Complementary** - What themes do you need around you?
3. **Action Items** - Specific, actionable recommendations

---

## Team Mode: 6 Phases

### Phase T1: Collect Team Profiles

**Input Methods:**
- Multiple PDF reports provided
- Theme lists in conversation (Top 5 or Full 34 per person)
- Mix of both

**Create Master List:**
```markdown
| Team Member | #1 | #2 | #3 | #4 | #5 |
|-------------|----|----|----|----|----|
| Alice | Strategic | Learner | Achiever | Input | Ideation |
| Bob | Connectedness | Achiever | Belief | Responsibility | Developer |
| Carol | Command | Activator | Woo | Competition | Self-Assurance |
```

---

### Phase T2: Generate Team Grid

**Domain-Organized View:**

```markdown
## Team Grid by Domain

### EXECUTING
| Member | Themes in Domain |
|--------|------------------|
| Alice | Achiever (#3) |
| Bob | Achiever (#2), Belief (#3), Responsibility (#4) |
| Carol | - |

### INFLUENCING
| Member | Themes in Domain |
|--------|------------------|
| Alice | - |
| Bob | - |
| Carol | Command (#1), Activator (#2), Woo (#3), Competition (#4), Self-Assurance (#5) |

### RELATIONSHIP BUILDING
| Member | Themes in Domain |
|--------|------------------|
| Alice | - |
| Bob | Connectedness (#1), Developer (#5) |
| Carol | - |

### STRATEGIC THINKING
| Member | Themes in Domain |
|--------|------------------|
| Alice | Strategic (#1), Learner (#2), Input (#4), Ideation (#5) |
| Bob | - |
| Carol | - |
```

---

### Phase T3: Domain Distribution Analysis

**Visual Distribution:**
```markdown
## Team Domain Coverage

               EXECUTING    INFLUENCING    RELATIONSHIP    STRATEGIC
Alice    [    *           ]              ]               [****        ]
Bob      [    ***         ]              ] **            ]            ]
Carol    [                ] *****        ]               ]            ]
─────────────────────────────────────────────────────────────────────
TEAM     [    ****        ] *****        ] **            ] ****       ]

Legend: Each * = 1 theme in Top 5
```

**Summary Table:**
```markdown
| Domain | Team Count | Coverage | Status |
|--------|------------|----------|--------|
| Executing | 4 | 27% | ADEQUATE |
| Influencing | 5 | 33% | STRONG |
| Relationship | 2 | 13% | GAP |
| Strategic | 4 | 27% | ADEQUATE |
```

---

### Phase T4: Theme Frequency Analysis

**Most Common Themes on Team:**
```markdown
| Theme | Frequency | Members |
|-------|-----------|---------|
| Achiever | 2 | Alice, Bob |
| [Next] | X | [Names] |
```

**Completely Missing Themes:**
List themes with 0 representation across team.

---

### Phase T5: Partnership Recommendations

**Complementary Pairs:**

Identify which team members naturally complement each other.

```markdown
## Recommended Partnerships

### Alice + Bob
**Complementary:** Alice's Strategic Thinking + Bob's Executing
**Value:** Alice generates strategies, Bob implements them
**Watch:** Alice may move too fast for Bob's methodical approach

### Bob + Carol
**Complementary:** Bob's Relationship Building + Carol's Influencing
**Value:** Bob builds trust, Carol amplifies message
**Watch:** Carol's Command may overwhelm Bob's Harmony-seeking

### Alice + Carol
**Complementary:** Alice's analysis + Carol's action
**Value:** Fast from insight to execution
**Watch:** May leave Bob behind (Relationship gap)
```

---

### Phase T6: Team Development Plan

**Gap Mitigation:**
- Identify missing domains/themes
- Recommend hiring profiles or external partners
- Suggest team rituals that compensate for gaps

**Conflict Prevention:**
- Identify tension points between members
- Create communication protocols
- Establish decision-making frameworks

**Collective Strengths:**
- What this team does exceptionally well
- Ideal project types
- Roles to avoid as a team

---

## Output Templates

### Individual Mode Output

```
output/career/strengths-analysis/{YYYY-MM-DD}/
├── STRENGTHS-ANALYSIS.md     # Full theme breakdown
├── BLINDSPOT-REPORT.md       # Brutally honest limitations
└── DEVELOPMENT-PLAN.md       # Name/Claim/Aim recommendations
```

### Team Mode Output

```
output/career/strengths-analysis/{YYYY-MM-DD}/
├── TEAM-GRID.md              # Visual team composition
├── DOMAIN-ANALYSIS.md        # Coverage and gaps
├── PARTNERSHIP-MAP.md        # Complementary partnerships
└── TEAM-DEVELOPMENT.md       # Collective recommendations
```

---

## Output Format Standards

**Clean Professional Markdown:**
- Use tables for structured data (not bullet lists)
- Horizontal rules between major sections
- Clear hierarchy (H1 → H2 → H3)
- Consistent column widths in tables

**Visual Elements:**
- ASCII domain charts for at-a-glance understanding
- Summary boxes for key insights
- Clean tables with alignment

**Resource Links:**
Include relevant Gallup and community resources at end of each document.

---

## Additional Resources Section

**Include in every output file:**

```markdown
---

## Additional Resources

### Official Gallup Resources
- [CliftonStrengths Assessment](https://www.gallup.com/cliftonstrengths/)
- [Theme Definitions](https://www.gallup.com/cliftonstrengths/en/253715/34-cliftonstrengths-themes.aspx)
- [Find a Certified Coach](https://www.gallupstrengthscenter.com/)

### Research & Development
- [Strengths-Based Leadership Research](https://www.gallup.com/workplace/266822/strengths-based-leadership.aspx)
- [Team Strengths Resources](https://www.gallup.com/cliftonstrengths/en/254039/team.aspx)

### Theme Deep Dives
- Search: "CliftonStrengths [Theme Name] development"
- Gallup Access articles on specific theme combinations
- Strengths community forums for real-world application stories
```

---

## Fast Mode (Default)

- No session tracking
- Direct execution → deliverable files
- Individual: 15-20 minutes
- Team: 25-40 minutes (depending on team size)
- Single session

---

## Quality Checklist

Before delivering output:

- [ ] All themes correctly categorized by domain
- [ ] Bottom 5 included (if Full 34 provided)
- [ ] Brutally honest tone (not validation-seeking)
- [ ] Actionable recommendations (not generic advice)
- [ ] Tables properly formatted
- [ ] Resource links included
- [ ] File names follow convention

---

**Related:**
- `workflows/career-advancement.md` - Job application workflow (uses strengths for GO/NO-GO)
- `workflows/skill-building.md` - Mentorship and learning
- `input/career/cliftonstrengths-analysis.md` - Complete theme reference
