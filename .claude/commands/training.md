---
name: training
description: Personalized fitness programming with assessment, routine generation, nutrition guidance, and progress tracking
---

# /training - Fitness Program Design

Personalized workout programs tailored to your goals, equipment, and schedule.

**Agent:** advisor
**Skill:** personal-training
**Output:** `output/health/fitness/{program-name}-{YYYY-MM}/`

---

## Quick Start

```
/training
```

**Or with context:**
```
/training I want to build strength, have dumbbells, 30 min 4x/week
```

---

## When to Use

**Use /training when:**
- Need a personalized workout program
- Want structured training plan with progression
- Need program adjusted for equipment/time constraints
- Want nutrition guidance to support fitness goals
- Need to track and adjust based on progress

**Don't use if:**
- Medical condition affecting exercise (consult doctor first)
- Need physical therapy exercises (see qualified therapist)

---

## Workflow

### Phase 1: Assessment (7 Questions)

Quick multi-choice assessment:
1. **Primary Goal** - Strength, Endurance, Weight Loss, Flexibility, General
2. **Fitness Level** - Beginner, Intermediate, Advanced
3. **Available Time** - 15min, 20-30min, 45-60min, Flexible
4. **Equipment** - None, Minimal, Home Gym, Full Gym
5. **Frequency** - 2-3x, 4x, 5-6x per week
6. **Limitations** - Joint issues, back problems, mobility (optional)
7. **Schedule** - Morning, Midday, Evening, Flexible

### Phase 2: Program Design

Based on assessment:
- Periodized training plan (4-week mesocycles)
- Progressive overload built-in
- Balanced push/pull/legs
- Recovery scheduling

### Phase 3: Deliverables

```
output/health/fitness/{program-name}-{YYYY-MM}/
├── PROGRAM-OVERVIEW.md       # Goals, schedule, principles
├── WEEKLY-ROUTINE.md         # Current week's workouts
├── EXERCISE-LIBRARY.md       # Exercise descriptions + form
├── NUTRITION-GUIDE.md        # Meal templates, macros
└── PROGRESS-TRACKER.md       # Weekly check-ins
```

---

## Web Search Integration

**For updated information:**
- Latest exercise science research
- Current nutrition guidelines (ISSN, ACSM)
- Exercise form videos and tutorials
- Equipment reviews and recommendations

**Search sources:**
- NSCA (National Strength & Conditioning Association)
- ACSM (American College of Sports Medicine)
- Examine.com (nutrition research)
- Stronger by Science (evidence-based training)

---

## Agent Routing

```typescript
Task({
  subagent_type: "advisor",
  model: "sonnet",
  prompt: `
Mode: training
Skill: personal-training
Workflow: program-design

Instructions:
1. Run assessment (or use provided context)
2. Design periodized program
3. Generate deliverables with nutrition guidance
4. Include exercise form cues

Output: output/health/fitness/{program-name}-{YYYY-MM}/
`
})
```

---

## Disclaimer

> This program is for informational purposes only and is not a substitute for professional medical advice. Consult a physician before starting any exercise program.

---

## Related Commands

- `/wellness` - Holistic health and natural remedies

---

**Version:** 1.0
**Last Updated:** 2025-12-19
**Framework:** Intelligence Adjacent (IA)
