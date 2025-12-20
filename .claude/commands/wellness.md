---
name: wellness
description: Alternative and complementary health reference with homeopathic, naturopathic, and holistic wellness guidance
---

# /wellness - Alternative Health Reference

Alternative and complementary health information combining homeopathic, naturopathic, and holistic approaches.

**Agent:** advisor
**Skill:** health-wellness
**Output:** `output/health/wellness/{topic}-{YYYY-MM-DD}.md`

---

## CRITICAL DISCLAIMER

> **THIS IS NOT MEDICAL ADVICE.** This provides educational information about alternative health approaches. It is NOT a substitute for professional medical diagnosis, treatment, or advice. Always consult qualified healthcare providers. In emergencies, call 911.

---

## Quick Start

```
/wellness natural remedies for sleep
```

**Examples:**
```
/wellness homeopathic remedy for bruising
/wellness Earth Clinic remedies for acid reflux
/wellness Dr. Reckeweg for joint pain
/wellness naturopathic approach to stress
```

---

## When to Use

**Use /wellness when:**
- Researching homeopathic remedies (Boiron, Reckeweg)
- Looking up Earth Clinic / Ted's remedies
- Exploring naturopathic approaches
- Understanding alternative health protocols

**Don't use if:**
- Medical emergency (call 911)
- Need diagnosis for symptoms (see doctor)
- Replacing prescribed medications (consult doctor)
- Serious or worsening symptoms

---

## Modes

| Request Type | Mode | Focus |
|--------------|------|-------|
| "Homeopathic remedy for X" | Homeopathy | Classical/complex homeopathy |
| "Natural remedy for X" | General Wellness | Multi-modality overview |
| "Earth Clinic remedy" | Folk/Traditional | Community remedies (Ted's) |
| "Dr. Reckeweg for X" | German Homeopathy | R-series formulas |
| "Naturopathic approach" | Naturopathy | Whole-body healing |

---

## Reference Sources

**Homeopathic:**
- Boiron USA (boironusa.com) - OTC homeopathic products
- Dr. Reckeweg (unitedremedies.com) - German complex formulas
- KV Lab (kvlab.com) - Professional-grade remedies

**Alternative:**
- Earth Clinic / Ted's Remedies (ted.earthclinic.com)
- Community-sourced protocols (ACV, borax, alkalizing)

**Naturopathic:**
- Six Principles of Naturopathy
- Foundational support (sleep, nutrition, movement, stress)

---

## Web Search Integration

**For current information:**
- Latest research on remedies and supplements
- Updated protocols and dosing
- New product formulations
- Safety updates and interactions
- Clinical studies and evidence

**Search approach:**
- Verify claims with current sources
- Check for interaction warnings
- Find practitioner recommendations
- Locate quality suppliers

---

## Output Format

Every response includes:
1. **Disclaimer** (prominent)
2. **Homeopathic approaches** (classical + complex)
3. **Naturopathic support** (lifestyle, supplements)
4. **Traditional remedies** (if applicable)
5. **When to seek medical care**
6. **Source citations**

---

## Agent Routing

```typescript
Task({
  subagent_type: "advisor",
  model: "sonnet",
  prompt: `
Mode: wellness
Skill: health-wellness

Query: {user query}

Instructions:
1. Include MANDATORY disclaimer
2. Research applicable remedies
3. Provide source citations
4. Include "when to see doctor" section
5. Web search for current information

Output: output/health/wellness/{topic}-{YYYY-MM-DD}.md
`
})
```

---

## Safety Guidelines

**Always refer to doctor for:**
- Chest pain or difficulty breathing
- Severe or worsening symptoms
- High fever (>103°F adults)
- Symptoms in infants/young children
- Pregnancy-related concerns
- Mental health emergencies

**Interaction cautions:**
- Research herb-drug interactions
- Inform doctors of all supplements
- Start low, go slow with new remedies

---

## Related Commands

- `/training` - Fitness programming

---

**Version:** 1.0
**Last Updated:** 2025-12-19
**Framework:** Intelligence Adjacent (IA)
