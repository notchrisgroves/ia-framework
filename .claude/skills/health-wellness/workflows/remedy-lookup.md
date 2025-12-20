---
name: remedy-lookup
description: Workflow for researching and presenting alternative health remedies
---

# Remedy Lookup Workflow

**Structured process for researching alternative health approaches**

---

## Step 1: Identify Request Type

| Request Pattern | Category | Primary Sources |
|-----------------|----------|-----------------|
| "Homeopathic for X" | Classical Homeopathy | Boiron, Materia Medica |
| "Dr. Reckeweg for X" | Complex Homeopathy | United Remedies R-Guide |
| "Natural remedy for X" | General Alternative | All sources |
| "Earth Clinic / Ted's remedy" | Folk/Traditional | Earth Clinic |
| "Naturopathic approach" | Naturopathy | Whole-body protocols |

---

## Step 2: Research Remedies

### Homeopathic Research

**For Classical (Single Remedy):**
1. Identify key symptoms
2. Match symptom picture to remedy
3. Note modalities (what makes better/worse)
4. Suggest potency based on acuity
5. Provide dosing guidance

**For Complex (Dr. Reckeweg):**
1. Identify condition category
2. Look up R-series number
3. Note indications and contraindications
4. Provide standard dosing

### Naturopathic Research

1. Identify root cause considerations
2. Lifestyle factors (sleep, stress, diet)
3. Supplement support options
4. Herbal considerations
5. Dietary modifications

### Earth Clinic Research

1. Search Ted's remedies for topic
2. Note popular community remedies
3. Include specific protocols (amounts, frequency)
4. Note safety considerations

---

## Step 3: Compile Response

### Required Sections

```markdown
# [Topic] - Alternative Health Reference

> **DISCLAIMER:** This information is for educational purposes only...
[Full disclaimer from SKILL.md]

---

## Condition Overview
[What is it, common causes, conventional understanding]

---

## Homeopathic Options

### Classical Single Remedies

**[Remedy Name] ([Potency])**
- Key indications: [When this remedy fits]
- Symptom picture: [Specific symptoms]
- Modalities: Better from X, Worse from Y
- Dosing: [Frequency and duration]

**[Remedy 2]...**

### Complex Homeopathy (Dr. Reckeweg)

**R[Number] - [Name]**
- Indications: [Uses]
- Composition: [Key ingredients]
- Dosing: [Standard protocol]
- Source: [United Remedies link]

### Boiron Products
[Relevant OTC products if applicable]

---

## Naturopathic Support

### Lifestyle Modifications
- [Sleep considerations]
- [Stress management]
- [Exercise/movement]

### Dietary Considerations
- [Foods to emphasize]
- [Foods to reduce]
- [Specific protocols]

### Supplement Support
| Supplement | Purpose | Notes |
|------------|---------|-------|
| [Name] | [Why] | [Dosing/cautions] |

### Herbal Support
- [Relevant herbs with uses]

---

## Traditional/Folk Remedies

### Earth Clinic Protocols

**[Protocol Name] (Ted's Remedy)**
- Ingredients: [Specific amounts]
- Preparation: [How to prepare]
- Dosing: [How to take, frequency]
- Duration: [How long to use]
- Source: [Earth Clinic link]

**[Additional protocols]**

---

## Safety & Cautions

### When to Seek Medical Care
- [Red flag symptoms]
- [Emergency situations]
- [Conditions requiring professional care]

### Potential Interactions
- [Drug interactions to consider]
- [Supplement interactions]

### Contraindications
- [Who should avoid what]
- [Pregnancy/nursing considerations]

---

## Sources & Further Reading

**Homeopathic:**
- [Boiron USA](https://www.boironusa.com/)
- [Dr. Reckeweg Reference](https://www.unitedremedies.com/pages/dr-reckeweg-reference-guide)
- [KV Lab](https://kvlab.com/)

**Traditional/Alternative:**
- [Earth Clinic - Ted's Remedies](https://ted.earthclinic.com/)
- [God's Universal Antidote](https://godsuniversalantidote.org/)

**Additional Sources:**
- [Relevant books, websites, practitioners]

---

*Educational information only. Consult healthcare professionals before use.*
```

---

## Step 4: Quality Checks

Before delivering response:

- [ ] Disclaimer prominently displayed
- [ ] "When to seek medical care" section included
- [ ] Sources cited for all recommendations
- [ ] Dosing information accurate
- [ ] Safety considerations addressed
- [ ] No claims of "cures" or guaranteed outcomes
- [ ] Language is educational, not prescriptive

---

## Condition Categories

### Quick Reference by System

**Digestive:**
- Homeopathic: Nux vomica, Lycopodium, Carbo veg
- Reckeweg: R5 (Stomach), R7 (Liver), R37 (Colic)
- Earth Clinic: ACV, baking soda, digestive bitters

**Respiratory:**
- Homeopathic: Bryonia, Phosphorus, Antimonium tart
- Reckeweg: R8 (Cough), R9 (Bronchitis), R45 (Larynx)
- Earth Clinic: Hydrogen peroxide, eucalyptus, honey

**Musculoskeletal:**
- Homeopathic: Arnica, Rhus tox, Bryonia, Ruta
- Reckeweg: R11 (Rheumatism), R55 (Injuries)
- Earth Clinic: Borax, DMSO, magnesium

**Sleep/Nervous:**
- Homeopathic: Coffea, Passiflora, Ignatia
- Reckeweg: R14 (Nerve & Sleep), R36 (Nervous diseases)
- Earth Clinic: Magnesium, melatonin protocols

**Immune/Acute:**
- Homeopathic: Oscillococcinum, Gelsemium, Belladonna
- Reckeweg: R1 (Inflammation), R88 (Viral)
- Earth Clinic: Vitamin C, zinc, elderberry

**Skin:**
- Homeopathic: Sulphur, Graphites, Calendula
- Reckeweg: R21 (Skin), R65 (Psoriasis)
- Earth Clinic: ACV topical, tea tree, coconut oil

---

## Emergency Exclusions

**Never provide alternative-only guidance for:**
- Chest pain / heart attack symptoms
- Stroke symptoms (FAST)
- Difficulty breathing / anaphylaxis
- Severe bleeding or trauma
- High fever in infants
- Suicidal ideation
- Diabetic emergencies
- Severe allergic reactions

**Response:** Immediate referral to emergency services + supportive information only.

---

**Model:** sonnet
**Output:** `output/health/wellness/{topic}-{YYYY-MM-DD}.md`
