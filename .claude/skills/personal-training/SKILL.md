---
name: personal-training
description: Personalized fitness programming with assessment, routine generation, nutrition guidance, and progress tracking
---

# Personal Training Skill

**Personalized fitness programs tailored to individual goals, equipment, and schedule**

---

## Quick Start

```
"Create a workout program for me"
"I want to get stronger but only have 20 minutes"
"Design a home workout routine without equipment"
```

**Output:** `output/health/fitness/{program-name}-{YYYY-MM}/`

---

## Mode Detection

| User Request | Mode | Workflow |
|--------------|------|----------|
| "Create workout program" | Program Design | `workflows/program-design.md` |
| "Update my routine" | Program Adjustment | `workflows/program-adjustment.md` |
| "Track my progress" | Progress Review | `workflows/progress-review.md` |
| "Nutrition guidance" | Nutrition Planning | `workflows/nutrition-planning.md` |

---

## Phase 1: Initial Assessment

**Gather through multi-choice questions (5-7 questions max):**

### Question 1: Primary Goal
- **Strength** - Build muscle, increase lifting capacity
- **Endurance** - Improve cardiovascular fitness, stamina
- **Weight Loss** - Reduce body fat, improve body composition
- **Flexibility** - Increase mobility, reduce stiffness
- **General Fitness** - Overall health improvement

### Question 2: Current Fitness Level
- **Beginner** - New to exercise or returning after 6+ months
- **Intermediate** - Consistent exercise 3-6 months
- **Advanced** - Regular training 1+ years

### Question 3: Available Time
- **15 minutes** - Quick daily routine
- **20-30 minutes** - Standard session
- **45-60 minutes** - Comprehensive workout
- **Flexible** - Varies by day

### Question 4: Equipment Access
- **None** - Bodyweight only
- **Minimal** - Resistance bands, dumbbells
- **Home Gym** - Barbell, bench, rack
- **Full Gym** - Commercial gym access

### Question 5: Training Frequency
- **2-3x/week** - Maintenance/beginner
- **4x/week** - Balanced progression
- **5-6x/week** - Intensive training

### Question 6: Limitations (Optional)
- Joint issues (specify)
- Back problems
- Time constraints
- Mobility limitations
- None

### Question 7: Schedule Preference
- **Morning** - Before work
- **Midday** - Lunch break
- **Evening** - After work
- **Flexible** - Varies

---

## Phase 2: Program Design

### Training Principles Applied

**Progressive Overload:**
- Weekly volume/intensity progression
- Deload every 4-6 weeks

**Exercise Selection:**
- Compound movements prioritized
- Balanced push/pull/legs
- Appropriate for equipment level

**Recovery:**
- 48-72 hours between same muscle groups
- Active recovery recommendations

### Program Templates by Goal

**Strength Focus:**
- Rep range: 3-6 reps
- Sets: 3-5 per exercise
- Rest: 2-3 minutes
- Frequency: 3-4x/week

**Endurance Focus:**
- Rep range: 12-20 reps or timed intervals
- Sets: 2-4 per exercise
- Rest: 30-60 seconds
- Frequency: 4-5x/week

**Weight Loss Focus:**
- Circuit training format
- Higher rep ranges (10-15)
- Minimal rest (30-45 seconds)
- HIIT components

**General Fitness:**
- Mixed rep ranges
- Full body approach
- 3x/week balanced

---

## Phase 3: Weekly Routine Generation

### Sample Output Structure

```markdown
## Week 1: Foundation Phase

### Day 1: Upper Body Push
| Exercise | Sets | Reps | Rest | Notes |
|----------|------|------|------|-------|
| Push-ups | 3 | 10-12 | 60s | Modify on knees if needed |
| Pike Press | 3 | 8-10 | 60s | Shoulder focus |
| Diamond Push-ups | 2 | 8-10 | 45s | Tricep emphasis |
| Plank | 3 | 30s | 30s | Core stability |

**Total Time:** ~18 minutes
**Focus:** Chest, shoulders, triceps, core

### Day 2: Lower Body
[Similar table format]

### Day 3: Rest or Active Recovery
- Light walking (15-20 min)
- Stretching routine
- Foam rolling
```

### Rotation Schedule

**4-Week Mesocycle:**
- Week 1-2: Base building (moderate intensity)
- Week 3: Intensification (increased volume/weight)
- Week 4: Deload (reduced volume, maintain intensity)

**Exercise Rotation:**
- Swap variations every 4-6 weeks
- Maintain movement patterns, change exercises
- Prevent adaptation plateaus

---

## Phase 4: Nutrition Guidance

**Note:** General guidance only, not medical/dietary advice.

### Macronutrient Framework

| Goal | Protein | Carbs | Fats |
|------|---------|-------|------|
| Strength | 1.6-2.2g/kg | Moderate-High | 0.8-1g/kg |
| Endurance | 1.2-1.6g/kg | High | Moderate |
| Weight Loss | 1.6-2.0g/kg | Low-Moderate | Moderate |
| General | 1.4-1.8g/kg | Moderate | Moderate |

### Meal Timing Suggestions
- Pre-workout: 1-2 hours before (carbs + protein)
- Post-workout: Within 2 hours (protein + carbs)
- Hydration: 0.5-1oz per pound bodyweight daily

### Simple Meal Templates
- Provide 3-5 meal ideas per goal
- Emphasize whole foods
- Accommodate dietary preferences

---

## Phase 5: Progress Tracking

### Weekly Check-In Format

```markdown
## Progress Review: Week X

### Completed Workouts
| Day | Planned | Completed | Notes |
|-----|---------|-----------|-------|
| Mon | Upper Push | Yes | Increased push-ups to 12 |
| Wed | Lower | Yes | Hip felt tight |
| Fri | Upper Pull | Partial | Cut short (time) |

### Metrics (Optional)
- Body weight: ___
- Energy level: 1-10
- Sleep quality: 1-10
- Soreness level: 1-10

### Adjustments for Next Week
- [Recommendations based on feedback]
```

---

## Output Structure

```
output/health/fitness/{program-name}-{YYYY-MM}/
├── PROGRAM-OVERVIEW.md       # Goals, assessment, schedule
├── WEEKLY-ROUTINE.md         # Current week's workouts
├── EXERCISE-LIBRARY.md       # Exercise descriptions + form cues
├── NUTRITION-GUIDE.md        # Meal templates, macros
├── PROGRESS-TRACKER.md       # Weekly check-ins
└── RESOURCES.md              # References and further reading
```

---

## Visual Elements

### Workout Tables
- Clear exercise/sets/reps/rest format
- Color-coded by muscle group (in rendered markdown)
- Notes column for modifications

### Progress Charts (Markdown)
```
Week 1: ████████░░ 80%
Week 2: █████████░ 90%
Week 3: ██████████ 100%
Week 4: ███████░░░ 70% (deload)
```

### Weekly Schedule Grid
```
        Mon   Tue   Wed   Thu   Fri   Sat   Sun
Week 1  Push  Rest  Pull  Rest  Legs  Active Rest
Week 2  Push  Rest  Pull  Rest  Legs  Active Rest
```

---

## Reference Sources

**Exercise Form & Programming:**
- NSCA (National Strength & Conditioning Association)
- ACSM (American College of Sports Medicine)
- ExRx.net (Exercise Prescription)
- Stronger by Science (evidence-based training)

**Nutrition:**
- Examine.com (supplement/nutrition research)
- Precision Nutrition (practical nutrition)
- ISSN (International Society of Sports Nutrition)

**Recovery:**
- Sleep Foundation
- NASM (National Academy of Sports Medicine)

---

## Disclaimers

**Required in all outputs:**

> This program is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Consult a physician before starting any exercise program, especially if you have pre-existing health conditions. Stop immediately if you experience pain, dizziness, or discomfort.

---

## Integration

**Agent:** advisor
**Invocation:** Detected via keywords (workout, fitness, exercise, training program)
**Model:** sonnet (sufficient for structured program generation)

---

## Examples

### Quick Home Workout Request
```
User: "I need a 20-minute home workout, no equipment, beginner level"

→ Skip full assessment (enough info provided)
→ Generate 3x/week bodyweight program
→ Include warm-up and cool-down
→ Provide exercise modifications
```

### Full Program Design
```
User: "Help me build a strength training program"

→ Run full 7-question assessment
→ Generate 4-6 week periodized program
→ Include nutrition guidance
→ Set up progress tracking
```

---

**Version:** 1.0
**Updated:** 2025-12-18
**Framework:** Intelligence Adjacent (IA)
